"""Estrategia 7 — MACD Momentum (categoría indicadores).

Hipótesis: el cruce de la línea MACD sobre su línea de señal, con histograma creciente,
indica aceleración del momentum. Filtros direccionales opcionales (``direction_filter``)
cuya contribución incremental se mide comparando variantes (``none`` frente a ``ema`` o
``zero_line``) en el análisis de sensibilidad.
"""

from __future__ import annotations

from typing import Literal

import pandas as pd
from pydantic import Field, model_validator

from bybit_quant_lab.indicators import crossover, crossunder, ema, macd
from bybit_quant_lab.strategies.base import Category, Events, Strategy, StrategyParams
from bybit_quant_lab.strategies.registry import register


class MACDMomentumParams(StrategyParams):
    """Parámetros de MACD Momentum."""

    fast: int = Field(12, ge=2, le=500)
    slow: int = Field(26, ge=3, le=1000)
    signal_period: int = Field(9, ge=2, le=200)
    require_hist_rising: bool = True
    direction_filter: Literal["none", "ema", "zero_line"] = "ema"
    trend_ema: int = Field(200, ge=10, le=2000)

    @model_validator(mode="after")
    def _check(self) -> MACDMomentumParams:
        if self.fast >= self.slow:
            raise ValueError("fast debe ser menor que slow")
        return self


@register
class MACDMomentumStrategy(Strategy):
    """Cruce MACD/señal con confirmación del histograma y filtro direccional."""

    name = "macd_momentum"
    category = Category.INDICATOR
    description = "Cambio de momentum por cruce MACD/señal confirmado por histograma"
    params_model = MACDMomentumParams
    params: MACDMomentumParams

    def warmup_bars(self) -> int:
        p = self.params
        trend = p.trend_ema if p.direction_filter == "ema" else 0
        return max(p.slow + p.signal_period, trend, p.atr_period) + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        m = macd(c, p.fast, p.slow, p.signal_period)
        hist = m["hist"]
        rising, falling = hist > hist.shift(1), hist < hist.shift(1)
        if not p.require_hist_rising:
            rising = falling = pd.Series(True, index=c.index)
        if p.direction_filter == "ema":
            t = ema(c, p.trend_ema)
            up_ok, dn_ok = c > t, c < t
        elif p.direction_filter == "zero_line":
            up_ok, dn_ok = m["macd"] > 0, m["macd"] < 0
        else:
            up_ok = dn_ok = pd.Series(True, index=c.index)
        scale = hist.abs().rolling(100, min_periods=20).max()
        conviction = (hist.abs() / scale).clip(0, 1)
        return Events(
            long_entry=crossover(m["macd"], m["signal"]) & rising & up_ok,
            short_entry=crossunder(m["macd"], m["signal"]) & falling & dn_ok,
            long_exit=crossunder(m["macd"], m["signal"]),
            short_exit=crossover(m["macd"], m["signal"]),
            conviction=conviction,
        )
