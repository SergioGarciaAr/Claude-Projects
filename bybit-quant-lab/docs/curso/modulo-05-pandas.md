# Módulo V. pandas, NumPy y series temporales

Casi todo el cálculo del proyecto pasa por dos bibliotecas: **NumPy**, para operar con arrays de
números a gran velocidad, y **pandas**, para trabajar con tablas cuyas filas tienen una fecha.
Este módulo enseña lo imprescindible con ejemplos pequeños, todos ejecutados, y termina con los
dos peligros que más afectan a un backtest: los valores ausentes y los huecos de tiempo.

---

## 5.1 Array, Series y DataFrame

### La idea

- Un **array** de NumPy es una lista de números del **mismo tipo**, guardada en un bloque de
  memoria contiguo. Las operaciones se aplican a todos los elementos a la vez, a velocidad de
  código compilado.
- Una **Series** de pandas es un array con **etiquetas** (un **índice**) en cada elemento. En
  este proyecto, la etiqueta es casi siempre una fecha.
- Un **DataFrame** es una tabla: varias Series que comparten el mismo índice, una por columna.

Analogía: el array es una fila de cajones numerados del 0 al N; la Series pone una etiqueta con
la fecha en cada cajón; el DataFrame es un armario con varias filas de cajones, todas con las
mismas etiquetas.

<!-- ejecutar -->
```python
import numpy as np
import pandas as pd

precios = np.array([100.0, 101.5, 99.0, 102.0])
print(precios * 2, precios.mean(), precios.dtype)

fechas = pd.date_range("2024-01-01", periods=4, freq="1h", tz="UTC")
cierre = pd.Series(precios, index=fechas, name="close")
print(cierre)

velas = pd.DataFrame({"close": precios, "volume": [5, 7, 3, 9]}, index=fechas)
print(velas.shape, list(velas.columns))
```
<!-- salida -->
```text
[200. 203. 198. 204.] 100.625 float64
2024-01-01 00:00:00+00:00    100.0
2024-01-01 01:00:00+00:00    101.5
2024-01-01 02:00:00+00:00     99.0
2024-01-01 03:00:00+00:00    102.0
Freq: h, Name: close, dtype: float64
(4, 2) ['close', 'volume']
```

`shape` es `(filas, columnas)`. Una columna de un DataFrame es una Series: `velas["close"]`.

---

## 5.2 Columnas, índices y tipos de datos

Cada columna tiene un **tipo** (`dtype`): `float64` (decimal de 64 bits), `int64` (entero),
`bool`, `object` (cualquier objeto de Python, lento), `datetime64[...]` (fechas).

**[Hecho]** Las velas del proyecto tienen siempre: índice `open_time` de tipo
`datetime64[..., UTC]` y columnas `open, high, low, close, volume, turnover` de tipo `float64`.
Lo garantiza la conversión final de `_parse_klines` (Módulo IV, sección 4.9) y la limpieza
(`clean_ohlcv`).

**Por qué importan los tipos:** un precio guardado como texto (`"42350.5"`) no se puede sumar.
`pd.to_numeric(..., errors="coerce")` convierte textos en números y lo que no se puede convertir
en `NaN` (sección 5.7).

<!-- ejecutar -->
```python
import pandas as pd

como_texto = pd.Series(["42350.5", "42400", "error"])
print(como_texto.dtype)
numeros = pd.to_numeric(como_texto, errors="coerce")
print(numeros.tolist(), numeros.dtype)
```
<!-- salida -->
```text
str
[42350.5, 42400.0, nan] float64
```

En pandas 3 una columna de textos tiene el tipo `str` (en versiones anteriores aparecía como
`object`). En la salida de arriba, la primera línea muestra ese tipo antes de la conversión.

---

## 5.3 Índices temporales y su resolución

Un `DatetimeIndex` es un índice de fechas. Permite seleccionar por fechas, calcular diferencias
de tiempo y agrupar por día. Dos atributos importan:

