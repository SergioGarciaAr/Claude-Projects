"""Pruebas de segmentación, walk-forward, sobreajuste y protección del test final."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from bybit_quant_lab.config import AppConfig
from bybit_quant_lab.signals import CombinationConfig
from bybit_quant_lab.validation.benchmarks import buy_and_hold, cash_benchmark, random_signals
from bybit_quant_lab.validation.experiment_log import (
    ExperimentLog,
    FinalTestAlreadyEvaluatedError,
)
from bybit_quant_lab.validation.overfitting import (
    deflated_sharpe,
    expected_max_sharpe,
    holm_bonferroni,
    mean_pvalue,
    probabilistic_sharpe,
    top_trade_dependence,
)
from bybit_quant_lab.validation.research import Researcher
from bybit_quant_lab.validation.sensitivity import param_grid, stability_summary
from bybit_quant_lab.validation.splits import chronological_split, walk_forward_windows

IDX = pd.date_range("2024-01-01", periods=1000, freq="1h", tz="UTC")


def test_chronological_split_is_ordered_and_disjoint() -> None:
    segs = chronological_split(IDX, 0.6, 0.2, embargo_bars=5)
    tr, va, te = segs["train"], segs["validation"], segs["test"]
    assert tr.start_pos == 0 and tr.end_pos == 599
    assert va.start_pos == 605 and te.start_pos == 805 and te.end_pos == 999
    assert tr.end < va.start and va.end < te.start
    with pytest.raises(ValueError):
        chronological_split(IDX, 0.7, 0.3)


def test_walk_forward_windows_rolling_and_anchored() -> None:
    w = walk_forward_windows(IDX, 400, 100)
    assert len(w) == 6
    for tr, te in w:
        assert tr.bars == 400 and te.bars == 100 and tr.end < te.start
    assert w[1][0].start_pos == 100
    a = walk_forward_windows(IDX, 400, 100, anchored=True)
    assert all(tr.start_pos == 0 for tr, _ in a) and a[2][0].bars == 600
    with pytest.raises(ValueError):
        walk_forward_windows(IDX[:100], 400, 100)


def test_param_grid_limit() -> None:
    assert len(param_grid({"a": [1, 2], "b": [3, 4, 5]}, 10)) == 6
    with pytest.raises(ValueError):
        param_grid({"a": list(range(20)), "b": list(range(20))}, 100)
    s = stability_summary(pd.DataFrame({"sharpe": [1.0, -1.0, 0.5, 2.0]}), "sharpe")
    assert s["fraction_positive"] == 0.75 and s["best"] == 2.0


def test_statistics_functions() -> None:
    rng = np.random.default_rng(1)
    good = pd.Series(rng.normal(0.002, 0.01, 2000))
    noise = pd.Series(rng.normal(0.0, 0.01, 2000))
    assert probabilistic_sharpe(good) > 0.95
    assert expected_max_sharpe(1, 0.01) == 0.0
    assert expected_max_sharpe(100, 0.01) > expected_max_sharpe(10, 0.01) > 0
    d1 = deflated_sharpe(good, 1)
    d100 = deflated_sharpe(good, 100, list(rng.normal(0, 0.05, 100)))
    assert d100["dsr"] < d1["dsr"]
    p, reliable = mean_pvalue(noise)
    assert p is not None and reliable and 0 <= p <= 1
    h = holm_bonferroni({"a": 0.01, "b": 0.04, "c": 0.5, "d": None})
    assert h["a"]["reject"] and not h["b"]["reject"] and h["a"]["p_adj"] == pytest.approx(0.03)
    t = pd.DataFrame({"net_pnl": [100.0, -10, -10, -10, 5]})
    dep = top_trade_dependence(t, k=1)
    assert dep["net_without_top_k"] == -25 and dep["sign_flips_without_top_k"]


def test_benchmarks(synth: pd.DataFrame) -> None:
    cfg = AppConfig()
    seg = chronological_split(pd.DatetimeIndex(synth.index), 0.6, 0.2)["validation"]
    bh = buy_and_hold(synth, cfg, seg, "BTCUSDT", "1h")
    ret = synth["close"].iloc[seg.end_pos] / synth["open"].iloc[seg.start_pos] - 1
    assert bh.final_equity / 10_000 - 1 == pytest.approx(ret, abs=0.003)
    assert bh.final_equity / 10_000 - 1 < ret  # los costes reducen el resultado
    assert cash_benchmark(synth, cfg, seg, "BTCUSDT", "1h").final_equity == 10_000
    ref = pd.DataFrame(
        {
            "signal": [0, 1, 1, 0, 0, -1, -1, 0] * 50,
            "conviction": 0.0,
            "stop_distance": 1.0,
            "take_profit_distance": np.nan,
            "trailing_distance": np.nan,
        }
    )
    r1, r2 = random_signals(ref, 3), random_signals(ref, 3)
    pd.testing.assert_frame_equal(r1, r2)
    assert not random_signals(ref, 4)["signal"].equals(r1["signal"])


@pytest.fixture
def researcher(synth: pd.DataFrame, tmp_path: Path) -> Researcher:
    cfg = AppConfig.model_validate({"validation": {"wf_train_bars": 800, "wf_test_bars": 300}})
    return Researcher(synth, "BTCUSDT", "1h", cfg, log=ExperimentLog(tmp_path / "log.jsonl"))


COMBOS = [
    CombinationConfig(name="vote", mode="simple_vote", min_margin=2),
    CombinationConfig(name="weighted", mode="weighted_vote"),
]


def test_comparison_never_touches_test_segment(researcher: Researcher) -> None:
    out = researcher.run_comparison(COMBOS, ["ema_crossover", "donchian_breakout", "adx_di"])
    assert set(out.summary["segment"]) == {"train", "validation"}
    test_start = researcher.segments["test"].start
    for res in out.results.values():
        assert res.equity.index.max() < test_start
    recs = researcher.log.records()
    assert recs and all(r["segment"] != "test" for r in recs)
    # Gross vs net: los costes reducen el resultado de cada estrategia con operaciones
    s = out.summary.set_index(["candidate", "segment", "cost_mode"])
    for name in ("ema_crossover", "donchian_breakout", "adx_di"):
        net, gross = s.loc[(name, "train", "net")], s.loc[(name, "train", "gross")]
        if net["num_trades"] > 0:
            assert net["total_costs"] > 0 and gross["total_costs"] == 0
    assert "weighted" in out.redundancy.get("thresholds", {})
    assert out.statistics["n_trials_logged"] >= 5


def test_final_test_guard(researcher: Researcher) -> None:
    out = researcher.run_comparison(
        COMBOS, ["ema_crossover", "donchian_breakout", "adx_di"], top_k=2
    )
    ft = researcher.run_final_test(out.selection, COMBOS)
    assert not ft["repeated"]
    for r in ft["candidates"].values():
        assert r["net"].start >= researcher.segments["test"].start
    with pytest.raises(FinalTestAlreadyEvaluatedError):
        researcher.run_final_test(out.selection, COMBOS)
    again = researcher.run_final_test(out.selection, COMBOS, allow_repeat=True)
    assert again["repeated"]
    tampered = {**out.selection, "data_hash": "otro"}
    with pytest.raises(ValueError):
        researcher.run_final_test(tampered, COMBOS)


def test_walk_forward_and_sensitivity(researcher: Researcher) -> None:
    wf = researcher.walk_forward("ema_crossover", {"fast": [8, 12], "slow": [26, 50]})
    assert wf["grid_size"] == 4 and len(wf["windows"]) >= 2
    for _, row in wf["windows"].iterrows():
        assert row["train_end"] < row["test_start"]
    table, summary = researcher.sensitivity("ema_crossover", {"fast": [8, 12]})
    assert len(table) == 2 and summary["n"] >= 1
    with pytest.raises(ValueError):
        researcher.sensitivity("ema_crossover", {"fast": [8]}, segment="test")


def test_comparison_is_deterministic(synth: pd.DataFrame) -> None:
    a = Researcher(synth, "BTCUSDT", "1h", AppConfig()).run_comparison(COMBOS, ["adx_di"])
    b = Researcher(synth, "BTCUSDT", "1h", AppConfig()).run_comparison(COMBOS, ["adx_di"])
    pd.testing.assert_frame_equal(a.summary, b.summary)
    assert a.selection == b.selection
