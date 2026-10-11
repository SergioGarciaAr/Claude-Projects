# Módulo XIII. Validación, walk-forward y control del sobreajuste

Un backtest siempre se puede mejorar mirando el resultado y cambiando algo. El problema es que
cada cambio "aprende" el ruido de los datos que se miran. Este módulo explica cómo el proyecto
separa los datos, qué decide con cada parte, qué estadísticos usa para medir la suerte y qué
errores de este tipo encontró y corrigió la auditoría.

Código: `src/bybit_quant_lab/validation/` (`splits.py`, `research.py`, `overfitting.py`,
`benchmarks.py`, `sensitivity.py`, `experiment_log.py`). Conceptos estadísticos de base: Módulo
VI (secciones 6.7–6.13).

> **[Hecho]** Los ejemplos usan datos sintéticos. Sirven para ver **cómo** se comportan los
> controles, no para concluir nada sobre ninguna estrategia en Bybit.

---

## 13.1 Sobreajuste: la intuición

**Analogía.** Un estudiante que memoriza las respuestas de los exámenes de años anteriores
saca un 10 en ellos, pero no ha aprendido la materia. El examen que importa es uno que **nunca
ha visto**. En el código, ese examen es el segmento de **test**, y la regla que lo protege es
`guard_final_test` (sección 13.11).

**Sobreajuste (overfitting):** ajustar reglas o parámetros hasta que describen el ruido
particular de una muestra, no un patrón que se repita. Síntoma típico: un resultado excelente en
los datos usados para elegir y mediocre o negativo en datos nuevos.

**Fuga de información (leakage):** que una decisión use, aunque sea indirectamente, datos que
no debería conocer en ese momento. Puede ser temporal (usar el futuro) o de protocolo (mirar el
test y luego "solo" ajustar un parámetro).

---

## 13.2 Tres segmentos cronológicos

<!-- cita: src/bybit_quant_lab/validation/splits.py#L48-L61 -->
`src/bybit_quant_lab/validation/splits.py` · líneas 48–61

```python
def chronological_split(
    index: pd.DatetimeIndex, train_frac: float, validation_frac: float, embargo_bars: int = 0
) -> dict[str, Segment]:
    """Divide ``index`` en ``train``, ``validation`` y ``test`` (resto), en ese orden."""
    n = len(index)
    if not 0 < train_frac < 1 or not 0 < validation_frac < 1 or train_frac + validation_frac >= 1:
        raise ValueError("Fracciones inválidas: se requiere train + validation < 1")
    n_train = int(n * train_frac)
    n_val = int(n * validation_frac)
    tr = _segment(index, "train", 0, n_train - 1)
    va = _segment(index, "validation", n_train + embargo_bars, n_train + n_val - 1)
    te = _segment(index, "test", n_train + n_val + embargo_bars, n - 1)
    assert tr.end < va.start < va.end < te.start, "segmentos no ordenados"
    return {"train": tr, "validation": va, "test": te}
```

Con 6000 velas y las fracciones por defecto (60 % / 20 %):

```text
n_train = int(6000 × 0,6) = 3600  → velas 0..3599
n_val   = int(6000 × 0,2) = 1200  → velas 3600..4799
test    = resto           = 1200  → velas 4800..5999
```

- **[Diseño] Cronológico, no aleatorio.** Mezclar velas al azar pondría datos del futuro en el
  entrenamiento. En series temporales, el orden es la información.
- **Embargo** (`embargo_bars`, 0 por defecto): velas que se dejan sin usar al principio de
  validación y de test. Reduce la dependencia entre el final de un segmento y el principio del
  siguiente (por ejemplo, una posición o un indicador que "cruza" la frontera). Con embargo,
  validación y test **pierden** velas; no se desplazan.
- **Línea 60:** una aserción garantiza el orden y la ausencia de solapamiento
  (`test_chronological_split_is_ordered_and_disjoint`).
- **[Diseño]** Las señales se calculan **una vez** sobre toda la serie y luego cada segmento se
  simula por separado, empezando sin posición (cabecera, líneas 5–7). Es correcto solo porque
  los indicadores son causales (Módulo VII): la señal de la vela 4000 no cambia por existir la
  vela 5000.

---

## 13.3 El protocolo: qué se decide con cada segmento

<!-- cita: src/bybit_quant_lab/validation/research.py#L1-L12 -->
`src/bybit_quant_lab/validation/research.py` · líneas 1–12

```python
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
```

| Segmento | Se usa para | No se usa para |
|---|---|---|
| Entrenamiento | Redundancia, pesos y umbral de `weighted_vote`; sensibilidad (por defecto) | Seleccionar candidatos |
| Validación | **Seleccionar** los mejores candidatos (`top_k`) | Ajustar parámetros |
| Test | Evaluar **una vez** la selección congelada | Cualquier decisión |

**[Discrepancia]** El punto 2 de la cabecera dice que los umbrales se eligen "solo con
validación". El código los elige con entrenamiento desde la corrección M-01 (Módulo IX,
sección 9.6). Manda el código.

**Por qué no basta con dos segmentos.** Si se seleccionara con el test, el resultado del test
sería el máximo de varios resultados ruidosos, sesgado al alza (sesgo de selección, sección
6.11). La validación absorbe ese sesgo; el test queda limpio.

---

## 13.4 Comparación y selección

`run_comparison` (`research.py`, líneas 244–299) simula cada candidato (diez estrategias y las
combinaciones) en entrenamiento y validación, **con y sin costes**, añade tres benchmarks y
calcula la redundancia en entrenamiento. Después selecciona:

<!-- cita: src/bybit_quant_lab/validation/research.py#L188-L193 -->
`src/bybit_quant_lab/validation/research.py` · líneas 188–193

```python
    def _score(self, m: dict[str, Any]) -> float:
        v = self.config.validation
        if (m.get("num_trades") or 0) < v.min_trades_selection:
            return float("-inf")
        val = m.get(v.selection_metric)
        return float(val) if val is not None and np.isfinite(val) else float("-inf")
```

<!-- cita: src/bybit_quant_lab/validation/research.py#L313-L379 -->
`src/bybit_quant_lab/validation/research.py` · líneas 313–379

