# Módulo II. Fundamentos de Python aplicados al proyecto

Este módulo no es un libro general de Python. Enseña **lo necesario para leer este
repositorio**, siempre con ejemplos tomados del código real. Si ya programas, puedes saltar a
las secciones 2.9 a 2.15 (clases, herencia, decoradores y modelos de configuración), que son las
que más usa el proyecto.

Para ejecutar los ejemplos: abre una terminal en `bybit-quant-lab/`, activa el entorno virtual
(sección 2.19) y escribe `python` para abrir el intérprete interactivo, o guarda el ejemplo en un
archivo `.py` y ejecútalo con `python archivo.py`.

---

## 2.1 Cómo se lee un archivo de Python

### La idea

Un archivo `.py` es texto con instrucciones que el **intérprete** de Python ejecuta de arriba
abajo. Los elementos que verás en todos los archivos del proyecto son:

- **Comentarios:** empiezan por `#` y Python los ignora. Son notas para personas.
- **Docstrings:** textos entre triples comillas `"""..."""` al principio de un archivo, una
  función o una clase. Documentan qué hace. A diferencia de los comentarios, Python los guarda
  y puedes leerlos con `help(funcion)`.
- **Indentación:** los espacios al principio de la línea indican qué instrucciones pertenecen
  a un bloque (una función, un `if`, un bucle). En este proyecto se usan 4 espacios. Una
  indentación incorrecta es un error, no una cuestión estética.

El archivo más corto del paquete muestra un docstring y dos variables:

<!-- cita: src/bybit_quant_lab/__init__.py#L1-L13 -->
`src/bybit_quant_lab/__init__.py` · líneas 1–13

```python
"""bybit-quant-lab: framework de investigación y backtesting para perpetuos lineales de Bybit.

Uso exclusivo de investigación. No ejecuta órdenes reales ni utiliza endpoints autenticados.
Los resultados históricos no garantizan resultados futuros.
"""

__version__ = "0.1.0"

DISCLAIMER = (
    "ADVERTENCIA: resultados de backtesting con fines exclusivos de investigación. "
    "Los resultados históricos no garantizan resultados futuros. Este software no ejecuta "
    "órdenes reales ni constituye recomendación de inversión."
)
```

`__version__` y `DISCLAIMER` son **variables de módulo**: cualquier otro archivo puede leerlas
con `from bybit_quant_lab import DISCLAIMER`. El texto de `DISCLAIMER` está partido en tres
líneas entre paréntesis; Python une automáticamente cadenas de texto contiguas.

---

## 2.2 Variables, tipos de datos y operadores

### La idea

Una **variable** es un nombre que apunta a un valor. Un **tipo** describe qué clase de valor es
y qué operaciones admite:

| Tipo | Ejemplo | Uso en el proyecto |
|---|---|---|
| `int` (entero) | `14` | Periodos de indicadores, número de velas |
| `float` (decimal) | `0.00055` | Precios, comisiones, rendimientos |
| `str` (texto) | `"BTCUSDT"` | Símbolos, nombres de estrategias |
| `bool` (lógico) | `True`, `False` | Opciones activadas/desactivadas |
| `None` | `None` | "No hay valor" (por ejemplo, sin take-profit) |

En `timeframes.py` hay una variable calculada con operadores aritméticos:

<!-- cita: src/bybit_quant_lab/timeframes.py#L18-L18 -->
`src/bybit_quant_lab/timeframes.py` · líneas 18–18

```python
MINUTES_PER_YEAR = 365 * 24 * 60  # mercado cripto 24/7, año de 365 días
```

`365 * 24 * 60` multiplica días × horas × minutos: el número de minutos de un año de 365 días.
La convención de MAYÚSCULAS indica una **constante**: un valor que no debe cambiar mientras el
programa funciona (Python no lo impide; es un acuerdo entre programadores).

Operadores que verás a menudo:

- Aritméticos: `+ - * /`, `//` (división entera), `%` (resto), `**` (potencia).
- Comparación: `== != < <= > >=` (devuelven `True` o `False`).
- Lógicos: `and`, `or`, `not`.
- Pertenencia: `in` ("¿está este elemento en esta colección?").

<!-- ejecutar -->
```python
minutos_por_anio = 365 * 24 * 60
velas_de_1h = minutos_por_anio / 60      # "/" siempre devuelve float
velas_de_4h = minutos_por_anio // 240     # "//" descarta los decimales
print(minutos_por_anio, velas_de_1h, velas_de_4h)
print(10_000 * 0.01)                      # el guion bajo separa miles, no cambia el número
print(0.1 + 0.2 == 0.3, abs((0.1 + 0.2) - 0.3) < 1e-12)
```
<!-- salida -->
```text
525600 8760.0 2190
100.0
False True
```

La última línea es importante: los `float` se guardan en binario y **no representan exactamente**
muchos decimales. `0.1 + 0.2` no es exactamente `0.3`. Por eso las pruebas del proyecto comparan
precios con `pytest.approx` (Módulo XIV) y no con `==`.

### Comprobación

¿Qué imprime `print(7 // 2, 7 % 2, 2 ** 3)`?

<details><summary>Ver respuesta</summary>

`3 1 8`: división entera, resto y potencia.
</details>

---

## 2.3 Condicionales y bucles

### La idea

- Un **condicional** (`if / elif / else`) ejecuta un bloque solo si se cumple una condición.
- Un **bucle** `for` repite un bloque para cada elemento de una secuencia.

La función `events_to_state` de `strategies/base.py` usa ambos, y es una de las funciones más
importantes del proyecto: convierte "eventos" (momentos en que se cumple una condición de
entrada o salida) en un "estado" que se mantiene vela tras vela.

<!-- cita: src/bybit_quant_lab/strategies/base.py#L191-L217 -->
`src/bybit_quant_lab/strategies/base.py` · líneas 191–217

```python
    le, se = long_entry.to_numpy(bool), short_entry.to_numpy(bool)
    lx, sx = long_exit.to_numpy(bool), short_exit.to_numpy(bool)
    n = len(le)
    out = np.zeros(n, dtype=np.int64)
    state, held, since_exit = 0, 0, cooldown_bars
    for i in range(n):
        if state == 1:
            held += 1
            if se[i] and not le[i]:
                state, held = -1, 0
            elif lx[i] or (max_holding_bars is not None and held >= max_holding_bars):
                state, since_exit = 0, 0
        elif state == -1:
            held += 1
            if le[i] and not se[i]:
                state, held = 1, 0
            elif sx[i] or (max_holding_bars is not None and held >= max_holding_bars):
                state, since_exit = 0, 0
        else:
            since_exit += 1
            if since_exit > cooldown_bars:
                if le[i] and not se[i] and not lx[i]:
                    state, held = 1, 0
                elif se[i] and not le[i] and not sx[i]:
                    state, held = -1, 0
        out[i] = state
    return pd.Series(out, index=long_entry.index, name="signal")
```

Línea por línea:

- **191–192:** convierte las cuatro series de eventos en arrays de `True/False` (Módulo V
  explica qué es un array). `le` = long entry, `se` = short entry, `lx` = long exit,
  `sx` = short exit.
