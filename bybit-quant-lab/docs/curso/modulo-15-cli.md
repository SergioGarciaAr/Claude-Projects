# Módulo XV. La línea de comandos, los informes y el uso práctico

Todo lo visto hasta ahora se usa desde una sola orden: `bql`. Este módulo describe sus doce
subórdenes tal como existen en la versión actual (`src/bybit_quant_lab/cli.py`), los archivos
que generan, cómo leer los informes y un flujo de trabajo completo ejecutado de verdad.

> **[Hecho]** Ninguna orden envía órdenes de trading, usa credenciales ni llama a endpoints
> autenticados. `download` usa solo endpoints públicos de mercado, y en el entorno donde se
> escribió este curso **no se ha podido probar** porque el proxy bloquea `api.bybit.com`.

---

## 15.1 Instalación y directorio de trabajo

```bash
cd bybit-quant-lab
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e ".[dev]"
bql --help
```

- `pip install -e` (modo editable) instala el paquete apuntando al código fuente: los cambios
  en `src/` se ven sin reinstalar.
- `[dev]` añade pytest, ruff y mypy.
- La orden `bql` la crea `pyproject.toml`:

<!-- cita: pyproject.toml#L33-L34 -->
`pyproject.toml` · líneas 33–34

```toml
[project.scripts]
bql = "bybit_quant_lab.cli:main"
```

Es decir, `bql` ejecuta la función `main` de `bybit_quant_lab/cli.py`. `python -m
bybit_quant_lab.cli` es equivalente.

**[Hecho] Hay que ejecutar `bql` desde `bybit-quant-lab/`.** Las rutas por defecto son
relativas:

<!-- cita: src/bybit_quant_lab/cli.py#L64-L91 -->
`src/bybit_quant_lab/cli.py` · líneas 64–91

```python
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
```

Si `configs/default.yaml` no existe en el directorio actual, se usan los valores por defecto del
código (línea 71) **sin aviso**. Si falta `configs/strategies.yaml`, se usan los parámetros por
defecto de cada estrategia y, como no hay combinaciones, una sola combinación `vote_all` con
`veto` (líneas 94–98; Módulo IX, sección 9.4). Los resultados cambiarían sin que nada lo
advierta.

---

## 15.2 Opciones globales y punto de entrada

<!-- cita: src/bybit_quant_lab/cli.py#L692-L711 -->
`src/bybit_quant_lab/cli.py` · líneas 692–711

```python
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
```

- **Opciones globales** (van **antes** de la suborden): `--config`, `--strategies-config`,
  `--data-dir`, `--output-dir`, `--log-level`.
- **Línea 696–697:** toda orden salvo `list-strategies` imprime en la salida de errores la
  advertencia legal ("resultados de backtesting con fines exclusivos de investigación...").
- **Líneas 703–707:** los errores esperables (archivo inexistente, parámetro inválido) se
  muestran como `Error: ...` sin traza, con código de salida 1.

**Códigos de salida:**

| Código | Significado |
|---|---|
| 0 | Correcto |
| 1 | Error de uso o datos (también `validate-data` con datos inválidos) |
| 2 | Error de la API de Bybit (`download`) |
| 3 | `final-test` rechazado porque el período de test ya se evaluó |

---

## 15.3 Las doce subórdenes

| Orden | Para qué | Argumentos obligatorios | Opcionales (por defecto) | Segmento |
|---|---|---|---|---|
| `list-strategies` | Listar estrategias | — | — | — |
| `synth` | Generar datos sintéticos | `--symbol`, `--timeframe` | `--bars` 6000, `--seed` 42, `--start` 2023-01-01 | — |
| `download` | Descargar velas (y funding) | `--symbol`, `--timeframe` (uno o varios), `--start` | `--end` (ahora), `--funding`, `--refresh` | — |
| `import` | Importar CSV/Parquet | `--symbol`, `--timeframe`, `--file` | `--time-column` | — |
| `validate-data` | Validar un dataset | `--symbol`, `--timeframe` | — | — |
| `backtest` | Una estrategia, con informe | `--symbol`, `--timeframe`, `--strategy` | `--params` (JSON), `--segment` train, `--out` | train / validation / full |
| `compare` | Todas las estrategias y combinaciones; selección | `--symbol`, `--timeframe` | `--strategies`, `--top-k` 3, `--out` | train + validation |
| `final-test` | Evaluar la selección congelada | `--selection` | `--allow-repeat`, `--out` | test |
| `walkforward` | Walk-forward con rejilla | `--symbol`, `--timeframe`, `--strategy` | `--grid` (JSON; si no, la del YAML), `--out` | train + validation |
| `sensitivity` | Rejilla de parámetros | `--symbol`, `--timeframe`, `--strategy` | `--grid`, `--segment` train, `--out` | train / validation |
| `markets` | Matriz símbolo × temporalidad | `--symbols`, `--timeframes` | `--strategies`, `--segment` validation, `--out` | train / validation |
| `report` | Regenerar el HTML de un backtest | `--run-dir` | — | — |

