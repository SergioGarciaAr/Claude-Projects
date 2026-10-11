# Módulo XIV. Pruebas, calidad del código y depuración

Un backtest no da error cuando está mal: da un número. Por eso las pruebas automáticas son la
única forma razonable de confiar en que el código hace lo que dice. Este módulo explica cómo
están organizadas las 231 pruebas del proyecto, qué técnicas usan, cómo se ejecutan las
herramientas de calidad y cómo depurar un resultado sospechoso.

---

## 14.1 Qué es una prueba y qué tipos hay en el proyecto

**Prueba automática:** una función que ejecuta un trozo de código con datos conocidos y
**comprueba** (`assert`) que el resultado es el esperado. Si no lo es, falla y lo dice.

| Tipo | Qué comprueba | Ejemplo en el proyecto |
|---|---|---|
| Unitaria | Una función aislada | `test_holm_step_down_by_hand` |
| De integración | Varias piezas juntas, como las usa un usuario | `tests/integration/test_cli_pipeline.py` (la CLI completa) |
| Calculada a mano | El resultado contra una aritmética independiente | `test_short_trade_with_fees_slippage_and_funding_by_hand` |
| De propiedad | Una regla que debe cumplirse para cualquier dato | `test_no_lookahead_truncation` (diez estrategias) |
| Contra referencia | Implementación vectorizada contra un bucle simple | `test_audit_indicators.py` |
| Estadística | Calibración por simulación | `test_psr_is_calibrated_under_null` |
| De regresión | Que un error corregido no vuelva | `test_walk_forward_never_uses_test_segment` |
| De contrato | Que la salida tiene la forma prometida | `test_output_contract` |

Funciones de prueba por archivo (con `@pytest.mark.parametrize`, una función genera varias
pruebas; el total ejecutado es 231):

| Archivo | Funciones | Tema |
|---|---|---|
| `tests/unit/test_strategies.py` | 27 | Estrategias, no look-ahead, contrato |
| `tests/unit/test_audit_statistics.py` | 14 | DSR, Holm, bootstrap, fugas de validación |
| `tests/unit/test_engine.py` | 13 | Motor |
| `tests/unit/test_indicators.py` | 13 | Indicadores |
| `tests/unit/test_data.py` | 12 | Cliente de Bybit (simulado), descarga, validación |
| `tests/unit/test_risk.py` | 11 | Dimensionamiento y límites |
| `tests/unit/test_signals.py` | 10 | Combinación, régimen, redundancia |
| `tests/unit/test_validation.py` | 10 | Separación, walk-forward, benchmarks |
| `tests/unit/test_audit_engine.py` | 9 | Operaciones a mano y bordes |
| `tests/unit/test_audit_indicators.py` | 9 | Indicadores contra bucles |
| `tests/unit/test_audit_data.py` | 5 | Forma de las peticiones, funding, CLI documentada |
| `tests/integration/test_cli_pipeline.py` | 7 | Flujo completo de la CLI |

---

## 14.2 pytest en cinco piezas

**1. `assert`.** Si la condición es falsa, la prueba falla y pytest muestra los valores.

**2. Fixtures.** Datos o recursos que pytest crea y pasa a las pruebas que los piden por
nombre:

<!-- fmt: off -->
<!-- cita: tests/conftest.py#L14-L17 -->
`tests/conftest.py` · líneas 14–17

```python
@pytest.fixture(scope="session")
def synth() -> pd.DataFrame:
    """3000 velas de 1h sintéticas (semilla fija)."""
    return generate_synthetic_ohlcv(bars=3000, timeframe="1h", seed=7)
```
<!-- fmt: on -->

`scope="session"` crea la serie una vez para toda la ejecución. Una prueba que declara
`synth` como parámetro la recibe. `tmp_path` (incorporada en pytest) da un directorio temporal
distinto para cada prueba: así ninguna prueba escribe en `outputs/` real.

**3. Parametrización.** Una función, muchas pruebas:

<!-- fmt: off -->
<!-- cita: tests/unit/test_strategies.py#L44-L50 -->
`tests/unit/test_strategies.py` · líneas 44–50

