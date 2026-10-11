# Módulo III. Arquitectura e ingeniería de software

Un programa pequeño cabe en la cabeza. Uno de 6.500 líneas no: necesita una **arquitectura**, es
decir, una forma de dividirse en partes para que cada una pueda entenderse, probarse y cambiarse
sin romper las demás. Este módulo explica la arquitectura **real** del proyecto, sus aciertos y
sus puntos débiles.

---

## 3.1 Separación de responsabilidades

### La idea

Cada parte del programa debe tener **una sola razón para cambiar**. Si el modelo de comisiones de
Bybit cambia, solo debería cambiar el código de costes; si se inventa una estrategia nueva, solo
debería añadirse un archivo de estrategia.

En términos técnicos esto se llama **principio de responsabilidad única** (Single Responsibility
Principle). En el proyecto se ve en la tabla de directorios del Módulo I (sección 1.9) y en
detalles como estos:

| Pregunta | La responde | Y nadie más |
|---|---|---|
| ¿Qué exposición quiero? | La estrategia (`generate_signals`) | El motor no decide señales |
| ¿Cuánto compro? | `risk/sizing.py` (`size_position`) | La estrategia no decide tamaños |
| ¿A qué precio se ejecuta? | `execution/` (`CostModel`, `check_gap_exit`, `check_intrabar_exit`) | El motor solo aplica el resultado |
| ¿Puedo abrir otra operación? | `risk/limits.py` (`RiskManager.can_open`) | Las estrategias no conocen los límites diarios |
| ¿Cómo de bueno fue? | `analytics/metrics.py` | El motor no calcula Sharpe |

### Comprobación

Si quisieras simular comisiones distintas para órdenes límite (maker), ¿qué archivos tocarías?

<details><summary>Ver respuesta</summary>

`execution/costs.py` ya sabe calcular comisiones maker (`fee(..., taker=False)`), pero el motor
(`backtesting/engine.py`) siempre pide la comisión taker porque solo simula órdenes a mercado.
Habría que cambiar el motor para que distinga el tipo de orden. Las estrategias no se tocarían.
</details>

---

## 3.2 Acoplamiento y cohesión

### La idea

- **Cohesión:** cuánto tienen que ver entre sí las cosas que están **dentro** de un módulo. Alta
  cohesión es buena: `indicators/core.py` solo contiene cálculos de indicadores.
- **Acoplamiento:** cuánto depende un módulo de **otros**. Bajo acoplamiento es bueno: si un
  módulo conoce pocos detalles de los demás, puedes cambiarlos sin romperlo.

Analogía: un enchufe estándar. La lámpara (estrategia) no necesita saber cómo se genera la
electricidad (el motor). Solo necesita que el enchufe tenga la forma acordada (el contrato de
señales).

### El contrato que desacopla estrategias y motor

El único acuerdo entre estrategias y motor son **cinco columnas** con significado fijo:

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/strategies/base.py#L36-L42 -->
`src/bybit_quant_lab/strategies/base.py` · líneas 36–42

```python
SIGNAL_COLUMNS: tuple[str, ...] = (
    "signal",
    "conviction",
    "stop_distance",
    "take_profit_distance",
    "trailing_distance",
)
```
<!-- fmt: on -->

El motor comprueba ese contrato al empezar y falla de inmediato si no se cumple:

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L246-L256 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 246–256

```python
    @staticmethod
    def _check_inputs(data: pd.DataFrame, signals: pd.DataFrame) -> None:
        missing = [c for c in SIGNAL_COLUMNS if c not in signals.columns]
        if missing:
            raise ValueError(f"Faltan columnas de señal: {missing}")
        if not data.index.equals(signals.index):
            raise ValueError("Las señales deben tener exactamente el mismo índice que los datos")
        if data.empty:
            raise ValueError("No hay datos para simular")
        if data[["open", "high", "low", "close"]].isna().any().any():
            raise ValueError("Los datos contienen precios NaN; límpialos antes de simular")
```
<!-- fmt: on -->

Gracias a este contrato, **una combinación de estrategias** (Módulo IX) devuelve las mismas
cinco columnas y el motor no necesita saber si recibe una estrategia o una votación de diez.

---

## 3.3 Capas y flujo de dependencias

### La idea

