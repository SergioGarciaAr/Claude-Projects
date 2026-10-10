"""Metadatos de reproducibilidad: versión de código, datos, configuración y semilla."""

from __future__ import annotations

import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from bybit_quant_lab import DISCLAIMER, __version__
from bybit_quant_lab.config.loader import config_hash
from bybit_quant_lab.config.models import AppConfig


def git_info(cwd: Path | None = None) -> dict[str, Any]:
    """Commit actual y si hay cambios sin confirmar (``unknown`` si no hay git)."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            ).stdout.strip()
        )
        return {"commit": commit, "dirty": dirty}
    except (OSError, subprocess.SubprocessError):
        return {"commit": "unknown", "dirty": None}


def build_metadata(
    config: AppConfig,
    data_hash: str,
    data_meta: dict[str, Any] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Metadatos completos del experimento."""
    meta = data_meta or {}
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "package_version": __version__,
        "git": git_info(Path(__file__).resolve().parent),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "data_hash": data_hash,
        "data_source": meta.get("source", "desconocido"),
        "data_synthetic": bool(meta.get("synthetic", False)),
        "data_rows": meta.get("rows"),
        "data_range": [meta.get("start"), meta.get("end")],
        "config_hash": config_hash(config),
        "config": config.model_dump(mode="json"),
        "seed": config.backtest.seed,
        "disclaimer": DISCLAIMER,
        **(extra or {}),
    }