```python
@pytest.mark.parametrize("name", ALL)
def test_no_lookahead_truncation(name: str, synth: pd.DataFrame) -> None:
    strat = create_strategy(name)
    full = strat.generate_signals(synth)
    for t in (400, 1100, 2203):
        part = strat.generate_signals(synth.iloc[: t + 1])
        pd.testing.assert_frame_equal(full.iloc[: t + 1], part, check_freq=False)
```
<!-- fmt: on -->

`ALL` es la lista de las diez estrategias: esta función genera diez pruebas.

**4. `pytest.approx`.** Compara números en coma flotante con tolerancia (Módulo II):
`0.1 + 0.2 == 0.3` es `False`, pero `0.1 + 0.2 == pytest.approx(0.3)` es `True`.

**5. `pytest.raises`.** Comprueba que algo **falla** como debe:
`with pytest.raises(FinalTestAlreadyEvaluatedError): ...`.

**Configuración** (`pyproject.toml`):

<!-- cita: pyproject.toml#L66-L69 -->
`pyproject.toml` · líneas 66–69

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
filterwarnings = ["error::FutureWarning"]
```

- `testpaths`: dónde buscar pruebas.
- `addopts = "-q"`: salida resumida por defecto. **Ojo:** si además se escribe `pytest -q`, el
  nivel pasa a `-qq` y desaparece la línea final con el recuento. Para verla, ejecuta `pytest`
  sin `-q`.
- `filterwarnings = ["error::FutureWarning"]`: cualquier `FutureWarning` (avisos de pandas sobre
  comportamientos que cambiarán) **hace fallar** la prueba. Así se detectan pronto los usos que
  romperían con la siguiente versión de pandas.

---

## 14.3 Técnica clave: probar la ausencia de look-ahead

**Idea.** Si la señal en `t` solo usa datos hasta `t`, entonces:

1. **Truncar** la serie después de `t` no cambia ninguna señal hasta `t`.
2. **Alterar** los datos posteriores a `t` no cambia ninguna señal hasta `t`.

<!-- fmt: off -->
<!-- cita: tests/unit/test_strategies.py#L53-L65 -->
`tests/unit/test_strategies.py` · líneas 53–65

```python
@pytest.mark.parametrize("name", ALL)
def test_no_lookahead_future_perturbation(name: str, synth: pd.DataFrame) -> None:
    strat = create_strategy(name)
    t = 1500
    altered = synth.copy()
    rng = np.random.default_rng(0)
    factor = np.exp(np.cumsum(rng.normal(0, 0.05, len(synth) - t - 1)))
    for col in ("open", "high", "low", "close"):
        altered.iloc[t + 1 :, altered.columns.get_loc(col)] *= factor
    altered.iloc[t + 1 :, altered.columns.get_loc("volume")] *= 10
    a = strat.generate_signals(synth).iloc[: t + 1]
    b = strat.generate_signals(altered).iloc[: t + 1]
    pd.testing.assert_frame_equal(a, b)
```
<!-- fmt: on -->

Demostración con un indicador correcto y uno "tramposo" que usa una media centrada (mira 10
velas hacia delante):

<!-- ejecutar -->
```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.indicators import sma

datos = generate_synthetic_ohlcv(bars=500, seed=1)


def causal(d):
    return (d["close"] > sma(d["close"], 20)).astype(int)


def tramposa(d):
    return (d["close"] > d["close"].rolling(21, center=True).mean()).astype(int)


t = 300
for nombre, f in (("causal", causal), ("tramposa", tramposa)):
    completa = f(datos).iloc[: t + 1]
    truncada = f(datos.iloc[: t + 1])
    print(f"{nombre:9s} velas distintas al truncar: {int((completa != truncada).sum())}")