- **Zona horaria** (`tz`): el proyecto exige UTC.
- **Resolución**: la unidad en que se guarda internamente (nanosegundos `ns`, microsegundos
  `us`, milisegundos `ms`...). pandas 3 puede usar distintas resoluciones según el origen.

### Un error real causado por la resolución

**[Hecho]** Durante el desarrollo, el motor calculaba el día UTC de cada vela dividiendo el
número interno del índice entre los nanosegundos de un día. Funcionaba con índices en `ns`, pero
los Parquet se cargaban en `ms`: el "día" cambiaba cada mil días, la referencia de pérdida
diaria no se reiniciaba y el límite diario saltaba sin motivo. Se detectó porque una estrategia
dio resultados distintos antes y después de una optimización, y se corrigió en el commit
`2f60aca` con un cálculo independiente de la resolución:

<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L109-L112 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 109–112

```python
        # Identificador de día UTC independiente de la resolución del índice (ns, us, ms...).
        day_ids = (
            idx.floor("D").as_unit("s").tz_convert(None).to_numpy().astype("int64") // 86_400
        ).tolist()
```

`floor("D")` lleva cada fecha a la medianoche de su día; `as_unit("s")` fija la resolución en
segundos **antes** de convertir a número; al dividir entre 86.400 (segundos de un día) se obtiene
un número de día que no depende de la resolución original. La prueba de regresión
`test_daily_reference_resets_regardless_of_index_resolution` (`tests/unit/test_risk.py`) repite
el escenario con resoluciones `ns`, `us`, `ms` y `s`.

<!-- ejecutar -->
```python
import pandas as pd

idx = pd.date_range("2024-01-01 22:00", periods=4, freq="1h", tz="UTC")
for unidad in ("ns", "ms"):
    i = idx.as_unit(unidad)
    ingenuo = (i.asi8 // 86_400_000_000_000).tolist()         # supone nanosegundos
    correcto = (i.floor("D").as_unit("s").tz_convert(None).to_numpy().astype("int64") // 86_400).tolist()
    print(unidad, "ingenuo:", ingenuo, "| correcto:", correcto)
```
<!-- salida -->
```text
ns ingenuo: [19723, 19723, 19724, 19724] | correcto: [19723, 19723, 19724, 19724]
ms ingenuo: [0, 0, 0, 0] | correcto: [19723, 19723, 19724, 19724]
```

Con `ms`, el cálculo ingenuo da el mismo "día" (0) a todas las velas, aunque pasan de un día a
otro. La lección general: **no supongas la unidad interna de una fecha**.

---

## 5.4 Seleccionar y filtrar filas

| Forma | Ejemplo | Selecciona por |
|---|---|---|
| `df["col"]` | `velas["close"]` | Nombre de columna |
| `df.loc[etiqueta]` | `velas.loc["2024-01-01 01:00"]` | Etiqueta del índice (fecha) |
| `df.iloc[posición]` | `velas.iloc[0]`, `velas.iloc[-1]` | Posición numérica (0 = primera, −1 = última) |
| Máscara booleana | `velas[velas["close"] > 100]` | Condición fila a fila |

Una **máscara booleana** es una Series de `True/False` del mismo tamaño que la tabla; al usarla
como filtro, solo quedan las filas `True`. Las condiciones se combinan con `&` (y), `|` (o) y `~`
(no), siempre entre paréntesis.

El cliente de Bybit usa máscaras para recortar el rango y descartar velas abiertas:

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L172-L174 -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 172–174

```python
        df = df[(df.index >= start) & (df.index < end)]
        closed = df.index + delta <= now
        return df[closed]
```

<!-- ejecutar -->
```python
import pandas as pd

fechas = pd.date_range("2024-01-01", periods=5, freq="1h", tz="UTC")
velas = pd.DataFrame({"close": [100, 103, 99, 104, 101.0]}, index=fechas)
print(velas.iloc[-1]["close"], velas.loc["2024-01-01 02:00", "close"])
sube = velas["close"] > velas["close"].shift(1)
print(velas[sube & (velas["close"] > 100)])
```
<!-- salida -->
```text
101.0 99.0
                           close
2024-01-01 01:00:00+00:00  103.0
2024-01-01 03:00:00+00:00  104.0
```

