# Módulo VI. Matemáticas y estadística necesarias

Este módulo no da por supuesta ninguna formación universitaria. Cada concepto se presenta con
números pequeños que puedes comprobar con una calculadora, después con una fórmula en la que se
definen todas las variables y, por último, con el lugar del proyecto donde se usa.

Notación: `Σ` (sigma mayúscula) significa "suma de"; `√` es raíz cuadrada; `x̄` (equis con barra)
es la media de los valores `x`; `n` es el número de valores.

---

## 6.1 Porcentajes y rendimientos

### Rendimiento simple

Si un precio pasa de `P₀` a `P₁`, el **rendimiento simple** es:

```text
r = P₁ / P₀ − 1
```

De 100 a 110: `r = 110/100 − 1 = 0,10 = 10 %`. De 110 a 100: `r = 100/110 − 1 = −0,0909 = −9,09 %`.

**Asimetría importante:** subir un 10 % y luego bajar un 10 % **no** te deja igual:
`100 × 1,10 × 0,90 = 99`. Para recuperar una pérdida del 50 % hace falta ganar un 100 %. Por eso
las caídas grandes (drawdowns, Módulo XII) son tan dañinas.

### Rendimiento logarítmico

```text
r_log = ln(P₁ / P₀)
```

`ln` es el logaritmo natural. Su ventaja es que los rendimientos logarítmicos **se suman** a lo
largo del tiempo: `ln(110/100) + ln(100/110) = 0`. Para movimientos pequeños, `r_log ≈ r`.

**[Hecho]** El proyecto usa **rendimientos simples** por vela sobre la curva de capital:

<!-- cita: src/bybit_quant_lab/analytics/metrics.py#L36-L40 -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 36–40

```python
def bar_returns(equity: pd.Series, initial: float) -> pd.Series:
    """Retornos simples por vela, empezando desde el capital inicial."""
    prev = equity.shift(1)
    prev.iloc[0] = initial
    return equity / prev - 1
```

`equity` es la serie de capital al cierre de cada vela. `shift(1)` trae el capital de la vela
anterior y, para la primera vela, se usa el capital inicial.

<!-- ejecutar -->
```python
import math

print(round(110 / 100 - 1, 4), round(100 / 110 - 1, 4))
print(round(100 * 1.10 * 0.90, 4))
print(round(math.log(110 / 100) + math.log(100 / 110), 12))
print(round(math.log(1.01), 6), "≈", 0.01)
```
<!-- salida -->
```text
0.1 -0.0909
99.0
0.0
0.00995 ≈ 0.01
```

---

## 6.2 Rendimientos acumulados y capitalización

Si en tres períodos obtienes `r₁`, `r₂`, `r₃`, el rendimiento **acumulado** no es la suma, sino:

```text
R = (1 + r₁)(1 + r₂)(1 + r₃) − 1
```

Con +10 %, −5 % y +8 %: `1,10 × 0,95 × 1,08 − 1 = 0,1286 = 12,86 %` (la suma daría 13 %).
Esto es la **capitalización compuesta**: cada período gana o pierde sobre lo acumulado.

La **tasa de crecimiento anual compuesta** (CAGR, Compound Annual Growth Rate) responde: "¿qué
rendimiento anual constante habría producido el mismo resultado?":

```text
CAGR = (E_final / E_inicial)^(365 / días) − 1
```

Ejemplo: de 10.000 a 12.100 en 730 días (2 años): `(1,21)^(365/730) − 1 = 1,21^0,5 − 1 = 10 %`.

**[Diseño]** El proyecto **no calcula** el CAGR si el período dura menos de 180 días
(`min_days_for_cagr`). Anualizar un mes excelente (por ejemplo, +5 % en 30 días da un CAGR del
81 %) produce cifras engañosas.

<!-- ejecutar -->
```python
r = [0.10, -0.05, 0.08]
acumulado = 1.0
for x in r:
    acumulado *= 1 + x
print(round(acumulado - 1, 4), round(sum(r), 4))
print(round((12_100 / 10_000) ** (365 / 730) - 1, 4))
print(round(1.05 ** (365 / 30) - 1, 4))
```
<!-- salida -->
```text
0.1286 0.13
0.1
0.8105
```