Detalles que conviene saber:

- **`backtest --segment full`** incluye el período de test. El informe lo advierte
  (`cli.py`, líneas 265–269), pero no lo impide: úsalo solo para inspeccionar, nunca para
  decidir.
- **`final-test`** no recibe símbolo ni temporalidad: los lee de `selection.json`
  (líneas 351–352). Recibe una lista de combinaciones (`_combos`), pero `run_final_test` no la
  usa: reconstruye cada combinación con los parámetros guardados en la selección
  (`research.py`, líneas 430–437). **[Hallazgo]** Es un parámetro sin efecto.
- **`report`** regenera el HTML desde los CSV y JSON exportados, pero sin benchmarks ni la
  comparación bruto/neto (pasa `None`, líneas 578–586): el informe regenerado tiene menos
  secciones que el original.
- **`--params`** en `backtest` se **fusiona** con los parámetros del YAML (línea 245); Pydantic
  valida el resultado.
- **[Discrepancia]** `docs/progress.md` (línea 13) habla de "11 órdenes"; la CLI actual tiene
  12 (`markets` se añadió después).

Comprobación de que todas las órdenes de este módulo son sintácticamente válidas para el
parser actual (la misma técnica que `test_every_documented_cli_command_parses`):

<!-- ejecutar -->
```python
import shlex

from bybit_quant_lab.cli import build_parser

ordenes = [
    "list-strategies",
    "synth --symbol BTCUSDT --timeframe 1h --bars 6000 --seed 42",
    "download --symbol BTCUSDT --timeframe 5m 15m 1h 4h --start 2023-01-01 --end 2024-12-31 --funding",
    "import --symbol BTCUSDT --timeframe 1h --file mis_velas.csv",
    "validate-data --symbol BTCUSDT --timeframe 1h",
    "backtest --symbol BTCUSDT --timeframe 1h --strategy ema_crossover --params '{\"fast\": 8}'",
    "backtest --symbol BTCUSDT --timeframe 1h --strategy donchian_breakout --segment validation",
    "compare --symbol BTCUSDT --timeframe 1h --top-k 3",
    "final-test --selection outputs/compare_BTCUSDT_1h_X/selection.json",
    "walkforward --symbol BTCUSDT --timeframe 1h --strategy ema_crossover",
    "walkforward --symbol BTCUSDT --timeframe 1h --strategy donchian_breakout --grid '{\"channel\": [20, 40]}'",
    "sensitivity --symbol BTCUSDT --timeframe 1h --strategy rsi_reversion --segment train",
    "markets --symbols BTCUSDT ETHUSDT --timeframes 1h 4h --segment validation",
    "report --run-dir outputs/backtest_BTCUSDT_1h_donchian_breakout_X",
    "--data-dir /tmp/datos --output-dir /tmp/salidas compare --symbol ETHUSDT --timeframe 4h",
]
parser = build_parser()
for orden in ordenes:
    args = parser.parse_args(shlex.split(orden))
    print(f"ok  {args.command}")
```
<!-- salida -->
```text
ok  list-strategies
ok  synth
ok  download
ok  import
ok  validate-data
ok  backtest
ok  backtest
ok  compare
ok  final-test
ok  walkforward
ok  walkforward
ok  sensitivity
ok  markets
ok  report
ok  compare
```

---

## 15.4 Una sesión completa, ejecutada