Las piezas se organizan en **capas**: las de abajo ofrecen servicios básicos y las de arriba los
combinan. Una regla sana es que **las dependencias apunten hacia abajo**: los módulos básicos no
deben importar módulos de alto nivel. Si dos módulos se importan mutuamente (un **ciclo**),
ninguno puede entenderse ni probarse por separado.

En lugar de dibujar el diagrama de memoria, este programa lo **extrae del código**: lee cada
archivo, encuentra sus `import` y anota qué subpaquete usa a cuál.

<!-- ejecutar -->
```python
import ast
import pathlib

raiz = pathlib.Path("src/bybit_quant_lab")
deps = {}
for archivo in raiz.rglob("*.py"):
    partes = archivo.relative_to(raiz).parts
    origen = (
        partes[0].removesuffix(".py") if len(partes) > 1 or partes[0] != "__init__.py" else "(raíz)"
    )
    for nodo in ast.walk(ast.parse(archivo.read_text(encoding="utf-8"))):
        if (
            isinstance(nodo, ast.ImportFrom)
            and nodo.module
            and nodo.module.startswith("bybit_quant_lab.")
        ):
            destino = nodo.module.split(".")[1]
            if destino != origen:
                deps.setdefault(origen, set()).add(destino)
for origen in sorted(deps):
    print(f"{origen:12s} -> {', '.join(sorted(deps[origen]))}")


def tiene_ciclo():
    def visita(n, camino):
        if n in camino:
            return camino[camino.index(n) :] + [n]
        for m in deps.get(n, ()):
            ciclo = visita(m, camino + [n])
            if ciclo:
                return ciclo
        return None

    for n in deps:
        ciclo = visita(n, [])
        if ciclo:
            return ciclo
    return None


print("ciclos entre subpaquetes:", tiene_ciclo())
```
<!-- salida -->
```text
analytics    -> backtesting, timeframes
backtesting  -> config, execution, portfolio, risk, strategies
cli          -> analytics, backtesting, config, data, logging_utils, reporting, signals, strategies, timeframes, validation
data         -> logging_utils, timeframes
execution    -> config
reporting    -> analytics, backtesting, config
risk         -> config
signals      -> indicators, strategies
strategies   -> indicators
validation   -> analytics, backtesting, config, data, execution, logging_utils, signals, strategies, timeframes
ciclos entre subpaquetes: None
```

**[Hecho]** No hay ciclos entre subpaquetes. Las capas, de abajo arriba, son:

1. **Base:** `timeframes`, `logging_utils`, `config` (no importan nada del proyecto salvo entre
   ellos).
2. **Datos y cálculo:** `data`, `indicators`.
3. **Dominio:** `strategies` (usa `indicators`), `execution`, `risk`, `portfolio`.
4. **Simulación:** `backtesting` (usa dominio, ejecución y riesgo).
5. **Análisis:** `analytics`, `signals`, `validation` (usan la simulación).
6. **Presentación:** `reporting` y `cli` (usan todo lo anterior).

Observa que `strategies` no aparece apuntando a `backtesting`: las estrategias no conocen el
motor, como prometía el Módulo I.

---

## 3.4 Diseño de interfaces entre módulos

### La idea

Una **interfaz** es "lo que un módulo promete a los demás": qué funciones ofrece, qué reciben y
qué devuelven. Una buena interfaz es **pequeña** y **estable**: puedes cambiar todo lo de dentro
sin que nadie lo note.

Interfaces principales del proyecto:

| Interfaz | Archivo | Qué promete |
|---|---|---|
| `Strategy.generate_signals(data)` | `strategies/base.py` | Una tabla con las cinco columnas de señal y el mismo índice que `data` |
| `create_strategy(nombre, params)` | `strategies/registry.py` | Una estrategia validada a partir de su nombre |
| `BacktestEngine(...).run(data, signals, ...)` | `backtesting/engine.py` | Un `BacktestResult` con equity, operaciones y eventos |
| `compute_metrics(result)` | `analytics/metrics.py` | Un diccionario de métricas con advertencias |
| `combine_signals(frames, categories, config, regime)` | `signals/combiners.py` | Una tabla de señales con el mismo contrato |
| `HTTPSession` (Protocol) | `data/bybit_client.py` | Cualquier objeto con `get(url, params, timeout)` |
| `FundingSource`, `OpenInterestSource`, `QuoteSource`, `TradeSource` (Protocols) | `data/interfaces.py` | Contratos para fuentes de datos futuras |