---

## 6.3 Media, mediana, varianza y desviación estándar

Usaremos los valores `x = [2, 4, 4, 4, 5, 5, 7, 9]` (`n = 8`).

- **Media:** `x̄ = Σx / n = 40 / 8 = 5`. El "centro de gravedad" de los datos.
- **Mediana:** el valor del medio con los datos ordenados. Con 8 valores, la media de los dos
  centrales: `(4 + 5) / 2 = 4,5`. Es robusta: un valor extremo la mueve poco.
- **Varianza:** la media de las distancias al cuadrado respecto a la media. Las distancias son
  `−3, −1, −1, −1, 0, 0, 2, 4`; sus cuadrados suman `9+1+1+1+0+0+4+16 = 32`.
  - **Poblacional** (divide entre `n`): `32 / 8 = 4`.
  - **Muestral** (divide entre `n − 1`): `32 / 7 ≈ 4,571`.
- **Desviación estándar:** la raíz de la varianza. Poblacional `√4 = 2`; muestral `≈ 2,138`.
  Se mide en las mismas unidades que los datos: es la "dispersión típica".

**¿Por qué `n − 1`?** Cuando los datos son una **muestra** de algo mayor (los rendimientos que
observaste, de todos los que podrían ocurrir), la media de la muestra está más cerca de sus
propios datos que la media verdadera. Dividir entre `n` subestima la dispersión; `n − 1`
(corrección de Bessel) lo compensa. En `pandas`, el parámetro `ddof` elige entre ambas:
`ddof=0` divide entre `n` y `ddof=1` entre `n − 1`.

**[Hecho]** En el proyecto, las métricas de rendimiento (Sharpe, p-valores) usan `ddof=1`
(muestra) y las bandas de Bollinger usan `ddof=0` (la convención habitual del indicador).

<!-- ejecutar -->
```python
import numpy as np

x = np.array([2, 4, 4, 4, 5, 5, 7, 9])
print(x.mean(), np.median(x))
print(x.var(ddof=0), round(x.var(ddof=1), 3))
print(x.std(ddof=0), round(x.std(ddof=1), 3))
```
<!-- salida -->
```text
5.0 4.5
4.0 4.571
2.0 2.138
```

---

## 6.4 Covarianza y correlación

### La idea

¿Tienden dos variables a moverse juntas? La **covarianza** mide si se mueven en la misma
dirección respecto a sus medias:

```text
cov(x, y) = Σ (xᵢ − x̄)(yᵢ − ȳ) / (n − 1)
```

Su valor depende de las unidades, así que se normaliza para obtener la **correlación de
Pearson**, siempre entre −1 y 1:

```text
corr(x, y) = cov(x, y) / (desv(x) · desv(y))
```

- `+1`: se mueven exactamente juntas (en proporción).
- `0`: no hay relación **lineal** (puede haber otra).
- `−1`: se mueven exactamente en sentido contrario.

Ejemplo: `x = [1, 2, 3]`, `y = [2, 4, 7]`. Medias 2 y 4,33. Productos de distancias:
`(−1)(−2,33) + (0)(−0,33) + (1)(2,67) = 5`, covarianza `5 / 2 = 2,5`. Desviaciones (muestrales)
1 y 2,517; correlación `2,5 / 2,517 ≈ 0,993`.

**[Hecho]** El proyecto usa la correlación entre las **señales** de estrategias (valores −1, 0 y
1) para detectar estrategias redundantes (`signals/redundancy.py`, Módulo IX). **[Limitación]**
Con señales que valen 0 la mayor parte del tiempo, Pearson subestima el parecido entre
estrategias: dos estrategias pueden coincidir el 95 % de las veces que ambas están activas y aun
así tener una correlación baja. La auditoría lo registró como M-05.