---

## 5.5 Ordenar, concatenar y eliminar duplicados

- `pd.concat([a, b])` **apila** tablas una debajo de otra.
- `df.index.duplicated(keep="last")` marca como `True` las repeticiones de una misma fecha salvo
  la última.
- `df.sort_index()` ordena por el índice (cronológicamente).

El cliente une las ventanas descargadas con exactamente esas tres operaciones:

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L170-L171 -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 170–171

```python
        df = pd.concat(frames)
        df = df[~df.index.duplicated(keep="last")].sort_index()
```

<!-- ejecutar -->
```python
import pandas as pd

def tabla(horas, cierres):
    idx = pd.to_datetime(horas).tz_localize("UTC")
    return pd.DataFrame({"close": cierres}, index=idx)

ventana_2 = tabla(["2024-01-01 02:00", "2024-01-01 03:00"], [102.0, 103.0])
ventana_1 = tabla(["2024-01-01 00:00", "2024-01-01 01:00", "2024-01-01 02:00"], [100.0, 101.0, 102.5])
unidas = pd.concat([ventana_2, ventana_1])
print(unidas.index.strftime("%H:%M").tolist())
limpias = unidas[~unidas.index.duplicated(keep="last")].sort_index()
print(limpias)
```
<!-- salida -->
```text
['02:00', '03:00', '00:00', '01:00', '02:00']
                           close
2024-01-01 00:00:00+00:00  100.0
2024-01-01 01:00:00+00:00  101.0
2024-01-01 02:00:00+00:00  102.5
2024-01-01 03:00:00+00:00  103.0
```

La vela de las 02:00 aparecía dos veces; se conservó la última aparición (102,5) y el resultado
quedó ordenado.

---

## 5.6 Operaciones vectorizadas

### La idea

**Vectorizar** es escribir una operación sobre la columna entera en lugar de un bucle elemento a
elemento. Es más corto y, sobre todo, mucho más rápido, porque el bucle se ejecuta dentro de
NumPy (código compilado) y no en Python.

El *true range* (Módulo VII) se calcula vectorizado:

<!-- cita: src/bybit_quant_lab/indicators/core.py#L41-L48 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 41–48

```python
def true_range(df: pd.DataFrame) -> pd.Series:
    """True Range: ``max(h-l, |h-c_prev|, |l-c_prev|)``."""
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [df["high"] - df["low"], (df["high"] - prev_close).abs(), (df["low"] - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    return tr.rename("tr")
```

Tres Series se calculan de una vez, `pd.concat(..., axis=1)` las pone lado a lado como columnas y
`.max(axis=1)` toma el máximo **de cada fila**.

<!-- ejecutar -->
```python
import time

import numpy as np

x = np.random.default_rng(0).normal(size=1_000_000)
t0 = time.perf_counter()
bucle = [v * 2 + 1 for v in x]
t1 = time.perf_counter()
vector = x * 2 + 1
t2 = time.perf_counter()
print("mismos resultados:", np.allclose(bucle, vector))
print("el bucle es más lento que la versión vectorizada:", (t1 - t0) > (t2 - t1))
```
<!-- salida -->
```text
mismos resultados: True
el bucle es más lento que la versión vectorizada: True
```

(Los tiempos exactos varían entre ordenadores, por eso el ejemplo solo imprime la comparación.)

**[Diseño]** El motor de backtesting **no** está vectorizado: recorre las velas una a una con un
bucle, porque cada vela depende del estado que dejó la anterior (posición abierta, stops,
límites de riesgo). Para acelerar ese bucle, convierte las columnas a arrays de NumPy antes de
empezar, ya que acceder a un elemento de un array es mucho más rápido que a uno de una Series:

<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L93-L101 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 93–101

