"""Importación de OHLCV desde CSV o Parquet externos."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from bybit_quant_lab.data.storage import dataset_path, save_dataset
from bybit_quant_lab.data.validation import DataQualityReport, clean_ohlcv

TIME_CANDIDATES = ("open_time", "timestamp", "time", "date", "datetime", "start_time")


def read_ohlcv_file(path: Path, time_column: str | None = None) -> pd.DataFrame:
    """Lee CSV/Parquet y devuelve un DataFrame indexado por ``open_time`` UTC.

    La columna temporal puede ser ISO-8601 o epoch en milisegundos/segundos.
    """
    path = Path(path)
    if path.suffix.lower() == ".parquet":
        raw = pd.read_parquet(path)
    elif path.suffix.lower() in {".csv", ".txt"}:
        raw = pd.read_csv(path)
    else:
        raise ValueError(f"Formato no soportado: {path.suffix} (use .csv o .parquet)")
    raw.columns = [str(c).strip().lower() for c in raw.columns]
    if isinstance(raw.index, pd.DatetimeIndex):
        raw.index.name = "open_time"
        return raw
    col = time_column or next((c for c in TIME_CANDIDATES if c in raw.columns), None)
    if col is None:
        raise ValueError(f"No se encontró columna temporal; opciones: {TIME_CANDIDATES}")
    values = raw[col]
    if pd.api.types.is_numeric_dtype(values):
        unit = "ms" if values.abs().max() > 1e11 else "s"
        ts = pd.to_datetime(values, unit=unit, utc=True)  # type: ignore[call-overload]
    else:
        ts = pd.to_datetime(values, utc=True)
    out = raw.drop(columns=[col]).set_index(pd.DatetimeIndex(ts, name="open_time"))
    return out


def import_ohlcv(
    file: Path, symbol: str, timeframe: str, data_dir: Path, time_column: str | None = None
) -> tuple[Path, DataQualityReport]:
    """Importa, limpia, valida y guarda un archivo externo como dataset procesado."""
    df = read_ohlcv_file(file, time_column)
    cleaned, report = clean_ohlcv(df, timeframe)
    if cleaned.empty:
        raise ValueError("El archivo no contiene velas válidas tras la limpieza")
    path = dataset_path(data_dir, symbol, timeframe)
    save_dataset(
        cleaned,
        path,
        {
            "source": "import",
            "origin_file": str(Path(file).resolve()),
            "symbol": symbol.upper(),
            "timeframe": timeframe,
            "synthetic": False,
            "quality": report.to_dict(),
        },
    )
    return path, report