```
<!-- salida -->
```text
causal    velas distintas al truncar: 0
tramposa  velas distintas al truncar: 5
```

La versión tramposa cambia en las últimas velas antes del corte: allí, con la serie completa, la
media "veía" el futuro; con la serie truncada no puede. Un backtest con esa señal parecería
excelente y sería imposible de reproducir en tiempo real.

**[Limitación]** La prueba comprueba tres puntos de corte (400, 1100, 2203) y una perturbación
en 1500. No es una demostración formal para todo `t`, pero detecta los errores habituales
(`shift(-1)`, `center=True`, `bfill`, normalizar con estadísticas de toda la serie).

---

## 14.4 Técnica clave: dobles de prueba para la API de Bybit

Las pruebas no pueden depender de internet (y en este entorno, Bybit está bloqueada). El
cliente recibe sus dependencias desde fuera (**inyección de dependencias**):

<!-- fmt: off -->
<!-- cita: tests/unit/test_data.py#L36-L49 -->
`tests/unit/test_data.py` · líneas 36–49

```python
class FakeExchange:
    """Simula /v5/market/kline (lista en orden descendente, como Bybit) y funding."""

    def __init__(self, failures: list[Any] | None = None) -> None:
        self.failures = list(failures or [])
        self.calls: list[dict[str, Any]] = []

    def get(self, url: str, params: dict[str, Any], timeout: float) -> FakeResponse:
        self.calls.append({"url": url, **params})
        if self.failures:
            f = self.failures.pop(0)
            if isinstance(f, Exception):
                raise f
            return f
```
<!-- fmt: on -->

<!-- fmt: off -->
<!-- cita: tests/unit/test_data.py#L90-L97 -->
`tests/unit/test_data.py` · líneas 90–97

```python