**Correlación no es causalidad:** que dos series se muevan juntas no significa que una cause la
otra; puede haber un tercer factor común (por ejemplo, la tendencia general del mercado).

<!-- ejecutar -->
```python
import numpy as np

x, y = np.array([1, 2, 3.0]), np.array([2, 4, 7.0])
print(round(np.cov(x, y, ddof=1)[0, 1], 3), round(np.corrcoef(x, y)[0, 1], 3))

a = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])     # dos señales casi siempre en 0...
b = np.array([0, 0, 0, 1, 0, 0, 0, 0, 1, 0])
activas = (a != 0) & (b != 0)
print("correlación:", round(np.corrcoef(a, b)[0, 1], 3),
      "| coinciden cuando ambas están activas:", float((a[activas] == b[activas]).mean()))
```
<!-- salida -->
```text
2.5 0.993
correlación: 0.375 | coinciden cuando ambas están activas: 1.0
```

---

## 6.5 Probabilidad y distribuciones

### La idea

Una **variable aleatoria** es un número cuyo valor depende del azar (el rendimiento de mañana).
Su **distribución** describe qué valores puede tomar y con qué probabilidad.

La **distribución normal** (campana de Gauss) queda definida por su media `μ` (mu) y su
desviación estándar `σ` (sigma). Aproximadamente el 68 % de los valores caen a menos de 1σ de la
media y el 95 % a menos de 1,96σ.

La **función de distribución acumulada** `Φ(z)` (fi mayúscula) da la probabilidad de que una
variable normal estándar (media 0, desviación 1) sea menor o igual que `z`. Su inversa,
`Φ⁻¹(p)`, da el valor `z` que deja una probabilidad `p` por debajo.

**[Hecho]** El proyecto usa la normal de la biblioteca estándar de Python
(`statistics.NormalDist`) en `validation/overfitting.py`, línea 25.

### Asimetría y curtosis

- **Asimetría** (skewness, `γ₃`): ¿la distribución es simétrica? Negativa significa una cola larga
  hacia las pérdidas (muchas ganancias pequeñas y alguna pérdida enorme).
- **Curtosis** (kurtosis, `γ₄`): ¿qué peso tienen las colas, los valores extremos? La normal tiene
  curtosis 3. Muchas series financieras tienen curtosis mucho mayor (**colas gruesas**): los
  movimientos extremos son más frecuentes de lo que predice la normal. A veces se usa la
  "curtosis en exceso" (`γ₄ − 3`); **[Hecho]** el proyecto usa la curtosis **sin** restar 3,
  como indica la fórmula del PSR (Módulo XIII).

<!-- cita: src/bybit_quant_lab/validation/overfitting.py#L28-L35 -->
`src/bybit_quant_lab/validation/overfitting.py` · líneas 28–35

```python
def _moments(returns: pd.Series) -> tuple[float, float, float, int]:
    r = returns.dropna().to_numpy(float)
    n = len(r)
    if n < 3 or r.std(ddof=1) == 0:
        return float("nan"), 0.0, 3.0, n
    sr = float(r.mean() / r.std(ddof=1))
    z = (r - r.mean()) / r.std(ddof=0)
    return sr, float(np.mean(z**3)), float(np.mean(z**4)), n
```

`z` son los valores **estandarizados** (restada la media y divididos entre la desviación); la
asimetría es la media de `z³` y la curtosis, la media de `z⁴`.

<!-- ejecutar -->
```python
from statistics import NormalDist

N = NormalDist()
print(round(N.cdf(0), 3), round(N.cdf(1.96), 4), round(N.cdf(1) - N.cdf(-1), 4))
print(round(N.inv_cdf(0.975), 4), round(N.inv_cdf(0.99), 4))
```
<!-- salida -->
```text
0.5 0.975 0.6827
1.96 2.3263
```

---

## 6.6 Muestreo y variabilidad

### La idea

Un backtest observa **una** muestra de la historia. Si la historia se hubiera desarrollado de otra
forma, la misma estrategia habría dado otro resultado. La pregunta estadística es: **¿cuánto
podría cambiar el resultado solo por azar?**

