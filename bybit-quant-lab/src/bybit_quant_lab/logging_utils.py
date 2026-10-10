"""Logging estructurado (clave=valor) para todo el paquete."""

from __future__ import annotations

import logging
import os
from typing import Any

_CONFIGURED = False


class KeyValueFormatter(logging.Formatter):
    """Formatea registros como ``ts level logger msg k=v ...`` para facilitar su análisis."""

    def format(self, record: logging.LogRecord) -> str:
        base = f"{self.formatTime(record)} {record.levelname} {record.name} {record.getMessage()}"
        extra: dict[str, Any] = getattr(record, "ctx", {}) or {}
        if extra:
            base += " " + " ".join(f"{k}={v}" for k, v in sorted(extra.items()))
        if record.exc_info:
            base += "\n" + self.formatException(record.exc_info)
        return base


def setup_logging(level: str | None = None) -> None:
    """Configura el logger raíz del paquete una sola vez."""
    global _CONFIGURED
    if _CONFIGURED:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(KeyValueFormatter())
    logger = logging.getLogger("bybit_quant_lab")
    logger.addHandler(handler)
    logger.setLevel((level or os.getenv("BQL_LOG_LEVEL") or "INFO").upper())
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Devuelve un logger hijo de ``bybit_quant_lab``."""
    return logging.getLogger(f"bybit_quant_lab.{name}")


def log_event(logger: logging.Logger, level: int, msg: str, **ctx: Any) -> None:
    """Registra un mensaje con contexto estructurado."""
    logger.log(level, msg, extra={"ctx": ctx})