- **193–194:** `n` es el número de velas; `out` es un array de `n` ceros donde se guardará el
  estado de cada vela.
- **195:** **asignación múltiple**. `state` es el estado actual (0 = FLAT), `held` cuenta las
  velas que lleva la posición y `since_exit` las velas desde la última salida.
- **196:** `for i in range(n)` recorre `i = 0, 1, ..., n-1`.
- **197–202:** si estamos largos (`state == 1`), sumamos una vela (`held += 1` equivale a
  `held = held + 1`). Si aparece una entrada corta sin una larga simultánea, revertimos a corto
  (`-1`). Si no, y hay una salida larga o se agotó el tiempo máximo, pasamos a FLAT.
- **203–208:** lo mismo, en espejo, para cuando estamos cortos.
- **209–215:** si estamos FLAT, solo entramos cuando ha pasado el enfriamiento
  (`since_exit > cooldown_bars`) y la entrada no entra en conflicto con otra.
- **216:** guardamos el estado de esta vela.
- **217:** devolvemos los estados como una serie de pandas con el mismo índice temporal que los
  eventos.

El orden de los `if` importa: al estar largos, la comprobación de "entrada corta" va antes que
la de "salida larga". Por eso, si en la misma vela hay entrada corta y salida larga, el estado
pasa directamente a corto (reversión) en vez de quedarse en FLAT. Es una **regla de diseño**
documentada en el docstring de la función.

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.strategies.base import events_to_state

def serie(valores):
    return pd.Series([bool(v) for v in valores])

estado = events_to_state(
    long_entry=serie([0, 1, 0, 0, 0, 0]),
    short_entry=serie([0, 0, 0, 1, 0, 0]),
    long_exit=serie([0, 0, 0, 0, 0, 0]),
    short_exit=serie([0, 0, 0, 0, 1, 0]),
)
print(estado.tolist())
```
<!-- salida -->
```text
[0, 1, 1, -1, 0, 0]
```

Lectura: vela 1, entrada larga → 1. Vela 3, entrada corta estando largos → reversión a −1.
Vela 4, salida corta → 0. Después no hay más eventos.

### Comprobación

Con `cooldown_bars=2`, tras salir en la vela 4, ¿en qué vela podría volver a entrar como pronto?

<details><summary>Ver respuesta</summary>

En la vela 4 se pone `since_exit = 0`. En la vela 5 pasa a 1, en la 6 a 2 y en la 7 a 3. La
condición es `since_exit > 2`, así que la primera vela posible es la **7**.
</details>

---

## 2.4 Funciones: parámetros, argumentos, retorno y alcance

### La idea

Una **función** es un bloque de código con nombre que recibe datos (**parámetros**), hace algo
y devuelve un resultado (**valor de retorno**). Cuando la llamas, los valores que le pasas son
los **argumentos**.

`timeframes.py` contiene cinco funciones pequeñas que se llaman unas a otras:

<!-- cita: src/bybit_quant_lab/timeframes.py#L21-L45 -->
`src/bybit_quant_lab/timeframes.py` · líneas 21–45

```python
def validate_timeframe(timeframe: str) -> str:
    """Valida y devuelve la temporalidad; lanza ``ValueError`` si no es soportada."""
    if timeframe not in TIMEFRAMES:
        raise ValueError(f"Temporalidad no soportada: {timeframe!r}. Opciones: {list(TIMEFRAMES)}")
    return timeframe


def timeframe_minutes(timeframe: str) -> int:
    """Duración de una vela en minutos."""
    return TIMEFRAMES[validate_timeframe(timeframe)][1]


def timeframe_delta(timeframe: str) -> pd.Timedelta:
    """Duración de una vela como ``Timedelta``."""
    return pd.Timedelta(minutes=timeframe_minutes(timeframe))


def bybit_interval(timeframe: str) -> str:
    """Código de intervalo de Bybit V5 para la temporalidad."""
    return TIMEFRAMES[validate_timeframe(timeframe)][0]


def bars_per_year(timeframe: str) -> float:
    """Número de velas por año (365 días, 24 h)."""
    return MINUTES_PER_YEAR / timeframe_minutes(timeframe)
```

- `def validate_timeframe(timeframe: str) -> str:` declara una función con un parámetro
  `timeframe` de tipo texto que devuelve texto (la parte `: str` y `-> str` son **type hints**,
  sección 2.14).
- `raise ValueError(...)` interrumpe la función con un error si la temporalidad no existe
  (sección 2.7).
- `return timeframe` devuelve el valor a quien llamó.
- `timeframe_minutes` **reutiliza** `validate_timeframe` y después busca en el diccionario
  `TIMEFRAMES` (sección 2.5): `[1]` toma el segundo elemento de la tupla.
- `f"..."` es una **f-string**: inserta valores dentro de un texto. `{timeframe!r}` inserta la
  representación del valor con comillas, útil en mensajes de error.

**Alcance (scope).** Las variables creadas dentro de una función solo existen dentro de ella.
`TIMEFRAMES`, en cambio, es una variable de módulo y todas las funciones del archivo pueden
leerla.

**Parámetros con valor por defecto y por nombre.** Muchas funciones del proyecto tienen
parámetros opcionales, por ejemplo `events_to_state(..., max_holding_bars=None, cooldown_bars=0)`
(líneas 173–180 de `strategies/base.py`). Si no los pasas, valen lo indicado. Al llamar puedes
usar el nombre del parámetro (`cooldown_bars=3`), lo que hace el código más legible.

<!-- ejecutar -->
```python
from bybit_quant_lab.timeframes import bars_per_year, bybit_interval, timeframe_minutes

print(timeframe_minutes("4h"), bybit_interval("4h"), bars_per_year("1h"))
try:
    timeframe_minutes("2h")
except ValueError as error:
    print("Error:", error)
