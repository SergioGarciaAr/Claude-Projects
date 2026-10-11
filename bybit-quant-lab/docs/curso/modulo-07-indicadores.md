# Módulo VII. Construcción matemática de los indicadores

Un **indicador** es un cálculo sobre precios y volúmenes pasados que resume una característica
del mercado: tendencia, volatilidad, impulso, participación... Las diez estrategias combinan
once indicadores. Todos están en `src/bybit_quant_lab/indicators/core.py` (208 líneas), salvo el
volumen relativo, que se calcula dentro de dos estrategias.

Cada sección sigue el mismo esquema: qué mide, intuición, fórmula, cálculo manual comparado con
la función real, implementación, parámetros, comportamiento al principio de la serie y con datos
ausentes, errores frecuentes, información del futuro que no debe usarse y limitaciones.

**[Hecho] Cómo se sabe que las fórmulas están bien implementadas.** El archivo
`tests/unit/test_audit_indicators.py` compara cada indicador con una implementación de referencia
escrita con bucles explícitos, sin pandas, con una tolerancia de 10⁻⁹. Además,
`tests/unit/test_strategies.py` comprueba que ningún indicador cambia sus valores pasados al
recortar o alterar los datos futuros.

---

## 7.0 Bloques comunes: SMA, EMA, suavizado de Wilder y la regla de causalidad

Los once indicadores se construyen con tres medias:

| Media | Fórmula | Función |
|---|---|---|
| Simple (SMA) | `SMA[t] = (x[t] + x[t−1] + ... + x[t−n+1]) / n` | `sma(s, n)` |
| Exponencial (EMA) | `EMA[t] = α·x[t] + (1−α)·EMA[t−1]`, con `α = 2/(n+1)` | `ema(s, n)` |
| Wilder | La misma recursión con `α = 1/n` | `wilder(s, n)` |

Las tres se explicaron con ejemplos en el Módulo V (secciones 5.9 y 5.10). La cabecera del
archivo resume las reglas que impiden usar información futura:

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/indicators/core.py#L1-L10 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 1–10

```python
"""Implementación vectorizada de indicadores.

Reglas de causalidad:

* Solo ``rolling``/``ewm`` hacia atrás, sin ``center=True`` ni ``bfill``.
* Las EMA usan ``adjust=False``: el valor en ``t`` depende únicamente de ``x[0..t]``, de modo
  que truncar la serie en ``t`` no cambia los valores hasta ``t``.
* Los canales que deben excluir la vela actual (Donchian) se desplazan una vela.
* Las series de temporalidad superior solo se exponen cuando la vela superior ha cerrado.
"""
```
<!-- fmt: on -->

### Convención de inicio: una diferencia con otras plataformas

**[Hecho] Variante implementada.** Las medias recursivas empiezan con el **primer valor válido**
(`adjust=False`) y se publican a partir de `n` valores (`min_periods=n`).

**Definición convencional de Wilder.** El valor inicial es la **media simple** de los primeros
`n` valores, y la recursión continúa desde ahí. Es la convención de TA-Lib y de muchas
plataformas de gráficos.

Ambas convenciones dan valores **distintos en las primeras velas** y convergen después, porque el
peso del valor inicial decae como `(1 − α)^t`. Para un ATR de 14 velas, tras unas 100 velas la
diferencia es despreciable:

<!-- ejecutar -->
```python
import numpy as np

from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.indicators import atr, true_range

datos = generate_synthetic_ohlcv(bars=300, seed=4)
tr = true_range(datos).to_numpy()
n = 14
clasico = np.full(len(tr), np.nan)
clasico[n - 1] = tr[:n].mean()  # semilla: media simple de los 14 primeros
for t in range(n, len(tr)):
    clasico[t] = clasico[t - 1] + (tr[t] - clasico[t - 1]) / n
proyecto = atr(datos, n).to_numpy()
for t in (13, 30, 100, 299):
    print(
        t,
        round(proyecto[t], 3),
        round(clasico[t], 3),
        f"diferencia {abs(proyecto[t] - clasico[t]) / clasico[t]:.2%}",
    )
```
<!-- salida -->
```text
13 343.425 342.653 diferencia 0.23%
30 342.363 342.144 diferencia 0.06%
100 341.571 341.57 diferencia 0.00%
299 534.714 534.714 diferencia 0.00%
```

**Consecuencia práctica:** si comparas los valores del proyecto con los de una plataforma de
gráficos, no coincidirán exactamente al principio de la serie. No es un error, sino una
convención distinta. Sí importa si una estrategia toma decisiones en esas primeras velas.

### El calentamiento real: NaN, no `warmup_bars`

Cada estrategia declara un método `warmup_bars()` con las velas que necesita para estabilizarse.
**[Hecho]** Ese método no lo llama **ningún** archivo del proyecto (compruébalo con
`grep -rn "warmup_bars()" src tests`). El calentamiento se gestiona solo:

1. Cada indicador vale `NaN` hasta tener `min_periods` datos.
2. Toda comparación con `NaN` es `False` (Módulo V, sección 5.7), así que no hay eventos.
3. Sin ATR válido, la clase base anula las entradas (sección 8.0).

**[Limitación]** "Válido" no significa "estable". Un indicador de Wilder publica su primer valor
a las `n` velas, pero con la convención de inicio del proyecto todavía arrastra el sesgo del
primer dato. El ADX necesita unas `2n` velas solo para tener su primer valor (sección 7.11). Las
primeras señales de cualquier serie se calculan con indicadores todavía poco fiables.

---

## 7.1 Volumen relativo (picos de volumen)

**Qué mide.** Cuánto volumen hubo en esta vela comparado con lo habitual en las anteriores.

**Intuición.** Un volumen tres veces mayor de lo normal indica que algo atrae a muchos
participantes. **No** dice en qué dirección.

**Fórmula.**

```text
vol_relativo[t] = V[t] / SMA(V, n)[t−1]
```

La media es la de las `n` velas **anteriores** (`shift(1)`). Si incluyera la vela actual, un pico
enorme subiría su propia media y se "escondería" en parte.

**Implementación** (dentro de la estrategia Volume Spike):

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/strategies/volume_spike.py#L49-L51 -->
`src/bybit_quant_lab/strategies/volume_spike.py` · líneas 49–51

```python
        vol_ma = sma(v, p.volume_window).shift(1)  # solo velas anteriores
        ratio = v / vol_ma.replace(0, np.nan)
        spike = ratio > p.spike_mult
```
<!-- fmt: on -->

`replace(0, np.nan)` evita dividir entre cero si el volumen medio fuera 0. La estrategia VWAP
Deviation usa el mismo cálculo en su línea 72.

**Cálculo manual.** Volúmenes `[10, 12, 8, 10, 40]`, `n = 4`. Para la última vela: media de las 4
anteriores `= (10 + 12 + 8 + 10) / 4 = 10`; volumen relativo `= 40 / 10 = 4`.

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.indicators import sma

v = pd.Series([10.0, 12.0, 8.0, 10.0, 40.0])
relativo = v / sma(v, 4).shift(1)
print(relativo.tolist())
print("incluyendo la vela actual:", (v / sma(v, 4)).round(3).tolist()[-1])
```
<!-- salida -->
```text
[nan, nan, nan, nan, 4.0]
incluyendo la vela actual: 2.286
```

Si la media incluyera la vela actual, el mismo pico parecería menor: 2,286 en lugar de 4.

**Parámetros.** `volume_window` (`n`, 20 por defecto) y `spike_mult` (umbral, 2,5).
**Inicio de la serie:** `NaN` hasta tener `n` velas previas. **Datos ausentes:** un volumen `NaN`
deja en `NaN` las medias que lo incluyen. **[Limitación]** Es el volumen de un solo exchange
(Bybit), no el del mercado completo.

---

## 7.2 On-Balance Volume (OBV)

**Qué mide.** Un total acumulado de volumen que suma en las velas que suben y resta en las que
bajan.

**Intuición.** Si el volumen se concentra en las subidas, el OBV crece: los compradores
"empujan". Se usa para ver si el volumen **confirma** la tendencia del precio.

**Fórmula.**

```text
OBV[0] = 0
OBV[t] = OBV[t−1] + signo(C[t] − C[t−1]) · V[t]
```

`signo` vale +1 si el cierre sube, −1 si baja y 0 si no cambia.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/indicators/core.py#L118-L121 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 118–121

```python
def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """On-Balance Volume acumulado desde el inicio de la serie (OBV[0] = 0)."""
    direction = np.sign(close.diff()).fillna(0.0)
    return (direction * volume).cumsum().rename("obv")
```
<!-- fmt: on -->

`close.diff()` es `C[t] − C[t−1]`; `np.sign` toma su signo; `fillna(0.0)` trata la primera vela
(sin anterior) como 0; `cumsum()` acumula.

**Cálculo manual.** Cierres `[10, 11, 10, 10, 12]`, volúmenes `[100, 200, 300, 400, 500]`:
`0 → +200 → −300 → 0 → +500`, acumulado `[0, 200, −100, −100, 400]`.

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.indicators import obv

print(obv(pd.Series([10, 11, 10, 10, 12.0]), pd.Series([100, 200, 300, 400, 500.0])).tolist())
```
<!-- salida -->
```text
[0.0, 200.0, -100.0, -100.0, 400.0]
```

**Detalle importante.** El **valor absoluto** del OBV depende de dónde empieza la serie: si
empiezas un día más tarde, toda la curva se desplaza. Por eso la estrategia solo usa sus
**cruces** con su propia media y su **pendiente**, que no dependen del punto de partida.
**[Limitación]** Una vela que sube un céntimo cuenta todo su volumen como "comprador": el OBV es
una aproximación tosca de la presión compradora.

---

## 7.3 VWAP y desviación respecto al VWAP