```python
        o = data["open"].to_numpy(float)
        h = data["high"].to_numpy(float)
        low = data["low"].to_numpy(float)
        c = data["close"].to_numpy(float)
        sig = signals["signal"].to_numpy(np.int64)
        conv = signals["conviction"].to_numpy(float)
        stop_d = signals["stop_distance"].to_numpy(float)
        tp_d = signals["take_profit_distance"].to_numpy(float)
        tr_d = signals["trailing_distance"].to_numpy(float)
```

---

## 5.7 Valores nulos (NaN) y cómo se propagan

### La idea

`NaN` ("Not a Number") representa un valor **ausente o indefinido**. En fechas, el equivalente
es `NaT`. Sus reglas son contraintuitivas:

1. Cualquier operación aritmética con `NaN` da `NaN`: `5 + NaN = NaN`. Se **propaga**.
2. Cualquier comparación con `NaN` da `False`: `NaN > 3` es `False`, y `NaN == NaN` también.
3. Las medias y sumas de pandas **ignoran** los `NaN` por defecto (`skipna=True`).

La regla 2 es la que más usa el proyecto: durante el **calentamiento** de un indicador (las
primeras velas, en las que todavía no hay datos suficientes) el indicador vale `NaN`, toda
comparación da `False` y, por tanto, **no se generan señales**. Es una protección automática.

Herramientas: `isna()` y `notna()` detectan ausentes, `fillna(v)` los sustituye y
`serie.where(condición, otro)` conserva los valores donde la condición es `True` y pone `otro`
donde es `False`.

El RSI usa `where` para tratar casos límite sin dividir entre cero:

<!-- cita: src/bybit_quant_lab/indicators/core.py#L56-L66 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 56–66

```python
def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    """RSI de Wilder en [0, 100]. Sin pérdidas -> 100; sin movimiento -> 50."""
    delta = close.diff()
    gain = wilder(delta.clip(lower=0), n)
    loss = wilder(-delta.clip(upper=0), n)
    with np.errstate(divide="ignore", invalid="ignore"):
        rs = gain / loss
        out = 100 - 100 / (1 + rs)
    out = out.where(loss != 0, 100.0)
    out = out.where(~((gain == 0) & (loss == 0)), 50.0)
    return out.where(gain.notna() & loss.notna()).rename("rsi")
```

- **61–63:** `np.errstate` silencia, **solo dentro del bloque**, los avisos de división por cero
  (un context manager, Módulo II, sección 2.16).
- **64:** donde no hubo pérdidas (`loss == 0`), el RSI es 100.
- **65:** donde no hubo ni ganancias ni pérdidas, el RSI es 50.
- **66:** donde falta información (calentamiento), el resultado se deja en `NaN`.

<!-- ejecutar -->
```python
import numpy as np
import pandas as pd

s = pd.Series([1.0, np.nan, 3.0])
print((s + 1).tolist(), (s > 2).tolist(), s.mean())
print(s.fillna(0).tolist(), s.where(s > 2, -1).tolist())
print(np.nan == np.nan)
```
<!-- salida -->
```text
[2.0, nan, 4.0] [False, False, True] 2.0
[1.0, 0.0, 3.0] [-1.0, -1.0, 3.0]
False
```

**[Hecho] Error frecuente:** `fillna(0)` en un precio convierte un dato ausente en un precio de
cero, que es un dato **falso**. El proyecto nunca rellena precios: la limpieza descarta las
velas con valores ausentes y deja el hueco a la vista.

---

## 5.8 Desplazamientos con `shift`: mirar al pasado

### La idea

`serie.shift(1)` desplaza los valores **una fila hacia abajo**: en la fila `t` aparece el valor
de `t−1`. Es la forma de preguntar "¿cuánto valía esto en la vela anterior?".

`shift(-1)` hace lo contrario: en la fila `t` aparece el valor de `t+1`, es decir, **el futuro**.
En una estrategia, usar `shift(-1)` es casi siempre un **look-ahead bias** (Módulo I, sección
1.4). **[Hecho]** El proyecto no contiene ningún `shift(-...)` en `src/`.

El canal de Donchian usa `shift(1)` para **excluir la vela actual** del canal:

<!-- cita: src/bybit_quant_lab/indicators/core.py#L145-L150 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 145–150