def _client(fake: FakeExchange) -> BybitPublicClient:
    return BybitPublicClient(
        session=fake,
        sleep=lambda _: None,
        backoff_seconds=0,
        min_request_interval=0,
        clock=lambda: NOW,
```
<!-- fmt: on -->

- `session=fake`: en lugar de `requests.Session`, un objeto con un método `get` que devuelve
  respuestas fabricadas con el formato de Bybit (lista en orden descendente, `retCode`).
- `sleep=lambda _: None`: los reintentos no esperan de verdad.
- `clock=lambda: NOW`: el "ahora" es fijo, así que la detección de la vela no cerrada es
  reproducible.

Con esto se prueban reintentos, errores HTTP, `retCode` distintos de 0, respuestas mal formadas
y paginación (Módulo IV). **[Hecho]** Lo que estos dobles **no** pueden probar es que la API
real se comporte como se supone (`docs/audit_report.md`, sección 5).

---

## 14.5 Evidencia: las pruebas de la auditoría fallaban antes de las correcciones

Una prueba de regresión solo demuestra algo si **falla** con el código erróneo. Para este curso
se reprodujo esa evidencia: la suite actual se ejecutó contra el código de `fc4e578` (anterior a
la auditoría) en un `git worktree` temporal, fuera del repositorio.

Procedimiento (no modifica el repositorio; `$TMP` es un directorio temporal cualquiera):

```bash
git worktree add --detach "$TMP/wt" fc4e578
rm -rf "$TMP/wt/bybit-quant-lab/tests"
cp -r bybit-quant-lab/tests "$TMP/wt/bybit-quant-lab/tests"
cd "$TMP/wt/bybit-quant-lab"
PYTHONPATH=src:. /ruta/al/.venv/bin/python -m pytest -o addopts="" -q
# ...
git worktree remove --force "$TMP/wt"
```

`test_audit_statistics.py` importa `psr_from_moments`, que no existía en `fc4e578`; para poder
ejecutarlo, en la copia temporal esa única función se cargó desde la versión actual (las
funciones bajo prueba siguen siendo las antiguas). Resultado:

| Archivo | Fallan | Pasan |
|---|---|---|
| Todos salvo `test_audit_statistics.py` | 3 | 214 |
| `test_audit_statistics.py` | 8 | 6 |
| **Total** | **11** | **220** |

Las 11 que fallan, una por hallazgo:

| Prueba | Hallazgo |
|---|---|
| `test_funding_pagination_stops_if_api_does_not_advance` | M-03 |
| `test_gap_through_liquidation_loses_isolated_margin_only` | M-02 |
| `test_no_spurious_entry_when_atr_warmup_exceeds_indicator_warmup` | M-04 |
| `test_walk_forward_never_uses_test_segment` | A-01 |
| `test_final_test_period_can_only_be_used_once` | A-02 |
| `test_final_test_uses_frozen_member_params` | A-03 |
| `test_final_test_rejects_changed_config` | A-03 |
| `test_combination_thresholds_not_tuned_on_validation` | M-01 |
| `test_configured_combinations_are_not_equivalent` | B-01 |
| `test_random_benchmark_calibrated_only_on_simulated_segment` | B-02 |
| `test_walk_forward_flags_windows_without_valid_selection` | B-03 |

Las 220 restantes pasan también con el código antiguo: son pruebas de comportamiento que ya era
correcto (cálculos a mano, indicadores contra bucles, DSR), y confirman que las correcciones no
cambiaron lo que funcionaba.

---

## 14.6 Ejecutar las pruebas

```bash
cd bybit-quant-lab
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pytest                              # toda la suite (~20 s)
pytest tests/unit/test_risk.py      # un archivo
pytest -k "lookahead"               # pruebas cuyo nombre contiene "lookahead"
pytest -x                           # parar en el primer fallo
pytest --durations=5                # las cinco más lentas
```

Ejecución desde Python de un archivo concreto (se muestra solo el recuento, sin el tiempo):

<!-- ejecutar -->
```python
import re
import subprocess
import sys

salida = subprocess.run(
    [
        sys.executable,
        "-m",
        "pytest",
        "-o",
        "addopts=",
        "-q",
        "-p",
        "no:cacheprovider",
        "tests/unit/test_risk.py",
        "tests/unit/test_signals.py",
    ],
    capture_output=True,
    text=True,
    check=False,
).stdout
print(re.sub(r" in [\d.]+s", "", salida.strip().splitlines()[-1]))
```
<!-- salida -->
```text
24 passed
```

---

## 14.7 Calidad estática: ruff y mypy

<!-- cita: pyproject.toml#L42-L64 -->
`pyproject.toml` · líneas 42–64

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP", "N", "SIM", "RUF", "PL"]
ignore = ["PLR0913", "PLR0917", "PLW0603", "PLR2004", "PLR0911", "PLR0912", "PLR0915", "RUF001", "RUF002", "RUF003"]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["PLR2004", "N802", "N806", "PLC0415"]

[tool.mypy]
python_version = "3.11"
strict = false
warn_unused_ignores = true
warn_redundant_casts = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
ignore_missing_imports = true
plugins = ["pydantic.mypy"]
```

**ruff** (linter y formateador):

- `line-length = 100`.
- Reglas activadas: `E`/`W` (estilo PEP 8), `F` (errores como variables sin usar), `I` (orden
  de importaciones), `B` (errores probables), `UP` (sintaxis moderna), `N` (nombres), `SIM`
  (simplificaciones), `RUF` y `PL` (Pylint).
- Se ignoran, por ejemplo, `PLR2004` (números "mágicos") y `RUF001–003` (caracteres
  ambiguos, necesarios en textos en castellano).

**mypy** (comprobación de tipos, Módulo II sección 2.14):

- `disallow_untyped_defs`: toda función debe tener anotaciones.
- `plugin pydantic.mypy`: entiende los modelos de Pydantic.

```bash
ruff check .            # errores de estilo y probables
ruff format --check .   # formato (sin modificar)
mypy src                # tipos
```

**[Hecho]** En la versión actual: `ruff check .` → "All checks passed!"; `mypy src` → "Success:
no issues found in 62 source files"; `pytest` → 231 pruebas superadas (sección 14.10).

---

## 14.8 Depurar un resultado sospechoso

**Método general:**

1. **Reproducir en pequeño.** Construye el caso mínimo con `make_bars` y `manual_signals`
   (`tests/conftest.py`), como en los Módulos X y XI. Diez velas bastan para casi cualquier
   duda sobre el motor.
2. **Mirar las tablas intermedias.** `res.equity` (vela a vela), `res.trades` (con
   `exit_reason`, `fees`, `slippage_cost`, `funding`), `res.rejected_signals` y
   `res.risk_events`.
3. **Comprobar la identidad contable.**
   `net_pnl == gross_pnl − slippage_cost − fees − funding` en cada operación.
4. **Comprobar el contrato temporal.** Para cada operación, `signal[entry_bar − 1]` debe ser el
   lado de la operación y `entry_price ≈ open[entry_bar] · (1 ± deslizamiento)`.
5. **Detener la ejecución.** `breakpoint()` en una copia local del código abre el depurador
   `pdb` en esa línea (`n` siguiente línea, `p variable` imprime, `c` continúa).
6. **Leer el traceback de abajo arriba** (Módulo II, sección 2.20).

**Errores típicos en este tipo de código:**

| Síntoma | Causa probable | Dónde mirar |
|---|---|---|
| Resultados demasiado buenos | Look-ahead (`shift(-1)`, `center=True`, `bfill`) | Sección 14.3 |
| Señales desplazadas una vela | `shift` en el sentido equivocado | Módulo V |
| `NaN` que se propagan | Calentamiento de indicadores | Módulo VII |
| Fechas desalineadas | Zona horaria o resolución del índice | Módulos IV y XI (sección 11.6) |
| Una asignación "no hace nada" | Asignación encadenada con pandas 3 | Abajo |
| Sharpe enorme | Muy pocas velas u operaciones | Módulo XII |

**Asignación encadenada en pandas 3.** Con *Copy-on-Write*, `df[filtro]["col"] = valor`
modifica una copia temporal y se pierde:

<!-- ejecutar -->
```python
import warnings

import pandas as pd

df = pd.DataFrame({"x": [1, -1, 2], "y": [0, 0, 0]})
with warnings.catch_warnings(record=True) as avisos:
    warnings.simplefilter("always")
    df[df["x"] > 0]["y"] = 1  # encadenada: no modifica df
print("encadenada:", df["y"].tolist(), [type(a.message).__name__ for a in avisos])
df.loc[df["x"] > 0, "y"] = 1  # correcta: una sola operación .loc
print("con .loc:  ", df["y"].tolist())
```
<!-- salida -->
```text
encadenada: [0, 0, 0] ['ChainedAssignmentError']
con .loc:   [1, 0, 1]
```

**Registro (logging).** `src/bybit_quant_lab/logging_utils.py` configura el registro y la CLI
acepta `--log-level DEBUG`. **[Hecho]** En la versión actual solo hay cuatro llamadas de
registro en `src` (guardado de datos, descarga y reintentos del cliente); el motor y las
estrategias no registran nada. Para depurarlos sirven las tablas del resultado.

---

## 14.9 Lo que las pruebas no garantizan

- **Que la API real se comporte como los dobles de prueba.** Pendiente de conectividad.
- **Que los supuestos sean realistas** (deslizamiento, comisiones, liquidación). Las pruebas
  verifican que el código aplica los supuestos, no que acierten.
- **Que una estrategia gane dinero.** Ninguna prueba evalúa rentabilidad, y no debería.
- **Que la documentación esté al día.** La cabecera de `research.py` y el texto del informe
  HTML sobre los umbrales quedaron desactualizados sin que ninguna prueba lo detectara
  (Módulo IX, sección 9.6). Solo la sintaxis de las órdenes documentadas se prueba
  (`test_every_documented_cli_command_parses`).

---

## 14.10 Estado verificado de la suite

Ejecutado al redactar este módulo, en la rama del proyecto:

```text
pytest              -> 231 passed
ruff check .        -> All checks passed!
mypy src            -> Success: no issues found in 62 source files
```

### Comprobación final del módulo

Escribes una estrategia nueva y su backtest da un Sharpe de 9 en validación. ¿Qué dos pruebas
de este módulo ejecutarías primero y por qué?

<details><summary>Ver respuesta</summary>

1. Las de **no look-ahead** (truncamiento y perturbación del futuro), añadiendo la estrategia a
   la parametrización: un Sharpe tan alto es el síntoma típico de usar información futura.
2. La comprobación del **contrato temporal** de las operaciones (sección 14.8, punto 4): que
   cada entrada se ejecuta en la apertura siguiente a una transición de la señal.

Si ambas pasan, el siguiente paso es estadístico: número de operaciones, DSR, Holm y
dependencia de las mejores operaciones (Módulo XIII).
</details>