```
<!-- salida -->
```text
240 240 8760.0
Error: Temporalidad no soportada: '2h'. Opciones: ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
```

### Comprobación

¿Qué devuelve `bybit_interval("1h")` y por qué no devuelve `"1h"`?

<details><summary>Ver respuesta</summary>

Devuelve `"60"`: es el código que espera la API de Bybit para velas de 60 minutos. La función
traduce el nombre interno del proyecto al código de la API.
</details>

---

## 2.5 Colecciones: listas, tuplas, diccionarios y conjuntos

### La idea

| Colección | Sintaxis | ¿Ordenada? | ¿Modificable? | ¿Duplicados? | Uso típico |
|---|---|---|---|---|---|
| Lista | `[1, 2, 3]` | Sí | Sí | Sí | Secuencias que crecen (operaciones, filas) |
| Tupla | `(1, 2, 3)` | Sí | No | Sí | Grupos fijos (columnas obligatorias) |
| Diccionario | `{"a": 1}` | Sí (orden de inserción) | Sí | Claves únicas | Buscar un valor por su clave |
| Conjunto | `{1, 2, 3}` | No | Sí | No | Pertenencia rápida, eliminar duplicados |

Un **diccionario** asocia claves con valores. `TIMEFRAMES` asocia cada temporalidad con una
tupla de dos elementos (código de Bybit, minutos):

<!-- cita: src/bybit_quant_lab/timeframes.py#L7-L16 -->
`src/bybit_quant_lab/timeframes.py` · líneas 7–16

```python
#: Temporalidad interna -> (intervalo Bybit, minutos)
TIMEFRAMES: dict[str, tuple[str, int]] = {
    "1m": ("1", 1),
    "5m": ("5", 5),
    "15m": ("15", 15),
    "30m": ("30", 30),
    "1h": ("60", 60),
    "4h": ("240", 240),
    "1d": ("D", 1440),
}
```

Una **tupla** define las columnas que toda señal debe tener. Se usa tupla y no lista porque no
debe modificarse:

<!-- cita: src/bybit_quant_lab/strategies/base.py#L36-L43 -->
`src/bybit_quant_lab/strategies/base.py` · líneas 36–43

```python
SIGNAL_COLUMNS: tuple[str, ...] = (
    "signal",
    "conviction",
    "stop_distance",
    "take_profit_distance",
    "trailing_distance",
)
REQUIRED_COLUMNS: tuple[str, ...] = ("open", "high", "low", "close", "volume")
```

Un **conjunto** guarda los códigos de error que merece la pena reintentar. Se usa conjunto
porque la única pregunta que se le hace es "¿este código está aquí?", y esa consulta es muy
rápida en un conjunto:

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L27-L30 -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 27–30

```python
#: retCode de Bybit considerados transitorios (10000: timeout del servidor,
#: 10006: demasiadas peticiones, 10016: error interno del servidor).
RETRYABLE_RET_CODES = {10000, 10006, 10016}
RETRYABLE_HTTP = {429, 500, 502, 503, 504}
```

<!-- ejecutar -->
```python
from bybit_quant_lab.timeframes import TIMEFRAMES

codigo, minutos = TIMEFRAMES["15m"]          # "desempaquetar" una tupla en dos variables
print(codigo, minutos)
print(list(TIMEFRAMES)[:3])                  # recorrer un diccionario da sus claves
print(10006 in {10000, 10006, 10016})        # pertenencia en un conjunto
operaciones = []
operaciones.append(12.5)
operaciones.append(-3.0)
print(operaciones, len(operaciones), sum(operaciones))
```
<!-- salida -->
```text
15 15
['1m', '5m', '15m']
True
[12.5, -3.0] 2 9.5
```

### Comprobación

¿Por qué `RETRYABLE_HTTP` es un conjunto y no una lista? ¿Funcionaría con una lista?

<details><summary>Ver respuesta</summary>

Funcionaría igual (`429 in [429, 500]` también es `True`), pero el conjunto expresa mejor la
intención (no importa el orden ni puede haber repetidos) y la consulta de pertenencia es más
rápida. Con cinco elementos la diferencia de velocidad es irrelevante; la claridad no.
</details>

---

## 2.6 Comprensiones y expresiones generadoras

### La idea

Una **comprensión** construye una colección a partir de otra en una sola expresión:
`[x * 2 for x in numeros if x > 0]` significa "para cada `x` de `numeros` que sea positivo,
pon `x * 2` en una lista nueva".

El registro de experimentos (`validation/experiment_log.py`) usa los tres tipos:

<!-- cita: src/bybit_quant_lab/validation/experiment_log.py#L30-L62 -->
`src/bybit_quant_lab/validation/experiment_log.py` · líneas 30–62

```python
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

- **Línea 35:** comprensión de **lista**. Lee cada línea del archivo, ignora las vacías
  (`if line.strip()`) y convierte cada una de JSON a diccionario.
- **Líneas 39–44:** **expresión generadora** dentro de `sum(...)`. Produce un `1` por cada
  registro que cumple los filtros y `sum` los suma: es una forma de contar. A diferencia de una
  lista, no guarda todos los `1` en memoria a la vez; los va generando uno a uno.
- **Líneas 54–61:** comprensión de **conjunto** (llaves `{...}`). Convierte cada combinación
  "candidato + parámetros" en un texto y, al ser un conjunto, los repetidos se eliminan solos.
  `len(keys)` es entonces el número de configuraciones **distintas** probadas, un dato clave para
  corregir el sesgo de selección (Módulo XIII).

<!-- ejecutar -->
```python
registros = [
    {"candidate": "rsi", "params": {"oversold": 30}, "segment": "validation"},
    {"candidate": "rsi", "params": {"oversold": 30}, "segment": "validation"},
    {"candidate": "rsi", "params": {"oversold": 25}, "segment": "validation"},
    {"candidate": "macd", "params": {}, "segment": "train"},
]
total_validacion = sum(1 for r in registros if r["segment"] == "validation")
distintas = {(r["candidate"], str(r["params"])) for r in registros if r["segment"] == "validation"}
print(total_validacion, len(distintas))
```
<!-- salida -->
```text
3 2
```

Se evaluaron 3 configuraciones en validación, pero solo 2 eran distintas.

---

## 2.7 Manejo de excepciones

### La idea

Una **excepción** es un error que interrumpe el programa, a menos que alguien la "capture". Hay
tres piezas:

- `raise TipoDeError("mensaje")` **lanza** una excepción.
- `try: ... except TipoDeError: ...` **captura** la excepción y ejecuta un plan alternativo.
- `raise NuevoError(...) from exc` lanza otra excepción más clara **conservando** la original
  como causa, para no perder información al depurar.

El registro de estrategias muestra las tres:

<!-- cita: src/bybit_quant_lab/strategies/registry.py#L25-L32 -->
`src/bybit_quant_lab/strategies/registry.py` · líneas 25–32

```python
def get_strategy_class(name: str) -> type[Strategy]:
    """Clase de estrategia por nombre."""
    try:
        return _REGISTRY[name]
    except KeyError as exc:
        raise KeyError(
            f"Estrategia desconocida: {name!r}. Disponibles: {available_strategies()}"
        ) from exc
```

Buscar una clave inexistente en un diccionario lanza `KeyError`. El código la captura y lanza
otra `KeyError` con un mensaje útil, que incluye la lista de estrategias disponibles.

El cliente HTTP define su **propia** excepción, heredando de una de Python (la herencia se
explica en 2.11):

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L33-L34 -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 33–34

```python
class BybitAPIError(RuntimeError):
    """Error no recuperable o reintentos agotados al consultar Bybit."""
```

Tener un tipo propio permite que la CLI capture exactamente los errores de Bybit y los muestre
de forma limpia, sin capturar por accidente errores de programación.

Y así captura los errores de red para reintentar en lugar de rendirse:

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L98-L102 -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 98–102

```python
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout_seconds)
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_error = f"error de red: {exc}"
                continue
```

`continue` salta a la siguiente vuelta del bucle de reintentos (lo verás completo en el
Módulo IV).

**[Diseño] Errores frecuentes que el proyecto evita:**

- `except:` sin tipo, que captura **todo** (incluso fallos de programación) y los oculta. El
  proyecto siempre indica el tipo concreto.
- Capturar un error y no hacer nada. El proyecto reintenta, re-lanza con un mensaje mejor o
  registra el problema.

### Comprobación

