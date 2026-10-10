"""Exportación de resultados a CSV y JSON."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bybit_quant_lab.backtesting.results import BacktestResult


def to_jsonable(obj: Any) -> Any:
    """Convierte recursivamente tipos de numpy/pandas a JSON (NaN/inf -> ``null``)."""
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list | tuple):
        return [to_jsonable(v) for v in obj]
    if isinstance(obj, pd.DataFrame):
        return to_jsonable(obj.reset_index().to_dict("records"))
    if isinstance(obj, pd.Series):
        return to_jsonable(obj.to_dict())
    if isinstance(obj, np.generic):
        obj = obj.item()
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    if isinstance(obj, pd.Timestamp):
        return str(obj)
    return obj


def write_json(obj: Any, path: Path) -> None:
    """Escribe ``obj`` como JSON legible."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(to_jsonable(obj), indent=2, default=str, ensure_ascii=False), encoding="utf-8"
    )


def export_result(
    result: BacktestResult, metrics: dict[str, Any], out_dir: Path, prefix: str = ""
) -> dict[str, Path]:
    """Exporta equity, operaciones, eventos de riesgo y métricas de un backtest."""
    out_dir.mkdir(parents=True, exist_ok=True)
    p = {
        "equity": out_dir / f"{prefix}equity.csv",
        "trades": out_dir / f"{prefix}trades.csv",
        "metrics": out_dir / f"{prefix}metrics.json",
        "risk_events": out_dir / f"{prefix}risk_events.json",
    }
    result.equity.to_csv(p["equity"])
    result.trades.to_csv(p["trades"], index=False)
    write_json(metrics, p["metrics"])
    write_json(
        {"risk_events": result.risk_events, "rejected_signals": result.rejected_signals},
        p["risk_events"],
    )
    return p
