"""Controles estadísticos de sobreajuste y pruebas múltiples.

Supuestos y limitaciones:

* Sharpe probabilístico (PSR) y deflactado (DSR) de Bailey y López de Prado (2012, 2014):
  asumen retornos estacionarios y aproximadamente independientes; se corrigen por asimetría
  y curtosis pero no por autocorrelación. El DSR usa el número de configuraciones probadas y
  la varianza de sus Sharpe para estimar el Sharpe máximo esperado por azar.
* p-valores de la expectativa por operación: aproximación normal del estadístico t
  (válida para muestras grandes; con < 30 operaciones se marca como poco fiable).
* Holm-Bonferroni controla la tasa de error familiar sin asumir independencia.
* Bootstrap i.i.d. de operaciones (semilla fija): ignora dependencia temporal.
"""

from __future__ import annotations

import math
from statistics import NormalDist
from typing import Any

import numpy as np
import pandas as pd

EULER_GAMMA = 0.5772156649015329
_N = NormalDist()


def _moments(returns: pd.Series) -> tuple[float, float, float, int]:
    r = returns.dropna().to_numpy(float)
    n = len(r)
    if n < 3 or r.std(ddof=1) == 0:
        return float("nan"), 0.0, 3.0, n
    sr = float(r.mean() / r.std(ddof=1))
    z = (r - r.mean()) / r.std(ddof=0)
    return sr, float(np.mean(z**3)), float(np.mean(z**4)), n


def probabilistic_sharpe(returns: pd.Series, benchmark_sr: float = 0.0) -> float | None:
    """P(SR verdadero > ``benchmark_sr``) con SR no anualizado por vela."""
    sr, skew, kurt, n = _moments(returns)
    if math.isnan(sr) or n < 3:
        return None
    denom = 1 - skew * sr + (kurt - 1) / 4 * sr**2
    if denom <= 0:
        return None
    return _N.cdf((sr - benchmark_sr) * math.sqrt(n - 1) / math.sqrt(denom))


def expected_max_sharpe(n_trials: int, sr_variance: float) -> float:
    """Sharpe máximo esperado bajo la hipótesis nula entre ``n_trials`` pruebas."""
    if n_trials <= 1 or sr_variance <= 0:
        return 0.0
    a = _N.inv_cdf(1 - 1 / n_trials)
    b = _N.inv_cdf(1 - 1 / (n_trials * math.e))
    return math.sqrt(sr_variance) * ((1 - EULER_GAMMA) * a + EULER_GAMMA * b)


def deflated_sharpe(
    returns: pd.Series, n_trials: int, trial_sharpes: list[float] | None = None
) -> dict[str, Any]:
    """Deflated Sharpe Ratio. ``trial_sharpes``: Sharpe no anualizados de todas las pruebas."""
    valid = [s for s in (trial_sharpes or []) if s is not None and math.isfinite(s)]
    var = float(np.var(valid, ddof=1)) if len(valid) > 1 else 0.0
    sr0 = expected_max_sharpe(n_trials, var)
    return {
        "n_trials": n_trials,
        "trial_sharpe_variance": var,
        "expected_max_sharpe_null": sr0,
        "dsr": probabilistic_sharpe(returns, sr0),
        "psr_vs_zero": probabilistic_sharpe(returns, 0.0),
    }


def mean_pvalue(values: pd.Series) -> tuple[float | None, bool]:
    """p-valor unilateral (H0: media <= 0) con aproximación normal. Devuelve (p, fiable)."""
    v = values.dropna().to_numpy(float)
    if len(v) < 2 or v.std(ddof=1) == 0:
        return None, False
    t = v.mean() / (v.std(ddof=1) / math.sqrt(len(v)))
    return 1 - _N.cdf(t), len(v) >= 30


def holm_bonferroni(pvalues: dict[str, float | None], alpha: float = 0.05) -> dict[str, dict]:
    """Ajuste de Holm. Devuelve p ajustado y si se rechaza H0 por hipótesis."""
    items = sorted(((k, p) for k, p in pvalues.items() if p is not None), key=lambda x: x[1])
    m = len(items)
    out: dict[str, dict] = {k: {"p": None, "p_adj": None, "reject": False} for k in pvalues}
    running = 0.0
    still = True
    for i, (k, p) in enumerate(items):
        adj = min(1.0, max(running, (m - i) * p))
        running = adj
        still = still and adj <= alpha
        out[k] = {"p": p, "p_adj": adj, "reject": still}
    return out


def bootstrap_mean_ci(
    values: pd.Series, n_samples: int = 1000, seed: int = 42, level: float = 0.95
) -> tuple[float, float] | None:
    """Intervalo bootstrap percentil para la media (p. ej., PnL neto por operación)."""
    v = values.dropna().to_numpy(float)
    if len(v) < 5:
        return None
    rng = np.random.default_rng(seed)
    means = rng.choice(v, size=(n_samples, len(v)), replace=True).mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, 1 - (1 - level) / 2])
    return float(lo), float(hi)


def top_trade_dependence(trades: pd.DataFrame, k: int = 3) -> dict[str, Any]:
    """Cuánto depende el resultado de las ``k`` mejores operaciones (y del 5 % superior)."""
    if trades.empty:
        return {"net": 0.0, "net_without_top_k": 0.0, "top_k_share": None, "k": k}
    net = trades["net_pnl"].astype(float).sort_values(ascending=False)
    total = float(net.sum())
    top = float(net.head(k).sum())
    n5 = max(1, math.ceil(len(net) * 0.05))
    return {
        "k": k,
        "net": total,
        "net_without_top_k": total - top,
        "top_k_share": top / total if total > 0 else None,
        "net_without_top_5pct": total - float(net.head(n5).sum()),
        "sign_flips_without_top_k": total > 0 >= total - top,
    }