¿Qué ventaja tiene `raise KeyError(...) from exc` frente a `raise KeyError(...)` a secas?

<details><summary>Ver respuesta</summary>

La traza de error mostrará las dos excepciones: la original (la clave que faltaba) y la nueva
(con el mensaje explicativo). Sin `from exc` también se encadenan de forma implícita, pero con
un mensaje que sugiere un segundo fallo accidental; `from exc` indica que la sustitución es
deliberada.
</details>

---

## 2.8 Módulos, paquetes e importaciones

### La idea

- Un **módulo** es un archivo `.py`.
- Un **paquete** es una carpeta con un archivo `__init__.py`; agrupa módulos.
- `import` y `from ... import ...` traen código de otros módulos.

La ruta `bybit_quant_lab.strategies.ema_crossover` corresponde al archivo
`src/bybit_quant_lab/strategies/ema_crossover.py`.

El `__init__.py` del paquete de estrategias tiene un detalle importante:

<!-- cita: src/bybit_quant_lab/strategies/__init__.py#L1-L14 -->
`src/bybit_quant_lab/strategies/__init__.py` · líneas 1–14

```python
"""Estrategias registradas. Importar este paquete registra las diez estrategias."""

from bybit_quant_lab.strategies import (  # noqa: F401  (registro por efecto de importación)
    adx_di,
    bollinger_reversion,
    donchian_breakout,
    ema_crossover,
    macd_momentum,
    obv_trend,
    rsi_reversion,
    stoch_rsi,
    volume_spike,
    vwap_deviation,
)
```

Importa los diez módulos de estrategias **aunque no use ningún nombre de ellos**. Lo hace por su
**efecto secundario**: al importarse, cada módulo ejecuta el decorador `@register`, que añade la
estrategia al registro (sección 2.12). El comentario `# noqa: F401` le dice a la herramienta de
lint Ruff que esa importación "sin usar" es intencionada.

**[Diseño]** La alternativa sería una lista escrita a mano con las diez clases. El registro por
decorador tiene la ventaja de que añadir una estrategia exige un único cambio en este archivo
(una línea de importación). Su desventaja es que es menos explícito: si olvidas importar el
módulo, la estrategia no existe para el sistema y no hay error, solo una ausencia.

La primera línea de código de casi todos los módulos es:

```python
from __future__ import annotations
```

Hace que Python no evalúe las anotaciones de tipo al cargar el archivo. Permite, por ejemplo,
que un método anote que devuelve su propia clase antes de que la clase termine de definirse.

---

## 2.9 Clases, objetos, atributos y métodos

### La idea

Una **clase** es un molde que describe un tipo de objeto: qué datos guarda (**atributos**) y qué
sabe hacer (**métodos**, funciones que pertenecen a la clase). Un **objeto** (o **instancia**) es
un ejemplar concreto creado con ese molde.

Analogía: la clase es el formulario en blanco "Posición abierta"; cada objeto es un formulario
rellenado con una posición concreta.

La clase `Position` representa una posición abierta:

<!-- cita: src/bybit_quant_lab/portfolio/position.py#L11-L53 -->
`src/bybit_quant_lab/portfolio/position.py` · líneas 11–53

```python
@dataclass
class Position:
    """Posición abierta en margen aislado (una por símbolo)."""

    side: int
    qty: float
    entry_price: float
    entry_time: pd.Timestamp
    entry_bar: int
    stop: float | None
    take_profit: float | None
    trailing_distance: float | None
    liquidation_price: float | None
    margin: float
    entry_fee: float
    entry_slippage: float
    conviction: float = 0.0
    funding: float = 0.0
    extreme: float = 0.0
    equity_at_entry: float = 0.0
    regime: str = ""

    @property
    def notional_entry(self) -> float:
        """Nocional a precio de entrada."""
        return self.qty * self.entry_price

    def unrealized(self, price: float) -> float:
        """PnL no realizado a ``price`` (sin costes de salida)."""
        return self.side * (price - self.entry_price) * self.qty

    def update_trailing(self, close: float) -> None:
        """Actualiza el trailing stop con el cierre (solo puede mejorar el stop)."""
        if self.trailing_distance is None:
            return
        if self.side > 0:
            self.extreme = max(self.extreme, close)
            candidate = self.extreme - self.trailing_distance
            self.stop = candidate if self.stop is None else max(self.stop, candidate)
        else:
            self.extreme = min(self.extreme, close)
            candidate = self.extreme + self.trailing_distance
            self.stop = candidate if self.stop is None else min(self.stop, candidate)
```

- **Líneas 15–31:** los atributos y sus tipos. Algunos tienen valor por defecto (`= 0.0`).
- **Líneas 33–36:** `@property` convierte un método en algo que se lee como un atributo:
  `posicion.notional_entry` (sin paréntesis) calcula `qty * entry_price` cada vez.
- **Líneas 38–40:** el método `unrealized` calcula la ganancia o pérdida "en papel" a un precio
  dado. `self` es el propio objeto: `self.side` es el lado de **esta** posición. El truco de
  multiplicar por `side` (+1 largo, −1 corto) sirve para ambos casos con una sola fórmula.
- **Líneas 42–53:** `update_trailing` **modifica** el objeto: mueve el stop si el precio
  avanzó a favor. `max(self.stop, candidate)` garantiza que el stop de un largo nunca baja.

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.portfolio.position import Position

p = Position(side=1, qty=0.5, entry_price=100.0, entry_time=pd.Timestamp("2024-01-01", tz="UTC"),
             entry_bar=0, stop=95.0, take_profit=None, trailing_distance=4.0,
             liquidation_price=None, margin=16.67, entry_fee=0.0, entry_slippage=0.0,
             extreme=100.0)
print(p.notional_entry, p.unrealized(104.0))
for cierre in (103.0, 106.0, 102.0):
    p.update_trailing(cierre)
    print(f"cierre {cierre}: stop = {p.stop}")
```
<!-- salida -->
```text
50.0 2.0
cierre 103.0: stop = 99.0
cierre 106.0: stop = 102.0
cierre 102.0: stop = 102.0
```

El stop sube de 95 a 99 (103 − 4) y luego a 102 (106 − 4). Cuando el precio baja a 102 no
retrocede: el trailing stop solo avanza a favor.

### Comprobación

Para una posición corta (`side=-1`) de 2 unidades abierta a 50, ¿cuánto vale `unrealized(45)`?

<details><summary>Ver respuesta</summary>

`-1 × (45 − 50) × 2 = 10`. Ganancia de 10, como corresponde a un corto cuando el precio baja.
</details>

---

## 2.10 Dataclasses

### La idea

Escribir una clase que solo guarda datos exige mucho código repetitivo (un método para
inicializar, otro para mostrarla, otro para compararla). El decorador `@dataclass` lo genera
automáticamente a partir de la lista de atributos. `Position` y `TradeRecord` son dataclasses.

`CostModel` usa además `frozen=True`, que hace los objetos **inmutables**: una vez creado, nadie
puede cambiar sus comisiones por error a mitad de una simulación.

<!-- cita: src/bybit_quant_lab/execution/costs.py#L15-L39 -->
`src/bybit_quant_lab/execution/costs.py` · líneas 15–39

```python
@dataclass(frozen=True)
class CostModel:
    """Comisiones y slippage."""

    taker_fee: float
    maker_fee: float
    slippage_bps: float

    @classmethod
    def from_config(cls, cfg: CostConfig) -> CostModel:
        """Construye el modelo desde ``CostConfig``."""
        return cls(cfg.taker_fee, cfg.maker_fee, cfg.slippage_bps)

    @property
    def slip(self) -> float:
        """Slippage como fracción."""
        return self.slippage_bps / 10_000

    def fill_price(self, reference: float, direction: int) -> float:
        """Precio con slippage adverso; ``direction`` = +1 compra, -1 venta."""
        return reference * (1 + self.slip * direction)

    def fee(self, notional: float, taker: bool = True) -> float:
        """Comisión sobre el nocional (``qty * precio_ejecución``)."""
        return abs(notional) * (self.taker_fee if taker else self.maker_fee)
