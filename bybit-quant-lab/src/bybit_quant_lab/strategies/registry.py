"""Registro de estrategias por nombre."""

from __future__ import annotations

from typing import Any

from bybit_quant_lab.strategies.base import Strategy

_REGISTRY: dict[str, type[Strategy]] = {}


def register(cls: type[Strategy]) -> type[Strategy]:
    """Decorador que registra una estrategia por su atributo ``name``."""
    if cls.name in _REGISTRY and _REGISTRY[cls.name] is not cls:
        raise ValueError(f"Estrategia duplicada: {cls.name}")
    _REGISTRY[cls.name] = cls
    return cls


def available_strategies() -> list[str]:
    """Nombres de estrategias registradas, en orden de registro."""
    return list(_REGISTRY)


def get_strategy_class(name: str) -> type[Strategy]:
    """Clase de estrategia por nombre."""
    try:
        return _REGISTRY[name]
    except KeyError as exc:
        raise KeyError(
            f"Estrategia desconocida: {name!r}. Disponibles: {available_strategies()}"
        ) from exc


def create_strategy(name: str, params: dict[str, Any] | None = None) -> Strategy:
    """Instancia una estrategia registrada con parámetros validados."""
    return get_strategy_class(name)(params or {})