```python
def donchian(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Canal de Donchian de las ``n`` velas **anteriores** (excluye la vela actual)."""
    _check_period(n)
    upper = df["high"].rolling(n, min_periods=n).max().shift(1)
    lower = df["low"].rolling(n, min_periods=n).min().shift(1)
    return pd.DataFrame({"upper": upper, "lower": lower, "mid": (upper + lower) / 2})
```

Así, la pregunta "¿el cierre de hoy supera el máximo de las 20 velas **anteriores**?" no compara
la vela consigo misma.

Y la detección de cruces compara "ahora" con "antes":

<!-- cita: src/bybit_quant_lab/indicators/core.py#L171-L174 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 171–174

```python
def crossover(a: pd.Series, b: pd.Series | float) -> pd.Series:
    """True en ``t`` si ``a`` cruza por encima de ``b`` entre ``t-1`` y ``t``."""
    bb = b if isinstance(b, pd.Series) else pd.Series(b, index=a.index)
    return ((a > bb) & (a.shift(1) <= bb.shift(1))).fillna(False).astype(bool)
```

Un cruce al alza en `t` ocurre si `a` está por encima de `b` en `t` **y** estaba por debajo o
igual en `t−1`.

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.indicators import crossover

rapida = pd.Series([1.0, 2.0, 3.0, 4.0, 3.0])
lenta = pd.Series([2.5, 2.5, 2.5, 2.5, 3.5])
tabla = pd.DataFrame({"rapida": rapida, "rapida_ayer": rapida.shift(1), "lenta": lenta,
                      "cruce_al_alza": crossover(rapida, lenta)})
print(tabla)
```
<!-- salida -->
```text
   rapida  rapida_ayer  lenta  cruce_al_alza
0     1.0          NaN    2.5          False
1     2.0          1.0    2.5          False
2     3.0          2.0    2.5           True
3     4.0          3.0    2.5          False
4     3.0          4.0    3.5          False
```

Solo hay cruce en la fila 2, cuando la rápida pasa de 2,0 (por debajo de 2,5) a 3,0 (por
encima).

---

## 5.9 Ventanas móviles con `rolling`

### La idea

Una **ventana móvil** calcula una estadística sobre las últimas `n` filas, avanzando una fila
cada vez. `serie.rolling(3).mean()` es la media de las 3 últimas velas en cada punto.

- `min_periods=n` exige `n` valores válidos; antes devuelve `NaN` (calentamiento).
- Sin `center=True`, la ventana de la fila `t` termina en `t`: solo usa pasado y presente.
  **[Hecho]** El proyecto nunca usa `center=True`, que incluiría filas futuras.

<!-- cita: src/bybit_quant_lab/indicators/core.py#L23-L26 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 23–26

```python
def sma(s: pd.Series, n: int) -> pd.Series:
    """Media móvil simple de ``n`` velas (NaN hasta disponer de ``n`` valores)."""
    _check_period(n)
    return s.rolling(n, min_periods=n).mean()
```

<!-- ejecutar -->
```python
import pandas as pd

cierre = pd.Series([10.0, 11.0, 12.0, 13.0, 14.0])
print(pd.DataFrame({"cierre": cierre,
                    "media_3": cierre.rolling(3, min_periods=3).mean(),
                    "max_3": cierre.rolling(3, min_periods=3).max(),
                    "desv_3": cierre.rolling(3, min_periods=3).std(ddof=0).round(4)}))
```
<!-- salida -->
```text
   cierre  media_3  max_3  desv_3
