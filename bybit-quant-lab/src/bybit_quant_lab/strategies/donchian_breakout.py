"""Estrategia 5 — Donchian Breakout + ATR (categoría tendencia).

Hipótesis: un cierre por encima del máximo de las ``channel`` velas **anteriores** (o por
debajo del mínimo) inicia un movimiento direccional. Stops en múltiplos de ATR; salida por
ruptura del canal corto opuesto (``exit_channel``). Filtro opcional de temporalidad superior
(``htf``): solo se usa la última vela superior **cerrada** y su EMA.
"""

from __future__ import annotations

import pandas as pd
from pydantic import Field, model_validator

from bybit_quant_lab.indicators import atr, donchian, higher_timeframe
from bybit_quant_lab.strategies.base import (
    Category,
    Events,
    Strategy,
    StrategyParams,
    infer_bar_delta,
)
from bybit_quant_lab.strategies.registry import register


class DonchianParams(StrategyParams):
    """Parámetros de Donchian Breakout."""

    channel: int = Field(20, ge=2, le=1000)
    exit_channel: int = Field(10, ge=2, le=1000)
    htf: str | None = None
    htf_ema: int = Field(50, ge=2, le=500)
    take_profit_r: float | None = Field(None, gt=0, le=50)
    trailing_atr_mult: float | None = Field(3.0, gt=0, le=20)

    @model_validator(mode="after")
    def _check(self) -> DonchianParams:
        if self.exit_channel > self.channel:
            raise ValueError("exit_channel no debe superar a channel")
        if self.htf is not None:
            pd.Timedelta(self.htf)  # lanza ValueError si el formato no es válido
        return self


@register
class DonchianBreakoutStrategy(Strategy):
    """Ruptura de canal Donchian previo con stop ATR y filtro HTF opcional."""

    name = "donchian_breakout"
    category = Category.TREND
    description = "Ruptura del canal Donchian de velas anteriores con gestión ATR"
    params_model = DonchianParams
    params: DonchianParams

    def warmup_bars(self) -> int:
        p = self.params
        return max(p.channel, p.atr_period) + 2

    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        ch = donchian(data, p.channel)
        ex = donchian(data, p.exit_channel)
        up_ok = pd.Series(True, index=c.index)
        dn_ok = pd.Series(True, index=c.index)
        if p.htf is not None and len(data) >= 2:
            htf = higher_timeframe(
                data,
                infer_bar_delta(pd.DatetimeIndex(data.index)),
                pd.Timedelta(p.htf),
                ema_period=p.htf_ema,
            )
            up_ok = htf["close"] > htf["ema"]
            dn_ok = htf["close"] < htf["ema"]
        width = (ch["upper"] - ch["lower"]).where(lambda w: w > 0)
        conviction = ((c - ch["mid"]).abs() / width).clip(0, 1) * 2
        a = atr(data, p.atr_period)
        return Events(
            long_entry=(c > ch["upper"]) & up_ok & a.notna(),
            short_entry=(c < ch["lower"]) & dn_ok & a.notna(),
            long_exit=c < ex["lower"],
            short_exit=c > ex["upper"],
            conviction=conviction,
        )
