"""Posición abierta y registro de operación cerrada."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd


@dataclass
class Position:
    """Posición abierta en margen aislado (una por símbolo)."""

    side: int
    qty: float
    entry_price: float
    entry_time: pd.Timestamp
    entry_bar: int
    stop: float | None
    take_profit: float | None
    trailing_distance: float | None
    liquidation_price: float | None
    margin: float
    entry_fee: float
    entry_slippage: float
    conviction: float = 0.0
    funding: float = 0.0
    extreme: float = 0.0
    equity_at_entry: float = 0.0
    regime: str = ""

    @property
    def notional_entry(self) -> float:
        """Nocional a precio de entrada."""
        return self.qty * self.entry_price

    def unrealized(self, price: float) -> float:
        """PnL no realizado a ``price`` (sin costes de salida)."""
        return self.side * (price - self.entry_price) * self.qty

    def update_trailing(self, close: float) -> None:
        """Actualiza el trailing stop con el cierre (solo puede mejorar el stop)."""
        if self.trailing_distance is None:
            return
        if self.side > 0:
            self.extreme = max(self.extreme, close)
            candidate = self.extreme - self.trailing_distance
            self.stop = candidate if self.stop is None else max(self.stop, candidate)
        else:
            self.extreme = min(self.extreme, close)
            candidate = self.extreme + self.trailing_distance
            self.stop = candidate if self.stop is None else min(self.stop, candidate)


@dataclass
class TradeRecord:
    """Operación cerrada con desglose de costes."""

    symbol: str
    side: str
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    entry_bar: int
    exit_bar: int
    qty: float
    entry_price: float
    exit_price: float
    gross_pnl: float
    fees: float
    slippage_cost: float
    funding: float
    net_pnl: float
    return_on_equity: float
    bars_held: int
    exit_reason: str
    conviction: float
    equity_at_entry: float
    regime: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serializa la operación."""
        return asdict(self)