```python
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
            # Parámetros de TODAS las estrategias individuales en el momento de la selección:
            # el test final reconstruye las combinaciones con ellos, no con el YAML vigente.
            "strategy_params": {n: c.params for n, c in cands.items() if c.kind == "strategy"},
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
```

- **316–320:** solo filas de **validación**, **netas**, de estrategias y combinaciones.
- **188–193 (`_score`):** la métrica de selección (`sharpe` por defecto); `−∞` si hay menos de
  `min_trades_selection` (10) operaciones o la métrica no existe.
- **325:** se toman los `top_k` mejores con puntuación finita.
- **326:** `n_trials` = configuraciones distintas evaluadas en validación con **estos datos**,
  contadas en el registro de experimentos de **todas** las ejecuciones (sección 13.11).
- **333–339:** p-valor de la expectativa por operación de cada candidato y ajuste de Holm.
- **341–354:** para los elegidos: DSR, intervalo bootstrap y dependencia de las mejores
  operaciones.
- **356–378:** la selección congelada: identificador, hashes de datos y configuración,
  parámetros de **todas** las estrategias (corrección A-03), segmentos y elegidos.

**[Hecho] El selector no filtra por los controles estadísticos.** Elige por la métrica de
validación con un mínimo de operaciones. DSR, Holm y la dependencia de pocas operaciones se
**informan**, pero no bloquean (`docs/audit_report.md`, sección 4). Revisarlos es tarea de
quien lee el informe.

---

## 13.5 Un ciclo completo: comparación, selección y test final

Configuración por defecto, 6000 velas sintéticas, semilla 42, parámetros y combinaciones del
YAML, registro de experimentos en un directorio temporal:

<!-- ejecutar -->
```python
import tempfile
from pathlib import Path

import yaml

from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import CombinationConfig
from bybit_quant_lab.validation.experiment_log import (
    ExperimentLog,
    FinalTestAlreadyEvaluatedError,
)
from bybit_quant_lab.validation.research import Researcher

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
params = load_strategy_params("configs/strategies.yaml")
combos = [
    CombinationConfig.model_validate(c)
    for c in yaml.safe_load(open("configs/strategies.yaml"))["combinations"]
]
with tempfile.TemporaryDirectory() as tmp:
    log = ExperimentLog(Path(tmp) / "experiments.jsonl")
    r = Researcher(datos, "BTCUSDT", "1h", load_config(), strategy_params=params, log=log)
    out = r.run_comparison(combos, top_k=3)
    st = out.statistics
    print("configuraciones evaluadas en validación:", st["n_trials_logged"])
    print("\nSELECCIÓN (validación, neto):")
    for s in out.selection["selected"]:
        d = st["selected_details"][s["name"]]
        ds, top = d["deflated_sharpe"], d["top_trade_dependence"]
        ic = d["bootstrap_ci_trade_pnl"]
        print(f"  {s['name']:14s} Sharpe={s['validation_score']:.2f} "
              f"DSR={ds['dsr']:.2f} PSR(0)={ds['psr_vs_zero']:.2f} "
              f"IC95 media/op=[{ic[0]:.1f}, {ic[1]:.1f}] "
              f"cambia de signo sin top-3={top['sign_flips_without_top_k']}")
    print("SR0 por vela (máximo esperado por azar):",
          round(next(iter(st["selected_details"].values()))["deflated_sharpe"]
                ["expected_max_sharpe_null"], 4))
    holm = st["holm_validation"]
    print("Holm rechaza H0 en:", [k for k, v in holm.items() if v["reject"]])
    mejor = min((v["p"], k) for k, v in holm.items() if v["p"] is not None)
    print(f"menor p: {mejor[1]} p={mejor[0]:.3f} p_ajustado={holm[mejor[1]]['p_adj']:.3f}")

    ft = r.run_final_test(out.selection, combos)
    s = out.summary
    print("\nVALIDACIÓN -> TEST (neto):")
    for nombre, res in ft["candidates"].items():
        v = s[(s.candidate == nombre) & (s.segment == "validation") & (s.cost_mode == "net")]
        mt = r.metrics(res["net"])
        print(f"  {nombre:14s} Sharpe {v['sharpe'].iloc[0]:6.2f} -> {mt['sharpe']:6.2f}   "
              f"retorno {v['net_profit_pct'].iloc[0]:6.2%} -> {mt['net_profit_pct']:6.2%}")
    bh = r.metrics(ft["benchmarks"]["buy_and_hold"])
    print(f"  comprar y mantener en test: {bh['net_profit_pct']:.2%}")
    try:
        r.run_final_test(out.selection, combos)
    except FinalTestAlreadyEvaluatedError as e:
        print("\nsegundo test final:", type(e).__name__)
```
<!-- salida -->
```text
configuraciones evaluadas en validación: 16

SELECCIÓN (validación, neto):
  stoch_rsi      Sharpe=5.62 DSR=0.80 PSR(0)=0.98 IC95 media/op=[-1.8, 43.2] cambia de signo sin top-3=False
  obv_trend      Sharpe=2.62 DSR=0.39 PSR(0)=0.83 IC95 media/op=[-13.9, 36.7] cambia de signo sin top-3=True
  regime_switch  Sharpe=1.61 DSR=0.26 PSR(0)=0.72 IC95 media/op=[-13.4, 23.7] cambia de signo sin top-3=True
SR0 por vela (máximo esperado por azar): 0.0357
Holm rechaza H0 en: []
menor p: stoch_rsi p=0.030 p_ajustado=0.479

VALIDACIÓN -> TEST (neto):
  stoch_rsi      Sharpe   5.62 ->  -2.93   retorno 14.49% -> -6.62%
  obv_trend      Sharpe   2.62 ->  -6.40   retorno  3.53% -> -7.32%
  regime_switch  Sharpe   1.61 ->   1.16   retorno  3.20% ->  2.30%
  comprar y mantener en test: 34.66%

segundo test final: FinalTestAlreadyEvaluatedError
```

Cómo leerlo:

1. **El ganador de validación se hunde en test.** Es lo esperable cuando la selección explota
   ruido: con dieciséis candidatos, alguno tiene un Sharpe alto por azar.
