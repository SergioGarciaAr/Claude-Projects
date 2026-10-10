"""Flujo completo reproducible con datos SINTÉTICOS, usando la API de Python.

Ejecución: ``python examples/full_workflow.py``. Todo se escribe en un directorio temporal.
Los datos sintéticos validan el funcionamiento del sistema, no la rentabilidad de nada.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from bybit_quant_lab import DISCLAIMER
from bybit_quant_lab.analytics import compute_metrics
from bybit_quant_lab.config import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.reporting import build_metadata, comparison_report
from bybit_quant_lab.signals import CombinationConfig
from bybit_quant_lab.validation import ExperimentLog
from bybit_quant_lab.validation.research import Researcher

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Compara las diez estrategias y evalúa una vez la selección en test."""
    print(DISCLAIMER)
    out = Path(tempfile.mkdtemp(prefix="bql_example_"))
    cfg = load_config(ROOT / "configs/default.yaml", {"output_dir": str(out)})
    params = load_strategy_params(ROOT / "configs/strategies.yaml")
    data = generate_synthetic_ohlcv(bars=6000, timeframe="1h", seed=42)

    research = Researcher(
        data,
        "BTCUSDT",
        "1h",
        cfg,
        params,
        funding=None,
        log=ExperimentLog(out / "experiments.jsonl"),
    )
    combos = [
        CombinationConfig(name="vote_all", mode="simple_vote", min_margin=3),
        CombinationConfig(name="category_2", mode="category_consensus", min_categories=2),
    ]
    comparison = research.run_comparison(combos)
    val = comparison.summary.query("segment == 'validation' and cost_mode == 'net'")
    print(val[["candidate", "kind", "net_profit", "sharpe", "num_trades"]].to_string(index=False))

    meta = build_metadata(
        cfg,
        research.data_hash,
        {"source": "synthetic", "synthetic": True},
        {"symbol": "BTCUSDT", "timeframe": "1h"},
    )
    report = comparison_report(comparison, meta, out / "comparison.html")
    print(f"\nInforme de comparación: {report}")

    final = research.run_final_test(comparison.selection, combos)
    for name, res in final["candidates"].items():
        m = compute_metrics(res["net"])
        print(f"Test final {name}: neto={m['net_profit']:.2f} operaciones={m['num_trades']}")


if __name__ == "__main__":
    main()
