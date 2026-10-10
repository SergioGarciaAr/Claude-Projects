"""Modelos Pydantic de configuración.

Todos los porcentajes se expresan como fracción decimal (0.01 = 1 %).
Los valores por defecto son referencias de investigación, no recomendaciones operativas.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class DataConfig(_Strict):
    """Origen y almacenamiento de datos de mercado."""

    data_dir: Path = Path("data")
    base_url: str = "https://api.bybit.com"
    category: Literal["linear"] = "linear"
    symbols: tuple[str, ...] = ("BTCUSDT", "ETHUSDT")
    timeframes: tuple[str, ...] = ("5m", "15m", "1h", "4h")
    request_limit: int = Field(1000, ge=1, le=1000)
    max_retries: int = Field(5, ge=0, le=20)
    backoff_seconds: float = Field(1.0, ge=0)
    min_request_interval: float = Field(0.05, ge=0)
    timeout_seconds: float = Field(15.0, gt=0)


class CostConfig(_Strict):
    """Modelo de costes.

    ``taker_fee``/``maker_fee``: tarifas base publicadas por Bybit para perpetuos USDT
    (0.055 % / 0.02 %, nivel no VIP). Verificar la tarifa vigente de la cuenta.
    ``slippage_bps``: deslizamiento adverso aplicado a cada ejecución a mercado o stop.
    """

    taker_fee: float = Field(0.00055, ge=0, le=0.01)
    maker_fee: float = Field(0.0002, ge=-0.001, le=0.01)
    slippage_bps: float = Field(2.0, ge=0, le=500)
    use_funding: bool = True


class ExecutionConfig(_Strict):
    """Reglas de ejecución del simulador."""

    leverage: float = Field(3.0, ge=1.0, le=100.0)
    #: Regla cuando una vela toca SL y TP: se asume siempre el stop primero.
    same_bar_policy: Literal["stop_first"] = "stop_first"
    #: Cerrar posiciones abiertas al final de los datos (al cierre de la última vela).
    close_at_end: bool = True
    #: Si la señal pasa a la dirección opuesta, cerrar y abrir en sentido contrario.
    allow_reversal: bool = True
    #: Tasa de margen de mantenimiento usada en la aproximación de liquidación.
    maintenance_margin_rate: float = Field(0.005, ge=0, le=0.5)
    simulate_liquidation: bool = True


class RiskConfig(_Strict):
    """Límites de riesgo del sistema (independientes de las estrategias)."""

    risk_per_trade: float = Field(0.01, gt=0, le=0.1)
    max_drawdown: float = Field(0.15, gt=0, le=1)
    drawdown_action: Literal["block", "close_and_block"] = "block"
    max_daily_loss: float = Field(0.05, gt=0, le=1)
    daily_loss_action: Literal["block", "close_and_block"] = "block"
    max_consecutive_losses: int = Field(3, ge=1)
    pause_bars_after_losses: int = Field(24, ge=1)
    max_open_positions: int = Field(1, ge=1, le=1)
    max_symbol_exposure: float = Field(3.0, gt=0, description="Nocional máximo / equity")
    max_leverage: float = Field(5.0, ge=1)
    margin_reserve: float = Field(0.2, ge=0, lt=1, description="Fracción de equity no usable")


class BacktestConfig(_Strict):
    """Parámetros generales de la simulación."""

    initial_capital: float = Field(10_000.0, gt=0)
    seed: int = 42
    min_trades_for_stats: int = Field(30, ge=1)
    min_days_for_cagr: int = Field(180, ge=1)


class ValidationConfig(_Strict):
    """Separación cronológica y walk-forward."""

    train_frac: float = Field(0.6, gt=0, lt=1)
    validation_frac: float = Field(0.2, gt=0, lt=1)
    embargo_bars: int = Field(0, ge=0)
    wf_train_bars: int = Field(2000, ge=50)
    wf_test_bars: int = Field(500, ge=10)
    wf_step_bars: int | None = None
    wf_anchored: bool = False
    max_grid_size: int = Field(200, ge=1)
    selection_metric: Literal["sharpe", "net_profit", "profit_factor", "expectancy"] = "sharpe"
    min_trades_selection: int = Field(10, ge=0)
    bootstrap_samples: int = Field(1000, ge=100)

    @model_validator(mode="after")
    def _check_fracs(self) -> ValidationConfig:
        if self.train_frac + self.validation_frac >= 1:
            raise ValueError("train_frac + validation_frac debe ser < 1 para dejar período de test")
        return self


class AppConfig(_Strict):
    """Configuración completa del experimento."""

    data: DataConfig = DataConfig()
    costs: CostConfig = CostConfig()
    execution: ExecutionConfig = ExecutionConfig()
    risk: RiskConfig = RiskConfig()
    backtest: BacktestConfig = BacktestConfig()
    validation: ValidationConfig = ValidationConfig()
    output_dir: Path = Path("outputs")

    @model_validator(mode="after")
    def _check_leverage(self) -> AppConfig:
        if self.execution.leverage > self.risk.max_leverage:
            raise ValueError(
                f"execution.leverage={self.execution.leverage} supera "
                f"risk.max_leverage={self.risk.max_leverage}"
            )
        return self
