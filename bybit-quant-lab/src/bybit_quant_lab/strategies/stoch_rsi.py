"""Estrategia 9 — Stochastic RSI (categoría indicadores).

Hipótesis: un cruce de %K sobre %D **dentro** de la zona extrema (``%K < lower``) con vela
de confirmación indica giro de corto plazo. Para no contar varias veces señales casi
idénticas en un mismo movimiento, una nueva señal del mismo lado exige que %K haya vuelto a
la zona neutral (``rearm_level``) desde la señal anterior.
"""

from __future__ import annotations

import pandas as pd
from pydantic import Field, model_validator

from bybit_quant_lab.indicators import crossover, crossunder, ema, stoch_rsi
from bybit_quant_lab.strategies.base import (
    Category,
    Events,
    Strategy,
    StrategyParams,
    rearm_events,
)
from bybit_quant_lab.strategies.registry import register


class StochRSIParams(StrategyParams):
    """Parámetros de Stochastic RSI."""

    rsi_period: int = Field(14, ge=2, le=200)
    stoch_period: int = Field(14, ge=2, le=200)
    k_smooth: int = Field(3, ge=1, le=50)
    d_smooth: int = Field(3, ge=1, le=50)
    lower: float = Field(20.0, gt=0, lt=50)
    upper: float = Field(80.0, gt=50, lt=100)
    rearm_level: float = Field(50.0, gt=0, lt=100)
    confirm_candle: bool = True
    trend_ema: int | None = Field(None, ge=10, le=2000)
    take_profit_r: float | None = Field(1.5, gt=0, le=50)
    max_holding_bars: int | None = Field(24, ge=1)
    cooldown_bars: int = Field(3, ge=0)

    @model_validator(mode="after")
    def _check(self) -> StochRSIParams:
        if not self.lower < self.rearm_level < self.upper:
            raise ValueError("Se requiere lower < rearm_level < upper")
        return self


@register
class StochRSIStrategy(Strategy):
    """Cruces %K/%D en zonas extremas con rearmado anti-duplicados."""

    name = "stoch_rsi"
    category = Category.INDICATOR
    description = "Cruces del Stochastic RSI en zonas extremas con confirmación"
    params_model = StochRSIParams
    params: StochRSIParams

    def warmup_bars(self) -> int:
        p = self.params
        base = p.rsi_period + p.stoch_period + p.k_smooth + p.d_smooth
        return max(base, p.trend_ema or 0, p.atr_period) + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        o, c = data["open"], data["close"]
        st = stoch_rsi(c, p.rsi_period, p.stoch_period, p.k_smooth, p.d_smooth)
        k, d = st["k"], st["d"]
        long_raw = crossover(k, d) & (k.shift(1) < p.lower)
        short_raw = crossunder(k, d) & (k.shift(1) > p.upper)
        if p.confirm_candle:
            long_raw &= c > o
            short_raw &= c < o
        if p.trend_ema:
            t = ema(c, p.trend_ema)
            long_raw &= c > t
            short_raw &= c < t
        long_entry = rearm_events(long_raw, k > p.rearm_level)
        short_entry = rearm_events(short_raw, k < p.rearm_level)
        conviction = ((p.lower - k.shift(1)).clip(lower=0) / p.lower).combine(
            ((k.shift(1) - p.upper).clip(lower=0) / (100 - p.upper)), max
        )
        return Events(
            long_entry=long_entry,
            short_entry=short_entry,
            long_exit=crossunder(k, d) & (k > p.rearm_level),
            short_exit=crossover(k, d) & (k < p.rearm_level),
            conviction=conviction,
        )
