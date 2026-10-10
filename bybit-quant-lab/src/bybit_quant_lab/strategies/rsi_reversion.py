"""Estrategia 6 — RSI Mean Reversion (categoría indicadores).

Hipótesis: tras una sobreventa (RSI < ``oversold``), el **regreso** del RSI por encima del
umbral indica agotamiento de la presión vendedora (simétrico para sobrecompra). Tocar la zona
no basta: se exige el cruce de salida. Filtro opcional de tendencia para no aplicar la
reversión indiscriminadamente en tendencias fuertes:

* ``ema``: solo largos sobre la EMA larga y cortos bajo ella.
* ``adx``: solo se opera si ADX < ``adx_max`` (tendencia débil).
"""

from __future__ import annotations

from typing import Literal

import pandas as pd
from pydantic import Field, model_validator

from bybit_quant_lab.indicators import adx, crossover, crossunder, ema, rsi
from bybit_quant_lab.strategies.base import Category, Events, Strategy, StrategyParams
from bybit_quant_lab.strategies.registry import register


class RSIReversionParams(StrategyParams):
    """Parámetros de RSI Mean Reversion."""

    rsi_period: int = Field(14, ge=2, le=200)
    oversold: float = Field(30.0, gt=0, lt=50)
    overbought: float = Field(70.0, gt=50, lt=100)
    exit_level: float = Field(50.0, gt=0, lt=100)
    trend_filter: Literal["none", "ema", "adx"] = "adx"
    trend_ema: int = Field(200, ge=10, le=2000)
    adx_period: int = Field(14, ge=2, le=200)
    adx_max: float = Field(25.0, gt=0, le=100)
    take_profit_r: float | None = Field(None, gt=0, le=50)
    max_holding_bars: int | None = Field(48, ge=1)

    @model_validator(mode="after")
    def _check(self) -> RSIReversionParams:
        if not self.oversold < self.exit_level < self.overbought:
            raise ValueError("Se requiere oversold < exit_level < overbought")
        return self


@register
class RSIReversionStrategy(Strategy):
    """Salida de zona extrema del RSI con filtro de tendencia opcional."""

    name = "rsi_reversion"
    category = Category.INDICATOR
    description = "Reversión a la media por salida de sobreventa/sobrecompra del RSI"
    params_model = RSIReversionParams
    params: RSIReversionParams

    def warmup_bars(self) -> int:
        p = self.params
        extra = p.trend_ema if p.trend_filter == "ema" else 2 * p.adx_period
        return max(p.rsi_period + 1, extra, p.atr_period) + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        r = rsi(c, p.rsi_period)
        long_ok = pd.Series(True, index=c.index)
        short_ok = pd.Series(True, index=c.index)
        if p.trend_filter == "ema":
            t = ema(c, p.trend_ema)
            long_ok, short_ok = c > t, c < t
        elif p.trend_filter == "adx":
            weak = adx(data, p.adx_period)["adx"] < p.adx_max
            long_ok, short_ok = weak, weak
        depth_long = (p.oversold - r.rolling(5, min_periods=1).min()) / p.oversold
        depth_short = (r.rolling(5, min_periods=1).max() - p.overbought) / (100 - p.overbought)
        conviction = depth_long.clip(lower=0).combine(depth_short.clip(lower=0), max) * 2
        return Events(
            long_entry=crossover(r, p.oversold) & long_ok,
            short_entry=crossunder(r, p.overbought) & short_ok,
            long_exit=r >= p.exit_level,
            short_exit=r <= p.exit_level,
            conviction=conviction,
        )
