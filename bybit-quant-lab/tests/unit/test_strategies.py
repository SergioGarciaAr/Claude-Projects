"""Pruebas de las diez estrategias: contrato, límites, datos ausentes y no look-ahead."""

from __future__ import annotations

import itertools

import numpy as np
import pandas as pd
import pytest

from bybit_quant_lab.strategies import (
    SIGNAL_COLUMNS,
    available_strategies,
    create_strategy,
    events_to_state,
)
from bybit_quant_lab.strategies.base import rearm_events
from tests.conftest import make_bars

ALL = available_strategies()


def test_exactly_ten_strategies_registered() -> None:
    assert len(ALL) == 10
    cats = {create_strategy(n).category.value for n in ALL}
    assert cats == {"volume", "trend", "indicator"}
    counts = pd.Series([create_strategy(n).category.value for n in ALL]).value_counts()
    assert counts.to_dict() == {"indicator": 5, "volume": 3, "trend": 2}


@pytest.mark.parametrize("name", ALL)
def test_output_contract(name: str, synth: pd.DataFrame) -> None:
    out = create_strategy(name).generate_signals(synth)
    assert list(out.columns) == list(SIGNAL_COLUMNS)
    assert out.index.equals(synth.index)
    assert set(out["signal"].unique()) <= {-1, 0, 1}
    assert out["conviction"].between(0, 1).all()
    assert (out.loc[out["signal"] == 0, "conviction"] == 0).all()
    active = out["signal"] != 0
    assert active.any(), "la estrategia debería generar alguna señal con 3000 velas"
    assert (out.loc[active, "stop_distance"] > 0).all()


@pytest.mark.parametrize("name", ALL)
def test_no_lookahead_truncation(name: str, synth: pd.DataFrame) -> None:
    strat = create_strategy(name)
    full = strat.generate_signals(synth)
    for t in (400, 1100, 2203):
        part = strat.generate_signals(synth.iloc[: t + 1])
        pd.testing.assert_frame_equal(full.iloc[: t + 1], part, check_freq=False)


@pytest.mark.parametrize("name", ALL)
def test_no_lookahead_future_perturbation(name: str, synth: pd.DataFrame) -> None:
    strat = create_strategy(name)
    t = 1500
    altered = synth.copy()
    rng = np.random.default_rng(0)
    factor = np.exp(np.cumsum(rng.normal(0, 0.05, len(synth) - t - 1)))
    for col in ("open", "high", "low", "close"):
        altered.iloc[t + 1 :, altered.columns.get_loc(col)] *= factor
    altered.iloc[t + 1 :, altered.columns.get_loc("volume")] *= 10
    a = strat.generate_signals(synth).iloc[: t + 1]
    b = strat.generate_signals(altered).iloc[: t + 1]
    pd.testing.assert_frame_equal(a, b)


@pytest.mark.parametrize("name", ALL)
def test_empty_and_short_data(name: str, synth: pd.DataFrame) -> None:
    strat = create_strategy(name)
    empty = strat.generate_signals(synth.iloc[:0])
    assert empty.empty and list(empty.columns) == list(SIGNAL_COLUMNS)
    short = strat.generate_signals(synth.iloc[:5])
    assert (short["signal"] == 0).all()


@pytest.mark.parametrize("name", ALL)
def test_missing_values_do_not_crash(name: str, synth: pd.DataFrame) -> None:
    df = synth.iloc[:800].copy()
    df.iloc[300:303, :] = np.nan
    out = create_strategy(name).generate_signals(df)
    assert set(out["signal"].unique()) <= {-1, 0, 1}
    assert out["conviction"].notna().all()


@pytest.mark.parametrize("name", ALL)
def test_missing_column_raises(name: str, synth: pd.DataFrame) -> None:
    with pytest.raises(ValueError):
        create_strategy(name).generate_signals(synth.drop(columns=["volume"]))


@pytest.mark.parametrize("name", ALL)
def test_long_only_mode(name: str, synth: pd.DataFrame) -> None:
    out = create_strategy(name, {"allow_short": False}).generate_signals(synth)
    assert (out["signal"] >= 0).all()


@pytest.mark.parametrize("name", ALL)
def test_invalid_params_rejected(name: str) -> None:
    with pytest.raises(ValueError):
        create_strategy(name, {"parametro_inexistente": 1})


# ----------------------------------------------------------------- casos conocidos
def _noisy(closes: np.ndarray, seed: int = 1, noise: float = 0.05) -> np.ndarray:
    return closes + np.random.default_rng(seed).normal(0, noise, len(closes))