2. **Las señales de alarma estaban ahí antes del test.** DSR por debajo de 0,95 en los tres,
   Holm no rechaza la hipótesis nula para ningún candidato, y dos de los tres cambian de signo
   al quitar sus tres mejores operaciones. Quien hubiera leído esos controles no habría dado por
   buena la selección.
3. **El benchmark gana.** En este tramo sintético hay una deriva alcista (Módulo XII, sección
   12.9) y comprar y mantener supera a todos los candidatos.
4. **El test no se puede repetir.** El segundo intento lanza `FinalTestAlreadyEvaluatedError`.
5. **[Hecho]** Estos números coinciden con los de `docs/audit_report.md`, sección 4.

---

## 13.6 Sharpe probabilístico (PSR) y deflactado (DSR)

**Intuición.** Un Sharpe medido es una **estimación** con error. El PSR responde: "¿qué
probabilidad hay de que el Sharpe verdadero supere un umbral `SR*`?". El DSR elige ese umbral
de forma especial: el **Sharpe máximo que cabría esperar por azar** tras probar `N`
configuraciones. Si la mejor de cien estrategias sin ventaja alguna ya tendría un Sharpe
aparente alto, superar ese nivel es lo mínimo exigible.

<!-- cita: src/bybit_quant_lab/validation/overfitting.py#L1-L13 -->
`src/bybit_quant_lab/validation/overfitting.py` · líneas 1–13

```python
"""Controles estadísticos de sobreajuste y pruebas múltiples.

Supuestos y limitaciones:

* Sharpe probabilístico (PSR) y deflactado (DSR) de Bailey y López de Prado (2012, 2014):
  asumen retornos estacionarios y aproximadamente independientes; se corrigen por asimetría
  y curtosis pero no por autocorrelación. El DSR usa el número de configuraciones probadas y
  la varianza de sus Sharpe para estimar el Sharpe máximo esperado por azar.
* p-valores de la expectativa por operación: aproximación normal del estadístico t
  (válida para muestras grandes; con < 30 operaciones se marca como poco fiable).
* Holm-Bonferroni controla la tasa de error familiar sin asumir independencia.
* Bootstrap i.i.d. de operaciones (semilla fija): ignora dependencia temporal.
"""
```

<!-- cita: src/bybit_quant_lab/validation/overfitting.py#L28-L82 -->
`src/bybit_quant_lab/validation/overfitting.py` · líneas 28–82

```python
def _moments(returns: pd.Series) -> tuple[float, float, float, int]:
    r = returns.dropna().to_numpy(float)
    n = len(r)
    if n < 3 or r.std(ddof=1) == 0:
        return float("nan"), 0.0, 3.0, n
    sr = float(r.mean() / r.std(ddof=1))
    z = (r - r.mean()) / r.std(ddof=0)
    return sr, float(np.mean(z**3)), float(np.mean(z**4)), n


def psr_from_moments(
    sr: float, skew: float, kurtosis: float, n_obs: int, benchmark_sr: float = 0.0
) -> float | None:
    """PSR = Φ((SR - SR*)·sqrt(T-1) / sqrt(1 - γ3·SR + (γ4-1)/4·SR²)).

    ``sr`` no anualizado (misma frecuencia que las observaciones); ``kurtosis`` es la curtosis
    **no** en exceso (normal = 3). Devuelve ``None`` si el denominador no es positivo.
    """
    if n_obs < 3 or math.isnan(sr):
        return None
    denom = 1 - skew * sr + (kurtosis - 1) / 4 * sr**2
    if denom <= 0:
        return None
    return _N.cdf((sr - benchmark_sr) * math.sqrt(n_obs - 1) / math.sqrt(denom))


def probabilistic_sharpe(returns: pd.Series, benchmark_sr: float = 0.0) -> float | None:
    """P(SR verdadero > ``benchmark_sr``) con SR no anualizado por vela."""
    sr, skew, kurt, n = _moments(returns)
    return psr_from_moments(sr, skew, kurt, n, benchmark_sr)


def expected_max_sharpe(n_trials: int, sr_variance: float) -> float:
    """Sharpe máximo esperado bajo la hipótesis nula entre ``n_trials`` pruebas."""
    if n_trials <= 1 or sr_variance <= 0:
        return 0.0
    a = _N.inv_cdf(1 - 1 / n_trials)
    b = _N.inv_cdf(1 - 1 / (n_trials * math.e))
    return math.sqrt(sr_variance) * ((1 - EULER_GAMMA) * a + EULER_GAMMA * b)


def deflated_sharpe(
    returns: pd.Series, n_trials: int, trial_sharpes: list[float] | None = None
) -> dict[str, Any]:
    """Deflated Sharpe Ratio. ``trial_sharpes``: Sharpe no anualizados de todas las pruebas."""
    valid = [s for s in (trial_sharpes or []) if s is not None and math.isfinite(s)]
    var = float(np.var(valid, ddof=1)) if len(valid) > 1 else 0.0
    sr0 = expected_max_sharpe(n_trials, var)
    return {
        "n_trials": n_trials,
        "trial_sharpe_variance": var,
        "expected_max_sharpe_null": sr0,
        "dsr": probabilistic_sharpe(returns, sr0),
        "psr_vs_zero": probabilistic_sharpe(returns, 0.0),
    }
```

**Fórmulas** (todo por vela, **sin** anualizar):

```text
PSR(SR*) = Φ( (SR − SR*) · √(T − 1) / √(1 − γ₃·SR + (γ₄ − 1)/4 · SR²) )

SR₀ = √V · [ (1 − γ) · Φ⁻¹(1 − 1/N) + γ · Φ⁻¹(1 − 1/(N·e)) ]

DSR = PSR(SR₀)
```

Variables:

- `SR`: Sharpe por vela medido; `T`: número de observaciones.
- `γ₃`: asimetría; `γ₄`: curtosis **no** en exceso (normal = 3).
- `Φ`: función de distribución normal estándar; `Φ⁻¹`: su inversa.
- `N`: número de pruebas; `V`: varianza de los Sharpe de esas pruebas.
- `γ ≈ 0,5772`: constante de Euler-Mascheroni; `e ≈ 2,718`.

