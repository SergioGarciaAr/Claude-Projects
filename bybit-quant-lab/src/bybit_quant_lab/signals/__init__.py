"""Combinación de señales, regímenes de mercado y análisis de redundancia."""

from bybit_quant_lab.signals.combiners import CombinationConfig, combine_signals, fit_weights
from bybit_quant_lab.signals.redundancy import (
    select_non_redundant,
    signal_agreement,
    signal_correlation,
)
from bybit_quant_lab.signals.regime import RegimeConfig, classify_regime

__all__ = [
    "CombinationConfig",
    "RegimeConfig",
    "classify_regime",
    "combine_signals",
    "fit_weights",
    "select_non_redundant",
    "signal_agreement",
    "signal_correlation",
]
