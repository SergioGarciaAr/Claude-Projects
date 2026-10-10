"""Modelo de costes: comisiones y slippage.

Todas las ejecuciones simuladas son órdenes a mercado o stops/TP disparados que se ejecutan
a mercado (comportamiento por defecto de TP/SL en Bybit), por lo que pagan comisión taker y
sufren slippage adverso de ``slippage_bps``.
"""

from __future__ import annotations

from dataclasses import dataclass

from bybit_quant_lab.config.models import CostConfig


@dataclass(frozen=True)
class CostModel:
    """Comisiones y slippage."""

    taker_fee: float
    maker_fee: float
    slippage_bps: float

    @classmethod
    def from_config(cls, cfg: CostConfig) -> CostModel:
        """Construye el modelo desde ``CostConfig``."""
        return cls(cfg.taker_fee, cfg.maker_fee, cfg.slippage_bps)

    @property
    def slip(self) -> float:
        """Slippage como fracción."""
        return self.slippage_bps / 10_000

    def fill_price(self, reference: float, direction: int) -> float:
        """Precio con slippage adverso; ``direction`` = +1 compra, -1 venta."""
        return reference * (1 + self.slip * direction)

    def fee(self, notional: float, taker: bool = True) -> float:
        """Comisión sobre el nocional (``qty * precio_ejecución``)."""
        return abs(notional) * (self.taker_fee if taker else self.maker_fee)
