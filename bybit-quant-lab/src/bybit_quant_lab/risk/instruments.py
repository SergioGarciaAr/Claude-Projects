"""Especificaciones de instrumentos (precisión, tamaños mínimos y máximos).

Los valores por defecto son **referencias** para BTCUSDT y ETHUSDT lineales y deben
contrastarse con ``GET /v5/market/instruments-info`` (``BybitPublicClient.fetch_instrument_info``
y ``spec_from_bybit``), ya que Bybit puede modificarlos.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class InstrumentSpec:
    """Restricciones de cantidad y precio de un contrato lineal."""

    symbol: str
    tick_size: float
    qty_step: float
    min_qty: float
    max_qty: float
    min_notional: float = 5.0
    verified: bool = False

    def round_qty(self, qty: float) -> float:
        """Redondea hacia abajo al múltiplo de ``qty_step`` (nunca aumenta el riesgo)."""
        if qty <= 0:
            return 0.0
        steps = math.floor(qty / self.qty_step + 1e-9)
        decimals = max(0, -math.floor(math.log10(self.qty_step)))
        return round(steps * self.qty_step, decimals)


DEFAULT_SPECS: dict[str, InstrumentSpec] = {
    "BTCUSDT": InstrumentSpec(
        "BTCUSDT", tick_size=0.1, qty_step=0.001, min_qty=0.001, max_qty=100.0
    ),
    "ETHUSDT": InstrumentSpec(
        "ETHUSDT", tick_size=0.01, qty_step=0.01, min_qty=0.01, max_qty=1000.0
    ),
}


def get_spec(symbol: str) -> InstrumentSpec:
    """Especificación por defecto del símbolo (genérica y no verificada si no existe)."""
    spec = DEFAULT_SPECS.get(symbol.upper())
    if spec is not None:
        return spec
    return InstrumentSpec(
        symbol.upper(), tick_size=0.0001, qty_step=0.001, min_qty=0.001, max_qty=1e9
    )


def spec_from_bybit(info: dict[str, Any]) -> InstrumentSpec:
    """Construye la especificación a partir de un registro de ``instruments-info``."""
    lot, price = info["lotSizeFilter"], info["priceFilter"]
    return InstrumentSpec(
        symbol=str(info["symbol"]),
        tick_size=float(price["tickSize"]),
        qty_step=float(lot["qtyStep"]),
        min_qty=float(lot["minOrderQty"]),
        max_qty=float(lot.get("maxMktOrderQty") or lot["maxOrderQty"]),
        min_notional=float(lot.get("minNotionalValue") or 0.0),
        verified=True,
    )
