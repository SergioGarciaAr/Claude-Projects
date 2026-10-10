"""Estrategia 2 — OBV Trend Confirmation (categoría volumen).

Hipótesis: un cruce del OBV sobre su media, con pendiente positiva del OBV y precio por encima
de su media, indica que el volumen confirma la tendencia del precio. El enfriamiento
(``cooldown_bars``) evita señales redundantes tras una salida.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from pydantic import Field

from bybit_quant_lab.indicators import crossover, crossunder, ema, obv
from bybit_quant_lab.strategies.base import Category, Events, Strategy, StrategyParams
from bybit_quant_lab.strategies.registry import register


class OBVTrendParams(StrategyParams):
    """Parámetros de OBV Trend."""

    obv_ema: int = Field(20, ge=2, le=1000)
    price_ema: int = Field(50, ge=2, le=1000)
    slope_window: int = Field(5, ge=1, le=200)
    cooldown_bars: int = Field(5, ge=0)


@register
class OBVTrendStrategy(Strategy):
    """Cruce OBV/EMA(OBV) con pendiente del OBV y dirección del precio coherentes."""

    name = "obv_trend"
    category = Category.VOLUME
    description = "Cruce del OBV sobre su EMA confirmado por pendiente y precio"
    params_model = OBVTrendParams
    params: OBVTrendParams

    def warmup_bars(self) -> int:
        p = self.params
        return max(p.obv_ema, p.price_ema, p.atr_period) + p.slope_window + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        o = obv(c, data["volume"])
        o_ma = ema(o, p.obv_ema)
        slope = o - o.shift(p.slope_window)
        price_ma = ema(c, p.price_ema)
        dev = o - o_ma
        scale = o.diff().abs().rolling(p.obv_ema, min_periods=p.obv_ema).mean()
        conviction = (dev.abs() / (scale * np.sqrt(p.obv_ema)).replace(0, np.nan)).clip(0, 1)
        return Events(
            long_entry=crossover(o, o_ma) & (slope > 0) & (c > price_ma),
            short_entry=crossunder(o, o_ma) & (slope < 0) & (c < price_ma),
            long_exit=crossunder(o, o_ma) | (c < price_ma),
            short_exit=crossover(o, o_ma) | (c > price_ma),
            conviction=conviction,
        )