El bloque siguiente ejecuta la CLI real en un directorio temporal, con datos sintéticos:
genera datos, los valida, hace un backtest, una comparación, el test final y un segundo test
final (que debe rechazarse), y regenera el informe. Para que la salida sea reproducible se
quitan las líneas de registro con hora, la advertencia legal y las fechas variables.

<!-- ejecutar -->
```python
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def bql(tmp, *args):
    base = [sys.executable, "-m", "bybit_quant_lab.cli",
            "--data-dir", f"{tmp}/data", "--output-dir", f"{tmp}/outputs"]
    p = subprocess.run([*base, *args], capture_output=True, text=True, check=False)
    texto = (p.stdout + p.stderr).replace(tmp, "<TMP>")
    lineas = [
        ln for ln in texto.splitlines()
        if not re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d+ ", ln)   # registro con hora
        and not ln.startswith("ADVERTENCIA:")                          # aviso legal
    ]
    texto = "\n".join(lineas)
    texto = re.sub(r"\d{4}-\d\d-\d\dT[\d:.+]+", "<FECHA>", texto)
    texto = re.sub(r"selección [0-9a-f]{16}", "selección <ID>", texto)
    return p.returncode, texto


with tempfile.TemporaryDirectory() as tmp:
    pasos = [
        ("synth", "--symbol", "BTCUSDT", "--timeframe", "1h", "--bars", "6000"),
        ("validate-data", "--symbol", "BTCUSDT", "--timeframe", "1h"),
        ("backtest", "--symbol", "BTCUSDT", "--timeframe", "1h",
         "--strategy", "donchian_breakout", "--out", f"{tmp}/outputs/bt"),
        ("compare", "--symbol", "BTCUSDT", "--timeframe", "1h", "--out", f"{tmp}/outputs/cmp"),
        ("final-test", "--selection", f"{tmp}/outputs/cmp/selection.json",
         "--out", f"{tmp}/outputs/ft"),
        ("final-test", "--selection", f"{tmp}/outputs/cmp/selection.json",
         "--out", f"{tmp}/outputs/ft2"),
        ("report", "--run-dir", f"{tmp}/outputs/bt"),
    ]
    for args in pasos:
        codigo, texto = bql(tmp, *args)
        print(f"$ bql {args[0]}  -> código {codigo}")
        if args[0] in ("validate-data", "final-test"):
            texto = "\n".join(texto.splitlines()[:4]) + "\n  [...]"
        print(texto)
        print()
    print("ARCHIVOS GENERADOS:")
    for p in sorted(Path(tmp).rglob("*")):
        if p.is_file():
            print(" ", p.relative_to(tmp))
```
<!-- salida -->
```text
$ bql synth  -> código 0
Dataset SINTÉTICO guardado en <TMP>/data/processed/BTCUSDT_1h.parquet (6000 velas). No usar para evaluar rentabilidad real.

$ bql validate-data  -> código 0
{
  "rows": 6000,
  "start": "2023-01-01 00:00:00+00:00",
  "end": "2023-09-07 23:00:00+00:00",
  [...]

$ bql backtest  -> código 0
Backtest donchian_breakout BTCUSDT 1h [train]
  net_profit       1765.7616
  net_profit_pct   0.1766
  sharpe           2.1710
  max_drawdown     0.0888
  num_trades       87
  win_rate         0.3678
  profit_factor    1.3787
  expectancy       20.2961
  total_costs      597.7763
  total_funding    0.0000
  ! Período de 150 días < 180: CAGR no calculado.
  ! Sin datos históricos de funding: no se aplica (no se simula). El resultado neto excluye el coste/ingreso de funding.
  ! Especificaciones de BTCUSDT no verificadas con instruments-info (valores de referencia).
Informe: <TMP>/outputs/bt/report.html

$ bql compare  -> código 0
                     candidate        kind  net_profit  sharpe  max_drawdown  num_trades
                        adx_di    strategy      81.261   0.455         0.047          25
           bollinger_reversion    strategy    -248.638  -1.570         0.054          38
             donchian_breakout    strategy    -246.487  -0.884         0.068          31
                 ema_crossover    strategy     -92.498     NaN         0.034           4
                 macd_momentum    strategy    -132.916  -0.609         0.058          43
                     obv_trend    strategy     353.285   2.617         0.033          35
                 rsi_reversion    strategy      36.583     NaN         0.010           3
                     stoch_rsi    strategy   1,449.071   5.619         0.062          68
                  volume_spike    strategy    -118.782     NaN         0.034           6
                vwap_deviation    strategy    -157.258  -1.099         0.051          11
                      vote_all combination       0.442   0.050         0.053          44
                weighted_train combination      20.955   0.315         0.028          19
                   consensus_3 combination     -18.264  -0.193         0.034          26
                    category_2 combination     -75.180  -0.678         0.042          33
                    dedup_vote combination    -108.475  -0.883         0.052          39
                 regime_switch combination     319.777   1.609         0.053          67
        benchmark_buy_and_hold   benchmark  -1,424.099  -1.267         0.339           1
                benchmark_cash   benchmark       0.000     NaN         0.000           0
benchmark_random_adx_di_seed42   benchmark      68.311   0.420         0.038          26

Seleccionados en validación: ['stoch_rsi', 'obv_trend', 'regime_switch']
Selección congelada: <TMP>/outputs/cmp/selection.json
Informe: <TMP>/outputs/cmp/report.html

$ bql final-test  -> código 0
stoch_rsi (test, neto):
  net_profit       -662.1794
  net_profit_pct   -0.0662
  sharpe           -2.9307
  [...]

$ bql final-test  -> código 3
El período de test de estos datos ya se evaluó el <FECHA> (selección <ID>). Evaluar otra selección o la misma tras cambios invalidaría la independencia del test. Usa --allow-repeat solo si entiendes la consecuencia; el informe lo marcará como no independiente.
  [...]

$ bql report  -> código 0
Informe regenerado: <TMP>/outputs/bt/report.html

ARCHIVOS GENERADOS:
  data/processed/BTCUSDT_1h.meta.json
  data/processed/BTCUSDT_1h.parquet
  outputs/bt/equity.csv
  outputs/bt/metadata.json
  outputs/bt/metrics.json
  outputs/bt/report.html
  outputs/bt/risk_events.json
  outputs/bt/run.json
  outputs/bt/trades.csv
  outputs/cmp/metadata.json
  outputs/cmp/report.html
  outputs/cmp/selection.json
  outputs/cmp/signal_correlation_train.csv
  outputs/cmp/statistics.json
  outputs/cmp/summary.csv
  outputs/experiments.jsonl
  outputs/ft/metadata.json
  outputs/ft/obv_trend_equity.csv
  outputs/ft/obv_trend_metrics.json
  outputs/ft/obv_trend_risk_events.json
  outputs/ft/obv_trend_trades.csv
  outputs/ft/regime_switch_equity.csv
  outputs/ft/regime_switch_metrics.json
  outputs/ft/regime_switch_risk_events.json
  outputs/ft/regime_switch_trades.csv
  outputs/ft/report.html
  outputs/ft/stoch_rsi_equity.csv
  outputs/ft/stoch_rsi_metrics.json
  outputs/ft/stoch_rsi_risk_events.json
  outputs/ft/stoch_rsi_trades.csv
```