**Por qué asimetría y curtosis.** Con retornos de colas gruesas (γ₄ grande) o asimetría
negativa, el Sharpe medido es menos fiable: el denominador crece y el PSR baja.

**Ejemplo numérico del artículo** (Bailey y López de Prado, 2014): N = 100, varianza anual de
los Sharpe 0,5 (0,5/250 diaria), T = 1250 días, Sharpe anual 2,5, γ₃ = −3, γ₄ = 10:

<!-- ejecutar -->
```python
import math

from bybit_quant_lab.validation.overfitting import expected_max_sharpe, psr_from_moments

sr0 = expected_max_sharpe(100, 0.5 / 250)
sr = 2.5 / math.sqrt(250)
print(f"SR diario = {sr:.4f}")
print(f"SR0       = {sr0:.4f}")
print(f"DSR       = {psr_from_moments(sr, -3.0, 10.0, 1250, sr0):.4f}")
print(f"PSR(0)    = {psr_from_moments(sr, -3.0, 10.0, 1250, 0.0):.4f}")
```
<!-- salida -->
```text
SR diario = 0.1581
SR0       = 0.1132
DSR       = 0.9004
PSR(0)    = 1.0000
```

**[Supuesto] Estado de verificación de esos valores.** La prueba
`test_dsr_reproduces_worked_example` compara con SR₀ ≈ 0,1132 y DSR ≈ 0,9004, valores que la
auditoría citó **de memoria**. Al redactar este curso se intentó confirmarlos en internet: la
búsqueda localiza el artículo (Journal of Portfolio Management 40(5), 2014; SSRN 2460551),
pero no devolvió el ejemplo numérico, y el entorno no pudo abrir las páginas. Siguen sin
confirmar con la fuente. La implementación sí tiene verificaciones independientes:

<!-- cita: tests/unit/test_audit_statistics.py#L47-L60 -->
`tests/unit/test_audit_statistics.py` · líneas 47–60

```python
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
```

- El SR₀ de la fórmula coincide con el máximo de `N` normales simulado por Monte Carlo
  (error relativo < 3 % para N = 10, 100 y 1000).
- Bajo la hipótesis nula (Sharpe verdadero 0), `P(PSR > 0,95)` está entre el 3,5 % y el 6,5 %:
  el PSR está **calibrado**.

**[Limitación] (B-05).** `n_trials` cuenta configuraciones de **todas** las ejecuciones
registradas, pero la varianza `V` usa solo los candidatos de la ejecución actual. El PSR corrige
asimetría y curtosis, no la autocorrelación. Un DSR de 0,80 **no** es "un 80 % de probabilidad
de que la estrategia funcione": es una probabilidad bajo supuestos que los retornos por vela
de una estrategia con posiciones largas no cumplen del todo.

**Umbral habitual.** DSR ≥ 0,95 se interpreta como evidencia suficiente al 5 %. Es una
convención, no una garantía.

---

## 13.7 p-valores por operación y ajuste de Holm

<!-- cita: src/bybit_quant_lab/validation/overfitting.py#L85-L106 -->
`src/bybit_quant_lab/validation/overfitting.py` · líneas 85–106

```python
def mean_pvalue(values: pd.Series) -> tuple[float | None, bool]:
    """p-valor unilateral (H0: media <= 0) con aproximación normal. Devuelve (p, fiable)."""
    v = values.dropna().to_numpy(float)
    if len(v) < 2 or v.std(ddof=1) == 0:
        return None, False
    t = v.mean() / (v.std(ddof=1) / math.sqrt(len(v)))
    return 1 - _N.cdf(t), len(v) >= 30


def holm_bonferroni(pvalues: dict[str, float | None], alpha: float = 0.05) -> dict[str, dict]:
    """Ajuste de Holm. Devuelve p ajustado y si se rechaza H0 por hipótesis."""
    items = sorted(((k, p) for k, p in pvalues.items() if p is not None), key=lambda x: x[1])
    m = len(items)
    out: dict[str, dict] = {k: {"p": None, "p_adj": None, "reject": False} for k in pvalues}
    running = 0.0
    still = True
    for i, (k, p) in enumerate(items):
        adj = min(1.0, max(running, (m - i) * p))
        running = adj
        still = still and adj <= alpha
        out[k] = {"p": p, "p_adj": adj, "reject": still}
    return out
```

**p-valor (líneas 85–91).** Hipótesis nula: la expectativa por operación es ≤ 0. Estadístico
`t = media / (desv / √n)`; p unilateral `= 1 − Φ(t)`. Con menos de 30 operaciones se marca
como **poco fiable** (la aproximación normal es pobre).

**Holm (líneas 94–106).** Con `m` hipótesis ordenadas de menor a mayor p:

```text
p_ajustado(i) = máx( p_ajustado(i−1), (m − i) · p(i) ),   i = 0, 1, ...
se rechaza mientras p_ajustado ≤ α; al primer fallo, ya no se rechaza ninguna más
```

**Cálculo a mano** (`test_holm_step_down_by_hand`): p = {a: 0,01; b: 0,04; c: 0,03; d: 0,005},
m = 4, α = 0,05.

| Orden | Hipótesis | p | Multiplicador | p ajustado | ¿Rechaza? |
|---|---|---|---|---|---|
| 0 | d | 0,005 | 4 | 0,02 | Sí |
| 1 | a | 0,01 | 3 | 0,03 | Sí |
| 2 | c | 0,03 | 2 | 0,06 | No |
| 3 | b | 0,04 | 1 | máx(0,06; 0,04) = 0,06 | No |

Sin ajuste, las cuatro serían "significativas" al 5 %. Con Holm, solo dos.

**Por qué Holm y no Bonferroni.** Bonferroni multiplica todos por `m` (aquí, 0,02; 0,04; 0,12;
0,16). Holm controla el mismo error familiar y es menos conservador. Ninguno de los dos asume
independencia entre las pruebas.

---

## 13.8 Bootstrap y dependencia de pocas operaciones

<!-- cita: src/bybit_quant_lab/validation/overfitting.py#L109-L137 -->
`src/bybit_quant_lab/validation/overfitting.py` · líneas 109–137

