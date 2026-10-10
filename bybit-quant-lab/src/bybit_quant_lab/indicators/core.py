"""Implementación vectorizada de indicadores.

Reglas de causalidad:

* Solo ``rolling``/``ewm`` hacia atrás, sin ``center=True`` ni ``bfill``.
* Las EMA usan ``adjust=False``: el valor en ``t`` depende únicamente de ``x[0..t]``, de modo
  que truncar la serie en ``t`` no cambia los valores hasta ``t``.
* Los canales que deben excluir la vela actual (Donchian) se desplazan una vela.
* Las series de temporalidad superior solo se exponen cuando la vela superior ha cerrado.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _check_period(n: int) -> None:
    if not isinstance(n, int | np.integer) or n < 1:
        raise ValueError(f"El período debe ser un entero >= 1 (recibido {n!r})")


def sma(s: pd.Series, n: int) -> pd.Series:
    """Media móvil simple de ``n`` velas (NaN hasta disponer de ``n`` valores)."""
    _check_period(n)
    return s.rolling(n, min_periods=n).mean()


def ema(s: pd.Series, n: int) -> pd.Series:
    """Media móvil exponencial con ``alpha = 2/(n+1)``, recursiva (``adjust=False``)."""
    _check_period(n)
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def wilder(s: pd.Series, n: int) -> pd.Series:
    """Suavizado de Wilder (``alpha = 1/n``)."""
    _check_period(n)
    return s.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()


def true_range(df: pd.DataFrame) -> pd.Series:
    """True Range: ``max(h-l, |h-c_prev|, |l-c_prev|)``."""
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [df["high"] - df["low"], (df["high"] - prev_close).abs(), (df["low"] - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    return tr.rename("tr")


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    """Average True Range de Wilder."""
    return wilder(true_range(df), n).rename("atr")


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    """RSI de Wilder en [0, 100]. Sin pérdidas -> 100; sin movimiento -> 50."""
    delta = close.diff()
    gain = wilder(delta.clip(lower=0), n)
    loss = wilder(-delta.clip(upper=0), n)
    with np.errstate(divide="ignore", invalid="ignore"):
        rs = gain / loss
        out = 100 - 100 / (1 + rs)
    out = out.where(loss != 0, 100.0)
    out = out.where(~((gain == 0) & (loss == 0)), 50.0)
    return out.where(gain.notna() & loss.notna()).rename("rsi")


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """MACD = EMA(fast) - EMA(slow); señal = EMA(MACD, signal); histograma = MACD - señal."""
    if fast >= slow:
        raise ValueError("fast debe ser menor que slow")
    line = ema(close, fast) - ema(close, slow)
    sig = line.ewm(span=signal, adjust=False, min_periods=signal).mean()
    return pd.DataFrame({"macd": line, "signal": sig, "hist": line - sig})


def bollinger(close: pd.Series, n: int = 20, k: float = 2.0) -> pd.DataFrame:
    """Bandas de Bollinger con desviación estándar poblacional (ddof=0)."""
    mid = sma(close, n)
    std = close.rolling(n, min_periods=n).std(ddof=0)
    return pd.DataFrame({"mid": mid, "upper": mid + k * std, "lower": mid - k * std, "std": std})


def stoch_rsi(
    close: pd.Series, rsi_n: int = 14, stoch_n: int = 14, k_smooth: int = 3, d_smooth: int = 3
) -> pd.DataFrame:
    """Stochastic RSI en [0, 100]: %K = SMA(estocástico del RSI), %D = SMA(%K)."""
    r = rsi(close, rsi_n)
    lo = r.rolling(stoch_n, min_periods=stoch_n).min()
    hi = r.rolling(stoch_n, min_periods=stoch_n).max()
    rng = hi - lo
    raw = ((r - lo) / rng.replace(0, np.nan) * 100).where(rng != 0, 50.0)
    raw = raw.where(r.notna() & lo.notna())
    k = sma(raw, k_smooth)
    d = sma(k, d_smooth)
    return pd.DataFrame({"k": k, "d": d})


def adx(df: pd.DataFrame, n: int = 14) -> pd.DataFrame:
    """ADX, +DI y -DI de Wilder."""
    up = df["high"].diff()
    down = -df["low"].diff()
    plus_dm = up.where((up > down) & (up > 0), 0.0)
    minus_dm = down.where((down > up) & (down > 0), 0.0)
    plus_dm[up.isna()] = np.nan
    minus_dm[down.isna()] = np.nan
    atr_ = wilder(true_range(df).where(df["close"].shift(1).notna()), n)
    with np.errstate(divide="ignore", invalid="ignore"):
        plus_di = 100 * wilder(plus_dm, n) / atr_
        minus_di = 100 * wilder(minus_dm, n) / atr_
        dsum = plus_di + minus_di
        dx = (100 * (plus_di - minus_di).abs() / dsum).where(dsum != 0, 0.0)
    dx = dx.where(plus_di.notna() & minus_di.notna())
    return pd.DataFrame({"plus_di": plus_di, "minus_di": minus_di, "adx": wilder(dx, n)})


def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """On-Balance Volume acumulado desde el inicio de la serie (OBV[0] = 0)."""
    direction = np.sign(close.diff()).fillna(0.0)
    return (direction * volume).cumsum().rename("obv")


def vwap_rolling(df: pd.DataFrame, n: int) -> pd.Series:
    """VWAP de ventana móvil de ``n`` velas con precio típico (h+l+c)/3."""
    _check_period(n)
    tp = (df["high"] + df["low"] + df["close"]) / 3
    pv = (tp * df["volume"]).rolling(n, min_periods=n).sum()
    vol = df["volume"].rolling(n, min_periods=n).sum()
    return (pv / vol.replace(0, np.nan)).rename("vwap")


def vwap_session(df: pd.DataFrame, session: str = "1D") -> pd.Series:
    """VWAP anclado a sesiones UTC de duración ``session`` (por defecto, día UTC 00:00).

    El acumulado se reinicia en cada frontera de sesión; el valor en ``t`` incluye la vela ``t``.
    """
    tp = (df["high"] + df["low"] + df["close"]) / 3
    key = pd.DatetimeIndex(df.index).floor(session)
    pv = (tp * df["volume"]).groupby(key).cumsum()
    vol = df["volume"].groupby(key).cumsum()
    return (pv / vol.replace(0, np.nan)).rename("vwap")


def donchian(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Canal de Donchian de las ``n`` velas **anteriores** (excluye la vela actual)."""
    _check_period(n)
    upper = df["high"].rolling(n, min_periods=n).max().shift(1)
    lower = df["low"].rolling(n, min_periods=n).min().shift(1)
    return pd.DataFrame({"upper": upper, "lower": lower, "mid": (upper + lower) / 2})