El **error estándar de la media** mide cuánto varía la media de una muestra de tamaño `n`:

```text
SE = s / √n
```

`s` es la desviación estándar muestral. Con más observaciones, la media es más precisa, pero
solo con la raíz de `n`: para reducir el error a la mitad hacen falta **cuatro veces** más datos.

Este ejemplo simula 2.000 "historias" de 20 operaciones cada una, con una ganancia media
verdadera de 0 (sin ninguna ventaja real) y una desviación de 50 USDT:

<!-- ejecutar -->
```python
import numpy as np

rng = np.random.default_rng(7)
historias = rng.normal(loc=0.0, scale=50.0, size=(2000, 20))   # media real = 0
medias = historias.mean(axis=1)
print("error estándar teórico:", round(50 / np.sqrt(20), 2))
print("desviación de las medias simuladas:", round(medias.std(ddof=1), 2))
print("historias con media > +15 USDT por operación:", round(float((medias > 15).mean()) * 100, 1), "%")
```
<!-- salida -->
```text
error estándar teórico: 11.18
desviación de las medias simuladas: 11.21
historias con media > +15 USDT por operación: 8.1 %
```

Sin ninguna ventaja real, alrededor del 8–9 % de las historias muestran una ganancia media
superior a 15 USDT por operación (8,1 % en esta simulación; la teoría da `1 − Φ(15/11,18) ≈ 9 %`). Con solo 20 operaciones, una media atractiva puede ser **pura suerte**.

---

## 6.7 Hipótesis nula, hipótesis alternativa y p-valor

### La idea

Un **contraste de hipótesis** es un razonamiento por reducción al absurdo:

1. **Hipótesis nula** (`H₀`): la explicación aburrida. "La estrategia no tiene ventaja: su
   ganancia media verdadera es 0 o menor".
2. **Hipótesis alternativa** (`H₁`): lo que te gustaría demostrar. "La ganancia media es mayor
   que 0".
3. Suponiendo que `H₀` es cierta, calculas la probabilidad de observar un resultado **al menos
   tan bueno** como el que obtuviste. Esa probabilidad es el **p-valor**.
4. Si el p-valor es muy pequeño (por convención, menor que un umbral `α = 0,05`), el resultado
   sería raro bajo `H₀` y la **rechazas**.

**Lo que el p-valor NO es:** no es la probabilidad de que la estrategia no funcione, ni la
probabilidad de que el resultado sea casualidad. Es la probabilidad de un resultado tan bueno
**si** no hubiera ventaja.

### El contraste que usa el proyecto

<!-- cita: src/bybit_quant_lab/validation/overfitting.py#L85-L91 -->
`src/bybit_quant_lab/validation/overfitting.py` · líneas 85–91

```python
def mean_pvalue(values: pd.Series) -> tuple[float | None, bool]:
    """p-valor unilateral (H0: media <= 0) con aproximación normal. Devuelve (p, fiable)."""
    v = values.dropna().to_numpy(float)
    if len(v) < 2 or v.std(ddof=1) == 0:
        return None, False
    t = v.mean() / (v.std(ddof=1) / math.sqrt(len(v)))
    return 1 - _N.cdf(t), len(v) >= 30
```

- **90:** el **estadístico t** mide cuántos errores estándar separan la media de 0:
  `t = x̄ / (s / √n)`.
- **91:** p-valor **unilateral** (solo cuenta resultados mejores, no peores): `1 − Φ(t)`.
  **[Supuesto]** Usa la distribución normal en lugar de la t de Student, una aproximación válida
  con muestras grandes. Por eso devuelve también un indicador `fiable` que solo es verdadero con
  30 o más operaciones.

Ejemplo a mano: 36 operaciones con ganancia media 10 USDT y desviación 30 USDT.
`SE = 30 / √36 = 5`; `t = 10 / 5 = 2`; `p = 1 − Φ(2) ≈ 0,0228`.

