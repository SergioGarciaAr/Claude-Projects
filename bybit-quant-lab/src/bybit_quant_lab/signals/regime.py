"""Clasificación causal del régimen de mercado.

Tres dimensiones independientes, calculadas solo con datos hasta cada vela:

* ``trend``: ``trend`` si ``ADX >= adx_trend``, si no ``range``.
* ``volatility``: ``high_vol`` si el percentil del ATR % respecto a las ``vol_window`` velas
  anteriores es ``>= high_vol_pct``; ``low_vol`` si es ``<= low_vol_pct``; si no ``normal_vol``.
* ``liquidity``: ``low_liq`` si el volumen relativo a la mediana de las ``liq_window`` velas
  anteriores es ``< low_liq_ratio``; si no ``normal_liq``. Es una aproximación por volumen: sin
  datos de libro de órdenes no se mide la liquidez real.

Durante el calentamiento las dimensiones valen ``unknown``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field

from bybit_quant_lab.indicators import adx, atr, rolling_percentile

REGIME_DIMENSIONS = ("trend", "volatility", "liquidity")


class RegimeConfig(BaseModel):
    """Umbrales del clasificador de régimen."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    adx_period: int = Field(14, ge=2)
    adx_trend: float = Field(25.0, gt=0, le=100)
    atr_period: int = Field(14, ge=2)
    vol_window: int = Field(500, ge=20)
    high_vol_pct: float = Field(0.8, gt=0, le=1)
    low_vol_pct: float = Field(0.2, ge=0, lt=1)
    liq_window: int = Field(200, ge=10)
    low_liq_ratio: float = Field(0.5, gt=0)


def classify_regime(data: pd.DataFrame, config: RegimeConfig | None = None) -> pd.DataFrame:
    """Devuelve columnas ``trend``, ``volatility``, ``liquidity`` y ``label`` (combinada)."""
    cfg = config or RegimeConfig()
    a = adx(data, cfg.adx_period)["adx"]
    trend = np.where(a.isna(), "unknown", np.where(a >= cfg.adx_trend, "trend", "range"))
    atr_pct = atr(data, cfg.atr_period) / data["close"]
    pct = rolling_percentile(atr_pct, cfg.vol_window)
    vol = np.select(
        [pct.isna(), pct >= cfg.high_vol_pct, pct <= cfg.low_vol_pct],
        ["unknown", "high_vol", "low_vol"],
        default="normal_vol",
    )
    med = data["volume"].rolling(cfg.liq_window, min_periods=cfg.liq_window).median().shift(1)
    rel = data["volume"] / med.replace(0, np.nan)
    liq = np.select(
        [rel.isna(), rel < cfg.low_liq_ratio], ["unknown", "low_liq"], default="normal_liq"
    )
    out = pd.DataFrame({"trend": trend, "volatility": vol, "liquidity": liq}, index=data.index)
    out["label"] = out["trend"] + "|" + out["volatility"]
    return out