```

- **`@classmethod` (líneas 23–26):** un método que se llama sobre la **clase**, no sobre un
  objeto, y suele usarse como constructor alternativo: `CostModel.from_config(cfg)` crea un
  modelo de costes a partir de la configuración. `cls` es la propia clase.
- **`slip` (líneas 28–31):** convierte puntos básicos en fracción. Un **punto básico** (bps) es
  una centésima de punto porcentual: 2 bps = 0,02 % = 0,0002.
- **`fill_price` (líneas 33–35):** el deslizamiento siempre es **adverso**. Al comprar
  (`direction=+1`) pagas más; al vender (`-1`) recibes menos.

La clase `Account` usa `__post_init__`, un método que la dataclass ejecuta justo después de crear
el objeto, para que el efectivo inicial sea igual al capital:

<!-- cita: src/bybit_quant_lab/portfolio/account.py#L20-L48 -->
`src/bybit_quant_lab/portfolio/account.py` · líneas 20–48

```python
@dataclass
class Account:
    """Estado contable de la simulación."""

    initial_capital: float
    cash: float = 0.0
    position: Position | None = None
    total_fees: float = 0.0
    total_slippage: float = 0.0
    total_funding: float = 0.0
    traded_notional: float = 0.0
    realized_pnl: float = 0.0
    history: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.cash = self.initial_capital

    @property
    def used_margin(self) -> float:
        """Margen inicial bloqueado por la posición abierta."""
        return self.position.margin if self.position else 0.0

    def equity(self, price: float) -> float:
        """Equity mark-to-market."""
        return self.cash + (self.position.unrealized(price) if self.position else 0.0)

    def available_margin(self, price: float) -> float:
        """Equity menos margen usado."""
        return self.equity(price) - self.used_margin
```

`field(default_factory=list)` (línea 32) evita un error clásico de Python: si escribieras
`history: list = []`, **todas** las cuentas compartirían la misma lista.

<!-- ejecutar -->
```python
from bybit_quant_lab.execution.costs import CostModel

costes = CostModel(taker_fee=0.00055, maker_fee=0.0002, slippage_bps=2.0)
print(costes.slip)
print(costes.fill_price(100.0, +1), costes.fill_price(100.0, -1))
print(costes.fee(notional=10_000))
try:
    costes.taker_fee = 0.0
except Exception as error:
    print(type(error).__name__)
```
<!-- salida -->
```text
0.0002
100.02 99.98
5.5
FrozenInstanceError
```

Comprar a 100 cuesta 100,02 y vender a 100 devuelve 99,98. La comisión taker de una operación de
10.000 USDT es 5,5 USDT. Modificar un objeto congelado lanza `FrozenInstanceError`.

---

## 2.11 Herencia, clases abstractas, polimorfismo, composición y encapsulación

### La idea

- **Herencia:** una clase hija recibe todo lo de su madre y añade o cambia algo. "Una EMA
  Crossover **es una** estrategia".
- **Clase abstracta:** una clase madre que no se puede usar directamente porque deja métodos sin
  implementar; obliga a las hijas a implementarlos.
- **Polimorfismo:** código que trabaja con "cualquier estrategia" sin saber cuál es, porque todas
  responden a los mismos métodos.
- **Composición:** un objeto que **tiene** otros objetos dentro. "El motor **tiene un** modelo de
  costes".
- **Encapsulación:** ocultar detalles internos. En Python es una convención: los nombres que
  empiezan por `_` son internos y no deberían usarse desde fuera.

### La clase base de las estrategias

<!-- cita: src/bybit_quant_lab/strategies/base.py#L87-L107 -->
`src/bybit_quant_lab/strategies/base.py` · líneas 87–107

```python
class Strategy(ABC):
    """Clase base de todas las estrategias. No conoce el motor de backtesting."""

    name: ClassVar[str] = "base"
    category: ClassVar[Category] = Category.INDICATOR
    description: ClassVar[str] = ""
    params_model: ClassVar[type[StrategyParams]] = StrategyParams

    def __init__(self, params: StrategyParams | dict[str, Any] | None = None, **kwargs: Any):
        data = params.model_dump() if isinstance(params, StrategyParams) else dict(params or {})
        data.update(kwargs)
        self.params = self.params_model.model_validate(data)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.params.model_dump()})"

    @abstractmethod
    def warmup_bars(self) -> int:
        """Velas necesarias antes de que los indicadores sean válidos."""

    @abstractmethod
```

- `class Strategy(ABC)` hereda de `ABC` (Abstract Base Class) y se convierte en abstracta.
- `ClassVar[...]` (líneas 90–93) marca **atributos de clase**: comunes a todas las instancias,
  como el nombre o la categoría. Cada estrategia hija los redefine.
- `@abstractmethod` (líneas 103–107): `warmup_bars` y `compute_events` **deben** implementarse
  en cada estrategia. Si una hija los olvida, Python impide crear objetos de ella.
- El constructor `__init__` (líneas 95–98) acepta los parámetros como objeto de configuración,
  como diccionario o como argumentos sueltos (`**kwargs` recoge todos los argumentos con nombre
  en un diccionario) y los valida con el modelo de parámetros de la estrategia
  (`self.params_model`, sección 2.15).

### Una estrategia hija completa

<!-- cita: src/bybit_quant_lab/strategies/ema_crossover.py#L20-L74 -->
`src/bybit_quant_lab/strategies/ema_crossover.py` · líneas 20–74

```python
class EMACrossoverParams(StrategyParams):
    """Parámetros de EMA Crossover."""

    fast: int = Field(12, ge=2, le=500)
    slow: int = Field(26, ge=3, le=1000)
    trend_ema: int | None = Field(200, ge=10, le=2000)
    regime_filter: Literal["none", "adx", "atr"] = "adx"
    adx_period: int = Field(14, ge=2, le=200)
    adx_min: float = Field(20.0, ge=0, le=100)
    atr_pct_min: float = Field(0.002, ge=0)

    @model_validator(mode="after")
    def _fast_lt_slow(self) -> EMACrossoverParams:
        if self.fast >= self.slow:
            raise ValueError("fast debe ser menor que slow")
        return self


