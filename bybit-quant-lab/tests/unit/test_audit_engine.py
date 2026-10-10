"""Auditoría del motor: operaciones verificadas a mano y casos límite.

Cada prueba calcula el resultado esperado de forma independiente (aritmética explícita) y lo
compara con el motor. Ver docs/audit_report.md.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from bybit_quant_lab.analytics import compute_metrics
from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.backtesting.results import BacktestResult
from bybit_quant_lab.config import AppConfig
from bybit_quant_lab.risk.instruments import InstrumentSpec
from tests.conftest import make_bars, manual_signals, zero_cost_config

SPEC = InstrumentSpec(
    "TEST", tick_size=0.01, qty_step=0.001, min_qty=0.001, max_qty=1e9, min_notional=0.0
)


def _cfg(
    fee: float = 0.0,
    slip_bps: float = 0.0,
    leverage: float = 10.0,
    liquidation: bool = False,
    **risk: object,
) -> AppConfig:
    cfg = zero_cost_config(**risk)
    return cfg.model_copy(
        update={
            "costs": cfg.costs.model_copy(update={"taker_fee": fee, "slippage_bps": slip_bps}),
            "execution": cfg.execution.model_copy(
                update={"leverage": leverage, "simulate_liquidation": liquidation}
            ),
        }
    )


def _floor_qty(q: float, step: float = 0.001) -> float:
    return math.floor(q / step + 1e-9) * step


def test_short_trade_with_fees_slippage_and_funding_by_hand() -> None:
    # Velas: open[t] = close[t-1]. Señal SHORT al cierre de la vela 1, FLAT al cierre de la 3.
    df = make_bars([100, 100, 100, 95, 90, 90], spread=0.1)
    sig = manual_signals(df.index, {1: -1, 3: 0}, stop=20)
    fee, slip = 0.001, 0.001
    funding = pd.Series([0.0005], index=[df.index[3]])  # pago a las 03:00, posición abierta
    res = run_backtest(df, sig, _cfg(fee, 10.0), "TEST", "1h", spec=SPEC, funding=funding)
    t = res.trades.iloc[0]

    entry_ref, exit_ref = 100.0, 95.0  # open[2] y open[4]
    entry_fill = entry_ref * (1 - slip)  # venta: precio peor = más bajo
    exit_fill = exit_ref * (1 + slip)  # recompra: precio peor = más alto
    qty = _floor_qty(10_000 * 0.01 / (20 + entry_fill * 2 * (fee + slip)))
    fees = fee * qty * (entry_fill + exit_fill)
    funding_paid = -1 * qty * 100.0 * 0.0005  # el corto cobra con tasa positiva
    net = (entry_fill - exit_fill) * qty - fees - funding_paid

    assert t["side"] == "SHORT" and t["qty"] == pytest.approx(qty)
    assert t["entry_time"] == df.index[2] and t["exit_time"] == df.index[4]
    assert t["entry_price"] == pytest.approx(entry_fill)
    assert t["exit_price"] == pytest.approx(exit_fill)
    assert t["fees"] == pytest.approx(fees)
    assert t["funding"] == pytest.approx(funding_paid) and t["funding"] < 0
    assert t["gross_pnl"] == pytest.approx((entry_ref - exit_ref) * qty)
    assert t["slippage_cost"] == pytest.approx(
        qty * (entry_ref - entry_fill + exit_fill - exit_ref)
    )
    assert t["net_pnl"] == pytest.approx(net)
    assert t["net_pnl"] == pytest.approx(
        t["gross_pnl"] - t["fees"] - t["slippage_cost"] - t["funding"]
    )
    assert res.final_equity == pytest.approx(10_000 + net)
    assert res.totals["funding"] == pytest.approx(funding_paid)


def test_long_sizing_margin_and_liquidation_price_by_hand() -> None:
    df = make_bars([200.0] * 8, spread=0.1)
    sig = manual_signals(df.index, {1: 1}, stop=10)
    cfg = AppConfig.model_validate(
        {
            "costs": {"taker_fee": 0.00055, "slippage_bps": 2.0},
            "execution": {"leverage": 3.0, "simulate_liquidation": True},
            "risk": {"max_symbol_exposure": 3.0, "max_leverage": 5.0, "margin_reserve": 0.2},
        }
    )
    res = run_backtest(df, sig, cfg, "TEST", "1h", spec=SPEC)
    fill = 200 * (1 + 2e-4)
    raw = 10_000 * 0.01 / (10 + fill * 2 * (0.00055 + 2e-4))
    caps = [10_000 * 3.0 / fill, 10_000 * 5.0 / fill, 10_000 * 0.8 * 3.0 / fill]
    qty = _floor_qty(min(raw, *caps))
    row = res.equity.iloc[2]  # vela de entrada
    assert row["position"] == pytest.approx(qty)
    assert row["margin_used"] == pytest.approx(qty * fill / 3.0)
    # El stop no está más allá de la liquidación: liq = fill * (1 - 1/3 + 0.005)
    assert fill - 10 > fill * (1 - 1 / 3 + 0.005)


def test_gap_through_liquidation_loses_isolated_margin_only() -> None:
    # Largo a 100 con apalancamiento 10: liquidación ~90.5, stop en 92. La vela siguiente
    # abre en 80 (gap por debajo de ambos). Con margen aislado la pérdida máxima es el margen.
    df = make_bars([100, 100, 100, 100, 80, 80], spread=0.1)
    df.loc[df.index[4], ["open", "high", "low"]] = [80.0, 80.5, 79.5]
    sig = manual_signals(df.index, {1: 1}, stop=8)
    res = run_backtest(df, sig, _cfg(leverage=10.0, liquidation=True), "TEST", "1h", spec=SPEC)
    t = res.trades.iloc[0]
    margin = t["qty"] * 100.0 / 10.0
    assert t["exit_reason"] == "liquidation_gap"
    assert t["net_pnl"] == pytest.approx(-margin)


def test_stop_and_target_same_bar_short_is_stop_first() -> None:
    df = make_bars([100, 100, 100, 100, 100])
    df.loc[df.index[3], ["high", "low"]] = [120.0, 80.0]
    sig = manual_signals(df.index, {1: -1}, stop=5, tp=5)
    t = run_backtest(df, sig, _cfg(), "TEST", "1h", spec=SPEC).trades.iloc[0]
    assert t["exit_reason"] == "stop_loss" and t["exit_price"] == pytest.approx(105.0)


def test_take_profit_gap_fills_at_open_not_at_target() -> None:
    df = make_bars([100, 100, 100, 100, 100])
    df.loc[df.index[3], ["open", "high", "low"]] = [110.0, 111.0, 109.0]
    sig = manual_signals(df.index, {1: 1}, stop=5, tp=5)
    t = run_backtest(df, sig, _cfg(), "TEST", "1h", spec=SPEC).trades.iloc[0]
    assert t["exit_reason"] == "take_profit_gap" and t["exit_price"] == pytest.approx(110.0)


def test_signal_on_last_bar_is_never_executed() -> None:
    df = make_bars([100, 101, 102, 103])
    sig = manual_signals(df.index, {3: 1}, stop=5)
    res = run_backtest(df, sig, _cfg(), "TEST", "1h", spec=SPEC)
    assert res.trades.empty  # no existe una apertura posterior a la última vela


def test_segment_start_does_not_enter_on_preexisting_signal() -> None:
    df = make_bars([100.0] * 10)
    sig = manual_signals(df.index, {2: 1}, stop=5)  # LONG desde la vela 2 y se mantiene
    res = run_backtest(df, sig, _cfg(), "TEST", "1h", spec=SPEC, start=df.index[5])
    assert res.trades.empty  # sin transición dentro del segmento no hay entrada


def test_metrics_match_hand_computation() -> None:
    rng = np.random.default_rng(3)
    idx = pd.date_range("2024-01-01", periods=60, freq="1h", tz="UTC")
    eq = 10_000 * np.cumprod(1 + rng.normal(0.0005, 0.01, 60))
    equity = pd.DataFrame(
        {
            "equity": eq,
            "cash": eq,
            "unrealized": 0.0,
            "position": 1.0,
            "margin_used": 0.0,
            "in_position": True,
        },
        index=idx,
    )
    equity["drawdown"] = equity["equity"] / equity["equity"].cummax() - 1
    pnl = np.array([50, -20, 30, -10, -40, 80, 15, -5, 25, -30, 60, -12], dtype=float)
    trades = pd.DataFrame(
        {
            "net_pnl": pnl,
            "gross_pnl": pnl + 1,
            "fees": 1.0,
            "funding": 0.0,
            "side": "LONG",
            "bars_held": 5,
            "return_on_equity": pnl / 1e4,
            "exit_reason": "signal_exit",
        }
    )
    res = BacktestResult(
        "x",
        "TEST",
        "1h",
        10_000.0,
        equity,
        trades,
        [],
        [],
        {"fees": 12.0, "slippage": 3.0, "funding": 0.0, "traded_notional": 50_000.0},
        False,
    )
    m = compute_metrics(res, min_trades=1, min_days_for_cagr=1)
    r = np.r_[eq[0] / 10_000 - 1, eq[1:] / eq[:-1] - 1]
    n_year = 365 * 24
    assert m["sharpe"] == pytest.approx(r.mean() / r.std(ddof=1) * math.sqrt(n_year))
    dd = math.sqrt(np.mean(np.minimum(r, 0) ** 2))
    assert m["sortino"] == pytest.approx(r.mean() / dd * math.sqrt(n_year))
    peak = np.maximum.accumulate(eq)
    assert m["max_drawdown"] == pytest.approx(float(np.max(1 - eq / peak)))
    assert m["profit_factor"] == pytest.approx(pnl[pnl > 0].sum() / -pnl[pnl < 0].sum())
    assert m["win_rate"] == pytest.approx((pnl > 0).mean())
    assert m["expectancy"] == pytest.approx(pnl.mean())
    days = 60 / 24
    assert m["cagr"] == pytest.approx((eq[-1] / 10_000) ** (365 / days) - 1)
    assert m["turnover"] == pytest.approx(50_000.0 / eq.mean())


def test_drawdown_duration_and_recovery_by_hand() -> None:
    from bybit_quant_lab.analytics.metrics import drawdown_stats

    idx = pd.date_range("2024-01-01", periods=8, freq="1h", tz="UTC")
    s = pd.Series([100, 110, 99, 95, 105, 111, 108, 112], index=idx, dtype=float)
    d = drawdown_stats(s)
    assert d["max_drawdown"] == pytest.approx(1 - 95 / 110)
    assert d["max_dd_start"] == str(idx[1]) and d["max_dd_trough"] == str(idx[3])
    assert d["max_dd_recovery_bars"] == 2 and d["max_dd_end"] == str(idx[5])
    assert d["max_dd_duration_bars"] == 3  # velas 2, 3 y 4 bajo el máximo de 110
