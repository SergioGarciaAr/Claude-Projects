"""Contenedor de resultados de un backtest."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class BacktestResult:
    """Resultado completo de una simulación.

    ``equity``: una fila por vela simulada (cierre) con ``equity``, ``cash``, ``unrealized``,
    ``position`` (cantidad con signo), ``margin_used``, ``drawdown`` e ``in_position``.
    ``trades``: una fila por operación cerrada (ver ``TradeRecord``).
    """

    label: str
    symbol: str
    timeframe: str
    initial_capital: float
    equity: pd.DataFrame
    trades: pd.DataFrame
    risk_events: list[dict[str, Any]]
    rejected_signals: list[dict[str, Any]]
    totals: dict[str, float]
    funding_applied: bool
    warnings: list[str] = field(default_factory=list)
    params: dict[str, Any] = field(default_factory=dict)

    @property
    def final_equity(self) -> float:
        """Equity al cierre de la última vela."""
        return float(self.equity["equity"].iloc[-1]) if len(self.equity) else self.initial_capital

    @property
    def start(self) -> pd.Timestamp | None:
        """Primera vela simulada."""
        return self.equity.index[0] if len(self.equity) else None

    @property
    def end(self) -> pd.Timestamp | None:
        """Última vela simulada."""
        return self.equity.index[-1] if len(self.equity) else None