0    10.0      NaN    NaN     NaN
1    11.0      NaN    NaN     NaN
2    12.0     11.0   12.0  0.8165
3    13.0     12.0   13.0  0.8165
4    14.0     13.0   14.0  0.8165
```

La media de la fila 2 es (10 + 11 + 12) / 3 = 11. Las dos primeras filas no tienen 3 valores y
quedan en `NaN`.

**`ddof`** ("delta degrees of freedom") decide si la desviación estándar divide entre `n`
(`ddof=0`, desviación **poblacional**) o entre `n−1` (`ddof=1`, desviación **muestral**). El
Módulo VI explica la diferencia. Las bandas de Bollinger del proyecto usan `ddof=0`; las métricas
de rendimiento usan `ddof=1`.

---

## 5.10 Medias exponenciales con `ewm`

### La idea

Una **media móvil exponencial** (EMA) da más peso a los datos recientes y nunca "olvida" del todo
los antiguos. Se calcula de forma **recursiva**: cada valor nuevo se mezcla con el valor
anterior de la media.

```text
EMA[t] = α · x[t] + (1 − α) · EMA[t−1]
```

`α` (alfa) es el peso del dato nuevo. Con `span=n`, pandas usa `α = 2 / (n + 1)`.

<!-- cita: src/bybit_quant_lab/indicators/core.py#L29-L38 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 29–38

```python
def ema(s: pd.Series, n: int) -> pd.Series:
    """Media móvil exponencial con ``alpha = 2/(n+1)``, recursiva (``adjust=False``)."""
    _check_period(n)
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def wilder(s: pd.Series, n: int) -> pd.Series:
    """Suavizado de Wilder (``alpha = 1/n``)."""
    _check_period(n)
    return s.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()
```

- `adjust=False` aplica exactamente la fórmula recursiva de arriba, empezando por el primer
  valor. **[Diseño]** Garantiza que el valor en `t` dependa solo de `x[0..t]`: si recortas la serie
  en `t`, los valores hasta `t` no cambian (es la base de las pruebas de ausencia de look-ahead).
- `wilder` es la misma idea con `α = 1/n`, el suavizado que usa J. Welles Wilder en el RSI, el
  ATR y el ADX (Módulo VII).

<!-- ejecutar -->
```python
import pandas as pd

x = pd.Series([10.0, 12.0, 11.0, 13.0])
alfa = 2 / (3 + 1)
manual = [float(x[0])]
for valor in x[1:]:
    manual.append(float(alfa * valor + (1 - alfa) * manual[-1]))
print("manual:", manual)
print("pandas:", x.ewm(span=3, adjust=False).mean().tolist())
```
<!-- salida -->
```text
manual: [10.0, 11.0, 11.0, 12.0]
pandas: [10.0, 11.0, 11.0, 12.0]
```

---

## 5.11 Agrupar y acumular: el VWAP de sesión

`groupby(clave).cumsum()` calcula una **suma acumulada que se reinicia** cada vez que cambia la
clave. El VWAP de sesión (Módulo VII) la usa con la clave "día UTC":

<!-- cita: src/bybit_quant_lab/indicators/core.py#L133-L142 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 133–142

```python
def vwap_session(df: pd.DataFrame, session: str = "1D") -> pd.Series:
    """VWAP anclado a sesiones UTC de duración ``session`` (por defecto, día UTC 00:00).

    El acumulado se reinicia en cada frontera de sesión; el valor en ``t`` incluye la vela ``t``.
    """
    tp = (df["high"] + df["low"] + df["close"]) / 3
    key = pd.DatetimeIndex(df.index).floor(session)
    pv = (tp * df["volume"]).groupby(key).cumsum()
    vol = df["volume"].groupby(key).cumsum()
    return (pv / vol.replace(0, np.nan)).rename("vwap")
```

<!-- ejecutar -->
```python
import pandas as pd

idx = pd.date_range("2024-01-01 22:00", periods=4, freq="1h", tz="UTC")
volumen = pd.Series([1.0, 2.0, 3.0, 4.0], index=idx)
dia = idx.floor("1D")
print(pd.DataFrame({"volumen": volumen, "acumulado_global": volumen.cumsum(),
                    "acumulado_por_dia": volumen.groupby(dia).cumsum()}))
```
<!-- salida -->
```text
                           volumen  acumulado_global  acumulado_por_dia