```python
def bootstrap_mean_ci(
    values: pd.Series, n_samples: int = 1000, seed: int = 42, level: float = 0.95
) -> tuple[float, float] | None:
    """Intervalo bootstrap percentil para la media (p. ej., PnL neto por operación)."""
    v = values.dropna().to_numpy(float)
    if len(v) < 5:
        return None
    rng = np.random.default_rng(seed)
    means = rng.choice(v, size=(n_samples, len(v)), replace=True).mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, 1 - (1 - level) / 2])
    return float(lo), float(hi)


def top_trade_dependence(trades: pd.DataFrame, k: int = 3) -> dict[str, Any]:
    """Cuánto depende el resultado de las ``k`` mejores operaciones (y del 5 % superior)."""
    if trades.empty:
        return {"net": 0.0, "net_without_top_k": 0.0, "top_k_share": None, "k": k}
    net = trades["net_pnl"].astype(float).sort_values(ascending=False)
    total = float(net.sum())
    top = float(net.head(k).sum())
    n5 = max(1, math.ceil(len(net) * 0.05))
    return {
        "k": k,
        "net": total,
        "net_without_top_k": total - top,
        "top_k_share": top / total if total > 0 else None,
        "net_without_top_5pct": total - float(net.head(n5).sum()),
        "sign_flips_without_top_k": total > 0 >= total - top,
    }
```

**Bootstrap (líneas 109–119).** Remuestrea las operaciones **con reemplazo** 1000 veces
(`bootstrap_samples`), calcula la media de cada remuestreo y toma los percentiles 2,5 y 97,5.
Si el intervalo incluye el 0, no se puede descartar que la expectativa sea nula. La prueba de
cobertura comprueba que el intervalo del 95 % contiene la media verdadera entre el 89 % y el
98 % de las veces. **[Limitación]** Supone operaciones independientes; las rachas no se
modelan.

**Dependencia de las mejores operaciones (líneas 122–137).**

- `top_k_share`: fracción del resultado total que aportan las 3 mejores. **Puede superar 1**:
  si el total es 353 y las tres mejores suman 559, el resto **pierde** 206. En el ejemplo de
  13.5, `obv_trend` tiene exactamente ese perfil.
- `sign_flips_without_top_k`: verdadero si quitar las 3 mejores convierte un total positivo en
  ≤ 0. Es la señal más clara de fragilidad: el resultado depende de unos pocos episodios que
  quizá no se repitan.

---

## 13.9 Benchmarks

<!-- cita: src/bybit_quant_lab/validation/benchmarks.py#L1-L10 -->
`src/bybit_quant_lab/validation/benchmarks.py` · líneas 1–10

```python
"""Benchmarks: buy-and-hold, efectivo (referencia neutral) y entradas aleatorias.

* ``buy_and_hold``: compra 1x el capital (sin apalancamiento) en la primera apertura del
  segmento con comisión y slippage, y vende al cierre final con los mismos costes.
* ``cash``: equity constante (retorno 0). Referencia neutral para estrategias long/short.
* ``random_entries``: estados aleatorios (semilla fija) con la misma fracción de velas activas
  y duración media similar a una estrategia de referencia, medidas solo en el segmento
  simulado, con el mismo motor, stops y costes. En ``bql compare`` la referencia es la primera
  estrategia de la lista (su nombre figura en la etiqueta); no es un benchmark por estrategia.
"""
```

| Benchmark | Qué responde | Detalle |
|---|---|---|
| `buy_and_hold` | ¿Supera la estrategia a simplemente comprar? | Compra 1× el capital con comisión y deslizamiento; sin funding (lo advierte) |
| `cash` | ¿Supera a no hacer nada? | Retorno 0 |
| `random` | ¿Supera a entrar al azar con la misma exposición y gestión? | Mismo motor, stops y costes; semilla fija |

<!-- cita: src/bybit_quant_lab/validation/benchmarks.py#L134-L161 -->
`src/bybit_quant_lab/validation/benchmarks.py` · líneas 134–161

```python
def random_signals(
    reference: pd.DataFrame, seed: int, calibration: slice | None = None
) -> pd.DataFrame:
    """Señales aleatorias con exposición y duración media similares a ``reference``.

    ``calibration`` limita las velas usadas para medir exposición y duración (el segmento
    simulado), de modo que el benchmark no use estadísticas de otros períodos.
    """
    rng = np.random.default_rng(seed)
    sig = reference["signal"].to_numpy()[calibration or slice(None)]
    n_out = len(reference)
    active = sig != 0
    starts = int(np.sum(active[1:] & (sig[1:] != sig[:-1]))) + int(active[0]) if len(sig) else 0
    avg_len = max(int(active.sum() / starts), 1) if starts else 1
    out = np.zeros(n_out, dtype=np.int64)
    p_start = starts / max(len(sig) - active.sum(), 1)
    i = 0
    while i < n_out:
        if rng.random() < p_start:
            length = max(1, int(rng.exponential(avg_len)))
            out[i : i + length] = rng.choice([-1, 1])
            i += length + 1
        else:
            i += 1
    frame = reference.copy()
    frame["signal"] = out
    frame["conviction"] = np.where(out != 0, 0.5, 0.0)
    return frame
```

- **143:** la exposición y la duración media se miden solo en el segmento simulado
  (`calibration`). Corrección B-02: antes se medían en toda la serie, incluido el test.
- **146–149:** número de "arranques" de la referencia, duración media de sus posiciones y
  probabilidad de iniciar una posición en cada vela libre.
- **152–155:** con esa probabilidad se abre una posición de dirección aleatoria y duración
  exponencial.

**[Limitación]** En `bql compare`, la referencia es la **primera** estrategia de la lista; no hay
un benchmark aleatorio por estrategia (la etiqueta lo indica). Un solo sorteo con semilla fija
no es una distribución: para comparar en serio habría que repetirlo con muchas semillas.

---

## 13.10 Walk-forward

**Intuición.** En lugar de una sola división, se repite el ciclo "optimizar en el pasado,
evaluar en el siguiente tramo" a lo largo del tiempo, como haría alguien que reoptimiza
periódicamente.