**Qué mide.** El precio medio ponderado por volumen: el precio al que, en promedio, se negoció
cada unidad.

**Intuición.** Muchos participantes lo usan como "precio justo" del período. Un precio muy por
encima o por debajo del VWAP está "estirado".

**Fórmula.** Con el precio típico `TP = (H + L + C) / 3`:

```text
VWAP = Σ (TP · V) / Σ V
```

El proyecto ofrece dos versiones:

- **Móvil** (`vwap_rolling`): las sumas cubren las últimas `n` velas.
- **De sesión** (`vwap_session`): las sumas se reinician en cada sesión UTC (por defecto, cada
  día a las 00:00 UTC).

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/indicators/core.py#L124-L142 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 124–142

```python
def vwap_rolling(df: pd.DataFrame, n: int) -> pd.Series:
    """VWAP de ventana móvil de ``n`` velas con precio típico (h+l+c)/3."""
    _check_period(n)
    tp = (df["high"] + df["low"] + df["close"]) / 3
    pv = (tp * df["volume"]).rolling(n, min_periods=n).sum()
    vol = df["volume"].rolling(n, min_periods=n).sum()
    return (pv / vol.replace(0, np.nan)).rename("vwap")


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
<!-- fmt: on -->

**Definición de sesión en un mercado 24/7.** Las bolsas tienen apertura y cierre; las
criptomonedas no. **[Diseño]** El proyecto define la sesión como el día UTC. Es una convención: no
hay una apertura "real" a las 00:00 UTC. Su efecto secundario es que, al principio de cada
sesión, el VWAP se basa en muy pocas velas y es muy sensible.

**Cálculo manual.** Dos velas: `TP₁ = 100`, `V₁ = 1` y `TP₂ = 110`, `V₂ = 3`.
`VWAP = (100·1 + 110·3) / (1 + 3) = 430 / 4 = 107,5`. Pesa más la vela con más volumen.

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.indicators import vwap_rolling

idx = pd.date_range("2024-01-01", periods=2, freq="1h", tz="UTC")
velas = pd.DataFrame(
    {"high": [101, 112.0], "low": [99, 108.0], "close": [100, 110.0], "volume": [1, 3.0]}, index=idx
)
print(vwap_rolling(velas, 2).tolist())
```
<!-- salida -->
```text
[nan, 107.5]
```

**La desviación normalizada (z-score)** que usa la estrategia 3 es:

```text
z[t] = (C[t] − VWAP[t]) / desviación(C − VWAP, últimas n velas anteriores)
```

Se calcula dentro de la estrategia (sección 8.3). El proyecto también tiene una función genérica
`rolling_zscore` (líneas 153–157), exportada pero **sin uso** en `src/`.

**[Limitación]** El VWAP de sesión no tiene ventana de calentamiento: en la primera vela de cada
día vale exactamente el precio típico de esa vela.

---

## 7.4 EMA y cruces de medias

**Qué mide.** La EMA es una media que da más peso a lo reciente. Un **cruce** ocurre cuando una
media rápida (pocas velas) pasa por encima o por debajo de una lenta (muchas velas).

**Intuición.** La media rápida reacciona antes a los cambios. Si supera a la lenta, el precio
reciente está por encima del precio "de fondo": posible inicio de tendencia alcista.

**Fórmulas.** `EMA` con `α = 2/(n+1)` (sección 7.0). Cruce al alza en `t`:
`rápida[t] > lenta[t]` y `rápida[t−1] ≤ lenta[t−1]`.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/indicators/core.py#L171-L180 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 171–180

```python
def crossover(a: pd.Series, b: pd.Series | float) -> pd.Series:
    """True en ``t`` si ``a`` cruza por encima de ``b`` entre ``t-1`` y ``t``."""
    bb = b if isinstance(b, pd.Series) else pd.Series(b, index=a.index)
    return ((a > bb) & (a.shift(1) <= bb.shift(1))).fillna(False).astype(bool)


def crossunder(a: pd.Series, b: pd.Series | float) -> pd.Series:
    """True en ``t`` si ``a`` cruza por debajo de ``b`` entre ``t-1`` y ``t``."""
    bb = b if isinstance(b, pd.Series) else pd.Series(b, index=a.index)
    return ((a < bb) & (a.shift(1) >= bb.shift(1))).fillna(False).astype(bool)
```
<!-- fmt: on -->

El cálculo manual de la EMA está en el Módulo V (sección 5.10) y el de un cruce, en la sección
5.8.

**Errores frecuentes.**

- Detectar el cruce comparando solo `rápida > lenta`: eso es un **estado**, y sería "verdadero"
  en todas las velas de la tendencia, no solo en el momento del cruce.
- Las medias se **retrasan**: una EMA de 26 velas reacciona tarde. En un mercado lateral, las
  medias se cruzan una y otra vez y generan señales falsas (por eso la estrategia 4 añade
  filtros).

---

## 7.5 Canal de Donchian

