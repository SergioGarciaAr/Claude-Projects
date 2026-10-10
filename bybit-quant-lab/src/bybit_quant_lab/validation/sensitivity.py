"""Rejillas de parámetros con límite de tamaño y análisis de estabilidad."""

from __future__ import annotations

import itertools
from typing import Any

import numpy as np
import pandas as pd


def param_grid(space: dict[str, list[Any]], max_size: int) -> list[dict[str, Any]]:
    """Producto cartesiano de ``space``. Lanza ``ValueError`` si supera ``max_size``."""
    if not space:
        return [{}]
    size = int(np.prod([len(v) for v in space.values()]))
    if size > max_size:
        raise ValueError(
            f"La rejilla tiene {size} combinaciones y el límite es {max_size}. Reduce el "
            "espacio de búsqueda (más pruebas = mayor riesgo de sobreajuste)."
        )
    keys = list(space)
    return [dict(zip(keys, combo, strict=True)) for combo in itertools.product(*space.values())]


def stability_summary(table: pd.DataFrame, metric: str) -> dict[str, Any]:
    """Resumen de la distribución de ``metric`` en la rejilla.

    Una mejor configuración muy alejada de la mediana, o pocas configuraciones con valor
    positivo, sugieren que el resultado depende de un ajuste fino (frágil).
    """
    vals = table[metric].astype(float).dropna()
    if vals.empty:
        return {"metric": metric, "n": 0}
    return {
        "metric": metric,
        "n": len(vals),
        "best": float(vals.max()),
        "median": float(vals.median()),
        "worst": float(vals.min()),
        "std": float(vals.std(ddof=1)) if len(vals) > 1 else 0.0,
        "fraction_positive": float((vals > 0).mean()),
        "best_minus_median": float(vals.max() - vals.median()),
    }