**[Hecho]** Las cuatro interfaces de `data/interfaces.py` existen como contrato, pero solo
`FundingSource` tiene una implementación real (el cliente de Bybit). Las otras tres no las
implementa ni las usa ningún archivo. Son **diseño anticipado**: definen cómo debería encajar una
fuente futura, sin fingir que los datos existen.

---

## 3.5 Configuración centralizada, YAML y variables de entorno

### La idea

Los números que quieres cambiar sin tocar el código (comisiones, riesgo por operación,
fracciones de entrenamiento...) se guardan en archivos de **configuración**. El proyecto usa
**YAML**, un formato de texto legible:

<!-- cita: configs/default.yaml#L17-L21 -->
`configs/default.yaml` · líneas 17–21

```yaml
costs:
  taker_fee: 0.00055                   # tarifa base publicada para perpetuos USDT (no VIP)
  maker_fee: 0.0002
  slippage_bps: 2.0
  use_funding: true                    # solo se aplica si hay funding descargado
```

- `clave: valor` define un dato; la indentación anida secciones (`costs` contiene `taker_fee`).
- `#` empieza un comentario.

Recorrido de la configuración:

1. `configs/default.yaml` se lee con `yaml.safe_load` en `config/loader.py`.
2. La CLI puede sobrescribir algunos valores (`--data-dir`, `--output-dir`).
3. Pydantic valida el resultado y crea un `AppConfig` **inmutable**.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/config/loader.py#L25-L35 -->
`src/bybit_quant_lab/config/loader.py` · líneas 25–35

```python
def load_config(
    path: str | Path | None = None, overrides: dict[str, Any] | None = None
) -> AppConfig:
    """Carga ``AppConfig`` desde YAML (o valores por defecto) aplicando ``overrides`` anidados."""
    raw: dict[str, Any] = _read_yaml(Path(path)) if path else {}
    for key, value in (overrides or {}).items():
        if isinstance(value, dict):
            raw.setdefault(key, {}).update(value)
        else:
            raw[key] = value
    return AppConfig.model_validate(raw)
```
<!-- fmt: on -->

`raw.setdefault(key, {}).update(value)` significa: "si la sección no existe, créala vacía; luego
mezcla en ella los valores nuevos". Así `--data-dir` cambia solo `data.data_dir` sin borrar el
resto de la sección `data`.

Y así construye la CLI esos valores a sobrescribir:

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/cli.py#L69-L78 -->
`src/bybit_quant_lab/cli.py` · líneas 69–78

```python
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
```
<!-- fmt: on -->

### Variables de entorno

Una **variable de entorno** es un valor que el sistema operativo pasa al programa (por ejemplo,
`BQL_LOG_LEVEL=DEBUG bql ...`). Son útiles para secretos (que nunca deben ir en archivos de Git)
y para ajustes que cambian entre máquinas.

**[Hecho] Discrepancia entre documentación y código:** `.env.example` documenta dos variables:

<!-- cita: .env.example#L1-L5 -->
`.env.example` · líneas 1–5

```text
# bybit-quant-lab no necesita credenciales: solo usa endpoints públicos de mercado.
# NUNCA coloques claves API privadas en este proyecto.
# Variables opcionales:
BQL_BYBIT_BASE_URL=https://api.bybit.com
BQL_LOG_LEVEL=INFO
```

Pero el código solo lee `BQL_LOG_LEVEL` (en `logging_utils.py`, línea 34). **Nadie lee
`BQL_BYBIT_BASE_URL`**: definirla no tiene ningún efecto. La URL de Bybit solo se cambia con
`data.base_url` en el YAML. Además, el proyecto no carga archivos `.env` automáticamente (no
depende de ninguna biblioteca para ello). Es una documentación engañosa que conviene corregir
(Módulo XVII).

### Comprobación

Quieres que todos los resultados se guarden en `/tmp/pruebas`. ¿Cómo lo harías sin editar
ningún archivo?

<details><summary>Ver respuesta</summary>

Con la opción global de la CLI, antes de la orden: `bql --output-dir /tmp/pruebas backtest ...`.
`_load_cfg` la convierte en un valor a sobrescribir antes de validar la configuración.
</details>