<!-- ejecutar -->
```python
import numpy as np
import pandas as pd

from bybit_quant_lab.validation.overfitting import mean_pvalue

rng = np.random.default_rng(1)
pnl = rng.normal(0, 30, 36)
pnl = (pnl - pnl.mean()) / pnl.std(ddof=1) * 30 + 10     # media 10 y desviación 30 exactas
p, fiable = mean_pvalue(pd.Series(pnl))
print(round(p, 4), fiable)
```
<!-- salida -->
```text
0.0228 True
```

### Comprobación

Una estrategia tiene p = 0,03 en su ganancia media. ¿Significa que hay un 97 % de probabilidad de
que funcione?

<details><summary>Ver respuesta</summary>

No. Significa que, **si** la estrategia no tuviera ventaja, solo un 3 % de las veces se obtendría
una media tan buena o mejor. La probabilidad de que "funcione" no se puede leer en el p-valor, y
además el p-valor no tiene en cuenta cuántas estrategias probaste antes de encontrar esta
(sección 6.9).
</details>

---

## 6.8 Intervalos de confianza

Un **intervalo de confianza** al 95 % es un rango construido con un procedimiento que, si
repitieras el experimento muchas veces, contendría el valor verdadero el 95 % de las veces. Con
la aproximación normal:

```text
IC 95 % = x̄ ± 1,96 · SE
```

Con el ejemplo anterior: `10 ± 1,96 × 5 = [0,2 ; 19,8]` USDT por operación. El intervalo es muy
ancho: con 36 operaciones, la ganancia verdadera podría ser casi cero o casi el doble.

**Interpretación correcta:** "el método produce intervalos que aciertan el 95 % de las veces".
**Interpretación incorrecta frecuente:** "hay un 95 % de probabilidad de que la media verdadera
esté en este intervalo concreto" (con este enfoque estadístico, la media verdadera es fija: o
está o no está).

---

## 6.9 El problema de las múltiples comparaciones

### La idea

Si haces **un** contraste con `α = 0,05`, tienes un 5 % de probabilidad de un falso positivo. Si
haces **muchos**, la probabilidad de **al menos uno** crece rápidamente:

```text
P(al menos un falso positivo) = 1 − (1 − α)^m
```

con `m` contrastes independientes. Con 20 estrategias sin ninguna ventaja:
`1 − 0,95^20 ≈ 64 %`. Lo más probable es que **alguna** parezca significativa.

### Bonferroni y Holm

- **Bonferroni:** multiplica cada p-valor por `m` (o, lo que es lo mismo, exige `p < α/m`). Es
  simple y muy conservador.
- **Holm:** un procedimiento **escalonado** igual de seguro y menos conservador. Se ordenan los
  p-valores de menor a mayor; el más pequeño se multiplica por `m`, el siguiente por `m − 1`, y
  así sucesivamente, obligando a que los valores ajustados no disminuyan. Se rechazan las
  hipótesis en orden **hasta la primera que no pase**; a partir de ahí, ninguna.

<!-- cita: src/bybit_quant_lab/validation/overfitting.py#L94-L106 -->
`src/bybit_quant_lab/validation/overfitting.py` · líneas 94–106

```python
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

- **96:** ordena los p-valores de menor a mayor (ignora los que no se pudieron calcular).
- **102:** `(m − i) · p` es el factor de Holm; `max(running, ...)` impide que un ajustado sea menor
  que el anterior; `min(1.0, ...)` lo limita a 1.
- **104:** `still` se vuelve falso en el primer fallo y ya no vuelve a ser verdadero.

Ejemplo a mano con cuatro p-valores `{a: 0,01; b: 0,04; c: 0,03; d: 0,005}` y `m = 4`:

| Orden | Hipótesis | p | Factor | p ajustado | ¿Rechaza? |
|---|---|---|---|---|---|
| 1 | d | 0,005 | ×4 | 0,02 | Sí |
| 2 | a | 0,01 | ×3 | 0,03 | Sí |
| 3 | c | 0,03 | ×2 | 0,06 | No (y se detiene aquí) |
| 4 | b | 0,04 | ×1 | máx(0,06; 0,04) = 0,06 | No |

**Supuestos:** Holm controla la probabilidad de **al menos un** falso positivo (la tasa de error
familiar) sin suponer que los contrastes son independientes, una ventaja cuando las estrategias
están correlacionadas.

<!-- ejecutar -->
```python
from bybit_quant_lab.validation.overfitting import holm_bonferroni