@register
class EMACrossoverStrategy(Strategy):
    """Cruce de EMAs con filtro de tendencia larga y de régimen."""

    name = "ema_crossover"
    category = Category.TREND
    description = "Cruce EMA rápida/lenta con filtro de tendencia y de lateralidad"
    params_model = EMACrossoverParams
    params: EMACrossoverParams

    def warmup_bars(self) -> int:
        p = self.params
        return max(p.slow, p.trend_ema or 0, 2 * p.adx_period, p.atr_period) + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        fast, slow = ema(c, p.fast), ema(c, p.slow)
        up_ok = pd.Series(True, index=c.index)
        dn_ok = pd.Series(True, index=c.index)
        if p.trend_ema:
            trend = ema(c, p.trend_ema)
            up_ok, dn_ok = c > trend, c < trend
        adx_df = adx(data, p.adx_period)
        if p.regime_filter == "adx":
            regime = adx_df["adx"] >= p.adx_min
        elif p.regime_filter == "atr":
            regime = atr(data, p.atr_period) / c >= p.atr_pct_min
        else:
            regime = pd.Series(True, index=c.index)
        return Events(
            long_entry=crossover(fast, slow) & up_ok & regime,
            short_entry=crossunder(fast, slow) & dn_ok & regime,
            long_exit=crossunder(fast, slow),
            short_exit=crossover(fast, slow),
            conviction=(adx_df["adx"] / 50).clip(0, 1),
        )
```

- **Líneas 20–35:** `EMACrossoverParams` **hereda** de `StrategyParams`. Recibe los parámetros
  comunes (stop, take-profit...) y añade los suyos (`fast`, `slow`...).
- **Línea 38:** `@register` la añade al registro.
- **Líneas 42–46:** redefine los atributos de clase.
- **Líneas 52–74:** implementa `compute_events`, la parte específica de esta estrategia.

### Polimorfismo en acción

`generate_signals` está escrita **una sola vez** en la clase base. Dentro llama a
`self.compute_events(data)`. Cuando el objeto es una `EMACrossoverStrategy`, se ejecuta su
versión; cuando es una `RSIReversionStrategy`, la suya. El motor y el flujo de investigación
llaman a `generate_signals` sin saber de qué estrategia se trata.

<!-- ejecutar -->
```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import Strategy, available_strategies, create_strategy

datos = generate_synthetic_ohlcv(bars=600, seed=3)
for nombre in available_strategies()[:3]:
    estrategia = create_strategy(nombre)
    senales = estrategia.generate_signals(datos)          # misma llamada, distinto comportamiento
    print(nombre, isinstance(estrategia, Strategy), int((senales["signal"] != 0).sum()))
try:
    Strategy()
except TypeError as error:
    print("No se puede instanciar la clase abstracta:", str(error)[:60])
```
<!-- salida -->
```text
adx_di True 335
bollinger_reversion True 134
donchian_breakout True 417
No se puede instanciar la clase abstracta: Can't instantiate abstract class Strategy without an impleme
```

El número de cada línea es la cantidad de velas, de 600, en las que esa estrategia quería estar
posicionada (señal distinta de 0). Cada estrategia da un número distinto con la misma llamada:
eso es el polimorfismo.

### Composición y encapsulación en el motor

`BacktestEngine` no hereda de nada relevante: **contiene** una configuración, una especificación
de instrumento y un `CostModel`, y delega en ellos. Sus métodos internos `_open`, `_close` y
`_map_funding` empiezan por `_`: son detalles de implementación que nadie fuera del motor
debería llamar (Módulo X).

**[Diseño]** ¿Por qué herencia para las estrategias y composición para el motor? Todas las
estrategias comparten exactamente la misma "forma" (entrada OHLCV, salida de señales, conversión
eventos → estado), así que la herencia evita repetir esa lógica diez veces. El motor, en cambio,
combina piezas independientes (costes, riesgo, ejecución) que pueden cambiarse por separado.

---

## 2.12 Decoradores

### La idea

Un **decorador** es una función que recibe otra función o clase y devuelve una versión
modificada o "anotada" de ella. Se escribe con `@` justo encima. Ya has visto varios:
`@dataclass`, `@property`, `@classmethod`, `@abstractmethod`.

El proyecto define uno propio, `@register`:

<!-- cita: src/bybit_quant_lab/strategies/registry.py#L9-L22 -->
`src/bybit_quant_lab/strategies/registry.py` · líneas 9–22

```python
_REGISTRY: dict[str, type[Strategy]] = {}


def register(cls: type[Strategy]) -> type[Strategy]:
    """Decorador que registra una estrategia por su atributo ``name``."""
    if cls.name in _REGISTRY and _REGISTRY[cls.name] is not cls:
        raise ValueError(f"Estrategia duplicada: {cls.name}")
    _REGISTRY[cls.name] = cls
    return cls


def available_strategies() -> list[str]:
    """Nombres de estrategias registradas, en orden de registro."""
    return list(_REGISTRY)
```

Escribir

```python
@register
class EMACrossoverStrategy(Strategy):
    ...
```

equivale exactamente a

```python
class EMACrossoverStrategy(Strategy):
    ...
EMACrossoverStrategy = register(EMACrossoverStrategy)
```

`register` guarda la clase en el diccionario `_REGISTRY` bajo su nombre y la devuelve sin
cambios. El guion bajo de `_REGISTRY` indica que es interno: desde fuera se consulta con
`available_strategies()` y `create_strategy()`.

### Comprobación

¿Qué ocurre si dos clases distintas usan el mismo `name = "ema_crossover"`?

<details><summary>Ver respuesta</summary>

La segunda llamada a `register` encuentra el nombre ya ocupado por otra clase (`is not cls`) y
lanza `ValueError("Estrategia duplicada: ema_crossover")` al importar el módulo.
</details>

---

## 2.13 Enumeraciones

### La idea

Una **enumeración** (enum) es un conjunto cerrado de valores con nombre. En vez de escribir
`1`, `-1` y `0` en todas partes (y equivocarse alguna vez), se definen nombres:

<!-- cita: src/bybit_quant_lab/strategies/base.py#L46-L59 -->
`src/bybit_quant_lab/strategies/base.py` · líneas 46–59

```python
class Signal(IntEnum):
    """Señal normalizada."""

    SHORT = -1
    FLAT = 0
    LONG = 1


class Category(StrEnum):
    """Categoría de estrategia (usada por el consenso por categorías)."""

    VOLUME = "volume"
    TREND = "trend"
    INDICATOR = "indicator"
```

- `IntEnum` hace que `Signal.LONG` **sea** también el entero `1`, así que se puede comparar y
  operar con números.
- `StrEnum` hace que `Category.TREND` **sea** también el texto `"trend"`.

<!-- ejecutar -->
```python
from bybit_quant_lab.strategies.base import Category, Signal