---

## 3.6 Validación temprana ("fail fast")

### La idea

Es mejor que un error de configuración detenga el programa **en el primer segundo** que
descubrirlo tras una hora de cálculos, o peor, no descubrirlo nunca y obtener resultados falsos.
Esto se llama **fallar pronto** (fail fast).

El proyecto valida en varios puntos de entrada:

| Punto | Qué valida | Dónde |
|---|---|---|
| Configuración | Rangos, tipos, campos desconocidos, relaciones entre campos | `config/models.py` (Pydantic) |
| Parámetros de estrategia | Lo mismo, por estrategia (`fast < slow`...) | Cada `*Params` en `strategies/` |
| Datos | Columnas, orden, duplicados, velas imposibles | `data/validation.py` |
| Contrato de señales | Columnas y alineación de índices | `BacktestEngine._check_inputs` |
| Argumentos de la CLI | Temporalidades y estrategias válidas | `argparse` (`choices=`) y `cli.main` |

<!-- ejecutar -->
```python
from pydantic import ValidationError

from bybit_quant_lab.config import load_config

configuracion = load_config("configs/default.yaml")
print(configuracion.risk.risk_per_trade, configuracion.execution.leverage)
try:
    load_config("configs/default.yaml", {"execution": {"leverage": 10}})
except ValidationError as error:
    print(error.errors()[0]["msg"])
```
<!-- salida -->
```text
0.01 3.0
Value error, execution.leverage=10.0 supera risk.max_leverage=5.0
```

---

## 3.7 Configuración que existe pero no tiene efecto

Una lección de ingeniería que este repositorio enseña **por sus defectos**: un campo de
configuración que el código nunca lee es peor que no tenerlo, porque el usuario cree que lo
controla.

**[Hecho]** Comprobado buscando cada nombre en `src/`:

| Elemento declarado | Dónde | Estado real |
|---|---|---|
| `execution.same_bar_policy` | `config/models.py`, línea 53 | Solo admite `"stop_first"` y el motor no lo lee: la regla está fija en `execution/fills.py`. Es documentación, no un interruptor. |
| `risk.max_open_positions` | `config/models.py`, línea 73 | Solo admite `1` y el motor no lo lee: el motor guarda una sola posición por diseño. |
| `data.symbols`, `data.timeframes` | `config/models.py`, líneas 25–26 | La CLI usa los argumentos `--symbol` y `--timeframe`, no estas listas. |
| `costs.maker_fee` | `config/models.py`, línea 43 | Se valida y se guarda, pero el motor solo cobra la comisión taker. |
| `BQL_BYBIT_BASE_URL` | `.env.example` | Ningún código lo lee. |
| `log_event` y el contexto `clave=valor` | `logging_utils.py` | Definidos, pero ninguna llamada los usa. |
| `Account.available_margin`, `Account.history`, `Position.notional_entry` | `portfolio/` | Definidos y sin uso en el resto del código. |

**[Diseño]** En el caso de `same_bar_policy` y `max_open_positions`, el tipo `Literal` y el
límite `le=1` impiden al menos poner un valor que el motor no respetaría: si escribes
`max_open_positions: 2`, la validación lo rechaza. Es una forma honesta de "configuración
documental". Los demás casos no tienen esa protección.

---

## 3.8 Gestión de errores y reintentos

### La idea

Los errores se dividen en dos familias, y deben tratarse de forma distinta:

- **Transitorios:** pueden resolverse solos si se reintenta (una desconexión, un servidor
  saturado). Se **reintentan** con esperas crecientes.
- **Permanentes:** reintentar no sirve (un símbolo que no existe, un parámetro inválido). Se
  **informan** de inmediato.

