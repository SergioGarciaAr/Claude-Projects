"""Flujos de investigación: comparación, walk-forward y test final.

Protocolo anti-fuga implementado:

1. Las señales de todas las estrategias se calculan una vez sobre toda la serie (indicadores
   causales) y cada segmento se simula por separado.
2. Redundancia y pesos de combinación se ajustan **solo con entrenamiento**; los umbrales de
   la votación ponderada se eligen **solo con validación**.
3. La selección de candidatos usa **solo validación** y se congela en ``selection.json``.
4. El test final evalúa únicamente la selección congelada, una vez (``guard_final_test``).
5. Cada configuración evaluada se registra en el log de experimentos.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bybit_quant_lab.analytics.metrics import bar_returns, compute_metrics
from bybit_quant_lab.backtesting.engine import BacktestEngine
from bybit_quant_lab.backtesting.results import BacktestResult
from bybit_quant_lab.config.loader import config_hash
from bybit_quant_lab.config.models import AppConfig
from bybit_quant_lab.data.storage import data_hash
from bybit_quant_lab.logging_utils import get_logger
from bybit_quant_lab.signals.combiners import CombinationConfig, combine_signals, fit_weights
from bybit_quant_lab.signals.redundancy import (
    select_non_redundant,
    signal_agreement,
    signal_correlation,
)
from bybit_quant_lab.signals.regime import classify_regime
from bybit_quant_lab.strategies import available_strategies, create_strategy
from bybit_quant_lab.timeframes import bars_per_year
from bybit_quant_lab.validation.benchmarks import buy_and_hold, cash_benchmark, random_benchmark
from bybit_quant_lab.validation.experiment_log import ExperimentLog, guard_final_test
from bybit_quant_lab.validation.overfitting import (
    bootstrap_mean_ci,
    deflated_sharpe,
    holm_bonferroni,
    mean_pvalue,
    top_trade_dependence,
)
from bybit_quant_lab.validation.sensitivity import param_grid, stability_summary
from bybit_quant_lab.validation.splits import Segment, chronological_split, walk_forward_windows

logger = get_logger("validation.research")

KEY_METRICS = (
    "net_profit",
    "net_profit_pct",
    "gross_profit_before_costs",
    "sharpe",
    "sortino",
    "max_drawdown",
    "profit_factor",
    "win_rate",
    "expectancy",
    "num_trades",
    "exposure",
    "total_costs",
    "total_funding",
    "cagr",
)


def gross_config(cfg: AppConfig) -> AppConfig:
    """Copia de ``cfg`` sin comisiones, slippage ni funding (resultado bruto)."""
    costs = cfg.costs.model_copy(
        update={"taker_fee": 0.0, "maker_fee": 0.0, "slippage_bps": 0.0, "use_funding": False}
    )
    return cfg.model_copy(update={"costs": costs})


def per_bar_sharpe(result: BacktestResult) -> float | None:
    """Sharpe no anualizado por vela (para DSR y varianza entre pruebas)."""
    r = bar_returns(result.equity["equity"], result.initial_capital)
    std = float(r.std(ddof=1)) if len(r) > 1 else 0.0
    return float(r.mean() / std) if std > 0 else None


@dataclass
class Candidate:
    """Estrategia individual o combinación evaluable."""

    name: str
    kind: str
    signals: pd.DataFrame
    params: dict[str, Any]


@dataclass
class ComparisonOutput:
    """Resultados de ``run_comparison``."""

    summary: pd.DataFrame
    results: dict[tuple[str, str, str], BacktestResult]
    segments: dict[str, Segment]
    correlation: pd.DataFrame
    agreement: pd.DataFrame
    redundancy: dict[str, Any]
    selection: dict[str, Any]
    statistics: dict[str, Any]
    candidates: dict[str, Candidate] = field(default_factory=dict)


class Researcher:
    """Orquesta señales, segmentos, simulaciones y registro para un símbolo/temporalidad."""

    def __init__(
        self,
        data: pd.DataFrame,
        symbol: str,
        timeframe: str,
        config: AppConfig,
        strategy_params: dict[str, dict[str, Any]] | None = None,
        funding: pd.Series | None = None,
        log: ExperimentLog | None = None,
    ) -> None:
        self.data = data
        self.symbol = symbol.upper()
        self.timeframe = timeframe
        self.config = config
        self.strategy_params = strategy_params or {}
        self.funding = funding
        self.log = log
        self.data_hash = data_hash(data)
        self.regime = classify_regime(data)
        v = config.validation
        self.segments = chronological_split(
            pd.DatetimeIndex(data.index), v.train_frac, v.validation_frac, v.embargo_bars
        )

    # ------------------------------------------------------------ helpers
    def strategy_candidate(self, name: str, overrides: dict[str, Any] | None = None) -> Candidate:
        """Calcula las señales de una estrategia con sus parámetros configurados."""
        params = {**self.strategy_params.get(name, {}), **(overrides or {})}
        strat = create_strategy(name, params)
        return Candidate(
            name, "strategy", strat.generate_signals(self.data), strat.params.model_dump()
        )

    def simulate(
        self, cand: Candidate, segment: Segment, gross: bool = False, record: bool = True
    ) -> BacktestResult:
        """Simula un candidato en un segmento (neto por defecto) y lo registra."""
        cfg = gross_config(self.config) if gross else self.config
        res = BacktestEngine(cfg, self.symbol, self.timeframe).run(
            self.data,
            cand.signals,
            funding=self.funding,
            start=segment.start,
            end=segment.end,
            regime=self.regime["label"],
            label=cand.name,
            params=cand.params,
        )
        if record and self.log is not None:
            m = self.metrics(res)
            self.log.append(
                {
                    "kind": "evaluation",
                    "candidate": cand.name,
                    "candidate_kind": cand.kind,
                    "segment": segment.name,
                    "cost_mode": "gross" if gross else "net",
                    "symbol": self.symbol,
                    "timeframe": self.timeframe,
                    "data_hash": self.data_hash,
                    "config_hash": config_hash(cfg),
                    "params": cand.params,
                    "metrics": {k: m.get(k) for k in KEY_METRICS},
                }
            )
        return res

    def metrics(self, res: BacktestResult) -> dict[str, Any]:
        """Métricas con los umbrales de la configuración."""
        b = self.config.backtest
        return compute_metrics(res, b.min_trades_for_stats, b.min_days_for_cagr)

    def _score(self, m: dict[str, Any]) -> float:
        v = self.config.validation
        if (m.get("num_trades") or 0) < v.min_trades_selection:
            return float("-inf")
        val = m.get(v.selection_metric)
        return float(val) if val is not None and np.isfinite(val) else float("-inf")

    # ---------------------------------------------------------- comparison
    def build_combinations(
        self, singles: dict[str, Candidate], combos: list[CombinationConfig]
    ) -> tuple[dict[str, Candidate], dict[str, Any]]:
        """Construye combinaciones; redundancia y pesos se ajustan con entrenamiento."""
        tr = self.segments["train"]
        frames = {n: c.signals for n, c in singles.items()}
        cats = {n: create_strategy(n).category.value for n in singles}
        train_sig = pd.DataFrame(
            {n: f["signal"].iloc[tr.start_pos : tr.end_pos + 1] for n, f in frames.items()}
        )
        corr = signal_correlation(train_sig)
        out: dict[str, Candidate] = {}
        info: dict[str, Any] = {"train_correlation": corr}
        for combo in combos:
            cfg = combo
            if cfg.members is None and cfg.name.startswith("dedup"):
                kept, dropped = select_non_redundant(corr.fillna(0), 0.7)
                cfg = cfg.model_copy(update={"members": kept})
                info["dedup"] = {"kept": kept, "dropped": dropped}
            if cfg.mode == "weighted_vote" and cfg.weights is None:
                members = cfg.members or list(frames)
                train_rets = {
                    n: bar_returns(r.equity["equity"], r.initial_capital)
                    for n in members
                    for r in [self.simulate(singles[n], tr, record=False)]
                }
                cfg = cfg.model_copy(update={"weights": fit_weights(train_rets)})
                info.setdefault("weights", {})[cfg.name] = cfg.weights
                # Umbral elegido con validación (rejilla pequeña y registrada)
                best_t, best_s = cfg.threshold, float("-inf")
                for t in (0.2, 0.3, 0.4, 0.5):
                    trial = cfg.model_copy(update={"threshold": t})
                    c = Candidate(
                        f"{cfg.name}@{t}",
                        "combo_trial",
                        combine_signals(frames, cats, trial, self.regime),
                        {},
                    )
                    s = self._score(self.metrics(self.simulate(c, self.segments["validation"])))
                    if s > best_s:
                        best_t, best_s = t, s
                cfg = cfg.model_copy(update={"threshold": best_t})
                info.setdefault("thresholds", {})[cfg.name] = best_t
            sig = combine_signals(frames, cats, cfg, self.regime)
            out[cfg.name] = Candidate(cfg.name, "combination", sig, cfg.model_dump())
        return out, info

    def run_comparison(
        self,
        combos: list[CombinationConfig],
        strategies: list[str] | None = None,
        top_k: int = 3,
    ) -> ComparisonOutput:
        """Compara estrategias, combinaciones y benchmarks en train y validación."""
        names = strategies or available_strategies()
        singles = {n: self.strategy_candidate(n) for n in names}
        combo_cands, combo_info = self.build_combinations(singles, combos)
        cands = {**singles, **combo_cands}
        rows: list[dict[str, Any]] = []
        results: dict[tuple[str, str, str], BacktestResult] = {}
        for seg_name in ("train", "validation"):
            seg = self.segments[seg_name]
            for cand in cands.values():
                for gross in (False, True):
                    res = self.simulate(cand, seg, gross=gross)
                    mode = "gross" if gross else "net"
                    results[(cand.name, seg_name, mode)] = res
                    rows.append(self._row(cand.name, cand.kind, seg_name, mode, res))
            ref = singles[names[0]].signals
            for bench in (
                buy_and_hold(self.data, self.config, seg, self.symbol, self.timeframe),
                cash_benchmark(self.data, self.config, seg, self.symbol, self.timeframe),
                random_benchmark(
                    self.data,
                    ref,
                    self.config,
                    seg,
                    self.symbol,
                    self.timeframe,
                    self.config.backtest.seed,
                    self.funding,
                ),
            ):
                results[(bench.label, seg_name, "net")] = bench
                rows.append(self._row(bench.label, "benchmark", seg_name, "net", bench))
        summary = pd.DataFrame(rows)
        all_sig = pd.DataFrame({n: c.signals["signal"] for n, c in singles.items()})
        tr = self.segments["train"]
        corr_train = signal_correlation(all_sig.iloc[tr.start_pos : tr.end_pos + 1])
        agree_train = signal_agreement(all_sig.iloc[tr.start_pos : tr.end_pos + 1])
        selection, stats = self._select(cands, results, summary, top_k)
        return ComparisonOutput(
            summary=summary,
            results=results,
            segments=self.segments,
            correlation=corr_train,
            agreement=agree_train,
            redundancy={k: v for k, v in combo_info.items() if k != "train_correlation"},
            selection=selection,
            statistics=stats,
            candidates=cands,
        )

    def _row(
        self, name: str, kind: str, seg: str, mode: str, res: BacktestResult
    ) -> dict[str, Any]:
        m = self.metrics(res)
        return {
            "candidate": name,
            "kind": kind,
            "segment": seg,
            "cost_mode": mode,
            **{k: m.get(k) for k in KEY_METRICS},
        }

    def _select(
        self, cands: dict[str, Candidate], results: dict, summary: pd.DataFrame, top_k: int
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        val = summary[
            (summary["segment"] == "validation")
            & (summary["cost_mode"] == "net")
            & summary["kind"].isin(["strategy", "combination"])
        ].copy()
        val["score"] = [
            self._score({str(k): v for k, v in r.items()}) for r in val.to_dict("records")
        ]
        ranked = val.sort_values("score", ascending=False)
        chosen = [r for r in ranked.to_dict("records") if np.isfinite(r["score"])][:top_k]
        n_trials = self.log.count_distinct_configs(self.data_hash) if self.log else len(val)
        trial_srs = [
            s
            for n in val["candidate"]
            if (s := per_bar_sharpe(results[(n, "validation", "net")])) is not None
        ]
        stats: dict[str, Any] = {"n_trials_logged": n_trials, "n_candidates_validation": len(val)}
        pvals = {}
        for name in val["candidate"]:
            tr = results[(name, "validation", "net")].trades
            p, reliable = mean_pvalue(tr["net_pnl"]) if len(tr) else (None, False)
            pvals[name] = p
            stats.setdefault("pvalue_reliable", {})[name] = reliable
        stats["holm_validation"] = holm_bonferroni(pvals)
        details = {}
        for r in chosen:
            res = results[(r["candidate"], "validation", "net")]
            rets = bar_returns(res.equity["equity"], res.initial_capital)
            details[r["candidate"]] = {
                "deflated_sharpe": deflated_sharpe(rets, max(n_trials, 1), trial_srs),
                "bootstrap_ci_trade_pnl": bootstrap_mean_ci(
                    res.trades["net_pnl"],
                    self.config.validation.bootstrap_samples,
                    self.config.backtest.seed,
                )
                if len(res.trades)
                else None,
                "top_trade_dependence": top_trade_dependence(res.trades),
            }
        stats["selected_details"] = details
        selection = {
            "selection_id": _selection_id(
                self.data_hash, [r["candidate"] for r in chosen], config_hash(self.config)
            ),
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "data_hash": self.data_hash,
            "config_hash": config_hash(self.config),
            "selection_metric": self.config.validation.selection_metric,
            "segments": {k: s.to_dict() for k, s in self.segments.items()},
            "selected": [
                {
                    "name": r["candidate"],
                    "kind": r["kind"],
                    "params": cands[r["candidate"]].params,
                    "validation_score": r["score"],
                }
                for r in chosen
            ],
        }
        return selection, stats

    # ---------------------------------------------------------- final test
    def run_final_test(
        self, selection: dict[str, Any], combos: list[CombinationConfig], allow_repeat: bool = False
    ) -> dict[str, Any]:
        """Evalúa la selección congelada en el período de test (una sola vez)."""
        if selection["data_hash"] != self.data_hash:
            raise ValueError("Los datos no coinciden con los usados en la selección")
        if self.log is None:
            raise ValueError("El test final requiere un log de experimentos")
        repeated = guard_final_test(self.log, selection["selection_id"], allow_repeat)
        seg = self.segments["test"]
        singles = {
            n: Candidate(
                n,
                "strategy",
                create_strategy(n, self._strategy_params_from(selection, n)).generate_signals(
                    self.data
                ),
                {},
            )
            for n in available_strategies()
        }
        frames = {n: c.signals for n, c in singles.items()}
        cats = {n: create_strategy(n).category.value for n in singles}
        out: dict[str, Any] = {
            "selection_id": selection["selection_id"],
            "repeated": repeated,
            "segment": seg.to_dict(),
            "candidates": {},
        }
        for sel in selection["selected"]:
            if sel["kind"] == "strategy":
                cand = Candidate(
                    sel["name"],
                    "strategy",
                    create_strategy(sel["name"], sel["params"]).generate_signals(self.data),
                    sel["params"],
                )
            else:
                cfg = CombinationConfig.model_validate(sel["params"])
                cand = Candidate(
                    sel["name"],
                    "combination",
                    combine_signals(frames, cats, cfg, self.regime),
                    sel["params"],
                )
            net = self.simulate(cand, seg, record=False)
            gross = self.simulate(cand, seg, gross=True, record=False)
            out["candidates"][sel["name"]] = {"net": net, "gross": gross}
        bh = buy_and_hold(self.data, self.config, seg, self.symbol, self.timeframe)
        out["benchmarks"] = {
            "buy_and_hold": bh,
            "cash": cash_benchmark(self.data, self.config, seg, self.symbol, self.timeframe),
        }
        self.log.append(
            {
                "kind": "final_test",
                "selection_id": selection["selection_id"],
                "repeated": repeated,
                "data_hash": self.data_hash,
                "metrics": {
                    n: {k: self.metrics(v["net"]).get(k) for k in KEY_METRICS}
                    for n, v in out["candidates"].items()
                },
            }
        )
        return out

    def _strategy_params_from(self, selection: dict[str, Any], name: str) -> dict[str, Any]:
        for sel in selection["selected"]:
            if sel["kind"] == "strategy" and sel["name"] == name:
                return dict(sel["params"])
        return self.strategy_params.get(name, {})

    # -------------------------------------------------------- walk-forward
    def walk_forward(self, strategy: str, space: dict[str, list[Any]]) -> dict[str, Any]:
        """Optimiza en cada ventana de entrenamiento y evalúa fuera de muestra."""
        v = self.config.validation
        grid = param_grid(space, v.max_grid_size)
        windows = walk_forward_windows(
            pd.DatetimeIndex(self.data.index),
            v.wf_train_bars,
            v.wf_test_bars,
            v.wf_step_bars,
            v.wf_anchored,
            v.embargo_bars,
        )
        cands = [self.strategy_candidate(strategy, p) for p in grid]
        rows: list[dict[str, Any]] = []
        oos_returns: list[pd.Series] = []
        oos_trades: list[pd.DataFrame] = []
        is_tables = []
        for k, (tr, te) in enumerate(windows):
            scored = []
            for gi, cand in enumerate(cands):
                m = self.metrics(self.simulate(cand, tr))
                scored.append((self._score(m), gi, m))
                is_tables.append({"window": k, **grid[gi], **{x: m.get(x) for x in KEY_METRICS}})
            best_score, best_i, best_m = max(scored, key=lambda x: (x[0], -x[1]))
            res = self.simulate(cands[best_i], te)
            m_oos = self.metrics(res)
            oos_returns.append(bar_returns(res.equity["equity"], res.initial_capital))
            oos_trades.append(res.trades.assign(window=k))
            rows.append(
                {
                    "window": k,
                    "train_start": str(tr.start),
                    "train_end": str(tr.end),
                    "test_start": str(te.start),
                    "test_end": str(te.end),
                    "params": grid[best_i],
                    "is_score": best_score,
                    "is_" + v.selection_metric: best_m.get(v.selection_metric),
                    "oos_net_profit": m_oos["net_profit"],
                    "oos_sharpe": m_oos["sharpe"],
                    "oos_trades": m_oos["num_trades"],
                    "oos_max_drawdown": m_oos["max_drawdown"],
                }
            )
        chained = pd.concat(oos_returns)
        equity = self.config.backtest.initial_capital * (1 + chained).cumprod()
        ann = bars_per_year(self.timeframe)
        std = float(chained.std(ddof=1))
        is_df = pd.DataFrame(is_tables)
        return {
            "strategy": strategy,
            "grid_size": len(grid),
            "windows": pd.DataFrame(rows),
            "oos_equity": equity,
            "oos_total_return": float(equity.iloc[-1] / self.config.backtest.initial_capital - 1),
            "oos_sharpe": float(chained.mean() / std * np.sqrt(ann)) if std > 0 else None,
            "oos_max_drawdown": float(-(equity / equity.cummax() - 1).min()),
            "oos_trades": pd.concat(oos_trades, ignore_index=True),
            "in_sample_table": is_df,
            "stability": stability_summary(is_df, v.selection_metric)
            if v.selection_metric in is_df
            else {},
        }

    def sensitivity(
        self, strategy: str, space: dict[str, list[Any]], segment: str = "train"
    ) -> tuple[pd.DataFrame, dict[str, Any]]:
        """Evalúa una rejilla en un segmento (por defecto entrenamiento)."""
        if segment == "test":
            raise ValueError("El análisis de sensibilidad no puede usar el período de test")
        grid = param_grid(space, self.config.validation.max_grid_size)
        seg = self.segments[segment]
        rows = []
        for p in grid:
            m = self.metrics(self.simulate(self.strategy_candidate(strategy, p), seg))
            rows.append({**p, **{k: m.get(k) for k in KEY_METRICS}})
        table = pd.DataFrame(rows)
        return table, stability_summary(table, self.config.validation.selection_metric)


def market_matrix(
    markets: list[Researcher],
    strategies: list[str] | None = None,
    segment: str = "validation",
) -> pd.DataFrame:
    """Métricas netas de cada estrategia en cada mercado (símbolo × temporalidad).

    Cada ``Researcher`` aplica su propia separación cronológica, de modo que el segmento
    ``validation`` de cada mercado es independiente de su período de test, que no se usa.
    """
    if segment == "test":
        raise ValueError("La matriz de mercados no puede usar el período de test")
    names = strategies or available_strategies()
    rows: list[dict[str, Any]] = []
    for r in markets:
        seg = r.segments[segment]
        for name in names:
            m = r.metrics(r.simulate(r.strategy_candidate(name), seg))
            rows.append(
                {
                    "symbol": r.symbol,
                    "timeframe": r.timeframe,
                    "candidate": name,
                    "segment": segment,
                    **{k: m.get(k) for k in KEY_METRICS},
                }
            )
        bh = r.metrics(buy_and_hold(r.data, r.config, seg, r.symbol, r.timeframe))
        rows.append(
            {
                "symbol": r.symbol,
                "timeframe": r.timeframe,
                "candidate": "benchmark_buy_and_hold",
                "segment": segment,
                **{k: bh.get(k) for k in KEY_METRICS},
            }
        )
    return pd.DataFrame(rows)


def consistency_summary(matrix: pd.DataFrame) -> pd.DataFrame:
    """Por estrategia: mercados evaluados, fracción con resultado neto positivo y dispersión.

    Un resultado positivo en un único mercado y negativo en el resto indica fragilidad.
    """
    strat = matrix[~matrix["candidate"].str.startswith("benchmark")]
    g = strat.groupby("candidate")
    return pd.DataFrame(
        {
            "markets": g.size(),
            "fraction_positive": g["net_profit_pct"].apply(lambda s: float((s > 0).mean())),
            "median_net_profit_pct": g["net_profit_pct"].median(),
            "worst_net_profit_pct": g["net_profit_pct"].min(),
            "best_net_profit_pct": g["net_profit_pct"].max(),
            "total_trades": g["num_trades"].sum(),
        }
    ).sort_values("fraction_positive", ascending=False)


def _selection_id(dhash: str, names: list[str], chash: str) -> str:
    blob = json.dumps({"d": dhash, "n": names, "c": chash}, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def save_selection(selection: dict[str, Any], path: Path) -> None:
    """Guarda la selección congelada."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(selection, indent=2, default=str), encoding="utf-8")


def load_selection(path: Path) -> dict[str, Any]:
    """Carga una selección congelada."""
    data: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    return data
