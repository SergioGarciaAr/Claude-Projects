"""Gráficos Matplotlib (PNG en base64) para los informes HTML.

Paleta categórica validada (orden fijo, nunca cíclico): azul, naranja, aqua. Como máximo tres
series por gráfico; los textos usan tintas neutras y cada gráfico se acompaña de su tabla.
"""

from __future__ import annotations

import base64
import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

SERIES = ("#2a78d6", "#eb6834", "#1baf7a")
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"


def _style(ax: plt.Axes, title: str) -> None:
    ax.set_facecolor(SURFACE)
    ax.set_title(title, loc="left", color=INK, fontsize=11)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.tick_params(colors=INK_2, labelsize=8)
    for spine in ax.spines.values():
        spine.set_visible(False)


def _encode(fig: plt.Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def line_chart(series: dict[str, pd.Series], title: str, ylabel: str = "") -> str:
    """Hasta tres series temporales en un eje (las adicionales se ignoran)."""
    fig, ax = plt.subplots(figsize=(9, 3.2))
    fig.patch.set_facecolor(SURFACE)
    for color, (name, s) in zip(SERIES, list(series.items())[:3], strict=False):
        ax.plot(s.index, s.to_numpy(), color=color, linewidth=1.6, label=name)
    _style(ax, title)
    ax.set_ylabel(ylabel, color=INK_2, fontsize=8)
    if len(series) > 1:
        ax.legend(frameon=False, fontsize=8, labelcolor=INK_2)
    return _encode(fig)


def drawdown_chart(drawdown: pd.Series, title: str = "Drawdown") -> str:
    """Área de drawdown (valores <= 0) en porcentaje."""
    fig, ax = plt.subplots(figsize=(9, 2.4))
    fig.patch.set_facecolor(SURFACE)
    ax.fill_between(
        drawdown.index, drawdown.to_numpy() * 100, 0, color=SERIES[0], alpha=0.35, linewidth=0
    )
    ax.plot(drawdown.index, drawdown.to_numpy() * 100, color=SERIES[0], linewidth=1.2)
    _style(ax, title)
    ax.set_ylabel("%", color=INK_2, fontsize=8)
    return _encode(fig)


def histogram(values: pd.Series, title: str, xlabel: str) -> str:
    """Histograma de una distribución (p. ej., retorno por operación)."""
    fig, ax = plt.subplots(figsize=(6, 2.8))
    fig.patch.set_facecolor(SURFACE)
    v = values.dropna()
    if len(v):
        ax.hist(
            v, bins=min(40, max(5, len(v) // 3)), color=SERIES[0], edgecolor=SURFACE, linewidth=1
        )
        ax.axvline(0, color=INK_2, linewidth=0.8)
    _style(ax, title)
    ax.set_xlabel(xlabel, color=INK_2, fontsize=8)
    return _encode(fig)


def bar_chart(values: pd.Series, title: str, xlabel: str) -> str:
    """Barras horizontales de una métrica por candidato (una sola serie)."""
    v = values.dropna().sort_values()
    fig, ax = plt.subplots(figsize=(8, max(2.0, 0.28 * len(v) + 0.8)))
    fig.patch.set_facecolor(SURFACE)
    ax.barh(v.index.astype(str), v.to_numpy(), color=SERIES[0], height=0.7)
    ax.axvline(0, color=INK_2, linewidth=0.8)
    _style(ax, title)
    ax.set_xlabel(xlabel, color=INK_2, fontsize=8)
    return _encode(fig)
