"""Estrategia 3 — VWAP Deviation + Volume Regime (categoría volumen).

Dos hipótesis **separadas**, seleccionadas con ``mode`` (nunca se mezclan):

* ``reversion``: desviación extrema respecto a VWAP con volumen **no** elevado
  (``rel_volume <= max_rel_volume``) -> se espera retorno hacia VWAP.
* ``continuation``: desviación extrema con volumen **elevado** (``rel_volume >=
  min_rel_volume``) -> se espera continuación en la dirección de la desviación.

VWAP: ``rolling`` (ventana de ``vwap_window`` velas) o ``session`` (anclado a sesiones UTC de
duración ``session``, por defecto el día UTC 00:00-24:00, ya que el mercado opera 24/7).
La desviación se normaliza con la desviación típica de las ``dev_window`` velas anteriores.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd
from pydantic import Field

from bybit_quant_lab.indicators import sma, vwap_rolling, vwap_session
from bybit_quant_lab.strategies.base import Category, Events, Strategy, StrategyParams
from bybit_quant_lab.strategies.registry import register


class VWAPDeviationParams(StrategyParams):
    """Parámetros de VWAP Deviation."""

    mode: Literal["reversion", "continuation"] = "reversion"
    vwap_type: Literal["rolling", "session"] = "rolling"
    vwap_window: int = Field(96, ge=2, le=5000)
    session: str = "1D"
    dev_window: int = Field(100, ge=10, le=5000)
    entry_z: float = Field(2.0, gt=0, le=10)
    exit_z: float = Field(0.5, ge=0, le=10)
    volume_window: int = Field(50, ge=2, le=5000)
    max_rel_volume: float = Field(1.5, gt=0)
    min_rel_volume: float = Field(1.5, gt=0)
    take_profit_r: float | None = Field(None, gt=0, le=50)


@register
class VWAPDeviationStrategy(Strategy):
    """Desviación normalizada respecto a VWAP filtrada por régimen de volumen."""

    name = "vwap_deviation"
    category = Category.VOLUME
    description = (
        "Desviación del precio respecto a VWAP con régimen de volumen (reversión o continuación)"
    )
    params_model = VWAPDeviationParams
    params: VWAPDeviationParams

    def warmup_bars(self) -> int:
        p = self.params
        base = p.vwap_window if p.vwap_type == "rolling" else 1
        return base + p.dev_window + max(p.volume_window, p.atr_period) + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c, v = data["close"], data["volume"]
        vw = (
            vwap_rolling(data, p.vwap_window)
            if p.vwap_type == "rolling"
            else vwap_session(data, p.session)
        )
        dev = c - vw
        std = dev.rolling(p.dev_window, min_periods=p.dev_window).std().shift(1)
        z = dev / std.replace(0, np.nan)
        rel_vol = v / sma(v, p.volume_window).shift(1).replace(0, np.nan)
        conviction = ((z.abs() - p.entry_z) / p.entry_z).clip(0, 1)
        if p.mode == "reversion":
            quiet = rel_vol <= p.max_rel_volume
            return Events(
                long_entry=(z <= -p.entry_z) & quiet,
                short_entry=(z >= p.entry_z) & quiet,
                long_exit=z >= -p.exit_z,
                short_exit=z <= p.exit_z,
                conviction=conviction,
            )
        active = rel_vol >= p.min_rel_volume
        return Events(
            long_entry=(z >= p.entry_z) & active,
            short_entry=(z <= -p.entry_z) & active,
            long_exit=z <= p.exit_z,
            short_exit=z >= -p.exit_z,
            conviction=conviction,
        )
