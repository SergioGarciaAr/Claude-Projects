"""Dimensionamiento de posición basado en riesgo.

``qty = (equity * risk_per_trade) / (stop_distance + costes_estimados_por_unidad)``

Los costes estimados por unidad incluyen comisión taker y slippage de entrada y salida. El
resultado se limita por exposición por símbolo, apalancamiento máximo, margen disponible
(respetando la reserva) y tamaño máximo del instrumento, y se redondea **hacia abajo**.
"""

from __future__ import annotations

from dataclasses import dataclass

from bybit_quant_lab.config.models import CostConfig, ExecutionConfig, RiskConfig
from bybit_quant_lab.risk.instruments import InstrumentSpec


@dataclass(frozen=True)
class SizingResult:
    """Resultado del dimensionamiento: ``qty > 0`` o ``qty == 0`` con motivo."""

    qty: float
    reason: str = "ok"
    capped_by: str | None = None


def liquidation_distance(price: float, leverage: float, mmr: float) -> float:
    """Distancia aproximada a liquidación con margen aislado: ``price * (1/lev - mmr)``."""
    return price * max(1.0 / leverage - mmr, 0.0)


def size_position(
    equity: float,
    used_margin: float,
    price: float,
    stop_distance: float,
    risk: RiskConfig,
    execution: ExecutionConfig,
    costs: CostConfig,
    spec: InstrumentSpec,
) -> SizingResult:
    """Cantidad de contratos para entrar a ``price`` con stop a ``stop_distance``."""
    if equity <= 0:
        return SizingResult(0.0, "equity_non_positive")
    if not stop_distance > 0 or price <= 0:
        return SizingResult(0.0, "invalid_stop")
    if execution.simulate_liquidation and stop_distance >= liquidation_distance(
        price, execution.leverage, execution.maintenance_margin_rate
    ):
        return SizingResult(0.0, "stop_beyond_liquidation")
    slip = costs.slippage_bps / 10_000
    per_unit = stop_distance + price * 2 * (costs.taker_fee + slip)
    qty = equity * risk.risk_per_trade / per_unit
    caps = {
        "symbol_exposure": equity * risk.max_symbol_exposure / price,
        "max_leverage": equity * risk.max_leverage / price,
        "available_margin": max(equity * (1 - risk.margin_reserve) - used_margin, 0.0)
        * execution.leverage
        / price,
        "instrument_max_qty": spec.max_qty,
    }
    capped_by = None
    for name, cap in caps.items():
        if cap < qty:
            qty, capped_by = cap, name
    qty = spec.round_qty(qty)
    if qty < spec.min_qty:
        return SizingResult(0.0, "below_min_qty", capped_by)
    if qty * price < spec.min_notional:
        return SizingResult(0.0, "below_min_notional", capped_by)
    return SizingResult(qty, "ok", capped_by)
