"""Pruebas del motor: ejecución en la apertura siguiente, costes, SL/TP y determinismo."""

from __future__ import annotations

import pandas as pd
import pytest

from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config import AppConfig
from bybit_quant_lab.risk.instruments import InstrumentSpec
from tests.conftest import make_bars, manual_signals, zero_cost_config

SPEC = InstrumentSpec(
    "TEST", tick_size=0.01, qty_step=0.001, min_qty=0.001, max_qty=1e9, min_notional=0.0
)


def _run(df: pd.DataFrame, sig: pd.DataFrame, cfg: AppConfig, **kw: object):
    return run_backtest(df, sig, cfg, "TEST", "1h", spec=SPEC, **kw)


def test_signal_executes_at_next_open() -> None:
    closes = [100, 101, 102, 110, 111, 112, 113, 114]
    df = make_bars(closes)
    sig = manual_signals(df.index, {2: 1, 6: 0}, stop=50)
    res = _run(df, sig, zero_cost_config())
    trade = res.trades.iloc[0]
    # Señal al cierre de la vela 2 -> entrada a la apertura de la vela 3 (= cierre de la 2 = 102),
    # no al cierre de la vela de la señal ni a la apertura de la vela 2.
    assert trade["entry_time"] == df.index[3]
    assert trade["entry_price"] == pytest.approx(df["open"].iloc[3])
    assert trade["exit_time"] == df.index[7]
    assert trade["exit_price"] == pytest.approx(df["open"].iloc[7])


def test_zero_cost_pnl_matches_price_change() -> None:
    df = make_bars([100, 100, 100, 105, 110, 120, 120])
    sig = manual_signals(df.index, {1: 1, 4: 0}, stop=10)
    res = _run(df, sig, zero_cost_config())
    t = res.trades.iloc[0]
    assert t["net_pnl"] == pytest.approx((df["open"].iloc[5] - df["open"].iloc[2]) * t["qty"])
    assert res.final_equity == pytest.approx(10_000 + t["net_pnl"])


def test_fees_and_slippage_reduce_net_exactly() -> None:
    df = make_bars([100, 100, 100, 105, 110, 120, 120])
    sig = manual_signals(df.index, {1: 1, 4: 0}, stop=10)
    cfg = zero_cost_config()
    cfg = cfg.model_copy(
        update={"costs": cfg.costs.model_copy(update={"taker_fee": 0.001, "slippage_bps": 10.0})}
    )
    res = _run(df, sig, cfg)
    t = res.trades.iloc[0]
    entry_ref, exit_ref = df["open"].iloc[2], df["open"].iloc[5]
    entry_fill, exit_fill = entry_ref * 1.001, exit_ref * 0.999
    qty = t["qty"]
    fees = 0.001 * qty * (entry_fill + exit_fill)
    assert t["entry_price"] == pytest.approx(entry_fill)
    assert t["exit_price"] == pytest.approx(exit_fill)
    assert t["fees"] == pytest.approx(fees)
    assert t["gross_pnl"] == pytest.approx((exit_ref - entry_ref) * qty)
    assert t["net_pnl"] == pytest.approx((exit_fill - entry_fill) * qty - fees)
    assert t["net_pnl"] == pytest.approx(t["gross_pnl"] - t["fees"] - t["slippage_cost"])
    assert res.final_equity == pytest.approx(10_000 + t["net_pnl"])


def test_stop_and_target_same_bar_assumes_stop_first() -> None:
    df = make_bars([100, 100, 100, 100, 100])
    # Vela 3 con rango enorme: toca stop (95) y objetivo (105).
    df.loc[df.index[3], ["high", "low"]] = [120.0, 80.0]
    sig = manual_signals(df.index, {1: 1}, stop=5, tp=5)
    res = _run(df, sig, zero_cost_config())
    t = res.trades.iloc[0]
    assert t["exit_reason"] == "stop_loss"
    assert t["exit_price"] == pytest.approx(95.0)
    assert t["net_pnl"] < 0


