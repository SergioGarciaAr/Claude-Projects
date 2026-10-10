"""Flujo completo de la CLI con datos sintéticos (sin red).

Valida que el pipeline funciona y es reproducible; NO valida rentabilidad alguna.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from bybit_quant_lab.cli import main

ROOT = Path(__file__).resolve().parents[2]


def _base(tmp: Path) -> list[str]:
    return [
        "--config",
        str(ROOT / "configs/default.yaml"),
        "--strategies-config",
        str(ROOT / "configs/strategies.yaml"),
        "--data-dir",
        str(tmp / "data"),
        "--output-dir",
        str(tmp / "out"),
    ]


@pytest.fixture(scope="module")
def workspace(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp = tmp_path_factory.mktemp("bql")
    assert (
        main(
            [
                *_base(tmp),
                "synth",
                "--symbol",
                "BTCUSDT",
                "--timeframe",
                "1h",
                "--bars",
                "4000",
                "--seed",
                "11",
            ]
        )
        == 0
    )
    return tmp


def test_list_and_validate(workspace: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([*_base(workspace), "list-strategies"]) == 0
    assert len(capsys.readouterr().out.strip().splitlines()) == 10
    assert (
        main([*_base(workspace), "validate-data", "--symbol", "BTCUSDT", "--timeframe", "1h"]) == 0
    )


def test_backtest_report_and_regeneration(workspace: Path) -> None:
    out = workspace / "bt"
    assert (
        main(
            [
                *_base(workspace),
                "backtest",
                "--symbol",
                "BTCUSDT",
                "--timeframe",
                "1h",
                "--strategy",
                "ema_crossover",
                "--segment",
                "validation",
                "--out",
                str(out),
            ]
        )
        == 0
    )
    for f in (
        "report.html",
        "equity.csv",
        "trades.csv",
        "metrics.json",
        "metadata.json",
        "run.json",
        "risk_events.json",
    ):
        assert (out / f).exists(), f
    meta = json.loads((out / "metadata.json").read_text())
    for key in ("git", "data_hash", "config_hash", "config", "seed", "package_version"):
        assert key in meta
    assert meta["data_synthetic"] is True
    html = (out / "report.html").read_text()
    assert meta["data_hash"] in html and "SINTÉTICOS" in html
    assert "no garantizan resultados futuros" in html
    metrics = json.loads((out / "metrics.json").read_text())
    (out / "report.html").unlink()
    assert main([*_base(workspace), "report", "--run-dir", str(out)]) == 0
    assert (out / "report.html").exists()
    # Reproducibilidad: misma ejecución -> mismas métricas
    out2 = workspace / "bt2"
    assert (
        main(
            [
                *_base(workspace),
                "backtest",
                "--symbol",
                "BTCUSDT",
                "--timeframe",
                "1h",
                "--strategy",
                "ema_crossover",
                "--segment",
                "validation",
                "--out",
                str(out2),
            ]
        )
        == 0
    )
    assert json.loads((out2 / "metrics.json").read_text()) == metrics
    pd.testing.assert_frame_equal(pd.read_csv(out / "trades.csv"), pd.read_csv(out2 / "trades.csv"))


def test_compare_then_final_test_once(workspace: Path) -> None:
    out = workspace / "cmp"
    assert (
        main(
            [
                *_base(workspace),
                "compare",
                "--symbol",
                "BTCUSDT",
                "--timeframe",
                "1h",
                "--out",
                str(out),
            ]
        )
        == 0
    )
    summary = pd.read_csv(out / "summary.csv")
    assert set(summary["segment"]) == {"train", "validation"}
    kinds = summary.groupby("kind")["candidate"].nunique().to_dict()
    assert kinds["strategy"] == 10 and kinds["combination"] == 6 and kinds["benchmark"] == 3
    sel = json.loads((out / "selection.json").read_text())
    assert sel["selected"]
    ft = workspace / "ft"
    args = [*_base(workspace), "final-test", "--selection", str(out / "selection.json")]
    assert main([*args, "--out", str(ft)]) == 0
    assert (ft / "report.html").exists()
    assert main([*args, "--out", str(workspace / "ft2")]) == 3  # segunda vez: bloqueado
    log = [json.loads(x) for x in (workspace / "out/experiments.jsonl").read_text().splitlines()]
    assert sum(1 for r in log if r["kind"] == "final_test") == 1


def test_walkforward_and_sensitivity(workspace: Path) -> None:
    out = workspace / "wf"
    assert (
        main(
            [
                *_base(workspace),
                "walkforward",
                "--symbol",
                "BTCUSDT",
                "--timeframe",
                "1h",
                "--strategy",
                "donchian_breakout",
                "--grid",
                '{"channel": [20, 40]}',
                "--out",
                str(out),
            ]
        )
        == 0
    )
    assert (out / "report.html").exists() and (out / "windows.csv").exists()
    out = workspace / "sens"
    assert (
        main(
            [
                *_base(workspace),
                "sensitivity",
                "--symbol",
                "BTCUSDT",
                "--timeframe",
                "1h",
                "--strategy",
                "rsi_reversion",
                "--out",
                str(out),
            ]
        )
        == 0
    )
    assert len(pd.read_csv(out / "grid.csv")) == 8


def test_import_csv(workspace: Path, tmp_path: Path) -> None:
    from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv

    csv = tmp_path / "eth.csv"
    generate_synthetic_ohlcv(500, "15m").reset_index().to_csv(csv, index=False)
    assert (
        main(
            [
                *_base(workspace),
                "import",
                "--symbol",
                "ETHUSDT",
                "--timeframe",
                "15m",
                "--file",
                str(csv),
            ]
        )
        == 0
    )
    assert (workspace / "data/processed/ETHUSDT_15m.parquet").exists()


def test_missing_data_and_bad_params_give_clean_errors(
    workspace: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert (
        main(
            [
                *_base(workspace),
                "backtest",
                "--symbol",
                "BTCUSDT",
                "--timeframe",
                "4h",
                "--strategy",
                "adx_di",
            ]
        )
        == 1
    )
    assert "No existe" in capsys.readouterr().err
    assert (
        main(
            [
                *_base(workspace),
                "backtest",
                "--symbol",
                "BTCUSDT",
                "--timeframe",
                "1h",
                "--strategy",
                "adx_di",
                "--params",
                '{"adx_period": -3}',
            ]
        )
        == 1
    )


def test_markets_command(workspace: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        main(
            [
                *_base(workspace),
                "synth",
                "--symbol",
                "ETHUSDT",
                "--timeframe",
                "1h",
                "--bars",
                "3000",
                "--seed",
                "5",
            ]
        )
        == 0
    )
    out = workspace / "mk"
    assert (
        main(
            [
                *_base(workspace),
                "markets",
                "--symbols",
                "BTCUSDT",
                "ETHUSDT",
                "--timeframes",
                "1h",
                "4h",
                "--strategies",
                "adx_di,ema_crossover",
                "--out",
                str(out),
            ]
        )
        == 0
    )
    matrix = pd.read_csv(out / "matrix.csv")
    # 4h no existe para ninguno de los dos símbolos: se omite con aviso
    assert set(zip(matrix["symbol"], matrix["timeframe"], strict=True)) == {
        ("BTCUSDT", "1h"),
        ("ETHUSDT", "1h"),
    }
    assert "se omite" in capsys.readouterr().err
    meta = json.loads((out / "metadata.json").read_text())
    assert set(meta["data_hashes"]) == {"BTCUSDT_1h", "ETHUSDT_1h"}
    assert (out / "report.html").exists()
