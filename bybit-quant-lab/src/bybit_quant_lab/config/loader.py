"""Carga de configuración desde YAML y hash reproducible."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

from bybit_quant_lab.config.models import AppConfig


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo de configuración: {path}")
    with path.open("r", encoding="utf-8") as fh:
        content = yaml.safe_load(fh) or {}
    if not isinstance(content, dict):
        raise ValueError(f"El archivo {path} debe contener un mapeo YAML")
    return content


def load_config(
    path: str | Path | None = None, overrides: dict[str, Any] | None = None
) -> AppConfig:
    """Carga ``AppConfig`` desde YAML (o valores por defecto) aplicando ``overrides`` anidados."""
    raw: dict[str, Any] = _read_yaml(Path(path)) if path else {}
    for key, value in (overrides or {}).items():
        if isinstance(value, dict):
            raw.setdefault(key, {}).update(value)
        else:
            raw[key] = value
    return AppConfig.model_validate(raw)


def load_strategy_params(path: str | Path) -> dict[str, dict[str, Any]]:
    """Carga parámetros de estrategias: ``{nombre_estrategia: {param: valor}}``."""
    raw = _read_yaml(Path(path))
    strategies = raw.get("strategies", raw)
    if not isinstance(strategies, dict):
        raise ValueError("La sección 'strategies' debe ser un mapeo")
    return {str(k): dict(v or {}) for k, v in strategies.items()}


def config_hash(payload: Any) -> str:
    """SHA-256 (16 hex) de un objeto serializable, con claves ordenadas."""
    if hasattr(payload, "model_dump"):
        payload = payload.model_dump(mode="json")
    blob = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]
