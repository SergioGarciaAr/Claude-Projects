"""Interfaz común de estrategias y conversión de eventos en señales normalizadas.

Semántica de la salida de ``Strategy.generate_signals`` (una fila por vela, mismo índice):

``signal``
    Exposición **objetivo** decidida al cierre de la vela: ``1`` LONG, ``-1`` SHORT, ``0`` FLAT.
    Nunca se ejecuta en la misma vela: el motor la ejecuta en la apertura siguiente.
``conviction``
    Puntuación en ``[0, 1]`` (0 cuando ``signal == 0``). Es una medida de intensidad del
    setup definida por cada estrategia, **no** una probabilidad ni una predicción calibrada.
``stop_distance``
    Distancia (en precio) del stop de estrategia, por defecto ``ATR * stop_atr_mult``.
``take_profit_distance``
    Distancia del objetivo (``stop_distance * take_profit_r``) o NaN si no hay objetivo.
``trailing_distance``
    Distancia del trailing stop (``ATR * trailing_atr_mult``) o NaN si no se usa.

Las estrategias producen *eventos* (entradas y salidas). ``events_to_state`` los convierte en
un estado persistente con reglas explícitas: conflicto de entradas en la misma vela -> FLAT,
reversión directa si hay entrada opuesta, salida por tiempo máximo y enfriamiento.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum, StrEnum
from typing import Any, ClassVar

import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field

from bybit_quant_lab.indicators import atr

SIGNAL_COLUMNS: tuple[str, ...] = (
    "signal",
    "conviction",
    "stop_distance",
    "take_profit_distance",
    "trailing_distance",
)
REQUIRED_COLUMNS: tuple[str, ...] = ("open", "high", "low", "close", "volume")


class Signal(IntEnum):
    """Señal normalizada."""

    SHORT = -1
    FLAT = 0
    LONG = 1


class Category(StrEnum):
    """Categoría de estrategia (usada por el consenso por categorías)."""

    VOLUME = "volume"
    TREND = "trend"
    INDICATOR = "indicator"


class StrategyParams(BaseModel):
    """Parámetros comunes de salida y gestión de la operación."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    atr_period: int = Field(14, ge=2, le=500)
    stop_atr_mult: float = Field(2.0, gt=0, le=20)
    take_profit_r: float | None = Field(2.0, gt=0, le=50)
    trailing_atr_mult: float | None = Field(None, gt=0, le=20)
    max_holding_bars: int | None = Field(None, ge=1)
    cooldown_bars: int = Field(0, ge=0)
    allow_short: bool = True


@dataclass
class Events:
    """Eventos booleanos por vela producidos por una estrategia."""

    long_entry: pd.Series
    short_entry: pd.Series
    long_exit: pd.Series
    short_exit: pd.Series
    conviction: pd.Series