2024-01-01 22:00:00+00:00      1.0               1.0                1.0
2024-01-01 23:00:00+00:00      2.0               3.0                3.0
2024-01-02 00:00:00+00:00      3.0               6.0                3.0
2024-01-02 01:00:00+00:00      4.0              10.0                7.0
```

A las 00:00 del día 2 el acumulado por día vuelve a empezar desde 3.

---

## 5.12 Frecuencia temporal frente a número de observaciones: el problema de los huecos

### La idea

`rolling(20)` significa "las últimas **20 filas**", no "las últimas 20 horas". Si faltan velas,
esas 20 filas abarcan más tiempo del que crees.

<!-- ejecutar -->
```python
import pandas as pd

idx = pd.to_datetime(["2024-01-01 00:00", "2024-01-01 01:00", "2024-01-01 02:00",
                      "2024-01-01 09:00", "2024-01-01 10:00"]).tz_localize("UTC")
cierre = pd.Series([100.0, 101.0, 102.0, 110.0, 111.0], index=idx)
print(pd.DataFrame({"cierre": cierre,
                    "ultimas_3_filas": cierre.rolling(3).mean().round(2),
                    "ultimas_3_horas": cierre.rolling("3h").mean().round(2)}))
```
<!-- salida -->
```text
                           cierre  ultimas_3_filas  ultimas_3_horas
2024-01-01 00:00:00+00:00   100.0              NaN            100.0
2024-01-01 01:00:00+00:00   101.0              NaN            100.5
2024-01-01 02:00:00+00:00   102.0           101.00            101.0
2024-01-01 09:00:00+00:00   110.0           104.33            110.0
2024-01-01 10:00:00+00:00   111.0           107.67            110.5
```

A las 09:00, "las últimas 3 filas" mezcla precios de las 01:00, las 02:00 y las 09:00 (siete
horas de diferencia), mientras que "las últimas 3 horas" solo ve las 09:00.

**[Limitación]** Todos los indicadores del proyecto usan ventanas por número de filas. Con
huecos, los indicadores cruzan el hueco sin saberlo. Es la limitación M-06 de la auditoría: la
validación informa de los huecos, pero no impide simular sobre ellos. Revisa `gap_ranges` en
`bql validate-data` antes de confiar en un resultado.

---

## 5.13 Por qué el orden temporal es fundamental

`shift`, `rolling`, `ewm`, `diff` y `cumsum` asumen que la fila anterior es el momento anterior.
Con datos desordenados, todos dan resultados absurdos **sin lanzar ningún error**:

<!-- ejecutar -->
```python
import pandas as pd

idx = pd.date_range("2024-01-01", periods=4, freq="1h", tz="UTC")
cierre = pd.Series([100.0, 101.0, 102.0, 103.0], index=idx)
desordenada = cierre.iloc[[2, 0, 3, 1]]
print("rendimiento ordenado:   ", cierre.pct_change().round(4).tolist())
print("rendimiento desordenado:", desordenada.pct_change().round(4).tolist())
print("¿ordenada?", desordenada.index.is_monotonic_increasing)
```
<!-- salida -->
```text
rendimiento ordenado:    [nan, 0.01, 0.0099, 0.0098]
rendimiento desordenado: [nan, -0.0196, 0.03, -0.0194]
¿ordenada? False
```

Por eso el proyecto ordena al descargar, al limpiar y al cargar, y por eso las estrategias
comprueban `is_monotonic_increasing` antes de calcular (`strategies/base.py`, función
`validate_input`).

### Comprobación final del módulo

Tienes una Series `cierre`. Explica qué calcula cada expresión y cuál introduce look-ahead bias si
se usa para decidir en `t`: (a) `cierre.rolling(5).mean()`, (b) `cierre.shift(-1) > cierre`,
(c) `cierre.rolling(5, center=True).mean()`, (d) `cierre.diff()`.

<details><summary>Ver respuesta</summary>

(a) Media de las 5 últimas velas hasta `t`: sin look-ahead. (b) Compara el cierre de **mañana**
con el de hoy: look-ahead. (c) Ventana centrada, que incluye las dos velas siguientes:
look-ahead. (d) Diferencia entre el cierre de `t` y el de `t−1`: sin look-ahead.
</details>
