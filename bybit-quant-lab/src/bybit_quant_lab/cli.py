"""Interfaz de línea de comandos ``bql``.

Todas las órdenes son de solo lectura respecto a Bybit (datos públicos). No existe ninguna
orden que envíe operaciones a un exchange.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from bybit_quant_lab import DISCLAIMER
from bybit_quant_lab.analytics.metrics import compute_metrics
from bybit_quant_lab.backtesting.results import BacktestResult
from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.config.models import AppConfig
from bybit_quant_lab.data.bybit_client import BybitAPIError, BybitPublicClient
from bybit_quant_lab.data.downloader import download_funding, download_ohlcv, load_funding
from bybit_quant_lab.data.importers import import_ohlcv
from bybit_quant_lab.data.storage import (
    data_hash,
    dataset_path,
    load_dataset,
    load_metadata,
    save_dataset,
)
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.data.validation import validate_ohlcv
from bybit_quant_lab.logging_utils import get_logger, setup_logging
from bybit_quant_lab.reporting import (
    backtest_report,
    build_metadata,
    comparison_report,
    export_result,
    final_test_report,
    walkforward_report,
    write_json,
)
from bybit_quant_lab.signals.combiners import CombinationConfig
from bybit_quant_lab.strategies import available_strategies, create_strategy, get_strategy_class
from bybit_quant_lab.timeframes import TIMEFRAMES, validate_timeframe
from bybit_quant_lab.validation.benchmarks import buy_and_hold, cash_benchmark
from bybit_quant_lab.validation.experiment_log import (
    ExperimentLog,
    FinalTestAlreadyEvaluatedError,
)
from bybit_quant_lab.validation.research import (
    Researcher,
    load_selection,
    save_selection,
)

logger = get_logger("cli")
DEFAULT_CONFIG = Path("configs/default.yaml")
DEFAULT_STRATEGIES = Path("configs/strategies.yaml")


# --------------------------------------------------------------------------- utilidades
def _load_cfg(args: argparse.Namespace) -> AppConfig:
    path = (
        Path(args.config) if args.config else (DEFAULT_CONFIG if DEFAULT_CONFIG.exists() else None)
    )
    overrides: dict[str, Any] = {}
    if args.data_dir:
        overrides["data"] = {"data_dir": args.data_dir}
    if args.output_dir:
        overrides["output_dir"] = args.output_dir
    return load_config(path, overrides)


def _strategies_file(args: argparse.Namespace) -> dict[str, Any]:
    path = Path(args.strategies_config) if args.strategies_config else DEFAULT_STRATEGIES
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return dict(data)


def _strategy_params(args: argparse.Namespace) -> dict[str, dict[str, Any]]:
    path = Path(args.strategies_config) if args.strategies_config else DEFAULT_STRATEGIES
    return load_strategy_params(path) if path.exists() else {}


def _combos(args: argparse.Namespace) -> list[CombinationConfig]:
    raw = _strategies_file(args).get("combinations") or []
    if not raw:
        return [CombinationConfig(name="vote_all", mode="simple_vote", min_margin=3)]
    return [CombinationConfig.model_validate(c) for c in raw]


def _load_data(cfg: AppConfig, symbol: str, timeframe: str) -> tuple[pd.DataFrame, dict]:
    path = dataset_path(cfg.data.data_dir, symbol, timeframe)
    df = load_dataset(path)
    rep = validate_ohlcv(df, timeframe)
    if not rep.is_valid:
        raise SystemExit(f"Datos inválidos en {path}: {rep.issues}. Ejecuta 'bql validate-data'.")
    return df, load_metadata(path)


def _out_dir(cfg: AppConfig, explicit: str | None, *parts: str) -> Path:
    """Directorio de salida: ``--out`` si se indica, si no uno con marca temporal."""
    if explicit:
        out = Path(explicit)
    else:
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        out = Path(cfg.output_dir) / ("_".join([*parts, stamp]))
    out.mkdir(parents=True, exist_ok=True)
    return out


def _log(cfg: AppConfig) -> ExperimentLog:
    return ExperimentLog(Path(cfg.output_dir) / "experiments.jsonl")


def _ts(value: str) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")


def _print_metrics(m: dict[str, Any]) -> None:
    keys = [
        "net_profit",
        "net_profit_pct",
        "sharpe",
        "max_drawdown",
        "num_trades",
        "win_rate",
        "profit_factor",
        "expectancy",
        "total_costs",
        "total_funding",
    ]
    for k in keys:
        v = m.get(k)
        print(f"  {k:<16} {v:.4f}" if isinstance(v, float) else f"  {k:<16} {v}")
    for w in m.get("warnings", []):
        print(f"  ! {w}")


# ----------------------------------------------------------------------------- órdenes
def cmd_list(args: argparse.Namespace) -> int:
    """Lista las estrategias registradas."""
    for name in available_strategies():
        cls = get_strategy_class(name)
        print(f"{name:<22} [{cls.category.value:<9}] {cls.description}")
    return 0


def cmd_synth(args: argparse.Namespace) -> int:
    """Genera un dataset sintético (solo para probar la lógica)."""
    cfg = _load_cfg(args)
    df = generate_synthetic_ohlcv(args.bars, args.timeframe, seed=args.seed, start=args.start)
    path = dataset_path(cfg.data.data_dir, args.symbol, args.timeframe)
    save_dataset(
        df,
        path,
        {
            "source": "synthetic",
            "synthetic": True,
            "seed": args.seed,
            "symbol": args.symbol.upper(),
            "timeframe": args.timeframe,
        },
    )
    print(
        f"Dataset SINTÉTICO guardado en {path} ({len(df)} velas). No usar para evaluar "
        "rentabilidad real."
    )
    return 0


def cmd_download(args: argparse.Namespace) -> int:
    """Descarga velas (y opcionalmente funding) desde la API pública de Bybit."""
    cfg = _load_cfg(args)
    d = cfg.data
    client = BybitPublicClient(
        d.base_url,
        max_retries=d.max_retries,
        backoff_seconds=d.backoff_seconds,
        min_request_interval=d.min_request_interval,
        timeout_seconds=d.timeout_seconds,
    )
    start, end = _ts(args.start), _ts(args.end) if args.end else pd.Timestamp.now(tz="UTC")
    try:
        for tf in args.timeframe:
            s = download_ohlcv(
                client,
                args.symbol,
                tf,
                start,
                end,
                d.data_dir,
                refresh=args.refresh,
                limit=d.request_limit,
            )
            q = s.quality
            print(
                f"{args.symbol} {tf}: {s.rows} velas en {s.path} | peticiones={s.requests} "
                f"| huecos={q['gaps']} ({q['missing_bars']} velas)"
            )
        if args.funding:
            p = download_funding(client, args.symbol, start, end, d.data_dir)
            print(f"Funding guardado en {p}")
    except BybitAPIError as exc:
        print(f"Error de la API de Bybit: {exc}", file=sys.stderr)
        return 2
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    """Importa un CSV/Parquet externo."""
    cfg = _load_cfg(args)
    path, rep = import_ohlcv(
        Path(args.file), args.symbol, args.timeframe, cfg.data.data_dir, args.time_column
    )
    print(f"Importado en {path}: {rep.rows} velas; válido={rep.is_valid}; avisos={rep.issues}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Valida un dataset local."""
    cfg = _load_cfg(args)
    df = load_dataset(dataset_path(cfg.data.data_dir, args.symbol, args.timeframe))
    rep = validate_ohlcv(df, args.timeframe)
    print(json.dumps(rep.to_dict(), indent=2, default=str))
    return 0 if rep.is_valid else 1