def rolling_zscore(s: pd.Series, n: int) -> pd.Series:
    """Z-score de ``s`` respecto a la media/desviación de las ``n`` velas anteriores."""
    mean = s.rolling(n, min_periods=n).mean().shift(1)
    std = s.rolling(n, min_periods=n).std().shift(1)
    return ((s - mean) / std.replace(0, np.nan)).rename("zscore")


def rolling_percentile(s: pd.Series, n: int) -> pd.Series:
    """Fracción (0-1) de las ``n`` velas **anteriores** con valor estrictamente menor que ``s[t]``.

    Se calcula con el rango mínimo de ``s[t]`` dentro de la ventana ``[t-n, t]``:
    ``(rank_min - 1) / n``. NaN si la ventana contiene valores ausentes.
    """
    _check_period(n)
    ranks = s.rolling(n + 1, min_periods=n + 1).rank(method="min")
    return ((ranks - 1) / n).rename("percentile")


def crossover(a: pd.Series, b: pd.Series | float) -> pd.Series:
    """True en ``t`` si ``a`` cruza por encima de ``b`` entre ``t-1`` y ``t``."""
    bb = b if isinstance(b, pd.Series) else pd.Series(b, index=a.index)
    return ((a > bb) & (a.shift(1) <= bb.shift(1))).fillna(False).astype(bool)


def crossunder(a: pd.Series, b: pd.Series | float) -> pd.Series:
    """True en ``t`` si ``a`` cruza por debajo de ``b`` entre ``t-1`` y ``t``."""
    bb = b if isinstance(b, pd.Series) else pd.Series(b, index=a.index)
    return ((a < bb) & (a.shift(1) >= bb.shift(1))).fillna(False).astype(bool)


def higher_timeframe(
    df: pd.DataFrame, base_tf: pd.Timedelta, htf: pd.Timedelta, ema_period: int | None = None
) -> pd.DataFrame:
    """Resamplea OHLCV a una temporalidad superior y lo alinea **sin anticipación**.

    Una vela superior que abre en ``T`` solo está disponible cuando cierra (``T + htf``). La
    vela base ``t`` toma su decisión al cierre (``t + base_tf``), así que recibe la última
    vela superior con ``T + htf <= t + base_tf``. Las velas superiores incompletas al final
    de los datos nunca se exponen. Con ``ema_period`` se añade la columna ``ema`` calculada
    sobre los cierres de la temporalidad superior (no sobre la serie base rellenada).
    """
    if htf <= base_tf:
        raise ValueError("htf debe ser mayor que la temporalidad base")
    agg = df.resample(htf, label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    )
    counts = df["close"].resample(htf, label="left", closed="left").count()
    expected = int(htf / base_tf)
    agg = agg[counts >= expected]
    if ema_period is not None:
        agg["ema"] = ema(agg["close"], ema_period)
    agg.index = agg.index + htf
    keys = df.index + base_tf
    aligned = agg.reindex(agg.index.union(keys)).ffill().reindex(keys)
    aligned.index = df.index
    return aligned