El cliente de Bybit implementa esa clasificación; el Módulo IV la estudia línea a línea. A nivel
de arquitectura, lo importante es **dónde** se convierten los errores en mensajes para la
persona usuaria: en un único lugar, la función `main` de la CLI:

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/cli.py#L692-L707 -->
`src/bybit_quant_lab/cli.py` · líneas 692–707

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
```
<!-- fmt: on -->

- **Línea 697:** antes de cualquier orden (salvo listar estrategias) se imprime la advertencia
  legal en la salida de error.
- **Líneas 698–701:** validación temprana de la temporalidad y la estrategia.
- **Líneas 702–707:** los errores **esperables** de uso (archivo inexistente, valor inválido,
  nombre desconocido) se muestran como una línea limpia y devuelven el **código de salida** 1.
  Cualquier otro error (un fallo de programación) deja ver la traza completa, para poder
  depurarlo.

El **código de salida** es el número que un programa devuelve al terminar: 0 significa éxito y
cualquier otro valor, fallo. Los scripts y las pruebas lo usan para saber si algo salió bien.
`bql` usa 0 (éxito), 1 (error de uso), 2 (error de la API de Bybit en `download`) y 3 (test final
ya evaluado en `final-test`).

**[Hecho] Inconsistencia menor:** `_load_data` (`cli.py`, líneas 101–107) señala los datos
inválidos con `raise SystemExit(...)` en lugar de `ValueError`. `SystemExit` no la captura el
bloque de las líneas 702–707: el programa termina con el mensaje y código de salida 1, así que el
efecto para la persona usuaria es casi el mismo, pero el mecanismo es distinto del resto.

---

## 3.9 Logging

### La idea

El **logging** (registro) es el diario del programa: mensajes con fecha, nivel de importancia y
origen, que ayudan a saber qué pasó sin tener que depurar. Los niveles habituales, de menor a
mayor gravedad, son `DEBUG`, `INFO`, `WARNING` y `ERROR`.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/logging_utils.py#L12-L40 -->
`src/bybit_quant_lab/logging_utils.py` · líneas 12–40

```python
class KeyValueFormatter(logging.Formatter):
    """Formatea registros como ``ts level logger msg k=v ...`` para facilitar su análisis."""

    def format(self, record: logging.LogRecord) -> str:
        base = f"{self.formatTime(record)} {record.levelname} {record.name} {record.getMessage()}"
        extra: dict[str, Any] = getattr(record, "ctx", {}) or {}
        if extra:
            base += " " + " ".join(f"{k}={v}" for k, v in sorted(extra.items()))
        if record.exc_info:
            base += "\n" + self.formatException(record.exc_info)
        return base