Lectura, orden por orden:

1. **`synth`** guarda `data/processed/BTCUSDT_1h.parquet` y su `.meta.json` con
   `"synthetic": true`. El mensaje recuerda que no sirve para evaluar rentabilidad.
2. **`validate-data`** imprime un informe JSON (duplicados, huecos, velas inválidas,
   alineación) y devuelve 0 porque los datos son válidos.
3. **`backtest`** usa por defecto el segmento de **entrenamiento**. Las métricas coinciden con
   las del Módulo XII (sección 12.9): es la misma simulación.
4. **`compare`** imprime la tabla de validación (neta) de los 16 candidatos y los tres
   benchmarks. `NaN` en el Sharpe significa "no calculado" (pocas operaciones, Módulo XII). La
   selección coincide con la del Módulo XIII (sección 13.5).
5. **Primer `final-test`**: código 0; evalúa los tres seleccionados en el test.
6. **Segundo `final-test`**: código 3 y el mensaje de la guarda.
7. **`report`** regenera `report.html` en el directorio del backtest.

---

## 15.5 Archivos generados y para qué sirve cada uno

| Archivo | Orden | Contenido |
|---|---|---|
| `data/processed/<SÍMBOLO>_<tf>.parquet` | synth, download, import | Velas OHLCV |
| `data/processed/<SÍMBOLO>_<tf>.meta.json` | idem | Origen, rango, peticiones, calidad, `synthetic` |
| `data/processed/<SÍMBOLO>_funding.parquet` | download `--funding` | Serie de funding |
| `outputs/experiments.jsonl` | todas las que simulan | Registro append-only (Módulo XIII) |
| `equity.csv`, `trades.csv` | backtest, final-test | Equity por vela y operaciones |
| `metrics.json` | backtest, final-test | Todas las métricas (Módulo XII) |
| `risk_events.json`, `run.json` | backtest (y `*_risk_events.json` en final-test) | Eventos de riesgo; datos para regenerar el informe |
| `metadata.json` | todas las que simulan | Reproducibilidad (sección 15.6) |
| `summary.csv` | compare | Una fila por candidato × segmento × neto/bruto |
| `selection.json` | compare | La selección congelada (entrada de `final-test`) |
| `statistics.json` | compare | DSR, Holm, bootstrap, dependencia |
| `signal_correlation_train.csv` | compare | Correlación de señales en entrenamiento |
| `windows.csv`, `in_sample_grid.csv`, `oos_trades.csv`, `oos_equity.csv`, `summary.json` | walkforward | Ventanas y resultados fuera de muestra |
| `grid.csv`, `stability.json` | sensitivity | Rejilla y estabilidad |
| `matrix.csv`, `consistency.csv` | markets | Métricas por mercado y consistencia |
| `report.html` | todas salvo sensitivity | Informe autocontenido (gráficos incrustados en base64) |