class Strategy(ABC):
    """Clase base de todas las estrategias. No conoce el motor de backtesting."""

    name: ClassVar[str] = "base"
    category: ClassVar[Category] = Category.INDICATOR
    description: ClassVar[str] = ""
    params_model: ClassVar[type[StrategyParams]] = StrategyParams

    def __init__(self, params: StrategyParams | dict[str, Any] | None = None, **kwargs: Any):
        data = params.model_dump() if isinstance(params, StrategyParams) else dict(params or {})
        data.update(kwargs)
        self.params = self.params_model.model_validate(data)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.params.model_dump()})"

    @abstractmethod
    def warmup_bars(self) -> int:
        """Velas necesarias antes de que los indicadores sean válidos."""

    @abstractmethod
    def compute_events(self, data: pd.DataFrame) -> Events:
        """Calcula eventos de entrada/salida usando solo información hasta cada vela."""

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Devuelve el DataFrame de señales normalizadas (ver docstring del módulo)."""
        validate_input(data)
        if data.empty:
            return empty_signal_frame(data.index)
        ev = self.compute_events(data)
        p = self.params
        long_entry, short_entry = _clean_bool(ev.long_entry), _clean_bool(ev.short_entry)
        if not p.allow_short:
            short_entry = pd.Series(False, index=data.index)
        atr_ = atr(data, p.atr_period)
        stop = atr_ * p.stop_atr_mult
        # Sin stop válido (calentamiento del ATR) no se permite ENTRAR. Se aplica a los eventos,
        # antes de la máquina de estados, para no crear transiciones ficticias después.
        valid_stop = stop.notna() & (stop > 0)
        long_entry &= valid_stop
        short_entry &= valid_stop
        state = events_to_state(
            long_entry,
            short_entry,
            _clean_bool(ev.long_exit),
            _clean_bool(ev.short_exit),
            max_holding_bars=p.max_holding_bars,
            cooldown_bars=p.cooldown_bars,
        )
        out = pd.DataFrame(index=data.index)
        out["signal"] = state.astype("int64")
        conv = ev.conviction.reindex(data.index).astype("float64").clip(0, 1).fillna(0.0)
        out["conviction"] = conv.where(out["signal"] != 0, 0.0)
        out["stop_distance"] = stop
        out["take_profit_distance"] = stop * p.take_profit_r if p.take_profit_r else np.nan
        out["trailing_distance"] = atr_ * p.trailing_atr_mult if p.trailing_atr_mult else np.nan
        # Sin stop válido (ATR aún no disponible) no se permite abrir: se fuerza FLAT.
        out.loc[out["stop_distance"].isna() | (out["stop_distance"] <= 0), "signal"] = 0
        out.loc[out["signal"] == 0, "conviction"] = 0.0
        return out


def validate_input(data: pd.DataFrame) -> None:
    """Comprueba columnas e índice temporal; lanza ``ValueError``/``TypeError`` si no cumple."""
    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        raise ValueError(f"Faltan columnas OHLCV: {missing}")
    if not isinstance(data.index, pd.DatetimeIndex):
        raise TypeError("El índice debe ser DatetimeIndex")
    if len(data) and not data.index.is_monotonic_increasing:
        raise ValueError("El índice debe estar ordenado cronológicamente")


def empty_signal_frame(index: pd.Index) -> pd.DataFrame:
    """DataFrame de señales vacío/neutral con las columnas estándar."""
    out = pd.DataFrame(index=index)
    out["signal"] = pd.Series(0, index=index, dtype="int64")
    for col in SIGNAL_COLUMNS[1:]:
        out[col] = pd.Series(np.nan if col != "conviction" else 0.0, index=index, dtype="float64")
    return out


def _clean_bool(s: pd.Series) -> pd.Series:
    return s.fillna(False).astype(bool)


def events_to_state(
    long_entry: pd.Series,
    short_entry: pd.Series,
    long_exit: pd.Series,
    short_exit: pd.Series,
    max_holding_bars: int | None = None,
    cooldown_bars: int = 0,
) -> pd.Series:
    """Convierte eventos en estado objetivo persistente (-1/0/1).

    Reglas (evaluadas al cierre de cada vela, en este orden):

    1. En posición LONG: una entrada SHORT revierte a SHORT; una salida LONG o alcanzar
       ``max_holding_bars`` pasa a FLAT.
    2. En FLAT: si hay entradas LONG y SHORT simultáneas -> se ignoran (conflicto); si no,
       se entra si han pasado ``cooldown_bars`` desde la última salida.
    3. Una salida en la misma vela que una entrada del mismo lado prevalece (no se entra).
    """
    le, se = long_entry.to_numpy(bool), short_entry.to_numpy(bool)
    lx, sx = long_exit.to_numpy(bool), short_exit.to_numpy(bool)
    n = len(le)
    out = np.zeros(n, dtype=np.int64)
    state, held, since_exit = 0, 0, cooldown_bars
    for i in range(n):
        if state == 1:
            held += 1
            if se[i] and not le[i]:
                state, held = -1, 0
            elif lx[i] or (max_holding_bars is not None and held >= max_holding_bars):
                state, since_exit = 0, 0
        elif state == -1:
            held += 1
            if le[i] and not se[i]:
                state, held = 1, 0
            elif sx[i] or (max_holding_bars is not None and held >= max_holding_bars):
                state, since_exit = 0, 0
        else:
            since_exit += 1
            if since_exit > cooldown_bars:
                if le[i] and not se[i] and not lx[i]:
                    state, held = 1, 0
                elif se[i] and not le[i] and not sx[i]:
                    state, held = -1, 0
        out[i] = state
    return pd.Series(out, index=long_entry.index, name="signal")


def rearm_events(events: pd.Series, reset: pd.Series) -> pd.Series:
    """Conserva un evento solo si ``reset`` ha ocurrido desde el último evento conservado.

    Evita contabilizar varias veces señales prácticamente idénticas dentro de un mismo
    movimiento (por ejemplo, varios cruces del Stochastic RSI en la misma zona extrema).
    """
    ev, rs = _clean_bool(events).to_numpy(), _clean_bool(reset).to_numpy()
    out = np.zeros(len(ev), dtype=bool)
    armed = True
    for i in range(len(ev)):
        if rs[i]:
            armed = True
        if ev[i] and armed:
            out[i] = True
            armed = False
    return pd.Series(out, index=events.index)


def infer_bar_delta(index: pd.DatetimeIndex) -> pd.Timedelta:
    """Infiere la duración de vela como la moda de las diferencias del índice."""
    if len(index) < 2:
        raise ValueError("Se necesitan al menos 2 velas para inferir la temporalidad")
    diffs = pd.Series(index[1:] - index[:-1])
    return pd.Timedelta(diffs.mode().iloc[0])