print(Signal.LONG == 1, Signal.SHORT + Signal.LONG, Signal(-1).name)
print(Category.TREND == "trend", [c.value for c in Category])
```
<!-- salida -->
```text
True 0 SHORT
True ['volume', 'trend', 'indicator']
```

**[Hecho] Observación de revisor:** la clase `Signal` está definida y se exporta, pero **ningún
archivo de `src/` la usa** (compruébalo con `grep -rn "Signal\." src`). Las estrategias y el
motor escriben directamente `1`, `-1` y `0` en la columna `signal`, porque trabajan con arrays de
NumPy. La enum documenta el significado de esos números, pero no los protege: nada impide que una
estrategia escriba un `2` por error. La protección real es la prueba
`test_output_contract` (`tests/unit/test_strategies.py`), que comprueba que las señales solo
toman los valores −1, 0 y 1.

---

## 2.14 Type hints: anotaciones de tipo

### La idea

Las **anotaciones de tipo** (type hints) indican qué tipo se espera en cada parámetro y valor de
retorno. **Python no las comprueba al ejecutar**: son documentación que lee una herramienta
externa, MyPy (Módulo XIV), para detectar errores antes de ejecutar.

| Anotación | Significa |
|---|---|
| `x: int` | `x` es un entero |
| `x: float \| None` | un decimal o `None` ("opcional") |
| `x: list[float]` | una lista de decimales |
| `x: dict[str, Any]` | un diccionario con claves de texto y valores de cualquier tipo |
| `x: Literal["none", "adx", "atr"]` | solo uno de esos tres textos |
| `ClassVar[str]` | atributo de clase, no de instancia |
| `-> pd.DataFrame` | la función devuelve un DataFrame |

Un uso avanzado es el **Protocol**: describe "cualquier objeto que tenga estos métodos", sin
exigir que herede de nada:

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L37-L42 -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 37–42

```python
class HTTPSession(Protocol):
    """Interfaz mínima de sesión HTTP (permite inyectar dobles de prueba)."""

    def get(self, url: str, params: dict[str, Any], timeout: float) -> Any:
        """Realiza una petición GET."""
        ...
```

El cliente acepta como sesión HTTP **cualquier** objeto con un método `get(url, params,
timeout)`. En producción es una `requests.Session`; en las pruebas es una clase falsa que
devuelve respuestas inventadas sin usar la red (Módulo IV, sección 4.12). Esta técnica se
llama **inyección de dependencias** y es la razón de que el cliente pueda probarse sin conexión.

<!-- ejecutar -->
```python
def doble(x: int) -> int:
    return x * 2

