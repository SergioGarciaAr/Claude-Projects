"""Combinación de señales de varias estrategias.

Entrada: un DataFrame de señales normalizadas por estrategia (mismo índice). Cada estrategia
emite su **estado** objetivo (-1/0/1); la combinación produce un nuevo estado objetivo con el
mismo contrato, de modo que el motor no distingue entre estrategia individual y combinación.

Modos:

``simple_vote``
    ``net = n_long - n_short``. LONG si ``net >= min_margin``; SHORT si ``net <= -min_margin``.
``weighted_vote``
    ``score = sum(w_i * s_i * c_i) / sum(w_i)`` (``c_i`` = convicción si ``use_conviction``,
    si no 1). LONG si ``score >= threshold``; SHORT si ``score <= -threshold``. Los pesos son
    configurables o se ajustan **solo** con datos de entrenamiento (``fit_weights``); un peso
    mayor no implica mayor capacidad predictiva.
``min_consensus``
    LONG si ``n_long >= min_votes`` (y SHORT análogo).
``category_consensus``
    Una categoría vota LONG si su voto neto interno es > 0. LONG si al menos ``min_categories``
    categorías distintas votan LONG.

Política de conflictos (``conflict_policy``): ``veto`` -> cualquier voto opuesto anula la señal
(FLAT); ``net`` -> se usa el resultado neto del modo. Las estrategias en FLAT o sin datos
(NaN) se consideran abstenciones.

Filtro de régimen (``regime_rules``): antes de votar, la señal de una estrategia se fuerza a
FLAT en las velas cuyo régimen no esté permitido. Reglas por nombre de estrategia, por
categoría o comodín ``*``; cada regla mapea dimensión -> valores permitidos.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field

from bybit_quant_lab.strategies.base import SIGNAL_COLUMNS, empty_signal_frame


class CombinationConfig(BaseModel):
    """Configuración de una combinación."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = "combo"
    mode: Literal["simple_vote", "weighted_vote", "min_consensus", "category_consensus"] = (
        "simple_vote"
    )
    members: list[str] | None = None
    min_margin: int = Field(2, ge=1)
    min_votes: int = Field(2, ge=1)
    min_categories: int = Field(2, ge=1)
    weights: dict[str, float] | None = None
    threshold: float = Field(0.3, gt=0, le=1)
    use_conviction: bool = False
    conflict_policy: Literal["veto", "net"] = "veto"
    regime_rules: dict[str, dict[str, list[str]]] | None = None


def apply_regime_filter(
    signals: pd.DataFrame,
    categories: dict[str, str],
    regime: pd.DataFrame,
    rules: dict[str, dict[str, list[str]]],
) -> pd.DataFrame:
    """Fuerza a 0 las señales de cada estrategia fuera de sus regímenes permitidos."""
    out = signals.copy()
    reg = regime.reindex(signals.index)
    for name in out.columns:
        allowed = pd.Series(True, index=out.index)
        for key in ("*", categories.get(name, ""), name):
            for dim, values in (rules.get(key) or {}).items():
                if dim not in reg.columns:
                    raise ValueError(f"Dimensión de régimen desconocida: {dim}")
                allowed &= reg[dim].isin(values)
        out.loc[~allowed, name] = 0
    return out


def _stack(frames: dict[str, pd.DataFrame], column: str, index: pd.Index) -> pd.DataFrame:
    return pd.DataFrame({n: f[column].reindex(index) for n, f in frames.items()}, index=index)


