"""Auditoría de indicadores: comparación con implementaciones de referencia en bucles puros.

Las referencias usan la misma convención de inicialización documentada (suavizados de
Wilder/EMA recursivos sembrados con el primer valor válido), escritas sin pandas.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from bybit_quant_lab import indicators as ind
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv

DF = generate_synthetic_ohlcv(400, "1h", seed=21)
H, L, C, V = (DF[k].to_numpy(float) for k in ("high", "low", "close", "volume"))
NAN = float("nan")


def rec_smooth(x: list[float], alpha: float, min_periods: int) -> list[float]:
    """y0 = primer valor válido; y_t = (1-a)·y_{t-1} + a·x_t; NaN hasta min_periods válidos."""
    out, y, count = [], None, 0
    for v in x:
        if not math.isnan(v):
            y = v if y is None else (1 - alpha) * y + alpha * v
            count += 1
        out.append(y if (y is not None and count >= min_periods) else NAN)
    return out


def ref_tr() -> list[float]:
    out = [H[0] - L[0]]
    for t in range(1, len(C)):
        out.append(max(H[t] - L[t], abs(H[t] - C[t - 1]), abs(L[t] - C[t - 1])))
    return out


def close_enough(a: pd.Series | np.ndarray, b: list[float]) -> None:
    np.testing.assert_allclose(
        np.asarray(a, float), np.asarray(b, float), rtol=1e-9, atol=1e-9, equal_nan=True
    )


def test_atr_matches_reference() -> None:
    close_enough(ind.atr(DF, 14), rec_smooth(ref_tr(), 1 / 14, 14))


def test_ema_matches_reference() -> None:
    close_enough(ind.ema(DF["close"], 20), rec_smooth(list(C), 2 / 21, 20))


def test_rsi_matches_reference() -> None:
    d = [NAN] + [C[t] - C[t - 1] for t in range(1, len(C))]
    g = rec_smooth([NAN if math.isnan(x) else max(x, 0) for x in d], 1 / 14, 14)
    lo = rec_smooth([NAN if math.isnan(x) else max(-x, 0) for x in d], 1 / 14, 14)
    ref = [
        NAN if math.isnan(a) else (100.0 if b == 0 else 100 - 100 / (1 + a / b))
        for a, b in zip(g, lo, strict=True)
    ]
    close_enough(ind.rsi(DF["close"], 14), ref)


def test_adx_matches_reference() -> None:
    n = 14
    pdm, mdm, tr = [NAN], [NAN], [NAN]
    for t in range(1, len(C)):
        up, down = H[t] - H[t - 1], L[t - 1] - L[t]
        pdm.append(up if (up > down and up > 0) else 0.0)
        mdm.append(down if (down > up and down > 0) else 0.0)
        tr.append(max(H[t] - L[t], abs(H[t] - C[t - 1]), abs(L[t] - C[t - 1])))
    sp, sm, st = (rec_smooth(x, 1 / n, n) for x in (pdm, mdm, tr))
    pdi = [100 * a / c if not math.isnan(a) else NAN for a, c in zip(sp, st, strict=True)]
    mdi = [100 * a / c if not math.isnan(a) else NAN for a, c in zip(sm, st, strict=True)]
    dx = [
        NAN if math.isnan(a) else (0.0 if a + b == 0 else 100 * abs(a - b) / (a + b))
        for a, b in zip(pdi, mdi, strict=True)
    ]
    out = ind.adx(DF, n)
    close_enough(out["plus_di"], pdi)
    close_enough(out["minus_di"], mdi)
    close_enough(out["adx"], rec_smooth(dx, 1 / n, n))


def test_macd_matches_reference() -> None:
    fast, slow = rec_smooth(list(C), 2 / 13, 12), rec_smooth(list(C), 2 / 27, 26)
    line = [a - b for a, b in zip(fast, slow, strict=True)]
    sig = rec_smooth(line, 2 / 10, 9)
    out = ind.macd(DF["close"])
    close_enough(out["macd"], line)
    close_enough(out["signal"], sig)


def test_bollinger_matches_reference() -> None:
    n, k = 20, 2.0
    mid, up = [], []
    for t in range(len(C)):
        if t < n - 1:
            mid.append(NAN)
            up.append(NAN)
        else:
            w = C[t - n + 1 : t + 1]
            mid.append(float(w.mean()))
            up.append(float(w.mean() + k * w.std(ddof=0)))
    out = ind.bollinger(DF["close"], n, k)
    close_enough(out["mid"], mid)
    close_enough(out["upper"], up)


def test_obv_vwap_donchian_match_reference() -> None:
    obv = [0.0]
    for t in range(1, len(C)):
        obv.append(obv[-1] + np.sign(C[t] - C[t - 1]) * V[t])
    close_enough(ind.obv(DF["close"], DF["volume"]), obv)
    tp = (H + L + C) / 3
    days = DF.index.floor("1D")
    vw, pv, vv, cur = [], 0.0, 0.0, None
    for t in range(len(C)):
        if days[t] != cur:
            cur, pv, vv = days[t], 0.0, 0.0
        pv += tp[t] * V[t]
        vv += V[t]
        vw.append(pv / vv)
    close_enough(ind.vwap_session(DF), vw)
    up = [NAN] * 20 + [float(H[t - 20 : t].max()) for t in range(20, len(C))]
    close_enough(ind.donchian(DF, 20)["upper"], up)


def test_stoch_rsi_matches_reference() -> None:
    r = list(ind.rsi(DF["close"], 14))
    raw = []
    for t in range(len(r)):
        w = r[t - 13 : t + 1] if t >= 13 else []
        if len(w) < 14 or any(math.isnan(x) for x in w):
            raw.append(NAN)
        else:
            lo, hi = min(w), max(w)
            raw.append(50.0 if hi == lo else 100 * (r[t] - lo) / (hi - lo))
    k = [
        NAN
        if t < 2 or any(math.isnan(x) for x in raw[t - 2 : t + 1])
        else float(np.mean(raw[t - 2 : t + 1]))
        for t in range(len(raw))
    ]
    close_enough(ind.stoch_rsi(DF["close"])["k"], k)


@pytest.mark.parametrize("cut", [101, 237, 350])
def test_higher_timeframe_uses_only_closed_bars(cut: int) -> None:
    base, htf = pd.Timedelta("1h"), pd.Timedelta("4h")
    full = ind.higher_timeframe(DF, base, htf, ema_period=5)
    altered = DF.copy()
    altered.iloc[cut + 1 :, :4] *= 1.5  # cambia todo el futuro de forma drástica
    alt = ind.higher_timeframe(altered, base, htf, ema_period=5)
    pd.testing.assert_frame_equal(full.iloc[: cut + 1], alt.iloc[: cut + 1])
    # Comprobación directa: la vela base t ve la vela 4h cuyo cierre es <= t + 1h.
    t = DF.index[cut]
    last_closed_open = (t + base).floor("4h") - htf
    expected = DF.loc[last_closed_open : last_closed_open + htf - base, "close"].iloc[-1]
    assert full["close"].iloc[cut] == pytest.approx(expected)
