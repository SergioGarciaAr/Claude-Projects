"""Cálculo de métricas. Fórmulas y convenciones (ver ``docs/metrics.md``):

* Retornos por vela: ``r_t = E_t / E_{t-1} - 1`` sobre la equity al cierre, incluyendo las
  velas sin posición (retorno 0). El primer retorno usa el capital inicial como ``E_{-1}``.
* Anualización: mercado 24/7, año de 365 días -> ``N = 525600 / minutos_por_vela``.
* Sharpe = ``mean(r) / std(r, ddof=1) * sqrt(N)`` con tasa libre de riesgo 0.
* Sortino = ``mean(r) / DD * sqrt(N)`` con ``DD = sqrt(mean(min(r, 0)^2))``.
* CAGR = ``(E_final / E_0)^(365 / días) - 1`` solo si ``días >= min_days_for_cagr``.
* Profit factor = suma de ganancias netas / |suma de pérdidas netas|.
* Expectativa = media del PnL neto por operación.
* Exposición = fracción de velas con posición abierta al cierre.
* Rotación = nocional negociado total / equity media.

Las métricas que no pueden calcularse válidamente se devuelven como ``None`` y se añade una
advertencia. Una muestra pequeña de operaciones también genera advertencia.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

from bybit_quant_lab.backtesting.results import BacktestResult
from bybit_quant_lab.timeframes import bars_per_year

MIN_BARS_FOR_RATIOS = 30


def bar_returns(equity: pd.Series, initial: float) -> pd.Series:
    """Retornos simples por vela, empezando desde el capital inicial."""
    prev = equity.shift(1)
    prev.iloc[0] = initial
    return equity / prev - 1


def drawdown_stats(equity: pd.Series) -> dict[str, Any]:
    """Drawdown máximo, duración máxima (velas) y velas de recuperación del máximo drawdown."""
    if equity.empty:
        return {
            "max_drawdown": 0.0,
            "max_dd_duration_bars": 0,
            "max_dd_recovery_bars": None,
            "max_dd_start": None,
            "max_dd_trough": None,
            "max_dd_end": None,
        }
    values = equity.to_numpy(float)
    peak = np.maximum.accumulate(values)
    dd = values / peak - 1
    trough = int(np.argmin(dd))
    peak_idx = int(np.argmax(values[: trough + 1])) if trough > 0 else 0
    rec = np.nonzero(values[trough:] >= peak[trough])[0]
    recovery = int(rec[0]) if len(rec) else None
    longest, cur = 0, 0
    for under in dd < 0:
        cur = cur + 1 if under else 0
        longest = max(longest, cur)
    idx = equity.index
    return {
        "max_drawdown": float(-np.min(dd)),
        "max_dd_duration_bars": longest,
        "max_dd_recovery_bars": recovery,
        "max_dd_start": str(idx[peak_idx]),
        "max_dd_trough": str(idx[trough]),
        "max_dd_end": str(idx[trough + recovery]) if recovery is not None else None,
    }


def _safe(x: float) -> float | None:
    return None if x is None or not math.isfinite(x) else float(x)


def compute_metrics(
    result: BacktestResult, min_trades: int = 30, min_days_for_cagr: int = 180
) -> dict[str, Any]:
    """Calcula el conjunto de métricas de un ``BacktestResult``."""
    warnings: list[str] = []
    eq = result.equity["equity"]
    init = result.initial_capital
    final = float(eq.iloc[-1]) if len(eq) else init
    trades = result.trades
    n_trades = len(trades)
    rets = bar_returns(eq, init) if len(eq) else pd.Series(dtype=float)
    n_bars = len(rets)
    ann = bars_per_year(result.timeframe)
    days = (n_bars * (525600 / ann)) / 1440 if n_bars else 0.0

    sharpe = sortino = None
    if n_bars >= MIN_BARS_FOR_RATIOS:
        std = float(rets.std(ddof=1))
        if std > 0:
            sharpe = float(rets.mean() / std * math.sqrt(ann))
        downside = float(np.sqrt(np.mean(np.minimum(rets.to_numpy(), 0.0) ** 2)))
        if downside > 0:
            sortino = float(rets.mean() / downside * math.sqrt(ann))
    else:
        warnings.append(f"Menos de {MIN_BARS_FOR_RATIOS} velas: Sharpe/Sortino no calculados.")
    cagr = None
    if days >= min_days_for_cagr and final > 0:
        cagr = (final / init) ** (365.0 / days) - 1
    else:
        warnings.append(f"Período de {days:.0f} días < {min_days_for_cagr}: CAGR no calculado.")
    if n_trades < min_trades:
        warnings.append(
            f"Solo {n_trades} operaciones (< {min_trades}): las métricas por operación tienen "
            "alta incertidumbre estadística."
        )

    net = trades["net_pnl"].astype(float) if n_trades else pd.Series(dtype=float)
    wins, losses = net[net > 0], net[net < 0]
    gross_win, gross_loss = float(wins.sum()), float(-losses.sum())
    dd = drawdown_stats(eq)
    gross_total = float(trades["gross_pnl"].sum()) if n_trades else 0.0
    m: dict[str, Any] = {
        "label": result.label,
        "symbol": result.symbol,
        "timeframe": result.timeframe,
        "start": str(result.start) if result.start is not None else None,
        "end": str(result.end) if result.end is not None else None,
        "bars": n_bars,
        "days": round(days, 2),
        "initial_capital": init,
        "final_equity": final,
        "net_profit": final - init,
        "net_profit_pct": final / init - 1,
        "gross_profit_before_costs": gross_total,
        "cumulative_return": final / init - 1,
        "cagr": _safe(cagr) if cagr is not None else None,
        "sharpe": _safe(sharpe) if sharpe is not None else None,
        "sortino": _safe(sortino) if sortino is not None else None,
        **dd,
        "num_trades": n_trades,
        "win_rate": float((net > 0).mean()) if n_trades else None,
        "avg_win": float(wins.mean()) if len(wins) else None,
        "avg_loss": float(losses.mean()) if len(losses) else None,
        "profit_factor": (gross_win / gross_loss) if gross_loss > 0 else None,
        "expectancy": float(net.mean()) if n_trades else None,
        "expectancy_pct_equity": float(trades["return_on_equity"].mean()) if n_trades else None,
        "exposure": float(result.equity["in_position"].mean()) if n_bars else 0.0,
        "turnover": result.totals["traded_notional"] / float(eq.mean()) if n_bars else 0.0,
        "total_fees": result.totals["fees"],
        "total_slippage": result.totals["slippage"],
        "total_costs": result.totals["fees"] + result.totals["slippage"],
        "total_funding": result.totals["funding"],
        "funding_applied": result.funding_applied,
        "avg_bars_in_trade": float(trades["bars_held"].mean()) if n_trades else None,
        "long_trades": int((trades["side"] == "LONG").sum()) if n_trades else 0,
        "short_trades": int((trades["side"] == "SHORT").sum()) if n_trades else 0,
        "rejected_signals": len(result.rejected_signals),
        "risk_events": len(result.risk_events),
        "warnings": warnings + list(result.warnings),
    }
    if m["profit_factor"] is None and n_trades:
        m["warnings"].append("Sin operaciones perdedoras: profit factor no definido.")
    return m
