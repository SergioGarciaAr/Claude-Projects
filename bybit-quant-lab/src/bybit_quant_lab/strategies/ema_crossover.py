"""Estrategia 4 — EMA Crossover + Trend Filter (categoría tendencia).

Hipótesis: el cruce de una EMA rápida sobre una lenta, alineado con una EMA larga y con
fuerza de tendencia suficiente (ADX) o volatilidad mínima (ATR %), captura tendencias.
Los filtros reducen los cruces repetidos en mercados laterales.
"""

from __future__ import annotations

from typing import Literal

import pandas as pd
from pydantic import Field, model_validator

from bybit_quant_lab.indicators import adx, atr, crossover, crossunder, ema
from bybit_quant_lab.strategies.base import Category, Events, Strategy, StrategyParams
from bybit_quant_lab.strategies.registry import register


class EMACrossoverParams(StrategyParams):
    """Parámetros de EMA Crossover."""

    fast: int = Field(12, ge=2, le=500)
    slow: int = Field(26, ge=3, le=1000)
    trend_ema: int | None = Field(200, ge=10, le=2000)
    regime_filter: Literal["none", "adx", "atr"] = "adx"
    adx_period: int = Field(14, ge=2, le=200)
    adx_min: float = Field(20.0, ge=0, le=100)
    atr_pct_min: float = Field(0.002, ge=0)

    @model_validator(mode="after")
    def _fast_lt_slow(self) -> EMACrossoverParams:
        if self.fast >= self.slow:
            raise ValueError("fast debe ser menor que slow")
        return self


@register
class EMACrossoverStrategy(Strategy):
    """Cruce de EMAs con filtro de tendencia larga y de régimen."""

    name = "ema_crossover"
    category = Category.TREND
    description = "Cruce EMA rápida/lenta con filtro de tendencia y de lateralidad"
    params_model = EMACrossoverParams
    params: EMACrossoverParams

    def warmup_bars(self) -> int:
        p = self.params
        return max(p.slow, p.trend_ema or 0, 2 * p.adx_period, p.atr_period) + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        fast, slow = ema(c, p.fast), ema(c, p.slow)
        up_ok = pd.Series(True, index=c.index)
        dn_ok = pd.Series(True, index=c.index)
        if p.trend_ema:
            trend = ema(c, p.trend_ema)
            up_ok, dn_ok = c > trend, c < trend
        adx_df = adx(data, p.adx_period)
        if p.regime_filter == "adx":
            regime = adx_df["adx"] >= p.adx_min
        elif p.regime_filter == "atr":
            regime = atr(data, p.atr_period) / c >= p.atr_pct_min
        else:
            regime = pd.Series(True, index=c.index)
        return Events(
            long_entry=crossover(fast, slow) & up_ok & regime,
            short_entry=crossunder(fast, slow) & dn_ok & regime,
            long_exit=crossunder(fast, slow),
            short_exit=crossover(fast, slow),
            conviction=(adx_df["adx"] / 50).clip(0, 1),
        )
