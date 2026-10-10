"""Pruebas del gestor de riesgo y del dimensionamiento."""

from __future__ import annotations

import pandas as pd
import pytest

from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config import AppConfig
from bybit_quant_lab.config.models import CostConfig, ExecutionConfig, RiskConfig
from bybit_quant_lab.risk import InstrumentSpec, RiskManager, size_position
from tests.conftest import make_bars, manual_signals, zero_cost_config

SPEC = InstrumentSpec(
    "TEST", tick_size=0.01, qty_step=0.001, min_qty=0.001, max_qty=1e9, min_notional=0.0
)


def test_size_uses_stop_distance_and_costs() -> None:
    res = size_position(
        10_000,
        0,
        100.0,
        5.0,
        RiskConfig(max_symbol_exposure=100, max_leverage=100, margin_reserve=0),
        ExecutionConfig(leverage=10, simulate_liquidation=False),
        CostConfig(taker_fee=0, slippage_bps=0),
        SPEC,
    )
    assert res.qty == pytest.approx(20.0)  # 1 % de 10 000 / 5
    with_costs = size_position(
        10_000,
        0,
        100.0,
        5.0,
        RiskConfig(max_symbol_exposure=100, max_leverage=100, margin_reserve=0),
        ExecutionConfig(leverage=10, simulate_liquidation=False),
        CostConfig(taker_fee=0.001, slippage_bps=10),
        SPEC,
    )
    assert with_costs.qty < res.qty


def test_size_capped_by_exposure_and_rounded_down() -> None:
    res = size_position(
        10_000,
        0,
        100.0,
        0.1,
        RiskConfig(max_symbol_exposure=2.0, max_leverage=5),
        ExecutionConfig(leverage=3, simulate_liquidation=False),
        CostConfig(taker_fee=0, slippage_bps=0),
        SPEC,
    )
    assert res.qty * 100 <= 20_000 + 1e-9
    assert res.capped_by in {"symbol_exposure", "available_margin"}


def test_size_rejects_below_min_qty() -> None:
    spec = InstrumentSpec("X", 0.1, qty_step=1.0, min_qty=1.0, max_qty=100)
    res = size_position(
        100,
        0,
        1000.0,
        50.0,
        RiskConfig(),
        ExecutionConfig(simulate_liquidation=False),
        CostConfig(),
        spec,
    )
    assert res.qty == 0 and res.reason == "below_min_qty"


def test_consecutive_losses_trigger_pause() -> None:
    rm = RiskManager(RiskConfig(max_consecutive_losses=3, pause_bars_after_losses=10), 1000)
    ts = pd.Timestamp("2024-01-01", tz="UTC")
    for i in range(3):
        rm.on_trade_closed(i, ts, -1.0)
    assert rm.can_open(5) == (False, "loss_streak_pause")
    assert rm.can_open(12) == (True, "ok")
    # Una ganancia reinicia la racha
    rm.on_trade_closed(20, ts, -1.0)
    rm.on_trade_closed(21, ts, 2.0)
    rm.on_trade_closed(22, ts, -1.0)
    assert rm.consecutive_losses == 1


def test_pause_does_not_override_other_limits() -> None:
    rm = RiskManager(RiskConfig(max_drawdown=0.1), 1000)
    rm.on_bar_open(pd.Timestamp("2024-01-01", tz="UTC"))
    rm.on_bar_close(pd.Timestamp("2024-01-01", tz="UTC"), 850)
    assert rm.can_open(100)[0] is False
    assert rm.halted


def test_daily_loss_blocks_until_next_utc_day() -> None:
    rm = RiskManager(RiskConfig(max_daily_loss=0.05, max_drawdown=0.9), 1000)
    t0 = pd.Timestamp("2024-01-01 10:00", tz="UTC")
    rm.on_bar_open(t0)
    rm.on_bar_close(t0, 940)  # -6 % mark-to-market (incluye no realizado)
    assert rm.can_open(1) == (False, "daily_loss_limit")
    t1 = pd.Timestamp("2024-01-02 00:00", tz="UTC")
    rm.on_bar_open(t1)
    assert rm.can_open(2) == (True, "ok")
    assert rm.day_start_equity == 940


