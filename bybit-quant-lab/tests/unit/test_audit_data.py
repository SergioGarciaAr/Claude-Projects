"""Auditoría de la capa de datos de Bybit y de la sintaxis de la CLI (sin red).

Las pruebas usan dobles HTTP. Verifican la forma de las peticiones (endpoint, categoría,
intervalo, ventanas, límites), el orden cronológico y UTC, y que velas y funding no se
mezclen. La conectividad real con api.bybit.com NO se prueba aquí.
"""

from __future__ import annotations

import re
import shlex
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from bybit_quant_lab.cli import build_parser
from bybit_quant_lab.data.bybit_client import BybitAPIError, BybitPublicClient
from bybit_quant_lab.data.downloader import download_funding, download_ohlcv, funding_path
from bybit_quant_lab.data.storage import data_hash, dataset_path, load_dataset
from tests.unit.test_data import FakeExchange, FakeResponse

ROOT = Path(__file__).resolve().parents[2]


def _client(session: Any, now: str = "2030-01-01") -> BybitPublicClient:
    return BybitPublicClient(
        session=session,
        sleep=lambda _: None,
        backoff_seconds=0,
        min_request_interval=0,
        clock=lambda: pd.Timestamp(now, tz="UTC"),
    )


@pytest.mark.parametrize(
    ("tf", "interval", "minutes"),
    [("5m", "5", 5), ("15m", "15", 15), ("1h", "60", 60), ("4h", "240", 240)],
)
def test_kline_request_shape_per_timeframe(tf: str, interval: str, minutes: int) -> None:
    fake = FakeExchange()
    start = pd.Timestamp("2024-01-01", tz="UTC")
    end = start + pd.Timedelta(minutes=minutes * 2500)
    df = _client(fake).fetch_klines("btcusdt", tf, start, end)
    assert len(df) == 2500 and len(fake.calls) == 3
    step = minutes * 60_000
    for i, call in enumerate(fake.calls):
        assert call["url"] == "https://api.bybit.com/v5/market/kline"
        assert call["category"] == "linear" and call["symbol"] == "BTCUSDT"
        assert call["interval"] == interval and call["limit"] == 1000
        # Ventanas contiguas, sin solape: [start, end] inclusivo de ≤ 1000 velas
        assert call["start"] == int(start.timestamp() * 1000) + i * 1000 * step
        assert call["end"] - call["start"] < 1000 * step
    assert df.index.tz is not None and str(df.index.tz) == "UTC"
    assert df.index.is_monotonic_increasing and not df.index.duplicated().any()
    assert ((df.index - start) % pd.Timedelta(minutes=minutes) == pd.Timedelta(0)).all()


def test_unaligned_start_is_rounded_up_to_bar_boundary() -> None:
    fake = FakeExchange()
    df = _client(fake).fetch_klines(
        "BTCUSDT",
        "1h",
        pd.Timestamp("2024-01-01 00:30", tz="UTC"),
        pd.Timestamp("2024-01-01 05:00", tz="UTC"),
    )
    assert df.index[0] == pd.Timestamp("2024-01-01 01:00", tz="UTC") and len(df) == 4


def test_funding_uses_its_own_endpoint_and_file(tmp_path: Path) -> None:
    fake = FakeExchange()
    client = _client(fake)
    s = pd.Timestamp("2024-01-01", tz="UTC")
    download_ohlcv(client, "BTCUSDT", "1h", s, s + pd.Timedelta(hours=48), tmp_path)
    before = data_hash(load_dataset(dataset_path(tmp_path, "BTCUSDT", "1h")))
    n_kline_calls = len(fake.calls)
    path = download_funding(client, "BTCUSDT", s, s + pd.Timedelta(days=3), tmp_path)
    funding_calls = fake.calls[n_kline_calls:]
    assert funding_calls and all(
        c["url"].endswith("/v5/market/funding/history") for c in funding_calls
    )
    assert all("interval" not in c for c in funding_calls)
    assert path == funding_path(tmp_path, "BTCUSDT") and path.name == "BTCUSDT_funding.parquet"
    assert data_hash(load_dataset(dataset_path(tmp_path, "BTCUSDT", "1h"))) == before


class StuckFundingAPI:
    """API que ignora endTime y devuelve siempre la misma página completa."""

    def __init__(self) -> None:
        self.calls = 0

    def get(self, url: str, params: dict[str, Any], timeout: float) -> FakeResponse:
        self.calls += 1
        if self.calls > 50:
            raise AssertionError("bucle de paginación sin fin")
        base = 1_704_067_200_000  # 2024-01-01
        items = [
            {"fundingRate": "0.0001", "fundingRateTimestamp": str(base + k * 28_800_000)}
            for k in range(200)
        ]
        return FakeResponse(200, {"retCode": 0, "result": {"list": items}})


def test_funding_pagination_stops_if_api_does_not_advance() -> None:
    api = StuckFundingAPI()
    with pytest.raises(BybitAPIError, match="no avanza"):
        _client(api).fetch_funding_history(
            "BTCUSDT", pd.Timestamp("2020-01-01", tz="UTC"), pd.Timestamp("2025-01-01", tz="UTC")
        )
    assert api.calls <= 3


def _documented_commands() -> list[str]:
    """Órdenes ``bql`` dentro de bloques de código de README y docs."""
    files = [ROOT / "README.md", ROOT / "data/README.md", *sorted((ROOT / "docs").glob("*.md"))]
    cmds = []
    for f in files:
        blocks = re.findall(r"```(?:bash)?\n(.*?)```", f.read_text(encoding="utf-8"), re.S)
        for block in blocks:
            for raw in block.replace("\\\n", " ").splitlines():
                cmd = raw.split("  #")[0].strip()
                if cmd.startswith("bql "):
                    cmds.append(cmd)
    return cmds


def test_every_documented_cli_command_parses() -> None:
    cmds = _documented_commands()
    assert len(cmds) >= 20
    parser = build_parser()
    for cmd in cmds:
        tokens = shlex.split(cmd)[1:]
        try:
            parser.parse_args(tokens)
        except SystemExit as exc:  # argparse sale con código != 0 ante sintaxis inválida
            pytest.fail(f"Comando documentado inválido: {cmd!r} ({exc})")
