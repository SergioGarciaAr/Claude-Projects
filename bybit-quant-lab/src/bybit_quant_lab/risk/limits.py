"""Límites de riesgo del sistema, independientes de las estrategias.

Definiciones (todas evaluadas con equity *mark-to-market* al **cierre** de cada vela):

* **Pérdida diaria**: ``equity_cierre - equity_inicio_día_UTC``, donde ``equity_inicio_día``
  es la equity al cierre de la última vela del día UTC anterior (o el capital inicial). Incluye
  PnL realizado y no realizado. Si la pérdida alcanza ``max_daily_loss * equity_inicio_día``
  se bloquean nuevas entradas hasta el siguiente día UTC (``block``) o, además, se cierra la
  posición en la siguiente apertura (``close_and_block``).
* **Drawdown máximo**: ``1 - equity / máximo_histórico_equity``. Al alcanzar ``max_drawdown``
  se detienen las nuevas entradas durante el resto de la simulación (kill-switch).
* **Pérdidas consecutivas**: operaciones con PnL neto < 0 incrementan la racha, > 0 la
  reinician (== 0 no la modifica). Al llegar a ``max_consecutive_losses`` se pausan las
  entradas ``pause_bars_after_losses`` velas y la racha se reinicia. La pausa no anula
  ningún otro límite: al terminar, siguen aplicándose todos.

El stop de estrategia (por operación), estos límites del sistema y la liquidación del
exchange (simulada por el motor) son mecanismos distintos y se registran por separado.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

import pandas as pd

from bybit_quant_lab.config.models import RiskConfig


@dataclass
class RiskEvent:
    """Evento del gestor de riesgo."""

    time: str
    kind: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        """Serializa el evento."""
        return asdict(self)


@dataclass
class RiskManager:
    """Estado y reglas de los límites de riesgo."""

    config: RiskConfig
    initial_equity: float
    day: int | None = None
    day_start_equity: float = 0.0
    last_equity: float = 0.0
    peak_equity: float = 0.0
    consecutive_losses: int = 0
    pause_until_bar: int = -1
    daily_blocked: bool = False
    halted: bool = False
    events: list[RiskEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.day_start_equity = self.last_equity = self.peak_equity = self.initial_equity

    def on_bar_open(self, ts: pd.Timestamp, day: int | None = None) -> None:
        """Gestiona el cambio de día UTC (reinicia la referencia diaria y el bloqueo diario).

        ``day`` es un identificador entero del día UTC (opcional, para evitar recalcularlo).
        """
        if day is None:
            day = int(ts.floor("D").as_unit("s").value // 86_400)
        if self.day is None:
            self.day = day
            return
        if day != self.day:
            self.day = day
            self.day_start_equity = self.last_equity
            if self.daily_blocked:
                self.events.append(RiskEvent(str(ts), "daily_block_lifted", "nuevo día UTC"))
            self.daily_blocked = False

    def on_bar_close(self, ts: pd.Timestamp, equity: float) -> bool:
        """Actualiza límites con la equity al cierre. Devuelve ``True`` si hay que cerrar."""
        self.last_equity = equity
        self.peak_equity = max(self.peak_equity, equity)
        force_close = False
        daily_pnl = equity - self.day_start_equity
        if (
            not self.daily_blocked
            and daily_pnl <= -self.config.max_daily_loss * self.day_start_equity
        ):
            self.daily_blocked = True
            self.events.append(
                RiskEvent(
                    str(ts),
                    "daily_loss_limit",
                    f"pnl_dia={daily_pnl:.2f} ref={self.day_start_equity:.2f}",
                )
            )
            force_close |= self.config.daily_loss_action == "close_and_block"
        dd = 1 - equity / self.peak_equity if self.peak_equity > 0 else 0.0
        if not self.halted and dd >= self.config.max_drawdown:
            self.halted = True
            self.events.append(RiskEvent(str(ts), "max_drawdown_halt", f"drawdown={dd:.4f}"))
            force_close |= self.config.drawdown_action == "close_and_block"
        return force_close

    def on_trade_closed(self, bar_index: int, ts: pd.Timestamp, net_pnl: float) -> None:
        """Actualiza la racha de pérdidas y activa la pausa si corresponde."""
        if net_pnl < 0:
            self.consecutive_losses += 1
        elif net_pnl > 0:
            self.consecutive_losses = 0
        if self.consecutive_losses >= self.config.max_consecutive_losses:
            self.pause_until_bar = bar_index + self.config.pause_bars_after_losses
            self.events.append(
                RiskEvent(
                    str(ts),
                    "loss_streak_pause",
                    f"{self.consecutive_losses} pérdidas; pausa hasta vela {self.pause_until_bar}",
                )
            )
            self.consecutive_losses = 0

    def can_open(self, bar_index: int) -> tuple[bool, str]:
        """Indica si se permiten nuevas entradas decididas en la vela ``bar_index``."""
        if self.halted:
            return False, "max_drawdown_halt"
        if self.daily_blocked:
            return False, "daily_loss_limit"
        if bar_index < self.pause_until_bar:
            return False, "loss_streak_pause"
        return True, "ok"
