"""Descarga incremental de OHLCV y funding con almacenamiento en Parquet."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from bybit_quant_lab.data.bybit_client import BybitPublicClient
from bybit_quant_lab.data.storage import (
    dataset_path,
    load_dataset,
    load_metadata,
    save_dataset,
)
from bybit_quant_lab.data.validation import clean_ohlcv, validate_ohlcv
from bybit_quant_lab.logging_utils import get_logger
from bybit_quant_lab.timeframes import timeframe_delta

logger = get_logger("data.downloader")


@dataclass
class DownloadSummary:
    """Resumen de una descarga."""

    path: Path
    rows: int
    fetched_ranges: list[tuple[str, str]]
    requests: int
    quality: dict[str, Any]


def missing_ranges(
    existing: pd.DatetimeIndex, start: pd.Timestamp, end: pd.Timestamp, timeframe: str
) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """Calcula los rangos ``[a, b)`` de ``[start, end)`` no cubiertos por ``existing``.

    Incluye cabecera, cola y huecos internos. Un hueco interno puede corresponder a una
    interrupción real del exchange; en ese caso volver a pedirlo simplemente no devuelve datos.
    """
    delta = timeframe_delta(timeframe)
    if len(existing) == 0:
        return [(start, end)] if start < end else []
    idx = existing[(existing >= start) & (existing < end)].sort_values()
    if len(idx) == 0:
        return [(start, end)]
    ranges: list[tuple[pd.Timestamp, pd.Timestamp]] = []
    if idx[0] > start:
        ranges.append((start, idx[0]))
    for a, b in itertools.pairwise(idx):
        if b - a > delta:
            ranges.append((a + delta, b))
    if idx[-1] + delta < end:
        ranges.append((idx[-1] + delta, end))
    return ranges


def download_ohlcv(
    client: BybitPublicClient,
    symbol: str,
    timeframe: str,
    start: pd.Timestamp,
    end: pd.Timestamp,
    data_dir: Path,
    refresh: bool = False,
    limit: int = 1000,
) -> DownloadSummary:
    """Descarga ``[start, end)`` reutilizando los datos locales válidos.

    Si existe un dataset local válido solo se piden los rangos faltantes. Con ``refresh=True``
    o si el dataset local no supera la validación, se descarga todo el rango.
    """
    path = dataset_path(data_dir, symbol, timeframe)
    existing = None
    if path.exists() and not refresh:
        existing = load_dataset(path)
        if not validate_ohlcv(existing, timeframe).is_valid:
            logger.warning("dataset local inválido, se descarga de nuevo: %s", path)
            existing = None
    have = pd.DatetimeIndex(existing.index if existing is not None else [], tz="UTC")
    todo = missing_ranges(have, start, end, timeframe)
    before = client.request_count
    frames = [existing] if existing is not None else []
    for a, b in todo:
        logger.info("descargando %s %s %s -> %s", symbol, timeframe, a, b)
        frames.append(client.fetch_klines(symbol, timeframe, a, b, limit=limit))
    non_empty = [f for f in frames if f is not None and len(f)]
    if not non_empty:
        raise ValueError(f"Bybit no devolvió datos para {symbol} {timeframe} en {start}..{end}")
    merged = pd.concat(non_empty)
    cleaned, report = clean_ohlcv(merged, timeframe)
    prev_meta = load_metadata(path) if existing is not None else {}
    history = list(prev_meta.get("downloads", []))
    history.append(
        {
            "downloaded_at": datetime.now(UTC).isoformat(),
            "requested_start": str(start),
            "requested_end": str(end),
            "fetched_ranges": [(str(a), str(b)) for a, b in todo],
            "requests": client.request_count - before,
        }
    )
    meta = {
        "source": "bybit_v5_public",
        "endpoint": "/v5/market/kline",
        "base_url": client.base_url,
        "category": "linear",
        "symbol": symbol.upper(),
        "timeframe": timeframe,
        "synthetic": False,
        "downloads": history,
        "quality": report.to_dict(),
    }
    save_dataset(cleaned, path, meta)
    return DownloadSummary(
        path=path,
        rows=len(cleaned),
        fetched_ranges=[(str(a), str(b)) for a, b in todo],
        requests=client.request_count - before,
        quality=report.to_dict(),
    )


def funding_path(data_dir: Path, symbol: str) -> Path:
    """Ruta del Parquet de funding de un símbolo."""
    return Path(data_dir) / "processed" / f"{symbol.upper()}_funding.parquet"


def download_funding(
    client: BybitPublicClient, symbol: str, start: pd.Timestamp, end: pd.Timestamp, data_dir: Path
) -> Path:
    """Descarga el historial de funding y lo guarda (fusionando con lo existente)."""
    path = funding_path(data_dir, symbol)
    series = client.fetch_funding_history(symbol, start, end)
    frame = series.to_frame()
    if path.exists():
        old = pd.read_parquet(path)
        frame = pd.concat([old, frame])
        frame = frame[~frame.index.duplicated(keep="last")].sort_index()
    meta = {
        "source": "bybit_v5_public",
        "endpoint": "/v5/market/funding/history",
        "symbol": symbol.upper(),
        "synthetic": False,
        "requested_start": str(start),
        "requested_end": str(end),
    }
    save_dataset(frame, path, meta)
    return path


def load_funding(data_dir: Path, symbol: str) -> pd.Series | None:
    """Carga el funding guardado o ``None`` si no se ha descargado (no se inventa)."""
    path = funding_path(data_dir, symbol)
    if not path.exists():
        return None
    df = pd.read_parquet(path)
    if pd.DatetimeIndex(df.index).tz is None:
        df = df.tz_localize("UTC")
    return df["funding_rate"].astype("float64").sort_index()