Sin `--out`, cada orden crea `outputs/<orden>_<símbolo>_<tf>[_<estrategia>]_<fecha UTC>`
(`_out_dir`, líneas 110–118): las ejecuciones no se sobrescriben.

---

## 15.6 Metadatos de reproducibilidad

<!-- cita: src/bybit_quant_lab/reporting/metadata.py#L43-L67 -->
`src/bybit_quant_lab/reporting/metadata.py` · líneas 43–67

```python
def build_metadata(
    config: AppConfig,
    data_hash: str,
    data_meta: dict[str, Any] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Metadatos completos del experimento."""
    meta = data_meta or {}
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "package_version": __version__,
        "git": git_info(Path(__file__).resolve().parent),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "data_hash": data_hash,
        "data_source": meta.get("source", "desconocido"),
        "data_synthetic": bool(meta.get("synthetic", False)),
        "data_rows": meta.get("rows"),
        "data_range": [meta.get("start"), meta.get("end")],
        "config_hash": config_hash(config),
        "config": config.model_dump(mode="json"),
        "seed": config.backtest.seed,
        "disclaimer": DISCLAIMER,
        **(extra or {}),
    }
```

Con `metadata.json` se puede saber **exactamente** qué produjo un resultado: commit de Git (y si
había cambios sin confirmar, `dirty`), versión de Python, hash de los datos, si eran sintéticos,
configuración completa y su hash, y semilla.

**[Hecho] El hash de configuración incluye las rutas.** `config_hash` serializa toda la
configuración, incluidas `data.data_dir` y `output_dir`. Consecuencia verificada: un
`final-test` lanzado con un `--output-dir` (o `--data-dir`) distinto del usado en `compare` se
rechaza con "La configuración actual difiere de la usada en la selección". Esto tiene un efecto
protector: cambiar de directorio de salida para esquivar el registro de experimentos no
funciona con la misma selección. **[Discrepancia]** `docs/audit_report.md` (sección 7, punto 5)
dice que con otro `--output-dir` "la guarda no puede detectarlo"; con la selección original el
hash lo impide. Sí sigue siendo cierto que **borrar** `experiments.jsonl` elimina la memoria de
la guarda.

---

## 15.7 Leer los informes HTML

Secciones del informe de `backtest` (`reporting/html.py`, líneas 108–220):

1. **Resumen ejecutivo**: resultado neto, comparación con los benchmarks y advertencias.
2. **Parámetros** de la estrategia.
3. **Métricas de rendimiento y riesgo**, con **neto frente a bruto** y benchmarks: si el bruto
   es positivo y el neto negativo, la estrategia no supera sus costes.