**Qué mide.** El máximo más alto y el mínimo más bajo de las últimas `n` velas.

**Intuición.** Superar el máximo de los últimos 20 días es "romper" un rango: algo nuevo está
pasando.

**Fórmula (variante implementada):**

```text
superior[t] = máx(H[t−n], ..., H[t−1])
inferior[t] = mín(L[t−n], ..., L[t−1])
medio[t]    = (superior[t] + inferior[t]) / 2
```

<!-- fmt: off -->
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
<!-- fmt: on -->

**[Diseño] Diferencia con la definición habitual.** Muchas plataformas incluyen la vela actual en
el canal. Entonces la condición "cierre > máximo del canal" es imposible por construcción (el
cierre nunca supera el máximo de su propia vela). El `shift(1)` excluye la vela actual.

**Cálculo manual.** Máximos `[5, 7, 6, 8, 12]`, `n = 3`. En la última vela, el canal superior es
el máximo de `[7, 6, 8]` = 8 (sin incluir el 12 actual).

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.indicators import donchian

velas = pd.DataFrame({"high": [5, 7, 6, 8, 12.0], "low": [4, 5, 5, 6, 9.0]})
print(donchian(velas, 3))
```
<!-- salida -->
```text
   upper  lower  mid
0    NaN    NaN  NaN
1    NaN    NaN  NaN
2    NaN    NaN  NaN
3    7.0    4.0  5.5
4    8.0    5.0  6.5
```

**Inicio de la serie:** `NaN` durante `n` velas (las `n − 1` de la ventana más el desplazamiento).

---

## 7.6 ATR (Average True Range)

**Qué mide.** La amplitud típica de una vela, contando también los saltos entre velas.

**Intuición.** Es la "volatilidad en unidades de precio". Si el ATR de BTC es 300 USDT, una vela
normal recorre unos 300 USDT. Por eso el proyecto lo usa para colocar los stops: un stop a
`2 × ATR` se adapta a lo agitado que esté el mercado.

**Fórmula.** El *true range* (rango verdadero) de una vela es el mayor de tres valores:

```text
TR[t] = máx( H[t] − L[t],  |H[t] − C[t−1]|,  |L[t] − C[t−1]| )
ATR[t] = Wilder(TR, n)[t]
```

Los dos últimos términos capturan los **gaps**: si una vela abre muy por encima del cierre
anterior, su rango propio puede ser pequeño, pero el movimiento real fue grande.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/indicators/core.py#L41-L53 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 41–53

```python
def true_range(df: pd.DataFrame) -> pd.Series:
    """True Range: ``max(h-l, |h-c_prev|, |l-c_prev|)``."""
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [df["high"] - df["low"], (df["high"] - prev_close).abs(), (df["low"] - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    return tr.rename("tr")


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    """Average True Range de Wilder."""
    return wilder(true_range(df), n).rename("atr")
```
<!-- fmt: on -->

**Cálculo manual.** Cierre anterior 98; vela actual con máximo 105 y mínimo 100:
`TR = máx(5, |105 − 98|, |100 − 98|) = máx(5, 7, 2) = 7`.

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.indicators import atr, true_range

velas = pd.DataFrame(
    {"high": [99, 105, 104, 103.0], "low": [97, 100, 101, 99.0], "close": [98, 103, 102, 100.0]}
)
tr = true_range(velas)
print(tr.tolist())
# Wilder con n = 2 (alfa = 1/2), sembrado con el primer valor y publicado desde el segundo
manual = [tr[0]]
for x in tr[1:]:
    manual.append(manual[-1] + (x - manual[-1]) / 2)
print([round(float(m), 4) for m in manual][1:], atr(velas, 2).round(4).tolist()[1:])
```
<!-- salida -->
```text
[2.0, 7.0, 3.0, 4.0]
[4.5, 3.75, 3.875] [4.5, 3.75, 3.875]
```

En la primera vela no hay cierre anterior y el TR es solo `H − L` (2). **[Limitación]** El ATR
está en unidades de precio: un ATR de 300 significa cosas muy distintas para BTC a 30.000 y a
90.000. Para comparar entre épocas o activos se usa `ATR / precio` (lo hacen las estrategias 1 y
4 y el clasificador de régimen).

---

## 7.7 RSI (Relative Strength Index)

**Qué mide.** La proporción entre las subidas y las bajadas recientes, en una escala de 0 a 100.

**Intuición.** Un RSI de 80 significa que las subidas recientes dominan claramente a las bajadas;
uno de 20, lo contrario. Tradicionalmente, por encima de 70 se habla de "sobrecompra" y por
debajo de 30 de "sobreventa".

**Fórmula.**

```text
Δ[t]        = C[t] − C[t−1]
ganancia[t] = máx(Δ[t], 0)          pérdida[t] = máx(−Δ[t], 0)
G = Wilder(ganancia, n)             P = Wilder(pérdida, n)
RS = G / P                          RSI = 100 − 100 / (1 + RS)
```

Casos límite del proyecto: sin pérdidas (`P = 0`), RSI = 100; sin movimiento (`G = P = 0`),
RSI = 50.

<!-- fmt: off -->
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
<!-- fmt: on -->

**Cálculo manual con `n = 2`.** Cierres `[10, 11, 10,5, 11,5, 12]`.

| t | Δ | ganancia | pérdida | G (Wilder, α = ½) | P (Wilder) | RS | RSI |
|---|---|---|---|---|---|---|---|
| 1 | +1 | 1 | 0 | 1 | 0 | — (aún no publica) | — |
| 2 | −0,5 | 0 | 0,5 | ½·0 + ½·1 = 0,5 | ½·0,5 + ½·0 = 0,25 | 2 | 66,67 |
| 3 | +1 | 1 | 0 | ½·1 + ½·0,5 = 0,75 | ½·0 + ½·0,25 = 0,125 | 6 | 85,71 |
| 4 | +0,5 | 0,5 | 0 | ½·0,5 + ½·0,75 = 0,625 | 0,0625 | 10 | 90,91 |

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.indicators import rsi

print(rsi(pd.Series([10, 11, 10.5, 11.5, 12]), 2).round(2).tolist())
```
<!-- salida -->
```text
[nan, nan, 66.67, 85.71, 90.91]
```

**Error interpretativo frecuente.** "RSI > 70 significa que el precio va a bajar". En una
tendencia fuerte, el RSI puede quedarse por encima de 70 durante mucho tiempo mientras el precio
sigue subiendo. Por eso la estrategia 6 exige un **cruce de salida** de la zona y ofrece filtros
de tendencia.

---

## 7.8 MACD (Moving Average Convergence Divergence)

**Qué mide.** La distancia entre una EMA rápida y una lenta (la línea MACD), una media de esa
distancia (la línea de señal) y la diferencia entre ambas (el histograma).

**Intuición.** Si la EMA rápida se aleja hacia arriba de la lenta, el impulso alcista crece. El
histograma muestra si ese impulso **se acelera o se frena**.

**Fórmula.**

```text
MACD       = EMA(C, rápida) − EMA(C, lenta)
señal      = EMA(MACD, n_señal)
histograma = MACD − señal
```

Parámetros clásicos: 12, 26 y 9.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/indicators/core.py#L69-L75 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 69–75

```python
def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """MACD = EMA(fast) - EMA(slow); señal = EMA(MACD, signal); histograma = MACD - señal."""
    if fast >= slow:
        raise ValueError("fast debe ser menor que slow")
    line = ema(close, fast) - ema(close, slow)
    sig = line.ewm(span=signal, adjust=False, min_periods=signal).mean()
    return pd.DataFrame({"macd": line, "signal": sig, "hist": line - sig})
```
<!-- fmt: on -->

**Cálculo comprobable.** Con `rápida=2`, `lenta=3` y `señal=2`, cada paso puede seguirse a mano con
la fórmula de la EMA:

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.indicators import ema, macd

c = pd.Series([10.0, 11.0, 12.0, 11.0, 13.0, 14.0])
m = macd(c, fast=2, slow=3, signal=2)
print(
    pd.DataFrame(
        {
            "ema2": ema(c, 2),
            "ema3": ema(c, 3),
            "macd": m["macd"],
            "senal": m["signal"],
            "hist": m["hist"],
        }
    ).round(4)
)
```
<!-- salida -->
```text
      ema2     ema3    macd   senal    hist
0      NaN      NaN     NaN     NaN     NaN
1  10.6667      NaN     NaN     NaN     NaN
2  11.5556  11.2500  0.3056     NaN     NaN
3  11.1852  11.1250  0.0602  0.1420 -0.0818
4  12.3951  12.0625  0.3326  0.2690  0.0635
5  13.4650  13.0312  0.4338  0.3789  0.0549
```

**Inicio de la serie.** La línea MACD necesita `lenta` velas; la señal, `n_señal` valores de MACD
más; con 12/26/9 el primer histograma aparece hacia la vela 34. **[Limitación]** El MACD está en
unidades de precio (como el ATR): su escala cambia con el nivel del precio.

---

## 7.9 Bandas de Bollinger

**Qué mide.** Una media móvil con dos bandas situadas a `k` desviaciones estándar por encima y
por debajo.

**Intuición.** Si los precios se distribuyeran de forma aproximadamente normal alrededor de la
media, la mayoría quedaría dentro de las bandas. Un cierre fuera de ellas es "inusual"
**respecto a la volatilidad reciente**.

**Fórmula.**

```text
medio    = SMA(C, n)
σ        = desviación estándar poblacional de C en las últimas n velas
superior = medio + k·σ          inferior = medio − k·σ
```

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/indicators/core.py#L78-L82 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 78–82

```python
def bollinger(close: pd.Series, n: int = 20, k: float = 2.0) -> pd.DataFrame:
    """Bandas de Bollinger con desviación estándar poblacional (ddof=0)."""
    mid = sma(close, n)
    std = close.rolling(n, min_periods=n).std(ddof=0)
    return pd.DataFrame({"mid": mid, "upper": mid + k * std, "lower": mid - k * std, "std": std})
```
<!-- fmt: on -->

**Cálculo manual.** Cierres `[2, 4, 4, 4, 5, 5, 7, 9]`, `n = 8`, `k = 2`. Media 5; σ poblacional 2
(Módulo VI, sección 6.3); bandas `[5 − 4 ; 5 + 4] = [1 ; 9]`.

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.indicators import bollinger

print(bollinger(pd.Series([2, 4, 4, 4, 5, 5, 7, 9.0]), n=8, k=2).iloc[-1].to_dict())
```
<!-- salida -->
```text
{'mid': 5.0, 'upper': 9.0, 'lower': 1.0, 'std': 2.0}
```

**[Hecho]** Usa la desviación **poblacional** (`ddof=0`), la convención original de Bollinger.
**Error frecuente:** pensar que "el 95 % de los precios estará dentro de las bandas". Los precios
no son normales ni independientes (Módulo VI, sección 6.5): el porcentaje real varía mucho, y en
tendencias fuertes el precio "camina" por una banda durante muchas velas.

---

## 7.10 Stochastic RSI

**Qué mide.** Dónde está el RSI actual dentro del rango que ha recorrido el propio RSI en las
últimas `n` velas, en una escala de 0 a 100. Es un "indicador de un indicador".

**Intuición.** El RSI puede pasar semanas entre 40 y 60 sin llegar nunca a 30 ni a 70. El
estocástico del RSI amplía ese rango: 0 significa "el RSI está en su mínimo reciente" y 100, "en
su máximo reciente".

**Fórmula.**

```text
crudo = 100 · (RSI − mín(RSI, n)) / (máx(RSI, n) − mín(RSI, n))     (50 si el rango es 0)
%K    = SMA(crudo, suavizado_k)
%D    = SMA(%K, suavizado_d)
```

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/indicators/core.py#L85-L97 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 85–97

```python
def stoch_rsi(
    close: pd.Series, rsi_n: int = 14, stoch_n: int = 14, k_smooth: int = 3, d_smooth: int = 3
) -> pd.DataFrame:
    """Stochastic RSI en [0, 100]: %K = SMA(estocástico del RSI), %D = SMA(%K)."""
    r = rsi(close, rsi_n)
    lo = r.rolling(stoch_n, min_periods=stoch_n).min()
    hi = r.rolling(stoch_n, min_periods=stoch_n).max()
    rng = hi - lo
    raw = ((r - lo) / rng.replace(0, np.nan) * 100).where(rng != 0, 50.0)
    raw = raw.where(r.notna() & lo.notna())
    k = sma(raw, k_smooth)
    d = sma(k, d_smooth)
    return pd.DataFrame({"k": k, "d": d})
```
<!-- fmt: on -->

**Cálculo manual del valor crudo.** Si en las últimas 14 velas el RSI estuvo entre 40 y 60 y ahora
vale 55: `crudo = 100 · (55 − 40) / (60 − 40) = 75`.

**[Diseño]** Si el RSI no se ha movido nada en la ventana (máximo igual a mínimo), la división
sería 0/0; el proyecto devuelve 50 (punto neutro) en ese caso.

**Inicio de la serie:** necesita el RSI (14) más la ventana (14) más dos suavizados (3 y 3):
unas 33 velas. **[Limitación]** Es muy sensible y oscila mucho; las señales "casi idénticas"
repetidas en un mismo movimiento son frecuentes (la estrategia 9 lo trata con un mecanismo de
rearmado, sección 8.9).

---

## 7.11 ADX y los indicadores direccionales (+DI, −DI)

**Qué mide.** +DI y −DI miden la fuerza relativa de los movimientos al alza y a la baja; el ADX
mide la **fuerza de la tendencia**, sin importar su dirección.

**Intuición.** Si cada vela supera el máximo de la anterior más de lo que perfora su mínimo, hay
dominio alcista (+DI alto). El ADX indica si **algún** lado domina con claridad (tendencia) o si
ninguno lo hace (mercado lateral).

**Fórmulas** (Wilder).

```text
subida[t] = H[t] − H[t−1]            bajada[t] = L[t−1] − L[t]
+DM[t] = subida  si subida > bajada y subida > 0;  si no, 0
−DM[t] = bajada  si bajada > subida y bajada > 0;  si no, 0
+DI = 100 · Wilder(+DM, n) / Wilder(TR, n)
−DI = 100 · Wilder(−DM, n) / Wilder(TR, n)
DX  = 100 · |+DI − −DI| / (+DI + −DI)
ADX = Wilder(DX, n)
```

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/indicators/core.py#L100-L115 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 100–115

```python
def adx(df: pd.DataFrame, n: int = 14) -> pd.DataFrame:
    """ADX, +DI y -DI de Wilder."""
    up = df["high"].diff()
    down = -df["low"].diff()
    plus_dm = up.where((up > down) & (up > 0), 0.0)
    minus_dm = down.where((down > up) & (down > 0), 0.0)
    plus_dm[up.isna()] = np.nan
    minus_dm[down.isna()] = np.nan
    atr_ = wilder(true_range(df).where(df["close"].shift(1).notna()), n)
    with np.errstate(divide="ignore", invalid="ignore"):
        plus_di = 100 * wilder(plus_dm, n) / atr_
        minus_di = 100 * wilder(minus_dm, n) / atr_
        dsum = plus_di + minus_di
        dx = (100 * (plus_di - minus_di).abs() / dsum).where(dsum != 0, 0.0)
    dx = dx.where(plus_di.notna() & minus_di.notna())
    return pd.DataFrame({"plus_di": plus_di, "minus_di": minus_di, "adx": wilder(dx, n)})
```
<!-- fmt: on -->

- **102–105:** los movimientos direccionales. Solo cuenta el lado que domina en esa vela.
- **106–108:** la primera vela no tiene anterior: sus valores se marcan como ausentes para que no
  cuenten como "0".
- **109–113:** los DI y el DX; si `+DI + −DI = 0`, el DX vale 0.
- **115:** el ADX es la media de Wilder del DX.

**Cálculo manual de los movimientos direccionales.**

| Vela | H | L | subida | bajada | +DM | −DM |
|---|---|---|---|---|---|---|
| 0 | 10 | 8 | — | — | — | — |
| 1 | 12 | 9 | 2 | −1 | 2 | 0 |
| 2 | 11 | 7 | −1 | 2 | 0 | 2 |
| 3 | 13 | 8 | 2 | −1 | 2 | 0 |

<!-- ejecutar -->
```python
import pandas as pd

velas = pd.DataFrame({"high": [10, 12, 11, 13.0], "low": [8, 9, 7, 8.0]})
subida = velas["high"].diff()
bajada = -velas["low"].diff()
print(
    pd.DataFrame(
        {
            "subida": subida,
            "bajada": bajada,
            "+DM": subida.where((subida > bajada) & (subida > 0), 0.0),
            "-DM": bajada.where((bajada > subida) & (bajada > 0), 0.0),
        }
    )
)
```
<!-- salida -->
```text
   subida  bajada  +DM  -DM
0     NaN     NaN  0.0  0.0
1     2.0    -1.0  2.0  0.0
2    -1.0     2.0  0.0  2.0
3     2.0    -1.0  2.0  0.0
```

(En la fila 0, el código del proyecto pone `NaN` en lugar de 0; este ejemplo simplificado no lo
hace.)

**Inicio de la serie.** Los DI necesitan `n` velas tras la primera, y el ADX otras `n` de DX: con
`n = 14`, el primer ADX aparece en torno a la vela 28. **[Limitación]** El ADX no dice la
dirección: un ADX de 40 puede ser una caída fuerte. Los umbrales habituales (20 o 25 para "hay
tendencia") son convenciones, no constantes del mercado.

---

## 7.12 Herramientas auxiliares: percentil móvil y temporalidad superior

### Percentil móvil (`rolling_percentile`)

Mide qué fracción de las `n` velas **anteriores** tenía un valor menor que el actual. El
clasificador de régimen (Módulo IX) lo usa con la volatilidad: un percentil de 0,9 significa
"la volatilidad actual supera al 90 % de la reciente".

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/indicators/core.py#L160-L168 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 160–168

```python
def rolling_percentile(s: pd.Series, n: int) -> pd.Series:
    """Fracción (0-1) de las ``n`` velas **anteriores** con valor estrictamente menor que ``s[t]``.

    Se calcula con el rango mínimo de ``s[t]`` dentro de la ventana ``[t-n, t]``:
    ``(rank_min - 1) / n``. NaN si la ventana contiene valores ausentes.
    """
    _check_period(n)
    ranks = s.rolling(n + 1, min_periods=n + 1).rank(method="min")
    return ((ranks - 1) / n).rename("percentile")
```
<!-- fmt: on -->

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.indicators import rolling_percentile

print(rolling_percentile(pd.Series([3, 1, 4, 1, 5.0]), 4).tolist())
```
<!-- salida -->
```text
[nan, nan, nan, nan, 1.0]
```

En la última vela, el 5 es mayor que los 4 valores anteriores `[3, 1, 4, 1]`: percentil 1,0.

### Temporalidad superior sin anticipación (`higher_timeframe`)

La estrategia 5 puede filtrar con una temporalidad mayor, por ejemplo velas de 4h sobre datos de
1h. El riesgo es usar una vela de 4h **antes de que termine**.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/indicators/core.py#L183-L208 -->
`src/bybit_quant_lab/indicators/core.py` · líneas 183–208

```python
def higher_timeframe(
    df: pd.DataFrame, base_tf: pd.Timedelta, htf: pd.Timedelta, ema_period: int | None = None
) -> pd.DataFrame:
    """Resamplea OHLCV a una temporalidad superior y lo alinea **sin anticipación**.

    Una vela superior que abre en ``T`` solo está disponible cuando cierra (``T + htf``). La
    vela base ``t`` toma su decisión al cierre (``t + base_tf``), así que recibe la última
    vela superior con ``T + htf <= t + base_tf``. Las velas superiores incompletas al final
    de los datos nunca se exponen. Con ``ema_period`` se añade la columna ``ema`` calculada
    sobre los cierres de la temporalidad superior (no sobre la serie base rellenada).
    """
    if htf <= base_tf:
        raise ValueError("htf debe ser mayor que la temporalidad base")
    agg = df.resample(htf, label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    )
    counts = df["close"].resample(htf, label="left", closed="left").count()
    expected = int(htf / base_tf)
    agg = agg[counts >= expected]
    if ema_period is not None:
        agg["ema"] = ema(agg["close"], ema_period)
    agg.index = agg.index + htf
    keys = df.index + base_tf
    aligned = agg.reindex(agg.index.union(keys)).ffill().reindex(keys)
    aligned.index = df.index
    return aligned
```
<!-- fmt: on -->

- **196–198:** agrega las velas base en velas de 4h (`resample`), con la etiqueta en la apertura.
- **199–201:** descarta las velas de 4h **incompletas** (con menos velas base de las esperadas,
  por un hueco o por el final de los datos).
- **204:** **mueve la etiqueta al cierre** de la vela de 4h: a partir de ese momento ya es
  información conocida.
- **205–207:** la vela base `t` decide en su cierre (`t + 1h`) y recibe la última vela de 4h ya
  cerrada en ese instante (`ffill` propaga el último valor conocido hacia delante, nunca hacia
  atrás).

<!-- ejecutar -->
```python
import numpy as np
import pandas as pd

from bybit_quant_lab.indicators import higher_timeframe

idx = pd.date_range("2024-01-01", periods=10, freq="1h", tz="UTC")
cierres = np.arange(1, 11, dtype=float)
velas = pd.DataFrame(
    {"open": cierres, "high": cierres, "low": cierres, "close": cierres, "volume": 1.0}, index=idx
)
h4 = higher_timeframe(velas, pd.Timedelta("1h"), pd.Timedelta("4h"))
print(pd.DataFrame({"cierre_1h": velas["close"], "cierre_4h_visible": h4["close"]}))
```
<!-- salida -->
```text
                           cierre_1h  cierre_4h_visible
2024-01-01 00:00:00+00:00        1.0                NaN
2024-01-01 01:00:00+00:00        2.0                NaN
2024-01-01 02:00:00+00:00        3.0                NaN
2024-01-01 03:00:00+00:00        4.0                4.0
2024-01-01 04:00:00+00:00        5.0                4.0
2024-01-01 05:00:00+00:00        6.0                4.0
2024-01-01 06:00:00+00:00        7.0                4.0
2024-01-01 07:00:00+00:00        8.0                8.0
2024-01-01 08:00:00+00:00        9.0                8.0
2024-01-01 09:00:00+00:00       10.0                8.0
```

La vela de 4h de 00:00 a 04:00 cierra con el valor 4. La vela base de las 03:00 decide a las
04:00 y ya puede verla; las de las 00:00 a las 02:00 todavía no. La prueba
`test_higher_timeframe_uses_only_closed_bars` (`tests/unit/test_audit_indicators.py`) lo verifica
alterando drásticamente los datos futuros.

---

## 7.13 Resumen: convención estándar frente a variante implementada

| Indicador | Convención habitual | Variante del proyecto | ¿Importa? |
|---|---|---|---|
| EMA | Semilla SMA o primer valor, según la plataforma | Primer valor (`adjust=False`) | Solo al principio |
| Wilder (ATR, RSI, ADX) | Semilla = SMA de los primeros `n` | Primer valor | Solo al principio (sección 7.0) |
| Donchian | A menudo incluye la vela actual | Excluye la vela actual | Sí: sin el desplazamiento, la ruptura del canal no es posible |
| Bollinger | Desviación poblacional | Poblacional | No |
| VWAP | Anclado a la sesión bursátil | Ventana móvil o día UTC | Convención en mercados 24/7 |
| StochRSI | %K = SMA(3) del crudo y %D = SMA(3) de %K | Igual | No |
| RSI con `P = 0` | 100 | 100 (y 50 si `G = P = 0`) | Solo en mercados sin movimiento |

### Comprobación final del módulo

¿Por qué el canal de Donchian del proyecto usa `shift(1)` y qué pasaría si se quitara?

<details><summary>Ver respuesta</summary>

Para excluir la vela actual del canal. Sin el desplazamiento, el canal superior incluiría el
máximo de la vela actual, y como el cierre nunca puede superar el máximo de su propia vela, la
condición "cierre > canal superior" no se cumpliría jamás: la estrategia no tendría ninguna
entrada.
</details>