def test_engine_pauses_after_three_losses() -> None:
    # Patrón: entra largo, cae y toca stop; repetido. Tras 3 pérdidas, se rechaza la 4.ª.
    closes: list[float] = []
    for _ in range(5):
        closes += [100, 100, 100, 90, 100]
    df = make_bars(closes, spread=0.1)
    sig_map = {}
    for k in range(5):
        sig_map[5 * k + 1] = 1
        sig_map[5 * k + 4] = 0
    sig = manual_signals(df.index, sig_map, stop=5)
    cfg = zero_cost_config(max_consecutive_losses=3, pause_bars_after_losses=100)
    res = run_backtest(df, sig, cfg, "TEST", "1h", spec=SPEC)
    assert len(res.trades) == 3
    assert (res.trades["net_pnl"] < 0).all()
    assert any(r["reason"] == "loss_streak_pause" for r in res.rejected_signals)
    assert any(e["kind"] == "loss_streak_pause" for e in res.risk_events)


def test_engine_daily_limit_close_and_block() -> None:
    closes = [100, 100, 100, 80, 80, 80, 80]
    df = make_bars(closes, spread=0.1)
    sig = manual_signals(df.index, {1: 1, 5: 0}, stop=30)
    cfg = zero_cost_config(
        max_daily_loss=0.01, daily_loss_action="close_and_block", risk_per_trade=0.05
    )
    res = run_backtest(df, sig, cfg, "TEST", "1h", spec=SPEC)
    t = res.trades.iloc[0]
    assert t["exit_reason"] == "risk_limit_close"
    assert t["exit_time"] == df.index[4]


def test_leverage_must_not_exceed_limit() -> None:
    with pytest.raises(ValueError):
        AppConfig.model_validate({"execution": {"leverage": 10}, "risk": {"max_leverage": 5}})


def test_leverage_does_not_change_pnl() -> None:
    df = make_bars([100, 100, 100, 105, 110, 120, 120])
    sig = manual_signals(df.index, {1: 1, 4: 0}, stop=10)
    pnls = []
    for lev in (2.0, 5.0):
        cfg = zero_cost_config()
        cfg = cfg.model_copy(
            update={"execution": cfg.execution.model_copy(update={"leverage": lev})}
        )
        pnls.append(run_backtest(df, sig, cfg, "TEST", "1h", spec=SPEC).trades["net_pnl"].iloc[0])
    assert pnls[0] == pytest.approx(pnls[1])


@pytest.mark.parametrize("unit", ["ns", "us", "ms", "s"])
def test_daily_reference_resets_regardless_of_index_resolution(unit: str) -> None:
    # Regresión: el identificador de día no debe depender de la resolución del índice.
    # Día 1: -3 %; día 2: otro -3 %. Con reinicio diario correcto nunca se alcanza el 5 %
    # diario; sin reinicio la pérdida acumulada (~6 %) activaría el límite.
    closes = [100.0] * 24 + [97.0] * 24 + [94.0] * 24 + [94.0] * 4
    df = make_bars(closes, spread=0.01, freq="1h")
    df.index = df.index.as_unit(unit)
    sig = manual_signals(df.index, {1: 1}, stop=10)
    cfg = zero_cost_config(max_daily_loss=0.05, risk_per_trade=0.1)
    res = run_backtest(df, sig, cfg, "TEST", "1h", spec=SPEC)
    assert res.trades["qty"].iloc[0] == pytest.approx(100.0)
    assert res.final_equity == pytest.approx(10_000 - 100 * (100 - 94))
    assert not any(e["kind"] == "daily_loss_limit" for e in res.risk_events)
