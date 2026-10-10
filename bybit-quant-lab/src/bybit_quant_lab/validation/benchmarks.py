"""Benchmarks: buy-and-hold, efectivo (referencia neutral) y entradas aleatorias.

* ``buy_and_hold``: compra 1x el capital (sin apalancamiento) en la primera apertura del
  segmento con comisión y slippage, y vende al cierre final con los mismos costes.
* ``cash``: equity constante (retorno 0). Referencia neutral para estrategias long/short.
* ``random_entries``: estados aleatorios (semilla fija) con la misma fracción de velas activas
  y duración media similar a la estrategia evaluada, simulados con el mismo motor, stops y
  costes. Sirve para medir si la estrategia supera a la aleatoriedad con igual exposición.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bybit_quant_lab.backtesting.engine import BacktestEngine
from bybit_quant_lab.backtesting.results import BacktestResult
from bybit_quant_lab.config.models import AppConfig
from bybit_quant_lab.execution.costs import CostModel
from bybit_quant_lab.validation.splits import Segment


def _empty_trades() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "net_pnl",
            "gross_pnl",
            "fees",
            "funding",
            "side",
            "bars_held",
            "return_on_equity",
            "exit_reason",
        ]
    )


def buy_and_hold(
    data: pd.DataFrame, config: AppConfig, segment: Segment, symbol: str, timeframe: str
) -> BacktestResult:
    """Benchmark de compra y mantenimiento 1x."""
    seg = data.iloc[segment.start_pos : segment.end_pos + 1]
    costs = CostModel.from_config(config.costs)
    cap = config.backtest.initial_capital
    entry = costs.fill_price(float(seg["open"].iloc[0]), 1)
    qty = cap / (entry * (1 + costs.taker_fee))
    entry_fee = costs.fee(qty * entry)
    cash = cap - entry_fee
    equity = cash + qty * (seg["close"] - entry)
    exit_fill = costs.fill_price(float(seg["close"].iloc[-1]), -1)
    exit_fee = costs.fee(qty * exit_fill)
    final = cash + qty * (exit_fill - entry) - exit_fee
    equity.iloc[-1] = final
    eq = pd.DataFrame(
        {
            "equity": equity,
            "cash": cash,
            "unrealized": equity - cash,
            "position": qty,
            "margin_used": qty * entry,
            "in_position": True,
        }
    )
    eq["drawdown"] = eq["equity"] / eq["equity"].cummax() - 1
    gross = qty * (float(seg["close"].iloc[-1]) - float(seg["open"].iloc[0]))
    trades = pd.DataFrame(
        [
            {
                "net_pnl": final - cap,
                "gross_pnl": gross,
                "fees": entry_fee + exit_fee,
                "funding": 0.0,
                "side": "LONG",
                "bars_held": len(seg),
                "return_on_equity": final / cap - 1,
                "exit_reason": "end_of_data",
            }
        ]
    )
    return BacktestResult(
        label="benchmark_buy_and_hold",
        symbol=symbol,
        timeframe=timeframe,
        initial_capital=cap,
        equity=eq,
        trades=trades,
        risk_events=[],
        rejected_signals=[],
        totals={
            "fees": entry_fee + exit_fee,
            "slippage": qty * (entry - float(seg["open"].iloc[0]))
            + qty * (float(seg["close"].iloc[-1]) - exit_fill),
            "funding": 0.0,
            "traded_notional": qty * (entry + exit_fill),
        },
        funding_applied=False,
        warnings=["Buy-and-hold sin funding: un largo perpetuo pagaría/cobraría funding."],
    )


def cash_benchmark(
    data: pd.DataFrame, config: AppConfig, segment: Segment, symbol: str, timeframe: str
) -> BacktestResult:
    """Referencia neutral: sin posición, retorno 0."""
    idx = data.index[segment.start_pos : segment.end_pos + 1]
    cap = config.backtest.initial_capital
    eq = pd.DataFrame(
        {
            "equity": cap,
            "cash": cap,
            "unrealized": 0.0,
            "position": 0.0,
            "margin_used": 0.0,
            "in_position": False,
            "drawdown": 0.0,
        },
        index=idx,
    )
    return BacktestResult(
        label="benchmark_cash",
        symbol=symbol,
        timeframe=timeframe,
        initial_capital=cap,
        equity=eq,
        trades=_empty_trades(),
        risk_events=[],
        rejected_signals=[],
        totals={"fees": 0.0, "slippage": 0.0, "funding": 0.0, "traded_notional": 0.0},
        funding_applied=False,
    )


def random_signals(reference: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Señales aleatorias con exposición y duración media similares a ``reference``."""
    rng = np.random.default_rng(seed)
    sig = reference["signal"].to_numpy()
    n = len(sig)
    active = sig != 0
    starts = int(np.sum(active[1:] & (sig[1:] != sig[:-1]))) + int(active[0]) if n else 0
    avg_len = max(int(active.sum() / starts), 1) if starts else 1
    out = np.zeros(n, dtype=np.int64)
    p_start = starts / max(n - active.sum(), 1)
    i = 0
    while i < n:
        if rng.random() < p_start:
            length = max(1, int(rng.exponential(avg_len)))
            out[i : i + length] = rng.choice([-1, 1])
            i += length + 1
        else:
            i += 1
    frame = reference.copy()
    frame["signal"] = out
    frame["conviction"] = np.where(out != 0, 0.5, 0.0)
    return frame


def random_benchmark(
    data: pd.DataFrame,
    reference_signals: pd.DataFrame,
    config: AppConfig,
    segment: Segment,
    symbol: str,
    timeframe: str,
    seed: int,
    funding: pd.Series | None = None,
) -> BacktestResult:
    """Simula entradas aleatorias (semilla fija) con el mismo motor y gestión de salidas."""
    sig = random_signals(reference_signals, seed)
    res = BacktestEngine(config, symbol, timeframe).run(
        data,
        sig,
        funding=funding,
        start=segment.start,
        end=segment.end,
        label=f"benchmark_random_seed{seed}",
    )
    return res
