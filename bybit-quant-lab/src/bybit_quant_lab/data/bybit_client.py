"""Cliente de solo lectura para la API pública de mercado de Bybit V5.

Endpoints usados (públicos, sin autenticación):

* ``GET /v5/market/kline`` — velas OHLCV (máx. 1000 por petición).
* ``GET /v5/market/funding/history`` — historial de funding (máx. 200 por petición).
* ``GET /v5/market/instruments-info`` — especificaciones del instrumento.

Este módulo no implementa, ni implementará en el flujo predeterminado, ningún endpoint de
trading. No acepta ni almacena claves API.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any, Protocol

import pandas as pd
import requests

from bybit_quant_lab.logging_utils import get_logger
from bybit_quant_lab.timeframes import bybit_interval, timeframe_delta

logger = get_logger("data.bybit")

#: retCode de Bybit considerados transitorios (10000: timeout del servidor,
#: 10006: demasiadas peticiones, 10016: error interno del servidor).
RETRYABLE_RET_CODES = {10000, 10006, 10016}
RETRYABLE_HTTP = {429, 500, 502, 503, 504}


class BybitAPIError(RuntimeError):
    """Error no recuperable o reintentos agotados al consultar Bybit."""


class HTTPSession(Protocol):
    """Interfaz mínima de sesión HTTP (permite inyectar dobles de prueba)."""

    def get(self, url: str, params: dict[str, Any], timeout: float) -> Any:
        """Realiza una petición GET."""
        ...


def _to_ms(ts: pd.Timestamp) -> int:
    return (
        int(ts.tz_convert("UTC").timestamp() * 1000)
        if ts.tzinfo
        else int(ts.tz_localize("UTC").timestamp() * 1000)
    )


class BybitPublicClient:
    """Cliente HTTP con reintentos, backoff exponencial y espaciado mínimo entre peticiones."""

    def __init__(
        self,
        base_url: str = "https://api.bybit.com",
        session: HTTPSession | None = None,
        max_retries: int = 5,
        backoff_seconds: float = 1.0,
        min_request_interval: float = 0.05,
        timeout_seconds: float = 15.0,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], pd.Timestamp] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session: HTTPSession = session if session is not None else requests.Session()  # type: ignore[assignment]
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds
        self.min_request_interval = min_request_interval
        self.timeout_seconds = timeout_seconds
        self._sleep = sleep
        self._clock = clock or (lambda: pd.Timestamp.now(tz="UTC"))
        self._last_request = 0.0
        self.request_count = 0

    # ------------------------------------------------------------------ HTTP
    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.min_request_interval:
            self._sleep(self.min_request_interval - elapsed)
        self._last_request = time.monotonic()

    def get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        """GET con reintentos. Devuelve ``result`` de la respuesta o lanza ``BybitAPIError``."""
        url = f"{self.base_url}{path}"
        last_error = "sin intentos"
        for attempt in range(self.max_retries + 1):
            if attempt:
                wait = self.backoff_seconds * (2 ** (attempt - 1))
                logger.warning(
                    "reintento %d/%d en %.1fs: %s", attempt, self.max_retries, wait, last_error
                )
                self._sleep(wait)
            self._throttle()
            self.request_count += 1
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout_seconds)
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_error = f"error de red: {exc}"
                continue
            status = int(getattr(resp, "status_code", 0))
            if status == 403:
                raise BybitAPIError(
                    "HTTP 403: acceso denegado o IP limitada por frecuencia. Bybit recomienda "
                    "detener las peticiones y esperar al menos 10 minutos."
                )
            if status in RETRYABLE_HTTP:
                last_error = f"HTTP {status}"
                continue
            if status != 200:
                raise BybitAPIError(f"HTTP {status} no recuperable en {path}")
            try:
                payload = resp.json()
            except ValueError:
                last_error = "respuesta no JSON"
                continue
            if not isinstance(payload, dict) or "retCode" not in payload:
                raise BybitAPIError(f"Respuesta con formato inesperado: {str(payload)[:200]}")
            code = int(payload["retCode"])
            if code in RETRYABLE_RET_CODES:
                last_error = f"retCode {code}: {payload.get('retMsg')}"
                continue
            if code != 0:
                raise BybitAPIError(f"retCode {code}: {payload.get('retMsg')}")
            result = payload.get("result")
            if not isinstance(result, dict):
                raise BybitAPIError("Respuesta sin campo 'result' válido")
            return result
        raise BybitAPIError(f"Reintentos agotados en {path}: {last_error}")

    # --------------------------------------------------------------- Klines
    def fetch_klines(
        self,
        symbol: str,
        timeframe: str,
        start: pd.Timestamp,
        end: pd.Timestamp,
        limit: int = 1000,
        category: str = "linear",
    ) -> pd.DataFrame:
        """Descarga velas cerradas en ``[start, end)`` paginando por ventanas de ``limit`` velas.

        Se usan ventanas fijas de tamaño ``limit * timeframe`` para que cada petición contenga
        como máximo ``limit`` velas, sin depender del orden en que la API devuelve la lista.
        La vela en curso (no cerrada) se descarta.
        """
        delta = timeframe_delta(timeframe)
        start = _align(start, delta, ceil=True)
        now = self._clock()
        end = min(end, _align(now, delta, ceil=False))
        frames: list[pd.DataFrame] = []
        cursor = start
        while cursor < end:
            window_end = min(cursor + delta * limit, end)
            params = {
                "category": category,
                "symbol": symbol.upper(),
                "interval": bybit_interval(timeframe),
                "start": _to_ms(cursor),
                "end": _to_ms(window_end) - 1,
                "limit": limit,
            }
            result = self.get("/v5/market/kline", params)
            frames.append(_parse_klines(result))
            cursor = window_end
        if not frames:
            return _empty_klines()
        df = pd.concat(frames)
        df = df[~df.index.duplicated(keep="last")].sort_index()
        df = df[(df.index >= start) & (df.index < end)]
        closed = df.index + delta <= now
        return df[closed]

    # -------------------------------------------------------------- Funding
    def fetch_funding_history(
        self,
        symbol: str,
        start: pd.Timestamp,
        end: pd.Timestamp,
        limit: int = 200,
        category: str = "linear",
    ) -> pd.Series:
        """Descarga tasas de funding históricas en ``[start, end]`` paginando hacia atrás."""
        rows: dict[pd.Timestamp, float] = {}
        cursor_end = end
        while cursor_end >= start:
            params = {
                "category": category,
                "symbol": symbol.upper(),
                "startTime": _to_ms(start),
                "endTime": _to_ms(cursor_end),
                "limit": limit,
            }
            result = self.get("/v5/market/funding/history", params)
            items = result.get("list") or []
            if not isinstance(items, list):
                raise BybitAPIError("Campo 'list' de funding inválido")
            if not items:
                break
            stamps = []
            for item in items:
                try:
                    ts = pd.to_datetime(int(item["fundingRateTimestamp"]), unit="ms", utc=True)
                    rows[ts] = float(item["fundingRate"])
                except (KeyError, TypeError, ValueError) as exc:
                    raise BybitAPIError(f"Registro de funding inválido: {item}") from exc
                stamps.append(ts)
            oldest = min(stamps)
            if len(items) < limit or oldest <= start:
                break
            cursor_end = oldest - pd.Timedelta(milliseconds=1)
        series = pd.Series(rows, dtype="float64", name="funding_rate").sort_index()
        series.index.name = "funding_time"
        return series[(series.index >= start) & (series.index <= end)]

    # ----------------------------------------------------------- Instrument
    def fetch_instrument_info(self, symbol: str, category: str = "linear") -> dict[str, Any]:
        """Devuelve el registro de ``instruments-info`` del símbolo."""
        result = self.get(
            "/v5/market/instruments-info", {"category": category, "symbol": symbol.upper()}
        )
        items = result.get("list") or []
        if not items:
            raise BybitAPIError(f"Instrumento no encontrado: {symbol}")
        info: dict[str, Any] = items[0]
        return info


def _align(ts: pd.Timestamp, delta: pd.Timedelta, ceil: bool) -> pd.Timestamp:
    ts = ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")
    return ts.ceil(delta) if ceil else ts.floor(delta)


def _empty_klines() -> pd.DataFrame:
    idx = pd.DatetimeIndex([], tz="UTC", name="open_time")
    cols = ["open", "high", "low", "close", "volume", "turnover"]
    return pd.DataFrame({c: pd.Series(dtype="float64") for c in cols}, index=idx)


def _parse_klines(result: dict[str, Any]) -> pd.DataFrame:
    """Convierte ``result.list`` (``[startTime, o, h, l, c, volume, turnover]``) en DataFrame."""
    items = result.get("list")
    if not isinstance(items, list):
        raise BybitAPIError("Campo 'list' de velas ausente o inválido")
    if not items:
        return _empty_klines()
    bad = [row for row in items if not isinstance(row, list | tuple) or len(row) < 7]
    if bad:
        raise BybitAPIError(f"Vela con formato inválido: {bad[0]}")
    df = pd.DataFrame(
        [row[:7] for row in items],
        columns=["open_time", "open", "high", "low", "close", "volume", "turnover"],
    )
    df["open_time"] = pd.to_datetime(
        pd.to_numeric(df["open_time"], errors="coerce"), unit="ms", utc=True
    )
    if df["open_time"].isna().any():
        raise BybitAPIError("Marca de tiempo de vela no numérica")
    df = df.set_index("open_time")
    return df.apply(pd.to_numeric, errors="coerce").astype("float64")
