"""Temporalidades soportadas y su correspondencia con los intervalos de Bybit V5."""

from __future__ import annotations

import pandas as pd

#: Temporalidad interna -> (intervalo Bybit, minutos)
TIMEFRAMES: dict[str, tuple[str, int]] = {
    "1m": ("1", 1),
    "5m": ("5", 5),
    "15m": ("15", 15),
    "30m": ("30", 30),
    "1h": ("60", 60),
    "4h": ("240", 240),
    "1d": ("D", 1440),
}

MINUTES_PER_YEAR = 365 * 24 * 60  # mercado cripto 24/7, año de 365 días


def validate_timeframe(timeframe: str) -> str:
    """Valida y devuelve la temporalidad; lanza ``ValueError`` si no es soportada."""
    if timeframe not in TIMEFRAMES:
        raise ValueError(f"Temporalidad no soportada: {timeframe!r}. Opciones: {list(TIMEFRAMES)}")
    return timeframe


def timeframe_minutes(timeframe: str) -> int:
    """Duración de una vela en minutos."""
    return TIMEFRAMES[validate_timeframe(timeframe)][1]


def timeframe_delta(timeframe: str) -> pd.Timedelta:
    """Duración de una vela como ``Timedelta``."""
    return pd.Timedelta(minutes=timeframe_minutes(timeframe))


def bybit_interval(timeframe: str) -> str:
    """Código de intervalo de Bybit V5 para la temporalidad."""
    return TIMEFRAMES[validate_timeframe(timeframe)][0]


def bars_per_year(timeframe: str) -> float:
    """Número de velas por año (365 días, 24 h)."""
    return MINUTES_PER_YEAR / timeframe_minutes(timeframe)
