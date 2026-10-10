"""Estrategia 10 — ADX + DI Directional System (categoría indicadores).

Hipótesis: con fuerza de tendencia suficiente (``ADX >= adx_threshold``) el sesgo direccional
lo da el diferencial ``+DI - (-DI)``.

Comportamiento con fuerza insuficiente: si ``ADX < adx_threshold`` **no se abren** posiciones
(estado FLAT). Si ``exit_on_weak_trend`` es verdadero, una posición abierta se cierra cuando
ADX cae por debajo de ``adx_exit`` (histéresis para evitar entradas/salidas alternadas).
"""

from __future__ import annotations

import pandas as pd
from pydantic import Field, model_validator

from bybit_quant_lab.indicators import adx
from bybit_quant_lab.strategies.base import Category, Events, Strategy, StrategyParams
from bybit_quant_lab.strategies.registry import register


class ADXDIParams(StrategyParams):
    """Parámetros de ADX + DI."""

    adx_period: int = Field(14, ge=2, le=200)
    adx_threshold: float = Field(25.0, gt=0, le=100)
    adx_exit: float = Field(20.0, gt=0, le=100)
    di_margin: float = Field(2.0, ge=0, le=100)
    require_adx_rising: bool = False
    exit_on_weak_trend: bool = True
    take_profit_r: float | None = Field(None, gt=0, le=50)
    trailing_atr_mult: float | None = Field(3.0, gt=0, le=20)

    @model_validator(mode="after")
    def _check(self) -> ADXDIParams:
        if self.adx_exit > self.adx_threshold:
            raise ValueError("adx_exit no debe superar adx_threshold")
        return self


@register
class ADXDIStrategy(Strategy):
    """Sesgo +DI/-DI condicionado a fuerza de tendencia ADX."""

    name = "adx_di"
    category = Category.INDICATOR
    description = "Dirección por +DI/-DI cuando ADX indica tendencia suficiente"
    params_model = ADXDIParams
    params: ADXDIParams

    def warmup_bars(self) -> int:
        return max(3 * self.params.adx_period, self.params.atr_period) + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        a = adx(data, p.adx_period)
        strong = a["adx"] >= p.adx_threshold
        if p.require_adx_rising:
            strong &= a["adx"] > a["adx"].shift(1)
        spread = a["plus_di"] - a["minus_di"]
        bull = strong & (spread > p.di_margin)
        bear = strong & (spread < -p.di_margin)
        weak = a["adx"] < p.adx_exit if p.exit_on_weak_trend else pd.Series(False, index=a.index)
        bull_edge = bull & ~bull.shift(1, fill_value=False)
        bear_edge = bear & ~bear.shift(1, fill_value=False)
        return Events(
            long_entry=bull_edge,
            short_entry=bear_edge,
            long_exit=(spread < 0) | weak,
            short_exit=(spread > 0) | weak,
            conviction=(a["adx"] / 50).clip(0, 1),
        )
