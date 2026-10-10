"""Pruebas de la capa de datos con respuestas HTTP simuladas (sin red)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pytest
import requests

from bybit_quant_lab.data.bybit_client import BybitAPIError, BybitPublicClient
from bybit_quant_lab.data.downloader import download_ohlcv, load_funding, missing_ranges
from bybit_quant_lab.data.importers import import_ohlcv
from bybit_quant_lab.data.storage import data_hash, dataset_path, load_dataset, load_metadata
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.data.validation import clean_ohlcv, validate_ohlcv
from bybit_quant_lab.risk.instruments import spec_from_bybit

NOW = pd.Timestamp("2024-01-10", tz="UTC")


class FakeResponse:
    def __init__(self, status: int, payload: Any) -> None:
        self.status_code = status
        self._payload = payload

    def json(self) -> Any:
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


class FakeExchange:
    """Simula /v5/market/kline (lista en orden descendente, como Bybit) y funding."""

    def __init__(self, failures: list[Any] | None = None) -> None:
        self.failures = list(failures or [])
        self.calls: list[dict[str, Any]] = []

    def get(self, url: str, params: dict[str, Any], timeout: float) -> FakeResponse:
        self.calls.append({"url": url, **params})
        if self.failures:
            f = self.failures.pop(0)
            if isinstance(f, Exception):
                raise f
            return f
        if url.endswith("/kline"):
            step = int(params["interval"]) * 60_000
            start = params["start"] - params["start"] % step
            if start < params["start"]:
                start += step
            rows = []
            for t in range(start, params["end"] + 1, step):
                price = 100 + (t // step) % 7
                rows.append(
                    [
                        str(t),
                        str(price),
                        str(price + 1),
                        str(price - 1),
                        str(price + 0.5),
                        "10",
                        "1000",
                    ]
                )
            rows = rows[: params["limit"]][::-1]
            return FakeResponse(
                200, {"retCode": 0, "retMsg": "OK", "result": {"category": "linear", "list": rows}}
            )
        if url.endswith("/funding/history"):
            step = 8 * 3600 * 1000
            end = params["endTime"] - params["endTime"] % step
            items = []
            t = end
            while t >= params["startTime"] and len(items) < params["limit"]:
                items.append(
                    {
                        "symbol": params["symbol"],
                        "fundingRate": "0.0001",
                        "fundingRateTimestamp": str(t),
                    }
                )
                t -= step
            return FakeResponse(200, {"retCode": 0, "result": {"list": items}})
        raise AssertionError(url)


def _client(fake: FakeExchange) -> BybitPublicClient:
    return BybitPublicClient(
        session=fake,
        sleep=lambda _: None,
        backoff_seconds=0,
        min_request_interval=0,
        clock=lambda: NOW,
    )


def test_fetch_klines_paginates_and_sorts() -> None:
    fake = FakeExchange()
    client = _client(fake)
    client._clock = lambda: pd.Timestamp("2030-01-01", tz="UTC")
    start = pd.Timestamp("2024-01-01", tz="UTC")
    df = client.fetch_klines("BTCUSDT", "1h", start, start + pd.Timedelta(hours=2500), limit=1000)
    assert len(fake.calls) == 3
    assert all(c["limit"] == 1000 for c in fake.calls)
    assert df.index.is_monotonic_increasing
    assert df.index[0] == start and len(df) == 2500
    assert validate_ohlcv(df, "1h").is_valid


def test_fetch_klines_drops_unclosed_candle() -> None:
    client = _client(FakeExchange())
    client._clock = lambda: pd.Timestamp("2024-01-01 05:30", tz="UTC")
    start = pd.Timestamp("2024-01-01", tz="UTC")
    df = client.fetch_klines("BTCUSDT", "1h", start, start + pd.Timedelta(hours=24))
    assert len(df) == 5  # 00:00..04:00; la vela de las 05:00 sigue abierta


def test_retries_on_transient_errors() -> None:
    fake = FakeExchange(
        failures=[
            requests.ConnectionError("down"),
            FakeResponse(503, {}),
            FakeResponse(200, ValueError("no json")),
            FakeResponse(200, {"retCode": 10006, "retMsg": "Too many visits"}),
        ]
    )
    start = pd.Timestamp("2024-01-01", tz="UTC")
    df = _client(fake).fetch_klines("BTCUSDT", "1h", start, start + pd.Timedelta(hours=5))
    assert len(df) == 5
    assert len(fake.calls) == 5


def test_non_retryable_and_exhausted_errors() -> None:
    start = pd.Timestamp("2024-01-01", tz="UTC")
    end = start + pd.Timedelta(hours=5)
    with pytest.raises(BybitAPIError, match="10001"):
        _client(
            FakeExchange([FakeResponse(200, {"retCode": 10001, "retMsg": "bad"})])
        ).fetch_klines("BTCUSDT", "1h", start, end)
    with pytest.raises(BybitAPIError, match="403"):
        _client(FakeExchange([FakeResponse(403, {})])).fetch_klines("BTCUSDT", "1h", start, end)
    client = _client(FakeExchange([FakeResponse(502, {})] * 10))
    client.max_retries = 2
    with pytest.raises(BybitAPIError, match="agotados"):
        client.fetch_klines("BTCUSDT", "1h", start, end)
    bad_rows = FakeResponse(200, {"retCode": 0, "result": {"list": [["1", "2"]]}})
    with pytest.raises(BybitAPIError, match="formato"):
        _client(FakeExchange([bad_rows])).fetch_klines("BTCUSDT", "1h", start, end)


def test_incremental_download_only_fetches_missing(tmp_path: Path) -> None:
    fake = FakeExchange()
    client = _client(fake)
    s = pd.Timestamp("2024-01-01", tz="UTC")
    first = download_ohlcv(client, "BTCUSDT", "1h", s, s + pd.Timedelta(hours=48), tmp_path)
    assert first.rows == 48
    calls_before = len(fake.calls)
    again = download_ohlcv(client, "BTCUSDT", "1h", s, s + pd.Timedelta(hours=48), tmp_path)
    assert len(fake.calls) == calls_before and again.fetched_ranges == []
    more = download_ohlcv(client, "BTCUSDT", "1h", s, s + pd.Timedelta(hours=72), tmp_path)
    assert more.rows == 72 and len(more.fetched_ranges) == 1
    meta = load_metadata(dataset_path(tmp_path, "BTCUSDT", "1h"))
    assert meta["source"] == "bybit_v5_public" and len(meta["downloads"]) == 3
    assert meta["sha256"] == data_hash(load_dataset(dataset_path(tmp_path, "BTCUSDT", "1h")))


def test_missing_ranges_detects_internal_gaps() -> None:
    idx = pd.date_range("2024-01-01", periods=10, freq="1h", tz="UTC").delete([4, 5])
    s, e = idx[0], idx[0] + pd.Timedelta(hours=12)
    ranges = missing_ranges(idx, s, e, "1h")
    assert ranges == [
        (idx[0] + pd.Timedelta(hours=4), idx[0] + pd.Timedelta(hours=6)),
        (idx[0] + pd.Timedelta(hours=10), e),
    ]


def test_funding_download_and_load(tmp_path: Path) -> None:
    from bybit_quant_lab.data.downloader import download_funding

    client = _client(FakeExchange())
    s = pd.Timestamp("2023-12-01", tz="UTC")
    download_funding(client, "BTCUSDT", s, s + pd.Timedelta(days=100), tmp_path)
    f = load_funding(tmp_path, "BTCUSDT")
    assert f is not None and len(f) == 301 and f.index.is_monotonic_increasing
    assert load_funding(tmp_path, "ETHUSDT") is None


def test_validation_detects_problems() -> None:
    df = generate_synthetic_ohlcv(50, "1h")
    bad = pd.concat([df, df.iloc[[10]]])
    bad.iloc[5, bad.columns.get_loc("high")] = bad.iloc[5]["low"] - 1
    bad.iloc[7, bad.columns.get_loc("close")] = np.nan
    bad = bad.drop(bad.index[20:23])
    rep = validate_ohlcv(bad, "1h")
    assert rep.duplicates == 1 and rep.unsorted and rep.invalid_candles == 1
    assert rep.nan_rows == 1 and rep.gaps == 1 and rep.missing_bars == 3
    assert not rep.is_valid
    cleaned, rep2 = clean_ohlcv(bad, "1h")
    assert rep2.is_valid and rep2.gaps >= 1
    assert len(cleaned) == 50 - 3 - 2


def test_validation_detects_misaligned_timestamps() -> None:
    df = generate_synthetic_ohlcv(10, "1h")
    df.index = df.index + pd.Timedelta(minutes=7)
    assert validate_ohlcv(df, "1h").misaligned == 10


def test_import_csv_epoch_ms(tmp_path: Path) -> None:
    df = generate_synthetic_ohlcv(30, "15m")
    csv = tmp_path / "x.csv"
    out = df.reset_index()
    out["timestamp"] = out["open_time"].astype("int64") // 10**6
    out.drop(columns=["open_time"]).to_csv(csv, index=False)
    path, rep = import_ohlcv(csv, "ETHUSDT", "15m", tmp_path)
    loaded = load_dataset(path)
    assert rep.is_valid and len(loaded) == 30
    assert loaded.index.tz is not None
    np.testing.assert_allclose(loaded["close"].to_numpy(), df["close"].to_numpy())
    assert json.loads(path.with_suffix(".meta.json").read_text())["source"] == "import"


def test_synthetic_is_deterministic() -> None:
    a = generate_synthetic_ohlcv(500, seed=3)
    b = generate_synthetic_ohlcv(500, seed=3)
    pd.testing.assert_frame_equal(a, b)
    assert validate_ohlcv(a, "1h").is_valid


def test_spec_from_bybit() -> None:
    info = {
        "symbol": "BTCUSDT",
        "priceFilter": {"tickSize": "0.10"},
        "lotSizeFilter": {
            "qtyStep": "0.001",
            "minOrderQty": "0.001",
            "maxOrderQty": "1190",
            "maxMktOrderQty": "119",
            "minNotionalValue": "5",
        },
    }
    spec = spec_from_bybit(info)
    assert spec.verified and spec.max_qty == 119 and spec.round_qty(0.0019) == 0.001