<!-- cita: src/bybit_quant_lab/validation/splits.py#L64-L94 -->
`src/bybit_quant_lab/validation/splits.py` · líneas 64–94

```python
def walk_forward_windows(
    index: pd.DatetimeIndex,
    train_bars: int,
    test_bars: int,
    step_bars: int | None = None,
    anchored: bool = False,
    embargo_bars: int = 0,
) -> list[tuple[Segment, Segment]]:
    """Ventanas (entrenamiento, prueba) consecutivas; ``anchored`` fija el inicio en 0."""
    step = step_bars or test_bars
    out = []
    k = 0
    start = 0
    while True:
        tr_end = start + train_bars - 1 if not anchored else train_bars - 1 + k * step
        te_start = tr_end + 1 + embargo_bars
        te_end = te_start + test_bars - 1
        if te_end >= len(index):
            break
        tr_start = 0 if anchored else start
        out.append(
            (
                _segment(index, f"wf{k}_train", tr_start, tr_end),
                _segment(index, f"wf{k}_test", te_start, te_end),
            )
        )
        k += 1
        start += step
    if not out:
        raise ValueError("Datos insuficientes para una sola ventana walk-forward")
    return out
```

- **Ventana móvil** (`anchored=False`): el entrenamiento tiene siempre `train_bars` velas y se
  desplaza `step` velas.
- **Ventana anclada** (`anchored=True`): el entrenamiento empieza siempre en 0 y crece.
- `step` es por defecto igual a `test_bars`: los tramos de prueba quedan contiguos.

<!-- cita: src/bybit_quant_lab/validation/research.py#L462-L533 -->
`src/bybit_quant_lab/validation/research.py` · líneas 462–533

```python
    def walk_forward(self, strategy: str, space: dict[str, list[Any]]) -> dict[str, Any]:
        """Optimiza en cada ventana de entrenamiento y evalúa fuera de muestra.

        Las ventanas se limitan a entrenamiento + validación: el período de test final nunca
        se usa, para que siga siendo una evaluación independiente.
        """
        v = self.config.validation
        grid = param_grid(space, v.max_grid_size)
        usable = self.segments["validation"].end_pos + 1
        windows = walk_forward_windows(
            pd.DatetimeIndex(self.data.index[:usable]),
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
                    # False: ninguna configuración alcanzó min_trades_selection en esta ventana
                    # y se usó la primera de la rejilla por defecto (no es una selección real).
                    "selection_valid": bool(np.isfinite(best_score)),
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
            "data_range": [str(self.data.index[0]), str(self.data.index[usable - 1])],
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
```

- **469:** la rejilla tiene un límite (`max_grid_size`, 200) (sección 13.12).
- **470–478 (corrección A-01):** las ventanas se construyen solo con entrenamiento +
  validación. Antes recorrían toda la serie y el último tramo fuera de muestra caía en el test.
- **486–490:** en cada ventana se elige la mejor configuración **en entrenamiento**; ante
  empates, la primera de la rejilla (`-x[1]`).
- **491–494:** se simula esa configuración en el tramo de prueba.
- **506 (corrección B-03):** `selection_valid` es `False` si ninguna configuración alcanzó el
  mínimo de operaciones; entonces se usó la primera de la rejilla y no hubo selección real.
- **514–527:** los retornos fuera de muestra se encadenan en una sola curva.

Ejemplo con la rejilla de `ema_crossover` del YAML (12 combinaciones):

<!-- ejecutar -->
```python
import yaml

from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.validation.research import Researcher

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
raw = yaml.safe_load(open("configs/strategies.yaml"))
r = Researcher(datos, "BTCUSDT", "1h", load_config(),
               strategy_params=load_strategy_params("configs/strategies.yaml"))
wf = r.walk_forward("ema_crossover", raw["grids"]["ema_crossover"])
print("rejilla:", wf["grid_size"], "| datos usados:", wf["data_range"])
print("inicio del test final:", r.segments["test"].start)
tabla = wf["windows"][["window", "test_start", "params", "selection_valid", "is_sharpe",
                        "oos_net_profit", "oos_trades"]]
print(tabla.round(2).to_string())
print(f"fuera de muestra: retorno {wf['oos_total_return']:.2%}, "
      f"Sharpe {wf['oos_sharpe']:.2f}, drawdown {wf['oos_max_drawdown']:.2%}")
print("estabilidad en entrenamiento:",
      {k: round(v, 3) if isinstance(v, float) else v for k, v in wf["stability"].items()})
```
<!-- salida -->
```text
rejilla: 12 | datos usados: ['2023-01-01 00:00:00+00:00', '2023-07-19 23:00:00+00:00']
inicio del test final: 2023-07-20 00:00:00+00:00
   window                 test_start                                            params  selection_valid  is_sharpe  oos_net_profit  oos_trades
0       0  2023-03-25 08:00:00+00:00  {'fast': 8, 'slow': 26, 'regime_filter': 'none'}             True       2.81            8.09           9
1       1  2023-04-15 04:00:00+00:00  {'fast': 8, 'slow': 26, 'regime_filter': 'none'}             True       1.83          256.72          10
2       2  2023-05-06 00:00:00+00:00   {'fast': 8, 'slow': 26, 'regime_filter': 'adx'}             True       2.61          270.91           3
3       3  2023-05-26 20:00:00+00:00   {'fast': 8, 'slow': 26, 'regime_filter': 'adx'}             True       3.13          -68.25           1
4       4  2023-06-16 16:00:00+00:00   {'fast': 8, 'slow': 26, 'regime_filter': 'adx'}             True       3.00         -270.79           3
fuera de muestra: retorno 1.88%, Sharpe 0.72, drawdown 4.27%
estabilidad en entrenamiento: {'metric': 'sharpe', 'n': 38, 'best': 3.129, 'median': -0.296, 'worst': -3.659, 'std': 1.983, 'fraction_positive': 0.447, 'best_minus_median': 3.425}
```

Cómo leerlo:

- Las ventanas terminan antes del inicio del test final: el test sigue intacto.
- La mejor configuración en entrenamiento tiene Sharpe entre 1,8 y 3,1 en todas las ventanas;
  fuera de muestra, el resultado es irregular, con varias ventanas de muy pocas operaciones.
- `stability`: de las configuraciones con Sharpe calculable, la mediana es negativa y menos de
  la mitad son positivas; la mejor está muy por encima de la mediana (`best_minus_median`).
  Es el patrón de un resultado que depende del ajuste fino (sección 13.12).

**[Limitación]** Los tramos de prueba del walk-forward **se solapan con el segmento de
validación** que `bql compare` usa para seleccionar. Las dos órdenes son independientes, pero si
alguien decide parámetros mirando el walk-forward y después selecciona con `compare`, usa la
validación dos veces. El registro de experimentos guarda ambas, pero el protocolo no lo impide.

---

## 13.11 Registro de experimentos y guarda del test final

<!-- cita: src/bybit_quant_lab/validation/experiment_log.py#L17-L62 -->
`src/bybit_quant_lab/validation/experiment_log.py` · líneas 17–62

```python
class ExperimentLog:
    """Registro append-only en ``path``."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record: dict[str, Any]) -> None:
        """Añade un registro con marca temporal UTC."""
        rec = {"logged_at": datetime.now(UTC).isoformat(), **record}
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, default=str, sort_keys=True) + "\n")

    def records(self) -> list[dict[str, Any]]:
        """Todos los registros."""
        if not self.path.exists():
            return []
        with self.path.open(encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]

    def count(self, kind: str | None = None, data_hash: str | None = None) -> int:
        """Número de configuraciones registradas (filtrables por tipo y datos)."""
        return sum(
            1
            for r in self.records()
            if (kind is None or r.get("kind") == kind)
            and (data_hash is None or r.get("data_hash") == data_hash)
        )

    def count_distinct_configs(
        self, data_hash: str, segment: str = "validation", cost_mode: str = "net"
    ) -> int:
        """Configuraciones distintas (candidato + parámetros) evaluadas en ``segment``.

        Es el número de pruebas que se usa para deflactar el Sharpe: incluye todas las
        ejecuciones registradas sobre los mismos datos, no solo la actual.
        """
        keys = {
            json.dumps([r.get("candidate"), r.get("params")], sort_keys=True, default=str)
            for r in self.records()
            if r.get("kind") == "evaluation"
            and r.get("data_hash") == data_hash
            and r.get("segment") == segment
            and r.get("cost_mode") == cost_mode
        }
        return len(keys)
```

- **Append-only:** solo se añaden líneas JSON (formato JSON Lines); nunca se reescriben.
- **`count_distinct_configs`:** cuenta pares (candidato, parámetros) evaluados en validación con
  el mismo hash de datos. Se acumula entre ejecuciones: si alguien prueba veinte variantes en
  días distintos, `N` lo refleja y el DSR se vuelve más exigente.

<!-- cita: src/bybit_quant_lab/validation/experiment_log.py#L69-L103 -->
`src/bybit_quant_lab/validation/experiment_log.py` · líneas 69–103

```python
def guard_final_test(
    log: ExperimentLog,
    selection_id: str,
    allow_repeat: bool,
    data_hash: str | None = None,
    test_segment: dict[str, Any] | None = None,
) -> bool:
    """Comprueba si el período de test ya se usó. Devuelve ``True`` si es repetición.

    Bloquea tanto la misma selección como **cualquier otra** evaluada sobre los mismos datos
    y el mismo período de test: probar varias selecciones contra el test y quedarse con la
    mejor equivale a seleccionar con el test.
    """

    def same_period(r: dict[str, Any]) -> bool:
        return (
            data_hash is not None
            and r.get("data_hash") == data_hash
            and (test_segment is None or r.get("test_segment") in (None, test_segment))
        )

    done = [
        r
        for r in log.records()
        if r.get("kind") == "final_test"
        and (r.get("selection_id") == selection_id or same_period(r))
    ]
    if done and not allow_repeat:
        raise FinalTestAlreadyEvaluatedError(
            f"El período de test de estos datos ya se evaluó el {done[0]['logged_at']} "
            f"(selección {done[0].get('selection_id')}). Evaluar otra selección o la misma tras "
            "cambios invalidaría la independencia del test. Usa --allow-repeat solo si "
            "entiendes la consecuencia; el informe lo marcará como no independiente."
        )
    return bool(done)
```

- **Corrección A-02:** la guarda bloquea cualquier evaluación con los **mismos datos y el mismo
  segmento de test**, no solo la misma selección. Antes, una selección con otro `top_k` tenía
  otro identificador y podía evaluarse sobre el mismo test: probar varias selecciones contra el
  test y quedarse con la mejor es seleccionar con el test.
- `--allow-repeat` permite repetir, pero el resultado queda marcado como no independiente.

**Corrección A-03 (selección congelada).** `run_final_test` (líneas 382–459) rechaza datos o
configuración distintos y reconstruye todas las estrategias con los `strategy_params`
**guardados**, no con el YAML vigente:

<!-- cita: src/bybit_quant_lab/validation/research.py#L386-L413 -->
`src/bybit_quant_lab/validation/research.py` · líneas 386–413

```python
        if selection["data_hash"] != self.data_hash:
            raise ValueError("Los datos no coinciden con los usados en la selección")
        if selection.get("config_hash") != config_hash(self.config):
            raise ValueError(
                "La configuración actual difiere de la usada en la selección (costes, riesgo, "
                "segmentos...); el test final debe usar exactamente la misma configuración."
            )
        frozen = selection.get("strategy_params")
        if not isinstance(frozen, dict):
            raise ValueError(
                "La selección no contiene 'strategy_params' (formato anterior a la auditoría); "
                "vuelve a ejecutar 'bql compare'."
            )
        if self.log is None:
            raise ValueError("El test final requiere un log de experimentos")
        seg = self.segments["test"]
        repeated = guard_final_test(
            self.log, selection["selection_id"], allow_repeat, self.data_hash, seg.to_dict()
        )
        singles = {
            n: Candidate(
                n,
                "strategy",
                create_strategy(n, frozen.get(n, {})).generate_signals(self.data),
                frozen.get(n, {}),
            )
            for n in available_strategies()
        }
```