def setup_logging(level: str | None = None) -> None:
    """Configura el logger raíz del paquete una sola vez."""
    global _CONFIGURED
    if _CONFIGURED:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(KeyValueFormatter())
    logger = logging.getLogger("bybit_quant_lab")
    logger.addHandler(handler)
    logger.setLevel((level or os.getenv("BQL_LOG_LEVEL") or "INFO").upper())
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Devuelve un logger hijo de ``bybit_quant_lab``."""
    return logging.getLogger(f"bybit_quant_lab.{name}")
```
<!-- fmt: on -->

- Cada módulo pide su logger con `get_logger("data.bybit")`, que cuelga del logger raíz
  `bybit_quant_lab`. Así los mensajes indican de qué parte vienen.
- `setup_logging` se ejecuta una sola vez (la variable global `_CONFIGURED` lo controla) y fija
  el nivel desde `--log-level`, la variable de entorno `BQL_LOG_LEVEL` o `INFO` por defecto.

**[Hecho]** El proyecto registra muy pocos eventos: cuatro llamadas en total (guardado de
datasets, descargas y reintentos). El formateador admite contexto estructurado `clave=valor`,
pero ninguna llamada lo usa. La información principal de cada ejecución no está en el log, sino
en los archivos de resultados y en `outputs/experiments.jsonl` (sección 3.11).

---

## 3.10 La CLI como capa de presentación

### La idea

Una **CLI** (Command-Line Interface, interfaz de línea de órdenes) permite usar el sistema
escribiendo órdenes en la terminal. `bql` tiene **subórdenes** (como `git commit` o `git push`):
`bql backtest`, `bql compare`...

La biblioteca estándar `argparse` construye el analizador de argumentos:

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/cli.py#L592-L622 -->
`src/bybit_quant_lab/cli.py` · líneas 592–622

```python
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
```
<!-- fmt: on -->

- **Líneas 599–603:** opciones **globales**, que van **antes** de la suborden
  (`bql --data-dir X backtest ...`).
- **Línea 604:** `add_subparsers` crea las subórdenes; `required=True` obliga a indicar una.
- **Líneas 607–612:** una función auxiliar que añade `--symbol` y `--timeframe` a varias
  subórdenes. `type=str.upper` convierte `btcusdt` en `BTCUSDT`; `choices=tfs` solo admite
  temporalidades conocidas.
- **Línea 615:** `set_defaults(func=cmd_list)` asocia la suborden con la función que la ejecuta.
  `main` simplemente llama a `args.func(args)`.

**[Diseño]** La CLI no contiene lógica de trading: lee argumentos, llama a funciones de los otros
paquetes y escribe archivos. Todo lo que hace la CLI puede hacerse desde Python importando esas
funciones (el ejemplo `examples/full_workflow.py` lo demuestra). El Módulo XV recorre cada orden.

---

## 3.11 Persistencia: Parquet, JSON, CSV, hashes y metadatos

### La idea

**Persistir** es guardar datos en disco para que sobrevivan al programa. El proyecto usa varios
formatos, cada uno por un motivo:

| Formato | Qué guarda | Por qué ese formato |
|---|---|---|
| **Parquet** | Velas (`data/processed/*.parquet`) | Binario, comprimido, por columnas y con tipos: conserva fechas UTC y decimales sin pérdidas, y se lee muy rápido |
| **JSON** | Metadatos, métricas, selección congelada | Texto legible por personas y programas, con estructura anidada |
| **JSON Lines** | Registro de experimentos (`experiments.jsonl`) | Un JSON por línea: se puede **añadir** sin reescribir el archivo |
| **CSV** | Equity, operaciones, tablas de resultados | Se abre en cualquier hoja de cálculo |
| **HTML** | Informes | Se abre en el navegador, con gráficos incrustados |

### Hashes: huellas digitales de los datos

Un **hash** es un número de longitud fija calculado a partir de un contenido, de modo que
cualquier cambio en el contenido (un solo decimal) produce un hash completamente distinto. Sirve
como huella digital: si dos ejecuciones tienen el mismo hash de datos, usaron exactamente los
mismos datos.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/data/storage.py#L28-L31 -->
`src/bybit_quant_lab/data/storage.py` · líneas 28–31

```python
def data_hash(df: pd.DataFrame) -> str:
    """SHA-256 determinista del contenido (índice + valores) de un DataFrame."""
    hashed = pd.util.hash_pandas_object(df, index=True).to_numpy()
    return hashlib.sha256(hashed.tobytes()).hexdigest()
```
<!-- fmt: on -->

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/config/loader.py#L47-L52 -->
`src/bybit_quant_lab/config/loader.py` · líneas 47–52

```python
def config_hash(payload: Any) -> str:
    """SHA-256 (16 hex) de un objeto serializable, con claves ordenadas."""
    if hasattr(payload, "model_dump"):
        payload = payload.model_dump(mode="json")
    blob = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]
```
<!-- fmt: on -->

`sort_keys=True` es importante: ordena las claves antes de calcular el hash, de modo que la misma
configuración escrita en otro orden produce el mismo hash.

<!-- ejecutar -->
```python
from bybit_quant_lab.config import AppConfig, config_hash
from bybit_quant_lab.data.storage import data_hash
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv

datos = generate_synthetic_ohlcv(bars=100, seed=5)
copia = datos.copy()
copia.iloc[50, copia.columns.get_loc("close")] += 0.01  # un céntimo en una sola vela
print(data_hash(datos)[:16], data_hash(datos)[:16] == data_hash(datos.copy())[:16])
print(data_hash(copia)[:16])
print(config_hash(AppConfig()))
print(config_hash(AppConfig.model_validate({"costs": {"taker_fee": 0.0006}})))
```
<!-- salida -->
```text
b751a566c58ab273 True
ee0aec2f3e42ffeb
363e4d0affad48ee
31144f553528bcdf
```

### Metadatos de reproducibilidad

Cada informe incluye un bloque de **metadatos**: todo lo necesario para saber exactamente qué se
ejecutó.

<!-- fmt: off -->
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
<!-- fmt: on -->

Si dentro de seis meses un resultado te sorprende, con el commit de Git (`git`), el hash de datos
y la configuración completa puedes reconstruir la ejecución exacta. `dirty: true` avisa de que
había cambios sin confirmar en el código, lo que hace la reproducción menos fiable.

---

## 3.12 Principios de diseño presentes en el código (y los que no)

| Principio | ¿Presente? | Dónde |
|---|---|---|
| Responsabilidad única | Sí | Estructura de paquetes (sección 3.1) |
| Contratos explícitos | Sí | `SIGNAL_COLUMNS`, `BacktestResult`, Protocols |
| Inyección de dependencias | Sí, puntual | La sesión HTTP, el reloj y la función de espera del cliente de Bybit son parámetros, para poder probarlo sin red ni esperas reales |
| Inmutabilidad | Sí | Configuración y parámetros congelados (`frozen=True`), `CostModel` congelado |
| Fallar pronto | Sí | Validación de configuración, datos y contrato de señales |
| Determinismo | Sí | Sin aleatoriedad salvo con semilla fija; las pruebas verifican resultados idénticos |
| Registro (plugin) | Sí | `@register` para estrategias |
| Patrón Strategy (Gamma et al.) | Sí | Las estrategias son objetos intercambiables con la misma interfaz |
| Capas con dependencias hacia abajo | Sí | Sección 3.3, sin ciclos |
| Logging estructurado | Parcial | El formateador lo permite, pero no se usa (sección 3.9) |
| Configuración sin efecto | Antipatrón presente | Sección 3.7 |
| Inversión de dependencias completa (interfaces para todo) | No | El motor depende de clases concretas (`RiskManager`, `CostModel`). Para este tamaño de proyecto es razonable |

---

## 3.13 Cómo añadir una funcionalidad sin romper otras

Procedimiento general (el Módulo XVI lo aplica con ejercicios):

1. **Localiza la capa** donde vive la responsabilidad. Una nueva métrica va en `analytics/`; una
   nueva fuente de datos, en `data/`.
2. **Respeta el contrato** de la interfaz que tocas. Si devuelves más columnas o claves, no quites
   las existentes.
3. **Escribe primero una prueba** que falle sin tu cambio (Módulo XIV).
4. **Ejecuta las tres comprobaciones:** `pytest`, `ruff check .` y `mypy src`.
5. **Revisa el impacto en resultados:** si el cambio afecta a señales, ejecución o costes,
   cualquier resultado anterior deja de ser comparable. Hay que repetir la validación, y el test
   final ya evaluado no puede reutilizarse (Módulo XIII).
6. **Actualiza la documentación** y, si cambiaste líneas citadas, ejecuta
   `python scripts/curso_citas.py --check`.

---

## 3.14 Refactorizaciones razonables y no justificadas

Una **refactorización** cambia la estructura del código sin cambiar su comportamiento.

**Razonables** (mejoran claridad o eliminan riesgos, con poco coste):

- Eliminar o conectar la configuración sin efecto de la sección 3.7 (por ejemplo, que el motor
  use `maker_fee` cuando existan órdenes límite, o quitar `BQL_BYBIT_BASE_URL`).
- Dividir `cli.py` (711 líneas) en un módulo por suborden. Hoy mezcla la construcción del
  analizador y diez funciones `cmd_*`.
- Dividir `validation/research.py` (624 líneas), que hace comparación, test final, walk-forward
  y sensibilidad en una sola clase.
- Hacer que `_load_data` lance `ValueError` como el resto de errores de uso.

**No justificadas por ahora:**

- Reescribir el motor para que sea vectorizado (más rápido): el bucle explícito es más fácil de
  auditar, y la auditoría de cada paso es lo que da valor a un backtest. Solo merecería la pena
  si el tiempo de cálculo llegara a ser un problema real con datos de 5 minutos de varios años.
- Introducir interfaces abstractas para cada componente del motor: añadiría complejidad sin un
  segundo uso que la justifique.
- Cambiar Pydantic por dataclasses con validación manual: perdería validaciones probadas.

### Comprobación final del módulo

Un compañero propone que cada estrategia calcule también su tamaño de posición "porque así es
más flexible". ¿Qué principio rompería y qué consecuencia práctica tendría?

<details><summary>Ver respuesta</summary>

Rompería la separación de responsabilidades: el riesgo dejaría de estar centralizado en `risk/`.
En la práctica, los límites del sistema (riesgo por operación, exposición, margen) podrían
aplicarse de forma distinta en cada estrategia, y una combinación de estrategias no sabría qué
tamaño usar. Además, cambiar la política de riesgo exigiría modificar diez archivos.
</details>