def combine_signals(
    frames: dict[str, pd.DataFrame],
    categories: dict[str, str],
    config: CombinationConfig,
    regime: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Combina señales individuales en un DataFrame con el contrato ``SIGNAL_COLUMNS``."""
    members = config.members or list(frames)
    missing = [m for m in members if m not in frames]
    if missing:
        raise KeyError(f"Estrategias no disponibles para la combinación: {missing}")
    if not members:
        raise ValueError("La combinación necesita al menos una estrategia")
    use = {m: frames[m] for m in members}
    index = next(iter(use.values())).index
    sig = _stack(use, "signal", index).fillna(0).astype(int)
    if config.regime_rules:
        if regime is None:
            raise ValueError("regime_rules requiere el DataFrame de régimen")
        sig = apply_regime_filter(sig, categories, regime, config.regime_rules)
    conv = _stack(use, "conviction", index).fillna(0.0)
    n_long = (sig > 0).sum(axis=1)
    n_short = (sig < 0).sum(axis=1)
    n = len(members)

    if config.mode == "simple_vote":
        net = n_long - n_short
        out = np.where(net >= config.min_margin, 1, np.where(net <= -config.min_margin, -1, 0))
        strength = net.abs() / n
    elif config.mode == "weighted_vote":
        w = pd.Series({m: (config.weights or {}).get(m, 1.0) for m in members}, dtype=float)
        if (w < 0).any() or w.sum() <= 0:
            raise ValueError("Los pesos deben ser no negativos y sumar > 0")
        factor = conv if config.use_conviction else pd.DataFrame(1.0, index=index, columns=members)
        score = (sig * factor).mul(w, axis=1).sum(axis=1) / w.sum()
        out = np.where(score >= config.threshold, 1, np.where(score <= -config.threshold, -1, 0))
        strength = score.abs()
    elif config.mode == "min_consensus":
        long_ok, short_ok = n_long >= config.min_votes, n_short >= config.min_votes
        out = np.where(long_ok & ~short_ok, 1, np.where(short_ok & ~long_ok, -1, 0))
        strength = pd.Series(np.maximum(n_long, n_short) / n, index=index)
    else:
        cats = pd.Series({m: categories.get(m, m) for m in members})
        cat_net = sig.T.groupby(cats).sum().T
        c_long, c_short = (cat_net > 0).sum(axis=1), (cat_net < 0).sum(axis=1)
        long_ok = c_long >= config.min_categories
        short_ok = c_short >= config.min_categories
        out = np.where(long_ok & ~short_ok, 1, np.where(short_ok & ~long_ok, -1, 0))
        strength = pd.Series(np.maximum(c_long, c_short) / max(cats.nunique(), 1), index=index)

    out_s = pd.Series(out, index=index).astype("int64")
    if config.conflict_policy == "veto":
        conflict = ((out_s > 0) & (n_short > 0)) | ((out_s < 0) & (n_long > 0))
        out_s[conflict] = 0
    result = empty_signal_frame(index)
    result["signal"] = out_s
    result["conviction"] = pd.Series(strength, index=index).clip(0, 1).where(out_s != 0, 0.0)
    for col in SIGNAL_COLUMNS[2:]:
        values = _stack(use, col, index)
        agree = sig.eq(out_s, axis=0) & (out_s != 0).to_numpy()[:, None]
        result[col] = values.where(agree).median(axis=1, skipna=True)
    no_stop = result["stop_distance"].isna() | (result["stop_distance"] <= 0)
    result.loc[no_stop, "signal"] = 0
    result.loc[result["signal"] == 0, "conviction"] = 0.0
    return result


def fit_weights(
    train_returns: dict[str, pd.Series], method: Literal["equal", "train_sharpe"] = "train_sharpe"
) -> dict[str, float]:
    """Ajusta pesos con retornos por vela del período de **entrenamiento** exclusivamente.

    ``train_sharpe``: peso = max(Sharpe no anualizado, 0); si todos son 0 se usan pesos iguales.
    """
    if method == "equal":
        return dict.fromkeys(train_returns, 1.0)
    weights = {}
    for name, r in train_returns.items():
        std = float(r.std(ddof=1)) if len(r) > 1 else 0.0
        weights[name] = max(float(r.mean()) / std, 0.0) if std > 0 else 0.0
    total = sum(weights.values())
    if total <= 0:
        return dict.fromkeys(train_returns, 1.0)
    return {k: v / total for k, v in weights.items()}
