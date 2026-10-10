"""Pruebas de combinación de señales, régimen y redundancia."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from bybit_quant_lab.signals import (
    CombinationConfig,
    classify_regime,
    combine_signals,
    fit_weights,
    select_non_redundant,
    signal_agreement,
    signal_correlation,
)
from bybit_quant_lab.strategies.base import empty_signal_frame

IDX = pd.date_range("2024-01-01", periods=6, freq="1h", tz="UTC")
CATS = {"a": "volume", "b": "trend", "c": "indicator", "d": "indicator"}


def _frame(values: list[int], stop: float = 2.0, conv: float = 1.0) -> pd.DataFrame:
    f = empty_signal_frame(IDX)
    f["signal"] = values
    f["conviction"] = [conv if v else 0.0 for v in values]
    f["stop_distance"] = stop
    return f


FRAMES = {
    "a": _frame([1, 1, 1, 0, -1, 1], stop=1.0),
    "b": _frame([1, 1, 0, 0, -1, -1], stop=3.0),
    "c": _frame([1, -1, 0, 0, -1, 0], stop=5.0),
    "d": _frame([0, 0, 1, 1, 0, 0], stop=7.0),
}


def test_simple_vote_with_veto_and_net() -> None:
    veto = combine_signals(FRAMES, CATS, CombinationConfig(mode="simple_vote", min_margin=2))
    assert veto["signal"].tolist() == [1, 0, 1, 0, -1, 0]
    net = combine_signals(
        FRAMES, CATS, CombinationConfig(mode="simple_vote", min_margin=1, conflict_policy="net")
    )
    assert net["signal"].tolist() == [1, 1, 1, 1, -1, 0]


def test_stop_is_median_of_agreeing_members() -> None:
    out = combine_signals(FRAMES, CATS, CombinationConfig(mode="simple_vote", min_margin=2))
    assert out["stop_distance"].iloc[0] == pytest.approx(3.0)  # a, b, c -> mediana(1, 3, 5)
    assert out["stop_distance"].iloc[2] == pytest.approx(4.0)  # a, d -> mediana(1, 7)
    assert out["conviction"].iloc[1] == 0.0


def test_min_consensus_counts_votes() -> None:
    out = combine_signals(FRAMES, CATS, CombinationConfig(mode="min_consensus", min_votes=3))
    assert out["signal"].tolist() == [1, 0, 0, 0, -1, 0]


def test_category_consensus_requires_distinct_categories() -> None:
    out = combine_signals(
        FRAMES, CATS, CombinationConfig(mode="category_consensus", min_categories=2)
    )
    # Vela 2: a(volume)=1 y d(indicator)=1 -> dos categorías; vela 3: solo d -> no.
    assert out["signal"].tolist() == [1, 0, 1, 0, -1, 0]
    same_cat = {"c": FRAMES["c"], "d": FRAMES["d"]}
    out2 = combine_signals(
        same_cat, CATS, CombinationConfig(mode="category_consensus", min_categories=2)
    )
    assert (out2["signal"] == 0).all()


def test_weighted_vote_uses_weights_and_threshold() -> None:
    cfg = CombinationConfig(
        mode="weighted_vote",
        weights={"a": 3, "b": 1, "c": 0, "d": 0},
        threshold=0.5,
        conflict_policy="net",
    )
    out = combine_signals(FRAMES, CATS, cfg)
    assert out["signal"].tolist()[:3] == [1, 1, 1]
    with pytest.raises(ValueError):
        combine_signals(FRAMES, CATS, cfg.model_copy(update={"weights": {"a": -1}}))


def test_missing_member_and_missing_data() -> None:
    with pytest.raises(KeyError):
        combine_signals(FRAMES, CATS, CombinationConfig(members=["a", "zz"]))
    partial = {"a": FRAMES["a"], "b": FRAMES["b"].iloc[:3]}  # b sin datos al final
    out = combine_signals(partial, CATS, CombinationConfig(mode="simple_vote", min_margin=2))
    assert out["signal"].iloc[5] == 0  # b ausente = abstención


def test_regime_filter_blocks_disallowed_strategies() -> None:
    regime = pd.DataFrame(
        {
            "trend": ["trend", "range", "trend", "range", "trend", "range"],
            "volatility": "normal_vol",
            "liquidity": "normal_liq",
        },
        index=IDX,
    )
    cfg = CombinationConfig(
        mode="min_consensus",
        min_votes=1,
        conflict_policy="net",
        members=["a"],
        regime_rules={"a": {"trend": ["trend"]}},
    )
    out = combine_signals(FRAMES, CATS, cfg, regime)
    assert out["signal"].tolist() == [1, 0, 1, 0, -1, 0]
    with pytest.raises(ValueError):
        combine_signals(FRAMES, CATS, cfg)


def test_redundancy_selection() -> None:
    sig = pd.DataFrame(
        {"x": [1, 1, 0, -1, 0, 1], "y": [1, 1, 0, -1, 0, 1], "z": [0, -1, 1, 0, 1, -1]}
    )
    corr = signal_correlation(sig)
    kept, dropped = select_non_redundant(corr, 0.9)
    assert kept == ["x", "z"] and dropped == {"y": "x"}
    assert signal_agreement(sig).loc["x", "y"] == 1.0


def test_fit_weights_uses_only_given_returns() -> None:
    rets = {"good": pd.Series([0.01, 0.02, 0.0, 0.01]), "bad": pd.Series([-0.01, -0.02, 0, 0])}
    w = fit_weights(rets)
    assert w["bad"] == 0 and w["good"] == pytest.approx(1.0)
    assert fit_weights({"x": pd.Series([-0.1, -0.2])}) == {"x": 1.0}


def test_regime_is_causal(synth: pd.DataFrame) -> None:
    full = classify_regime(synth)
    part = classify_regime(synth.iloc[:1200])
    pd.testing.assert_frame_equal(full.iloc[:1200], part)
    assert set(full["trend"].unique()) <= {"trend", "range", "unknown"}
    assert np.all(full["liquidity"].isin(["low_liq", "normal_liq", "unknown"]))