def test_take_profit_hit() -> None:
    df = make_bars([100, 100, 100, 100, 100])
    df.loc[df.index[3], "high"] = 106.0
    sig = manual_signals(df.index, {1: 1}, stop=5, tp=5)
    t = _run(df, sig, zero_cost_config()).trades.iloc[0]
    assert t["exit_reason"] == "take_profit"
    assert t["exit_price"] == pytest.approx(105.0)


def test_gap_through_stop_fills_at_open() -> None:
    df = make_bars([100, 100, 100, 100, 90, 90])
    df.loc[df.index[4], ["open", "high", "low"]] = [90.0, 91.0, 89.0]
    sig = manual_signals(df.index, {1: 1}, stop=5)
    t = _run(df, sig, zero_cost_config()).trades.iloc[0]
    assert t["exit_reason"] == "stop_loss_gap"
    assert t["exit_price"] == pytest.approx(90.0)


def test_short_position_pnl_sign() -> None:
    df = make_bars([100, 100, 100, 95, 90, 90])
    sig = manual_signals(df.index, {1: -1, 3: 0}, stop=20)
    t = _run(df, sig, zero_cost_config()).trades.iloc[0]
    assert t["side"] == "SHORT"
    assert t["net_pnl"] > 0


def test_trailing_stop_moves_with_close() -> None:
    df = make_bars([100, 100, 100, 110, 120, 130, 110])
    df.loc[df.index[6], ["open", "high", "low"]] = [130.0, 131.0, 105.0]
    sig = manual_signals(df.index, {1: 1}, stop=10, trail=10)
    t = _run(df, sig, zero_cost_config()).trades.iloc[0]
    assert t["exit_reason"] == "stop_loss"
    assert t["exit_price"] == pytest.approx(120.0)  # máximo cierre 130 - 10


def test_funding_applied_only_when_data_present() -> None:
    df = make_bars([100] * 20)
    sig = manual_signals(df.index, {1: 1}, stop=50)
    no_fund = _run(df, sig, zero_cost_config())
    assert not no_fund.funding_applied
    assert any("funding" in w.lower() for w in no_fund.warnings)
    funding = pd.Series([0.001, 0.001], index=[df.index[8], df.index[16]])
    res = _run(df, sig, zero_cost_config(), funding=funding)
    t = res.trades.iloc[0]
    expected = 2 * 0.001 * t["qty"] * 100.0
    assert res.funding_applied
    assert t["funding"] == pytest.approx(expected)
    assert t["net_pnl"] == pytest.approx(-expected)


def test_backtest_is_deterministic(synth: pd.DataFrame) -> None:
    from bybit_quant_lab.strategies import create_strategy

    sig = create_strategy("donchian_breakout").generate_signals(synth)
    a = run_backtest(synth, sig, AppConfig(), "BTCUSDT", "1h")
    b = run_backtest(synth, sig, AppConfig(), "BTCUSDT", "1h")
    pd.testing.assert_frame_equal(a.equity, b.equity)
    pd.testing.assert_frame_equal(a.trades, b.trades)


def test_liquidation_loses_margin() -> None:
    df = make_bars([100, 100, 100, 100, 100])
    df.loc[df.index[3], "low"] = 50.0
    cfg = zero_cost_config()
    cfg = cfg.model_copy(
        update={
            "execution": cfg.execution.model_copy(
                update={
                    "simulate_liquidation": True,
                    "leverage": 10.0,
                    "maintenance_margin_rate": 0.005,
                }
            )
        }
    )
    # Stop más allá de la liquidación -> la entrada se rechaza.
    sig = manual_signals(df.index, {1: 1}, stop=20)
    res = _run(df, sig, cfg)
    assert res.trades.empty
    assert res.rejected_signals[0]["reason"] == "stop_beyond_liquidation"
    # Sin stop efectivo (stop dentro del rango permitido pero la vela atraviesa ambos):
    sig2 = manual_signals(df.index, {1: 1}, stop=8)
    t = _run(df, sig2, cfg).trades.iloc[0]
    assert t["exit_reason"] == "stop_loss"  # el stop (92) está antes que la liquidación (~90.5)


def test_misaligned_signals_rejected() -> None:
    df = make_bars([100] * 5)
    sig = manual_signals(df.index[:-1], {})
    with pytest.raises(ValueError):
        _run(df, sig, zero_cost_config())
