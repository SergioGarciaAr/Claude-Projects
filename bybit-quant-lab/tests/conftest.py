"""Fixtures compartidos. Todos los datos son sintéticos y deterministas."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from bybit_quant_lab.config import AppConfig
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies.base import empty_signal_frame


@pytest.fixture(scope="session")
def synth() -> pd.DataFrame:
    """3000 velas de 1h sintéticas (semilla fija)."""
    return generate_synthetic_ohlcv(bars=3000, timeframe="1h", seed=7)


def make_bars(
    closes: list[float],
    spread: float = 0.5,
    start: str = "2024-01-01",
    freq: str = "1h",
    volume: float = 100.0,
) -> pd.DataFrame:
    """Velas con open = close previo y mechas de ``spread`` (para casos controlados)."""
    closes_arr = np.asarray(closes, dtype=float)
    opens = np.r_[closes_arr[0], closes_arr[:-1]]
    idx = pd.date_range(start, periods=len(closes_arr), freq=freq, tz="UTC", name="open_time")
    return pd.DataFrame(
        {
            "open": opens,
            "high": np.maximum(opens, closes_arr) + spread,
            "low": np.minimum(opens, closes_arr) - spread,
            "close": closes_arr,
            "volume": volume,
        },
        index=idx,
    )


def manual_signals(
    index: pd.Index,
    signal: dict[int, int],
    stop: float = 5.0,
    tp: float | None = None,
    trail: float | None = None,
) -> pd.DataFrame:
    """Señales fijadas a mano: ``signal`` mapea posición -> objetivo (se mantiene hasta cambio)."""
    sig = empty_signal_frame(index)
    values = np.zeros(len(index), dtype=np.int64)
    current = 0
    for i in range(len(index)):
        current = signal.get(i, current)
        values[i] = current
    sig["signal"] = values
    sig["conviction"] = np.where(values != 0, 1.0, 0.0)
    sig["stop_distance"] = stop
    sig["take_profit_distance"] = tp if tp is not None else np.nan
    sig["trailing_distance"] = trail if trail is not None else np.nan
    return sig


def zero_cost_config(**risk: object) -> AppConfig:
    """Configuración sin costes ni límites restrictivos, para verificar aritmética."""
    base_risk = {
        "max_symbol_exposure": 100.0,
        "max_leverage": 100.0,
        "margin_reserve": 0.0,
        "max_daily_loss": 1.0,
        "max_drawdown": 1.0,
        "max_consecutive_losses": 1000,
    }
    base_risk.update(risk)
    return AppConfig.model_validate(
        {
            "costs": {"taker_fee": 0.0, "maker_fee": 0.0, "slippage_bps": 0.0, "use_funding": True},
            "execution": {"leverage": 10.0, "simulate_liquidation": False},
            "risk": base_risk,
        }
    )
