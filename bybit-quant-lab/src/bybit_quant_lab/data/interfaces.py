"""Interfaces para fuentes de datos futuras.

Definen el contrato de funding, interés abierto, bid/ask y operaciones individuales. Solo
``BybitPublicClient.fetch_funding_history`` implementa por ahora una de ellas. El resto se
dejan como protocolos: el sistema **no** simula disponer de esos datos.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

import pandas as pd


@runtime_checkable
class FundingSource(Protocol):
    """Fuente de tasas de funding históricas (índice: ``funding_time`` UTC)."""

    def fetch_funding_history(
        self, symbol: str, start: pd.Timestamp, end: pd.Timestamp
    ) -> pd.Series:
        """Serie ``funding_rate`` por marca de liquidación de funding."""
        ...


@runtime_checkable
class OpenInterestSource(Protocol):
    """Fuente de interés abierto histórico (pendiente de implementar)."""

    def fetch_open_interest(
        self, symbol: str, start: pd.Timestamp, end: pd.Timestamp, interval: str
    ) -> pd.Series:
        """Serie de interés abierto."""
        ...


@runtime_checkable
class QuoteSource(Protocol):
    """Fuente de mejores bid/ask históricos (pendiente de implementar)."""

    def fetch_quotes(self, symbol: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
        """DataFrame con columnas ``bid``, ``ask``, ``bid_size``, ``ask_size``."""
        ...


@runtime_checkable
class TradeSource(Protocol):
    """Fuente de operaciones individuales históricas (pendiente de implementar)."""

    def fetch_trades(self, symbol: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
        """DataFrame con ``price``, ``size``, ``side``."""
        ...