4. **Curva de equity y drawdown.**
5. **Distribución de retornos** por operación.
6. **Costes y funding.**
7. **Desgloses** por dirección, motivo de salida y régimen (Módulo XII).
8. **Eventos de riesgo y señales rechazadas.**
9. **Tabla de operaciones.**

El informe de `compare` añade segmentos, resultados por segmento, bruto frente a neto,
redundancia (con el texto desactualizado sobre los umbrales, Módulo IX), y la sección
"Selección y validación estadística" con DSR, bootstrap y dependencia. El de `final-test` marca
el resultado como no independiente si se forzó con `--allow-repeat`.

**Orden de lectura recomendado:** advertencias → número de operaciones → neto frente a bruto →
drawdown → controles estadísticos (en `compare`) → solo entonces el Sharpe o el beneficio.

---

## 15.8 Flujo de trabajo recomendado

**Ahora (datos sintéticos):** sirve para aprender la herramienta y comprobar la lógica, no para
evaluar estrategias.

**Con datos reales** (cuando haya conectividad; pasos de `docs/audit_report.md`, sección 8):

```bash
# 1. Comprobar conectividad con la API pública (sin credenciales)
curl -sS "https://api.bybit.com/v5/market/time"
# 2. Descargar velas y funding
bql download --symbol BTCUSDT --timeframe 1h --start 2022-01-01 --end 2025-01-01 --funding
# 3. Validar y revisar huecos
bql validate-data --symbol BTCUSDT --timeframe 1h
# 4. Explorar SOLO en entrenamiento
bql backtest --symbol BTCUSDT --timeframe 1h --strategy ema_crossover --segment train
bql sensitivity --symbol BTCUSDT --timeframe 1h --strategy ema_crossover --segment train
# 5. Comparar y seleccionar (validación)
bql compare --symbol BTCUSDT --timeframe 1h
# 6. Revisar statistics.json y el informe; decidir si la selección merece el test
# 7. Una única vez
bql final-test --selection outputs/compare_BTCUSDT_1h_<fecha>/selection.json
```

Reglas prácticas:

- Decide **antes** de mirar validación cuántas variantes vas a probar.
- No uses `--segment full` ni `--allow-repeat` para tomar decisiones.
- Conserva `outputs/experiments.jsonl`: es la memoria de cuántas pruebas has hecho.
- Si cambias costes, riesgo o segmentos después de `compare`, la selección deja de ser válida
  (el hash lo detecta): vuelve a ejecutar `compare`.

---

## 15.9 Errores frecuentes al usar la CLI

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `Error: No existe data/processed/...parquet` | No hay datos para ese símbolo/temporalidad | `synth`, `download` o `import` antes |
| `Datos inválidos en ...` | El dataset no pasa la validación | `bql validate-data` y revisar |
| Resultados distintos a los esperados sin error | Ejecutado fuera de `bybit-quant-lab/` (sin YAML) | `cd bybit-quant-lab` |
| `La configuración actual difiere...` | Cambió algo de la configuración (o las rutas) | Repetir `compare` |
| Código 3 en `final-test` | El test ya se evaluó | Es intencionado (Módulo XIII) |
| `No hay rejilla para ...` | La estrategia no tiene `grids` en el YAML | Pasar `--grid '{"param": [...]}'` |
| `CONNECT tunnel failed, response 403` | Proxy o red que bloquea `api.bybit.com` | Problema del entorno, no del código (Módulo IV) |

### Comprobación final del módulo

Ejecutas `bql compare` desde la carpeta raíz del repositorio (no desde `bybit-quant-lab/`), con
`--data-dir bybit-quant-lab/data`. ¿Qué configuración y qué combinaciones se usan?

<details><summary>Ver respuesta</summary>

`configs/default.yaml` y `configs/strategies.yaml` no existen en el directorio actual, así que
se usan los valores por defecto del código (que coinciden con el YAML en costes y riesgo, pero
no tiene por qué ser siempre así), los parámetros por defecto de cada estrategia y **una sola
combinación**, `vote_all` con política `veto`. No se muestra ningún aviso. La solución es
ejecutar desde `bybit-quant-lab/` o pasar `--config` y `--strategies-config` explícitos.
</details>