print(round(1 - 0.95 ** 20, 3))
resultado = holm_bonferroni({"a": 0.01, "b": 0.04, "c": 0.03, "d": 0.005})
for nombre in "dacb":
    print(nombre, resultado[nombre])
```
<!-- salida -->
```text
0.642
d {'p': 0.005, 'p_adj': 0.02, 'reject': True}
a {'p': 0.01, 'p_adj': 0.03, 'reject': True}
c {'p': 0.03, 'p_adj': 0.06, 'reject': False}
b {'p': 0.04, 'p_adj': 0.06, 'reject': False}
```

---

## 6.10 Bootstrap

### La idea

A veces no sabemos qué forma tiene la distribución de un resultado. El **bootstrap** la estima
con los propios datos: se crean muchas "muestras nuevas" **sacando valores al azar de la muestra
original con reemplazo** (un mismo valor puede salir varias veces), se calcula la estadística en
cada una y se observa cómo varía.

Analogía: tienes 40 papeletas con los resultados de tus operaciones en una urna. Sacas una,
anotas su valor, **la devuelves** a la urna y repites 40 veces. Calculas la media de esas 40.
Repites todo mil veces. Las mil medias muestran cuánto podría variar la media.

<!-- cita: src/bybit_quant_lab/validation/overfitting.py#L109-L119 -->
`src/bybit_quant_lab/validation/overfitting.py` · líneas 109–119

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
```

- **117:** genera de una vez `n_samples` remuestras del mismo tamaño que los datos y calcula la
  media de cada una.
- **118:** el intervalo de confianza **percentil** al 95 % son los percentiles 2,5 y 97,5 de esas
  medias.
- **116:** la semilla fija hace que el resultado sea reproducible.

**[Supuesto]** El bootstrap simple supone que las observaciones son **independientes** entre sí.
Si las operaciones ganadoras se concentran en rachas (por ejemplo, en una tendencia), el
intervalo será demasiado estrecho. Existen variantes por bloques que conservan la dependencia
temporal; el proyecto no las implementa.

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.validation.overfitting import bootstrap_mean_ci

pnl = pd.Series([120, -40, -35, 60, -30, 15, -25, 200, -45, 10, -20, 35] * 3, dtype=float)
print("media observada:", round(pnl.mean(), 2))
bajo, alto = bootstrap_mean_ci(pnl, n_samples=2000, seed=1)
print("IC 95 % bootstrap:", round(bajo, 2), "a", round(alto, 2))
```
<!-- salida -->
```text
media observada: 20.42
IC 95 % bootstrap: -0.69 a 44.03
```

La media observada es positiva (unos 20 USDT por operación), pero el intervalo incluye valores
negativos: con 36 operaciones de resultados tan dispersos, no se puede descartar que la ganancia
media verdadera sea cero o negativa. Una sola operación de +200 USDT, repetida tres veces en la
lista, pesa mucho en la media.

---

## 6.11 Sesgo de selección

### La idea

Si pruebas muchas estrategias y te quedas con la mejor, su resultado está **sesgado hacia
arriba**: la elegiste precisamente porque tuvo suerte. Aunque ninguna tenga ventaja real, la
mejor de cien parecerá buena.

<!-- ejecutar -->
```python
import numpy as np