def test_events_to_state_rules() -> None:
    idx = pd.RangeIndex(8)
    s = lambda v: pd.Series(v, index=idx, dtype=bool)  # noqa: E731
    le = s([0, 1, 0, 0, 0, 1, 0, 0])
    se = s([0, 0, 0, 1, 0, 1, 0, 0])
    lx = s([0, 0, 0, 0, 0, 0, 0, 0])
    sx = s([0, 0, 0, 0, 1, 0, 0, 0])
    out = events_to_state(le, se, lx, sx).tolist()
    # entra largo (1), revierte a corto (3), sale (4), conflicto simultáneo ignorado (5)
    assert out == [0, 1, 1, -1, 0, 0, 0, 0]
    assert events_to_state(le, se, lx, sx, max_holding_bars=1).tolist()[:3] == [0, 1, 0]


def test_rearm_events_deduplicates() -> None:
    ev = pd.Series([1, 1, 0, 1, 0, 1], dtype=bool)
    reset = pd.Series([0, 0, 0, 0, 1, 0], dtype=bool)
    assert rearm_events(ev, reset).tolist() == [True, False, False, False, False, True]


def test_volume_spike_requires_price_confirmation() -> None:
    closes = _noisy(np.full(60, 100.0))
    df = make_bars(list(closes), spread=0.2)
    i = 50
    df.loc[df.index[i], ["open", "close", "high", "low", "volume"]] = [100, 103, 103.2, 99.9, 1000]
    strat = create_strategy("volume_spike", {"spike_mult": 3.0})
    assert strat.generate_signals(df)["signal"].iloc[i] == 1
    # Mismo pico de volumen con vela doji: no hay dirección -> sin señal
    doji = df.copy()
    doji.loc[doji.index[i], ["open", "close", "high", "low"]] = [100, 100.01, 101, 99]
    assert strat.generate_signals(doji)["signal"].iloc[i] == 0
    # Vela fuerte sin volumen anormal: sin señal
    quiet = df.copy()
    quiet.loc[quiet.index[i], "volume"] = 100
    assert strat.generate_signals(quiet)["signal"].iloc[i] == 0


def test_vwap_hypotheses_are_separate() -> None:
    closes = _noisy(np.full(300, 100.0), noise=0.2)
    df = make_bars(list(closes), spread=0.2)
    i = 280
    df.loc[df.index[i], ["open", "close", "high", "low"]] = [100, 95, 100.2, 94.8]
    rev = create_strategy(
        "vwap_deviation", {"mode": "reversion", "vwap_window": 50, "dev_window": 50}
    )
    cont = create_strategy(
        "vwap_deviation", {"mode": "continuation", "vwap_window": 50, "dev_window": 50}
    )
    assert rev.generate_signals(df)["signal"].iloc[i] == 1  # volumen normal -> reversión
    assert cont.generate_signals(df)["signal"].iloc[i] == 0
    loud = df.copy()
    loud.loc[loud.index[i], "volume"] = 1000
    assert rev.generate_signals(loud)["signal"].iloc[i] == 0
    assert cont.generate_signals(loud)["signal"].iloc[i] == -1  # volumen alto -> continuación


def test_vwap_session_mode_runs() -> None:
    df = make_bars(list(_noisy(np.linspace(100, 110, 400), noise=0.3)), spread=0.2)
    out = create_strategy("vwap_deviation", {"vwap_type": "session"}).generate_signals(df)
    assert set(out["signal"].unique()) <= {-1, 0, 1}


def test_ema_crossover_v_shape_goes_long() -> None:
    closes = np.r_[np.linspace(120, 100, 80), np.linspace(100, 130, 80)]
    df = make_bars(list(_noisy(closes)), spread=0.3)
    out = create_strategy("ema_crossover", {"trend_ema": None, "regime_filter": "none"})
    sig = out.generate_signals(df)["signal"]
    assert (sig.iloc[100:] == 1).any()
    assert (sig.iloc[120:] != -1).all()


def test_ema_crossover_regime_filter_blocks_range() -> None:
    closes = 100 + np.sin(np.arange(400) / 6.0) * 0.5
    df = make_bars(list(closes), spread=0.05)
    sig = create_strategy(
        "ema_crossover", {"trend_ema": None, "regime_filter": "adx", "adx_min": 40}
    ).generate_signals(df)["signal"]
    unfiltered = create_strategy("ema_crossover", {"trend_ema": None, "regime_filter": "none"})
    assert (sig != 0).sum() < (unfiltered.generate_signals(df)["signal"] != 0).sum()


