"""Estrategia 1 — Volume Spike + Price Confirmation (categoría volumen).

Hipótesis: un volumen anormal **acompañado** de una vela direccional fuerte que rompe el
rango de la vela anterior indica participación en la dirección del movimiento. El pico de
volumen por sí solo no define dirección: sin confirmación de precio no hay señal.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from pydantic import Field

from bybit_quant_lab.indicators import atr, ema, sma
from bybit_quant_lab.strategies.base import Category, Events, Strategy, StrategyParams
from bybit_quant_lab.strategies.registry import register


class VolumeSpikeParams(StrategyParams):
    """Parámetros de Volume Spike."""

    volume_window: int = Field(20, ge=2, le=1000)
    spike_mult: float = Field(2.5, gt=1, le=50)
    min_body_ratio: float = Field(0.5, ge=0, le=1)
    require_range_break: bool = True
    min_atr_pct: float = Field(0.0, ge=0)
    max_atr_pct: float | None = Field(None, gt=0)
    exit_ema: int = Field(20, ge=2, le=500)
    max_holding_bars: int | None = Field(48, ge=1)


@register
class VolumeSpikeStrategy(Strategy):
    """Pico de volumen respecto a SMA previa + vela de confirmación + filtro de volatilidad."""

    name = "volume_spike"
    category = Category.VOLUME
    description = "Pico de volumen confirmado por vela direccional y ruptura del rango previo"
    params_model = VolumeSpikeParams
    params: VolumeSpikeParams

    def warmup_bars(self) -> int:
        p = self.params
        return max(p.volume_window + 1, p.exit_ema, p.atr_period) + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        o, h, low, c, v = (data[k] for k in ("open", "high", "low", "close", "volume"))
        vol_ma = sma(v, p.volume_window).shift(1)  # solo velas anteriores
        ratio = v / vol_ma.replace(0, np.nan)
        spike = ratio > p.spike_mult
        rng = (h - low).replace(0, np.nan)
        body_ratio = (c - o).abs() / rng
        strong = body_ratio >= p.min_body_ratio
        atr_pct = atr(data, p.atr_period) / c
        vol_ok = atr_pct >= p.min_atr_pct
        if p.max_atr_pct is not None:
            vol_ok &= atr_pct <= p.max_atr_pct
        bull = (c > o) & strong
        bear = (c < o) & strong
        if p.require_range_break:
            bull &= c > h.shift(1)
            bear &= c < low.shift(1)
        trend_exit = ema(c, p.exit_ema)
        conviction = (ratio / (2 * p.spike_mult)).clip(0, 1) * body_ratio.fillna(0)
        return Events(
            long_entry=spike & bull & vol_ok,
            short_entry=spike & bear & vol_ok,
            long_exit=c < trend_exit,
            short_exit=c > trend_exit,
            conviction=conviction,
        )
