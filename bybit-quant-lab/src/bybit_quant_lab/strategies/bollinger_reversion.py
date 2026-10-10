"""Estrategia 8 — Bollinger Bands Reversion (categoría indicadores).

Hipótesis de **reversión** (separada de cualquier lógica de ruptura de bandas): un cierre
fuera de la banda seguido de un cierre de **regreso** dentro de ella, con vela de
confirmación opcional, anticipa el retorno a la media. Tocar la banda no genera señal.

Salida: cierre en la media (``mid``). Invalidación: un nuevo cierre fuera de la banda en la
dirección adversa después de la entrada cierra la posición.
"""

from __future__ import annotations

import pandas as pd
from pydantic import Field

from bybit_quant_lab.indicators import adx, bollinger
from bybit_quant_lab.strategies.base import Category, Events, Strategy, StrategyParams
from bybit_quant_lab.strategies.registry import register


class BollingerParams(StrategyParams):
    """Parámetros de Bollinger Reversion."""

    period: int = Field(20, ge=2, le=1000)
    num_std: float = Field(2.0, gt=0, le=10)
    confirm_candle: bool = True
    adx_max: float | None = Field(30.0, gt=0, le=100)
    adx_period: int = Field(14, ge=2, le=200)
    take_profit_r: float | None = Field(None, gt=0, le=50)
    max_holding_bars: int | None = Field(48, ge=1)


@register
class BollingerReversionStrategy(Strategy):
    """Reingreso confirmado en las bandas de Bollinger."""

    name = "bollinger_reversion"
    category = Category.INDICATOR
    description = "Reversión tras reingreso confirmado en las bandas de Bollinger"
    params_model = BollingerParams
    params: BollingerParams

    def warmup_bars(self) -> int:
        p = self.params
        return max(p.period + 1, 2 * p.adx_period, p.atr_period) + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        o, c = data["open"], data["close"]
        bb = bollinger(c, p.period, p.num_std)
        below_prev = c.shift(1) < bb["lower"].shift(1)
        above_prev = c.shift(1) > bb["upper"].shift(1)
        long_setup = below_prev & (c > bb["lower"])
        short_setup = above_prev & (c < bb["upper"])
        if p.confirm_candle:
            long_setup &= c > o
            short_setup &= c < o
        if p.adx_max is not None:
            weak = adx(data, p.adx_period)["adx"] < p.adx_max
            long_setup &= weak
            short_setup &= weak
        width = (bb["upper"] - bb["lower"]).where(lambda w: w > 0)
        conviction = ((bb["mid"] - c).abs() / (width / 2)).clip(0, 1)
        return Events(
            long_entry=long_setup,
            short_entry=short_setup,
            long_exit=(c >= bb["mid"]) | (c < bb["lower"]),
            short_exit=(c <= bb["mid"]) | (c > bb["upper"]),
            conviction=conviction,
        )
