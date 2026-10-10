"""Redundancia entre señales: correlación, coincidencia y selección de estrategias no redundantes.

Estas medidas deben calcularse **en el período de entrenamiento** cuando se usan para decidir
qué estrategias entran en una combinación.
"""

from __future__ import annotations

import pandas as pd


def signal_correlation(signals: pd.DataFrame) -> pd.DataFrame:
    """Correlación de Pearson entre series de estado (-1/0/1). Columnas constantes -> NaN."""
    return signals.astype(float).corr()


def signal_agreement(signals: pd.DataFrame) -> pd.DataFrame:
    """Proporción de velas con la misma dirección entre las velas en que ambas están activas."""
    names = list(signals.columns)
    out = pd.DataFrame(index=names, columns=names, dtype=float)
    for a in names:
        for b in names:
            both = (signals[a] != 0) & (signals[b] != 0)
            out.loc[a, b] = (
                float((signals[a][both] == signals[b][both]).mean()) if both.any() else float("nan")
            )
    return out


def select_non_redundant(
    corr: pd.DataFrame, threshold: float = 0.7, priority: list[str] | None = None
) -> tuple[list[str], dict[str, str]]:
    """Selección voraz: recorre ``priority`` y descarta las que superan ``|corr| > threshold``
    con alguna ya seleccionada. Devuelve (seleccionadas, {descartada: correlacionada_con})."""
    order = priority or list(corr.columns)
    values = corr.astype(float).fillna(0.0).to_numpy()
    pos = {str(c): i for i, c in enumerate(corr.columns)}
    kept: list[str] = []
    dropped: dict[str, str] = {}
    for name in order:
        clash = next((k for k in kept if abs(float(values[pos[name], pos[k]])) > threshold), None)
        if clash is None:
            kept.append(name)
        else:
            dropped[name] = clash
    return kept, dropped