def cmd_backtest(args: argparse.Namespace) -> int:
    """Backtest individual con informe."""
    cfg = _load_cfg(args)
    df, dmeta = _load_data(cfg, args.symbol, args.timeframe)
    params = _strategy_params(args).get(args.strategy, {})
    if args.params:
        params.update(json.loads(args.params))
    research = Researcher(
        df,
        args.symbol,
        args.timeframe,
        cfg,
        {args.strategy: params},
        load_funding(cfg.data.data_dir, args.symbol),
        _log(cfg),
    )
    cand = research.strategy_candidate(args.strategy)
    if args.segment == "full":
        seg = research.segments["train"].__class__(
            "full", 0, len(df) - 1, df.index[0], df.index[-1]
        )
    else:
        seg = research.segments[args.segment]
    res = research.simulate(cand, seg)
    gross = research.simulate(cand, seg, gross=True)
    m = compute_metrics(res, cfg.backtest.min_trades_for_stats, cfg.backtest.min_days_for_cagr)
    if args.segment == "full":
        m["warnings"].append(
            "El segmento 'full' incluye el período de test: no lo uses para "
            "seleccionar estrategias ni parámetros."
        )
    out = _out_dir(cfg, args.out, "backtest", args.symbol, args.timeframe, args.strategy)
    export_result(res, m, out)
    _save_run(res, out)
    meta = build_metadata(
        cfg,
        data_hash(df),
        dmeta,
        {
            "symbol": args.symbol,
            "timeframe": args.timeframe,
            "strategy": args.strategy,
            "segment": seg.to_dict(),
        },
    )
    write_json(meta, out / "metadata.json")
    bms = {
        "buy_and_hold": buy_and_hold(df, cfg, seg, args.symbol, args.timeframe),
        "cash": cash_benchmark(df, cfg, seg, args.symbol, args.timeframe),
    }
    report = backtest_report(
        res,
        meta,
        out / "report.html",
        bms,
        gross,
        cfg.backtest.min_trades_for_stats,
        cfg.backtest.min_days_for_cagr,
    )
    print(f"Backtest {args.strategy} {args.symbol} {args.timeframe} [{seg.name}]")
    _print_metrics(m)
    print(f"Informe: {report}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    """Compara las estrategias y combinaciones en entrenamiento y validación."""
    cfg = _load_cfg(args)
    df, dmeta = _load_data(cfg, args.symbol, args.timeframe)
    research = Researcher(
        df,
        args.symbol,
        args.timeframe,
        cfg,
        _strategy_params(args),
        load_funding(cfg.data.data_dir, args.symbol),
        _log(cfg),
    )
    names = args.strategies.split(",") if args.strategies else None
    out_obj = research.run_comparison(_combos(args), names, top_k=args.top_k)
    out = _out_dir(cfg, args.out, "compare", args.symbol, args.timeframe)
    out_obj.summary.to_csv(out / "summary.csv", index=False)
    out_obj.correlation.to_csv(out / "signal_correlation_train.csv")
    save_selection(out_obj.selection, out / "selection.json")
    write_json(out_obj.statistics, out / "statistics.json")
    meta = build_metadata(
        cfg,
        research.data_hash,
        dmeta,
        {
            "symbol": args.symbol,
            "timeframe": args.timeframe,
            "command": "compare",
            "segments": {k: v.to_dict() for k, v in research.segments.items()},
        },
    )
    write_json(meta, out / "metadata.json")
    report = comparison_report(out_obj, meta, out / "report.html")
    val = out_obj.summary[
        (out_obj.summary["segment"] == "validation") & (out_obj.summary["cost_mode"] == "net")
    ]
    cols = ["candidate", "kind", "net_profit", "sharpe", "max_drawdown", "num_trades"]
    print(val[cols].to_string(index=False, float_format=lambda x: f"{x:,.3f}"))
    print(f"\nSeleccionados en validación: {[s['name'] for s in out_obj.selection['selected']]}")
    print(f"Selección congelada: {out / 'selection.json'}")
    print(f"Informe: {report}")
    return 0


def cmd_final_test(args: argparse.Namespace) -> int:
    """Evalúa una selección congelada en el período de test (una sola vez)."""
    cfg = _load_cfg(args)
    selection = load_selection(Path(args.selection))
    symbol, tf = selection["symbol"], selection["timeframe"]
    df, dmeta = _load_data(cfg, symbol, tf)
    research = Researcher(
        df,
        symbol,
        tf,
        cfg,
        _strategy_params(args),
        load_funding(cfg.data.data_dir, symbol),
        _log(cfg),
    )
    try:
        ft = research.run_final_test(selection, _combos(args), allow_repeat=args.allow_repeat)
    except FinalTestAlreadyEvaluatedError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    out = _out_dir(cfg, args.out, "final_test", symbol, tf)
    meta = build_metadata(
        cfg,
        research.data_hash,
        dmeta,
        {
            "symbol": symbol,
            "timeframe": tf,
            "command": "final-test",
            "selection_id": selection["selection_id"],
            "repeated": ft["repeated"],
        },
    )
    write_json(meta, out / "metadata.json")
    for name, r in ft["candidates"].items():
        m = compute_metrics(
            r["net"], cfg.backtest.min_trades_for_stats, cfg.backtest.min_days_for_cagr
        )
        export_result(r["net"], m, out, prefix=f"{name}_")
        print(f"{name} (test, neto):")
        _print_metrics(m)
    report = final_test_report(
        ft,
        meta,
        out / "report.html",
        cfg.backtest.min_trades_for_stats,
        cfg.backtest.min_days_for_cagr,
    )
    print(f"Informe: {report}")
    return 0


def _grid(args: argparse.Namespace, strategy: str) -> dict[str, list[Any]]:
    if args.grid:
        return dict(json.loads(args.grid))
    grids = _strategies_file(args).get("grids") or {}
    if strategy not in grids:
        raise SystemExit(f"No hay rejilla para {strategy}; usa --grid '{{\"param\": [..]}}'")
    return dict(grids[strategy])


def cmd_walkforward(args: argparse.Namespace) -> int:
    """Walk-forward con optimización acotada por ventana."""
    cfg = _load_cfg(args)
    df, dmeta = _load_data(cfg, args.symbol, args.timeframe)
    research = Researcher(
        df,
        args.symbol,
        args.timeframe,
        cfg,
        _strategy_params(args),
        load_funding(cfg.data.data_dir, args.symbol),
        _log(cfg),
    )
    wf = research.walk_forward(args.strategy, _grid(args, args.strategy))
    out = _out_dir(cfg, args.out, "walkforward", args.symbol, args.timeframe, args.strategy)
    wf["windows"].to_csv(out / "windows.csv", index=False)
    wf["in_sample_table"].to_csv(out / "in_sample_grid.csv", index=False)
    wf["oos_trades"].to_csv(out / "oos_trades.csv", index=False)
    wf["oos_equity"].to_csv(out / "oos_equity.csv")
    write_json(
        {
            k: wf[k]
            for k in (
                "strategy",
                "grid_size",
                "oos_total_return",
                "oos_sharpe",
                "oos_max_drawdown",
                "stability",
            )
        },
        out / "summary.json",
    )
    meta = build_metadata(
        cfg,
        research.data_hash,
        dmeta,
        {
            "symbol": args.symbol,
            "timeframe": args.timeframe,
            "command": "walkforward",
            "strategy": args.strategy,
        },
    )
    write_json(meta, out / "metadata.json")
    report = walkforward_report(wf, meta, out / "report.html")
    print(wf["windows"].to_string(index=False))
    print(
        f"OOS: retorno={wf['oos_total_return']:.4f} sharpe={wf['oos_sharpe']} "
        f"maxDD={wf['oos_max_drawdown']:.4f}"
    )
    print(f"Informe: {report}")
    return 0


def cmd_sensitivity(args: argparse.Namespace) -> int:
    """Sensibilidad de parámetros en entrenamiento o validación."""
    cfg = _load_cfg(args)
    df, _ = _load_data(cfg, args.symbol, args.timeframe)
    research = Researcher(
        df,
        args.symbol,
        args.timeframe,
        cfg,
        _strategy_params(args),
        load_funding(cfg.data.data_dir, args.symbol),
        _log(cfg),
    )
    table, summary = research.sensitivity(args.strategy, _grid(args, args.strategy), args.segment)
    out = _out_dir(cfg, args.out, "sensitivity", args.symbol, args.timeframe, args.strategy)
    table.to_csv(out / "grid.csv", index=False)
    write_json(summary, out / "stability.json")
    print(table.to_string(index=False, float_format=lambda x: f"{x:,.3f}"))
    print(json.dumps(summary, indent=2))
    print(f"Resultados: {out}")
    return 0


def _save_run(res: BacktestResult, out: Path) -> None:
    write_json(
        {
            "label": res.label,
            "symbol": res.symbol,
            "timeframe": res.timeframe,
            "initial_capital": res.initial_capital,
            "totals": res.totals,
            "funding_applied": res.funding_applied,
            "warnings": res.warnings,
            "params": res.params,
            "risk_events": res.risk_events,
            "rejected_signals": res.rejected_signals,
        },
        out / "run.json",
    )


def load_run(run_dir: Path) -> BacktestResult:
    """Reconstruye un ``BacktestResult`` desde los archivos exportados de un backtest."""
    run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    equity = pd.read_csv(run_dir / "equity.csv", index_col=0, parse_dates=True)
    trades = pd.read_csv(run_dir / "trades.csv")
    return BacktestResult(
        label=run["label"],
        symbol=run["symbol"],
        timeframe=run["timeframe"],
        initial_capital=run["initial_capital"],
        equity=equity,
        trades=trades,
        risk_events=run["risk_events"],
        rejected_signals=run["rejected_signals"],
        totals=run["totals"],
        funding_applied=run["funding_applied"],
        warnings=run["warnings"],
        params=run["params"],
    )


def cmd_report(args: argparse.Namespace) -> int:
    """Regenera el informe HTML de un backtest desde sus archivos exportados."""
    run_dir = Path(args.run_dir)
    res = load_run(run_dir)
    meta = json.loads((run_dir / "metadata.json").read_text(encoding="utf-8"))
    cfg = AppConfig.model_validate(meta["config"])
    path = backtest_report(
        res,
        meta,
        run_dir / "report.html",
        None,
        None,
        cfg.backtest.min_trades_for_stats,
        cfg.backtest.min_days_for_cagr,
    )
    print(f"Informe regenerado: {path}")
    return 0


# ------------------------------------------------------------------------------ parser
def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de argumentos."""
    p = argparse.ArgumentParser(
        prog="bql",
        description="bybit-quant-lab: investigación y "
        "backtesting de perpetuos lineales de Bybit (sin trading real).",
    )
    p.add_argument("--config", help="YAML de configuración (por defecto configs/default.yaml)")
    p.add_argument("--strategies-config", help="YAML de estrategias (configs/strategies.yaml)")
    p.add_argument("--data-dir", help="Directorio de datos (sobrescribe la configuración)")
    p.add_argument("--output-dir", help="Directorio de resultados")
    p.add_argument("--log-level", default=None)
    sub = p.add_subparsers(dest="command", required=True)
    tfs = list(TIMEFRAMES)

    def sym(sp: argparse.ArgumentParser, multi_tf: bool = False) -> None:
        sp.add_argument("--symbol", required=True, type=str.upper)
        if multi_tf:
            sp.add_argument("--timeframe", required=True, nargs="+", choices=tfs)
        else:
            sp.add_argument("--timeframe", required=True, choices=tfs)

    sp = sub.add_parser("list-strategies", help="Lista las estrategias registradas")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("synth", help="Genera datos sintéticos (solo pruebas de lógica)")
    sym(sp)
    sp.add_argument("--bars", type=int, default=6000)
    sp.add_argument("--seed", type=int, default=42)
    sp.add_argument("--start", default="2023-01-01")
    sp.set_defaults(func=cmd_synth)

    sp = sub.add_parser("download", help="Descarga OHLCV (y funding) de la API pública")
    sym(sp, multi_tf=True)
    sp.add_argument("--start", required=True, help="Fecha UTC, p. ej. 2024-01-01")
    sp.add_argument("--end", help="Fecha UTC final (por defecto, ahora)")
    sp.add_argument("--funding", action="store_true", help="Descargar también el funding")
    sp.add_argument("--refresh", action="store_true", help="Ignorar datos locales")
    sp.set_defaults(func=cmd_download)

    sp = sub.add_parser("import", help="Importa OHLCV desde CSV o Parquet")
    sym(sp)
    sp.add_argument("--file", required=True)
    sp.add_argument("--time-column")
    sp.set_defaults(func=cmd_import)

    sp = sub.add_parser("validate-data", help="Valida un dataset local")
    sym(sp)
    sp.set_defaults(func=cmd_validate)

    sp = sub.add_parser("backtest", help="Backtest de una estrategia con informe")
    sym(sp)
    sp.add_argument("--strategy", required=True, choices=available_strategies())
    sp.add_argument("--params", help="JSON con parámetros que sobrescriben el YAML")
    sp.add_argument("--segment", default="train", choices=["train", "validation", "full"])
    sp.add_argument("--out")
    sp.set_defaults(func=cmd_backtest)

    sp = sub.add_parser("compare", help="Compara estrategias y combinaciones (train/validación)")
    sym(sp)
    sp.add_argument("--strategies", help="Lista separada por comas (por defecto, las diez)")
    sp.add_argument("--top-k", type=int, default=3)
    sp.add_argument("--out")
    sp.set_defaults(func=cmd_compare)

    sp = sub.add_parser("final-test", help="Evalúa una selección congelada en test (una vez)")
    sp.add_argument("--selection", required=True)
    sp.add_argument("--allow-repeat", action="store_true")
    sp.add_argument("--out")
    sp.set_defaults(func=cmd_final_test)

    sp = sub.add_parser("walkforward", help="Walk-forward con optimización por ventana")
    sym(sp)
    sp.add_argument("--strategy", required=True, choices=available_strategies())
    sp.add_argument("--grid", help="JSON {param: [valores]} (por defecto, de strategies.yaml)")
    sp.add_argument("--out")
    sp.set_defaults(func=cmd_walkforward)

    sp = sub.add_parser("sensitivity", help="Sensibilidad de parámetros (train o validación)")
    sym(sp)
    sp.add_argument("--strategy", required=True, choices=available_strategies())
    sp.add_argument("--grid")
    sp.add_argument("--segment", default="train", choices=["train", "validation"])
    sp.add_argument("--out")
    sp.set_defaults(func=cmd_sensitivity)

    sp = sub.add_parser("report", help="Regenera el HTML de un backtest exportado")
    sp.add_argument("--run-dir", required=True)
    sp.set_defaults(func=cmd_report)
    return p


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada."""
    args = build_parser().parse_args(argv)
    setup_logging(args.log_level)
    if args.command != "list-strategies":
        print(DISCLAIMER, file=sys.stderr)
    if hasattr(args, "timeframe") and isinstance(args.timeframe, str):
        validate_timeframe(args.timeframe)
    if hasattr(args, "strategy") and args.strategy:
        create_strategy(args.strategy)  # valida que exista
    try:
        return int(args.func(args))
    except (FileNotFoundError, ValueError, KeyError) as exc:
        # Errores esperables de uso (datos ausentes, parámetros inválidos): mensaje sin traza.
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
