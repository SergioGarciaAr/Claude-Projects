"""Informes HTML reproducibles (backtest individual, comparación, walk-forward y test final)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from typing import Any

import pandas as pd
from jinja2 import Environment, select_autoescape

from bybit_quant_lab import DISCLAIMER
from bybit_quant_lab.analytics.breakdowns import breakdown_trades
from bybit_quant_lab.analytics.metrics import compute_metrics
from bybit_quant_lab.backtesting.results import BacktestResult
from bybit_quant_lab.reporting import charts
from bybit_quant_lab.reporting.export import to_jsonable

MAX_TRADE_ROWS = 500


@dataclass
class Section:
    """Sección del informe."""

    title: str
    text: str = ""
    images: list[dict[str, str]] = field(default_factory=list)
    tables: list[dict[str, str]] = field(default_factory=list)
    pre: str = ""

    def table(self, df: pd.DataFrame, caption: str = "", index: bool = True) -> Section:
        """Añade una tabla formateada."""
        html = df.to_html(
            index=index, float_format=lambda x: f"{x:,.4g}", na_rep="—", border=0, escape=True
        )
        self.tables.append({"html": html, "caption": caption})
        return self

    def image(self, data: str, alt: str) -> Section:
        """Añade un gráfico PNG en base64."""
        self.images.append({"data": data, "alt": alt})
        return self


def render(
    title: str,
    subtitle: str,
    sections: list[Section],
    metadata: dict[str, Any],
    warnings: list[str],
    path: Path,
) -> Path:
    """Renderiza el HTML final."""
    env = Environment(autoescape=select_autoescape(["html"]))
    template_text = (
        resources.files("bybit_quant_lab.reporting") / "templates" / "report.html"
    ).read_text(encoding="utf-8")
    html = env.from_string(template_text).render(
        title=title,
        subtitle=subtitle,
        sections=sections,
        disclaimer=DISCLAIMER,
        warnings=sorted(set(warnings)),
        metadata_json=json.dumps(to_jsonable(metadata), indent=2, ensure_ascii=False),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path


def _metrics_table(m: dict[str, Any]) -> pd.DataFrame:
    rows = {k: v for k, v in m.items() if k != "warnings" and not isinstance(v, list | dict)}
    return pd.DataFrame({"valor": pd.Series(rows, dtype=object)})


def executive_summary(m: dict[str, Any], benchmarks: dict[str, dict[str, Any]]) -> str:
    """Resumen ejecutivo factual (sin juicios de rentabilidad futura)."""

    def pct(x: float | None) -> str:
        return "n/d" if x is None else f"{x * 100:.2f} %"

    def num(x: float | None) -> str:
        return "n/d" if x is None else f"{x:.2f}"

    parts = [
        f"Resultado neto {m['net_profit']:,.2f} ({pct(m['net_profit_pct'])}) con "
        f"{m['num_trades']} operaciones entre {m['start']} y {m['end']}.",
        f"Drawdown máximo {pct(m['max_drawdown'])}; Sharpe {num(m['sharpe'])}; "
        f"profit factor {num(m['profit_factor'])}; costes {m['total_costs']:,.2f}; "
        f"funding {m['total_funding']:,.2f} "
        f"({'aplicado' if m['funding_applied'] else 'no aplicado'}).",
    ]
    for name, bm in benchmarks.items():
        parts.append(f"Referencia {name}: {pct(bm['net_profit_pct'])}.")
    if m["num_trades"] < 30:
        parts.append("Muestra pequeña: los resultados no son estadísticamente concluyentes.")
    return " ".join(parts)


def backtest_report(
    result: BacktestResult,
    metadata: dict[str, Any],
    path: Path,
    benchmarks: dict[str, BacktestResult] | None = None,
    gross: BacktestResult | None = None,
    min_trades: int = 30,
    min_days_for_cagr: int = 180,
) -> Path:
    """Informe de un backtest individual."""
    m = compute_metrics(result, min_trades, min_days_for_cagr)
    bms = {
        k: compute_metrics(v, min_trades, min_days_for_cagr) for k, v in (benchmarks or {}).items()
    }
    secs: list[Section] = [Section("Resumen ejecutivo", text=executive_summary(m, bms))]
    secs.append(
        Section("Parámetros").table(pd.DataFrame({"valor": pd.Series(result.params, dtype=object)}))
    )
    cmp_rows = {"estrategia (neto)": m}
    if gross is not None:
        cmp_rows["estrategia (bruto, sin costes)"] = compute_metrics(
            gross, min_trades, min_days_for_cagr
        )
    cmp_rows.update({f"benchmark {k}": v for k, v in bms.items()})
    keys = [
        "net_profit",
        "net_profit_pct",
        "sharpe",
        "sortino",
        "max_drawdown",
        "cagr",
        "num_trades",
        "win_rate",
        "profit_factor",
        "expectancy",
        "total_costs",
        "total_funding",
        "exposure",
    ]
    secs.append(
        Section("Métricas de rendimiento y riesgo")
        .table(_metrics_table(m))
        .table(
            pd.DataFrame({k: {x: v.get(x) for x in keys} for k, v in cmp_rows.items()}).T,
            "Neto frente a bruto y benchmarks",
        )
    )
    curves = {"estrategia": result.equity["equity"]}
    for k, v in (benchmarks or {}).items():
        curves[k] = v.equity["equity"]
    secs.append(
        Section("Curva de equity y drawdown")
        .image(charts.line_chart(curves, "Equity", "USDT"), "Curva de equity")
        .image(charts.drawdown_chart(result.equity["drawdown"]), "Drawdown")
    )
    t = result.trades
    dist = Section("Distribución de retornos")
    if len(t):
        dist.image(
            charts.histogram(
                t["return_on_equity"].astype(float) * 100,
                "Retorno neto por operación",
                "% de equity",
            ),
            "Histograma de retornos por operación",
        )
    secs.append(dist)
    costs = pd.DataFrame(
        {
            "valor": {
                "comisiones": result.totals["fees"],
                "slippage": result.totals["slippage"],
                "funding": result.totals["funding"],
                "funding_aplicado": result.funding_applied,
            }
        }
    )
    secs.append(Section("Costes y funding").table(costs))
    br = Section("Desgloses")
    for col, label in (
        ("side", "Por dirección"),
        ("exit_reason", "Por motivo de salida"),
        ("regime", "Por régimen al entrar"),
    ):
        br.table(breakdown_trades(t, col), label)
    secs.append(br)
    risk = Section("Eventos de riesgo y señales rechazadas")
    if result.risk_events:
        risk.table(pd.DataFrame(result.risk_events), index=False)
    if result.rejected_signals:
        risk.table(
            pd.DataFrame(result.rejected_signals)["reason"].value_counts().to_frame(),
            "Señales rechazadas por motivo",
        )
    secs.append(risk)
    secs.append(
        Section(
            "Tabla de operaciones",
            text=f"Se muestran hasta {MAX_TRADE_ROWS} operaciones; el CSV contiene todas.",
        ).table(t.head(MAX_TRADE_ROWS), index=False)
    )
    warnings = list(m["warnings"])
    if metadata.get("data_synthetic"):
        warnings.append("Datos SINTÉTICOS: sirven para validar la lógica, no la rentabilidad.")
    return render(
        f"Backtest {result.label} — {result.symbol} {result.timeframe}",
        f"{m['start']} → {m['end']}",
        secs,
        metadata,
        warnings,
        path,
    )


def comparison_report(out: Any, metadata: dict[str, Any], path: Path) -> Path:
    """Informe de comparación (``ComparisonOutput``) en entrenamiento y validación."""
    s = out.summary
    secs = [
        Section(
            "Resumen ejecutivo",
            text=(
                "Comparación de estrategias individuales, combinaciones y benchmarks en "
                "entrenamiento y validación. El período de test NO se ha usado. La selección "
                "se basó solo en validación y quedó congelada en selection.json."
            ),
        ).table(
            pd.DataFrame({k: v.to_dict() for k, v in out.segments.items()}).T,
            "Segmentos cronológicos",
        )
    ]
    for seg in ("train", "validation"):
        sub = s[(s["segment"] == seg)]
        net = sub[sub["cost_mode"] == "net"].set_index("candidate")
        sec = Section(f"Resultados — {seg}")
        sec.table(net.drop(columns=["segment", "cost_mode"]), "Netos de costes")
        gross = sub[sub["cost_mode"] == "gross"].set_index("candidate")["net_profit"]
        if len(gross):
            sec.table(
                pd.DataFrame(
                    {
                        "bruto": gross,
                        "neto": net["net_profit"].reindex(gross.index),
                        "costes": net["total_costs"].reindex(gross.index),
                    }
                ),
                "Bruto frente a neto",
            )
        sec.image(
            charts.bar_chart(net["net_profit"], f"Beneficio neto ({seg})", "USDT"),
            f"Beneficio neto por candidato en {seg}",
        )
        secs.append(sec)
    top = [x["name"] for x in out.selection["selected"]][:2]
    curves = {n: out.results[(n, "validation", "net")].equity["equity"] for n in top}
    curves["buy_and_hold"] = out.results[("benchmark_buy_and_hold", "validation", "net")].equity[
        "equity"
    ]
    secs.append(
        Section("Equity en validación (seleccionados y buy-and-hold)").image(
            charts.line_chart(curves, "Equity en validación", "USDT"), "Equity en validación"
        )
    )
    secs.append(
        Section(
            "Redundancia entre señales (entrenamiento)",
            text="Correlación de Pearson y coincidencia direccional de los estados "
            "-1/0/1. Alta correlación = información redundante.",
        )
        .table(out.correlation.round(2), "Correlación")
        .table(out.agreement.round(2), "Coincidencia cuando ambas están activas")
        .table(
            pd.DataFrame({"valor": pd.Series(out.redundancy, dtype=object)}),
            "Decisiones de combinación ajustadas en entrenamiento/validación",
        )
    )
    st = out.statistics
    holm = pd.DataFrame(st["holm_validation"]).T
    secs.append(
        Section(
            "Selección y validación estadística",
            text=f"Configuraciones distintas evaluadas en validación con estos "
            f"datos: {st['n_trials_logged']}. El DSR deflacta el Sharpe por ese "
            "número de pruebas.",
        )
        .table(
            pd.DataFrame(out.selection["selected"]).drop(columns=["params"]),
            "Candidatos seleccionados (validación)",
            index=False,
        )
        .table(holm, "p-valores de la expectativa por operación con ajuste de Holm")
        .table(
            pd.json_normalize([{"candidate": k, **v} for k, v in st["selected_details"].items()])
            .set_index("candidate")
            .T,
            "DSR, intervalo bootstrap y dependencia de las mejores operaciones",
        )
    )
    warnings = [
        "Combinar estrategias no garantiza mejorar resultados; compare con las "
        "individuales y los benchmarks.",
        "Un Sharpe alto en validación con DSR bajo indica probable selección por azar.",
    ]
    if metadata.get("data_synthetic"):
        warnings.append("Datos SINTÉTICOS: sirven para validar la lógica, no la rentabilidad.")
    return render(
        "Comparación de estrategias",
        f"{metadata.get('symbol')} {metadata.get('timeframe')}",
        secs,
        metadata,
        warnings,
        path,
    )


def final_test_report(
    ft: dict[str, Any],
    metadata: dict[str, Any],
    path: Path,
    min_trades: int = 30,
    min_days: int = 180,
) -> Path:
    """Informe del test final sobre la selección congelada."""
    rows: dict[str, dict[str, Any]] = {}
    curves: dict[str, pd.Series] = {}
    for name, r in ft["candidates"].items():
        rows[f"{name} (neto)"] = compute_metrics(r["net"], min_trades, min_days)
        rows[f"{name} (bruto)"] = compute_metrics(r["gross"], min_trades, min_days)
        if len(curves) < 2:
            curves[name] = r["net"].equity["equity"]
    for name, r in ft["benchmarks"].items():
        rows[f"benchmark {name}"] = compute_metrics(r, min_trades, min_days)
    curves["buy_and_hold"] = ft["benchmarks"]["buy_and_hold"].equity["equity"]
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
    secs = [
        Section(
            "Resumen ejecutivo",
            text="Evaluación única de la selección congelada en el período de test. "
            "Estos resultados no se han usado para ajustar nada.",
        ).table(pd.DataFrame({k: {x: v.get(x) for x in keys} for k, v in rows.items()}).T),
        Section("Equity en test").image(
            charts.line_chart(curves, "Equity en test", "USDT"), "Equity en test"
        ),
    ]
    warnings = [w for v in rows.values() for w in v["warnings"]]
    if ft.get("repeated"):
        warnings.append(
            "ATENCIÓN: esta selección ya se había evaluado en test; el resultado "
            "ya no es una evaluación independiente."
        )
    if metadata.get("data_synthetic"):
        warnings.append("Datos SINTÉTICOS: sirven para validar la lógica, no la rentabilidad.")
    return render(
        "Test final (fuera de muestra)", str(ft["segment"]), secs, metadata, warnings, path
    )


def walkforward_report(wf: dict[str, Any], metadata: dict[str, Any], path: Path) -> Path:
    """Informe walk-forward."""
    sharpe = "n/d" if wf["oos_sharpe"] is None else f"{wf['oos_sharpe']:.2f}"
    secs = [
        Section(
            "Resumen ejecutivo",
            text=(
                f"Estrategia {wf['strategy']}: rejilla de {wf['grid_size']} "
                "configuraciones optimizada en cada ventana de entrenamiento y evaluada "
                "en la ventana siguiente. Retorno OOS encadenado "
                f"{wf['oos_total_return'] * 100:.2f} %, Sharpe OOS {sharpe}, "
                f"drawdown máximo OOS {wf['oos_max_drawdown'] * 100:.2f} %."
            ),
        ),
        Section("Ventanas").table(wf["windows"], index=False),
        Section("Equity fuera de muestra").image(
            charts.line_chart({"OOS": wf["oos_equity"]}, "Equity OOS encadenada", "USDT"),
            "Equity OOS",
        ),
        Section("Estabilidad de la rejilla (in-sample)").table(
            pd.DataFrame({"valor": pd.Series(wf["stability"], dtype=object)})
        ),
    ]
    warnings = [
        "La equity OOS encadena retornos de ventanas independientes que empiezan sin posición."
    ]
    if metadata.get("data_synthetic"):
        warnings.append("Datos SINTÉTICOS: sirven para validar la lógica, no la rentabilidad.")
    return render(
        "Walk-forward",
        f"{metadata.get('symbol')} {metadata.get('timeframe')}",
        secs,
        metadata,
        warnings,
        path,
    )
