"""Generador de datos OHLCV sintéticos y deterministas.

Uso exclusivo para pruebas de lógica y demostraciones. Los datos sintéticos **no** sirven
para evaluar la rentabilidad real de ninguna estrategia.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bybit_quant_lab.timeframes import timeframe_delta


def generate_synthetic_ohlcv(
    bars: int = 3000,
    timeframe: str = "1h",
    seed: int = 42,
    start: str = "2023-01-01",
    start_price: float = 30_000.0,
    regime_length: int = 300,
    base_vol: float = 0.006,
) -> pd.DataFrame:
    """Genera OHLCV con regímenes alternos (tendencia alcista, lateral, bajista, alta vol).

    El volumen se correlaciona con el valor absoluto del retorno para que las estrategias de
    volumen tengan algo que medir. La serie es reproducible con la misma ``seed``.
    """
    if bars < 2:
        raise ValueError("bars debe ser >= 2")
    rng = np.random.default_rng(seed)
    regimes = [(0.0008, 1.0), (0.0, 0.7), (-0.0008, 1.1), (0.0, 1.8)]
    drift = np.empty(bars)
    vol = np.empty(bars)
    for i in range(bars):
        mu, scale = regimes[(i // regime_length) % len(regimes)]
        drift[i], vol[i] = mu, base_vol * scale
    rets = drift + vol * rng.standard_normal(bars)
    close = start_price * np.exp(np.cumsum(rets))
    open_ = np.empty(bars)
    open_[0] = start_price
    open_[1:] = close[:-1] * np.exp(0.1 * vol[1:] * rng.standard_normal(bars - 1))
    wick_hi = np.abs(rng.standard_normal(bars)) * vol * 0.6
    wick_lo = np.abs(rng.standard_normal(bars)) * vol * 0.6
    high = np.maximum(open_, close) * np.exp(wick_hi)
    low = np.minimum(open_, close) * np.exp(-wick_lo)
    base_volume = 1_000.0 * (1 + 40 * np.abs(rets)) * np.exp(0.3 * rng.standard_normal(bars))
    spikes = rng.random(bars) < 0.02
    volume = base_volume * np.where(spikes, rng.uniform(3, 6, bars), 1.0)
    idx = pd.date_range(
        pd.Timestamp(start, tz="UTC"),
        periods=bars,
        freq=timeframe_delta(timeframe),
        name="open_time",
    )
    df = pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume}, index=idx
    )
    df["turnover"] = df["volume"] * (df["high"] + df["low"] + df["close"]) / 3
    return df
