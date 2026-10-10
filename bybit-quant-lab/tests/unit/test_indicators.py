"""Pruebas de indicadores con valores conocidos y causalidad."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from bybit_quant_lab import indicators as ind
from tests.conftest import make_bars


def test_sma_ema_known_values() -> None:
    s = pd.Series([1.0, 2, 3, 4, 5])
    assert ind.sma(s, 3).tolist()[2:] == [2.0, 3.0, 4.0]
    e = ind.ema(s, 3)  # alpha = 0.5, semilla x0 = 1
    assert np.isnan(e.iloc[1])
    assert e.iloc[2] == pytest.approx(2.25)
    assert e.iloc[4] == pytest.approx(4.0625)


def test_rsi_extremes() -> None:
    up = pd.Series(np.arange(1, 40, dtype=float))
    assert ind.rsi(up, 14).iloc[-1] == pytest.approx(100.0)
    down = pd.Series(np.arange(40, 1, -1, dtype=float))
    assert ind.rsi(down, 14).iloc[-1] == pytest.approx(0.0)
    flat = pd.Series(np.full(40, 5.0))
    assert ind.rsi(flat, 14).iloc[-1] == pytest.approx(50.0)


def test_atr_constant_range() -> None:
    df = make_bars([100.0] * 50, spread=1.0)
    assert ind.atr(df, 14).iloc[-1] == pytest.approx(2.0)


def test_obv_accumulates_signed_volume() -> None:
    close = pd.Series([1.0, 2, 1, 1, 3])
    vol = pd.Series([10.0, 20, 30, 40, 50])
    assert ind.obv(close, vol).tolist() == [0, 20, -10, -10, 40]


def test_donchian_excludes_current_bar() -> None:
    df = make_bars([1.0, 2, 3, 4, 10], spread=0.0)
    ch = ind.donchian(df, 3)
    assert ch["upper"].iloc[4] == 4.0  # máximo de las velas 1..3, no incluye el 10


def test_vwap_session_resets_daily() -> None:
    df = make_bars([100.0] * 24 + [200.0] * 24, spread=0.0)
    df.iloc[24, df.columns.get_loc("open")] = 200.0
    df.iloc[24, df.columns.get_loc("low")] = 200.0
    v = ind.vwap_session(df)
    assert v.iloc[23] == pytest.approx(100.0)
    assert v.iloc[24] == pytest.approx(200.0)


def test_bollinger_and_macd_shapes() -> None:
    s = pd.Series(np.linspace(1, 2, 100))
    bb = ind.bollinger(s, 20, 2)
    assert (bb["upper"].dropna() >= bb["lower"].dropna()).all()
    m = ind.macd(s)
    valid = m.dropna()
    np.testing.assert_allclose(valid["hist"], valid["macd"] - valid["signal"])
    with pytest.raises(ValueError):
        ind.macd(s, 26, 12)


def test_stoch_rsi_bounds(synth: pd.DataFrame) -> None:
    st = ind.stoch_rsi(synth["close"]).dropna()
    assert st["k"].between(0, 100).all() and st["d"].between(0, 100).all()


def test_adx_bounds(synth: pd.DataFrame) -> None:
    a = ind.adx(synth).dropna()
    assert a["adx"].between(0, 100).all()
    assert (a["plus_di"] >= 0).all() and (a["minus_di"] >= 0).all()


def test_crossover_detection() -> None:
    a = pd.Series([1.0, 2, 3, 2, 1])
    b = pd.Series([2.0, 2, 2, 2, 2])
    assert ind.crossover(a, b).tolist() == [False, False, True, False, False]
    assert ind.crossunder(a, b).tolist() == [False, False, False, False, True]


def test_rolling_percentile_and_zscore_exclude_current() -> None:
    s = pd.Series([1.0, 2, 3, 4, 100])
    assert ind.rolling_percentile(s, 4).iloc[4] == 1.0
    z = ind.rolling_zscore(s, 4)
    assert z.iloc[4] > 50


def test_higher_timeframe_only_closed_bars() -> None:
    df = make_bars(list(np.arange(1, 13, dtype=float)), spread=0.0)  # 12 velas de 1h
    htf = ind.higher_timeframe(df, pd.Timedelta("1h"), pd.Timedelta("4h"))
    # La vela 4h [00:00, 04:00) cierra a las 04:00 = cierre de la vela base de las 03:00.
    assert np.isnan(htf["close"].iloc[2])
    assert htf["close"].iloc[3] == 4.0
    assert htf["close"].iloc[6] == 4.0
    assert htf["close"].iloc[7] == 8.0


@pytest.mark.parametrize("fn", ["sma", "ema", "wilder"])
def test_invalid_period(fn: str) -> None:
    with pytest.raises(ValueError):
        getattr(ind, fn)(pd.Series([1.0, 2.0]), 0)
