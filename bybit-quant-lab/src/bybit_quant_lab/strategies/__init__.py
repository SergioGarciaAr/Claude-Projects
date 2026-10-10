"""Estrategias registradas. Importar este paquete registra las diez estrategias."""

from bybit_quant_lab.strategies import (  # noqa: F401  (registro por efecto de importación)
    adx_di,
    bollinger_reversion,
    donchian_breakout,
    ema_crossover,
    macd_momentum,
    obv_trend,
    rsi_reversion,
    stoch_rsi,
    volume_spike,
    vwap_deviation,
)
from bybit_quant_lab.strategies.base import (
    SIGNAL_COLUMNS,
    Category,
    Events,
    Signal,
    Strategy,
    StrategyParams,
    events_to_state,
)
from bybit_quant_lab.strategies.registry import (
    available_strategies,
    create_strategy,
    get_strategy_class,
    register,
)

__all__ = [
    "SIGNAL_COLUMNS",
    "Category",
    "Events",
    "Signal",
    "Strategy",
    "StrategyParams",
    "available_strategies",
    "create_strategy",
    "events_to_state",
    "get_strategy_class",
    "register",
]
