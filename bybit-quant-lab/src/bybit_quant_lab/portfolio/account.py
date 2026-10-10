"""Cuenta de margen aislado con una posición como máximo por símbolo.

Contabilidad:

* ``cash`` = capital inicial + PnL realizado - comisiones - funding pagado.
* ``equity(price)`` = ``cash`` + PnL no realizado a ``price``.
* ``used_margin`` = nocional de entrada / apalancamiento.

El apalancamiento solo afecta al margen y al precio de liquidación, **no** al PnL de una
cantidad dada de contratos.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from bybit_quant_lab.portfolio.position import Position


@dataclass
class Account:
    """Estado contable de la simulación."""

    initial_capital: float
    cash: float = 0.0
    position: Position | None = None
    total_fees: float = 0.0
    total_slippage: float = 0.0
    total_funding: float = 0.0
    traded_notional: float = 0.0
    realized_pnl: float = 0.0
    history: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.cash = self.initial_capital

    @property
    def used_margin(self) -> float:
        """Margen inicial bloqueado por la posición abierta."""
        return self.position.margin if self.position else 0.0

    def equity(self, price: float) -> float:
        """Equity mark-to-market."""
        return self.cash + (self.position.unrealized(price) if self.position else 0.0)

    def available_margin(self, price: float) -> float:
        """Equity menos margen usado."""
        return self.equity(price) - self.used_margin
