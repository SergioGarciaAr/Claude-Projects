"""Almacenamiento local en Parquet con metadatos JSON de procedencia."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from bybit_quant_lab.logging_utils import get_logger

logger = get_logger("data.storage")


def dataset_path(data_dir: Path, symbol: str, timeframe: str, kind: str = "processed") -> Path:
    """Ruta del Parquet de un símbolo/temporalidad."""
    return Path(data_dir) / kind / f"{symbol.upper()}_{timeframe}.parquet"


def meta_path(parquet_path: Path) -> Path:
    """Ruta del JSON de metadatos asociado a un Parquet."""
    return parquet_path.with_suffix(".meta.json")


def data_hash(df: pd.DataFrame) -> str:
    """SHA-256 determinista del contenido (índice + valores) de un DataFrame."""
    hashed = pd.util.hash_pandas_object(df, index=True).to_numpy()
    return hashlib.sha256(hashed.tobytes()).hexdigest()


def save_dataset(
    df: pd.DataFrame, path: Path, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Guarda ``df`` en Parquet y escribe metadatos (procedencia, rango, hash)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, engine="pyarrow")
    meta: dict[str, Any] = dict(metadata or {})
    meta.update(
        {
            "rows": len(df),
            "start": str(df.index[0]) if len(df) else None,
            "end": str(df.index[-1]) if len(df) else None,
            "sha256": data_hash(df),
            "saved_at": datetime.now(UTC).isoformat(),
            "columns": list(df.columns),
        }
    )
    meta_path(path).write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")
    logger.info("dataset guardado %s filas=%d", path, len(df))
    return meta


def load_dataset(path: Path) -> pd.DataFrame:
    """Carga un Parquet OHLCV garantizando índice UTC ordenado."""
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Descarga datos con 'bql download', impórtalos con 'bql import' "
            "o genera datos sintéticos con 'bql synth'."
        )
    df = pd.read_parquet(path, engine="pyarrow")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError(f"{path} no tiene un índice temporal")
    if df.index.tz is None:
        df = df.tz_localize("UTC")
    df.index.name = "open_time"
    return df.sort_index()


def load_metadata(path: Path) -> dict[str, Any]:
    """Lee los metadatos de un dataset (``{}`` si no existen)."""
    mp = meta_path(path)
    if not mp.exists():
        return {}
    data: dict[str, Any] = json.loads(mp.read_text(encoding="utf-8"))
    return data
