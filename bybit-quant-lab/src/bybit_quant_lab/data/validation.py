"""Validación y limpieza de series OHLCV.

Convención: índice ``open_time`` (``DatetimeIndex`` UTC) que marca la apertura de cada vela.
La limpieza nunca inventa velas: los huecos se reportan, no se rellenan.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from bybit_quant_lab.timeframes import timeframe_delta

REQUIRED = ("open", "high", "low", "close", "volume")


@dataclass
class DataQualityReport:
    """Resultado de la validación de una serie OHLCV."""

    rows: int = 0
    start: str | None = None
    end: str | None = None
    duplicates: int = 0
    unsorted: bool = False
    non_numeric: int = 0
    nan_rows: int = 0
    invalid_candles: int = 0
    negative_volume: int = 0
    gaps: int = 0
    missing_bars: int = 0
    gap_ranges: list[tuple[str, str]] = field(default_factory=list)
    misaligned: int = 0
    issues: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Válida si no hay errores estructurales (los huecos se toleran y se reportan)."""
        return not (
            self.duplicates
            or self.unsorted
            or self.non_numeric
            or self.nan_rows
            or self.invalid_candles
            or self.negative_volume
            or self.misaligned
        )

    def to_dict(self) -> dict[str, Any]:
        """Serializa el informe (incluye ``is_valid``)."""
        out = asdict(self)
        out["is_valid"] = self.is_valid
        return out


def _ensure_utc_index(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("El índice debe ser DatetimeIndex (open_time)")
    df = df.tz_localize("UTC") if df.index.tz is None else df.tz_convert("UTC")
    df.index.name = "open_time"
    return df


def validate_ohlcv(df: pd.DataFrame, timeframe: str, max_gap_ranges: int = 50) -> DataQualityReport:
    """Valida orden, duplicados, numéricos, coherencia OHLC, volumen y huecos."""
    rep = DataQualityReport(rows=len(df))
    missing_cols = [c for c in REQUIRED if c not in df.columns]
    if missing_cols:
        rep.issues.append(f"faltan columnas: {missing_cols}")
        rep.non_numeric = len(df)
        return rep
    if df.empty:
        rep.issues.append("serie vacía")
        return rep
    df = _ensure_utc_index(df.copy())
    rep.start, rep.end = str(df.index[0]), str(df.index[-1])
    rep.duplicates = int(df.index.duplicated().sum())
    rep.unsorted = not df.index.is_monotonic_increasing
    numeric = df[list(REQUIRED)].apply(pd.to_numeric, errors="coerce")
    raw_nan = df[list(REQUIRED)].isna()
    rep.non_numeric = int((numeric.isna() & ~raw_nan).any(axis=1).sum())
    rep.nan_rows = int(numeric.isna().any(axis=1).sum())
    o, h, low, c, v = (numeric[k] for k in REQUIRED)
    bad = (h < low) | (h < o) | (h < c) | (low > o) | (low > c) | (o <= 0) | (c <= 0) | (low <= 0)
    rep.invalid_candles = int(bad.fillna(False).sum())
    rep.negative_volume = int((v < 0).fillna(False).sum())
    delta = timeframe_delta(timeframe)
    epoch = pd.Timestamp("1970-01-01", tz="UTC")
    dt_index = pd.DatetimeIndex(df.index)
    offsets = (dt_index - epoch).to_numpy() % delta.to_timedelta64()
    rep.misaligned = int((offsets != np.timedelta64(0, "ns")).sum())
    idx = dt_index[~dt_index.duplicated()].sort_values()
    starts, ends = idx[:-1], idx[1:]
    diffs = ends - starts
    gap_mask = np.asarray(diffs > delta)
    rep.gaps = int(gap_mask.sum())
    if rep.gaps:
        rep.missing_bars = int(sum(d // delta - 1 for d in diffs[gap_mask]))
        for a, b in list(zip(starts[gap_mask], ends[gap_mask], strict=True))[:max_gap_ranges]:
            rep.gap_ranges.append((str(a + delta), str(b - delta)))
        rep.issues.append(f"{rep.gaps} huecos ({rep.missing_bars} velas faltantes)")
    for name in ("duplicates", "non_numeric", "nan_rows", "invalid_candles", "negative_volume"):
        if getattr(rep, name):
            rep.issues.append(f"{name}={getattr(rep, name)}")
    if rep.unsorted:
        rep.issues.append("índice no ordenado")
    if rep.misaligned:
        rep.issues.append(f"{rep.misaligned} marcas de tiempo no alineadas a {timeframe}")
    return rep


def clean_ohlcv(df: pd.DataFrame, timeframe: str) -> tuple[pd.DataFrame, DataQualityReport]:
    """Normaliza a UTC, ordena, elimina duplicados (conserva el último) y filas inválidas.

    Devuelve la serie limpia y el informe de calidad **posterior** a la limpieza. Las filas
    descartadas se registran en ``issues``. Los huecos no se rellenan.
    """
    out = _ensure_utc_index(df.copy())
    cols = [c for c in (*REQUIRED, "turnover") if c in out.columns]
    out = out[cols].apply(pd.to_numeric, errors="coerce").astype("float64")
    before = len(out)
    out = out[~out.index.duplicated(keep="last")].sort_index()
    o, h, low, c = out["open"], out["high"], out["low"], out["close"]
    valid = (
        out[list(REQUIRED)].notna().all(axis=1)
        & (h >= np.maximum(o, c))
        & (low <= np.minimum(o, c))
        & (low > 0)
        & (out["volume"] >= 0)
    )
    out = out[valid]
    rep = validate_ohlcv(out, timeframe)
    dropped = before - len(out)
    if dropped:
        rep.issues.insert(0, f"limpieza: {dropped} filas descartadas (duplicadas o inválidas)")
    return out, rep