print(doble(3), doble("ab"))   # Python no impide pasar un texto: las anotaciones no se comprueban al ejecutar
```
<!-- salida -->
```text
6 abab
```

MyPy sí señalaría `doble("ab")` como error. Por eso el proyecto ejecuta MyPy además de las
pruebas.

---

## 2.15 Modelos de configuración con Pydantic

### La idea

Los parámetros vienen de archivos YAML escritos por personas, y las personas se equivocan
(`stop_atr_mult: -2`, `fasst: 12`...). **Pydantic** es una biblioteca que define modelos de datos
con reglas de validación: si un valor no cumple las reglas, se rechaza **con un mensaje claro
antes de empezar**, en lugar de producir resultados absurdos horas después.

Los parámetros comunes de todas las estrategias:

<!-- cita: src/bybit_quant_lab/strategies/base.py#L62-L73 -->
`src/bybit_quant_lab/strategies/base.py` · líneas 62–73

```python
class StrategyParams(BaseModel):
    """Parámetros comunes de salida y gestión de la operación."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    atr_period: int = Field(14, ge=2, le=500)
    stop_atr_mult: float = Field(2.0, gt=0, le=20)
    take_profit_r: float | None = Field(2.0, gt=0, le=50)
    trailing_atr_mult: float | None = Field(None, gt=0, le=20)
    max_holding_bars: int | None = Field(None, ge=1)
    cooldown_bars: int = Field(0, ge=0)
    allow_short: bool = True
```

- `BaseModel` es la clase base de Pydantic.
- `extra="forbid"`: un parámetro desconocido (por ejemplo, una errata) es un error.
- `frozen=True`: los parámetros no se pueden modificar tras crearlos.
- `Field(14, ge=2, le=500)`: valor por defecto 14, mayor o igual que 2 (`ge`) y menor o igual que
  500 (`le`). `gt` y `lt` son "estrictamente mayor/menor".

Las reglas que relacionan varios campos se escriben con `@model_validator`. La configuración
global impide, por ejemplo, un apalancamiento superior al máximo de riesgo:

<!-- cita: src/bybit_quant_lab/config/models.py#L110-L128 -->
`src/bybit_quant_lab/config/models.py` · líneas 110–128

```python
class AppConfig(_Strict):
    """Configuración completa del experimento."""

    data: DataConfig = DataConfig()
    costs: CostConfig = CostConfig()
    execution: ExecutionConfig = ExecutionConfig()
    risk: RiskConfig = RiskConfig()
    backtest: BacktestConfig = BacktestConfig()
    validation: ValidationConfig = ValidationConfig()
    output_dir: Path = Path("outputs")

    @model_validator(mode="after")
    def _check_leverage(self) -> AppConfig:
        if self.execution.leverage > self.risk.max_leverage:
            raise ValueError(
                f"execution.leverage={self.execution.leverage} supera "
                f"risk.max_leverage={self.risk.max_leverage}"
            )
        return self
```

<!-- ejecutar -->
```python
from pydantic import ValidationError

from bybit_quant_lab.strategies import create_strategy

print(create_strategy("ema_crossover", {"fast": 8}).params.fast)
for erroneo in ({"fasst": 8}, {"fast": 30, "slow": 26}, {"stop_atr_mult": -1}):
    try:
        create_strategy("ema_crossover", erroneo)
    except ValidationError as error:
        print(erroneo, "->", error.errors()[0]["msg"])
```
<!-- salida -->
```text
8
{'fasst': 8} -> Extra inputs are not permitted
{'fast': 30, 'slow': 26} -> Value error, fast debe ser menor que slow
{'stop_atr_mult': -1} -> Input should be greater than 0
```

**[Limitación]** La validación se aplica al **crear** el objeto. Si un programa copia una
configuración con `model_copy(update=...)`, Pydantic no vuelve a validarla. La auditoría lo
documenta como hallazgo B-06; desde YAML y la CLI no ocurre (Módulo XVII).

---

## 2.16 Context managers: `with`

### La idea

Algunos recursos deben **liberarse** siempre, aunque ocurra un error: un archivo abierto debe
cerrarse. La instrucción `with` garantiza que se libere al salir del bloque, pase lo que pase.

<!-- cita: src/bybit_quant_lab/validation/experiment_log.py#L24-L28 -->
`src/bybit_quant_lab/validation/experiment_log.py` · líneas 24–28

```python
    def append(self, record: dict[str, Any]) -> None:
        """Añade un registro con marca temporal UTC."""
        rec = {"logged_at": datetime.now(UTC).isoformat(), **record}
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, default=str, sort_keys=True) + "\n")
```

`self.path.open("a")` abre el archivo para **añadir** al final (`"a"` de append). Al terminar el
bloque `with`, Python lo cierra automáticamente. Sin `with`, un error a mitad de escritura podría
dejar el archivo abierto.

El proyecto también usa `with np.errstate(...)` en los indicadores para silenciar avisos de
división por cero **solo dentro de ese bloque** (Módulo VII): es un context manager que cambia
una configuración temporalmente y la restaura al salir.

---

## 2.17 Iteradores y utilidades de iteración

### La idea

Un **iterador** es un objeto que entrega elementos uno a uno (`for` usa iteradores por dentro).
Dos herramientas útiles que aparecen en el proyecto:

- `zip(a, b, strict=True)`: recorre dos secuencias a la vez; con `strict=True` lanza un error si
  tienen distinta longitud (así se detectan desajustes silenciosos).
- `itertools.pairwise(x)`: produce pares consecutivos `(x0, x1), (x1, x2), ...`.

El descargador usa `pairwise` para encontrar huecos entre velas consecutivas:

<!-- cita: src/bybit_quant_lab/data/downloader.py#L55-L57 -->
`src/bybit_quant_lab/data/downloader.py` · líneas 55–57

```python
    for a, b in itertools.pairwise(idx):
        if b - a > delta:
            ranges.append((a + delta, b))
```

<!-- ejecutar -->
```python
import itertools

horas = [0, 1, 2, 5, 6]
for a, b in itertools.pairwise(horas):
    if b - a > 1:
        print(f"hueco entre la hora {a} y la hora {b}: faltan {b - a - 1} velas")
```
<!-- salida -->
```text
hueco entre la hora 2 y la hora 5: faltan 2 velas
```

---

## 2.18 Programación orientada a objetos frente a programación funcional

### La idea

- **Funcional:** funciones "puras" que reciben datos y devuelven un resultado **sin modificar
  nada más**. Si les das lo mismo, devuelven lo mismo.
- **Orientada a objetos:** objetos con estado que cambia con el tiempo.

El proyecto mezcla ambos estilos **a propósito**:

| Parte | Estilo | Por qué |
|---|---|---|
| `indicators/core.py` | Funcional (`ema(serie, n)` devuelve otra serie) | Fácil de probar y de razonar: sin estado oculto, el mismo dato produce siempre el mismo indicador |
| `strategies/` | Objetos inmutables con un método puro | Los parámetros viajan con la estrategia, pero `generate_signals` no cambia el objeto |
| `backtesting/engine.py`, `portfolio/` | Orientado a objetos con estado | Una simulación **es** un estado que evoluciona: efectivo, posición, límites de riesgo |
| `validation/research.py` | Un objeto `Researcher` que orquesta | Guarda datos, configuración y segmentos para no repetirlos en cada llamada |

---

## 2.19 Entornos virtuales, dependencias y ejecución de comandos

### La idea

Un proyecto depende de bibliotecas concretas en versiones concretas (pandas, numpy...). Si
instalas todo en el Python del sistema, distintos proyectos se pisan entre sí. Un **entorno
virtual** es una carpeta (`.venv/`) con un Python y unas bibliotecas propias del proyecto.

```bash
cd bybit-quant-lab
python3 -m venv .venv            # 1. crea el entorno (una vez)
source .venv/bin/activate        # 2. lo activa (cada vez que abres una terminal; en Windows: .venv\Scripts\activate)
pip install -e ".[dev]"          # 3. instala el proyecto y las herramientas de desarrollo
bql list-strategies              # 4. comprueba que funciona
```

- `pip` es el instalador de paquetes de Python.
- `-e` ("editable") instala el proyecto apuntando a tu carpeta `src/`: los cambios que hagas en
  el código se ven sin reinstalar.
- `".[dev]"` instala también las dependencias opcionales del grupo `dev` (pytest, ruff, mypy...).

Las dependencias están declaradas en `pyproject.toml`:

<!-- cita: pyproject.toml#L5-L32 -->
`pyproject.toml` · líneas 5–32

```toml
[project]
name = "bybit-quant-lab"
version = "0.1.0"
description = "Framework de investigación y backtesting para futuros perpetuos lineales de Bybit (solo lectura, sin ejecución real)."
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
dependencies = [
    "numpy>=2.0,<3",
    "pandas>=2.2,<4",
    "pydantic>=2.7,<3",
    "pyarrow>=16",
    "matplotlib>=3.8,<4",
    "jinja2>=3.1,<4",
    "pyyaml>=6.0,<7",
    "requests>=2.31,<3",
]

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "ruff>=0.5",
    "mypy>=1.10",
    "pandas-stubs>=2.2",
    "types-requests>=2.31",
    "types-PyYAML>=6.0",
]

```

Los rangos como `pandas>=2.2,<4` permiten actualizaciones compatibles y evitan una versión mayor
futura que podría romper el código. La sección `[project.scripts]` crea la orden `bql`, que
llama a la función `main` de `bybit_quant_lab/cli.py`.

---

## 2.20 Cómo leer un error (traceback)

### La idea

Cuando una excepción no se captura, Python imprime una **traza** (traceback): la cadena de
llamadas que llevó al error. Se lee **de abajo arriba**:

1. La **última línea** dice el tipo de error y el mensaje. Empieza siempre por ahí.
2. Las líneas de encima muestran qué función llamó a cuál. La más baja que pertenezca a **tu**
   código (`src/bybit_quant_lab/...`) suele ser el mejor punto para investigar.

<!-- ejecutar -->
```python
import traceback

from bybit_quant_lab.strategies import create_strategy

try:
    create_strategy("ema_cruce")
except KeyError:
    lineas = traceback.format_exc().strip().splitlines()
    print(lineas[0])
    print("...")
    print(lineas[-1])
```
<!-- salida -->
```text
Traceback (most recent call last):
...
KeyError: "Estrategia desconocida: 'ema_cruce'. Disponibles: ['adx_di', 'bollinger_reversion', 'donchian_breakout', 'ema_crossover', 'macd_momentum', 'obv_trend', 'rsi_reversion', 'stoch_rsi', 'volume_spike', 'vwap_deviation']"
```

La última línea dice exactamente qué pasó (no existe la estrategia `ema_cruce`) y ofrece la lista
de nombres válidos. Ese mensaje existe porque `get_strategy_class` (sección 2.7) re-lanza el
error con contexto.

**Método para depurar cualquier error:**

1. Lee la última línea: tipo y mensaje.
2. Busca la línea más baja de la traza dentro de `src/bybit_quant_lab/`.
3. Abre ese archivo en esa línea y lee qué valor esperaba.
4. Reproduce el error con el ejemplo más pequeño posible (el Módulo XIV enseña a convertirlo en
   una prueba).

### Comprobación final del módulo

Lee esta línea: `raise ValueError(f"Temporalidad no soportada: {timeframe!r}. Opciones: {list(TIMEFRAMES)}")`.
Explica con tus palabras qué la dispara, qué tipo de error lanza y qué información incluye el
mensaje.

<details><summary>Ver respuesta</summary>

Está en `validate_timeframe` y se dispara cuando la temporalidad pedida no es una clave del
diccionario `TIMEFRAMES`. Lanza `ValueError` (valor inválido) con un mensaje que incluye el valor
recibido entre comillas (`!r`) y la lista de temporalidades permitidas.
</details>
