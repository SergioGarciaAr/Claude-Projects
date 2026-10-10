"""Auditoría estadística y metodológica.

Incluye la verificación de fórmulas (DSR/PSR, Holm, bootstrap) por dos vías independientes
(ejemplo numérico y simulación de Monte Carlo) y pruebas de regresión de los hallazgos de
fuga de información documentados en docs/audit_report.md.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from bybit_quant_lab.config import AppConfig
from bybit_quant_lab.signals import CombinationConfig, combine_signals
from bybit_quant_lab.strategies import available_strategies, create_strategy
from bybit_quant_lab.validation.experiment_log import (
    ExperimentLog,
    FinalTestAlreadyEvaluatedError,
)
from bybit_quant_lab.validation.overfitting import (
    bootstrap_mean_ci,
    expected_max_sharpe,
    holm_bonferroni,
    probabilistic_sharpe,
    psr_from_moments,
)
from bybit_quant_lab.validation.research import Researcher

ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------- fórmulas
def test_dsr_reproduces_worked_example() -> None:
    # Ejemplo numérico de Bailey y López de Prado (2014): N=100 pruebas, varianza anual de
    # los Sharpe 0.5, T=1250 observaciones diarias, SR anual 2.5, asimetría -3, curtosis 10.
    # Valores esperados SR0 ≈ 0.1132 y DSR ≈ 0.9004 (citados del artículo; recalculados aquí).
    sr0 = expected_max_sharpe(100, 0.5 / 250)
    assert sr0 == pytest.approx(0.1132, abs=5e-4)
    dsr = psr_from_moments(2.5 / math.sqrt(250), -3.0, 10.0, 1250, sr0)
    assert dsr == pytest.approx(0.9004, abs=5e-4)


def test_expected_max_sharpe_matches_monte_carlo() -> None:
    # La aproximación de valores extremos debe acercarse al máximo esperado simulado.
    rng = np.random.default_rng(0)
    for n in (10, 100, 1000):
        mc = rng.standard_normal((4000, n)).max(axis=1).mean()
        assert expected_max_sharpe(n, 1.0) == pytest.approx(mc, rel=0.03)


def test_psr_is_calibrated_under_null() -> None:
    # Con SR verdadero 0 y retornos i.i.d., P(PSR > 0.95) debe ser ≈ 5 %.
    rng = np.random.default_rng(1)
    psr = [probabilistic_sharpe(pd.Series(rng.normal(0, 0.01, 500))) for _ in range(2000)]
    rate = float(np.mean([p is not None and p > 0.95 for p in psr]))
    assert 0.035 <= rate <= 0.065


def test_holm_step_down_by_hand() -> None:
    h = holm_bonferroni({"a": 0.01, "b": 0.04, "c": 0.03, "d": 0.005})
    # Ordenados: d .005·4=.02, a .01·3=.03, c .03·2=.06, b max(.06, .04·1)=.06
    assert [h[k]["p_adj"] for k in "dacb"] == pytest.approx([0.02, 0.03, 0.06, 0.06])
    assert [h[k]["reject"] for k in "dacb"] == [True, True, False, False]


def test_bootstrap_ci_coverage() -> None:
    rng = np.random.default_rng(2)
    hits = 0
    for i in range(300):
        ci = bootstrap_mean_ci(pd.Series(rng.normal(1.0, 2.0, 60)), 500, seed=i)
        assert ci is not None
        hits += ci[0] <= 1.0 <= ci[1]
    assert 0.89 <= hits / 300 <= 0.98  # cobertura nominal 95 %


# ------------------------------------------------------------- fugas de información
@pytest.fixture
def researcher(synth: pd.DataFrame, tmp_path: Path) -> Researcher:
    cfg = AppConfig.model_validate({"validation": {"wf_train_bars": 600, "wf_test_bars": 200}})
    return Researcher(synth, "BTCUSDT", "1h", cfg, log=ExperimentLog(tmp_path / "log.jsonl"))


def test_walk_forward_never_uses_test_segment(researcher: Researcher) -> None:
    wf = researcher.walk_forward("ema_crossover", {"fast": [8, 12]})
    test_start = researcher.segments["test"].start
    assert (pd.to_datetime(wf["windows"]["test_end"]) < test_start).all()
    assert wf["oos_equity"].index.max() < test_start


def test_final_test_period_can_only_be_used_once(researcher: Researcher) -> None:
    combos = [CombinationConfig(name="vote", mode="simple_vote", min_margin=2)]
    names = ["ema_crossover", "donchian_breakout", "adx_di", "macd_momentum"]
    out1 = researcher.run_comparison(combos, names, top_k=1)
    out2 = researcher.run_comparison(combos, names, top_k=2)
    assert out1.selection["selection_id"] != out2.selection["selection_id"]
    researcher.run_final_test(out1.selection, combos)
    # Una selección distinta sobre el MISMO período de test también debe bloquearse.
    with pytest.raises(FinalTestAlreadyEvaluatedError):
        researcher.run_final_test(out2.selection, combos)


def test_final_test_uses_frozen_member_params(synth: pd.DataFrame, tmp_path: Path) -> None:
    combos = [
        CombinationConfig(name="vote", mode="simple_vote", min_margin=1, conflict_policy="net")
    ]
    log = ExperimentLog(tmp_path / "log.jsonl")
    a = Researcher(synth, "BTCUSDT", "1h", AppConfig(), log=log)
    out = a.run_comparison(combos, available_strategies(), top_k=1)
    sel = dict(out.selection)
    sel["selected"] = [
        {
            "name": "vote",
            "kind": "combination",
            "params": out.candidates["vote"].params,
            "validation_score": 0.0,
        }
    ]
    # Tras la selección, el usuario cambia parámetros en el YAML: no debe afectar al test.
    changed = {"ema_crossover": {"fast": 5, "slow": 60}, "adx_di": {"adx_threshold": 40}}
    b = Researcher(synth, "BTCUSDT", "1h", AppConfig(), changed, log=log)
    ft = b.run_final_test(sel, combos)
    frames = {n: create_strategy(n).generate_signals(synth) for n in available_strategies()}
    cats = {n: create_strategy(n).category.value for n in frames}
    expected = combine_signals(
        frames, cats, CombinationConfig.model_validate(out.candidates["vote"].params), a.regime
    )
    seg = a.segments["test"]
    ref = a.simulate(
        type(out.candidates["vote"])("vote", "combination", expected, {}), seg, record=False
    )
    pd.testing.assert_frame_equal(ft["candidates"]["vote"]["net"].equity, ref.equity)


def test_final_test_rejects_changed_config(researcher: Researcher, synth: pd.DataFrame) -> None:
    out = researcher.run_comparison([], ["adx_di", "donchian_breakout"], top_k=1)
    other = AppConfig.model_validate(
        {"costs": {"taker_fee": 0.0001}, "validation": {"wf_train_bars": 600, "wf_test_bars": 200}}
    )
    r2 = Researcher(synth, "BTCUSDT", "1h", other, log=researcher.log)
    with pytest.raises(ValueError, match="configuración"):
        r2.run_final_test(out.selection, [])


def test_combination_thresholds_not_tuned_on_validation(researcher: Researcher) -> None:
    combos = [CombinationConfig(name="weighted", mode="weighted_vote")]
    researcher.run_comparison(combos, ["ema_crossover", "adx_di", "macd_momentum"])
    trials = [r for r in researcher.log.records() if r.get("candidate_kind") == "combo_trial"]
    assert trials, "los ensayos de umbral deben registrarse"
    # El umbral se elige en entrenamiento; validación queda limpia para la selección.
    assert {r["segment"] for r in trials} == {"train"}


def test_configured_combinations_are_not_equivalent() -> None:
    import yaml

    raw = yaml.safe_load((ROOT / "configs/strategies.yaml").read_text())["combinations"]
    cfgs = [CombinationConfig.model_validate(c) for c in raw]

    def key(c: CombinationConfig) -> tuple | None:
        # simple_vote(margen k, veto) ≡ min_consensus(k, veto): n_dir ≥ k y n_opuesto = 0.
        if c.conflict_policy == "veto" and c.members is None and not c.regime_rules:
            if c.mode == "simple_vote":
                return ("veto", c.min_margin)
            if c.mode == "min_consensus":
                return ("veto", c.min_votes)
        return None

    keys = [k for k in map(key, cfgs) if k is not None]
    assert len(keys) == len(set(keys)), "dos combinaciones configuradas son idénticas"


def test_simple_vote_veto_equals_min_consensus_veto(synth: pd.DataFrame) -> None:
    # Documenta la equivalencia matemática que motivó el cambio de configuración.
    frames = {n: create_strategy(n).generate_signals(synth) for n in available_strategies()}
    cats = {n: create_strategy(n).category.value for n in frames}
    a = combine_signals(frames, cats, CombinationConfig(mode="simple_vote", min_margin=3))
    b = combine_signals(frames, cats, CombinationConfig(mode="min_consensus", min_votes=3))
    pd.testing.assert_series_equal(a["signal"], b["signal"])


def test_random_benchmark_calibrated_only_on_simulated_segment() -> None:
    from bybit_quant_lab.validation.benchmarks import random_signals

    # Referencia activa solo en la segunda mitad: calibrar con la primera mitad no debe
    # producir actividad (la segunda mitad no puede influir).
    ref = pd.DataFrame(
        {
            "signal": [0] * 500 + [1, 1, 0, 0] * 125,
            "conviction": 0.0,
            "stop_distance": 1.0,
            "take_profit_distance": np.nan,
            "trailing_distance": np.nan,
        }
    )
    first_half = random_signals(ref, 1, slice(0, 500))
    assert (first_half["signal"] == 0).all()
    assert (random_signals(ref, 1, slice(500, 1000))["signal"] != 0).any()
