"""Resolución de stops, objetivos y liquidación con velas OHLC.

Las velas OHLC no revelan el orden real de los precios dentro de la vela. Reglas aplicadas:

1. **Gap en apertura**: si la apertura ya está más allá de un nivel (stop, liquidación u
   objetivo), la orden se ejecuta a la apertura (precio realmente disponible).
2. **Intravela, stop primero**: si en la misma vela se tocan el nivel adverso (stop o
   liquidación) y el objetivo, se asume que se tocó **primero el adverso**. Nunca se asume
   el resultado más favorable.
3. **Liquidación frente a stop**: el nivel adverso efectivo es el más cercano al precio de
   entrada (para largos, ``max(stop, liquidación)``). Si ambos coinciden prevalece la
   liquidación.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExitCheck:
    """Salida detectada: precio de referencia (antes de slippage) y motivo."""

    price: float
    reason: str


def _adverse(side: int, stop: float | None, liq: float | None) -> tuple[float | None, str]:
    levels = [
        (lvl, name) for lvl, name in ((liq, "liquidation"), (stop, "stop_loss")) if lvl is not None
    ]
    if not levels:
        return None, ""
    # Largo: el nivel más alto se toca primero al caer; corto: el más bajo.
    best = max(levels, key=lambda x: x[0]) if side > 0 else min(levels, key=lambda x: x[0])
    return best


def check_gap_exit(
    side: int, open_: float, stop: float | None, take_profit: float | None, liq: float | None
) -> ExitCheck | None:
    """Comprueba si la apertura ya ha superado algún nivel."""
    level, name = _adverse(side, stop, liq)
    if level is not None and (open_ <= level if side > 0 else open_ >= level):
        return ExitCheck(open_, f"{name}_gap")
    if take_profit is not None and (open_ >= take_profit if side > 0 else open_ <= take_profit):
        return ExitCheck(open_, "take_profit_gap")
    return None


def check_intrabar_exit(
    side: int,
    high: float,
    low: float,
    stop: float | None,
    take_profit: float | None,
    liq: float | None,
) -> ExitCheck | None:
    """Comprueba la vela con la regla conservadora *stop primero*."""
    level, name = _adverse(side, stop, liq)
    if level is not None and (low <= level if side > 0 else high >= level):
        return ExitCheck(level, name)
    if take_profit is not None and (high >= take_profit if side > 0 else low <= take_profit):
        return ExitCheck(take_profit, "take_profit")
    return None