def test_donchian_uses_previous_bars_only() -> None:
    closes = list(_noisy(np.full(40, 100.0), noise=0.1))
    df = make_bars(closes, spread=0.2)
    i = 35
    prev_high = df["high"].iloc[i - 20 : i].max()
    df.loc[df.index[i], ["close", "high"]] = [prev_high + 0.01, prev_high + 0.02]
    sig = create_strategy(
        "donchian_breakout", {"channel": 20, "exit_channel": 10, "atr_period": 5}
    ).generate_signals(df)
    assert sig["signal"].iloc[i] == 1
    assert (sig["signal"].iloc[:i] == 0).all()


def test_donchian_htf_filter_runs_without_lookahead(synth: pd.DataFrame) -> None:
    strat = create_strategy("donchian_breakout", {"htf": "4h"})
    full = strat.generate_signals(synth)
    part = strat.generate_signals(synth.iloc[:1001])
    pd.testing.assert_frame_equal(full.iloc[:1001], part)


def test_rsi_reversion_long_after_oversold_exit() -> None:
    closes = np.r_[np.full(30, 100.0), np.linspace(100, 80, 20), np.linspace(80, 84, 6)]
    df = make_bars(list(_noisy(closes, noise=0.02)), spread=0.1)
    sig = create_strategy("rsi_reversion", {"trend_filter": "none"}).generate_signals(df)
    assert (sig["signal"].iloc[50:] == 1).any()
    assert (sig["signal"].iloc[30:50] == 0).all()  # en sobreventa aún no se entra


def test_macd_v_shape_goes_long() -> None:
    closes = np.r_[np.linspace(120, 100, 80), np.linspace(100, 125, 60)]
    df = make_bars(list(_noisy(closes)), spread=0.3)
    sig = create_strategy("macd_momentum", {"direction_filter": "none"}).generate_signals(df)
    assert (sig["signal"].iloc[80:] == 1).any()


def test_bollinger_touch_is_not_signal_but_reentry_is() -> None:
    closes = list(_noisy(np.full(80, 100.0), noise=0.3))
    df = make_bars(closes, spread=0.1)
    params = {"adx_max": None, "confirm_candle": True}
    # Toque: mínimo por debajo de la banda pero cierre dentro -> sin señal
    touch = df.copy()
    touch.loc[touch.index[60], "low"] = 95.0
    assert (
        create_strategy("bollinger_reversion", params).generate_signals(touch)["signal"].iloc[58:63]
        == 0
    ).all()
    # Cierre fuera de banda y reingreso alcista confirmado -> LONG
    re = df.copy()
    re.loc[re.index[60], ["open", "close", "low", "high"]] = [100.0, 97.0, 96.9, 100.1]
    re.loc[re.index[61], ["open", "close", "low", "high"]] = [97.0, 99.5, 96.95, 99.6]
    assert (
        create_strategy("bollinger_reversion", params).generate_signals(re)["signal"].iloc[61] == 1
    )


def test_adx_no_entries_when_trend_weak(synth: pd.DataFrame) -> None:
    from bybit_quant_lab.indicators import adx

    strat = create_strategy("adx_di")
    sig = strat.generate_signals(synth)["signal"]
    a = adx(synth, 14)["adx"]
    entries = (sig != 0) & (sig != sig.shift(1))
    assert entries.any()
    assert (a[entries] >= strat.params.adx_threshold).all()
    # Con ADX por debajo de adx_exit no se mantiene ninguna posición.
    assert (sig[a < strat.params.adx_exit] == 0).all()


def test_adx_long_in_strong_uptrend() -> None:
    closes = np.r_[np.full(50, 100.0), np.linspace(100, 160, 150)]
    df = make_bars(list(_noisy(closes, noise=0.1)), spread=0.2)
    sig = create_strategy("adx_di").generate_signals(df)["signal"]
    assert (sig.iloc[100:] == 1).any()
    assert (sig.iloc[100:] != -1).all()


def test_stoch_rsi_counts_one_signal_per_move(synth: pd.DataFrame) -> None:
    strat = create_strategy("stoch_rsi")
    from bybit_quant_lab.indicators import stoch_rsi

    out = strat.generate_signals(synth)
    k = stoch_rsi(synth["close"])["k"]
    entries = (out["signal"] == 1) & (out["signal"].shift(1) != 1)
    times = list(np.nonzero(entries.to_numpy())[0])
    # Entre dos entradas largas consecutivas, %K debe haber superado el nivel de rearme.
    for a, b in itertools.pairwise(times):
        assert (k.iloc[a + 1 : b + 1] > 50).any()


def test_obv_no_shorts_in_steady_uptrend() -> None:
    closes = np.linspace(100, 150, 300)
    df = make_bars(list(_noisy(closes, noise=0.05)), spread=0.1)
    sig = create_strategy("obv_trend").generate_signals(df)["signal"]
    assert (sig.iloc[100:] != -1).all()
