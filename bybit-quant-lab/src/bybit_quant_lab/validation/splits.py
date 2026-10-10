"""Separación cronológica train/validación/test y ventanas walk-forward.

Los segmentos nunca se solapan y respetan el orden temporal. ``embargo_bars`` deja velas sin
usar entre segmentos para reducir la dependencia entre el final de uno y el inicio del
siguiente. Las señales se calculan una vez sobre toda la serie (los indicadores son causales,
así que el valor en ``t`` solo depende de ``[0, t]``) y luego cada segmento se simula por
separado empezando sin posición.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class Segment:
    """Segmento temporal ``[start, end]`` (ambos inclusive) en posiciones e instantes."""

    name: str
    start_pos: int
    end_pos: int
    start: pd.Timestamp
    end: pd.Timestamp

    @property
    def bars(self) -> int:
        """Número de velas del segmento."""
        return self.end_pos - self.start_pos + 1

    def to_dict(self) -> dict[str, object]:
        """Serializa el segmento."""
        return {
            "name": self.name,
            "start": str(self.start),
            "end": str(self.end),
            "bars": self.bars,
        }


def _segment(index: pd.DatetimeIndex, name: str, a: int, b: int) -> Segment:
    if b < a:
        raise ValueError(f"Segmento '{name}' vacío; usa más datos o ajusta las fracciones")
    return Segment(name, a, b, index[a], index[b])


def chronological_split(
    index: pd.DatetimeIndex, train_frac: float, validation_frac: float, embargo_bars: int = 0
) -> dict[str, Segment]:
    """Divide ``index`` en ``train``, ``validation`` y ``test`` (resto), en ese orden."""
    n = len(index)
    if not 0 < train_frac < 1 or not 0 < validation_frac < 1 or train_frac + validation_frac >= 1:
        raise ValueError("Fracciones inválidas: se requiere train + validation < 1")
    n_train = int(n * train_frac)
    n_val = int(n * validation_frac)
    tr = _segment(index, "train", 0, n_train - 1)
    va = _segment(index, "validation", n_train + embargo_bars, n_train + n_val - 1)
    te = _segment(index, "test", n_train + n_val + embargo_bars, n - 1)
    assert tr.end < va.start < va.end < te.start, "segmentos no ordenados"
    return {"train": tr, "validation": va, "test": te}


def walk_forward_windows(
    index: pd.DatetimeIndex,
    train_bars: int,
    test_bars: int,
    step_bars: int | None = None,
    anchored: bool = False,
    embargo_bars: int = 0,
) -> list[tuple[Segment, Segment]]:
    """Ventanas (entrenamiento, prueba) consecutivas; ``anchored`` fija el inicio en 0."""
    step = step_bars or test_bars
    out = []
    k = 0
    start = 0
    while True:
        tr_end = start + train_bars - 1 if not anchored else train_bars - 1 + k * step
        te_start = tr_end + 1 + embargo_bars
        te_end = te_start + test_bars - 1
        if te_end >= len(index):
            break
        tr_start = 0 if anchored else start
        out.append(
            (
                _segment(index, f"wf{k}_train", tr_start, tr_end),
                _segment(index, f"wf{k}_test", te_start, te_end),
            )
        )
        k += 1
        start += step
    if not out:
        raise ValueError("Datos insuficientes para una sola ventana walk-forward")
    return out