rng = np.random.default_rng(3)
# 100 estrategias sin ninguna ventaja: Sharpe verdadero 0, ruido de muestra 0,5
sharpes_observados = rng.normal(0.0, 0.5, size=(5000, 100))
mejor = sharpes_observados.max(axis=1)
print("Sharpe verdadero de todas: 0.0")
print("Sharpe medio de la mejor de 100:", round(mejor.mean(), 2))
```
<!-- salida -->
```text
Sharpe verdadero de todas: 0.0
Sharpe medio de la mejor de 100: 1.25
```

La "mejor" de cien estrategias inútiles muestra en promedio un Sharpe de alrededor de 1,25. El
proyecto corrige este efecto con el **Deflated Sharpe Ratio** (Módulo XIII), que usa exactamente
esta idea: estima el Sharpe máximo que cabría esperar por azar entre `N` pruebas y exige superar
**ese** listón, no cero:

<!-- cita: src/bybit_quant_lab/validation/overfitting.py#L60-L66 -->
`src/bybit_quant_lab/validation/overfitting.py` · líneas 60–66

```python
def expected_max_sharpe(n_trials: int, sr_variance: float) -> float:
    """Sharpe máximo esperado bajo la hipótesis nula entre ``n_trials`` pruebas."""
    if n_trials <= 1 or sr_variance <= 0:
        return 0.0
    a = _N.inv_cdf(1 - 1 / n_trials)
    b = _N.inv_cdf(1 - 1 / (n_trials * math.e))
    return math.sqrt(sr_variance) * ((1 - EULER_GAMMA) * a + EULER_GAMMA * b)
```

---

## 6.12 Muestras de entrenamiento, validación y prueba

### La idea

Si usas los mismos datos para **elegir** una estrategia y para **medir** lo buena que es, la
medida estará sesgada (sección 6.11). La solución es dividir la historia en tramos con funciones
distintas:

- **Entrenamiento:** para ajustar parámetros y pesos.
- **Validación:** para elegir entre candidatos.
- **Prueba final (test):** para medir **una sola vez** el resultado de la elección, sin tocar
  nada después.

En series temporales la división debe ser **cronológica** (primero entrenamiento, luego
validación, luego test): mezclar fechas permitiría que el pasado "viera" el futuro. El Módulo XIII
desarrolla el procedimiento del proyecto y los errores que se corrigieron en la auditoría.

---

## 6.13 Estabilidad de los resultados

Un resultado **estable** no depende de un ajuste fino. Señales de alarma:

- El mejor parámetro está aislado: sus vecinos dan resultados mucho peores.
- El resultado cambia de signo al quitar las 3 mejores operaciones.
- Funciona en un símbolo o una temporalidad, pero no en los demás.

**[Hecho]** El proyecto mide las tres cosas: `stability_summary` (fracción de configuraciones
positivas de una rejilla, Módulo XIII), `top_trade_dependence` (`validation/overfitting.py`,
líneas 122–137) y `bql markets` (Módulo XV).

---

## 6.14 Tamaño de muestra, significancia estadística y significancia económica

- **Significancia estadística:** el resultado es difícilmente atribuible al azar.
- **Significancia económica:** el resultado es lo bastante grande como para que importe, después
  de costes y teniendo en cuenta el riesgo.

Son cosas distintas:

| Caso | Estadística | Económica |
|---|---|---|
| 100.000 operaciones con 0,01 USDT de ganancia media y comisiones de 0,05 USDT | Puede ser significativa | Pierde dinero tras costes |
| 8 operaciones con +500 USDT de media | No significativa (muestra minúscula) | Parece enorme, pero no es fiable |

**[Hecho]** El proyecto exige un mínimo de operaciones para presentar Sharpe y Sortino (10, salvo
exposición casi continua) y avisa por debajo de 30 operaciones (`min_trades_for_stats`), y
compara siempre el resultado **bruto** con el **neto de costes**.

### Comprobación final del módulo

Probaste 50 configuraciones y la mejor tiene un p-valor de 0,02. ¿Es un resultado significativo
al 5 %? Usa Bonferroni para responder.

<details><summary>Ver respuesta</summary>

No. Con 50 contrastes, Bonferroni exige `p < 0,05 / 50 = 0,001`. Un p-valor de 0,02 entre 50
pruebas es perfectamente compatible con el azar: con 50 estrategias sin ventaja, se espera que
una tenga `p ≤ 0,02` (50 × 0,02 = 1).
</details>