---

## 13.12 Sensibilidad de parámetros y tamaño de las rejillas

<!-- cita: src/bybit_quant_lab/validation/sensitivity.py#L12-L44 -->
`src/bybit_quant_lab/validation/sensitivity.py` · líneas 12–44

```python
def param_grid(space: dict[str, list[Any]], max_size: int) -> list[dict[str, Any]]:
    """Producto cartesiano de ``space``. Lanza ``ValueError`` si supera ``max_size``."""
    if not space:
        return [{}]
    size = int(np.prod([len(v) for v in space.values()]))
    if size > max_size:
        raise ValueError(
            f"La rejilla tiene {size} combinaciones y el límite es {max_size}. Reduce el "
            "espacio de búsqueda (más pruebas = mayor riesgo de sobreajuste)."
        )
    keys = list(space)
    return [dict(zip(keys, combo, strict=True)) for combo in itertools.product(*space.values())]


def stability_summary(table: pd.DataFrame, metric: str) -> dict[str, Any]:
    """Resumen de la distribución de ``metric`` en la rejilla.

    Una mejor configuración muy alejada de la mediana, o pocas configuraciones con valor
    positivo, sugieren que el resultado depende de un ajuste fino (frágil).
    """
    vals = table[metric].astype(float).dropna()
    if vals.empty:
        return {"metric": metric, "n": 0}
    return {
        "metric": metric,
        "n": len(vals),
        "best": float(vals.max()),
        "median": float(vals.median()),
        "worst": float(vals.min()),
        "std": float(vals.std(ddof=1)) if len(vals) > 1 else 0.0,
        "fraction_positive": float((vals > 0).mean()),
        "best_minus_median": float(vals.max() - vals.median()),
    }
```

- **`param_grid`:** producto cartesiano; si supera `max_grid_size` (200), error explícito. Cada
  combinación es una prueba más (sección 6.9).
- **`stability_summary`:** si la mejor configuración está muy lejos de la mediana o pocas son
  positivas, el resultado es **frágil**: depende de haber acertado un valor concreto.
- `Researcher.sensitivity` (líneas 535–548) prohíbe el segmento de test.

**[Limitación]** La sensibilidad admite `--segment validation`. Explorar parámetros en
validación y después seleccionar con la misma validación es un doble uso que el código permite
(aunque lo registra).

**[Hallazgo] Rejilla con duplicados.** La rejilla de `macd_momentum` del YAML (línea 185)
combina `require_hist_rising: [true, false]`, un parámetro sin efecto (Módulo VIII, sección
8.7): la mitad de las configuraciones son idénticas a la otra mitad, y cuentan como pruebas
distintas.

---

## 13.13 Historia de las correcciones de la auditoría

Las correcciones de validación están en dos commits. Cada prueba **fallaba** en `fc4e578` (la
versión anterior a la auditoría) y pasa desde la corrección (`docs/audit_report.md`).

| Hallazgo | Problema | Commit | Prueba que lo impide |
|---|---|---|---|
| A-01 | Walk-forward sobre el test | `a50ac62` | `test_walk_forward_never_uses_test_segment` |
| A-02 | Guarda por selección, no por período | `a50ac62` | `test_final_test_period_can_only_be_used_once` |
| A-03 | Selección no congelada; sin control de configuración | `a50ac62` | `test_final_test_uses_frozen_member_params`, `test_final_test_rejects_changed_config` |
| M-01 | Umbral ponderado ajustado en validación | `a50ac62` | `test_combination_thresholds_not_tuned_on_validation` |
| B-01 | Dos combinaciones idénticas | `a50ac62` | `test_configured_combinations_are_not_equivalent` |
| B-02 | Benchmark aleatorio calibrado con toda la serie | `a50ac62` | `test_random_benchmark_calibrated_only_on_simulated_segment` |
| B-03 | Walk-forward sin selección válida no señalado | `697b6af` | `test_walk_forward_flags_windows_without_valid_selection` |

La prueba de A-02, completa:

<!-- cita: tests/unit/test_audit_statistics.py#L94-L103 -->
`tests/unit/test_audit_statistics.py` · líneas 94–103

```python
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
```

Para ver un cambio concreto: `git show a50ac62 -- src/bybit_quant_lab/validation/research.py`.

---

## 13.14 Supuestos y limitaciones

| Tema | Estado |
|---|---|
| Un único corte train/validación/test | [Diseño]; un solo test es una sola muestra |
| El selector no usa DSR/Holm/dependencia | [Hecho]; se informan, no bloquean |
| `N` acumulado pero `V` solo de la ejecución actual | [Limitación] B-05 |
| DSR/PSR sin corrección por autocorrelación | [Limitación] |
| Valores del ejemplo del artículo sin confirmar en la fuente | [Pendiente] |
| Walk-forward y sensibilidad pueden reutilizar validación | [Limitación] de protocolo |
| Bootstrap i.i.d. | [Limitación] |
| Benchmark aleatorio con una sola semilla | [Limitación] |
| Rejilla de MACD con duplicados | [Hallazgo] |

### Comprobación final del módulo

Ejecutas `bql compare`, no te gusta la selección, cambias `top_k` de 3 a 5, vuelves a ejecutar
`compare` y lanzas `bql final-test` con la segunda selección. Después lanzas `final-test` con la
primera. ¿Qué ocurre en cada paso y por qué?

<details><summary>Ver respuesta</summary>

- El segundo `compare` registra más evaluaciones: `N` crece y el DSR se vuelve más exigente
  (aunque las configuraciones repetidas no cuentan dos veces, porque se cuentan pares distintos).
- El primer `final-test` (segunda selección) se ejecuta y queda registrado.
- El segundo `final-test` (primera selección) se **rechaza**: mismos datos y mismo segmento de
  test, aunque el `selection_id` sea distinto (corrección A-02). Solo podría forzarse con
  `--allow-repeat`, y el informe lo marcaría como no independiente.
- Además, cambiar `top_k` **después de ver** la selección ya es una decisión tomada con la
  validación; el registro no lo detecta, pero es parte del sesgo de selección.
</details>
