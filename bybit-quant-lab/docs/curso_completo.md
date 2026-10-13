# Curso: bybit-quant-lab de cero a avanzado

> Documento generado con `scripts/curso_unificar.py` a partir de `docs/curso/` (commit `007df17`, 2026-10-13). Para corregirlo, edita los archivos de `docs/curso/` y vuelve a generarlo. Los comentarios de control de las citas se han eliminado: cada cita conserva la línea con su archivo y sus números de línea, y las respuestas de las comprobaciones aparecen desplegadas.

Manual de aprendizaje y libro de referencia técnica construido sobre **el código real** de
este repositorio. Cada capítulo explica primero la idea con palabras sencillas, después la
terminología técnica, y finalmente el código que la implementa, con la ruta exacta del archivo
y los números de línea.

> Este curso es material educativo sobre un software de **investigación**. Nada de lo que
> contiene es una recomendación de inversión. El sistema no envía órdenes a ningún exchange y
> ninguna estrategia se ha validado con datos reales de mercado (ver Módulo XVII).

## Cómo leer este curso

- **Si empiezas desde cero:** lee los módulos en orden. Cada uno usa lo aprendido en el anterior.
- **Si buscas algo concreto:** usa el índice de abajo o el glosario.
- **Si estás cansado:** las secciones empiezan, casi siempre, por la intuición (párrafos
  *Intuición* o *Analogía*), que se pueden leer solos. La profundidad técnica viene después y
  puedes volver a ella más tarde.
- **Tras cada concepto** hay una *Comprobación*: una pregunta o un ejercicio corto. La
  respuesta está plegada debajo (haz clic en "Ver respuesta"). Intenta responder antes de mirar.

## Convenciones

### Etiquetas de certeza

El curso distingue con cuidado entre lo que el código **demuestra** y lo que **supone**:

| Etiqueta | Significado |
|---|---|
| **[Hecho]** | Comportamiento comprobable leyendo el código o ejecutando las pruebas del repositorio. |
| **[Diseño]** | Una elección deliberada entre varias alternativas razonables. Se explica el porqué. |
| **[Supuesto]** | Algo que el código da por cierto pero que no se ha comprobado (por ejemplo, el formato real de la API de Bybit). |
| **[Limitación]** | Algo que el sistema no hace o hace de forma aproximada. |
| **[Pendiente]** | Algo que debe verificarse o implementarse antes de confiar en los resultados. |
| **[Discrepancia]** | Un texto (documentación, cabecera, informe) que no coincide con lo que hace el código. Manda el código. |
| **[Hallazgo]** | Un problema encontrado al revisar el código para este curso que la auditoría no recogía. Está verificado, pero no corregido. |

### Citas de código verificadas

Los fragmentos de código del repositorio aparecen así:

```text
<!-- cita: src/bybit_quant_lab/<archivo>.py#L<inicio>-L<fin> -->
```

(con números de línea reales) seguido del bloque con esas líneas exactas. Ese comentario HTML
no se ve en un visor de Markdown; encima de cada cita el texto indica igualmente el archivo y
las líneas. Todas las rutas son relativas a la carpeta
`bybit-quant-lab/`. Las citas **no están copiadas a mano**: las rellena y las comprueba el
script `scripts/curso_citas.py`.

```bash
python scripts/curso_citas.py --check   # ¿siguen coincidiendo las citas con el código?
python scripts/curso_citas.py --fill    # actualiza citas y salidas tras cambiar el código
```

Si cambias el código, `--check` te dirá qué partes del curso quedaron desfasadas.

Las citas de Python van rodeadas de `<!-- fmt: off -->` y `<!-- fmt: on -->` (comentarios
invisibles al leer). `ruff format` también formatea los bloques de Python dentro de Markdown, y
esos marcadores impiden que altere las citas, que deben coincidir carácter a carácter con el
código. Los ejemplos ejecutables, en cambio, sí siguen el formato de ruff.

### Ejemplos ejecutables

Los bloques marcados como ejecutables se han ejecutado de verdad con el entorno del proyecto.
Su salida, que aparece debajo, es la salida real, no una salida inventada. Puedes copiarlos en
un archivo y ejecutarlos con `python archivo.py` desde la carpeta `bybit-quant-lab/`, con el
entorno virtual activado.

### Estado del repositorio que describe el curso

- Rama `claude/festive-franklin-jqcjz2`; el curso describe el código del commit `30debc4`.
  Mientras se escribía, solo se añadieron el curso y `scripts/curso_citas.py`: el código de
  producción no cambió (`git diff 30debc4 -- src tests configs` está vacío).
- Python 3.13, pandas 3.0, numpy 2.5 y pydantic 2.14 en el entorno donde se verificó.
- 231 pruebas superadas, ruff y mypy sin errores (las secciones 14.6, 14.7 y 14.10 explican qué significa eso).

## Índice

| Módulo | Contenido |
|---|---|
| I. Entender el sistema | Qué problema resuelve, vocabulario del trading sistemático, mapa de la arquitectura, recorrido de una vela |
| II. Python aplicado al proyecto | Tipos, funciones, clases, herencia, type hints, dataclasses, enumeraciones, excepciones, entornos virtuales |
| III. Arquitectura e ingeniería de software | Capas, dependencias, configuración, validación, errores, logging, CLI, persistencia |
| IV. Conectividad con Bybit e ingeniería de datos | HTTP, el endpoint de velas, paginación, validación, Parquet, pruebas con respuestas simuladas |
| V. pandas, NumPy y series temporales | DataFrame, índices temporales, `shift`, `rolling`, NaN, huecos |
| VI. Matemáticas y estadística | Rendimientos, dispersión, correlación, probabilidad, contrastes, bootstrap, sesgo de selección |
| VII. Indicadores | EMA, ATR, RSI, MACD, Bollinger, StochRSI, ADX, OBV, VWAP, Donchian, volumen relativo |
| VIII. Las diez estrategias | Hipótesis, reglas, código, ejemplos y limitaciones de cada estrategia |
| IX. Combinación y regímenes | Votaciones, consenso, regímenes de mercado, redundancia |
| X. El motor de backtesting | Señal frente a ejecución, costes, stops, gaps, una operación completa calculada a mano |
| XI. Riesgo y contabilidad | Dimensionamiento, apalancamiento, margen, liquidación, límites diarios y drawdown |
| XII. Métricas | Sharpe, Sortino, drawdown, profit factor, CAGR y cómo no malinterpretarlos |
| XIII. Validación y sobreajuste | Train/validación/test, walk-forward, DSR, Holm, bootstrap, los errores de la auditoría |
| XIV. Tests, calidad y depuración | Pruebas unitarias y de integración, mocks, ruff, mypy, escribir la prueba antes del arreglo |
| XV. CLI, informes y uso práctico | Todas las órdenes `bql`, archivos que generan y un flujo completo de investigación |
| XVI. Modificar el proyecto con autonomía | Cómo leer un módulo, seguir una ejecución, añadir una estrategia sin tocar `src/` y once ejercicios graduados con solución |
| XVII. Limitaciones y camino a un sistema más riguroso | Qué está corregido, qué falta, qué hay que verificar antes de confiar |
| Glosario | Todos los términos técnicos, con el módulo donde se explican |

## Ruta mínima si tienes poco tiempo

1. Módulo I completo (el mapa mental de todo lo demás).
2. Módulo X, secciones 10.1 a 10.4 y 10.10 (cómo se simula una operación, calculada a mano).
3. Módulo XIII, secciones 13.1 a 13.5 (por qué un buen resultado histórico puede ser falso).
4. Módulo XVII (qué no debes creer todavía).

<div style="page-break-before: always;"></div>

# Módulo I. Entender el sistema antes de programar

Este módulo no exige saber programar. Su objetivo es que tengas un **mapa mental** del sistema
completo: qué problema resuelve, con qué vocabulario se describe y cómo viaja un dato desde
Bybit hasta un número en un informe. El resto del curso profundiza en cada pieza de este mapa.

---

## 1.1 Qué problema resuelve bybit-quant-lab

### La idea

Imagina que se te ocurre una regla para operar: "compro bitcoin cuando su precio supera el
máximo de los últimos 20 días". Antes de arriesgar dinero quieres saber qué habría pasado si
hubieras aplicado esa regla en el pasado, de forma disciplinada, sin excepciones. Hacer eso a
mano con miles de velas es imposible, y hacerlo mal es muy fácil: basta con mirar sin querer un
precio que todavía no conocías para que la regla parezca mucho mejor de lo que es.

`bybit-quant-lab` es un **laboratorio** para hacer esa pregunta con rigor:

1. Obtiene precios históricos de Bybit (o los importa, o los genera de forma sintética).
2. Aplica reglas de trading escritas como código (las "estrategias").
3. Simula las operaciones que esas reglas habrían producido, con costes realistas.
4. Mide los resultados con métricas estadísticas.
5. Intenta detectar si un buen resultado es real o fruto del azar o del sobreajuste.

### Lo que NO hace

El propio paquete lo declara en su primer archivo:

<!-- fmt: off -->
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
<!-- fmt: on -->

**[Hecho]** No hay ninguna función en el repositorio que envíe órdenes a un exchange. El cliente
de Bybit solo implementa tres consultas públicas de datos de mercado (lo verás en la sección
1.8). No hay claves API, ni contraseñas, ni conexión a una cuenta.

### Comprobación

¿Puede `bybit-quant-lab`, tal como está, comprar bitcoin en tu cuenta de Bybit?

**Respuesta:**

No. No contiene ningún endpoint de trading ni maneja credenciales. Solo lee datos públicos de
mercado y simula operaciones en memoria.

---

## 1.2 Trading sistemático e investigación cuantitativa

### La idea

- **Trading discrecional:** una persona decide cada operación mirando el mercado.
- **Trading sistemático:** las decisiones las toman reglas fijas y explícitas, escritas de
  antemano. Dos personas que apliquen la misma regla a los mismos datos obtienen exactamente
  las mismas operaciones.
- **Investigación cuantitativa** ("quant research"): el trabajo de formular esas reglas,
  probarlas con datos y medir con estadística si funcionan, cuánto riesgo tienen y si el
  resultado podría ser casualidad.

La ventaja del enfoque sistemático es que **se puede comprobar**. La desventaja es que también
se puede **engañar uno mismo** con mucha facilidad: si pruebas cien reglas, alguna parecerá
excelente por pura suerte. Gran parte de este proyecto (Módulo XIII) existe para defenderse de
ese autoengaño.

### Comprobación

Si pruebas 100 reglas que en realidad no tienen ninguna ventaja, ¿es probable que alguna
parezca buena en el pasado?

**Respuesta:**

Sí. Con suficientes intentos, el azar produce algún resultado que parece excelente. Por eso el
proyecto cuenta cuántas configuraciones se han probado y corrige las métricas por ese número
(Deflated Sharpe Ratio y corrección de Holm, Módulo XIII).

---

## 1.3 Vocabulario: indicador, señal, estrategia, orden, operación, posición

Estos términos se confunden a menudo. En este proyecto cada uno vive en un lugar distinto del
código, y entender la diferencia es la clave para entender la arquitectura.

| Término | Qué es (idea) | Ejemplo | Dónde vive en el código |
|---|---|---|---|
| **Precio / vela** | Lo que ocurrió en el mercado en un intervalo | La hora de 10:00 a 11:00 abrió en 100 y cerró en 102 | `data/` |
| **Indicador** | Un cálculo sobre precios pasados que resume algo | La media de los últimos 20 cierres | `indicators/core.py` |
| **Evento** | Una condición que se cumple en una vela concreta | "La media rápida cruzó por encima de la lenta" | Cada estrategia, `compute_events` |
| **Señal** | La exposición que la estrategia **quiere** tener al cierre de una vela: LONG, SHORT o FLAT | "Quiero estar comprado" | `strategies/base.py`, `generate_signals` |
| **Estrategia** | El conjunto de reglas que convierte indicadores en señales | "EMA Crossover" | `strategies/*.py` |
| **Orden** | La instrucción de comprar o vender que resulta de una señal | "Compra en la próxima apertura" | `backtesting/engine.py` (orden pendiente) |
| **Ejecución (fill)** | El precio al que realmente se compró o vendió | "Se compró a 102,02 por el deslizamiento" | `execution/` |
| **Posición** | Lo que tienes abierto ahora mismo | "0,5 BTC comprados a 102,02" | `portfolio/position.py` |
| **Operación (trade)** | Una posición desde que se abre hasta que se cierra, con su resultado | "Entré a 102,02, salí a 105, gané 1,49 USDT" | `portfolio/position.py` (`TradeRecord`) |

Algunas definiciones necesarias para leer la tabla:

- **LONG (largo):** posición que gana si el precio sube. Compras primero, vendes después.
- **SHORT (corto):** posición que gana si el precio baja. Vendes primero (algo que no tienes,
  porque operas un contrato derivado) y recompras después.
- **FLAT (neutral):** sin posición.

**[Diseño]** La separación es estricta: una estrategia **nunca** decide precios de ejecución ni
tamaños de posición. Solo dice qué exposición quiere. El motor decide si esa intención se puede
ejecutar, a qué precio y con qué tamaño. Así se pueden cambiar las reglas de ejecución sin tocar
las estrategias, y al revés.

El contrato de lo que produce una estrategia está escrito al principio de su clase base:

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/base.py` · líneas 1–21

```python
"""Interfaz común de estrategias y conversión de eventos en señales normalizadas.

Semántica de la salida de ``Strategy.generate_signals`` (una fila por vela, mismo índice):

``signal``
    Exposición **objetivo** decidida al cierre de la vela: ``1`` LONG, ``-1`` SHORT, ``0`` FLAT.
    Nunca se ejecuta en la misma vela: el motor la ejecuta en la apertura siguiente.
``conviction``
    Puntuación en ``[0, 1]`` (0 cuando ``signal == 0``). Es una medida de intensidad del
    setup definida por cada estrategia, **no** una probabilidad ni una predicción calibrada.
``stop_distance``
    Distancia (en precio) del stop de estrategia, por defecto ``ATR * stop_atr_mult``.
``take_profit_distance``
    Distancia del objetivo (``stop_distance * take_profit_r``) o NaN si no hay objetivo.
``trailing_distance``
    Distancia del trailing stop (``ATR * trailing_atr_mult``) o NaN si no se usa.

Las estrategias producen *eventos* (entradas y salidas). ``events_to_state`` los convierte en
un estado persistente con reglas explícitas: conflicto de entradas en la misma vela -> FLAT,
reversión directa si hay entrada opuesta, salida por tiempo máximo y enfriamiento.
"""
```
<!-- fmt: on -->

Fíjate en la frase "Nunca se ejecuta en la misma vela": es la primera defensa contra el error
más grave del backtesting, que verás a continuación.

### Comprobación

Una estrategia devuelve `signal = 1` al cierre de la vela de las 10:00. ¿Significa que se compró
a ese precio de cierre?

**Respuesta:**

No. `signal = 1` es una **intención** ("quiero estar largo"). El motor programa una orden que se
ejecuta en la **apertura de la vela siguiente**, con deslizamiento y comisión. Además, la entrada
puede rechazarse (por un límite de riesgo, por un tamaño demasiado pequeño, etc.).

---

## 1.4 Qué es un backtest y para qué sirve

### La idea

Un **backtest** es una simulación: se recorren los datos históricos vela a vela, en orden, y en
cada vela se aplica la regla **usando solo la información que se conocía en ese momento**. Al
final se obtienen la lista de operaciones y la evolución del capital.

Sirve para:

- descartar ideas que ni siquiera funcionaron en el pasado;
- medir cuánto riesgo habrían tenido (pérdidas máximas, rachas);
- entender cuánto de la ganancia se comen los costes.

No sirve para:

- **demostrar** que una regla funcionará en el futuro;
- reproducir con exactitud lo que habría ocurrido con dinero real (deslizamientos, liquidez,
  caídas del exchange... todo se aproxima).

### El error más grave: el look-ahead bias

**Look-ahead bias** (sesgo de anticipación) es usar, sin darse cuenta, información del futuro
para tomar una decisión del pasado. Un ejemplo típico: calcular una señal con el precio de
cierre de una vela y "comprar" a ese mismo precio de cierre. En la realidad, cuando conoces el
cierre la vela ya terminó y ese precio ya no está disponible. El resultado parece mejor de lo
que es, a veces muchísimo mejor.

El motor del proyecto documenta en su primer bloque el orden exacto en que procesa cada vela
para evitarlo:

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 1–20

```python
"""Motor de backtesting determinista, vela a vela.

Orden de eventos dentro de cada vela ``i`` (índice = apertura de la vela):

1. Cambio de día UTC -> el gestor de riesgo reinicia la referencia diaria.
2. Funding: los pagos con marca de tiempo en ``(open[i-1], open[i]]`` se aplican a la
   posición mantenida al final de la vela ``i-1``, valorada a ``open[i]``.
3. Gap: si la apertura supera el stop/liquidación/objetivo, salida a la apertura.
4. Órdenes pendientes decididas al cierre de ``i-1``: primero salida, después entrada, ambas
   a ``open[i]`` con slippage adverso y comisión taker.
5. Intravela: stop/liquidación/objetivo con la regla *stop primero* (ver ``execution.fills``).
6. Cierre: valoración mark-to-market, registro de equity, límites de riesgo.
7. Trailing stop: se actualiza con el cierre y rige desde la vela siguiente.
8. Señal al cierre de ``i``: se programan órdenes para ``open[i+1]``. Nunca se ejecuta una
   señal al precio de la vela en que se generó.

Las entradas son *edge-triggered*: solo se abre posición cuando el objetivo de la estrategia
cambia a LONG/SHORT. Si un stop cierra la operación y la estrategia sigue en LONG, no se
reabre hasta una nueva transición. Las entradas rechazadas por riesgo no se difieren.
"""
```
<!-- fmt: on -->

No necesitas entender aún cada paso; el Módulo X los explica uno por uno. Lo importante ahora es
el paso 8: **la decisión se toma al cierre de la vela `i` y se ejecuta en la apertura de `i+1`**.

### Comprobación

¿Por qué es peligroso que una regla use el precio de cierre de una vela para decidir y ejecute
la compra a ese mismo cierre?

**Respuesta:**

Porque el precio de cierre solo se conoce cuando la vela ya terminó: en la realidad ya no
podrías comprar a ese precio. La simulación estaría usando información "del futuro" respecto al
momento de la orden y los resultados serían artificialmente buenos.

---

## 1.5 OHLCV: cómo se representa una vela

### La idea

El precio de un activo cambia miles de veces por minuto. Para trabajar con él se resume en
intervalos fijos llamados **velas** (candles). Cada vela guarda cinco números:

| Letra | Nombre | Significado |
|---|---|---|
| **O** | Open | Precio de la primera operación del intervalo (apertura) |
| **H** | High | Precio máximo alcanzado |
| **L** | Low | Precio mínimo alcanzado |
| **C** | Close | Precio de la última operación (cierre) |
| **V** | Volume | Cantidad negociada (en Bybit lineal, en unidades del activo base, p. ej. BTC) |

De ahí el nombre **OHLCV**. El proyecto guarda además `turnover` (volumen en la moneda de
cotización, USDT).

La **temporalidad** (timeframe) es la duración de cada vela: 5 minutos (`5m`), 15 minutos
(`15m`), 1 hora (`1h`), 4 horas (`4h`)...

**[Hecho]** En todo el proyecto, la marca de tiempo de una vela es su **apertura** en **UTC**
(Tiempo Universal Coordinado, la hora de referencia mundial, sin horario de verano). La vela
`2024-01-01 10:00` de 1h cubre de 10:00 a 10:59:59.

### Ejemplo con el generador sintético del proyecto

El proyecto puede generar velas **sintéticas** (inventadas por un modelo aleatorio con semilla
fija) para probar la lógica sin conexión a internet. No representan ningún mercado real:

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv

velas = generate_synthetic_ohlcv(bars=3, timeframe="1h", seed=42)
# to_string() imprime la tabla completa; se omite 'turnover' para que quepa en pantalla
print(velas[["open", "high", "low", "close", "volume"]].round(2).to_string())
```
*Salida real:*

```text
                               open      high       low     close   volume
open_time                                                                 
2023-01-01 00:00:00+00:00  30000.00  30220.29  29998.19  30078.95  1395.57
2023-01-01 01:00:00+00:00  30095.93  30109.79  29824.04  29915.77  1241.96
2023-01-01 02:00:00+00:00  29880.77  30109.09  29786.32  30074.83  1699.84
```

Cada fila es una vela; el índice de la izquierda es la hora de apertura en UTC (`+00:00`). Observa
que siempre se cumple `low <= open, close <= high`: es una de las comprobaciones que el
proyecto hace al validar datos (Módulo IV).

### Comprobación

Una vela de 1h tiene open = 100, high = 103, low = 99, close = 98. ¿Es válida?

**Respuesta:**

No: el cierre (98) es menor que el mínimo (99). El mínimo debe ser menor o igual que la apertura y
el cierre. `data/validation.py` la contaría como vela inválida y la limpieza la descartaría.

---

## 1.6 Futuros perpetuos lineales

### La idea

El proyecto no simula la compra de bitcoin "real", sino de **contratos de futuros perpetuos
lineales USDT** de Bybit (por ejemplo, `BTCUSDT`).

- **Contrato de futuros:** un acuerdo cuyo valor sigue al precio de un activo. Permite ganar si
  sube (largo) **o si baja** (corto) sin poseer el activo.
- **Perpetuo:** no tiene fecha de vencimiento.
- **Lineal / USDT:** las ganancias, pérdidas y garantías se calculan en USDT (una moneda estable
  ligada al dólar). Si compras 0,1 BTC de contrato y el precio sube 1.000 USDT, ganas
  0,1 × 1.000 = 100 USDT.
- **Funding (financiación):** como el perpetuo no vence, cada cierto tiempo (normalmente cada
  8 horas en Bybit) los largos pagan a los cortos, o al revés, una pequeña tasa para que el
  precio del contrato no se aleje del precio al contado. Es un coste o un ingreso real.
- **Apalancamiento y margen:** solo se deposita una parte del valor de la posición como
  garantía (el **margen**). Con apalancamiento 3, una posición de 3.000 USDT requiere 1.000 USDT
  de margen. Si las pérdidas consumen el margen, el exchange cierra la posición a la fuerza
  (**liquidación**). El Módulo XI lo explica con números.

**[Limitación]** El simulador modela estos conceptos de forma aproximada (liquidación con una
tasa de mantenimiento fija, funding solo si se descargó). Lo verás en los Módulos X, XI y XVII.

### Comprobación

Tienes un corto de 0,2 BTC abierto a 50.000 USDT y el precio baja a 49.000. ¿Ganas o pierdes, y
cuánto, sin contar costes?

**Respuesta:**

Ganas, porque un corto gana cuando el precio baja: 0,2 × (50.000 − 49.000) = 200 USDT.

---

## 1.7 Bybit, APIs, HTTP y JSON (visión general)

### La idea

Bybit es un **exchange** (mercado) de criptomonedas. Además de su web, ofrece una **API**
(Application Programming Interface, "interfaz de programación"): una forma de que un programa le
pida datos directamente.

- **HTTP** es el protocolo con el que tu navegador pide páginas web. Un programa lo usa igual:
  envía una **petición** (request) a una dirección y recibe una **respuesta** (response).
- Una **API REST** organiza esas peticiones como direcciones legibles. Cada dirección concreta
  que ofrece un servicio se llama **endpoint**. Por ejemplo, `/v5/market/kline` es el endpoint de
  velas ("kline" es otro nombre de vela) de la versión 5 de la API de Bybit.
- **GET** es el tipo de petición para **leer** datos sin modificar nada.
- **JSON** (JavaScript Object Notation) es el formato de texto de la respuesta: listas `[...]`,
  diccionarios `{"clave": valor}`, textos y números.
- **API pública:** endpoints que no requieren identificarse, porque solo devuelven datos de
  mercado. Los endpoints **privados** (crear órdenes, consultar saldos) requieren claves. El
  proyecto solo usa endpoints públicos.

Una petición de velas tiene esta forma (la explicaremos parámetro a parámetro en el Módulo IV):

```text
GET https://api.bybit.com/v5/market/kline?category=linear&symbol=BTCUSDT&interval=60&start=1704067200000&end=1707667199999&limit=1000
```

**[Pendiente]** En el entorno donde se desarrolló el proyecto, la red bloqueaba `api.bybit.com`.
El cliente se probó con **respuestas simuladas** que imitan el formato documentado, pero **no**
con la API real. El Módulo IV detalla qué está comprobado y qué no.

### Comprobación

¿Qué diferencia hay entre un endpoint público y uno privado?

**Respuesta:**

El público devuelve información de mercado accesible para cualquiera, sin identificarse. El
privado actúa sobre una cuenta (órdenes, saldos) y exige claves de autenticación. El proyecto
solo usa públicos.

---

## 1.8 Qué partes son investigación y cuáles podrían tocar dinero real

**[Hecho]** Ninguna parte toca dinero real. El cliente HTTP declara exactamente qué endpoints usa:

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 1–11

```python
"""Cliente de solo lectura para la API pública de mercado de Bybit V5.

Endpoints usados (públicos, sin autenticación):

* ``GET /v5/market/kline`` — velas OHLCV (máx. 1000 por petición).
* ``GET /v5/market/funding/history`` — historial de funding (máx. 200 por petición).
* ``GET /v5/market/instruments-info`` — especificaciones del instrumento.

Este módulo no implementa, ni implementará en el flujo predeterminado, ningún endpoint de
trading. No acepta ni almacena claves API.
"""
```
<!-- fmt: on -->

Los tres son de la familia `/v5/market/`, que en la API de Bybit agrupa datos públicos de
mercado. Puedes comprobarlo tú mismo buscando cualquier otra ruta en el código:

*Ejemplo ejecutable:*

```python
import pathlib
import re

rutas = set()
for archivo in pathlib.Path("src").rglob("*.py"):
    rutas.update(re.findall(r'"(/v5/[a-z/-]+)"', archivo.read_text(encoding="utf-8")))
print(sorted(rutas))
```
*Salida real:*

```text
['/v5/market/funding/history', '/v5/market/instruments-info', '/v5/market/kline']
```

---

## 1.9 Un sistema modular: qué hace cada directorio

### La idea

Un sistema es **modular** cuando está dividido en piezas con una responsabilidad clara que se
comunican mediante "contratos" sencillos. Es como una cocina profesional: quien corta verduras no
necesita saber cómo se emplata. Si cambias el proveedor de verduras, la receta sigue igual.

### Mapa de directorios

Todo el código está en `src/bybit_quant_lab/`:

| Directorio | Responsabilidad | Recibe | Entrega |
|---|---|---|---|
| `config/` | Leer y validar la configuración (YAML) | Archivos `configs/*.yaml` | Objetos `AppConfig` validados |
| `data/` | Descargar, validar, limpiar, guardar e importar velas | API de Bybit, CSV, Parquet | Tabla OHLCV limpia en UTC |
| `indicators/` | Cálculos técnicos causales | Series de precios | Series de indicadores |
| `strategies/` | Las diez estrategias y su interfaz común | Tabla OHLCV | Tabla de señales |
| `signals/` | Combinar señales, clasificar el régimen, medir redundancia | Señales de varias estrategias | Una señal combinada |
| `execution/` | Costes y resolución de stops, objetivos y gaps | Precios y niveles | Precio de ejecución y motivo |
| `risk/` | Dimensionar posiciones y aplicar límites del sistema | Capital, stop, configuración | Cantidad a operar, bloqueos |
| `portfolio/` | Representar la cuenta, la posición y las operaciones | Ejecuciones | Estado contable |
| `backtesting/` | El motor que recorre las velas | Datos + señales + configuración | `BacktestResult` |
| `analytics/` | Métricas de rendimiento y riesgo | `BacktestResult` | Diccionario de métricas |
| `validation/` | Segmentos, walk-forward, benchmarks, estadística anti-sobreajuste, flujos de investigación | Datos, estrategias | Tablas comparativas, selección |
| `reporting/` | Informes HTML, CSV y JSON con metadatos | Resultados y métricas | Archivos en `outputs/` |
| `cli.py` | La orden `bql` de la terminal | Argumentos del usuario | Ejecuta todo lo anterior |

Fuera de `src/`:

| Ruta | Contenido |
|---|---|
| `configs/default.yaml` | Costes, riesgo, segmentos de validación, origen de datos |
| `configs/strategies.yaml` | Parámetros de las diez estrategias, combinaciones y rejillas de búsqueda |
| `tests/` | 231 pruebas automáticas (unitarias e integración) |
| `docs/` | Documentación técnica, informe de auditoría y este curso |
| `data/` | Datos descargados (excluidos de Git) |
| `outputs/` | Resultados de las ejecuciones (excluidos de Git) |
| `scripts/` | Verificación de instalación y herramienta de citas del curso |
| `examples/` | Un flujo completo de ejemplo con datos sintéticos |

### Diagrama de flujo

```text
          Bybit (API pública)        CSV / Parquet          Generador sintético
                  │                        │                        │
                  └────────────┬───────────┴────────────┬───────────┘
                               v                        v
                     data/ (descargar, validar, limpiar, guardar Parquet)
                               │  tabla OHLCV en UTC
                               v
                     indicators/  ──>  strategies/  ──>  signals/ (opcional)
                                           │ tabla de señales (LONG/SHORT/FLAT + stops)
                                           v
        execution/ (costes, fills) <── backtesting/engine ──> risk/ (tamaño, límites)
                                           │                  portfolio/ (cuenta)
                                           v
                                   BacktestResult (equity, operaciones, eventos)
                                           │
                   ┌───────────────────────┼──────────────────────┐
                   v                       v                      v
              analytics/             validation/              reporting/
              (métricas)      (train/val/test, DSR...)   (HTML, CSV, JSON)
```

Las flechas indican quién **usa** a quién. Observa que las estrategias no apuntan al motor: no
lo conocen. El motor recibe sus señales como una tabla, sin saber qué estrategia las produjo.

### Comprobación

Si mañana quisieras cambiar el modelo de comisiones, ¿qué directorio tocarías? ¿Tendrías que
modificar alguna estrategia?

**Respuesta:**

`execution/costs.py` (y la sección `costs` de `configs/default.yaml`). No habría que tocar
ninguna estrategia: las estrategias no saben nada de comisiones.

---

## 1.10 El recorrido completo de una vela

Sigamos una vela desde el exchange hasta una métrica. Entre paréntesis está el archivo y la
función que hace cada paso; los módulos siguientes los explican en detalle.

1. **Petición.** `bql download` crea un cliente y pide velas a Bybit en ventanas de hasta 1000
   (`cli.py`, `cmd_download` → `data/bybit_client.py`, `fetch_klines`).
2. **Traducción.** La respuesta JSON trae los números como texto y la lista en orden inverso. El
   cliente la convierte en una tabla con fechas UTC y números decimales (`_parse_klines`).
3. **Limpieza y guardado.** Se eliminan duplicados y velas imposibles, se informan los huecos y
   se guarda en `data/processed/BTCUSDT_1h.parquet` con un archivo de metadatos
   (`data/downloader.py`, `download_ohlcv` → `data/validation.py`, `clean_ohlcv` →
   `data/storage.py`, `save_dataset`).
4. **Carga.** Una orden como `bql backtest` lee el Parquet y comprueba su validez
   (`cli.py`, `_load_data`).
5. **Indicadores y señal.** La estrategia calcula sus indicadores con datos hasta cada vela y
   decide la exposición deseada al cierre (`strategies/<estrategia>.py`, `compute_events` →
   `strategies/base.py`, `generate_signals`).
6. **Simulación.** El motor ve la señal al cierre de la vela `i`, dimensiona la posición según
   el riesgo y la ejecuta en la apertura de `i+1` con deslizamiento y comisión. Después vigila
   stops y objetivos vela a vela (`backtesting/engine.py`, `BacktestEngine.run`).
7. **Contabilidad.** Al cerrar la operación se registra su resultado bruto, costes, funding y
   resultado neto (`TradeRecord` en `portfolio/position.py`).
8. **Métricas.** Con la curva de capital y la lista de operaciones se calculan Sharpe, drawdown,
   profit factor, etc. (`analytics/metrics.py`, `compute_metrics`).
9. **Validación.** Se repite en segmentos de entrenamiento y validación, se compara con
   benchmarks y se corrige por el número de pruebas (`validation/research.py`).
10. **Informe.** Todo se escribe en HTML, CSV y JSON con los metadatos para reproducirlo
    (`reporting/`).

### Los pasos 5 a 8 ejecutados de verdad

Este programa hace los pasos 5 a 8 con datos sintéticos (los pasos 1 a 4 necesitan Bybit o un
archivo; aquí los sustituye el generador). Los números describen datos inventados y **no dicen
nada sobre ningún mercado real**:

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.analytics import compute_metrics
from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config import AppConfig
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=2000, timeframe="1h", seed=1)  # sustituye a pasos 1-4
senales = create_strategy("ema_crossover").generate_signals(datos)  # paso 5
resultado = run_backtest(datos, senales, AppConfig(), "BTCUSDT", "1h")  # pasos 6-7
metricas = compute_metrics(resultado)  # paso 8

print("velas simuladas:", len(resultado.equity))
print("operaciones:", metricas["num_trades"])
print("primera operación:")
print(resultado.trades.iloc[0][["side", "entry_time", "entry_price", "exit_reason", "net_pnl"]])
print("capital final:", round(metricas["final_equity"], 2))
print("advertencias:", len(metricas["warnings"]))
```
*Salida real:*

```text
velas simuladas: 2000
operaciones: 15
primera operación:
side                               SHORT
entry_time     2023-01-14 11:00:00+00:00
entry_price                 31208.680363
exit_reason                  signal_exit
net_pnl                        19.412236
Name: 0, dtype: object
capital final: 9124.07
advertencias: 4
```

Todo lo que ves en esta salida (cómo se eligió la entrada, de dónde sale el precio con decimales,
por qué hay advertencias) se explica en los módulos siguientes.

### Comprobación final del módulo

Ordena estos pasos: (a) se calcula el Sharpe; (b) la estrategia devuelve `signal = 1`; (c) la
orden se ejecuta en la apertura siguiente; (d) se descarga la vela; (e) se cierra la operación
por stop-loss.

**Respuesta:**

(d) → (b) → (c) → (e) → (a).

<div style="page-break-before: always;"></div>

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

<!-- fmt: off -->
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
<!-- fmt: on -->

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

<!-- fmt: off -->
`src/bybit_quant_lab/timeframes.py` · líneas 18–18

```python
MINUTES_PER_YEAR = 365 * 24 * 60  # mercado cripto 24/7, año de 365 días
```
<!-- fmt: on -->

`365 * 24 * 60` multiplica días × horas × minutos: el número de minutos de un año de 365 días.
La convención de MAYÚSCULAS indica una **constante**: un valor que no debe cambiar mientras el
programa funciona (Python no lo impide; es un acuerdo entre programadores).

Operadores que verás a menudo:

- Aritméticos: `+ - * /`, `//` (división entera), `%` (resto), `**` (potencia).
- Comparación: `== != < <= > >=` (devuelven `True` o `False`).
- Lógicos: `and`, `or`, `not`.
- Pertenencia: `in` ("¿está este elemento en esta colección?").

*Ejemplo ejecutable:*

```python
minutos_por_anio = 365 * 24 * 60
velas_de_1h = minutos_por_anio / 60  # "/" siempre devuelve float
velas_de_4h = minutos_por_anio // 240  # "//" descarta los decimales
print(minutos_por_anio, velas_de_1h, velas_de_4h)
print(10_000 * 0.01)  # el guion bajo separa miles, no cambia el número
print(0.1 + 0.2 == 0.3, abs((0.1 + 0.2) - 0.3) < 1e-12)
```
*Salida real:*

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

**Respuesta:**

`3 1 8`: división entera, resto y potencia.

---

## 2.3 Condicionales y bucles

### La idea

- Un **condicional** (`if / elif / else`) ejecuta un bloque solo si se cumple una condición.
- Un **bucle** `for` repite un bloque para cada elemento de una secuencia.

La función `events_to_state` de `strategies/base.py` usa ambos, y es una de las funciones más
importantes del proyecto: convierte "eventos" (momentos en que se cumple una condición de
entrada o salida) en un "estado" que se mantiene vela tras vela.

<!-- fmt: off -->
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
<!-- fmt: on -->

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

*Ejemplo ejecutable:*

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
*Salida real:*

```text
[0, 1, 1, -1, 0, 0]
```

Lectura: vela 1, entrada larga → 1. Vela 3, entrada corta estando largos → reversión a −1.
Vela 4, salida corta → 0. Después no hay más eventos.

### Comprobación

Con `cooldown_bars=2`, tras salir en la vela 4, ¿en qué vela podría volver a entrar como pronto?

**Respuesta:**

En la vela 4 se pone `since_exit = 0`. En la vela 5 pasa a 1, en la 6 a 2 y en la 7 a 3. La
condición es `since_exit > 2`, así que la primera vela posible es la **7**.

---

## 2.4 Funciones: parámetros, argumentos, retorno y alcance

### La idea

Una **función** es un bloque de código con nombre que recibe datos (**parámetros**), hace algo
y devuelve un resultado (**valor de retorno**). Cuando la llamas, los valores que le pasas son
los **argumentos**.

`timeframes.py` contiene cinco funciones pequeñas que se llaman unas a otras:

<!-- fmt: off -->
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
<!-- fmt: on -->

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

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.timeframes import bars_per_year, bybit_interval, timeframe_minutes

print(timeframe_minutes("4h"), bybit_interval("4h"), bars_per_year("1h"))
try:
    timeframe_minutes("2h")
except ValueError as error:
    print("Error:", error)
```
*Salida real:*

```text
240 240 8760.0
Error: Temporalidad no soportada: '2h'. Opciones: ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
```

### Comprobación

¿Qué devuelve `bybit_interval("1h")` y por qué no devuelve `"1h"`?

**Respuesta:**

Devuelve `"60"`: es el código que espera la API de Bybit para velas de 60 minutos. La función
traduce el nombre interno del proyecto al código de la API.

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

<!-- fmt: off -->
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
<!-- fmt: on -->

Una **tupla** define las columnas que toda señal debe tener. Se usa tupla y no lista porque no
debe modificarse:

<!-- fmt: off -->
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
<!-- fmt: on -->

Un **conjunto** guarda los códigos de error que merece la pena reintentar. Se usa conjunto
porque la única pregunta que se le hace es "¿este código está aquí?", y esa consulta es muy
rápida en un conjunto:

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 27–30

```python
#: retCode de Bybit considerados transitorios (10000: timeout del servidor,
#: 10006: demasiadas peticiones, 10016: error interno del servidor).
RETRYABLE_RET_CODES = {10000, 10006, 10016}
RETRYABLE_HTTP = {429, 500, 502, 503, 504}
```
<!-- fmt: on -->

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.timeframes import TIMEFRAMES

codigo, minutos = TIMEFRAMES["15m"]  # "desempaquetar" una tupla en dos variables
print(codigo, minutos)
print(list(TIMEFRAMES)[:3])  # recorrer un diccionario da sus claves
print(10006 in {10000, 10006, 10016})  # pertenencia en un conjunto
operaciones = []
operaciones.append(12.5)
operaciones.append(-3.0)
print(operaciones, len(operaciones), sum(operaciones))
```
*Salida real:*

```text
15 15
['1m', '5m', '15m']
True
[12.5, -3.0] 2 9.5
```

### Comprobación

¿Por qué `RETRYABLE_HTTP` es un conjunto y no una lista? ¿Funcionaría con una lista?

**Respuesta:**

Funcionaría igual (`429 in [429, 500]` también es `True`), pero el conjunto expresa mejor la
intención (no importa el orden ni puede haber repetidos) y la consulta de pertenencia es más
rápida. Con cinco elementos la diferencia de velocidad es irrelevante; la claridad no.

---

## 2.6 Comprensiones y expresiones generadoras

### La idea

Una **comprensión** construye una colección a partir de otra en una sola expresión:
`[x * 2 for x in numeros if x > 0]` significa "para cada `x` de `numeros` que sea positivo,
pon `x * 2` en una lista nueva".

El registro de experimentos (`validation/experiment_log.py`) usa los tres tipos:

<!-- fmt: off -->
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
<!-- fmt: on -->

- **Línea 35:** comprensión de **lista**. Lee cada línea del archivo, ignora las vacías
  (`if line.strip()`) y convierte cada una de JSON a diccionario.
- **Líneas 39–44:** **expresión generadora** dentro de `sum(...)`. Produce un `1` por cada
  registro que cumple los filtros y `sum` los suma: es una forma de contar. A diferencia de una
  lista, no guarda todos los `1` en memoria a la vez; los va generando uno a uno.
- **Líneas 54–61:** comprensión de **conjunto** (llaves `{...}`). Convierte cada combinación
  "candidato + parámetros" en un texto y, al ser un conjunto, los repetidos se eliminan solos.
  `len(keys)` es entonces el número de configuraciones **distintas** probadas, un dato clave para
  corregir el sesgo de selección (Módulo XIII).

*Ejemplo ejecutable:*

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
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

Buscar una clave inexistente en un diccionario lanza `KeyError`. El código la captura y lanza
otra `KeyError` con un mensaje útil, que incluye la lista de estrategias disponibles.

El cliente HTTP define su **propia** excepción, heredando de una de Python (la herencia se
explica en 2.11):

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 33–34

```python
class BybitAPIError(RuntimeError):
    """Error no recuperable o reintentos agotados al consultar Bybit."""
```
<!-- fmt: on -->

Tener un tipo propio permite que la CLI capture exactamente los errores de Bybit y los muestre
de forma limpia, sin capturar por accidente errores de programación.

Y así captura los errores de red para reintentar en lugar de rendirse:

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 98–102

```python
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout_seconds)
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_error = f"error de red: {exc}"
                continue
```
<!-- fmt: on -->

`continue` salta a la siguiente vuelta del bucle de reintentos (lo verás completo en el
Módulo IV).

**[Diseño] Errores frecuentes que el proyecto evita:**

- `except:` sin tipo, que captura **todo** (incluso fallos de programación) y los oculta. El
  proyecto siempre indica el tipo concreto.
- Capturar un error y no hacer nada. El proyecto reintenta, re-lanza con un mensaje mejor o
  registra el problema.

### Comprobación

¿Qué ventaja tiene `raise KeyError(...) from exc` frente a `raise KeyError(...)` a secas?

**Respuesta:**

La traza de error mostrará las dos excepciones: la original (la clave que faltaba) y la nueva
(con el mensaje explicativo). Sin `from exc` también se encadenan de forma implícita, pero con
un mensaje que sugiere un segundo fallo accidental; `from exc` indica que la sustitución es
deliberada.

---

## 2.8 Módulos, paquetes e importaciones

### La idea

- Un **módulo** es un archivo `.py`.
- Un **paquete** es una carpeta con un archivo `__init__.py`; agrupa módulos.
- `import` y `from ... import ...` traen código de otros módulos.

La ruta `bybit_quant_lab.strategies.ema_crossover` corresponde al archivo
`src/bybit_quant_lab/strategies/ema_crossover.py`.

El `__init__.py` del paquete de estrategias tiene un detalle importante:

<!-- fmt: off -->
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
<!-- fmt: on -->

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

<!-- fmt: off -->
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
<!-- fmt: on -->

- **Líneas 15–31:** los atributos y sus tipos. Algunos tienen valor por defecto (`= 0.0`).
- **Líneas 33–36:** `@property` convierte un método en algo que se lee como un atributo:
  `posicion.notional_entry` (sin paréntesis) calcula `qty * entry_price` cada vez.
- **Líneas 38–40:** el método `unrealized` calcula la ganancia o pérdida "en papel" a un precio
  dado. `self` es el propio objeto: `self.side` es el lado de **esta** posición. El truco de
  multiplicar por `side` (+1 largo, −1 corto) sirve para ambos casos con una sola fórmula.
- **Líneas 42–53:** `update_trailing` **modifica** el objeto: mueve el stop si el precio
  avanzó a favor. `max(self.stop, candidate)` garantiza que el stop de un largo nunca baja.

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.portfolio.position import Position

p = Position(
    side=1,
    qty=0.5,
    entry_price=100.0,
    entry_time=pd.Timestamp("2024-01-01", tz="UTC"),
    entry_bar=0,
    stop=95.0,
    take_profit=None,
    trailing_distance=4.0,
    liquidation_price=None,
    margin=16.67,
    entry_fee=0.0,
    entry_slippage=0.0,
    extreme=100.0,
)
print(p.notional_entry, p.unrealized(104.0))
for cierre in (103.0, 106.0, 102.0):
    p.update_trailing(cierre)
    print(f"cierre {cierre}: stop = {p.stop}")
```
*Salida real:*

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

**Respuesta:**

`-1 × (45 − 50) × 2 = 10`. Ganancia de 10, como corresponde a un corto cuando el precio baja.

---

## 2.10 Dataclasses

### La idea

Escribir una clase que solo guarda datos exige mucho código repetitivo (un método para
inicializar, otro para mostrarla, otro para compararla). El decorador `@dataclass` lo genera
automáticamente a partir de la lista de atributos. `Position` y `TradeRecord` son dataclasses.

`CostModel` usa además `frozen=True`, que hace los objetos **inmutables**: una vez creado, nadie
puede cambiar sus comisiones por error a mitad de una simulación.

<!-- fmt: off -->
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
<!-- fmt: on -->

- **`@classmethod` (líneas 23–26):** un método que se llama sobre la **clase**, no sobre un
  objeto, y suele usarse como constructor alternativo: `CostModel.from_config(cfg)` crea un
  modelo de costes a partir de la configuración. `cls` es la propia clase.
- **`slip` (líneas 28–31):** convierte puntos básicos en fracción. Un **punto básico** (bps) es
  una centésima de punto porcentual: 2 bps = 0,02 % = 0,0002.
- **`fill_price` (líneas 33–35):** el deslizamiento siempre es **adverso**. Al comprar
  (`direction=+1`) pagas más; al vender (`-1`) recibes menos.

La clase `Account` usa `__post_init__`, un método que la dataclass ejecuta justo después de crear
el objeto, para que el efectivo inicial sea igual al capital:

<!-- fmt: off -->
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
<!-- fmt: on -->

`field(default_factory=list)` (línea 32) evita un error clásico de Python: si escribieras
`history: list = []`, **todas** las cuentas compartirían la misma lista.

*Ejemplo ejecutable:*

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
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

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

<!-- fmt: off -->
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
<!-- fmt: on -->

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

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import Strategy, available_strategies, create_strategy

datos = generate_synthetic_ohlcv(bars=600, seed=3)
for nombre in available_strategies()[:3]:
    estrategia = create_strategy(nombre)
    senales = estrategia.generate_signals(datos)  # misma llamada, distinto comportamiento
    print(nombre, isinstance(estrategia, Strategy), int((senales["signal"] != 0).sum()))
try:
    Strategy()
except TypeError as error:
    print("No se puede instanciar la clase abstracta:", str(error)[:60])
```
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

Escribir

```python
@register
class EMACrossoverStrategy(Strategy): ...
```

equivale exactamente a

```python
class EMACrossoverStrategy(Strategy): ...


EMACrossoverStrategy = register(EMACrossoverStrategy)
```

`register` guarda la clase en el diccionario `_REGISTRY` bajo su nombre y la devuelve sin
cambios. El guion bajo de `_REGISTRY` indica que es interno: desde fuera se consulta con
`available_strategies()` y `create_strategy()`.

### Comprobación

¿Qué ocurre si dos clases distintas usan el mismo `name = "ema_crossover"`?

**Respuesta:**

La segunda llamada a `register` encuentra el nombre ya ocupado por otra clase (`is not cls`) y
lanza `ValueError("Estrategia duplicada: ema_crossover")` al importar el módulo.

---

## 2.13 Enumeraciones

### La idea

Una **enumeración** (enum) es un conjunto cerrado de valores con nombre. En vez de escribir
`1`, `-1` y `0` en todas partes (y equivocarse alguna vez), se definen nombres:

<!-- fmt: off -->
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
<!-- fmt: on -->

- `IntEnum` hace que `Signal.LONG` **sea** también el entero `1`, así que se puede comparar y
  operar con números.
- `StrEnum` hace que `Category.TREND` **sea** también el texto `"trend"`.

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.strategies.base import Category, Signal

print(Signal.LONG == 1, Signal.SHORT + Signal.LONG, Signal(-1).name)
print(Category.TREND == "trend", [c.value for c in Category])
```
*Salida real:*

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

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 37–42

```python
class HTTPSession(Protocol):
    """Interfaz mínima de sesión HTTP (permite inyectar dobles de prueba)."""

    def get(self, url: str, params: dict[str, Any], timeout: float) -> Any:
        """Realiza una petición GET."""
        ...
```
<!-- fmt: on -->

El cliente acepta como sesión HTTP **cualquier** objeto con un método `get(url, params,
timeout)`. En producción es una `requests.Session`; en las pruebas es una clase falsa que
devuelve respuestas inventadas sin usar la red (Módulo IV, sección 4.12). Esta técnica se
llama **inyección de dependencias** y es la razón de que el cliente pueda probarse sin conexión.

*Ejemplo ejecutable:*

```python
def doble(x: int) -> int:
    return x * 2


print(
    doble(3), doble("ab")
)  # Python no impide pasar un texto: las anotaciones no se comprueban al ejecutar
```
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

- `BaseModel` es la clase base de Pydantic.
- `extra="forbid"`: un parámetro desconocido (por ejemplo, una errata) es un error.
- `frozen=True`: los parámetros no se pueden modificar tras crearlos.
- `Field(14, ge=2, le=500)`: valor por defecto 14, mayor o igual que 2 (`ge`) y menor o igual que
  500 (`le`). `gt` y `lt` son "estrictamente mayor/menor".

Las reglas que relacionan varios campos se escriben con `@model_validator`. La configuración
global impide, por ejemplo, un apalancamiento superior al máximo de riesgo:

<!-- fmt: off -->
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
<!-- fmt: on -->

*Ejemplo ejecutable:*

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
*Salida real:*

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

<!-- fmt: off -->
`src/bybit_quant_lab/validation/experiment_log.py` · líneas 24–28

```python
    def append(self, record: dict[str, Any]) -> None:
        """Añade un registro con marca temporal UTC."""
        rec = {"logged_at": datetime.now(UTC).isoformat(), **record}
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, default=str, sort_keys=True) + "\n")
```
<!-- fmt: on -->

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

<!-- fmt: off -->
`src/bybit_quant_lab/data/downloader.py` · líneas 55–57

```python
    for a, b in itertools.pairwise(idx):
        if b - a > delta:
            ranges.append((a + delta, b))
```
<!-- fmt: on -->

*Ejemplo ejecutable:*

```python
import itertools

horas = [0, 1, 2, 5, 6]
for a, b in itertools.pairwise(horas):
    if b - a > 1:
        print(f"hueco entre la hora {a} y la hora {b}: faltan {b - a - 1} velas")
```
*Salida real:*

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

*Ejemplo ejecutable:*

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
*Salida real:*

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

**Respuesta:**

Está en `validate_timeframe` y se dispara cuando la temporalidad pedida no es una clave del
diccionario `TIMEFRAMES`. Lanza `ValueError` (valor inválido) con un mensaje que incluye el valor
recibido entre comillas (`!r`) y la lista de temporalidades permitidas.

<div style="page-break-before: always;"></div>

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

**Respuesta:**

`execution/costs.py` ya sabe calcular comisiones maker (`fee(..., taker=False)`), pero el motor
(`backtesting/engine.py`) siempre pide la comisión taker porque solo simula órdenes a mercado.
Habría que cambiar el motor para que distinga el tipo de orden. Las estrategias no se tocarían.

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

*Ejemplo ejecutable:*

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
*Salida real:*

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

**Respuesta:**

Con la opción global de la CLI, antes de la orden: `bql --output-dir /tmp/pruebas backtest ...`.
`_load_cfg` la convierte en un valor a sobrescribir antes de validar la configuración.

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

*Ejemplo ejecutable:*

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
*Salida real:*

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
`src/bybit_quant_lab/data/storage.py` · líneas 28–31

```python
def data_hash(df: pd.DataFrame) -> str:
    """SHA-256 determinista del contenido (índice + valores) de un DataFrame."""
    hashed = pd.util.hash_pandas_object(df, index=True).to_numpy()
    return hashlib.sha256(hashed.tobytes()).hexdigest()
```
<!-- fmt: on -->

<!-- fmt: off -->
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

*Ejemplo ejecutable:*

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
*Salida real:*

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

**Respuesta:**

Rompería la separación de responsabilidades: el riesgo dejaría de estar centralizado en `risk/`.
En la práctica, los límites del sistema (riesgo por operación, exposición, margen) podrían
aplicarse de forma distinta en cada estrategia, y una combinación de estrategias no sabría qué
tamaño usar. Además, cambiar la política de riesgo exigiría modificar diez archivos.

<div style="page-break-before: always;"></div>

# Módulo IV. Conectividad con Bybit e ingeniería de datos

Un backtest no puede ser mejor que sus datos. Este módulo sigue el camino de una vela desde la
API de Bybit hasta una tabla limpia en disco, con el código real del cliente
(`data/bybit_client.py`), el descargador (`data/downloader.py`), la validación
(`data/validation.py`) y el almacenamiento (`data/storage.py`).

> **[Pendiente] Advertencia que recorre todo el módulo.** El entorno donde se escribió el código
> no tenía acceso a `api.bybit.com` (el proxy de red rechazaba la conexión). Todo lo que se
> describe aquí se ha comprobado con **respuestas simuladas** que imitan el formato documentado
> de Bybit, **no** con la API real. La sección 4.19 separa con precisión lo comprobado de lo
> supuesto.

---

## 4.1 Cómo funciona una petición HTTP

### La idea

Pedir datos a una API es como pedir algo en un mostrador con un formulario:

1. Rellenas un **formulario** (la petición): a qué ventanilla vas (la URL), qué tipo de trámite
   es (el **método**, por ejemplo GET para consultar) y los datos concretos (los **parámetros**).
2. El empleado te devuelve una **respuesta** con un **código de estado** ("hecho", "no
   encontrado", "vuelva más tarde") y, si todo fue bien, el **cuerpo** con lo que pediste.

Partes técnicas de una petición y una respuesta HTTP:

| Parte | Ejemplo | Significado |
|---|---|---|
| Método | `GET` | Leer, sin modificar nada en el servidor |
| URL | `https://api.bybit.com/v5/market/kline?...` | Dirección del recurso |
| Cabeceras (headers) | `Content-Type: application/json` | Metadatos de la petición o respuesta |
| Código de estado | `200` | `2xx` éxito, `4xx` error del cliente, `5xx` error del servidor |
| Cuerpo (body) | `{"retCode": 0, ...}` | El contenido (aquí, JSON) |

En Python, el proyecto usa la biblioteca `requests`. Su objeto `Session` reutiliza la conexión
entre peticiones, lo que es más rápido cuando se hacen muchas seguidas.

---

## 4.2 Cómo se construye una URL con parámetros

Una URL se compone de:

```text
https://api.bybit.com/v5/market/kline?category=linear&symbol=BTCUSDT&interval=60
└─┬──┘ └─────┬──────┘└──────┬──────┘ └──────────────────┬────────────────────┘
esquema   dominio        ruta (endpoint)          cadena de consulta (query string)
```

La **cadena de consulta** empieza con `?` y separa los parámetros con `&`. El cliente nunca
construye este texto a mano: pasa un diccionario a `requests` y la biblioteca lo codifica. Este
ejemplo prepara la petición **sin enviarla**, para ver la URL resultante:

*Ejemplo ejecutable:*

```python
import requests

parametros = {
    "category": "linear",
    "symbol": "BTCUSDT",
    "interval": "60",
    "start": 1704067200000,
    "end": 1707667199999,
    "limit": 1000,
}
peticion = requests.Request(
    "GET", "https://api.bybit.com/v5/market/kline", params=parametros
).prepare()
print(peticion.method)
print(peticion.url)
```
*Salida real:*

```text
GET
https://api.bybit.com/v5/market/kline?category=linear&symbol=BTCUSDT&interval=60&start=1704067200000&end=1707667199999&limit=1000
```

---

## 4.3 El endpoint de velas y sus parámetros

El cliente construye exactamente estos parámetros para cada petición de velas:

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 157–165

```python
            params = {
                "category": category,
                "symbol": symbol.upper(),
                "interval": bybit_interval(timeframe),
                "start": _to_ms(cursor),
                "end": _to_ms(window_end) - 1,
                "limit": limit,
            }
            result = self.get("/v5/market/kline", params)
```
<!-- fmt: on -->

| Parámetro | Valor | Significado | Estado |
|---|---|---|---|
| `category` | `"linear"` | Tipo de producto: perpetuos/futuros lineales liquidados en USDT | **[Hecho]** fijado en el código y en `DataConfig` |
| `symbol` | `"BTCUSDT"` | Instrumento; se pasa a mayúsculas | **[Hecho]** |
| `interval` | `"5"`, `"15"`, `"60"`, `"240"`... | Duración de la vela en minutos (`"D"` para un día) | **[Hecho]** traducido por `bybit_interval` |
| `start` | milisegundos Unix | Apertura de la primera vela pedida | **[Hecho]** |
| `end` | milisegundos Unix | Límite final; el cliente envía "fin de la ventana − 1 ms" | **[Supuesto]** que Bybit trate `end` como inclusivo sobre la hora de apertura |
| `limit` | `1000` | Máximo de velas por respuesta (1000 es el máximo documentado) | **[Supuesto]** límite según la documentación pública |

---

## 4.4 Milisegundos Unix, fechas UTC y zonas horarias

### La idea

Los ordenadores suelen guardar el tiempo como un **número**: el tiempo transcurrido desde el
1 de enero de 1970 a las 00:00 UTC (la "época Unix"). Bybit usa **milisegundos** desde esa fecha.
`1704067200000` ms son 1.704.067.200 segundos, que corresponden al 1 de enero de 2024, 00:00 UTC.

Una **zona horaria** es una regla para convertir ese instante en la hora "de reloj" de un lugar.
El mismo instante es 00:00 en UTC y 21:00 del día anterior en Buenos Aires (UTC−3). Mezclar
zonas horarias es una fuente clásica de errores de un día o de horas en los datos.

**[Diseño]** El proyecto trabaja **siempre en UTC**: el cliente convierte los milisegundos a
fechas UTC, la validación convierte cualquier índice a UTC y el almacenamiento lo conserva.

Conversión de fecha a milisegundos en el cliente:

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 45–50

```python
def _to_ms(ts: pd.Timestamp) -> int:
    return (
        int(ts.tz_convert("UTC").timestamp() * 1000)
        if ts.tzinfo
        else int(ts.tz_localize("UTC").timestamp() * 1000)
    )
```
<!-- fmt: on -->

Si la fecha no tiene zona (`tzinfo` vacío), se **supone** UTC (`tz_localize("UTC")`); si la
tiene, se **convierte** a UTC (`tz_convert("UTC")`). Son operaciones distintas: localizar
declara en qué zona estaba expresada una hora; convertir cambia la hora de reloj sin cambiar el
instante.

Alineación de fechas al borde de una vela:

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 238–240

```python
def _align(ts: pd.Timestamp, delta: pd.Timedelta, ceil: bool) -> pd.Timestamp:
    ts = ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")
    return ts.ceil(delta) if ceil else ts.floor(delta)
```
<!-- fmt: on -->

`ceil` redondea hacia arriba al múltiplo de la duración de vela y `floor` hacia abajo.

*Ejemplo ejecutable:*

```python
import pandas as pd

ms = 1704067200000
instante = pd.to_datetime(ms, unit="ms", utc=True)
print(instante)
print(instante.tz_convert("America/Argentina/Buenos_Aires"))
print(int(instante.timestamp() * 1000) == ms)
hora = pd.Timestamp("2024-01-01 00:30", tz="UTC")
print(hora.ceil(pd.Timedelta("1h")), hora.floor(pd.Timedelta("1h")))
```
*Salida real:*

```text
2024-01-01 00:00:00+00:00
2023-12-31 21:00:00-03:00
True
2024-01-01 01:00:00+00:00 2024-01-01 00:00:00+00:00
```

### Comprobación

Si pides velas de 1h desde las 00:30, ¿cuál será la primera vela descargada y por qué?

**Respuesta:**

La de las 01:00. `fetch_klines` alinea el inicio con `ceil` (redondeo hacia arriba), porque la
vela de las 00:00 empezó antes del inicio pedido. Lo verifica la prueba
`test_unaligned_start_is_rounded_up_to_bar_boundary` (`tests/unit/test_audit_data.py`).

---

## 4.5 La respuesta JSON y sus dos niveles de error

### La idea

Según la documentación de Bybit V5, una respuesta de velas tiene esta forma (los valores son de
ejemplo; **[Supuesto]** no se han comparado con una respuesta real en este entorno):

```json
{
  "retCode": 0,
  "retMsg": "OK",
  "result": {
    "category": "linear",
    "symbol": "BTCUSDT",
    "list": [
      ["1704070800000", "42350.5", "42400", "42300.1", "42380", "120.5", "5104371.25"],
      ["1704067200000", "42300", "42360", "42250", "42350.5", "98.2", "4155230.10"]
    ]
  },
  "time": 1704074400000
}
```

Observa tres detalles que el código tiene que resolver:

1. **Todo son textos**, incluidos los precios (`"42350.5"`). Hay que convertirlos a números.
2. La lista está en orden **descendente** (la vela más reciente primero).
3. Cada vela es una lista de 7 elementos sin nombres: `[apertura_ms, open, high, low, close,
   volume, turnover]`. El orden de los campos es un **[Supuesto]** basado en la documentación.

Hay **dos niveles de error**:

- **HTTP:** el código de estado (`200`, `429`, `503`...). Indica si la conversación con el
  servidor funcionó.
- **API:** el campo `retCode` dentro del JSON. Bybit puede responder `200` (la conversación fue
  bien) con `retCode` distinto de 0 (la petición no se pudo atender: símbolo inexistente, demasiadas
  peticiones...).

### El método `get`, línea por línea

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 85–131

```python
    def get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        """GET con reintentos. Devuelve ``result`` de la respuesta o lanza ``BybitAPIError``."""
        url = f"{self.base_url}{path}"
        last_error = "sin intentos"
        for attempt in range(self.max_retries + 1):
            if attempt:
                wait = self.backoff_seconds * (2 ** (attempt - 1))
                logger.warning(
                    "reintento %d/%d en %.1fs: %s", attempt, self.max_retries, wait, last_error
                )
                self._sleep(wait)
            self._throttle()
            self.request_count += 1
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout_seconds)
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_error = f"error de red: {exc}"
                continue
            status = int(getattr(resp, "status_code", 0))
            if status == 403:
                raise BybitAPIError(
                    "HTTP 403: acceso denegado o IP limitada por frecuencia. Bybit recomienda "
                    "detener las peticiones y esperar al menos 10 minutos."
                )
            if status in RETRYABLE_HTTP:
                last_error = f"HTTP {status}"
                continue
            if status != 200:
                raise BybitAPIError(f"HTTP {status} no recuperable en {path}")
            try:
                payload = resp.json()
            except ValueError:
                last_error = "respuesta no JSON"
                continue
            if not isinstance(payload, dict) or "retCode" not in payload:
                raise BybitAPIError(f"Respuesta con formato inesperado: {str(payload)[:200]}")
            code = int(payload["retCode"])
            if code in RETRYABLE_RET_CODES:
                last_error = f"retCode {code}: {payload.get('retMsg')}"
                continue
            if code != 0:
                raise BybitAPIError(f"retCode {code}: {payload.get('retMsg')}")
            result = payload.get("result")
            if not isinstance(result, dict):
                raise BybitAPIError("Respuesta sin campo 'result' válido")
            return result
        raise BybitAPIError(f"Reintentos agotados en {path}: {last_error}")
```
<!-- fmt: on -->

- **87:** construye la URL completa uniendo la base y la ruta.
- **89:** bucle de intentos: el primero más `max_retries` reintentos (5 por defecto, 6 intentos en
  total).
- **90–95:** antes de cada reintento espera `backoff_seconds · 2^(intento−1)` segundos
  (sección 4.6).
- **96:** respeta un intervalo mínimo entre peticiones.
- **98–102:** errores de red (conexión rechazada, tiempo agotado): se reintenta.
- **104–108:** **HTTP 403** (prohibido) no se reintenta. Según la documentación de Bybit, un 403
  puede indicar que la IP fue limitada por exceso de peticiones, y reintentar lo empeoraría.
- **109–111:** 429 (demasiadas peticiones) y errores 5xx del servidor: se reintenta.
- **112–113:** cualquier otro código distinto de 200: error definitivo.
- **114–118:** si el cuerpo no es JSON válido, se reintenta (puede ser una respuesta cortada).
- **119–120:** si el JSON no tiene `retCode`, la respuesta no tiene la forma esperada: error
  definitivo.
- **121–126:** `retCode` transitorios (10000, 10006, 10016: timeout, exceso de peticiones,
  error interno) se reintentan; cualquier otro distinto de 0 es un error definitivo con el
  mensaje de Bybit.
- **127–130:** devuelve solo la parte `result`.
- **131:** si se agotan los intentos, error con el último motivo.

### Comprobación

Bybit responde HTTP 200 con `{"retCode": 10001, "retMsg": "params error"}`. ¿Qué hace el cliente?

**Respuesta:**

El HTTP 200 pasa las comprobaciones de estado, el JSON tiene `retCode`, y 10001 no está en
`RETRYABLE_RET_CODES`, así que lanza `BybitAPIError("retCode 10001: params error")` sin
reintentar. Lo verifica `test_non_retryable_and_exhausted_errors` en `tests/unit/test_data.py`.

---

## 4.6 Timeouts, reintentos, backoff y límites de peticiones

### La idea

- **Timeout:** tiempo máximo que se espera una respuesta (15 s por defecto). Sin él, una
  conexión colgada bloquearía el programa para siempre.
- **Reintento:** volver a intentar tras un error transitorio.
- **Backoff exponencial:** esperar cada vez más entre reintentos (1, 2, 4, 8, 16 s...), para no
  saturar a un servidor que ya tiene problemas.
- **Límite de peticiones (rate limit):** máximo de peticiones permitidas por unidad de tiempo.
  La documentación de Bybit V5 indica 600 peticiones cada 5 segundos por IP.

El intervalo mínimo entre peticiones se impone así:

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 79–83

```python
    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.min_request_interval:
            self._sleep(self.min_request_interval - elapsed)
        self._last_request = time.monotonic()
```
<!-- fmt: on -->

Con `min_request_interval = 0.05` s, el cliente hace como máximo 20 peticiones por segundo, es
decir, 100 cada 5 segundos: una sexta parte del límite documentado.

Este ejemplo usa una **sesión simulada** que falla tres veces y luego responde bien, y una
función de espera falsa que, en lugar de dormir, anota cuánto habría esperado:

*Ejemplo ejecutable:*

```python
import requests

from bybit_quant_lab.data.bybit_client import BybitPublicClient


class Respuesta:
    def __init__(self, estado, cuerpo):
        self.status_code, self._cuerpo = estado, cuerpo

    def json(self):
        return self._cuerpo


class SesionSimulada:
    """No usa la red: devuelve respuestas preparadas en orden."""

    def __init__(self):
        self.guion = [
            requests.ConnectionError("red caída"),
            Respuesta(503, {}),
            Respuesta(200, {"retCode": 10006, "retMsg": "Too many visits"}),
            Respuesta(200, {"retCode": 0, "result": {"list": []}}),
        ]

    def get(self, url, params, timeout):
        paso = self.guion.pop(0)
        if isinstance(paso, Exception):
            raise paso
        return paso


esperas = []
cliente = BybitPublicClient(
    session=SesionSimulada(), sleep=esperas.append, backoff_seconds=1.0, min_request_interval=0
)
print(cliente.get("/v5/market/kline", {}))
print("esperas de backoff:", esperas, "| peticiones:", cliente.request_count)
```
*Salida real:*

```text
{'list': []}
esperas de backoff: [1.0, 2.0, 4.0] | peticiones: 4
```

Tres fallos transitorios provocan esperas de 1, 2 y 4 segundos; el cuarto intento tiene éxito.

---

## 4.7 Paginación: reconstruir años de datos con muchas peticiones

### La idea

Cada petición devuelve como máximo 1000 velas. Tres años de velas de 1 hora son unas
3 × 365 × 24 = 26.280 velas (26.304 si el período incluye un 29 de febrero, como en el ejemplo de
abajo): hacen falta muchas peticiones. **Paginar** es pedir los datos por
trozos y unirlos.

Hay dos formas habituales de paginar:

1. **Por cursor:** pedir "las 1000 velas anteriores a X" y usar la más antigua recibida como
   nuevo X. Depende de en qué orden y qué subconjunto devuelve la API.
2. **Por ventanas fijas:** dividir el tiempo en tramos que contengan como mucho 1000 velas y
   pedir cada tramo con `start` y `end`.

**[Diseño]** El cliente usa ventanas fijas: cada ventana dura exactamente `1000 × duración de
vela`, así que nunca puede contener más de 1000 velas, y el resultado **no depende del orden** en
que Bybit devuelva la lista.

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 134–174

```python
    def fetch_klines(
        self,
        symbol: str,
        timeframe: str,
        start: pd.Timestamp,
        end: pd.Timestamp,
        limit: int = 1000,
        category: str = "linear",
    ) -> pd.DataFrame:
        """Descarga velas cerradas en ``[start, end)`` paginando por ventanas de ``limit`` velas.

        Se usan ventanas fijas de tamaño ``limit * timeframe`` para que cada petición contenga
        como máximo ``limit`` velas, sin depender del orden en que la API devuelve la lista.
        La vela en curso (no cerrada) se descarta.
        """
        delta = timeframe_delta(timeframe)
        start = _align(start, delta, ceil=True)
        now = self._clock()
        end = min(end, _align(now, delta, ceil=False))
        frames: list[pd.DataFrame] = []
        cursor = start
        while cursor < end:
            window_end = min(cursor + delta * limit, end)
            params = {
                "category": category,
                "symbol": symbol.upper(),
                "interval": bybit_interval(timeframe),
                "start": _to_ms(cursor),
                "end": _to_ms(window_end) - 1,
                "limit": limit,
            }
            result = self.get("/v5/market/kline", params)
            frames.append(_parse_klines(result))
            cursor = window_end
        if not frames:
            return _empty_klines()
        df = pd.concat(frames)
        df = df[~df.index.duplicated(keep="last")].sort_index()
        df = df[(df.index >= start) & (df.index < end)]
        closed = df.index + delta <= now
        return df[closed]
```
<!-- fmt: on -->

- **149:** duración de una vela (`Timedelta`).
- **150:** alinea el inicio hacia arriba (sección 4.4).
- **151–152:** el final nunca supera el último borde de vela anterior a "ahora".
- **155–167:** bucle de ventanas: `window_end = cursor + 1000 velas` (o el final, si llega
  antes). Se pide `[cursor, window_end − 1 ms]` y se avanza `cursor = window_end`. Las ventanas
  son contiguas y no se solapan.
- **170–171:** une todas las ventanas, elimina horas repetidas (se queda con la última
  aparición) y **ordena cronológicamente**.
- **172:** recorta exactamente al rango pedido `[start, end)` (inicio incluido, fin excluido).
- **173–174:** descarta la vela que todavía no ha cerrado (sección 4.8).

*Ejemplo ejecutable:*

```python
import math

import pandas as pd

inicio, fin = pd.Timestamp("2022-01-01", tz="UTC"), pd.Timestamp("2025-01-01", tz="UTC")
for tf, minutos in (("5m", 5), ("1h", 60), ("4h", 240)):
    velas = int((fin - inicio) / pd.Timedelta(minutes=minutos))
    print(f"{tf}: {velas} velas -> {math.ceil(velas / 1000)} peticiones")
```
*Salida real:*

```text
5m: 315648 velas -> 316 peticiones
1h: 26304 velas -> 27 peticiones
4h: 6576 velas -> 7 peticiones
```

Con una petición cada 0,05 s, incluso los tres años de velas de 5 minutos se descargan en pocos
segundos de espera entre peticiones (más el tiempo de respuesta de la red, que no se puede
estimar sin conexión).

### Comprobación

Pides 2.500 velas de 1h. ¿Cuántas peticiones hace `fetch_klines` y de cuántas velas cada una?

**Respuesta:**

Tres: 1000, 1000 y 500. Lo comprueba `test_fetch_klines_paginates_and_sorts`
(`tests/unit/test_data.py`, línea 101).

---

## 4.8 Orden cronológico, duplicados y velas abiertas

- **Orden:** todo el sistema asume que las filas están ordenadas de la más antigua a la más
  reciente. Las ventanas móviles y los desplazamientos (Módulo V) darían resultados falsos con
  datos desordenados. Por eso se ordena **siempre** (línea 171), sin fiarse del orden de la API.
- **Duplicados:** si dos ventanas o dos descargas traen la misma vela, se conserva una sola
  (`keep="last"`, la más reciente descargada).
- **Vela abierta:** la vela actual todavía no ha terminado: su máximo, mínimo, cierre y volumen
  seguirán cambiando. Si se guardara, el dataset contendría una vela "a medias" que no coincide
  con la definitiva. La línea 173 conserva solo las velas cuyo final (`apertura + duración`)
  ya pasó.

*Ejemplo ejecutable:*

```python
import pandas as pd

ahora = pd.Timestamp("2024-01-01 05:30", tz="UTC")
aperturas = pd.date_range("2024-01-01 03:00", periods=3, freq="1h", tz="UTC")
cerradas = aperturas + pd.Timedelta("1h") <= ahora
for apertura, cerrada in zip(aperturas, cerradas):
    print(apertura.strftime("%H:%M"), "cerrada" if cerrada else "ABIERTA (se descarta)")
```
*Salida real:*

```text
03:00 cerrada
04:00 cerrada
05:00 ABIERTA (se descarta)
```

---

## 4.9 Normalización: de lista de textos a tabla tipada

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 249–269

```python
def _parse_klines(result: dict[str, Any]) -> pd.DataFrame:
    """Convierte ``result.list`` (``[startTime, o, h, l, c, volume, turnover]``) en DataFrame."""
    items = result.get("list")
    if not isinstance(items, list):
        raise BybitAPIError("Campo 'list' de velas ausente o inválido")
    if not items:
        return _empty_klines()
    bad = [row for row in items if not isinstance(row, list | tuple) or len(row) < 7]
    if bad:
        raise BybitAPIError(f"Vela con formato inválido: {bad[0]}")
    df = pd.DataFrame(
        [row[:7] for row in items],
        columns=["open_time", "open", "high", "low", "close", "volume", "turnover"],
    )
    df["open_time"] = pd.to_datetime(
        pd.to_numeric(df["open_time"], errors="coerce"), unit="ms", utc=True
    )
    if df["open_time"].isna().any():
        raise BybitAPIError("Marca de tiempo de vela no numérica")
    df = df.set_index("open_time")
    return df.apply(pd.to_numeric, errors="coerce").astype("float64")
```
<!-- fmt: on -->

- **251–255:** `list` debe existir y ser una lista; una lista vacía es válida (no hay velas en
  ese tramo).
- **256–258:** cada vela debe tener al menos 7 elementos; si no, la respuesta no tiene la forma
  esperada.
- **259–262:** crea la tabla poniendo nombre a cada posición.
- **263–267:** convierte la apertura de milisegundos a fecha UTC. `errors="coerce"` convierte lo
  que no sea un número en "vacío" (`NaT`), y si aparece alguno se lanza un error.
- **268:** la fecha pasa a ser el **índice** de la tabla (Módulo V).
- **269:** convierte los precios y volúmenes de texto a `float64`. Un valor no numérico se
  convierte en `NaN` (vacío) en vez de detener el programa; la limpieza posterior descarta esas
  filas y lo anota en el informe de calidad.

---

## 4.10 Ejemplo completo: de una respuesta JSON a una tabla para las estrategias

Este ejemplo simula la API con el formato de la sección 4.5 (textos, orden descendente, 7 campos)
y recorre el flujo real del proyecto: descargar, limpiar, guardar en Parquet, volver a cargar y
pasar los datos a una estrategia. **No usa la red.** Los precios son inventados.

*Ejemplo ejecutable:*

```python
import tempfile
from pathlib import Path

import pandas as pd

from bybit_quant_lab.data.bybit_client import BybitPublicClient
from bybit_quant_lab.data.downloader import download_ohlcv
from bybit_quant_lab.data.storage import dataset_path, load_dataset, load_metadata
from bybit_quant_lab.strategies import create_strategy


class Respuesta:
    def __init__(self, cuerpo):
        self.status_code, self._cuerpo = 200, cuerpo

    def json(self):
        return self._cuerpo


class BybitSimulado:
    """Imita /v5/market/kline: textos, 7 campos, lista de la más reciente a la más antigua."""

    def __init__(self):
        self.peticiones = []

    def get(self, url, params, timeout):
        self.peticiones.append(params)
        paso = int(params["interval"]) * 60_000
        filas, t = [], params["start"]
        while t <= params["end"] and len(filas) < params["limit"]:
            p = 42000 + (t // paso) % 40
            filas.append(
                [str(t), f"{p}", f"{p + 15}", f"{p - 12}", f"{p + 5}", "3.5", f"{3.5 * p:.2f}"]
            )
            t += paso
        return Respuesta(
            {
                "retCode": 0,
                "retMsg": "OK",
                "result": {"category": "linear", "symbol": params["symbol"], "list": filas[::-1]},
            }
        )


carpeta = Path(tempfile.mkdtemp())
api = BybitSimulado()
cliente = BybitPublicClient(
    session=api, min_request_interval=0, clock=lambda: pd.Timestamp("2026-01-01", tz="UTC")
)
resumen = download_ohlcv(
    cliente,
    "BTCUSDT",
    "1h",
    pd.Timestamp("2024-01-01", tz="UTC"),
    pd.Timestamp("2024-03-01", tz="UTC"),
    carpeta,
)
print("peticiones:", resumen.requests, "| velas:", resumen.rows)
tabla = load_dataset(dataset_path(carpeta, "BTCUSDT", "1h"))
print(tabla.head(3).to_string())
print("tipos:", sorted(set(map(str, tabla.dtypes))), "| índice:", tabla.index.dtype)
print(
    "ordenada:",
    tabla.index.is_monotonic_increasing,
    "| duplicados:",
    int(tabla.index.duplicated().sum()),
)
print(
    "calidad válida:", load_metadata(dataset_path(carpeta, "BTCUSDT", "1h"))["quality"]["is_valid"]
)
senales = create_strategy("donchian_breakout").generate_signals(tabla)
print("señales con el mismo índice:", senales.index.equals(tabla.index))
```
*Salida real:*

```text
peticiones: 2 | velas: 1440
                              open     high      low    close  volume  turnover
open_time                                                                      
2024-01-01 00:00:00+00:00  42032.0  42047.0  42020.0  42037.0     3.5  147112.0
2024-01-01 01:00:00+00:00  42033.0  42048.0  42021.0  42038.0     3.5  147115.5
2024-01-01 02:00:00+00:00  42034.0  42049.0  42022.0  42039.0     3.5  147119.0
tipos: ['float64'] | índice: datetime64[ms, UTC]
ordenada: True | duplicados: 0
calidad válida: True
señales con el mismo índice: True
```

El resultado son 1.440 velas (60 días × 24 horas) en 2 peticiones, ordenadas, sin duplicados,
con números de tipo `float64`, listas para cualquier estrategia.

---

## 4.11 Validación de OHLCV

### La idea

Antes de usar datos hay que comprobar que tienen sentido. El informe de calidad cuenta cada tipo
de problema:

<!-- fmt: off -->
`src/bybit_quant_lab/data/validation.py` · líneas 20–50

```python
@dataclass
class DataQualityReport:
    """Resultado de la validación de una serie OHLCV."""

    rows: int = 0
    start: str | None = None
    end: str | None = None
    duplicates: int = 0
    unsorted: bool = False
    non_numeric: int = 0
    nan_rows: int = 0
    invalid_candles: int = 0
    negative_volume: int = 0
    gaps: int = 0
    missing_bars: int = 0
    gap_ranges: list[tuple[str, str]] = field(default_factory=list)
    misaligned: int = 0
    issues: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Válida si no hay errores estructurales (los huecos se toleran y se reportan)."""
        return not (
            self.duplicates
            or self.unsorted
            or self.non_numeric
            or self.nan_rows
            or self.invalid_candles
            or self.negative_volume
            or self.misaligned
        )
```
<!-- fmt: on -->

`is_valid` es `True` solo si no hay **errores estructurales**. **[Diseño]** Los huecos
(`gaps`) **no** invalidan los datos: se informan, porque pueden ser interrupciones reales del
exchange y no hay forma honesta de rellenarlos.

Las comprobaciones de cada vela:

<!-- fmt: off -->
`src/bybit_quant_lab/data/validation.py` · líneas 86–94

```python
    o, h, low, c, v = (numeric[k] for k in REQUIRED)
    bad = (h < low) | (h < o) | (h < c) | (low > o) | (low > c) | (o <= 0) | (c <= 0) | (low <= 0)
    rep.invalid_candles = int(bad.fillna(False).sum())
    rep.negative_volume = int((v < 0).fillna(False).sum())
    delta = timeframe_delta(timeframe)
    epoch = pd.Timestamp("1970-01-01", tz="UTC")
    dt_index = pd.DatetimeIndex(df.index)
    offsets = (dt_index - epoch).to_numpy() % delta.to_timedelta64()
    rep.misaligned = int((offsets != np.timedelta64(0, "ns")).sum())
```
<!-- fmt: on -->

- **87:** una vela es inválida si el máximo es menor que el mínimo, la apertura o el cierre; si
  el mínimo es mayor que la apertura o el cierre; o si algún precio es cero o negativo.
- **93–94:** una marca de tiempo está **desalineada** si no cae en un borde exacto de vela desde
  la época Unix (por ejemplo, una vela de 1h a las 10:07).

La limpieza normaliza, ordena, elimina duplicados y descarta filas inválidas, y **después**
vuelve a validar:

<!-- fmt: off -->
`src/bybit_quant_lab/data/validation.py` · líneas 115–139

```python
def clean_ohlcv(df: pd.DataFrame, timeframe: str) -> tuple[pd.DataFrame, DataQualityReport]:
    """Normaliza a UTC, ordena, elimina duplicados (conserva el último) y filas inválidas.

    Devuelve la serie limpia y el informe de calidad **posterior** a la limpieza. Las filas
    descartadas se registran en ``issues``. Los huecos no se rellenan.
    """
    out = _ensure_utc_index(df.copy())
    cols = [c for c in (*REQUIRED, "turnover") if c in out.columns]
    out = out[cols].apply(pd.to_numeric, errors="coerce").astype("float64")
    before = len(out)
    out = out[~out.index.duplicated(keep="last")].sort_index()
    o, h, low, c = out["open"], out["high"], out["low"], out["close"]
    valid = (
        out[list(REQUIRED)].notna().all(axis=1)
        & (h >= np.maximum(o, c))
        & (low <= np.minimum(o, c))
        & (low > 0)
        & (out["volume"] >= 0)
    )
    out = out[valid]
    rep = validate_ohlcv(out, timeframe)
    dropped = before - len(out)
    if dropped:
        rep.issues.insert(0, f"limpieza: {dropped} filas descartadas (duplicadas o inválidas)")
    return out, rep
```
<!-- fmt: on -->

*Ejemplo ejecutable:*

```python
import numpy as np
import pandas as pd

from bybit_quant_lab.data.validation import clean_ohlcv, validate_ohlcv

idx = pd.date_range("2024-01-01", periods=6, freq="1h", tz="UTC")
velas = pd.DataFrame(
    {
        "open": [100, 101, 102, 103, 104, 105.0],
        "high": [101, 102, 103, 104, 105, 106.0],
        "low": [99, 100, 101, 102, 103, 104.0],
        "close": [101, 102, 103, 104, 105, 105.5],
        "volume": [10, 11, 12, 13, 14, 15.0],
    },
    index=idx,
)
velas.iloc[2, velas.columns.get_loc("high")] = 90.0  # máximo imposible
velas.iloc[4, velas.columns.get_loc("close")] = np.nan  # dato ausente
velas = velas.drop(idx[3])  # una vela que falta
informe = validate_ohlcv(velas, "1h")
print("válido:", informe.is_valid, "| problemas:", informe.issues)
limpia, informe_limpio = clean_ohlcv(velas, "1h")
print("filas:", len(velas), "->", len(limpia), "| válido tras limpiar:", informe_limpio.is_valid)
print("huecos:", informe_limpio.gaps, "| velas faltantes:", informe_limpio.missing_bars)
```
*Salida real:*

```text
válido: False | problemas: ['1 huecos (1 velas faltantes)', 'nan_rows=1', 'invalid_candles=1']
filas: 5 -> 3 | válido tras limpiar: True
huecos: 1 | velas faltantes: 3
```

Tras limpiar quedan 3 velas válidas. Los datos son "válidos", pero ahora tienen huecos: las
velas eliminadas y la que faltaba. La limpieza **no inventa** las velas que faltan.

---

## 4.12 Datos faltantes y huecos temporales

**[Limitación]** Un hueco es tolerado y solo informado. Las consecuencias para el resto del
sistema son importantes (se explican en el Módulo V, sección 5.12):

- Los indicadores cuentan **filas**, no tiempo. Una media de "20 velas" que atraviesa un hueco de
  10 horas abarca 30 horas reales.
- El motor mantiene la posición abierta a través del hueco. El primer precio tras el hueco se
  trata como cualquier apertura (puede producir un gap de ejecución, Módulo X).

`bql validate-data` muestra los huecos y sus rangos (`gap_ranges`). Revísalos antes de
interpretar cualquier resultado; la auditoría lo registra como limitación M-06.

---

## 4.13 Descargas incrementales y caché

### La idea

Volver a descargar años de datos cada vez sería lento y gastaría peticiones. Una **descarga
incremental** solo pide lo que falta. Los datos ya guardados actúan como **caché**: una copia
local que evita repetir el trabajo.

Cálculo de los tramos que faltan:

<!-- fmt: off -->
`src/bybit_quant_lab/data/downloader.py` · líneas 38–60

```python
def missing_ranges(
    existing: pd.DatetimeIndex, start: pd.Timestamp, end: pd.Timestamp, timeframe: str
) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """Calcula los rangos ``[a, b)`` de ``[start, end)`` no cubiertos por ``existing``.

    Incluye cabecera, cola y huecos internos. Un hueco interno puede corresponder a una
    interrupción real del exchange; en ese caso volver a pedirlo simplemente no devuelve datos.
    """
    delta = timeframe_delta(timeframe)
    if len(existing) == 0:
        return [(start, end)] if start < end else []
    idx = existing[(existing >= start) & (existing < end)].sort_values()
    if len(idx) == 0:
        return [(start, end)]
    ranges: list[tuple[pd.Timestamp, pd.Timestamp]] = []
    if idx[0] > start:
        ranges.append((start, idx[0]))
    for a, b in itertools.pairwise(idx):
        if b - a > delta:
            ranges.append((a + delta, b))
    if idx[-1] + delta < end:
        ranges.append((idx[-1] + delta, end))
    return ranges
```
<!-- fmt: on -->

Tres tipos de tramo pendiente: la **cabecera** (antes de la primera vela guardada), los **huecos
internos** y la **cola** (después de la última vela guardada).

El proceso completo:

<!-- fmt: off -->
`src/bybit_quant_lab/data/downloader.py` · líneas 78–96

```python
    path = dataset_path(data_dir, symbol, timeframe)
    existing = None
    if path.exists() and not refresh:
        existing = load_dataset(path)
        if not validate_ohlcv(existing, timeframe).is_valid:
            logger.warning("dataset local inválido, se descarga de nuevo: %s", path)
            existing = None
    have = pd.DatetimeIndex(existing.index if existing is not None else [], tz="UTC")
    todo = missing_ranges(have, start, end, timeframe)
    before = client.request_count
    frames = [existing] if existing is not None else []
    for a, b in todo:
        logger.info("descargando %s %s %s -> %s", symbol, timeframe, a, b)
        frames.append(client.fetch_klines(symbol, timeframe, a, b, limit=limit))
    non_empty = [f for f in frames if f is not None and len(f)]
    if not non_empty:
        raise ValueError(f"Bybit no devolvió datos para {symbol} {timeframe} en {start}..{end}")
    merged = pd.concat(non_empty)
    cleaned, report = clean_ohlcv(merged, timeframe)
```
<!-- fmt: on -->

- **80–84:** si existe un archivo local y no se pidió `--refresh`, se carga; si no supera la
  validación, se ignora y se descarga todo de nuevo.
- **86:** calcula los tramos que faltan.
- **89–91:** descarga solo esos tramos.
- **95–96:** une lo antiguo con lo nuevo y limpia el conjunto.

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.data.downloader import missing_ranges

guardadas = pd.date_range("2024-01-01 02:00", periods=8, freq="1h", tz="UTC").delete([3, 4])
tramos = missing_ranges(
    guardadas,
    pd.Timestamp("2024-01-01", tz="UTC"),
    pd.Timestamp("2024-01-01 12:00", tz="UTC"),
    "1h",
)
for a, b in tramos:
    print(a.strftime("%H:%M"), "->", b.strftime("%H:%M"))
```
*Salida real:*

```text
00:00 -> 02:00
05:00 -> 07:00
10:00 -> 12:00
```

Cabecera (00:00–02:00), hueco interno (05:00–07:00) y cola (10:00–12:00).

**[Limitación]** Los huecos reales del exchange (si Bybit no tiene esas velas) se vuelven a pedir
en cada descarga, porque el descargador no recuerda que ya los intentó. Es un desperdicio de
peticiones, no un error en los datos.

---

## 4.14 Almacenamiento en Parquet y metadatos

<!-- fmt: off -->
`src/bybit_quant_lab/data/storage.py` · líneas 34–69

```python
def save_dataset(
    df: pd.DataFrame, path: Path, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Guarda ``df`` en Parquet y escribe metadatos (procedencia, rango, hash)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, engine="pyarrow")
    meta: dict[str, Any] = dict(metadata or {})
    meta.update(
        {
            "rows": len(df),
            "start": str(df.index[0]) if len(df) else None,
            "end": str(df.index[-1]) if len(df) else None,
            "sha256": data_hash(df),
            "saved_at": datetime.now(UTC).isoformat(),
            "columns": list(df.columns),
        }
    )
    meta_path(path).write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")
    logger.info("dataset guardado %s filas=%d", path, len(df))
    return meta


def load_dataset(path: Path) -> pd.DataFrame:
    """Carga un Parquet OHLCV garantizando índice UTC ordenado."""
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Descarga datos con 'bql download', impórtalos con 'bql import' "
            "o genera datos sintéticos con 'bql synth'."
        )
    df = pd.read_parquet(path, engine="pyarrow")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError(f"{path} no tiene un índice temporal")
    if df.index.tz is None:
        df = df.tz_localize("UTC")
    df.index.name = "open_time"
    return df.sort_index()
```
<!-- fmt: on -->

- **save_dataset:** escribe el Parquet y, al lado, un archivo `.meta.json` con la procedencia
  (fuente, endpoint, URL base, historial de descargas), el informe de calidad, el número de
  filas, el rango y el **hash** del contenido (Módulo III, sección 3.11).
- **load_dataset:** si el archivo no existe, el error sugiere cómo obtener los datos. Garantiza
  índice UTC y orden cronológico al cargar.

**[Hecho]** La prueba `test_incremental_download_only_fetches_missing` comprueba que el hash
guardado en los metadatos coincide con el contenido del Parquet.

---

## 4.15 Funding: una descarga separada de las velas

El funding se descarga de **otro endpoint** (`/v5/market/funding/history`), se guarda en **otro
archivo** (`<SÍMBOLO>_funding.parquet`) y pagina en sentido contrario:

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 177–223

```python
    def fetch_funding_history(
        self,
        symbol: str,
        start: pd.Timestamp,
        end: pd.Timestamp,
        limit: int = 200,
        category: str = "linear",
    ) -> pd.Series:
        """Descarga tasas de funding históricas en ``[start, end]`` paginando hacia atrás."""
        rows: dict[pd.Timestamp, float] = {}
        cursor_end = end
        previous_oldest: pd.Timestamp | None = None
        while cursor_end >= start:
            params = {
                "category": category,
                "symbol": symbol.upper(),
                "startTime": _to_ms(start),
                "endTime": _to_ms(cursor_end),
                "limit": limit,
            }
            result = self.get("/v5/market/funding/history", params)
            items = result.get("list") or []
            if not isinstance(items, list):
                raise BybitAPIError("Campo 'list' de funding inválido")
            if not items:
                break
            stamps = []
            for item in items:
                try:
                    ts = pd.to_datetime(int(item["fundingRateTimestamp"]), unit="ms", utc=True)
                    rows[ts] = float(item["fundingRate"])
                except (KeyError, TypeError, ValueError) as exc:
                    raise BybitAPIError(f"Registro de funding inválido: {item}") from exc
                stamps.append(ts)
            oldest = min(stamps)
            if previous_oldest is not None and oldest >= previous_oldest:
                raise BybitAPIError(
                    "La paginación de funding no avanza (la API no respeta endTime); se "
                    "detiene para evitar un bucle infinito."
                )
            previous_oldest = oldest
            if len(items) < limit or oldest <= start:
                break
            cursor_end = oldest - pd.Timedelta(milliseconds=1)
        series = pd.Series(rows, dtype="float64", name="funding_rate").sort_index()
        series.index.name = "funding_time"
        return series[(series.index >= start) & (series.index <= end)]
```
<!-- fmt: on -->

- **Paginación hacia atrás (líneas 189–220):** pide hasta 200 registros que terminen en
  `cursor_end`, toma la marca más antigua recibida y mueve el cursor justo antes de ella.
- **Protección contra bucles (líneas 211–217):** si la marca más antigua no retrocede (porque la
  API ignora `endTime` y devuelve siempre la misma página), se lanza un error en vez de repetir la
  misma petición sin fin. **Esta protección se añadió en la auditoría** (hallazgo M-03,
  commit `a50ac62`); la prueba `test_funding_pagination_stops_if_api_does_not_advance`
  (`tests/unit/test_audit_data.py`, línea 106) falla con el código anterior.

**[Hecho]** Velas y funding nunca se mezclan: lo comprueba
`test_funding_uses_its_own_endpoint_and_file` (misma carpeta de pruebas, línea 71), que verifica
el endpoint, el nombre de archivo y que el Parquet de velas no cambia al descargar funding.

**[Supuesto]** Que la API real acepte `startTime` y `endTime` a la vez en este endpoint y pagine
como se describe. No se ha verificado contra Bybit.

---

## 4.16 Importar datos de otra fuente

Si no tienes acceso a la API, puedes importar un CSV o Parquet:

<!-- fmt: off -->
`src/bybit_quant_lab/data/importers.py` · líneas 15–41

```python
def read_ohlcv_file(path: Path, time_column: str | None = None) -> pd.DataFrame:
    """Lee CSV/Parquet y devuelve un DataFrame indexado por ``open_time`` UTC.

    La columna temporal puede ser ISO-8601 o epoch en milisegundos/segundos.
    """
    path = Path(path)
    if path.suffix.lower() == ".parquet":
        raw = pd.read_parquet(path)
    elif path.suffix.lower() in {".csv", ".txt"}:
        raw = pd.read_csv(path)
    else:
        raise ValueError(f"Formato no soportado: {path.suffix} (use .csv o .parquet)")
    raw.columns = [str(c).strip().lower() for c in raw.columns]
    if isinstance(raw.index, pd.DatetimeIndex):
        raw.index.name = "open_time"
        return raw
    col = time_column or next((c for c in TIME_CANDIDATES if c in raw.columns), None)
    if col is None:
        raise ValueError(f"No se encontró columna temporal; opciones: {TIME_CANDIDATES}")
    values = raw[col]
    if pd.api.types.is_numeric_dtype(values):
        unit = "ms" if values.abs().max() > 1e11 else "s"
        ts = pd.to_datetime(values, unit=unit, utc=True)  # type: ignore[call-overload]
    else:
        ts = pd.to_datetime(values, utc=True)
    out = raw.drop(columns=[col]).set_index(pd.DatetimeIndex(ts, name="open_time"))
    return out
```
<!-- fmt: on -->

- **27:** los nombres de columna se pasan a minúsculas y sin espacios.
- **31:** si no se indica la columna temporal, busca una de una lista de nombres habituales.
- **35–37:** si las fechas son números, decide si son milisegundos o segundos: un valor mayor que
  10^11 solo puede ser milisegundos (10^11 segundos sería el año 5138).
- **39:** si son textos, los interpreta como fechas. **[Supuesto]** Con `utc=True`, una fecha
  **sin** zona horaria se interpreta como UTC. Si tu CSV está en hora local, las velas quedarán
  desplazadas: convierte a UTC antes de importar.

---

## 4.17 Probar un cliente HTTP sin red: dobles de prueba

### La idea

Una prueba que depende de internet es lenta, frágil (falla si la red falla) e imposible de
ejecutar en entornos sin acceso, como el de este proyecto. La solución es sustituir la sesión
HTTP real por un **doble de prueba** (a menudo llamado *mock* o *fake*): un objeto que se
comporta como la sesión pero devuelve respuestas preparadas.

El cliente lo permite porque recibe la sesión, la función de espera y el reloj como parámetros
(inyección de dependencias, Módulo II, sección 2.14):

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 56–76

```python
    def __init__(
        self,
        base_url: str = "https://api.bybit.com",
        session: HTTPSession | None = None,
        max_retries: int = 5,
        backoff_seconds: float = 1.0,
        min_request_interval: float = 0.05,
        timeout_seconds: float = 15.0,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], pd.Timestamp] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session: HTTPSession = session if session is not None else requests.Session()  # type: ignore[assignment]
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds
        self.min_request_interval = min_request_interval
        self.timeout_seconds = timeout_seconds
        self._sleep = sleep
        self._clock = clock or (lambda: pd.Timestamp.now(tz="UTC"))
        self._last_request = 0.0
        self.request_count = 0
```
<!-- fmt: on -->

Y las pruebas definen un exchange simulado que imita el formato documentado, incluido el orden
descendente:

<!-- fmt: off -->
`tests/unit/test_data.py` · líneas 36–72

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
        if url.endswith("/kline"):
            step = int(params["interval"]) * 60_000
            start = params["start"] - params["start"] % step
            if start < params["start"]:
                start += step
            rows = []
            for t in range(start, params["end"] + 1, step):
                price = 100 + (t // step) % 7
                rows.append(
                    [
                        str(t),
                        str(price),
                        str(price + 1),
                        str(price - 1),
                        str(price + 0.5),
                        "10",
                        "1000",
                    ]
                )
            rows = rows[: params["limit"]][::-1]
            return FakeResponse(
                200, {"retCode": 0, "retMsg": "OK", "result": {"category": "linear", "list": rows}}
            )
```
<!-- fmt: on -->

Con él se comprueban paginación, orden, recorte de la vela abierta, reintentos ante cada tipo de
error, errores definitivos, descarga incremental, funding y la forma exacta de cada petición
para 5m, 15m, 1h y 4h (`tests/unit/test_data.py` y `tests/unit/test_audit_data.py`).

---

## 4.18 Qué demuestra una simulación y qué no

Un doble de prueba solo puede comprobar que el código **reacciona correctamente a las respuestas
que alguien imaginó**. Si la API real se comporta de otra forma, las pruebas pasarán igual.

| Comprobado con dobles de prueba **[Hecho]** | Solo comprobable con la API real **[Pendiente]** |
|---|---|
| Forma de las peticiones: endpoint, `category`, intervalos, ventanas contiguas sin solape, `limit` | Que Bybit devuelva todas las velas de `[start, end]` con la semántica supuesta de `end` |
| Conversión de textos, orden, duplicados, UTC, recorte de la vela abierta | El orden real de los 7 campos de cada vela |
| Reintentos ante red, 429, 5xx, JSON inválido y `retCode` transitorios; errores definitivos; 403 | Los `retCode` y mensajes reales en cada situación |
| Descarga incremental y detección de huecos | La disponibilidad histórica de cada símbolo y sus huecos reales |
| Separación entre funding y velas; protección contra bucles | La paginación real del funding con `startTime` y `endTime` |
| — | Las especificaciones reales del instrumento (`instruments-info`) |

---

## 4.19 Diagnosticar errores de red, proxy y API

Al ejecutar `bql download`, distintos problemas producen síntomas distintos:

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| Avisos `reintento 1/5 ... error de red: ... ProxyError` y al final `Reintentos agotados` | La red o un proxy impiden conectar con Bybit. **Es lo que ocurre en el entorno cloud donde se desarrolló el proyecto** | Comprueba la conexión: `curl -sS https://api.bybit.com/v5/market/time`. Si falla, el problema es de red, no del código |
| `HTTP 403: acceso denegado o IP limitada...` | Bybit (no el proxy) rechazó la petición: exceso de peticiones o bloqueo de la región | Espera al menos 10 minutos; revisa si tu región tiene acceso |
| `retCode 10001: ...` | Parámetros inválidos (por ejemplo, un símbolo que no existe en `linear`) | Revisa el símbolo |
| `Bybit no devolvió datos para ...` | El rango pedido es anterior al lanzamiento del contrato o está vacío | Ajusta `--start` |
| `Respuesta con formato inesperado` / `Vela con formato inválido` | La API respondió con una forma distinta de la supuesta | Es justo lo que hay que verificar con datos reales; informa del caso |

**[Hecho] Detalle de diagnóstico:** cuando es un **proxy** el que responde 403, `requests` lanza
`ProxyError`, que es un tipo de `ConnectionError`. El cliente lo trata como error de red
transitorio y reintenta cinco veces (unos 31 segundos de espera en total: 1 + 2 + 4 + 8 + 16)
antes de rendirse. El mensaje específico de 403 de las líneas 104–108 solo aparece si el 403
viene de Bybit. El resultado final es correcto (la descarga falla con un mensaje), pero el
diagnóstico podría ser más claro.

### Comprobación final del módulo

Una compañera dice: "las 20 pruebas de datos pasan, así que la descarga de Bybit funciona". ¿Qué
le responderías?

**Respuesta:**

Que las pruebas demuestran que el código maneja correctamente las respuestas **simuladas**, que
imitan el formato documentado. No demuestran que la API real responda así: el orden de los
campos, la semántica de `end`, la paginación del funding y los códigos de error reales solo se
confirman con una descarga real seguida de `bql validate-data`.

<div style="page-break-before: always;"></div>

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

*Ejemplo ejecutable:*

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
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import pandas as pd

como_texto = pd.Series(["42350.5", "42400", "error"])
print(como_texto.dtype)
numeros = pd.to_numeric(como_texto, errors="coerce")
print(numeros.tolist(), numeros.dtype)
```
*Salida real:*

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

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 109–112

```python
        # Identificador de día UTC independiente de la resolución del índice (ns, us, ms...).
        day_ids = (
            idx.floor("D").as_unit("s").tz_convert(None).to_numpy().astype("int64") // 86_400
        ).tolist()
```
<!-- fmt: on -->

`floor("D")` lleva cada fecha a la medianoche de su día; `as_unit("s")` fija la resolución en
segundos **antes** de convertir a número; al dividir entre 86.400 (segundos de un día) se obtiene
un número de día que no depende de la resolución original. La prueba de regresión
`test_daily_reference_resets_regardless_of_index_resolution` (`tests/unit/test_risk.py`) repite
el escenario con resoluciones `ns`, `us`, `ms` y `s`.

*Ejemplo ejecutable:*

```python
import pandas as pd

idx = pd.date_range("2024-01-01 22:00", periods=4, freq="1h", tz="UTC")
for unidad in ("ns", "ms"):
    i = idx.as_unit(unidad)
    ingenuo = (i.asi8 // 86_400_000_000_000).tolist()  # supone nanosegundos
    correcto = (
        i.floor("D").as_unit("s").tz_convert(None).to_numpy().astype("int64") // 86_400
    ).tolist()
    print(unidad, "ingenuo:", ingenuo, "| correcto:", correcto)
```
*Salida real:*

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

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 172–174

```python
        df = df[(df.index >= start) & (df.index < end)]
        closed = df.index + delta <= now
        return df[closed]
```
<!-- fmt: on -->

*Ejemplo ejecutable:*

```python
import pandas as pd

fechas = pd.date_range("2024-01-01", periods=5, freq="1h", tz="UTC")
velas = pd.DataFrame({"close": [100, 103, 99, 104, 101.0]}, index=fechas)
print(velas.iloc[-1]["close"], velas.loc["2024-01-01 02:00", "close"])
sube = velas["close"] > velas["close"].shift(1)
print(velas[sube & (velas["close"] > 100)])
```
*Salida real:*

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

<!-- fmt: off -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 170–171

```python
        df = pd.concat(frames)
        df = df[~df.index.duplicated(keep="last")].sort_index()
```
<!-- fmt: on -->

*Ejemplo ejecutable:*

```python
import pandas as pd


def tabla(horas, cierres):
    idx = pd.to_datetime(horas).tz_localize("UTC")
    return pd.DataFrame({"close": cierres}, index=idx)


ventana_2 = tabla(["2024-01-01 02:00", "2024-01-01 03:00"], [102.0, 103.0])
ventana_1 = tabla(
    ["2024-01-01 00:00", "2024-01-01 01:00", "2024-01-01 02:00"], [100.0, 101.0, 102.5]
)
unidas = pd.concat([ventana_2, ventana_1])
print(unidas.index.strftime("%H:%M").tolist())
limpias = unidas[~unidas.index.duplicated(keep="last")].sort_index()
print(limpias)
```
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

Tres Series se calculan de una vez, `pd.concat(..., axis=1)` las pone lado a lado como columnas y
`.max(axis=1)` toma el máximo **de cada fila**.

*Ejemplo ejecutable:*

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
*Salida real:*

```text
mismos resultados: True
el bucle es más lento que la versión vectorizada: True
```

(Los tiempos exactos varían entre ordenadores, por eso el ejemplo solo imprime la comparación.)

**[Diseño]** El motor de backtesting **no** está vectorizado: recorre las velas una a una con un
bucle, porque cada vela depende del estado que dejó la anterior (posición abierta, stops,
límites de riesgo). Para acelerar ese bucle, convierte las columnas a arrays de NumPy antes de
empezar, ya que acceder a un elemento de un array es mucho más rápido que a uno de una Series:

<!-- fmt: off -->
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
<!-- fmt: on -->

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

<!-- fmt: off -->
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

- **61–63:** `np.errstate` silencia, **solo dentro del bloque**, los avisos de división por cero
  (un context manager, Módulo II, sección 2.16).
- **64:** donde no hubo pérdidas (`loss == 0`), el RSI es 100.
- **65:** donde no hubo ni ganancias ni pérdidas, el RSI es 50.
- **66:** donde falta información (calentamiento), el resultado se deja en `NaN`.

*Ejemplo ejecutable:*

```python
import numpy as np
import pandas as pd

s = pd.Series([1.0, np.nan, 3.0])
print((s + 1).tolist(), (s > 2).tolist(), s.mean())
print(s.fillna(0).tolist(), s.where(s > 2, -1).tolist())
print(np.nan == np.nan)
```
*Salida real:*

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

<!-- fmt: off -->
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

Así, la pregunta "¿el cierre de hoy supera el máximo de las 20 velas **anteriores**?" no compara
la vela consigo misma.

Y la detección de cruces compara "ahora" con "antes":

<!-- fmt: off -->
`src/bybit_quant_lab/indicators/core.py` · líneas 171–174

```python
def crossover(a: pd.Series, b: pd.Series | float) -> pd.Series:
    """True en ``t`` si ``a`` cruza por encima de ``b`` entre ``t-1`` y ``t``."""
    bb = b if isinstance(b, pd.Series) else pd.Series(b, index=a.index)
    return ((a > bb) & (a.shift(1) <= bb.shift(1))).fillna(False).astype(bool)
```
<!-- fmt: on -->

Un cruce al alza en `t` ocurre si `a` está por encima de `b` en `t` **y** estaba por debajo o
igual en `t−1`.

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.indicators import crossover

rapida = pd.Series([1.0, 2.0, 3.0, 4.0, 3.0])
lenta = pd.Series([2.5, 2.5, 2.5, 2.5, 3.5])
tabla = pd.DataFrame(
    {
        "rapida": rapida,
        "rapida_ayer": rapida.shift(1),
        "lenta": lenta,
        "cruce_al_alza": crossover(rapida, lenta),
    }
)
print(tabla)
```
*Salida real:*

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

<!-- fmt: off -->
`src/bybit_quant_lab/indicators/core.py` · líneas 23–26

```python
def sma(s: pd.Series, n: int) -> pd.Series:
    """Media móvil simple de ``n`` velas (NaN hasta disponer de ``n`` valores)."""
    _check_period(n)
    return s.rolling(n, min_periods=n).mean()
```
<!-- fmt: on -->

*Ejemplo ejecutable:*

```python
import pandas as pd

cierre = pd.Series([10.0, 11.0, 12.0, 13.0, 14.0])
print(
    pd.DataFrame(
        {
            "cierre": cierre,
            "media_3": cierre.rolling(3, min_periods=3).mean(),
            "max_3": cierre.rolling(3, min_periods=3).max(),
            "desv_3": cierre.rolling(3, min_periods=3).std(ddof=0).round(4),
        }
    )
)
```
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

- `adjust=False` aplica exactamente la fórmula recursiva de arriba, empezando por el primer
  valor. **[Diseño]** Garantiza que el valor en `t` dependa solo de `x[0..t]`: si recortas la serie
  en `t`, los valores hasta `t` no cambian (es la base de las pruebas de ausencia de look-ahead).
- `wilder` es la misma idea con `α = 1/n`, el suavizado que usa J. Welles Wilder en el RSI, el
  ATR y el ADX (Módulo VII).

*Ejemplo ejecutable:*

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
*Salida real:*

```text
manual: [10.0, 11.0, 11.0, 12.0]
pandas: [10.0, 11.0, 11.0, 12.0]
```

---

## 5.11 Agrupar y acumular: el VWAP de sesión

`groupby(clave).cumsum()` calcula una **suma acumulada que se reinicia** cada vez que cambia la
clave. El VWAP de sesión (Módulo VII) la usa con la clave "día UTC":

<!-- fmt: off -->
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
<!-- fmt: on -->

*Ejemplo ejecutable:*

```python
import pandas as pd

idx = pd.date_range("2024-01-01 22:00", periods=4, freq="1h", tz="UTC")
volumen = pd.Series([1.0, 2.0, 3.0, 4.0], index=idx)
dia = idx.floor("1D")
print(
    pd.DataFrame(
        {
            "volumen": volumen,
            "acumulado_global": volumen.cumsum(),
            "acumulado_por_dia": volumen.groupby(dia).cumsum(),
        }
    )
)
```
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import pandas as pd

idx = pd.to_datetime(
    [
        "2024-01-01 00:00",
        "2024-01-01 01:00",
        "2024-01-01 02:00",
        "2024-01-01 09:00",
        "2024-01-01 10:00",
    ]
).tz_localize("UTC")
cierre = pd.Series([100.0, 101.0, 102.0, 110.0, 111.0], index=idx)
print(
    pd.DataFrame(
        {
            "cierre": cierre,
            "ultimas_3_filas": cierre.rolling(3).mean().round(2),
            "ultimas_3_horas": cierre.rolling("3h").mean().round(2),
        }
    )
)
```
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import pandas as pd

idx = pd.date_range("2024-01-01", periods=4, freq="1h", tz="UTC")
cierre = pd.Series([100.0, 101.0, 102.0, 103.0], index=idx)
desordenada = cierre.iloc[[2, 0, 3, 1]]
print("rendimiento ordenado:   ", cierre.pct_change().round(4).tolist())
print("rendimiento desordenado:", desordenada.pct_change().round(4).tolist())
print("¿ordenada?", desordenada.index.is_monotonic_increasing)
```
*Salida real:*

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

**Respuesta:**

(a) Media de las 5 últimas velas hasta `t`: sin look-ahead. (b) Compara el cierre de **mañana**
con el de hoy: look-ahead. (c) Ventana centrada, que incluye las dos velas siguientes:
look-ahead. (d) Diferencia entre el cierre de `t` y el de `t−1`: sin look-ahead.

<div style="page-break-before: always;"></div>

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

<!-- fmt: off -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 36–40

```python
def bar_returns(equity: pd.Series, initial: float) -> pd.Series:
    """Retornos simples por vela, empezando desde el capital inicial."""
    prev = equity.shift(1)
    prev.iloc[0] = initial
    return equity / prev - 1
```
<!-- fmt: on -->

`equity` es la serie de capital al cierre de cada vela. `shift(1)` trae el capital de la vela
anterior y, para la primera vela, se usa el capital inicial.

*Ejemplo ejecutable:*

```python
import math

print(round(110 / 100 - 1, 4), round(100 / 110 - 1, 4))
print(round(100 * 1.10 * 0.90, 4))
print(round(math.log(110 / 100) + math.log(100 / 110), 12))
print(round(math.log(1.01), 6), "≈", 0.01)
```
*Salida real:*

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

*Ejemplo ejecutable:*

```python
r = [0.10, -0.05, 0.08]
acumulado = 1.0
for x in r:
    acumulado *= 1 + x
print(round(acumulado - 1, 4), round(sum(r), 4))
print(round((12_100 / 10_000) ** (365 / 730) - 1, 4))
print(round(1.05 ** (365 / 30) - 1, 4))
```
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import numpy as np

x = np.array([2, 4, 4, 4, 5, 5, 7, 9])
print(x.mean(), np.median(x))
print(x.var(ddof=0), round(x.var(ddof=1), 3))
print(x.std(ddof=0), round(x.std(ddof=1), 3))
```
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import numpy as np

x, y = np.array([1, 2, 3.0]), np.array([2, 4, 7.0])
print(round(np.cov(x, y, ddof=1)[0, 1], 3), round(np.corrcoef(x, y)[0, 1], 3))

a = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])  # dos señales casi siempre en 0...
b = np.array([0, 0, 0, 1, 0, 0, 0, 0, 1, 0])
activas = (a != 0) & (b != 0)
print(
    "correlación:",
    round(np.corrcoef(a, b)[0, 1], 3),
    "| coinciden cuando ambas están activas:",
    float((a[activas] == b[activas]).mean()),
)
```
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

`z` son los valores **estandarizados** (restada la media y divididos entre la desviación); la
asimetría es la media de `z³` y la curtosis, la media de `z⁴`.

*Ejemplo ejecutable:*

```python
from statistics import NormalDist

N = NormalDist()
print(round(N.cdf(0), 3), round(N.cdf(1.96), 4), round(N.cdf(1) - N.cdf(-1), 4))
print(round(N.inv_cdf(0.975), 4), round(N.inv_cdf(0.99), 4))
```
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import numpy as np

rng = np.random.default_rng(7)
historias = rng.normal(loc=0.0, scale=50.0, size=(2000, 20))  # media real = 0
medias = historias.mean(axis=1)
print("error estándar teórico:", round(50 / np.sqrt(20), 2))
print("desviación de las medias simuladas:", round(medias.std(ddof=1), 2))
print(
    "historias con media > +15 USDT por operación:",
    round(float((medias > 15).mean()) * 100, 1),
    "%",
)
```
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

- **90:** el **estadístico t** mide cuántos errores estándar separan la media de 0:
  `t = x̄ / (s / √n)`.
- **91:** p-valor **unilateral** (solo cuenta resultados mejores, no peores): `1 − Φ(t)`.
  **[Supuesto]** Usa la distribución normal en lugar de la t de Student, una aproximación válida
  con muestras grandes. Por eso devuelve también un indicador `fiable` que solo es verdadero con
  30 o más operaciones.

Ejemplo a mano: 36 operaciones con ganancia media 10 USDT y desviación 30 USDT.
`SE = 30 / √36 = 5`; `t = 10 / 5 = 2`; `p = 1 − Φ(2) ≈ 0,0228`.

*Ejemplo ejecutable:*

```python
import numpy as np
import pandas as pd

from bybit_quant_lab.validation.overfitting import mean_pvalue

rng = np.random.default_rng(1)
pnl = rng.normal(0, 30, 36)
pnl = (pnl - pnl.mean()) / pnl.std(ddof=1) * 30 + 10  # media 10 y desviación 30 exactas
p, fiable = mean_pvalue(pd.Series(pnl))
print(round(p, 4), fiable)
```
*Salida real:*

```text
0.0228 True
```

### Comprobación

Una estrategia tiene p = 0,03 en su ganancia media. ¿Significa que hay un 97 % de probabilidad de
que funcione?

**Respuesta:**

No. Significa que, **si** la estrategia no tuviera ventaja, solo un 3 % de las veces se obtendría
una media tan buena o mejor. La probabilidad de que "funcione" no se puede leer en el p-valor, y
además el p-valor no tiene en cuenta cuántas estrategias probaste antes de encontrar esta
(sección 6.9).

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

<!-- fmt: off -->
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
<!-- fmt: on -->

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

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.validation.overfitting import holm_bonferroni

print(round(1 - 0.95**20, 3))
resultado = holm_bonferroni({"a": 0.01, "b": 0.04, "c": 0.03, "d": 0.005})
for nombre in "dacb":
    print(nombre, resultado[nombre])
```
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

- **117:** genera de una vez `n_samples` remuestras del mismo tamaño que los datos y calcula la
  media de cada una.
- **118:** el intervalo de confianza **percentil** al 95 % son los percentiles 2,5 y 97,5 de esas
  medias.
- **116:** la semilla fija hace que el resultado sea reproducible.

**[Supuesto]** El bootstrap simple supone que las observaciones son **independientes** entre sí.
Si las operaciones ganadoras se concentran en rachas (por ejemplo, en una tendencia), el
intervalo será demasiado estrecho. Existen variantes por bloques que conservan la dependencia
temporal; el proyecto no las implementa.

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.validation.overfitting import bootstrap_mean_ci

pnl = pd.Series([120, -40, -35, 60, -30, 15, -25, 200, -45, 10, -20, 35] * 3, dtype=float)
print("media observada:", round(pnl.mean(), 2))
bajo, alto = bootstrap_mean_ci(pnl, n_samples=2000, seed=1)
print("IC 95 % bootstrap:", round(bajo, 2), "a", round(alto, 2))
```
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import numpy as np

rng = np.random.default_rng(3)
# 100 estrategias sin ninguna ventaja: Sharpe verdadero 0, ruido de muestra 0,5
sharpes_observados = rng.normal(0.0, 0.5, size=(5000, 100))
mejor = sharpes_observados.max(axis=1)
print("Sharpe verdadero de todas: 0.0")
print("Sharpe medio de la mejor de 100:", round(mejor.mean(), 2))
```
*Salida real:*

```text
Sharpe verdadero de todas: 0.0
Sharpe medio de la mejor de 100: 1.25
```

La "mejor" de cien estrategias inútiles muestra en promedio un Sharpe de alrededor de 1,25. El
proyecto corrige este efecto con el **Deflated Sharpe Ratio** (Módulo XIII), que usa exactamente
esta idea: estima el Sharpe máximo que cabría esperar por azar entre `N` pruebas y exige superar
**ese** listón, no cero:

<!-- fmt: off -->
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
<!-- fmt: on -->

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

**Respuesta:**

No. Con 50 contrastes, Bonferroni exige `p < 0,05 / 50 = 0,001`. Un p-valor de 0,02 entre 50
pruebas es perfectamente compatible con el azar: con 50 estrategias sin ventaja, se espera que
una tenga `p ≤ 0,02` (50 × 0,02 = 1).

<div style="page-break-before: always;"></div>

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

*Ejemplo ejecutable:*

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
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.indicators import sma

v = pd.Series([10.0, 12.0, 8.0, 10.0, 40.0])
relativo = v / sma(v, 4).shift(1)
print(relativo.tolist())
print("incluyendo la vela actual:", (v / sma(v, 4)).round(3).tolist()[-1])
```
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.indicators import obv

print(obv(pd.Series([10, 11, 10, 10, 12.0]), pd.Series([100, 200, 300, 400, 500.0])).tolist())
```
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.indicators import vwap_rolling

idx = pd.date_range("2024-01-01", periods=2, freq="1h", tz="UTC")
velas = pd.DataFrame(
    {"high": [101, 112.0], "low": [99, 108.0], "close": [100, 110.0], "volume": [1, 3.0]}, index=idx
)
print(vwap_rolling(velas, 2).tolist())
```
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.indicators import donchian

velas = pd.DataFrame({"high": [5, 7, 6, 8, 12.0], "low": [4, 5, 5, 6, 9.0]})
print(donchian(velas, 3))
```
*Salida real:*

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

*Ejemplo ejecutable:*

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
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.indicators import rsi

print(rsi(pd.Series([10, 11, 10.5, 11.5, 12]), 2).round(2).tolist())
```
*Salida real:*

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

*Ejemplo ejecutable:*

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
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.indicators import bollinger

print(bollinger(pd.Series([2, 4, 4, 4, 5, 5, 7, 9.0]), n=8, k=2).iloc[-1].to_dict())
```
*Salida real:*

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

*Ejemplo ejecutable:*

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
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.indicators import rolling_percentile

print(rolling_percentile(pd.Series([3, 1, 4, 1, 5.0]), 4).tolist())
```
*Salida real:*

```text
[nan, nan, nan, nan, 1.0]
```

En la última vela, el 5 es mayor que los 4 valores anteriores `[3, 1, 4, 1]`: percentil 1,0.

### Temporalidad superior sin anticipación (`higher_timeframe`)

La estrategia 5 puede filtrar con una temporalidad mayor, por ejemplo velas de 4h sobre datos de
1h. El riesgo es usar una vela de 4h **antes de que termine**.

<!-- fmt: off -->
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

*Ejemplo ejecutable:*

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
*Salida real:*

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

**Respuesta:**

Para excluir la vela actual del canal. Sin el desplazamiento, el canal superior incluiría el
máximo de la vela actual, y como el cierre nunca puede superar el máximo de su propia vela, la
condición "cierre > canal superior" no se cumpliría jamás: la estrategia no tendría ninguna
entrada.

<div style="page-break-before: always;"></div>

# Módulo VIII. Las diez estrategias, una por una

Este módulo dedica un capítulo a cada estrategia. Antes, la sección 8.0 explica lo que todas
comparten: la clase base, los stops y cómo se convierte una señal en una operación simulada.

> **[Hecho] Advertencia general.** Que una estrategia produzca señales y pase sus pruebas solo
> demuestra que **implementa correctamente su regla**. No demuestra que la regla gane dinero. En
> este repositorio **ninguna** estrategia se ha evaluado con datos reales de mercado. Todos los
> ejemplos usan datos sintéticos o escenarios construidos a mano.

Las diez estrategias registradas (nombre interno, categoría y descripción):

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.strategies import available_strategies, get_strategy_class

for nombre in available_strategies():
    clase = get_strategy_class(nombre)
    print(f"{nombre:20s} {clase.category.value:10s} {clase.description}")
```
*Salida real:*

```text
adx_di               indicator  Dirección por +DI/-DI cuando ADX indica tendencia suficiente
bollinger_reversion  indicator  Reversión tras reingreso confirmado en las bandas de Bollinger
donchian_breakout    trend      Ruptura del canal Donchian de velas anteriores con gestión ATR
ema_crossover        trend      Cruce EMA rápida/lenta con filtro de tendencia y de lateralidad
macd_momentum        indicator  Cambio de momentum por cruce MACD/señal confirmado por histograma
obv_trend            volume     Cruce del OBV sobre su EMA confirmado por pendiente y precio
rsi_reversion        indicator  Reversión a la media por salida de sobreventa/sobrecompra del RSI
stoch_rsi            indicator  Cruces del Stochastic RSI en zonas extremas con confirmación
volume_spike         volume     Pico de volumen confirmado por vela direccional y ruptura del rango previo
vwap_deviation       volume     Desviación del precio respecto a VWAP con régimen de volumen (reversión o continuación)
```

**[Hecho]** El orden en que aparecen es el orden de importación en `strategies/__init__.py`
(alfabético). Los capítulos siguen la numeración del encargo original (volumen, tendencia,
indicadores).

---

## 8.0 Lo que comparten todas las estrategias

### Del evento a la señal: `generate_signals`

Cada estrategia solo implementa `compute_events`, que devuelve cinco series: entrada larga,
entrada corta, salida larga, salida corta y convicción. El resto lo hace la clase base:

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/base.py` · líneas 111–146

```python
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Devuelve el DataFrame de señales normalizadas (ver docstring del módulo)."""
        validate_input(data)
        if data.empty:
            return empty_signal_frame(data.index)
        ev = self.compute_events(data)
        p = self.params
        long_entry, short_entry = _clean_bool(ev.long_entry), _clean_bool(ev.short_entry)
        if not p.allow_short:
            short_entry = pd.Series(False, index=data.index)
        atr_ = atr(data, p.atr_period)
        stop = atr_ * p.stop_atr_mult
        # Sin stop válido (calentamiento del ATR) no se permite ENTRAR. Se aplica a los eventos,
        # antes de la máquina de estados, para no crear transiciones ficticias después.
        valid_stop = stop.notna() & (stop > 0)
        long_entry &= valid_stop
        short_entry &= valid_stop
        state = events_to_state(
            long_entry,
            short_entry,
            _clean_bool(ev.long_exit),
            _clean_bool(ev.short_exit),
            max_holding_bars=p.max_holding_bars,
            cooldown_bars=p.cooldown_bars,
        )
        out = pd.DataFrame(index=data.index)
        out["signal"] = state.astype("int64")
        conv = ev.conviction.reindex(data.index).astype("float64").clip(0, 1).fillna(0.0)
        out["conviction"] = conv.where(out["signal"] != 0, 0.0)
        out["stop_distance"] = stop
        out["take_profit_distance"] = stop * p.take_profit_r if p.take_profit_r else np.nan
        out["trailing_distance"] = atr_ * p.trailing_atr_mult if p.trailing_atr_mult else np.nan
        # Sin stop válido (ATR aún no disponible) no se permite abrir: se fuerza FLAT.
        out.loc[out["stop_distance"].isna() | (out["stop_distance"] <= 0), "signal"] = 0
        out.loc[out["signal"] == 0, "conviction"] = 0.0
        return out
```
<!-- fmt: on -->

- **113–115:** valida las columnas y el orden; con datos vacíos devuelve una tabla neutral.
- **116:** llama a la estrategia concreta (polimorfismo, Módulo II, sección 2.11).
- **118–120:** limpia los eventos (`NaN` → `False`) y, si `allow_short` es falso, anula los
  cortos.
- **121–127:** calcula el ATR y la distancia del stop (`ATR · stop_atr_mult`). Donde no hay stop
  válido (calentamiento del ATR), **anula las entradas antes de la máquina de estados**. Este
  orden se corrigió en la auditoría (commit `697b6af`, hallazgo M-04): antes se anulaba la señal
  **después**, y con un `atr_period` largo aparecía una entrada ficticia en la primera vela con
  ATR válido.
- **128–135:** convierte eventos en estado con `events_to_state` (explicada línea a línea en el
  Módulo II, sección 2.3).
- **136–145:** construye las cinco columnas del contrato. La convicción se recorta a [0, 1] y
  vale 0 cuando no hay posición deseada.

### Eventos "de nivel" y eventos "de cruce"

Dos tipos de condición aparecen en las estrategias:

- **Cruce:** verdadera solo en la vela en que algo **cambia** (la EMA rápida cruza la lenta).
- **Nivel:** verdadera **mientras** se cumple algo (el cierre está por encima del canal de
  Donchian).

Con la máquina de estados, ambos tipos funcionan: una vez en posición, una entrada repetida no
cambia nada. Pero el motor solo abre posición en la vela en que el estado **cambia** (entradas
"por transición", Módulo X). Consecuencia: si un stop cierra la operación y la condición de
nivel sigue cumpliéndose, **no** se vuelve a entrar hasta que el estado pase por FLAT y vuelva.

### Stops, objetivos y tiempo máximo por defecto

Los parámetros de salida comunes los define `StrategyParams` y cada estrategia cambia algunos.
Valores por defecto reales:

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.strategies import available_strategies, get_strategy_class

cols = [
    "atr_period",
    "stop_atr_mult",
    "take_profit_r",
    "trailing_atr_mult",
    "max_holding_bars",
    "cooldown_bars",
]
print(f"{'estrategia':20s} " + " ".join(f"{c[:14]:>14s}" for c in cols))
for nombre in available_strategies():
    p = get_strategy_class(nombre).params_model()
    print(f"{nombre:20s} " + " ".join(f"{str(getattr(p, c)):>14s}" for c in cols))
```
*Salida real:*

```text
estrategia               atr_period  stop_atr_mult  take_profit_r trailing_atr_m max_holding_ba  cooldown_bars
adx_di                           14            2.0           None            3.0           None              0
bollinger_reversion              14            2.0           None           None             48              0
donchian_breakout                14            2.0           None            3.0           None              0
ema_crossover                    14            2.0            2.0           None           None              0
macd_momentum                    14            2.0            2.0           None           None              0
obv_trend                        14            2.0            2.0           None           None              5
rsi_reversion                    14            2.0           None           None             48              0
stoch_rsi                        14            2.0            1.5           None             24              3
volume_spike                     14            2.0            2.0           None             48              0
vwap_deviation                   14            2.0           None           None           None              0
```

- `take_profit_r = 2.0` significa un objetivo a **2 veces la distancia del stop** ("2R").
  `None` significa sin objetivo fijo: la salida la decide la regla de la estrategia, el stop o
  el trailing.
- `trailing_atr_mult = 3.0` activa un stop que persigue al precio a 3 ATR del extremo alcanzado.
- `max_holding_bars` fuerza la salida tras ese número de velas.
- `cooldown_bars` impone una espera tras cada salida.

**[Limitación]** Todos estos valores son **convencionales o arbitrarios**: ninguno se ha
optimizado ni validado con datos reales (Módulo XVII).

### De la señal a la operación simulada

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config import AppConfig
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=3000, seed=7)
senales = create_strategy("ema_crossover").generate_signals(datos)
resultado = run_backtest(datos, senales, AppConfig(), "BTCUSDT", "1h")
op = resultado.trades.iloc[0]
i = datos.index.get_loc(op["entry_time"])
print(
    "señal al cierre de la vela",
    i - 1,
    "->",
    int(senales["signal"].iloc[i - 1]),
    "| vela anterior:",
    int(senales["signal"].iloc[i - 2]),
)
print(
    "entrada en la apertura de la vela",
    i,
    ":",
    round(datos["open"].iloc[i], 2),
    "-> ejecutada a",
    round(op["entry_price"], 2),
)
print(
    "stop a",
    round(senales["stop_distance"].iloc[i - 1], 2),
    "de distancia |",
    "salida:",
    op["exit_reason"],
    "| resultado neto:",
    round(op["net_pnl"], 2),
)
```
*Salida real:*

```text
señal al cierre de la vela 222 -> -1 | vela anterior: 0
entrada en la apertura de la vela 223 : 29387.94 -> ejecutada a 29382.07
stop a 599.27 de distancia | salida: take_profit | resultado neto: 179.99
```

El recorrido completo es:

1. **Cierre de la vela `i−1`:** la estrategia pasa de 0 a ±1.
2. **El motor** ve la transición y comprueba los límites de riesgo. Si puede, programa una orden.
3. **Apertura de la vela `i`:** compra (o vende) al precio de apertura con deslizamiento adverso
   (2 puntos básicos por defecto) y paga comisión. El tamaño depende de la distancia del stop
   (Módulo XI).
4. **Velas siguientes:** se vigilan stop, objetivo, trailing y liquidación; la regla de salida de
   la estrategia también puede cerrar la posición (Módulo X).

### Pruebas comunes a las diez estrategias

En `tests/unit/test_strategies.py`, parametrizadas para las diez:

| Prueba | Qué verifica |
|---|---|
| `test_output_contract` | Columnas, índice, señales en {−1, 0, 1}, convicción en [0, 1], stops positivos cuando hay señal |
| `test_no_lookahead_truncation` | Recortar los datos en `t` no cambia ninguna señal hasta `t` |
| `test_no_lookahead_future_perturbation` | Alterar precios y volumen posteriores a `t` no cambia nada hasta `t` |
| `test_empty_and_short_data` | Datos vacíos y series más cortas que el calentamiento |
| `test_missing_values_do_not_crash` | `NaN` intercalados |
| `test_missing_column_raises`, `test_invalid_params_rejected` | Errores claros con datos o parámetros inválidos |
| `test_long_only_mode` | `allow_short=False` elimina los cortos |
| `test_every_entry_coincides_with_an_entry_event` | Toda entrada tiene un evento de entrada detrás (regresión de M-04) |

---

## 8.1 Volume Spike + Price Confirmation (`volume_spike`)

**Hipótesis.** Un volumen anormalmente alto, **acompañado** de una vela fuerte que rompe el rango
de la vela anterior, indica una participación decidida en esa dirección. El volumen por sí solo no
dice hacia dónde.

**Condiciones.**

| Evento | Condición (todas a la vez) |
|---|---|
| Entrada larga | volumen relativo > `spike_mult`; cierre > apertura; cuerpo ≥ `min_body_ratio` del rango; cierre > máximo anterior (si `require_range_break`); ATR % dentro de los límites |
| Entrada corta | lo mismo en espejo: cierre < apertura, cierre < mínimo anterior |
| Salida larga | cierre < EMA(`exit_ema`) |
| Salida corta | cierre > EMA(`exit_ema`) |

**Código.**

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/volume_spike.py` · líneas 46–72

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        o, h, low, c, v = (data[k] for k in ("open", "high", "low", "close", "volume"))
        vol_ma = sma(v, p.volume_window).shift(1)  # solo velas anteriores
        ratio = v / vol_ma.replace(0, np.nan)
        spike = ratio > p.spike_mult
        rng = (h - low).replace(0, np.nan)
        body_ratio = (c - o).abs() / rng
        strong = body_ratio >= p.min_body_ratio
        atr_pct = atr(data, p.atr_period) / c
        vol_ok = atr_pct >= p.min_atr_pct
        if p.max_atr_pct is not None:
            vol_ok &= atr_pct <= p.max_atr_pct
        bull = (c > o) & strong
        bear = (c < o) & strong
        if p.require_range_break:
            bull &= c > h.shift(1)
            bear &= c < low.shift(1)
        trend_exit = ema(c, p.exit_ema)
        conviction = (ratio / (2 * p.spike_mult)).clip(0, 1) * body_ratio.fillna(0)
        return Events(
            long_entry=spike & bull & vol_ok,
            short_entry=spike & bear & vol_ok,
            long_exit=c < trend_exit,
            short_exit=c > trend_exit,
            conviction=conviction,
        )
```
<!-- fmt: on -->

- **52–54:** la "fuerza" de la vela es su cuerpo (`|cierre − apertura|`) dividido entre su rango
  (`máximo − mínimo`). Un cuerpo del 50 % o más es una vela decidida; un doji (cuerpo casi nulo)
  no lo es.
- **65:** convicción: volumen relativo dividido entre `2·spike_mult`, recortado y multiplicado
  por la fuerza del cuerpo.

**Parámetros.**

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/volume_spike.py` · líneas 19–29

```python
class VolumeSpikeParams(StrategyParams):
    """Parámetros de Volume Spike."""

    volume_window: int = Field(20, ge=2, le=1000)
    spike_mult: float = Field(2.5, gt=1, le=50)
    min_body_ratio: float = Field(0.5, ge=0, le=1)
    require_range_break: bool = True
    min_atr_pct: float = Field(0.0, ge=0)
    max_atr_pct: float | None = Field(None, gt=0)
    exit_ema: int = Field(20, ge=2, le=500)
    max_holding_bars: int | None = Field(48, ge=1)
```
<!-- fmt: on -->

**Ejemplos controlados.** Una serie plana de 60 velas con volumen 100; en la vela 50 se coloca
una vela concreta y se mira la señal en esa vela:

*Ejemplo ejecutable:*

```python
import numpy as np
import pandas as pd

from bybit_quant_lab.strategies import create_strategy

rng = np.random.default_rng(1)
cierres = 100 + rng.normal(0, 0.05, 60)
aperturas = np.r_[cierres[0], cierres[:-1]]
base = pd.DataFrame(
    {
        "open": aperturas,
        "high": np.maximum(aperturas, cierres) + 0.2,
        "low": np.minimum(aperturas, cierres) - 0.2,
        "close": cierres,
        "volume": 100.0,
    },
    index=pd.date_range("2024-01-01", periods=60, freq="1h", tz="UTC"),
)
estrategia = create_strategy("volume_spike", {"spike_mult": 3.0})


def senal_en_vela_50(open_, high, low, close, volume):
    datos = base.copy()
    datos.iloc[50] = [open_, high, low, close, volume]
    return int(estrategia.generate_signals(datos)["signal"].iloc[50])


print("vela alcista fuerte, volumen x10:", senal_en_vela_50(100, 103.2, 99.9, 103.0, 1000))
print("vela bajista fuerte, volumen x10:", senal_en_vela_50(100, 100.1, 96.8, 97.0, 1000))
print("doji, volumen x10:              ", senal_en_vela_50(100, 101.0, 99.0, 100.01, 1000))
print("vela alcista, volumen normal:   ", senal_en_vela_50(100, 103.2, 99.9, 103.0, 100))
```
*Salida real:*

```text
vela alcista fuerte, volumen x10: 1
vela bajista fuerte, volumen x10: -1
doji, volumen x10:               0
vela alcista, volumen normal:    0
```

Cálculo de la vela alcista: volumen relativo `1000 / 100 = 10 > 3`; cuerpo
`(103 − 100) / (103,2 − 99,9) = 0,91 ≥ 0,5`; cierre 103 por encima del máximo anterior (≈100,2).
Se cumplen todas las condiciones. El doji tiene el mismo volumen, pero su cuerpo es casi 0: sin
dirección no hay señal.

**Casos sin señal.** Volumen alto con vela indecisa; vela fuerte sin volumen; vela fuerte que no
rompe el rango anterior; y además, **[Hecho] detalle sutil**: si el cierre de la vela alcista
queda por debajo de su EMA de salida, la entrada y la salida coinciden en la misma vela y la regla
3 de `events_to_state` (la salida prevalece) impide entrar. En la práctica funciona como un filtro
implícito: no compra picos alcistas que ocurren por debajo de la EMA de 20 velas.

**Calentamiento.** `volume_window + 1` velas para el volumen relativo; 14 para el ATR; 20 para la
EMA de salida.

**Pruebas específicas.** `test_volume_spike_requires_price_confirmation`.

**Limitaciones.** Un solo exchange de volumen; los umbrales (2,5 veces, 50 % de cuerpo) son
arbitrarios; los picos de volumen son poco frecuentes, así que se esperan **pocas operaciones**, y
con pocas operaciones cualquier métrica es muy incierta (Módulo VI, sección 6.6).

---

## 8.2 OBV Trend Confirmation (`obv_trend`)

**Hipótesis.** Cuando el OBV cruza por encima de su media, con pendiente positiva, y el precio
está por encima de su propia media, el volumen **confirma** la tendencia alcista del precio (y en
espejo para la bajista).

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | OBV cruza al alza su EMA(`obv_ema`); OBV[t] − OBV[t−`slope_window`] > 0; cierre > EMA(`price_ema`) |
| Entrada corta | Espejo |
| Salida larga | OBV cruza a la baja su EMA **o** cierre < EMA del precio |
| Salida corta | Espejo |

**Código.**

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/obv_trend.py` · líneas 42–58

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        o = obv(c, data["volume"])
        o_ma = ema(o, p.obv_ema)
        slope = o - o.shift(p.slope_window)
        price_ma = ema(c, p.price_ema)
        dev = o - o_ma
        scale = o.diff().abs().rolling(p.obv_ema, min_periods=p.obv_ema).mean()
        conviction = (dev.abs() / (scale * np.sqrt(p.obv_ema)).replace(0, np.nan)).clip(0, 1)
        return Events(
            long_entry=crossover(o, o_ma) & (slope > 0) & (c > price_ma),
            short_entry=crossunder(o, o_ma) & (slope < 0) & (c < price_ma),
            long_exit=crossunder(o, o_ma) | (c < price_ma),
            short_exit=crossover(o, o_ma) | (c > price_ma),
            conviction=conviction,
        )
```
<!-- fmt: on -->

- **47:** la pendiente es la variación del OBV en las últimas `slope_window` velas.
- **49–51:** convicción: distancia entre el OBV y su media, dividida entre el cambio absoluto
  medio del OBV multiplicado por `√obv_ema`. **[Limitación]** Es una normalización arbitraria,
  sin interpretación estadística.

**Parámetros:** `obv_ema` 20, `price_ema` 50, `slope_window` 5, `cooldown_bars` 5 (líneas 19–25).
El enfriamiento evita reentrar en la vela siguiente a una salida, cuando el OBV oscila alrededor
de su media.

**Anatomía de una señal real** (datos sintéticos):

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.indicators import ema, obv
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=3000, seed=7)
s = create_strategy("obv_trend").generate_signals(datos)["signal"]
o = obv(datos["close"], datos["volume"])
tabla = pd.DataFrame(
    {
        "OBV": o,
        "EMA20(OBV)": ema(o, 20),
        "pendiente5": o - o.shift(5),
        "cierre": datos["close"],
        "EMA50(cierre)": ema(datos["close"], 50),
        "senal": s,
    }
)
for lado in (1, -1):
    t = int(((s == lado) & (s.shift(1, fill_value=0) != lado)).to_numpy().argmax())
    print("primera entrada", "LARGA" if lado == 1 else "CORTA", "en la vela", t)
    print(tabla.iloc[t - 1 : t + 1].round(1).to_string())
```
*Salida real:*

```text
primera entrada LARGA en la vela 70
                              OBV  EMA20(OBV)  pendiente5   cierre  EMA50(cierre)  senal
open_time                                                                               
2023-01-03 21:00:00+00:00 -3460.1     -3240.4       345.5  29044.1        28937.5      0
2023-01-03 22:00:00+00:00 -1410.6     -3066.1      3153.0  29180.3        28947.0      1
primera entrada CORTA en la vela 99
                              OBV  EMA20(OBV)  pendiente5   cierre  EMA50(cierre)  senal
open_time                                                                               
2023-01-05 02:00:00+00:00  1110.8      -143.0       162.0  29631.9        29310.6      1
2023-01-05 03:00:00+00:00  -603.8      -186.9     -2865.4  29295.7        29310.0     -1
```

Comprueba en cada caso: en la vela `t−1` el OBV estaba al otro lado de su EMA; en `t` la cruza, la
pendiente tiene el signo correcto y el cierre está del lado correcto de su EMA de 50.

**Pruebas específicas.** `test_obv_no_shorts_in_steady_uptrend`.

**Limitaciones.** El OBV es una aproximación tosca (Módulo VII, sección 7.2); la condición de
precio sobre EMA(50) se solapa con las estrategias de tendencia (redundancia, Módulo IX).

---

## 8.3 VWAP Deviation + Volume Regime (`vwap_deviation`)

**Hipótesis (dos, mutuamente excluyentes, elegidas con `mode`).**

- **`reversion`:** un precio muy alejado del VWAP **con volumen normal** está "estirado" sin
  respaldo y tiende a volver.
- **`continuation`:** un precio muy alejado del VWAP **con volumen alto** refleja una presión real
  que tiende a continuar.

**[Diseño]** Las dos lógicas nunca se mezclan: una ejecución usa una u otra. Mezclarlas sin una
regla que decida cuándo aplicar cada una produciría señales contradictorias.

**Condiciones** (`z` es la desviación normalizada respecto al VWAP, `vol_rel` el volumen
relativo):

| Modo | Entrada larga | Entrada corta | Salida larga | Salida corta |
|---|---|---|---|---|
| reversion | `z ≤ −entry_z` y `vol_rel ≤ max_rel_volume` | `z ≥ entry_z` y volumen tranquilo | `z ≥ −exit_z` | `z ≤ exit_z` |
| continuation | `z ≥ entry_z` y `vol_rel ≥ min_rel_volume` | `z ≤ −entry_z` y volumen activo | `z ≤ exit_z` | `z ≥ −exit_z` |

**Código.**

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/vwap_deviation.py` · líneas 61–90

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c, v = data["close"], data["volume"]
        vw = (
            vwap_rolling(data, p.vwap_window)
            if p.vwap_type == "rolling"
            else vwap_session(data, p.session)
        )
        dev = c - vw
        std = dev.rolling(p.dev_window, min_periods=p.dev_window).std().shift(1)
        z = dev / std.replace(0, np.nan)
        rel_vol = v / sma(v, p.volume_window).shift(1).replace(0, np.nan)
        conviction = ((z.abs() - p.entry_z) / p.entry_z).clip(0, 1)
        if p.mode == "reversion":
            quiet = rel_vol <= p.max_rel_volume
            return Events(
                long_entry=(z <= -p.entry_z) & quiet,
                short_entry=(z >= p.entry_z) & quiet,
                long_exit=z >= -p.exit_z,
                short_exit=z <= p.exit_z,
                conviction=conviction,
            )
        active = rel_vol >= p.min_rel_volume
        return Events(
            long_entry=(z >= p.entry_z) & active,
            short_entry=(z <= -p.entry_z) & active,
            long_exit=z <= p.exit_z,
            short_exit=z >= -p.exit_z,
            conviction=conviction,
        )
```
<!-- fmt: on -->

- **70–71:** el z-score usa la desviación de las `dev_window` velas **anteriores** (`shift(1)`):
  la vela actual no infla su propia normalización.
- **72:** volumen relativo, como en la sección 8.1.

**Parámetros** (líneas 28–41): `mode` reversion, `vwap_type` rolling, `vwap_window` 96,
`session` "1D", `dev_window` 100, `entry_z` 2,0, `exit_z` 0,5, `volume_window` 50,
`max_rel_volume` y `min_rel_volume` 1,5, sin objetivo fijo.

**Ejemplo controlado.** 300 velas casi planas; en la vela 280 el precio cae de 100 a 95:

*Ejemplo ejecutable:*

```python
import numpy as np
import pandas as pd

from bybit_quant_lab.strategies import create_strategy

rng = np.random.default_rng(1)
cierres = 100 + rng.normal(0, 0.2, 300)
aperturas = np.r_[cierres[0], cierres[:-1]]
datos = pd.DataFrame(
    {
        "open": aperturas,
        "high": np.maximum(aperturas, cierres) + 0.2,
        "low": np.minimum(aperturas, cierres) - 0.2,
        "close": cierres,
        "volume": 100.0,
    },
    index=pd.date_range("2024-01-01", periods=300, freq="1h", tz="UTC"),
)
datos.iloc[280, :4] = [100, 100.2, 94.8, 95]
parametros = {"vwap_window": 50, "dev_window": 50}
for volumen in (100.0, 1000.0):
    datos.iloc[280, 4] = volumen
    rev = create_strategy("vwap_deviation", {**parametros, "mode": "reversion"}).generate_signals(
        datos
    )
    con = create_strategy(
        "vwap_deviation", {**parametros, "mode": "continuation"}
    ).generate_signals(datos)
    print(
        f"volumen {volumen:6.0f}: reversion -> {int(rev['signal'].iloc[280]):2d} | "
        f"continuation -> {int(con['signal'].iloc[280]):2d}"
    )
```
*Salida real:*

```text
volumen    100: reversion ->  1 | continuation ->  0
volumen   1000: reversion ->  0 | continuation -> -1
```

Con volumen normal, solo la hipótesis de reversión actúa (compra esperando el regreso al VWAP).
Con volumen diez veces mayor, solo actúa la de continuación (vende siguiendo la caída). Es la
prueba `test_vwap_hypotheses_are_separate`.

**Calentamiento.** En modo móvil, `vwap_window` + `dev_window` velas (unas 196 por defecto).
**Limitaciones.** El VWAP de sesión se basa en muy pocas velas al principio de cada día UTC
(Módulo VII, sección 7.3); `entry_z = 2` no implica una probabilidad del 5 %, porque las
desviaciones no son normales.

---

## 8.4 EMA Crossover + Trend Filter (`ema_crossover`)

**Hipótesis.** Un cruce de una EMA rápida sobre una lenta, en la dirección de la tendencia de
fondo y con fuerza de tendencia suficiente, marca el inicio de un movimiento sostenido.

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | EMA(`fast`) cruza al alza EMA(`slow`); cierre > EMA(`trend_ema`) (si está activa); filtro de régimen (ADX ≥ `adx_min`, ATR % ≥ `atr_pct_min` o ninguno) |
| Entrada corta | Espejo |
| Salida larga / corta | El cruce contrario |

**Código y parámetros:** `strategies/ema_crossover.py`, líneas 20–74, explicado línea a línea en
el Módulo II (sección 2.11). Por defecto: 12/26, EMA de tendencia 200, filtro ADX ≥ 20, objetivo
2R.

**Anatomía de una señal real:**

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.indicators import adx, ema
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=3000, seed=7)
c = datos["close"]
s = create_strategy("ema_crossover").generate_signals(datos)["signal"]
tabla = pd.DataFrame(
    {
        "EMA12": ema(c, 12),
        "EMA26": ema(c, 26),
        "cierre": c,
        "EMA200": ema(c, 200),
        "ADX": adx(datos, 14)["adx"],
        "senal": s,
    }
)
t = int(((s == 1) & (s.shift(1, fill_value=0) != 1)).to_numpy().argmax())
print("primera entrada larga en la vela", t)
print(tabla.iloc[t - 1 : t + 1].round(2).to_string())
print(
    "velas con señal sin filtros:",
    int(
        (
            create_strategy(
                "ema_crossover", {"trend_ema": None, "regime_filter": "none"}
            ).generate_signals(datos)["signal"]
            != 0
        ).sum()
    ),
    "| con filtros:",
    int((s != 0).sum()),
)
```
*Salida real:*

```text
primera entrada larga en la vela 986
                              EMA12     EMA26    cierre    EMA200    ADX  senal
open_time                                                                      
2023-02-11 01:00:00+00:00  22245.80  22248.51  22135.06  21369.72  28.77      0
2023-02-11 02:00:00+00:00  22267.52  22258.77  22386.98  21379.84  27.69      1
velas con señal sin filtros: 2945 | con filtros: 464
```

En `t−1` la EMA12 está por debajo de la EMA26 y en `t` por encima: hay cruce. El cierre supera la
EMA200 y el ADX supera 20. La última línea muestra el efecto de los filtros: el número de velas en
posición se reduce mucho.

**Pruebas específicas.** `test_ema_crossover_v_shape_goes_long`,
`test_ema_crossover_regime_filter_blocks_range`.

**Limitaciones.** Las medias se retrasan; en mercados laterales los cruces se repiten (los
filtros los reducen, no los eliminan); la EMA200 exige 200 velas de historia. Con los filtros
activos, el número de operaciones puede ser pequeño.

---

## 8.5 Donchian Breakout + ATR (`donchian_breakout`)

**Hipótesis.** Un cierre fuera del rango de las últimas `channel` velas inicia un movimiento
direccional (la idea clásica de los sistemas de "tortugas").

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | cierre > máximo de las `channel` velas **anteriores**; filtro de temporalidad superior (opcional) |
| Entrada corta | cierre < mínimo de las `channel` velas anteriores |
| Salida larga | cierre < mínimo de las `exit_channel` velas anteriores |
| Salida corta | cierre > máximo de las `exit_channel` velas anteriores |

**Código.**

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/donchian_breakout.py` · líneas 58–83

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        ch = donchian(data, p.channel)
        ex = donchian(data, p.exit_channel)
        up_ok = pd.Series(True, index=c.index)
        dn_ok = pd.Series(True, index=c.index)
        if p.htf is not None and len(data) >= 2:
            htf = higher_timeframe(
                data,
                infer_bar_delta(pd.DatetimeIndex(data.index)),
                pd.Timedelta(p.htf),
                ema_period=p.htf_ema,
            )
            up_ok = htf["close"] > htf["ema"]
            dn_ok = htf["close"] < htf["ema"]
        width = (ch["upper"] - ch["lower"]).where(lambda w: w > 0)
        conviction = ((c - ch["mid"]).abs() / width).clip(0, 1) * 2
        a = atr(data, p.atr_period)
        return Events(
            long_entry=(c > ch["upper"]) & up_ok & a.notna(),
            short_entry=(c < ch["lower"]) & dn_ok & a.notna(),
            long_exit=c < ex["lower"],
            short_exit=c > ex["upper"],
            conviction=conviction,
        )
```
<!-- fmt: on -->

- **65–73:** filtro opcional de temporalidad superior (por ejemplo, `htf: "4h"`): solo largos si
  el cierre de la última vela de 4h **cerrada** está por encima de su EMA. La alineación sin
  anticipación se explicó en el Módulo VII (sección 7.12).
- **78–79:** `a.notna()` exige un ATR válido. **[Hecho]** Desde la corrección M-04 la clase base
  ya lo garantiza; la condición es redundante, aunque inofensiva.

**Parámetros** (líneas 25–41): `channel` 20, `exit_channel` 10 (no puede superar a `channel`),
`htf` desactivado, `htf_ema` 50, **sin objetivo** y **trailing de 3 ATR**: la estrategia deja
correr las tendencias y sale por el canal corto o por el trailing.

**Ejemplos controlados** (prueba `test_donchian_uses_previous_bars_only`):

*Ejemplo ejecutable:*

```python
import numpy as np
import pandas as pd

from bybit_quant_lab.strategies import create_strategy

rng = np.random.default_rng(1)
cierres = 100 + rng.normal(0, 0.1, 40)
aperturas = np.r_[cierres[0], cierres[:-1]]
base = pd.DataFrame(
    {
        "open": aperturas,
        "high": np.maximum(aperturas, cierres) + 0.2,
        "low": np.minimum(aperturas, cierres) - 0.2,
        "close": cierres,
        "volume": 100.0,
    },
    index=pd.date_range("2024-01-01", periods=40, freq="1h", tz="UTC"),
)
estrategia = create_strategy(
    "donchian_breakout", {"channel": 20, "exit_channel": 10, "atr_period": 5}
)
maximo_previo = base["high"].iloc[15:35].max()
minimo_previo = base["low"].iloc[15:35].min()
print("máximo de las 20 velas anteriores:", round(maximo_previo, 3))
for nombre, cierre, extremo in (
    ("ruptura al alza", maximo_previo + 0.01, maximo_previo + 0.02),
    ("ruptura a la baja", minimo_previo - 0.01, minimo_previo - 0.02),
    ("dentro del canal", 100.0, 100.1),
):
    datos = base.copy()
    columna = "high" if cierre > 100 else "low"
    datos.loc[datos.index[35], ["close", columna]] = [cierre, extremo]
    print(
        f"{nombre:18s} -> señal en la vela 35:",
        int(estrategia.generate_signals(datos)["signal"].iloc[35]),
    )
```
*Salida real:*

```text
máximo de las 20 velas anteriores: 100.412
ruptura al alza    -> señal en la vela 35: 1
ruptura a la baja  -> señal en la vela 35: -1
dentro del canal   -> señal en la vela 35: 0
```

Basta con superar el máximo previo en un céntimo. Esta sensibilidad tiene su contrapartida: en
mercados laterales, las rupturas falsas son frecuentes, y el stop de 2 ATR las convierte en
pequeñas pérdidas repetidas.

**[Hecho] Hallazgo de revisión (nuevo, no recogido en la auditoría): la convicción no informa.**
La línea 75 calcula `(|cierre − medio| / ancho).clip(0, 1) * 2`. En una ruptura el cierre está
fuera del canal, la fracción es al menos 0,5 y, multiplicada por 2, llega a 1 o más; la clase base
la recorta a 1. Con 6.000 velas sintéticas, la convicción valía exactamente 1 en las 165 entradas.
Solo afecta a las combinaciones que ponderan por convicción (`use_conviction`, Módulo IX), que
por defecto no lo hacen.

**Pruebas específicas.** `test_donchian_uses_previous_bars_only`,
`test_donchian_htf_filter_runs_without_lookahead`.

---

## 8.6 RSI Mean Reversion (`rsi_reversion`)

**Hipótesis.** Tras una sobreventa (RSI < 30), el **regreso** del RSI por encima de 30 indica que
la presión vendedora se agota y el precio tiende a rebotar (en espejo para la sobrecompra).

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | RSI cruza al alza `oversold` (30); filtro de tendencia |
| Entrada corta | RSI cruza a la baja `overbought` (70); filtro de tendencia |
| Salida larga | RSI ≥ `exit_level` (50) |
| Salida corta | RSI ≤ `exit_level` |

**[Diseño]** Tocar la zona no basta: se exige **salir** de ella. Comprar mientras el RSI sigue
cayendo por debajo de 30 sería "intentar atrapar un cuchillo que cae".

**Código.**

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/rsi_reversion.py` · líneas 60–81

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        r = rsi(c, p.rsi_period)
        long_ok = pd.Series(True, index=c.index)
        short_ok = pd.Series(True, index=c.index)
        if p.trend_filter == "ema":
            t = ema(c, p.trend_ema)
            long_ok, short_ok = c > t, c < t
        elif p.trend_filter == "adx":
            weak = adx(data, p.adx_period)["adx"] < p.adx_max
            long_ok, short_ok = weak, weak
        depth_long = (p.oversold - r.rolling(5, min_periods=1).min()) / p.oversold
        depth_short = (r.rolling(5, min_periods=1).max() - p.overbought) / (100 - p.overbought)
        conviction = depth_long.clip(lower=0).combine(depth_short.clip(lower=0), max) * 2
        return Events(
            long_entry=crossover(r, p.oversold) & long_ok,
            short_entry=crossunder(r, p.overbought) & short_ok,
            long_exit=r >= p.exit_level,
            short_exit=r <= p.exit_level,
            conviction=conviction,
        )
```
<!-- fmt: on -->

- **66–71:** filtro de tendencia. Con `ema`, solo largos por encima de la EMA200 (comprar caídas
  dentro de una tendencia alcista). Con `adx` (por defecto), solo se opera si el ADX < 25, es
  decir, cuando **no** hay tendencia fuerte: la reversión a la media tiene más sentido en un
  mercado lateral.
- **72–74:** convicción: profundidad de la incursión en la zona en las últimas 5 velas,
  multiplicada por 2.

**Parámetros** (líneas 24–42): validación `oversold < exit_level < overbought`; sin objetivo
fijo; máximo 48 velas.

**Ejemplo controlado:** 30 velas planas, una caída de 100 a 80 y un rebote:

*Ejemplo ejecutable:*

```python
import numpy as np
import pandas as pd

from bybit_quant_lab.indicators import rsi
from bybit_quant_lab.strategies import create_strategy

rng = np.random.default_rng(1)
cierres = np.r_[np.full(30, 100.0), np.linspace(100, 80, 20), np.linspace(80, 84, 6)] + rng.normal(
    0, 0.02, 56
)
aperturas = np.r_[cierres[0], cierres[:-1]]
datos = pd.DataFrame(
    {
        "open": aperturas,
        "high": np.maximum(aperturas, cierres) + 0.1,
        "low": np.minimum(aperturas, cierres) - 0.1,
        "close": cierres,
        "volume": 100.0,
    },
    index=pd.date_range("2024-01-01", periods=56, freq="1h", tz="UTC"),
)
s = create_strategy("rsi_reversion", {"trend_filter": "none"}).generate_signals(datos)["signal"]
r = rsi(datos["close"], 14)
for t in range(48, 56):
    print(t, round(r.iloc[t], 1), int(s.iloc[t]))
```
*Salida real:*

```text
48 0.4 0
49 0.3 0
50 0.3 0
51 7.8 0
52 15.0 0
53 21.3 0
54 27.4 0
55 32.6 1
```

Durante la caída el RSI se hunde muy por debajo de 30 sin señal; la entrada larga aparece en la
vela en que el RSI **vuelve a cruzar** por encima de 30.

**Pruebas específicas.** `test_rsi_reversion_long_after_oversold_exit`.

**Limitaciones.** En tendencias fuertes, la reversión pierde repetidamente (de ahí el filtro). Sin
objetivo fijo y con salida en RSI 50, el beneficio por operación suele ser pequeño y **sensible a
los costes**. Es una de las estrategias con menos operaciones en los datos sintéticos.

---

## 8.7 MACD Momentum (`macd_momentum`)

**Hipótesis.** El cruce de la línea MACD sobre su señal marca una aceleración del impulso. Un
filtro direccional opcional exige que ese impulso vaya a favor de la tendencia de fondo.

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | MACD cruza al alza la señal; histograma creciente (si `require_hist_rising`); filtro direccional (`ema`: cierre > EMA200; `zero_line`: MACD > 0; `none`) |
| Entrada corta | Espejo |
| Salida | El cruce contrario |

**Código.**

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/macd_momentum.py` · líneas 53–76

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        m = macd(c, p.fast, p.slow, p.signal_period)
        hist = m["hist"]
        rising, falling = hist > hist.shift(1), hist < hist.shift(1)
        if not p.require_hist_rising:
            rising = falling = pd.Series(True, index=c.index)
        if p.direction_filter == "ema":
            t = ema(c, p.trend_ema)
            up_ok, dn_ok = c > t, c < t
        elif p.direction_filter == "zero_line":
            up_ok, dn_ok = m["macd"] > 0, m["macd"] < 0
        else:
            up_ok = dn_ok = pd.Series(True, index=c.index)
        scale = hist.abs().rolling(100, min_periods=20).max()
        conviction = (hist.abs() / scale).clip(0, 1)
        return Events(
            long_entry=crossover(m["macd"], m["signal"]) & rising & up_ok,
            short_entry=crossunder(m["macd"], m["signal"]) & falling & dn_ok,
            long_exit=crossunder(m["macd"], m["signal"]),
            short_exit=crossover(m["macd"], m["signal"]),
            conviction=conviction,
        )
```
<!-- fmt: on -->

**[Hecho] Hallazgo de revisión (nuevo, no recogido en la auditoría): `require_hist_rising` no
tiene ningún efecto.** El histograma es `MACD − señal`. Un cruce al alza en `t` exige
`MACD[t] > señal[t]` (histograma positivo) y `MACD[t−1] ≤ señal[t−1]` (histograma ≤ 0). Por tanto
`hist[t] > 0 ≥ hist[t−1]`: el histograma **siempre** sube en un cruce al alza. La condición de la
línea 58 es matemáticamente redundante:

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=6000, seed=11)
for filtro in ("none", "ema", "zero_line"):
    con = create_strategy(
        "macd_momentum", {"require_hist_rising": True, "direction_filter": filtro}
    )
    sin = create_strategy(
        "macd_momentum", {"require_hist_rising": False, "direction_filter": filtro}
    )
    print(
        filtro,
        "señales idénticas:",
        con.generate_signals(datos)["signal"].equals(sin.generate_signals(datos)["signal"]),
    )
```
*Salida real:*

```text
none señales idénticas: True
ema señales idénticas: True
zero_line señales idénticas: True
```

**Consecuencia:** la rejilla de búsqueda de `configs/strategies.yaml` (línea 185) incluye
`require_hist_rising: [true, false]` y **duplica** configuraciones que producen exactamente las
mismas operaciones. El registro de experimentos las cuenta como pruebas distintas, lo que infla
el número de pruebas del Deflated Sharpe (Módulo XIII), en la dirección conservadora. Es el mismo
tipo de problema que el hallazgo B-01 de la auditoría (dos combinaciones idénticas).

**Contribución incremental del filtro direccional.** Para medir si un filtro aporta algo hay que
comparar variantes **en entrenamiento**, nunca en el test:

```bash
bql sensitivity --symbol BTCUSDT --timeframe 1h --strategy macd_momentum \
  --grid '{"direction_filter": ["none", "ema", "zero_line"]}'
```

**Pruebas específicas.** `test_macd_v_shape_goes_long`. **Limitaciones.** Los cruces del MACD
son frecuentes y se retrasan; en mercados laterales generan muchas entradas y salidas.

---

## 8.8 Bollinger Bands Reversion (`bollinger_reversion`)

**Hipótesis.** Un cierre **fuera** de la banda seguido de un cierre de **regreso** dentro de ella
indica que el exceso se corrige: el precio tiende a volver a la media.

**[Diseño]** Es una hipótesis de **reversión**, separada de la de **ruptura** de bandas (que
diría lo contrario: salir de la banda es el inicio de un movimiento). Tocar la banda no basta.

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | cierre[t−1] < banda inferior[t−1] **y** cierre[t] > banda inferior[t]; vela alcista (si `confirm_candle`); ADX < `adx_max` (si está definido) |
| Entrada corta | Espejo con la banda superior |
| Salida larga | cierre ≥ media (objetivo alcanzado) **o** cierre < banda inferior (invalidación: el setup falló) |
| Salida corta | Espejo |

**Código.**

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/bollinger_reversion.py` · líneas 47–70

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        o, c = data["open"], data["close"]
        bb = bollinger(c, p.period, p.num_std)
        below_prev = c.shift(1) < bb["lower"].shift(1)
        above_prev = c.shift(1) > bb["upper"].shift(1)
        long_setup = below_prev & (c > bb["lower"])
        short_setup = above_prev & (c < bb["upper"])
        if p.confirm_candle:
            long_setup &= c > o
            short_setup &= c < o
        if p.adx_max is not None:
            weak = adx(data, p.adx_period)["adx"] < p.adx_max
            long_setup &= weak
            short_setup &= weak
        width = (bb["upper"] - bb["lower"]).where(lambda w: w > 0)
        conviction = ((bb["mid"] - c).abs() / (width / 2)).clip(0, 1)
        return Events(
            long_entry=long_setup,
            short_entry=short_setup,
            long_exit=(c >= bb["mid"]) | (c < bb["lower"]),
            short_exit=(c <= bb["mid"]) | (c > bb["upper"]),
            conviction=conviction,
        )
```
<!-- fmt: on -->

**Ejemplo controlado** (prueba `test_bollinger_touch_is_not_signal_but_reentry_is`):

*Ejemplo ejecutable:*

```python
import numpy as np
import pandas as pd

from bybit_quant_lab.indicators import bollinger
from bybit_quant_lab.strategies import create_strategy

rng = np.random.default_rng(1)
cierres = 100 + rng.normal(0, 0.3, 80)
aperturas = np.r_[cierres[0], cierres[:-1]]
base = pd.DataFrame(
    {
        "open": aperturas,
        "high": np.maximum(aperturas, cierres) + 0.1,
        "low": np.minimum(aperturas, cierres) - 0.1,
        "close": cierres,
        "volume": 100.0,
    },
    index=pd.date_range("2024-01-01", periods=80, freq="1h", tz="UTC"),
)
estrategia = create_strategy("bollinger_reversion", {"adx_max": None, "confirm_candle": True})

toque = base.copy()
toque.loc[toque.index[60], "low"] = 95.0  # la mecha toca, el cierre no sale
print(
    "toque de banda -> señales en velas 58-62:",
    estrategia.generate_signals(toque)["signal"].iloc[58:63].tolist(),
)

reingreso = base.copy()
reingreso.loc[reingreso.index[60], ["open", "close", "low", "high"]] = [100.0, 97.0, 96.9, 100.1]
reingreso.loc[reingreso.index[61], ["open", "close", "low", "high"]] = [97.0, 99.5, 96.95, 99.6]
bandas = bollinger(reingreso["close"], 20, 2.0)
for t in (60, 61):
    print(
        t,
        "cierre",
        reingreso["close"].iloc[t],
        "| banda inferior",
        round(bandas["lower"].iloc[t], 2),
        "| señal",
        int(estrategia.generate_signals(reingreso)["signal"].iloc[t]),
    )
```
*Salida real:*

```text
toque de banda -> señales en velas 58-62: [0, 0, 0, 0, 0]
60 cierre 97.0 | banda inferior 98.47 | señal 0
61 cierre 99.5 | banda inferior 98.45 | señal 1
```

En la vela 60 el cierre (97) queda **por debajo** de la banda inferior; en la 61 vuelve a entrar
(99,5 por encima de la banda) con una vela alcista: entrada larga.

**Limitaciones.** En tendencias fuertes el precio "camina" por la banda y la reversión falla (de
ahí el filtro de ADX < 30). La salida en la media ofrece un recorrido limitado frente a un stop de
2 ATR: la relación entre ganancia y pérdida por operación puede ser desfavorable incluso con un
alto porcentaje de aciertos (Módulo XII).

---

## 8.9 Stochastic RSI (`stoch_rsi`)

**Hipótesis.** Un cruce de %K sobre %D **dentro** de la zona extrema (%K < 20) con una vela de
confirmación indica un giro de corto plazo.

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | %K cruza al alza %D con %K[t−1] < `lower`; vela alcista (si `confirm_candle`); cierre > EMA(`trend_ema`) (si se define); **rearmado** |
| Entrada corta | Espejo con `upper` |
| Salida larga | %K cruza a la baja %D con %K > `rearm_level` |
| Salida corta | Espejo |

**Código.**

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/stoch_rsi.py` · líneas 63–88

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        o, c = data["open"], data["close"]
        st = stoch_rsi(c, p.rsi_period, p.stoch_period, p.k_smooth, p.d_smooth)
        k, d = st["k"], st["d"]
        long_raw = crossover(k, d) & (k.shift(1) < p.lower)
        short_raw = crossunder(k, d) & (k.shift(1) > p.upper)
        if p.confirm_candle:
            long_raw &= c > o
            short_raw &= c < o
        if p.trend_ema:
            t = ema(c, p.trend_ema)
            long_raw &= c > t
            short_raw &= c < t
        long_entry = rearm_events(long_raw, k > p.rearm_level)
        short_entry = rearm_events(short_raw, k < p.rearm_level)
        conviction = ((p.lower - k.shift(1)).clip(lower=0) / p.lower).combine(
            ((k.shift(1) - p.upper).clip(lower=0) / (100 - p.upper)), max
        )
        return Events(
            long_entry=long_entry,
            short_entry=short_entry,
            long_exit=crossunder(k, d) & (k > p.rearm_level),
            short_exit=crossover(k, d) & (k < p.rearm_level),
            conviction=conviction,
        )
```
<!-- fmt: on -->

**El rearmado (líneas 77–78).** El Stochastic RSI oscila mucho: dentro de una misma zona de
sobreventa puede cruzar %D varias veces en pocas velas. Contar cada cruce como una señal nueva
sobrerrepresentaría un único movimiento. `rearm_events` (`strategies/base.py`, líneas 220–235)
solo acepta un nuevo evento largo si %K ha pasado por encima de `rearm_level` (50) desde el
último aceptado.

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.indicators import crossover, stoch_rsi
from bybit_quant_lab.strategies.base import rearm_events

datos = generate_synthetic_ohlcv(bars=3000, seed=7)
st = stoch_rsi(datos["close"])
k, d = st["k"], st["d"]
crudos = crossover(k, d) & (k.shift(1) < 20) & (datos["close"] > datos["open"])
rearmados = rearm_events(crudos, k > 50)
print(
    "cruces alcistas en zona extrema:",
    int(crudos.sum()),
    "| tras el rearmado:",
    int(rearmados.sum()),
)
```
*Salida real:*

```text
cruces alcistas en zona extrema: 156 | tras el rearmado: 95
```

**Parámetros** (líneas 25–45): 14/14/3/3, zonas 20/80, rearmado en 50, objetivo 1,5R, máximo 24
velas y enfriamiento de 3.

**Pruebas específicas.** `test_stoch_rsi_counts_one_signal_per_move` (comprueba que entre dos
entradas largas %K superó el nivel de rearmado), `test_rearm_events_deduplicates`.

**Limitaciones.** Es la estrategia con más operaciones en los datos sintéticos, y por tanto la más
expuesta a los **costes**. Cuatro parámetros de suavizado y tres niveles dan muchas combinaciones
posibles: un riesgo alto de sobreajuste si se optimizan todos.

---

## 8.10 ADX + DI Directional System (`adx_di`)

**Hipótesis.** Cuando la tendencia es fuerte (ADX alto), su dirección la marca el diferencial
entre +DI y −DI.

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | **transición** a: ADX ≥ `adx_threshold` (25) y +DI − (−DI) > `di_margin` (2) |
| Entrada corta | Transición a: ADX ≥ 25 y −DI − (+DI) > 2 |
| Salida larga | +DI < −DI, **o** ADX < `adx_exit` (20) si `exit_on_weak_trend` |
| Salida corta | Espejo |

**Comportamiento con fuerza insuficiente.** Con ADX < 25 no se abre nada. Una posición abierta se
cierra si el ADX cae por debajo de 20. La diferencia entre 25 (entrar) y 20 (salir) es una
**histéresis**: evita que un ADX que oscila alrededor de 25 provoque entradas y salidas en cada
vela.

**Código.**

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/adx_di.py` · líneas 53–71

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        a = adx(data, p.adx_period)
        strong = a["adx"] >= p.adx_threshold
        if p.require_adx_rising:
            strong &= a["adx"] > a["adx"].shift(1)
        spread = a["plus_di"] - a["minus_di"]
        bull = strong & (spread > p.di_margin)
        bear = strong & (spread < -p.di_margin)
        weak = a["adx"] < p.adx_exit if p.exit_on_weak_trend else pd.Series(False, index=a.index)
        bull_edge = bull & ~bull.shift(1, fill_value=False)
        bear_edge = bear & ~bear.shift(1, fill_value=False)
        return Events(
            long_entry=bull_edge,
            short_entry=bear_edge,
            long_exit=(spread < 0) | weak,
            short_exit=(spread > 0) | weak,
            conviction=(a["adx"] / 50).clip(0, 1),
        )
```
<!-- fmt: on -->

- **63–64:** los eventos de entrada son **transiciones** (`bull` y no `bull` en la vela anterior),
  no niveles.

**Anatomía de una señal real:**

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.indicators import adx
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=3000, seed=7)
a = adx(datos, 14)
s = create_strategy("adx_di").generate_signals(datos)["signal"]
tabla = pd.DataFrame({"ADX": a["adx"], "+DI": a["plus_di"], "-DI": a["minus_di"], "senal": s})
for lado in (1, -1):
    t = int(((s == lado) & (s.shift(1, fill_value=0) != lado)).to_numpy().argmax())
    print("primera entrada", "LARGA" if lado == 1 else "CORTA", "en la vela", t)
    print(tabla.iloc[t - 1 : t + 1].round(1).to_string())
print("velas en posición con ADX < 20:", int(((s != 0) & (a["adx"] < 20)).sum()))
```
*Salida real:*

```text
primera entrada LARGA en la vela 44
                            ADX   +DI   -DI  senal
open_time                                         
2023-01-02 19:00:00+00:00  30.3  14.0  19.6     -1
2023-01-02 20:00:00+00:00  28.5  19.2  17.1      1
primera entrada CORTA en la vela 27
                            ADX   +DI   -DI  senal
open_time                                         
2023-01-02 02:00:00+00:00   NaN  16.4  31.9      0
2023-01-02 03:00:00+00:00  37.4  15.2  33.4     -1
velas en posición con ADX < 20: 0
```

Lectura de la salida:

- **Vela 27 (CORTA).** En la vela 26 el ADX todavía es `NaN` (calentamiento de los dos
  suavizados de Wilder). En la 27 aparece por primera vez: 37,4 ≥ 25 y −DI − (+DI) =
  33,4 − 15,2 = 18,2 > 2. `bear` pasa de falso a verdadero, hay transición y se entra corto.
  Que la primera entrada coincida con el primer ADX válido es habitual: el `NaN` previo cuenta
  como "no `bear`", así que el primer valor fuerte siempre es una transición.
- **Vela 44 (LARGA).** No es una entrada desde FLAT, sino una **reversión**: la señal previa era
  −1. En la 44, +DI (19,2) supera a −DI (17,1) por 2,1 > 2 con ADX 28,5, y la regla 1 de
  `events_to_state` (`base.py`, líneas 203–206) cambia de −1 a +1 en la misma vela. Con
  `execution.allow_reversal: true` (valor por defecto, `configs/default.yaml` línea 27) el motor
  cierra el corto y abre el largo en la apertura de la vela 45 (Módulo X).
- **0 velas en posición con ADX < 20:** la salida por tendencia débil funciona en esta serie.

**Pruebas específicas.** `test_adx_no_entries_when_trend_weak` (toda entrada ocurre con ADX ≥
umbral y no hay posición con ADX < 20), `test_adx_long_in_strong_uptrend`.

**Limitaciones.** El ADX se retrasa (dos suavizados de Wilder); cuando confirma la tendencia, una
parte del movimiento ya ocurrió. Los umbrales 20/25 son convenciones.

---

## 8.11 Resumen crítico de las diez estrategias

| Estrategia | Tipo de hipótesis | Riesgo principal | Hallazgos de revisión |
|---|---|---|---|
| volume_spike | Participación + dirección | Muy pocas operaciones | Filtro implícito por la EMA de salida |
| obv_trend | Confirmación por volumen | Solapamiento con las de tendencia | Convicción arbitraria |
| vwap_deviation | Reversión **o** continuación | Sesión UTC convencional | — |
| ema_crossover | Tendencia | Retraso, señales en lateral | Pocas operaciones con filtros |
| donchian_breakout | Ruptura de tendencia | Rupturas falsas | Convicción siempre 1; `a.notna()` redundante |
| rsi_reversion | Reversión | Tendencias fuertes; costes | — |
| macd_momentum | Impulso | Retraso, lateral | `require_hist_rising` sin efecto |
| bollinger_reversion | Reversión | Caminar por la banda | — |
| stoch_rsi | Giro de corto plazo | Muchas operaciones y costes; sobreajuste | — |
| adx_di | Tendencia con fuerza | Retraso | — |

**Redundancia esperable.** Cinco de las diez estrategias (ema_crossover, donchian_breakout,
macd_momentum, adx_di y, en parte, obv_trend) apuestan por la **continuación de tendencias**;
cuatro (rsi_reversion, bollinger_reversion, stoch_rsi y vwap_deviation en modo reversión) por la
**reversión**. Combinarlas no suma diez opiniones independientes (Módulo IX).

### Comprobación final del módulo

La estrategia RSI genera `signal = 1` en la vela 52. El motor rechaza la entrada por la pausa
tras tres pérdidas. En la vela 53 la estrategia sigue en `signal = 1` y la pausa ya terminó.
¿Entra el motor en la vela 54?

**Respuesta:**

No. El motor solo entra en la **transición** de la señal a LONG (de 0 a 1 en la vela 52). La
entrada rechazada no se aplaza: en la vela 53 la señal sigue en 1, no hay transición, y el motor
no hace nada hasta que la estrategia pase por FLAT y vuelva a LONG. Es una regla de diseño del
motor (Módulo X), documentada en su cabecera.

<div style="page-break-before: always;"></div>

# Módulo IX. Combinación de estrategias y regímenes de mercado

Este módulo explica cómo el proyecto convierte las señales de varias estrategias en **una sola
señal**, cómo clasifica el mercado en regímenes y cómo mide si dos estrategias dicen lo mismo.
Todo el código está en `src/bybit_quant_lab/signals/` (tres archivos: `combiners.py`,
`regime.py`, `redundancy.py`) y en `Researcher.build_combinations`
(`src/bybit_quant_lab/validation/research.py`).

> **[Hecho]** Las combinaciones se han evaluado solo con datos sintéticos. Los números de este
> módulo describen el **comportamiento del código**, no la calidad de ninguna combinación.

---

## 9.0 Intuición: un comité de opiniones que no son independientes

Imagina un comité de diez personas que vota si conviene comprar. Si las diez leyeron el mismo
periódico, sus diez votos valen poco más que uno. El comité solo aporta algo si sus miembros
tienen **información distinta** y aciertan con alguna frecuencia.

Traducido al proyecto:

- Cada estrategia emite un **estado objetivo** por vela: +1 (largo), −1 (corto) o 0 (fuera).
- Una **combinación** cuenta esos estados con una regla (votación, consenso, pesos) y produce
  **otro estado objetivo** con el mismo formato.
- Si varias estrategias usan la misma información (por ejemplo, cinco de las diez siguen
  tendencias, Módulo VIII), sus votos están **correlacionados** y el consenso es más débil de lo
  que parece.

**[Diseño]** La combinación devuelve exactamente el mismo contrato de columnas que una
estrategia individual (`signal`, `conviction`, `stop_distance`, `take_profit_distance`,
`trailing_distance`). Por eso el motor no distingue entre una estrategia y una combinación.

<!-- fmt: off -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 1–29

```python
"""Combinación de señales de varias estrategias.

Entrada: un DataFrame de señales normalizadas por estrategia (mismo índice). Cada estrategia
emite su **estado** objetivo (-1/0/1); la combinación produce un nuevo estado objetivo con el
mismo contrato, de modo que el motor no distingue entre estrategia individual y combinación.

Modos:

``simple_vote``
    ``net = n_long - n_short``. LONG si ``net >= min_margin``; SHORT si ``net <= -min_margin``.
``weighted_vote``
    ``score = sum(w_i * s_i * c_i) / sum(w_i)`` (``c_i`` = convicción si ``use_conviction``,
    si no 1). LONG si ``score >= threshold``; SHORT si ``score <= -threshold``. Los pesos son
    configurables o se ajustan **solo** con datos de entrenamiento (``fit_weights``); un peso
    mayor no implica mayor capacidad predictiva.
``min_consensus``
    LONG si ``n_long >= min_votes`` (y SHORT análogo).
``category_consensus``
    Una categoría vota LONG si su voto neto interno es > 0. LONG si al menos ``min_categories``
    categorías distintas votan LONG.

Política de conflictos (``conflict_policy``): ``veto`` -> cualquier voto opuesto anula la señal
(FLAT); ``net`` -> se usa el resultado neto del modo. Las estrategias en FLAT o sin datos
(NaN) se consideran abstenciones.

Filtro de régimen (``regime_rules``): antes de votar, la señal de una estrategia se fuerza a
FLAT en las velas cuyo régimen no esté permitido. Reglas por nombre de estrategia, por
categoría o comodín ``*``; cada regla mapea dimensión -> valores permitidos.
"""
```
<!-- fmt: on -->

Términos que aparecen en esa cabecera:

- **Voto**: el estado de una estrategia en una vela. +1 cuenta como voto largo, −1 como voto
  corto y 0 (o dato ausente) como **abstención**.
- **`n_long` / `n_short`**: número de votos largos y cortos en una vela.
- **Voto neto** (`net`): `n_long − n_short`.
- **Umbral / margen**: cantidad mínima de apoyo para que la combinación tome posición.
- **Política de conflictos**: qué hacer cuando hay votos en ambas direcciones.

---

## 9.1 La configuración de una combinación

<!-- fmt: off -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 42–59

```python
class CombinationConfig(BaseModel):
    """Configuración de una combinación."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = "combo"
    mode: Literal["simple_vote", "weighted_vote", "min_consensus", "category_consensus"] = (
        "simple_vote"
    )
    members: list[str] | None = None
    min_margin: int = Field(2, ge=1)
    min_votes: int = Field(2, ge=1)
    min_categories: int = Field(2, ge=1)
    weights: dict[str, float] | None = None
    threshold: float = Field(0.3, gt=0, le=1)
    use_conviction: bool = False
    conflict_policy: Literal["veto", "net"] = "veto"
    regime_rules: dict[str, dict[str, list[str]]] | None = None
```
<!-- fmt: on -->

| Campo | Significado | Lo usa |
|---|---|---|
| `name` | Nombre del candidato en informes y registros | todos |
| `mode` | Regla de combinación | todos |
| `members` | Estrategias que votan (`None` = todas las disponibles) | todos |
| `min_margin` | Voto neto mínimo | `simple_vote` |
| `min_votes` | Votos mínimos en una dirección | `min_consensus` |
| `min_categories` | Categorías mínimas de acuerdo | `category_consensus` |
| `weights` | Peso por estrategia (`None` = se ajustan en entrenamiento) | `weighted_vote` |
| `threshold` | Puntuación mínima, en (0, 1] | `weighted_vote` |
| `use_conviction` | Multiplicar cada voto por su convicción | `weighted_vote` |
| `conflict_policy` | `veto` o `net` | todos |
| `regime_rules` | Regímenes permitidos por estrategia/categoría | todos |

**[Diseño]** `extra="forbid"` rechaza campos desconocidos: un error tipográfico en el YAML
(`min_vote` en lugar de `min_votes`) produce un error de validación en lugar de pasar
inadvertido. `frozen=True` impide modificar la configuración después de crearla; los ajustes
se hacen con `model_copy(update=...)`, que devuelve una copia nueva. Recuerda la limitación de
la sección 2.15: esa copia **no se vuelve a validar** (hallazgo B-06). `build_combinations` la usa
para pesos, umbrales y miembros; los valores que introduce (umbrales de 0,2 a 0,5, pesos no
negativos) cumplen las restricciones, pero nada lo comprueba en ese punto.

**Comprobación.** ¿Qué campo se ignora si `mode` es `min_consensus`?

**Respuesta:**

`min_margin`, `min_categories`, `weights`, `threshold` y `use_conviction`. Pydantic los acepta
(tienen valor por defecto), pero `combine_signals` no los lee en esa rama.

---

## 9.2 El flujo de `combine_signals`, línea a línea

<!-- fmt: off -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 86–110

```python
def combine_signals(
    frames: dict[str, pd.DataFrame],
    categories: dict[str, str],
    config: CombinationConfig,
    regime: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Combina señales individuales en un DataFrame con el contrato ``SIGNAL_COLUMNS``."""
    members = config.members or list(frames)
    missing = [m for m in members if m not in frames]
    if missing:
        raise KeyError(f"Estrategias no disponibles para la combinación: {missing}")
    if not members:
        raise ValueError("La combinación necesita al menos una estrategia")
    use = {m: frames[m] for m in members}
    index = next(iter(use.values())).index
    sig = _stack(use, "signal", index).fillna(0).astype(int)
    if config.regime_rules:
        if regime is None:
            raise ValueError("regime_rules requiere el DataFrame de régimen")
        sig = apply_regime_filter(sig, categories, regime, config.regime_rules)
    conv = _stack(use, "conviction", index).fillna(0.0)
    n_long = (sig > 0).sum(axis=1)
    n_short = (sig < 0).sum(axis=1)
    n = len(members)

```
<!-- fmt: on -->

- **93–98:** valida los miembros. Un nombre inexistente lanza `KeyError`; una lista vacía,
  `ValueError`.
- **100:** el índice de referencia es el de la **primera** estrategia. `_stack` (líneas 82–83)
  reindexa todas las demás a ese índice.
- **101:** `fillna(0)`: si a una estrategia le faltan velas, en esas velas **se abstiene**.
- **102–105:** el filtro de régimen se aplica **antes** de votar (sección 9.10).
- **106:** las convicciones, con 0 donde falten.
- **107–108:** `(sig > 0).sum(axis=1)` cuenta, fila a fila, cuántas columnas valen +1. El
  `axis=1` significa "a lo largo de las columnas" (Módulo V).

Después vienen las cuatro ramas (secciones 9.3–9.7) y el cierre común:

<!-- fmt: off -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 136–150

```python
    out_s = pd.Series(out, index=index).astype("int64")
    if config.conflict_policy == "veto":
        conflict = ((out_s > 0) & (n_short > 0)) | ((out_s < 0) & (n_long > 0))
        out_s[conflict] = 0
    result = empty_signal_frame(index)
    result["signal"] = out_s
    result["conviction"] = pd.Series(strength, index=index).clip(0, 1).where(out_s != 0, 0.0)
    for col in SIGNAL_COLUMNS[2:]:
        values = _stack(use, col, index)
        agree = sig.eq(out_s, axis=0) & (out_s != 0).to_numpy()[:, None]
        result[col] = values.where(agree).median(axis=1, skipna=True)
    no_stop = result["stop_distance"].isna() | (result["stop_distance"] <= 0)
    result.loc[no_stop, "signal"] = 0
    result.loc[result["signal"] == 0, "conviction"] = 0.0
    return result
```
<!-- fmt: on -->

- **137–139:** política `veto` (sección 9.4).
- **142:** la convicción de la combinación es la **fuerza del acuerdo** (`strength`), recortada a
  [0, 1] y a 0 cuando la combinación está fuera.
- **143–146:** stops, take profit y trailing salen de la **mediana** de los miembros que
  **coinciden** con la dirección final (sección 9.8).
- **147–149:** sin stop válido no hay posición (misma regla que en las estrategias individuales,
  Módulo VIII, sección 8.0).

---

## 9.3 Ejemplo de referencia construido a mano

Para todo el módulo se usa el ejemplo de `tests/unit/test_signals.py`: cuatro estrategias
ficticias (`a`, `b`, `c`, `d`) y seis velas.

<!-- fmt: off -->
`tests/unit/test_signals.py` · líneas 20–37

```python
IDX = pd.date_range("2024-01-01", periods=6, freq="1h", tz="UTC")
CATS = {"a": "volume", "b": "trend", "c": "indicator", "d": "indicator"}


def _frame(values: list[int], stop: float = 2.0, conv: float = 1.0) -> pd.DataFrame:
    f = empty_signal_frame(IDX)
    f["signal"] = values
    f["conviction"] = [conv if v else 0.0 for v in values]
    f["stop_distance"] = stop
    return f


FRAMES = {
    "a": _frame([1, 1, 1, 0, -1, 1], stop=1.0),
    "b": _frame([1, 1, 0, 0, -1, -1], stop=3.0),
    "c": _frame([1, -1, 0, 0, -1, 0], stop=5.0),
    "d": _frame([0, 0, 1, 1, 0, 0], stop=7.0),
}
```
<!-- fmt: on -->

Tabla de votos (categorías: `a`=volume, `b`=trend, `c` y `d`=indicator):

| Vela | a | b | c | d | `n_long` | `n_short` | `net` |
|---|---|---|---|---|---|---|---|
| 0 | +1 | +1 | +1 | 0 | 3 | 0 | +3 |
| 1 | +1 | +1 | −1 | 0 | 2 | 1 | +1 |
| 2 | +1 | 0 | 0 | +1 | 2 | 0 | +2 |
| 3 | 0 | 0 | 0 | +1 | 1 | 0 | +1 |
| 4 | −1 | −1 | −1 | 0 | 0 | 3 | −3 |
| 5 | +1 | −1 | 0 | 0 | 1 | 1 | 0 |

Las secciones siguientes calculan a mano cada modo sobre esta tabla, y un único bloque
ejecutable al final (sección 9.7) lo comprueba con el código real.

---

## 9.4 Votación simple y política de conflictos

**Regla.** Con `m = min_margin`:

```text
señal = +1  si  net ≥  m
señal = −1  si  net ≤ −m
señal =  0  en otro caso
```

<!-- fmt: off -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 111–114

```python
    if config.mode == "simple_vote":
        net = n_long - n_short
        out = np.where(net >= config.min_margin, 1, np.where(net <= -config.min_margin, -1, 0))
        strength = net.abs() / n
```
<!-- fmt: on -->

`np.where(cond, a, b)` elige `a` donde la condición es verdadera y `b` donde no; anidado,
implementa el "si / si no si / si no". `strength = |net| / n` es la fracción de miembros que
forman la mayoría neta.

**Cálculo con `m = 2`.** `net` = [+3, +1, +2, +1, −3, 0] → señal antes de conflictos:
[+1, 0, +1, 0, −1, 0].

**Política de conflictos.**

- `net`: se queda con el resultado anterior.
- `veto`: si la combinación quedó larga pero **algún** miembro vota corto (o al revés), la
  señal pasa a 0 (líneas 137–139).

Con `m = 2` no cambia nada: en las velas 0 y 2 nadie vota corto y en la 4 nadie vota largo. El
resultado es [+1, 0, +1, 0, −1, 0] en ambos casos.

**Cálculo con `m = 1`.** Antes de conflictos: [+1, +1, +1, +1, −1, 0].

- Con `net`: [+1, +1, +1, +1, −1, 0].
- Con `veto`: en la vela 1 la estrategia `c` vota −1 → se anula. Resultado:
  [+1, 0, +1, +1, −1, 0].

**Equivalencia que detectó la auditoría (B-01).** Con `veto`, la condición de entrar largo es
`net ≥ m` **y** `n_short = 0`. Si `n_short = 0`, entonces `net = n_long`, así que la condición es
`n_long ≥ m` y `n_short = 0`, que es exactamente `min_consensus` con `min_votes = m` y `veto`.
Las dos combinaciones de la configuración original (`vote_all`, margen 3, y `consensus_3`) eran
**la misma regla con dos nombres**. Eso inflaba el número de pruebas (Módulo XIII, DSR) sin
aportar información. Corrección en `a50ac62`: `vote_all` usa `conflict_policy: net`.

`configs/strategies.yaml` · líneas 152–162

```yaml
combinations:
  - name: vote_all
    mode: simple_vote
    min_margin: 3
    conflict_policy: net         # con 'veto' sería idéntica a consensus_3 (auditoría L1)
  - name: weighted_train
    mode: weighted_vote          # pesos = Sharpe de entrenamiento (no negativos)
    use_conviction: false
  - name: consensus_3
    mode: min_consensus
    min_votes: 3
```

La prueba que documenta la equivalencia y la que impide repetir el error:

<!-- fmt: off -->
`tests/unit/test_audit_statistics.py` · líneas 157–182

```python
def test_configured_combinations_are_not_equivalent() -> None:
    import yaml

    raw = yaml.safe_load((ROOT / "configs/strategies.yaml").read_text())["combinations"]
    cfgs = [CombinationConfig.model_validate(c) for c in raw]

    def key(c: CombinationConfig) -> tuple | None:
        # simple_vote(margen k, veto) ≡ min_consensus(k, veto): n_dir ≥ k y n_opuesto = 0.
        if c.conflict_policy == "veto" and c.members is None and not c.regime_rules:
            if c.mode == "simple_vote":
                return ("veto", c.min_margin)
            if c.mode == "min_consensus":
                return ("veto", c.min_votes)
        return None

    keys = [k for k in map(key, cfgs) if k is not None]
    assert len(keys) == len(set(keys)), "dos combinaciones configuradas son idénticas"


def test_simple_vote_veto_equals_min_consensus_veto(synth: pd.DataFrame) -> None:
    # Documenta la equivalencia matemática que motivó el cambio de configuración.
    frames = {n: create_strategy(n).generate_signals(synth) for n in available_strategies()}
    cats = {n: create_strategy(n).category.value for n in frames}
    a = combine_signals(frames, cats, CombinationConfig(mode="simple_vote", min_margin=3))
    b = combine_signals(frames, cats, CombinationConfig(mode="min_consensus", min_votes=3))
    pd.testing.assert_series_equal(a["signal"], b["signal"])
```
<!-- fmt: on -->

**[Discrepancia]** Si `configs/strategies.yaml` no tiene sección `combinations`, la CLI crea
una combinación por defecto llamada también `vote_all`, pero con la política por defecto
(`veto`), es decir, la versión anterior a la corrección:

<!-- fmt: off -->
`src/bybit_quant_lab/cli.py` · líneas 94–98

```python
def _combos(args: argparse.Namespace) -> list[CombinationConfig]:
    raw = _strategies_file(args).get("combinations") or []
    if not raw:
        return [CombinationConfig(name="vote_all", mode="simple_vote", min_margin=3)]
    return [CombinationConfig.model_validate(c) for c in raw]
```
<!-- fmt: on -->

Con el YAML del repositorio esa rama no se ejecuta.

**Error común.** Pensar que `veto` es "más prudente y por tanto mejor". Es más restrictivo:
reduce operaciones, y con menos operaciones las métricas son más inciertas (Módulo VI).

---

## 9.5 Consenso mínimo

**Regla.** Con `k = min_votes`: largo si `n_long ≥ k` y **no** `n_short ≥ k`; corto en espejo.

<!-- fmt: off -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 123–126

```python
    elif config.mode == "min_consensus":
        long_ok, short_ok = n_long >= config.min_votes, n_short >= config.min_votes
        out = np.where(long_ok & ~short_ok, 1, np.where(short_ok & ~long_ok, -1, 0))
        strength = pd.Series(np.maximum(n_long, n_short) / n, index=index)
```
<!-- fmt: on -->

La condición `& ~short_ok` resuelve el empate extremo (k votos en cada dirección → 0).

**Cálculo con `k = 3`.** `n_long ≥ 3` solo en la vela 0; `n_short ≥ 3` solo en la vela 4 →
[+1, 0, 0, 0, −1, 0].

**Cálculo con `k = 2` y `veto`.** `n_long ≥ 2` en las velas 0, 1 y 2; `n_short ≥ 2` en la 4 →
[+1, +1, +1, 0, −1, 0]. El veto anula la vela 1 (voto corto de `c`) →
[+1, 0, +1, 0, −1, 0].

**Diferencia con la votación simple (`net`).** `min_consensus` no resta los votos contrarios:
con 3 largos y 2 cortos y `k = 3`, entra largo con `net` aunque el voto neto sea solo +1.

---

## 9.6 Votación ponderada y ajuste de pesos

**Fórmula.** Con pesos `w_i ≥ 0`, estados `s_i ∈ {−1, 0, 1}` y factor `c_i` (la convicción si
`use_conviction`, si no 1):

```text
score = Σ w_i · s_i · c_i / Σ w_i        (score ∈ [−1, 1])
señal = +1 si score ≥ θ,  −1 si score ≤ −θ,  0 en otro caso       (θ = threshold)
```

<!-- fmt: off -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 115–122

```python
    elif config.mode == "weighted_vote":
        w = pd.Series({m: (config.weights or {}).get(m, 1.0) for m in members}, dtype=float)
        if (w < 0).any() or w.sum() <= 0:
            raise ValueError("Los pesos deben ser no negativos y sumar > 0")
        factor = conv if config.use_conviction else pd.DataFrame(1.0, index=index, columns=members)
        score = (sig * factor).mul(w, axis=1).sum(axis=1) / w.sum()
        out = np.where(score >= config.threshold, 1, np.where(score <= -config.threshold, -1, 0))
        strength = score.abs()
```
<!-- fmt: on -->

- **116:** un miembro sin peso explícito recibe 1.
- **117–118:** pesos negativos o suma no positiva → `ValueError`.
- **120:** `.mul(w, axis=1)` multiplica cada columna por su peso (alineando por nombre).

**Cálculo a mano** (test `test_weighted_vote_uses_weights_and_threshold`): pesos a=3, b=1, c=0,
d=0; θ = 0,5; política `net`. Σw = 4, así que `score = (3·a + 1·b) / 4`:

| Vela | a | b | score | señal |
|---|---|---|---|---|
| 0 | +1 | +1 | (3+1)/4 = 1,00 | +1 |
| 1 | +1 | +1 | 1,00 | +1 |
| 2 | +1 | 0 | 3/4 = 0,75 | +1 |
| 3 | 0 | 0 | 0 | 0 |
| 4 | −1 | −1 | −1,00 | −1 |
| 5 | +1 | −1 | (3−1)/4 = 0,50 | +1 (0,50 ≥ 0,5) |

La vela 5 está justo en el umbral: el `>=` la convierte en larga. Con θ = 0,51 sería 0.

### Cómo se ajustan los pesos (`fit_weights`)

<!-- fmt: off -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 153–169

```python
def fit_weights(
    train_returns: dict[str, pd.Series], method: Literal["equal", "train_sharpe"] = "train_sharpe"
) -> dict[str, float]:
    """Ajusta pesos con retornos por vela del período de **entrenamiento** exclusivamente.

    ``train_sharpe``: peso = max(Sharpe no anualizado, 0); si todos son 0 se usan pesos iguales.
    """
    if method == "equal":
        return dict.fromkeys(train_returns, 1.0)
    weights = {}
    for name, r in train_returns.items():
        std = float(r.std(ddof=1)) if len(r) > 1 else 0.0
        weights[name] = max(float(r.mean()) / std, 0.0) if std > 0 else 0.0
    total = sum(weights.values())
    if total <= 0:
        return dict.fromkeys(train_returns, 1.0)
    return {k: v / total for k, v in weights.items()}
```
<!-- fmt: on -->

**Intuición.** Cada estrategia recibe un peso proporcional a su Sharpe por vela en
entrenamiento; las de Sharpe negativo reciben 0. Luego se normaliza para que sumen 1.

**Fórmula.** Para la estrategia `i` con retornos por vela `r_i` en entrenamiento:

```text
SR_i = media(r_i) / desv(r_i)        (ddof=1, sin anualizar)
w_i  = max(SR_i, 0) / Σ_j max(SR_j, 0)
```

Si todas tienen `SR ≤ 0`, se usan pesos iguales (líneas 167–168): no hay información para
preferir a ninguna.

**Ejemplo** (test `test_fit_weights_uses_only_given_returns`): `good` = [0,01, 0,02, 0, 0,01]
tiene media 0,01 y desviación > 0 → SR > 0; `bad` tiene media negativa → peso 0. Tras normalizar,
`good` = 1,0 y `bad` = 0.

**[Diseño]** El peso refleja el comportamiento **pasado** en entrenamiento. Un peso alto no
implica capacidad predictiva futura (lo dice la propia cabecera, líneas 14–15).

### Dónde se usan pesos y umbral: `build_combinations`

<!-- fmt: off -->
`src/bybit_quant_lab/validation/research.py` · líneas 196–242

```python
    def build_combinations(
        self, singles: dict[str, Candidate], combos: list[CombinationConfig]
    ) -> tuple[dict[str, Candidate], dict[str, Any]]:
        """Construye combinaciones; redundancia, pesos y umbrales se ajustan con entrenamiento."""
        tr = self.segments["train"]
        frames = {n: c.signals for n, c in singles.items()}
        cats = {n: create_strategy(n).category.value for n in singles}
        train_sig = pd.DataFrame(
            {n: f["signal"].iloc[tr.start_pos : tr.end_pos + 1] for n, f in frames.items()}
        )
        corr = signal_correlation(train_sig)
        out: dict[str, Candidate] = {}
        info: dict[str, Any] = {"train_correlation": corr}
        for combo in combos:
            cfg = combo
            if cfg.members is None and cfg.name.startswith("dedup"):
                kept, dropped = select_non_redundant(corr.fillna(0), 0.7)
                cfg = cfg.model_copy(update={"members": kept})
                info["dedup"] = {"kept": kept, "dropped": dropped}
            if cfg.mode == "weighted_vote" and cfg.weights is None:
                members = cfg.members or list(frames)
                train_rets = {
                    n: bar_returns(r.equity["equity"], r.initial_capital)
                    for n in members
                    for r in [self.simulate(singles[n], tr, record=False)]
                }
                cfg = cfg.model_copy(update={"weights": fit_weights(train_rets)})
                info.setdefault("weights", {})[cfg.name] = cfg.weights
                # Umbral elegido en ENTRENAMIENTO (rejilla pequeña y registrada). Validación
                # queda reservada para seleccionar candidatos sin doble uso de los datos.
                best_t, best_s = cfg.threshold, float("-inf")
                for t in (0.2, 0.3, 0.4, 0.5):
                    trial = cfg.model_copy(update={"threshold": t})
                    c = Candidate(
                        f"{cfg.name}@{t}",
                        "combo_trial",
                        combine_signals(frames, cats, trial, self.regime),
                        {},
                    )
                    s = self._score(self.metrics(self.simulate(c, tr)))
                    if s > best_s:
                        best_t, best_s = t, s
                cfg = cfg.model_copy(update={"threshold": best_t})
                info.setdefault("thresholds", {})[cfg.name] = best_t
            sig = combine_signals(frames, cats, cfg, self.regime)
            out[cfg.name] = Candidate(cfg.name, "combination", sig, cfg.model_dump())
        return out, info
```
<!-- fmt: on -->

- **203–206:** la correlación de señales se calcula **solo** con las velas de entrenamiento.
- **211–214:** las combinaciones cuyo nombre empieza por `dedup` y no tienen miembros reciben
  los miembros "no redundantes" (sección 9.11).
- **215–223:** si `weighted_vote` no trae pesos, se simula cada miembro en entrenamiento y se
  ajustan con `fit_weights`.
- **226–239:** se prueba una rejilla de cuatro umbrales (0,2; 0,3; 0,4; 0,5) **en entrenamiento**
  y se elige el de mejor puntuación (`_score`, líneas 188–193: la métrica de selección, o −∞
  con menos de `min_trades_selection` operaciones). Cada ensayo se registra como
  `combo_trial`.

### Historia de una corrección: el umbral se elegía con validación (M-01)

Antes de la auditoría, la línea que puntuaba cada umbral simulaba en **validación**:

```text
-                    s = self._score(self.metrics(self.simulate(c, self.segments["validation"])))
+                    s = self._score(self.metrics(self.simulate(c, tr)))
```

(Extracto de `git show a50ac62 -- src/bybit_quant_lab/validation/research.py`.)

**Por qué era un error.** La validación se usa después para **seleccionar** candidatos. Si el
umbral se elige mirando validación, la combinación ponderada llega a la selección con una
ventaja: su mejor versión ya se escogió con esos mismos datos (doble uso del segmento,
Módulo XIII). La prueba que lo impide comprueba que todos los ensayos `combo_trial` están en
`train`:

<!-- fmt: off -->
`tests/unit/test_audit_statistics.py` · líneas 148–154

```python
def test_combination_thresholds_not_tuned_on_validation(researcher: Researcher) -> None:
    combos = [CombinationConfig(name="weighted", mode="weighted_vote")]
    researcher.run_comparison(combos, ["ema_crossover", "adx_di", "macd_momentum"])
    trials = [r for r in researcher.log.records() if r.get("candidate_kind") == "combo_trial"]
    assert trials, "los ensayos de umbral deben registrarse"
    # El umbral se elige en entrenamiento; validación queda limpia para la selección.
    assert {r["segment"] for r in trials} == {"train"}
```
<!-- fmt: on -->

**[Discrepancia] Dos textos quedaron desactualizados tras la corrección.** El código y
`docs/methodology.md` (punto 3 de la sección 4) dicen "entrenamiento", pero:

- la cabecera del módulo `research.py` sigue diciendo "validación":

<!-- fmt: off -->
`src/bybit_quant_lab/validation/research.py` · líneas 7–8

```python
2. Redundancia y pesos de combinación se ajustan **solo con entrenamiento**; los umbrales de
   la votación ponderada se eligen **solo con validación**.
```
<!-- fmt: on -->

- y el informe HTML rotula esas decisiones como "validación (umbrales)":

<!-- fmt: off -->
`src/bybit_quant_lab/reporting/html.py` · líneas 279–282

```python
    secs[-1].pre = (
        "Decisiones de combinación ajustadas en entrenamiento (pesos, redundancia) y "
        "validación (umbrales):\n"
        + json.dumps(to_jsonable(out.redundancy), indent=2, ensure_ascii=False)
```
<!-- fmt: on -->

Manda el código: el umbral se ajusta en entrenamiento. Corregir esos dos textos es un ejercicio
del Módulo XVI.

### Hallazgo: los miembros con peso 0 siguen influyendo

**[Hecho, verificado con el código]** En `weighted_train` (YAML, líneas 157–159) la política de
conflictos es la de por defecto, `veto`. El veto (líneas 137–139) usa `n_short`/`n_long`, que
cuentan los votos de **todos** los miembros, incluidos los que `fit_weights` dejó con peso 0.
Además, la mediana del stop (líneas 143–146) incluye a los miembros con peso 0 que coinciden en
dirección.

Medición con datos sintéticos (6000 velas, semilla 42, parámetros del YAML):

*Ejemplo ejecutable:*

```python
import yaml

from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import CombinationConfig, combine_signals
from bybit_quant_lab.strategies import available_strategies
from bybit_quant_lab.validation.research import Researcher

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
params = load_strategy_params("configs/strategies.yaml")
r = Researcher(datos, "BTCUSDT", "1h", load_config(), strategy_params=params)
combos = [
    CombinationConfig.model_validate(c)
    for c in yaml.safe_load(open("configs/strategies.yaml"))["combinations"]
]
singles = {n: r.strategy_candidate(n) for n in available_strategies()}
cands, info = r.build_combinations(singles, combos)

w = info["weights"]["weighted_train"]
print("pesos (entrenamiento):", {k: round(v, 3) for k, v in w.items() if v > 0})
print("con peso 0:", sorted(k for k, v in w.items() if v == 0))
print("umbral elegido en entrenamiento:", info["thresholds"]["weighted_train"])

cfg = CombinationConfig.model_validate(cands["weighted_train"].params)
frames = {n: c.signals for n, c in singles.items()}
cats = {n: "x" for n in frames}
todos = combine_signals(frames, cats, cfg)["signal"]
activos = [n for n, v in w.items() if v > 0]
solo = combine_signals(
    frames, cats, cfg.model_copy(update={"members": activos, "weights": {n: w[n] for n in activos}})
)["signal"]
print("política:", cfg.conflict_policy)
print("velas en posición, 10 miembros:", int((todos != 0).sum()))
print("velas en posición, solo miembros con peso > 0:", int((solo != 0).sum()))
```
*Salida real:*

```text
pesos (entrenamiento): {'adx_di': 0.162, 'donchian_breakout': 0.316, 'macd_momentum': 0.284, 'obv_trend': 0.238}
con peso 0: ['bollinger_reversion', 'ema_crossover', 'rsi_reversion', 'stoch_rsi', 'volume_spike', 'vwap_deviation']
umbral elegido en entrenamiento: 0.5
política: veto
velas en posición, 10 miembros: 307
velas en posición, solo miembros con peso > 0: 2483
```

Interpretación: seis estrategias con peso 0 no suman nada a la puntuación, pero con `veto`
**bloquean** la mayor parte de las posiciones. "Peso 0" no significa "excluida". Es una
interacción entre dos decisiones de diseño razonables por separado, no un error de cálculo; se
recoge como pendiente en el Módulo XVII.

**Comprobación.** Con pesos a=3, b=1, c=0, d=0, θ=0,5 y política `veto`, ¿qué señal da la
vela 1 del ejemplo de referencia?

**Respuesta:**

0. El `score` es 1,0 (≥ 0,5), pero `c` vota −1. Aunque su peso es 0, `n_short = 1 > 0` y el veto
anula la señal larga.

---

## 9.7 Consenso por categorías

**Intuición.** En lugar de contar estrategias, se cuentan **familias**: dos estrategias de
volumen que coinciden valen como una categoría, no como dos votos.

<!-- fmt: off -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 127–134

```python
    else:
        cats = pd.Series({m: categories.get(m, m) for m in members})
        cat_net = sig.T.groupby(cats).sum().T
        c_long, c_short = (cat_net > 0).sum(axis=1), (cat_net < 0).sum(axis=1)
        long_ok = c_long >= config.min_categories
        short_ok = c_short >= config.min_categories
        out = np.where(long_ok & ~short_ok, 1, np.where(short_ok & ~long_ok, -1, 0))
        strength = pd.Series(np.maximum(c_long, c_short) / max(cats.nunique(), 1), index=index)
```
<!-- fmt: on -->

- **128:** asigna a cada miembro su categoría (`volume`, `trend` o `indicator`).
- **129:** `sig.T.groupby(cats).sum().T` suma los estados **dentro de cada categoría**. Se
  transpone porque `groupby` agrupa filas; tras transponer, las estrategias son filas. El
  resultado es una columna por categoría con su voto neto interno.
- **130–133:** una categoría vota largo si su neto es > 0; la combinación entra si al menos
  `min_categories` categorías coinciden.

**Cálculo con `min_categories = 2`:**

| Vela | volume (a) | trend (b) | indicator (c+d) | categorías L / C | antes de veto | final (`veto`) |
|---|---|---|---|---|---|---|
| 0 | +1 | +1 | +1 | 3 / 0 | +1 | +1 |
| 1 | +1 | +1 | −1 | 2 / 1 | +1 | 0 (`c` corto) |
| 2 | +1 | 0 | +1 | 2 / 0 | +1 | +1 |
| 3 | 0 | 0 | +1 | 1 / 0 | 0 | 0 |
| 4 | −1 | −1 | −1 | 0 / 3 | −1 | −1 |
| 5 | +1 | −1 | 0 | 1 / 1 | 0 | 0 |

Resultado [+1, 0, +1, 0, −1, 0]. Comprobación de los cálculos a mano de 9.4–9.7 con el código:

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.signals import CombinationConfig, combine_signals
from bybit_quant_lab.strategies.base import empty_signal_frame

idx = pd.date_range("2024-01-01", periods=6, freq="1h", tz="UTC")


def marco(valores, stop):
    f = empty_signal_frame(idx)
    f["signal"] = valores
    f["conviction"] = [1.0 if v else 0.0 for v in valores]
    f["stop_distance"] = stop
    return f


frames = {
    "a": marco([1, 1, 1, 0, -1, 1], 1.0),
    "b": marco([1, 1, 0, 0, -1, -1], 3.0),
    "c": marco([1, -1, 0, 0, -1, 0], 5.0),
    "d": marco([0, 0, 1, 1, 0, 0], 7.0),
}
cats = {"a": "volume", "b": "trend", "c": "indicator", "d": "indicator"}
casos = {
    "simple m=2 veto": CombinationConfig(mode="simple_vote", min_margin=2),
    "simple m=1 net": CombinationConfig(mode="simple_vote", min_margin=1, conflict_policy="net"),
    "simple m=1 veto": CombinationConfig(mode="simple_vote", min_margin=1),
    "consenso k=3": CombinationConfig(mode="min_consensus", min_votes=3),
    "consenso k=2 veto": CombinationConfig(mode="min_consensus", min_votes=2),
    "ponderada net": CombinationConfig(
        mode="weighted_vote",
        weights={"a": 3, "b": 1, "c": 0, "d": 0},
        threshold=0.5,
        conflict_policy="net",
    ),
    "ponderada veto": CombinationConfig(
        mode="weighted_vote",
        weights={"a": 3, "b": 1, "c": 0, "d": 0},
        threshold=0.5,
    ),
    "categorías 2": CombinationConfig(mode="category_consensus", min_categories=2),
}
for nombre, cfg in casos.items():
    out = combine_signals(frames, cats, cfg)
    print(f"{nombre:18s} {out['signal'].tolist()}")
```
*Salida real:*

```text
simple m=2 veto    [1, 0, 1, 0, -1, 0]
simple m=1 net     [1, 1, 1, 1, -1, 0]
simple m=1 veto    [1, 0, 1, 1, -1, 0]
consenso k=3       [1, 0, 0, 0, -1, 0]
consenso k=2 veto  [1, 0, 1, 0, -1, 0]
ponderada net      [1, 1, 1, 0, -1, 1]
ponderada veto     [1, 0, 1, 0, -1, 0]
categorías 2       [1, 0, 1, 0, -1, 0]
```

**[Limitación] Categorías heterogéneas (M-05, pendiente).** La categoría `indicator` mezcla
estrategias de tendencia (`macd_momentum`, `adx_di`) y de reversión (`rsi_reversion`,
`bollinger_reversion`, `stoch_rsi`). En una vela, el neto de `indicator` puede ser 0 porque
una estrategia de tendencia y otra de reversión se cancelan, o +1 por pura información de
tendencia, que ya cuenta en la categoría `trend`. El consenso "entre dos categorías" puede ser,
en la práctica, la misma hipótesis contada dos veces. La clasificación en tres categorías viene
del encargo original y no se cambió (`docs/audit_report.md`, M-05).

---

## 9.8 Stops, take profit y convicción de una combinación

<!-- fmt: off -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 143–146

```python
    for col in SIGNAL_COLUMNS[2:]:
        values = _stack(use, col, index)
        agree = sig.eq(out_s, axis=0) & (out_s != 0).to_numpy()[:, None]
        result[col] = values.where(agree).median(axis=1, skipna=True)
```
<!-- fmt: on -->

- `agree` es una matriz booleana: verdadero donde el miembro vota **igual** que la combinación y
  la combinación no está en 0. `sig.eq(out_s, axis=0)` compara cada columna con la serie
  `out_s` fila a fila.
- `values.where(agree)` deja `NaN` donde el miembro no coincide; `median(skipna=True)` calcula la
  mediana de los que coinciden.

**Ejemplo** (test `test_stop_is_median_of_agreeing_members`): en la vela 0 coinciden `a`, `b`
y `c` con stops 1, 3 y 5 → mediana 3. En la vela 2 coinciden `a` y `d` (stops 1 y 7) → con dos
valores la mediana es su media, 4.

**Por qué la mediana.** Es robusta: un miembro con un stop desproporcionado no lo arrastra.

**[Hecho] Matiz del take profit y el trailing.** Con `skipna=True`, si solo uno de los miembros
coincidentes define take profit, la combinación usa **ese** take profit. Una regla de salida de
una sola estrategia puede gobernar toda la posición combinada.

**[Hecho] La convicción de la combinación es informativa.** `strength` se guarda en la
columna `conviction` y el motor la copia a cada operación (`backtesting/engine.py`, líneas 98
y 200), pero **ningún módulo de riesgo la usa** para dimensionar: una búsqueda de
`conviction` en `src/bybit_quant_lab/risk/` no devuelve resultados. El tamaño depende del stop
y del riesgo por operación (Módulo XI). `use_conviction` solo cambia la **puntuación** de
`weighted_vote`, no el tamaño.

---

## 9.9 Regímenes de mercado: qué son y cómo se calculan

**Intuición.** Un **régimen** es una etiqueta que describe el estado del mercado en una vela:
"hay tendencia o no", "la volatilidad es alta o baja", "hay poco volumen". Sirve para dos
cosas: desglosar resultados (¿la estrategia gana solo en tendencia?) y filtrar estrategias (no
usar reversión a la media en plena tendencia).

<!-- fmt: off -->
`src/bybit_quant_lab/signals/regime.py` · líneas 1–13

```python
"""Clasificación causal del régimen de mercado.

Tres dimensiones independientes, calculadas solo con datos hasta cada vela:

* ``trend``: ``trend`` si ``ADX >= adx_trend``, si no ``range``.
* ``volatility``: ``high_vol`` si el percentil del ATR % respecto a las ``vol_window`` velas
  anteriores es ``>= high_vol_pct``; ``low_vol`` si es ``<= low_vol_pct``; si no ``normal_vol``.
* ``liquidity``: ``low_liq`` si el volumen relativo a la mediana de las ``liq_window`` velas
  anteriores es ``< low_liq_ratio``; si no ``normal_liq``. Es una aproximación por volumen: sin
  datos de libro de órdenes no se mide la liquidez real.

Durante el calentamiento las dimensiones valen ``unknown``.
"""
```
<!-- fmt: on -->

<!-- fmt: off -->
`src/bybit_quant_lab/signals/regime.py` · líneas 41–60

```python
def classify_regime(data: pd.DataFrame, config: RegimeConfig | None = None) -> pd.DataFrame:
    """Devuelve columnas ``trend``, ``volatility``, ``liquidity`` y ``label`` (combinada)."""
    cfg = config or RegimeConfig()
    a = adx(data, cfg.adx_period)["adx"]
    trend = np.where(a.isna(), "unknown", np.where(a >= cfg.adx_trend, "trend", "range"))
    atr_pct = atr(data, cfg.atr_period) / data["close"]
    pct = rolling_percentile(atr_pct, cfg.vol_window)
    vol = np.select(
        [pct.isna(), pct >= cfg.high_vol_pct, pct <= cfg.low_vol_pct],
        ["unknown", "high_vol", "low_vol"],
        default="normal_vol",
    )
    med = data["volume"].rolling(cfg.liq_window, min_periods=cfg.liq_window).median().shift(1)
    rel = data["volume"] / med.replace(0, np.nan)
    liq = np.select(
        [rel.isna(), rel < cfg.low_liq_ratio], ["unknown", "low_liq"], default="normal_liq"
    )
    out = pd.DataFrame({"trend": trend, "volatility": vol, "liquidity": liq}, index=data.index)
    out["label"] = out["trend"] + "|" + out["volatility"]
    return out
```
<!-- fmt: on -->

Tres dimensiones independientes:

| Dimensión | Valores | Regla (valores por defecto) |
|---|---|---|
| `trend` | `trend` / `range` / `unknown` | ADX(14) ≥ 25 → `trend` |
| `volatility` | `high_vol` / `normal_vol` / `low_vol` / `unknown` | percentil del ATR % frente a las 500 velas **anteriores**: ≥ 0,8 alta, ≤ 0,2 baja |
| `liquidity` | `low_liq` / `normal_liq` / `unknown` | volumen / mediana de las 200 velas anteriores < 0,5 → `low_liq` |

- **45:** `np.where` anidado, igual que en las combinaciones. Mientras el ADX es `NaN`, la
  etiqueta es `unknown`.
- **46–47:** el ATR % (ATR / cierre) hace comparable la volatilidad a distintos precios. El
  percentil móvil (`rolling_percentile`, Módulo VII) compara el valor actual con las `n` velas
  anteriores: 0,9 significa "mayor que el 90 % de las últimas 500".
- **48–52:** `np.select(condiciones, valores, default)` evalúa las condiciones **en orden** y
  toma la primera verdadera. Por eso `unknown` va primero.
- **53:** la mediana del volumen lleva `shift(1)`: la vela actual no entra en su propia
  referencia (causalidad, Módulo VII).
- **59:** `label` combina tendencia y volatilidad (`trend|high_vol`). Es la etiqueta que el
  motor guarda en cada operación para los desgloses por régimen (`Researcher.simulate`,
  `research.py`, línea 160).

**[Limitación]** `liquidity` es una **aproximación por volumen**: sin libro de órdenes no se
mide la liquidez real (diferencial, profundidad). Lo dice la cabecera (líneas 8–10).

**Causalidad.** `test_regime_is_causal` compara el régimen calculado con toda la serie y con
solo las primeras 1200 velas: deben coincidir en esas 1200.

<!-- fmt: off -->
`tests/unit/test_signals.py` · líneas 134–139

```python
def test_regime_is_causal(synth: pd.DataFrame) -> None:
    full = classify_regime(synth)
    part = classify_regime(synth.iloc[:1200])
    pd.testing.assert_frame_equal(full.iloc[:1200], part)
    assert set(full["trend"].unique()) <= {"trend", "range", "unknown"}
    assert np.all(full["liquidity"].isin(["low_liq", "normal_liq", "unknown"]))
```
<!-- fmt: on -->

Distribución en la serie sintética:

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import classify_regime

reg = classify_regime(generate_synthetic_ohlcv(bars=6000, seed=42))
for dim in ("trend", "volatility", "liquidity"):
    print(dim, reg[dim].value_counts().to_dict())
t = reg["trend"]
validas = t.isin(["trend", "range"]) & t.shift(1).isin(["trend", "range"])
print("cambios trend<->range:", int(((t != t.shift(1)) & validas).sum()))
```
*Salida real:*

```text
trend {'range': 3287, 'trend': 2686, 'unknown': 27}
volatility {'high_vol': 2131, 'normal_vol': 1727, 'low_vol': 1629, 'unknown': 513}
liquidity {'normal_liq': 5701, 'unknown': 200, 'low_liq': 99}
cambios trend<->range: 185
```

Lectura:

- **`unknown` en `trend` (27 velas):** el calentamiento del ADX(14), igual que en la sección
  8.10.
- **`unknown` en `volatility`:** el ATR necesita 14 velas y el percentil 501 valores más.
- **`high_vol` > 20 %:** el percentil es **relativo a las 500 velas anteriores**. Si la
  volatilidad crece de forma sostenida, muchas velas quedan por encima del percentil 80 de su
  pasado reciente. No es una proporción fija.
- **185 cambios entre `trend` y `range`:** el régimen de tendencia **no tiene histéresis**
  (a diferencia de `adx_di`, que entra con 25 y sale con 20). Un ADX que oscila alrededor de 25
  cambia la etiqueta muchas veces. Consecuencia en la sección siguiente.

---

## 9.10 Filtro de régimen

<!-- fmt: off -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 62–79

```python
def apply_regime_filter(
    signals: pd.DataFrame,
    categories: dict[str, str],
    regime: pd.DataFrame,
    rules: dict[str, dict[str, list[str]]],
) -> pd.DataFrame:
    """Fuerza a 0 las señales de cada estrategia fuera de sus regímenes permitidos."""
    out = signals.copy()
    reg = regime.reindex(signals.index)
    for name in out.columns:
        allowed = pd.Series(True, index=out.index)
        for key in ("*", categories.get(name, ""), name):
            for dim, values in (rules.get(key) or {}).items():
                if dim not in reg.columns:
                    raise ValueError(f"Dimensión de régimen desconocida: {dim}")
                allowed &= reg[dim].isin(values)
        out.loc[~allowed, name] = 0
    return out
```
<!-- fmt: on -->

- **73:** para cada estrategia se consultan tres claves de reglas, en este orden: el comodín
  `*`, el nombre de su categoría y su propio nombre.
- **74–77:** cada regla exige que el régimen esté en la lista de valores permitidos. Las
  condiciones se combinan con `&=`, es decir, **todas** deben cumplirse. Una regla específica
  de una estrategia **no puede relajar** una regla de `*`; solo puede añadir restricciones.
- **75–76:** una dimensión inexistente es un error, no se ignora en silencio.
- **78:** donde no está permitido, el estado de la estrategia se fuerza a 0 **antes de votar**.

La combinación configurada que usa reglas:

`configs/strategies.yaml` · líneas 169–178

```yaml
  - name: regime_switch
    mode: min_consensus
    min_votes: 2
    regime_rules:
      trend: {trend: [trend]}                         # categoría tendencia solo en tendencia
      rsi_reversion: {trend: [range]}                 # reversión solo en lateral
      bollinger_reversion: {trend: [range]}
      vwap_deviation: {trend: [range]}
      stoch_rsi: {trend: [range]}
      "*": {liquidity: [normal_liq, unknown]}         # bloquear baja liquidez
```

**Cuidado con la lectura de la línea 173.** `trend: {trend: [trend]}` contiene tres "trend"
distintos: la **categoría** `trend` (clave exterior), la **dimensión** `trend` y el **valor**
`trend`. Significa: "a las estrategias de la categoría tendencia, permíteles operar solo cuando
la dimensión de tendencia vale `trend`".

**[Hecho] Efecto lateral: entradas a mitad de una posición.** El filtro actúa sobre el
**estado**, no sobre los eventos. Si una estrategia está larga desde hace 30 velas, el régimen
pasa a `range` (estado forzado a 0) y vuelve a `trend`, la señal filtrada pasa de 0 a +1: para
el motor es una **entrada nueva**, aunque la estrategia no haya generado ninguna. Medición con
una sola estrategia y la regla de tendencia:

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import CombinationConfig, classify_regime, combine_signals
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
reg = classify_regime(datos)
frames = {"ema_crossover": create_strategy("ema_crossover").generate_signals(datos)}
cfg = CombinationConfig(
    mode="min_consensus",
    min_votes=1,
    conflict_policy="net",
    regime_rules={"ema_crossover": {"trend": ["trend"]}},
)
orig = frames["ema_crossover"]["signal"]
filt = combine_signals(frames, {"ema_crossover": "trend"}, cfg, reg)["signal"]


def entradas(s):
    return (s != 0) & (s != s.shift(1, fill_value=0))


sin_evento = entradas(filt) & (orig == orig.shift(1, fill_value=0))
forzadas = (filt == 0) & (filt.shift(1, fill_value=0) != 0) & (orig != 0)
print("entradas de la estrategia:", int(entradas(orig).sum()))
print("entradas tras el filtro:", int(entradas(filt).sum()))
print("  de ellas, sin cambio en la estrategia:", int(sin_evento.sum()))
print("salidas forzadas por el régimen:", int(forzadas.sum()))
print("velas en posición:", int((orig != 0).sum()), "->", int((filt != 0).sum()))
```
*Salida real:*

```text
entradas de la estrategia: 23
entradas tras el filtro: 17
  de ellas, sin cambio en la estrategia: 9
salidas forzadas por el régimen: 11
velas en posición: 642 -> 343
```

Interpretación:

- El filtro **reduce** la exposición (de 642 a 343 velas), pero **no** reduce las operaciones en
  la misma proporción: de las entradas filtradas, más de la mitad son **reentradas** creadas
  por el regreso del régimen, a un precio peor que el de la entrada original, y cada una paga
  comisión y deslizamiento (Módulo X).
- Las salidas forzadas no son decisiones de la estrategia: las provoca el cambio de etiqueta,
  que sin histéresis oscila (sección 9.9).

**[Diseño]** Es coherente con el contrato del motor: entra en cada **transición** del estado
objetivo, venga de donde venga. Una alternativa sería filtrar solo los **eventos de entrada**
(bloquear entradas en régimen no permitido, pero no expulsar posiciones abiertas). No está
implementada.

**[Hecho] El régimen no bloquea operaciones de estrategias individuales.** En los backtests de
una sola estrategia, el régimen solo se usa como **etiqueta** de las operaciones. Filtra únicamente
dentro de una combinación con `regime_rules`.

**Comprobación.** Con la regla `"*": {liquidity: [normal_liq]}` (sin `unknown`), ¿qué ocurre en
las primeras 200 velas?

**Respuesta:**

Ninguna estrategia puede operar: la mediana del volumen necesita 200 velas anteriores, así que
`liquidity` vale `unknown` y no está en la lista permitida. Por eso la configuración del
repositorio incluye `unknown` en esa regla.

---

## 9.11 Detección de redundancia

<!-- fmt: off -->
`src/bybit_quant_lab/signals/redundancy.py` · líneas 1–46

```python
"""Redundancia entre señales: correlación, coincidencia y selección de estrategias no redundantes.

Estas medidas deben calcularse **en el período de entrenamiento** cuando se usan para decidir
qué estrategias entran en una combinación.
"""

from __future__ import annotations

import pandas as pd


def signal_correlation(signals: pd.DataFrame) -> pd.DataFrame:
    """Correlación de Pearson entre series de estado (-1/0/1). Columnas constantes -> NaN."""
    return signals.astype(float).corr()


def signal_agreement(signals: pd.DataFrame) -> pd.DataFrame:
    """Proporción de velas con la misma dirección entre las velas en que ambas están activas."""
    names = list(signals.columns)
    out = pd.DataFrame(index=names, columns=names, dtype=float)
    for a in names:
        for b in names:
            both = (signals[a] != 0) & (signals[b] != 0)
            out.loc[a, b] = (
                float((signals[a][both] == signals[b][both]).mean()) if both.any() else float("nan")
            )
    return out


def select_non_redundant(
    corr: pd.DataFrame, threshold: float = 0.7, priority: list[str] | None = None
) -> tuple[list[str], dict[str, str]]:
    """Selección voraz: recorre ``priority`` y descarta las que superan ``|corr| > threshold``
    con alguna ya seleccionada. Devuelve (seleccionadas, {descartada: correlacionada_con})."""
    order = priority or list(corr.columns)
    values = corr.astype(float).fillna(0.0).to_numpy()
    pos = {str(c): i for i, c in enumerate(corr.columns)}
    kept: list[str] = []
    dropped: dict[str, str] = {}
    for name in order:
        clash = next((k for k in kept if abs(float(values[pos[name], pos[k]])) > threshold), None)
        if clash is None:
            kept.append(name)
        else:
            dropped[name] = clash
    return kept, dropped
```
<!-- fmt: on -->

Dos medidas:

- **Correlación de Pearson** (`signal_correlation`) entre series de estados −1/0/1 (Módulo VI).
- **Coincidencia direccional** (`signal_agreement`): entre las velas en que **ambas** están
  activas, la fracción en que tienen la misma dirección.

Y un procedimiento de selección voraz (`select_non_redundant`, líneas 30–46): recorre las
estrategias en orden; conserva una si su |correlación| con todas las ya conservadas es ≤ el
umbral; si no, la descarta y anota con cuál chocó. "Voraz" significa que decide una a una sin
reconsiderar: el resultado depende del **orden** (por defecto, el de las columnas, que es
alfabético en `build_combinations`).

### Por qué la correlación subestima la redundancia: cálculo a mano

Dos estrategias que **siempre** coinciden cuando ambas están activas, pero que entran y salen en
momentos distintos:

```text
vela:  0   1   2   3   4   5   6   7
x   :  1   1   0   0   0   0  -1  -1
y   :  0   1   1   0   0   0   0  -1
```

- Ambas activas en las velas 1 (+1, +1) y 7 (−1, −1) → coincidencia = 2/2 = **1,0**.
- Pearson (n = 8): media de x = 0; media de y = 1/8.
  - Σ x·y = 1·1 + (−1)·(−1) = 2; como la media de x es 0, cov = 2/7.
  - var(x) = Σx²/7 = 4/7; var(y) = (Σy² − 8·(1/8)²)/7 = (3 − 0,125)/7 = 2,875/7.
  - ρ = (2/7) / √(4/7 · 2,875/7) = 2 / √11,5 ≈ **0,590**.

Con el umbral 0,7, estas dos estrategias se considerarían **no redundantes**, aunque nunca se
contradicen. Los muchos ceros (velas fuera de posición) y los desfases de entrada diluyen la
correlación.

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.signals import signal_agreement, signal_correlation

s = pd.DataFrame({"x": [1, 1, 0, 0, 0, 0, -1, -1], "y": [0, 1, 1, 0, 0, 0, 0, -1]})
print("correlación:", round(float(signal_correlation(s).loc["x", "y"]), 3))
print("coincidencia:", float(signal_agreement(s).loc["x", "y"]))
```
*Salida real:*

```text
correlación: 0.59
coincidencia: 1.0
```

**[Limitación] La coincidencia tampoco basta sola.** Dos estrategias activas a la vez en una
sola vela, y de acuerdo, dan coincidencia 1,0 con una muestra de tamaño 1. Conviene mirar
ambas medidas **y** cuántas velas comparten.

---

## 9.12 Cuando el filtro de redundancia no elimina ninguna estrategia

Resultado real en el entrenamiento sintético (las 3600 primeras velas de 6000, semilla 42):

*Ejemplo ejecutable:*

```python
import numpy as np
import pandas as pd

from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import select_non_redundant, signal_agreement, signal_correlation
from bybit_quant_lab.strategies import available_strategies
from bybit_quant_lab.validation.research import Researcher

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
params = load_strategy_params("configs/strategies.yaml")
r = Researcher(datos, "BTCUSDT", "1h", load_config(), strategy_params=params)
tr = r.segments["train"]
sig = pd.DataFrame(
    {n: r.strategy_candidate(n).signals["signal"] for n in available_strategies()}
).iloc[tr.start_pos : tr.end_pos + 1]
corr = signal_correlation(sig)
fuera_diag = corr.where(~np.eye(len(corr), dtype=bool)).abs().stack()
print("velas de entrenamiento:", len(sig))
print("par más correlacionado:", fuera_diag.idxmax(), round(float(fuera_diag.max()), 3))
kept, dropped = select_non_redundant(corr.fillna(0), 0.7)
print("conservadas:", len(kept), "descartadas:", dropped)
tend = ["ema_crossover", "donchian_breakout", "adx_di"]
print(signal_agreement(sig).loc[tend, tend].round(2).to_string())
```
*Salida real:*

```text
velas de entrenamiento: 3600
par más correlacionado: ('adx_di', 'donchian_breakout') 0.652
conservadas: 10 descartadas: {}
                   ema_crossover  donchian_breakout  adx_di
ema_crossover               1.00               0.96    0.91
donchian_breakout           0.96               1.00    0.97
adx_di                      0.91               0.97    1.00
```

**Cómo interpretarlo.**

1. **Hecho:** con el umbral 0,7 no se descarta ninguna estrategia. `dedup_vote` usa las diez y
   es, en la práctica, `simple_vote` con margen 2 y `veto` sobre todas las estrategias.
2. **No significa** que las estrategias sean independientes. La coincidencia entre las de
   tendencia supera 0,9: cuando están activas a la vez, casi siempre dicen lo mismo.
3. **Por qué ocurre:** la medida (Pearson sobre estados con muchos ceros) es débil para este
   tipo de señal (sección 9.11). El umbral 0,7 es una convención, no un valor calibrado.
4. **Qué mirar en el informe:** la sección "Redundancia entre señales (entrenamiento)" del HTML
   muestra ambas matrices y el JSON con `"dropped": {}`. Un diccionario vacío es un resultado,
   no un error, y hay que leerlo como "la medida no detectó redundancia", no como "no la hay".
5. **Qué no hacer:** bajar el umbral mirando los resultados de validación hasta que la
   combinación "mejore". Sería ajustar con el segmento de selección (Módulo XIII). Si se cambia
   la medida o el umbral, debe hacerse con entrenamiento y quedar registrado.
6. **Opciones documentadas** (`docs/audit_report.md`, M-05): usar `signal_agreement` o fijar
   `members` explícitos en el YAML. Ejercicio en el Módulo XVI.

---

## 9.13 Las seis combinaciones configuradas

Con los mismos datos y parámetros que en 9.6, número de entradas y de velas en posición de cada
combinación sobre la serie completa:

*Ejemplo ejecutable:*

```python
import yaml

from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import CombinationConfig
from bybit_quant_lab.strategies import available_strategies
from bybit_quant_lab.validation.research import Researcher

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
params = load_strategy_params("configs/strategies.yaml")
r = Researcher(datos, "BTCUSDT", "1h", load_config(), strategy_params=params)
combos = [
    CombinationConfig.model_validate(c)
    for c in yaml.safe_load(open("configs/strategies.yaml"))["combinations"]
]
singles = {n: r.strategy_candidate(n) for n in available_strategies()}
cands, _ = r.build_combinations(singles, combos)
print(f"{'combinación':16s} {'modo':20s} {'entradas':>8s} {'velas':>6s}")
for nombre, c in cands.items():
    s = c.signals["signal"]
    entradas = int(((s != 0) & (s != s.shift(1, fill_value=0))).sum())
    print(f"{nombre:16s} {c.params['mode']:20s} {entradas:8d} {int((s != 0).sum()):6d}")
```
*Salida real:*

```text
combinación      modo                 entradas  velas
vote_all         simple_vote               210    876
weighted_train   weighted_vote             106    307
consensus_3      min_consensus             108    318
category_2       category_consensus        168    608
dedup_vote       simple_vote               190    737
regime_switch    min_consensus             371   2988
```

Observaciones:

- `regime_switch` es la combinación con **más** exposición y más entradas, pese a tener filtros.
  El bloque siguiente aísla la causa.
- `weighted_train` y `consensus_3` tienen exposición parecida por motivos distintos: la primera,
  por el veto de los miembros con peso 0 (9.6).
**¿Un filtro que aumenta la exposición?** Se compara `regime_switch` con y sin sus reglas de
régimen, y se cuenta cuántos vetos vienen de estrategias de reversión:

*Ejemplo ejecutable:*

```python
import yaml

from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import CombinationConfig, combine_signals
from bybit_quant_lab.strategies import available_strategies, create_strategy
from bybit_quant_lab.validation.research import Researcher

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
params = load_strategy_params("configs/strategies.yaml")
r = Researcher(datos, "BTCUSDT", "1h", load_config(), strategy_params=params)
frames = {n: r.strategy_candidate(n).signals for n in available_strategies()}
cats = {n: create_strategy(n).category.value for n in frames}
raw = yaml.safe_load(open("configs/strategies.yaml"))["combinations"]
cfg = CombinationConfig.model_validate(next(c for c in raw if c["name"] == "regime_switch"))


def resumen(s):
    entradas = int(((s != 0) & (s != s.shift(1, fill_value=0))).sum())
    return entradas, int((s != 0).sum())


sin = combine_signals(frames, cats, cfg.model_copy(update={"regime_rules": None}))["signal"]
con = combine_signals(frames, cats, cfg, r.regime)["signal"]
print("sin reglas de régimen (entradas, velas):", resumen(sin))
print("con reglas de régimen (entradas, velas):", resumen(con))

import pandas as pd

S = pd.DataFrame({n: f["signal"] for n, f in frames.items()})
n_long, n_short = (S > 0).sum(axis=1), (S < 0).sum(axis=1)
direccion = (n_long >= 2).astype(int) - (n_short >= 2).astype(int)
# direccion = +1/-1 si una sola dirección alcanza 2 votos; vetada si hay voto contrario
vetadas = ((direccion > 0) & (n_short > 0)) | ((direccion < 0) & (n_long > 0))
reversion = ["rsi_reversion", "bollinger_reversion", "stoch_rsi", "vwap_deviation"]
por_reversion = vetadas & (S[reversion].mul(direccion, axis=0) < 0).any(axis=1)
print("velas vetadas sin filtro:", int(vetadas.sum()))
print("  con algún voto contrario de reversión:", int(por_reversion.sum()))
```
*Salida real:*

```text
sin reglas de régimen (entradas, velas): (190, 737)
con reglas de régimen (entradas, velas): (371, 2988)
velas vetadas sin filtro: 2354
  con algún voto contrario de reversión: 1813
```

Explicación: `regime_switch` usa `veto`. Sin filtro, en una tendencia las estrategias de
reversión suelen votar en contra de las de tendencia y **vetan** sus entradas. El filtro apaga
las de reversión en régimen `trend` (y las de tendencia en `range`), así que desaparecen esos
vetos (en esta serie, 1813 de las 2354 velas vetadas tenían un voto contrario de reversión) y la combinación pasa mucho más tiempo en posición. A esto se suman las reentradas de
9.10. Observa también que "sin reglas" da lo mismo que `dedup_vote`: ambas son, por la
equivalencia de 9.4, "dos votos en una dirección y ninguno en contra" sobre las diez
estrategias.

- Cada combinación es una **prueba más** que entra en el recuento de ensayos del DSR
  (Módulo XIII). Seis combinaciones más diez estrategias son al menos dieciséis candidatos por
  mercado, más los ensayos de umbral registrados.

---

## 9.14 Resumen y errores comunes

| Idea | Dónde | Etiqueta |
|---|---|---|
| La combinación devuelve el mismo contrato que una estrategia | `combiners.py` 136–150 | [Diseño] |
| `simple_vote` + `veto` ≡ `min_consensus` + `veto` | test de auditoría B-01 | [Hecho] |
| Pesos y umbral se ajustan en entrenamiento | `research.py` 215–239 | [Hecho] tras `a50ac62` |
| Cabecera de `research.py` e informe HTML aún dicen "validación" | 7–8; `html.py` 279–282 | [Discrepancia] |
| Miembros con peso 0 vetan y aportan stop | `combiners.py` 137–146 | [Hecho], pendiente |
| La convicción no cambia el tamaño | búsqueda en `risk/` | [Hecho] |
| Régimen sin histéresis; el filtro crea reentradas | `regime.py` 45; `combiners.py` 78 | [Hecho] |
| Categoría `indicator` heterogénea | M-05 | [Limitación], pendiente |
| Pearson sobre estados subestima la redundancia | M-05 | [Limitación], pendiente |
| `liquidity` es una aproximación por volumen | `regime.py` 8–10 | [Limitación] |

**Errores comunes.**

1. Contar diez votos como diez opiniones independientes.
2. Creer que un peso 0 excluye a una estrategia cuando la política es `veto`.
3. Interpretar `"dropped": {}` como prueba de independencia.
4. Ajustar umbrales, pesos o miembros con validación y luego seleccionar con la misma
   validación.
5. Suponer que un filtro de régimen solo "quita" operaciones: también puede añadir reentradas.

### Comprobación final del módulo

En una vela, cinco estrategias votan +1, dos votan −1 y tres se abstienen. Calcula la señal de:
(a) `simple_vote`, margen 3, `net`; (b) `simple_vote`, margen 3, `veto`; (c) `min_consensus`,
3 votos, `net`; (d) `weighted_vote` con pesos iguales, θ = 0,3, `net`.

**Respuesta:**

- (a) net = 5 − 2 = 3 ≥ 3 → **+1**.
- (b) +1 antes del veto, pero hay votos cortos → **0**.
- (c) n_long = 5 ≥ 3 y n_short = 2 < 3 → **+1**.
- (d) score = (5 − 2)/10 = 0,3 ≥ 0,3 → **+1** (las abstenciones cuentan en el denominador,
  porque se divide por la suma de **todos** los pesos).

<div style="page-break-before: always;"></div>

# Módulo X. El motor de backtesting

El motor es la pieza que convierte una serie de señales en operaciones, costes y una curva de
equity. Si el motor se equivoca, **todos** los resultados del proyecto son falsos, por buenas
que sean las estrategias. Por eso este módulo es el más detallado del curso: recorre el bucle
línea a línea, calcula una operación completa a mano y la reproduce con el código.

Archivos principales:

| Archivo | Papel |
|---|---|
| `src/bybit_quant_lab/backtesting/engine.py` | Bucle vela a vela, apertura y cierre de posiciones |
| `src/bybit_quant_lab/execution/costs.py` | Comisiones y deslizamiento |
| `src/bybit_quant_lab/execution/fills.py` | Stops, objetivos, gaps y liquidación con velas OHLC |
| `src/bybit_quant_lab/portfolio/position.py` | Posición abierta, trailing stop y registro de operación |
| `src/bybit_quant_lab/backtesting/results.py` | Contenedor de resultados |

El dimensionamiento, los límites de riesgo y la contabilidad de margen se tratan en el
Módulo XI; aquí se usan sus resultados.

---

## 10.1 Qué es un motor de backtesting y por qué uno "vela a vela"

**Intuición.** Un backtest responde a la pregunta: "si hubiera seguido estas reglas en el
pasado, ¿qué habría pasado con mi cuenta?". Para responderla sin hacer trampa hay que
reproducir el paso del tiempo: en cada momento solo se puede usar lo que ya se sabía.

**Dos familias de motores.**

- **Vectorizado:** calcula todo con operaciones sobre columnas completas
  (`posición × retorno`). Es rápido, pero modela mal los stops intravela, los costes que
  dependen del tamaño, los límites de riesgo que dependen de la equity y las salidas que
  dependen del camino recorrido.
- **Por eventos (vela a vela):** un bucle recorre las velas en orden y mantiene un **estado**
  (efectivo, posición, límites). Es más lento, pero cada decisión usa solo el estado anterior.

**[Diseño]** El proyecto usa un bucle explícito en Python (`for i in range(i0, i1 + 1)`). Es
más lento que una versión vectorizada, pero cada paso se puede leer y auditar.

**Término: determinista.** Con las mismas entradas produce exactamente las mismas salidas. El
motor no usa números aleatorios. `test_backtest_is_deterministic` lo comprueba ejecutando dos
veces y comparando equity y operaciones (`tests/unit/test_engine.py`, líneas 129–136).

---

## 10.2 El orden de los eventos dentro de una vela

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 1–20

```python
"""Motor de backtesting determinista, vela a vela.

Orden de eventos dentro de cada vela ``i`` (índice = apertura de la vela):

1. Cambio de día UTC -> el gestor de riesgo reinicia la referencia diaria.
2. Funding: los pagos con marca de tiempo en ``(open[i-1], open[i]]`` se aplican a la
   posición mantenida al final de la vela ``i-1``, valorada a ``open[i]``.
3. Gap: si la apertura supera el stop/liquidación/objetivo, salida a la apertura.
4. Órdenes pendientes decididas al cierre de ``i-1``: primero salida, después entrada, ambas
   a ``open[i]`` con slippage adverso y comisión taker.
5. Intravela: stop/liquidación/objetivo con la regla *stop primero* (ver ``execution.fills``).
6. Cierre: valoración mark-to-market, registro de equity, límites de riesgo.
7. Trailing stop: se actualiza con el cierre y rige desde la vela siguiente.
8. Señal al cierre de ``i``: se programan órdenes para ``open[i+1]``. Nunca se ejecuta una
   señal al precio de la vela en que se generó.

Las entradas son *edge-triggered*: solo se abre posición cuando el objetivo de la estrategia
cambia a LONG/SHORT. Si un stop cierra la operación y la estrategia sigue en LONG, no se
reabre hasta una nueva transición. Las entradas rechazadas por riesgo no se difieren.
"""
```
<!-- fmt: on -->

**Por qué importa el orden.** Una vela OHLC resume una hora (o 5 minutos, o 4 horas) en cuatro
precios. Todo lo que ocurre dentro de ella ya pasó cuando se conoce el cierre. El motor tiene
que decidir **qué pudo hacerse y en qué momento**:

```text
open[i] ─────────────────────────────────────────────────── close[i]
  │ 1 día UTC  2 funding  3 gap  4 órdenes pendientes  5 intravela │ 6 valoración 7 trailing 8 señal
  └──────────────── precio disponible: open[i] ──────────────────┘   └──── se conoce close[i] ────┘
```

Los pasos 1–4 ocurren **en la apertura**; el 5, **durante** la vela; los 6–8, **al cierre**.
La señal calculada al cierre de `i` (paso 8) solo se ejecuta en la apertura de `i+1` (paso 4 de
la vela siguiente).

**[Hecho]** "Nunca se ejecuta una señal al precio de la vela en que se generó" (líneas 14–15).
Esta es la regla que impide el error más común de los backtests: decidir con el cierre y
comprar a ese mismo cierre, que en la realidad ya no está disponible cuando el cálculo termina.

**Comprobación.** Una estrategia calcula su señal con el cierre de la vela de las 10:00 (que
termina a las 10:59:59). ¿A qué precio entra el motor?

**Respuesta:**

A la apertura de la vela de las 11:00, con deslizamiento adverso. Nunca al cierre de la vela
de las 10:00.

---

## 10.3 Preparación: entradas, segmento y arrays

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 71–120

```python
    def run(
        self,
        data: pd.DataFrame,
        signals: pd.DataFrame,
        funding: pd.Series | None = None,
        start: pd.Timestamp | None = None,
        end: pd.Timestamp | None = None,
        regime: pd.Series | None = None,
        label: str = "",
        params: dict[str, Any] | None = None,
    ) -> BacktestResult:
        """Simula ``[start, end]`` (inclusive). Las señales deben estar alineadas con ``data``."""
        self._check_inputs(data, signals)
        idx = pd.DatetimeIndex(data.index)
        i0 = 0 if start is None else int(idx.searchsorted(start, side="left"))
        i1 = len(idx) - 1 if end is None else int(idx.searchsorted(end, side="right")) - 1
        warnings: list[str] = []
        if i1 < i0:
            raise ValueError("El segmento solicitado no contiene velas")
        cfg = self.config
        acct = Account(cfg.backtest.initial_capital)
        risk = RiskManager(cfg.risk, cfg.backtest.initial_capital)
        o = data["open"].to_numpy(float)
        h = data["high"].to_numpy(float)
        low = data["low"].to_numpy(float)
        c = data["close"].to_numpy(float)
        sig = signals["signal"].to_numpy(np.int64)
        conv = signals["conviction"].to_numpy(float)
        stop_d = signals["stop_distance"].to_numpy(float)
        tp_d = signals["take_profit_distance"].to_numpy(float)
        tr_d = signals["trailing_distance"].to_numpy(float)
        regimes = (
            regime.reindex(idx).fillna("unknown").astype(str).to_numpy()
            if regime is not None
            else None
        )
        funding_by_bar, funding_ok, fw = self._map_funding(funding, idx, i0, i1)
        stamps = list(idx[i0 : i1 + 1])
        # Identificador de día UTC independiente de la resolución del índice (ns, us, ms...).
        day_ids = (
            idx.floor("D").as_unit("s").tz_convert(None).to_numpy().astype("int64") // 86_400
        ).tolist()
        warnings.extend(fw)

        trades: list[TradeRecord] = []
        rejected: list[dict[str, Any]] = []
        rows: list[tuple[float, float, float, float, float, bool]] = []
        pending_exit: str | None = None
        pending_entry: _PendingEntry | None = None
        prev_target = int(sig[i0 - 1]) if i0 > 0 else 0
```
<!-- fmt: on -->

Línea a línea:

- **83:** `_check_inputs` (líneas 246–256) exige las columnas de señal, el **mismo índice** en
  datos y señales, datos no vacíos y precios sin `NaN`. Un índice desalineado es un error
  inmediato (`test_misaligned_signals_rejected`), no un `reindex` silencioso.
- **85–86:** `searchsorted` convierte las fechas `start`/`end` en posiciones. `i0` es la primera
  vela con `open_time ≥ start`; `i1`, la última con `open_time ≤ end`. El segmento es
  **inclusivo** en ambos extremos.
- **91–92:** cada simulación empieza con una cuenta y un gestor de riesgo nuevos: los segmentos
  no comparten estado.
- **93–101:** las columnas se convierten a arrays de NumPy (`to_numpy`). Acceder a `o[i]` en un
  array es mucho más rápido que `df["open"].iloc[i]` dentro de un bucle (Módulo V).
- **102–106:** el régimen es solo una **etiqueta** que se copia a cada operación.
- **107:** el funding se traduce a "pagos por índice de vela" (sección 10.6).
- **110–112:** identificador entero del día UTC para cada vela (días desde 1970-01-01), usado
  por el límite de pérdida diaria. Se calcula una sola vez para todo el índice. `as_unit("s")`
  fija la unidad antes de convertir a entero: un índice puede guardarse internamente en
  nanosegundos, microsegundos o milisegundos, y dividir el entero bruto por 86 400 solo es
  correcto si la unidad es el segundo. Se introdujo en `2f60aca`; antes, `on_bar_open`
  comparaba objetos `Timestamp` (`ts.floor("D")`) en cada vela.
- **120:** `prev_target` empieza con la señal de la vela **anterior al segmento**. Si una
  estrategia ya estaba larga antes de `start`, no hay transición al empezar y el motor **no
  entra** (`test_segment_start_does_not_enter_on_preexisting_signal`). Así, un segmento de
  validación no empieza con una entrada artificial.

---

## 10.4 El bucle, paso a paso

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 122–148

```python
        for i in range(i0, i1 + 1):
            ts = stamps[i - i0]
            risk.on_bar_open(ts, day_ids[i])
            pos = acct.position
            # 2. funding
            if pos is not None and i in funding_by_bar:
                payment = pos.side * pos.qty * o[i] * funding_by_bar[i]
                acct.cash -= payment
                acct.total_funding += payment
                pos.funding += payment
            # 3. gap
            if pos is not None:
                gap = check_gap_exit(
                    pos.side, o[i], pos.stop, pos.take_profit, pos.liquidation_price
                )
                if gap is not None:
                    trades.append(self._close(acct, risk, gap, i, ts))
                    pending_exit = None
            # 4. pending orders at open
            if pending_exit is not None and acct.position is not None:
                trades.append(self._close(acct, risk, ExitCheck(o[i], pending_exit), i, ts))
            pending_exit = None
            if pending_entry is not None and acct.position is None:
                rej = self._open(acct, pending_entry, o[i], i, ts)
                if rej:
                    rejected.append({"time": str(ts), "side": pending_entry.side, "reason": rej})
            pending_entry = None
```
<!-- fmt: on -->

- **124 (paso 1):** el gestor de riesgo detecta el cambio de día UTC (Módulo XI).
- **127–131 (paso 2, funding):** `payment = lado × cantidad × open[i] × tasa`. Para un largo
  (`lado = +1`) con tasa positiva, `payment > 0` y el efectivo **baja**: el largo paga. Para un
  corto, `payment < 0` y el efectivo **sube**: el corto cobra. Se acumula en la cuenta y en la
  posición.
- **133–139 (paso 3, gap):** si la apertura ya está más allá del stop, la liquidación o el
  objetivo, se cierra ahí (sección 10.7). Si había una salida pendiente, se descarta: la
  posición ya no existe.
- **141–143 (paso 4, salida pendiente):** se ejecuta a `open[i]`. Primero la salida...
- **144–148 (paso 4, entrada pendiente):** ...después la entrada, solo si no queda posición.
  Si el dimensionamiento devuelve 0 (por ejemplo, cantidad por debajo del mínimo), la entrada
  se registra como **rechazada** con el motivo.

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 149–176

```python
            # 5. intrabar
            pos = acct.position
            if pos is not None:
                hit = check_intrabar_exit(
                    pos.side, h[i], low[i], pos.stop, pos.take_profit, pos.liquidation_price
                )
                if hit is not None:
                    trades.append(self._close(acct, risk, hit, i, ts))
            # 6. close / mark to market
            pos = acct.position
            unreal = pos.unrealized(c[i]) if pos else 0.0
            equity = acct.cash + unreal
            rows.append(
                (
                    equity,
                    acct.cash,
                    unreal,
                    pos.side * pos.qty if pos else 0.0,
                    acct.used_margin,
                    pos is not None,
                )
            )
            force_close = risk.on_bar_close(ts, equity)
            # 7. trailing
            if pos is not None:
                pos.update_trailing(c[i])
            if i == i1:
                break
```
<!-- fmt: on -->

- **150–156 (paso 5, intravela):** con el máximo y el mínimo de la vela se comprueba si se tocó
  stop, liquidación u objetivo (sección 10.7).
- **158–170 (paso 6, valoración):** `equity = efectivo + PnL no realizado al cierre`. Se guarda
  una fila por vela con equity, efectivo, no realizado, posición con signo, margen y si hay
  posición abierta.
- **171:** el gestor de riesgo evalúa la pérdida diaria y el drawdown con esa equity; puede
  pedir un cierre forzado.
- **173–174 (paso 7):** el trailing stop se mueve con el cierre; el nuevo nivel rige desde la
  vela siguiente (sección 10.8).
- **175–176:** en la última vela no se decide nada: no existe una apertura posterior donde
  ejecutar (`test_signal_on_last_bar_is_never_executed`).

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 177–202

```python
            # 8. decision at close
            target = int(sig[i])
            if force_close and acct.position is not None:
                pending_exit = "risk_limit_close"
            elif acct.position is not None and target != acct.position.side:
                pending_exit = "signal_exit" if target == 0 else "signal_reverse"
            is_edge = target not in (0, prev_target)
            prev_target = target
            if is_edge:
                can_reverse = acct.position is None or (
                    pending_exit is not None and cfg.execution.allow_reversal
                )
                allowed, reason = risk.can_open(i)
                if not can_reverse:
                    rejected.append({"time": str(ts), "side": target, "reason": "position_open"})
                elif not allowed:
                    rejected.append({"time": str(ts), "side": target, "reason": reason})
                else:
                    pending_entry = _PendingEntry(
                        side=target,
                        stop_distance=float(stop_d[i]),
                        tp_distance=_nan_to_none(tp_d[i]),
                        trail_distance=_nan_to_none(tr_d[i]),
                        conviction=float(conv[i]),
                        regime=str(regimes[i]) if regimes is not None else "",
                    )
```
<!-- fmt: on -->

- **178:** `target` es el estado objetivo de la estrategia al cierre de `i`.
- **179–182:** se programa una salida si el riesgo lo exige o si el objetivo ya no coincide con
  el lado de la posición (a 0: `signal_exit`; al lado contrario: `signal_reverse`).
- **183 (entrada por transición):** `is_edge` es verdadero solo si el objetivo es +1 o −1
  **y** distinto del de la vela anterior. Mantener `signal = 1` durante 50 velas produce **una**
  entrada, no 50.
- **186–188:** se puede entrar si no hay posición, o si la hay pero se va a cerrar en la misma
  apertura y `allow_reversal` está activo (por defecto, sí).
- **189–193:** el gestor de riesgo puede vetar la entrada. La entrada vetada **se pierde**: no
  se reintenta en la vela siguiente, porque la siguiente no es una transición.
- **195–202:** la entrada queda pendiente con la distancia de stop, el objetivo, el trailing,
  la convicción y el régimen **de la vela de la señal**.

**[Diseño] Consecuencias de las entradas por transición.**

1. Si un stop cierra la operación y la estrategia sigue en +1, **no se reabre**. Hay que
   esperar a que la estrategia pase por 0 (o −1) y vuelva a +1.
2. Una entrada rechazada por riesgo no se aplaza (pregunta final del Módulo VIII).
3. La alternativa (entrar siempre que el objetivo sea +1 y no haya posición) reabriría
   posiciones justo después de cada stop, en la misma dirección que acaba de fallar.

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 203–207

```python
        # final
        if acct.position is not None and cfg.execution.close_at_end:
            trades.append(self._close(acct, risk, ExitCheck(c[i1], "end_of_data"), i1, idx[i1]))
            final_equity = acct.cash
            rows[-1] = (final_equity, acct.cash, 0.0, 0.0, 0.0, rows[-1][5])
```
<!-- fmt: on -->

- **204–207:** con `close_at_end` (por defecto activo), la posición abierta al final se cierra
  al **cierre** de la última vela con deslizamiento y comisión (`end_of_data`). La última fila
  de equity se sustituye por el efectivo final. Así, el resultado final siempre incluye el coste
  de salir.

---

## 10.5 Costes: comisión y deslizamiento

<!-- fmt: off -->
`src/bybit_quant_lab/execution/costs.py` · líneas 1–39

```python
"""Modelo de costes: comisiones y slippage.

Todas las ejecuciones simuladas son órdenes a mercado o stops/TP disparados que se ejecutan
a mercado (comportamiento por defecto de TP/SL en Bybit), por lo que pagan comisión taker y
sufren slippage adverso de ``slippage_bps``.
"""

from __future__ import annotations

from dataclasses import dataclass

from bybit_quant_lab.config.models import CostConfig


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
<!-- fmt: on -->

**Términos.**

- **Comisión taker:** la que cobra el exchange a la orden que **consume** liquidez (orden a
  mercado). **Maker:** la que **añade** liquidez (orden límite que espera en el libro).
- **Deslizamiento (slippage):** diferencia entre el precio de referencia y el precio realmente
  obtenido. Se expresa en **puntos básicos** (bps): 1 bp = 0,01 % = 0,0001.
- **Nocional:** cantidad × precio. Es el valor de la posición, no el dinero aportado.

**Fórmulas** (con `s = slippage_bps / 10 000` y `d = +1` al comprar, `−1` al vender):

```text
precio_ejecución = referencia × (1 + s · d)
comisión         = |cantidad × precio_ejecución| × taker_fee
```

Al comprar, `d = +1` y se paga **más**; al vender, `d = −1` y se recibe **menos**. El
deslizamiento siempre perjudica.

**[Hecho]** Todas las ejecuciones simuladas pagan comisión **taker**: entradas y salidas por
señal son órdenes a mercado, y los stops y objetivos se modelan como órdenes que se ejecutan a
mercado al dispararse. `maker_fee` existe en la configuración, pero el motor nunca llama a
`fee(..., taker=False)` (Módulo III, sección 3.7).

**[Supuesto]** 0,055 % (taker) es la tarifa base publicada por Bybit para perpetuos USDT sin
nivel VIP en el momento de escribir el código; 2 bps de deslizamiento es una estimación, no
una medición. Ambos deben contrastarse con la cuenta y el mercado reales (Módulo XVII).

---

## 10.6 Funding: cómo se asigna cada pago a una vela

**Intuición.** En un perpetuo, cada 8 horas (habitualmente a las 00:00, 08:00 y 16:00 UTC) los
largos pagan a los cortos o al revés, según la **tasa de funding**. Es lo que mantiene el precio
del perpetuo cerca del índice al contado.

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 258–283

```python
    def _map_funding(
        self, funding: pd.Series | None, idx: pd.DatetimeIndex, i0: int, i1: int
    ) -> tuple[dict[int, float], bool, list[str]]:
        if not self.config.costs.use_funding:
            return {}, False, ["Funding desactivado en la configuración."]
        if funding is None or funding.empty:
            return (
                {},
                False,
                [
                    "Sin datos históricos de funding: no se aplica (no se simula). El resultado "
                    "neto excluye el coste/ingreso de funding."
                ],
            )
        seg_start, seg_end = idx[i0], idx[i1]
        warnings = []
        if funding.index.min() > seg_start + FUNDING_INTERVAL or funding.index.max() < (
            seg_end - FUNDING_INTERVAL
        ):
            warnings.append("El funding disponible no cubre todo el período simulado.")
        out: dict[int, float] = {}
        positions = idx.searchsorted(pd.DatetimeIndex(funding.index), side="left")
        for j, rate in zip(positions, funding.to_numpy(float), strict=True):
            if i0 < j <= i1 and not np.isnan(rate):
                out[int(j)] = out.get(int(j), 0.0) + float(rate)
        return out, True, warnings
```
<!-- fmt: on -->

- **261–271:** sin funding activado o sin datos, no se aplica y se añade una **advertencia**
  explícita. El resultado neto queda sin ese coste o ingreso; no se inventa una tasa.
- **274–277:** si la serie de funding no cubre el segmento, otra advertencia.
- **279:** `searchsorted(..., side="left")` devuelve, para cada marca de funding `t`, la primera
  vela con `open_time ≥ t`. Un pago en `(open[j−1], open[j]]` se asigna a la vela `j`.
- **281:** `i0 < j`: un pago asignado a la primera vela del segmento se ignora, porque el
  segmento empieza sin posición. `j ≤ i1`: los pagos posteriores al segmento, también.
- **282:** si dos pagos caen en la misma vela (temporalidades largas), se suman.

**Ejemplo.** Velas de 1 h; pago a las 08:00. La vela de las 08:00 tiene `open_time = 08:00`, así
que `j` es esa vela. En el paso 2 de esa vela se cobra a la posición que estaba abierta **al
final de la vela de las 07:00**, valorada a `open` de las 08:00. Una entrada ejecutada en la
apertura de las 08:00 (paso 4, después del funding) no paga ese pago.

**[Supuesto]** El pago se valora a `cantidad × open[j]`. En Bybit se usa el precio de marca
(mark price) en el momento del cobro; la apertura de la vela es una aproximación.

---

## 10.7 Stops, objetivos, gaps y liquidación con velas OHLC

**El problema.** Una vela dice que el precio estuvo entre `low` y `high`, pero no **en qué
orden**. Si una vela toca a la vez el stop y el objetivo, no se sabe cuál ocurrió primero.

<!-- fmt: off -->
`src/bybit_quant_lab/execution/fills.py` · líneas 1–74

```python
"""Resolución de stops, objetivos y liquidación con velas OHLC.

Las velas OHLC no revelan el orden real de los precios dentro de la vela. Reglas aplicadas:

1. **Gap en apertura**: si la apertura ya está más allá de un nivel (stop, liquidación u
   objetivo), la orden se ejecuta a la apertura (precio realmente disponible).
2. **Intravela, stop primero**: si en la misma vela se tocan el nivel adverso (stop o
   liquidación) y el objetivo, se asume que se tocó **primero el adverso**. Nunca se asume
   el resultado más favorable.
3. **Gap más allá de la liquidación**: se liquida (pérdida = margen aislado), aunque el
   stop estuviera más cerca de la entrada.
4. **Liquidación frente a stop**: el nivel adverso efectivo es el más cercano al precio de
   entrada (para largos, ``max(stop, liquidación)``). Si ambos coinciden prevalece la
   liquidación.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExitCheck:
    """Salida detectada: precio de referencia (antes de slippage) y motivo."""

    price: float
    reason: str


def _adverse(side: int, stop: float | None, liq: float | None) -> tuple[float | None, str]:
    levels = [
        (lvl, name) for lvl, name in ((liq, "liquidation"), (stop, "stop_loss")) if lvl is not None
    ]
    if not levels:
        return None, ""
    # Largo: el nivel más alto se toca primero al caer; corto: el más bajo.
    best = max(levels, key=lambda x: x[0]) if side > 0 else min(levels, key=lambda x: x[0])
    return best


def check_gap_exit(
    side: int, open_: float, stop: float | None, take_profit: float | None, liq: float | None
) -> ExitCheck | None:
    """Comprueba si la apertura ya ha superado algún nivel.

    Si la apertura supera el precio de liquidación, la posición se liquida aunque el stop
    estuviera más cerca: con margen aislado la pérdida queda limitada al margen y nunca se
    ejecuta un stop a un precio peor que la liquidación.
    """
    if liq is not None and (open_ <= liq if side > 0 else open_ >= liq):
        return ExitCheck(liq, "liquidation_gap")
    level, name = _adverse(side, stop, liq)
    if level is not None and (open_ <= level if side > 0 else open_ >= level):
        return ExitCheck(open_, f"{name}_gap")
    if take_profit is not None and (open_ >= take_profit if side > 0 else open_ <= take_profit):
        return ExitCheck(open_, "take_profit_gap")
    return None


def check_intrabar_exit(
    side: int,
    high: float,
    low: float,
    stop: float | None,
    take_profit: float | None,
    liq: float | None,
) -> ExitCheck | None:
    """Comprueba la vela con la regla conservadora *stop primero*."""
    level, name = _adverse(side, stop, liq)
    if level is not None and (low <= level if side > 0 else high >= level):
        return ExitCheck(level, name)
    if take_profit is not None and (high >= take_profit if side > 0 else low <= take_profit):
        return ExitCheck(take_profit, "take_profit")
    return None
```
<!-- fmt: on -->

Reglas, en lenguaje llano:

1. **Gap en apertura** (`check_gap_exit`, líneas 41–57): si el precio **abre** más allá del stop
   (por ejemplo, el stop está en 95 y la vela abre en 90), no hubo ningún momento en que se
   pudiera vender a 95. Se ejecuta a la apertura, 90. Lo mismo con el objetivo: un gap
   favorable se ejecuta a la apertura, no al objetivo
   (`test_take_profit_gap_fills_at_open_not_at_target`).
2. **Stop primero** (`check_intrabar_exit`, líneas 60–74): si en la vela se tocan el nivel
   adverso y el objetivo, se asume que se tocó **primero el adverso**. Es la hipótesis
   pesimista: nunca se atribuye al backtest el mejor caso posible.
3. **Nivel adverso efectivo** (`_adverse`, líneas 30–38): entre stop y liquidación, cuenta el
   que se alcanza antes. Para un largo, el más alto; para un corto, el más bajo.
4. **Gap más allá de la liquidación** (líneas 50–51): se liquida aunque el stop estuviera más
   cerca. Corrección M-02 de la auditoría (`a50ac62`): antes se ejecutaba como stop a la
   apertura, con una pérdida mayor que el margen aislado.

**Ejemplo de stop primero** (`tests/unit/test_engine.py`, líneas 67–76): largo a 100, stop en
95, objetivo en 105; la vela 3 tiene `high = 120` y `low = 80`. Toca ambos. El motor registra
`stop_loss` a 95, con pérdida.

**Ejemplo de gap** (líneas 88–94 del mismo archivo): stop en 95, la vela abre en 90. Salida
`stop_loss_gap` a 90.

**[Limitación]** "Stop primero" es conservador para la **salida**, pero no resuelve todo:
con velas largas (4 h), una entrada y su stop pueden ocurrir en la misma vela de un modo que el
modelo no ve. Los datos de menor temporalidad son la única forma de reducir esa ambigüedad.

**[Hecho] El precio de salida de un stop es el nivel, más deslizamiento.** En `_close`
(sección 10.9) el precio de referencia `ex.price` (el nivel del stop) pasa por
`fill_price` con dirección contraria a la posición: un largo que sale por stop a 95 con 2 bps
vende a `95 × (1 − 0,0002)`.

---

## 10.8 Trailing stop

<!-- fmt: off -->
`src/bybit_quant_lab/portfolio/position.py` · líneas 38–53

```python
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
<!-- fmt: on -->

**Intuición.** Un trailing stop "persigue" al precio: para un largo, se coloca a una distancia
fija por debajo del **máximo cierre** alcanzado y nunca baja.

- **47:** `extreme` guarda el cierre más favorable (empieza en el precio de entrada).
- **48–49:** el candidato es `extreme − distancia`; con `max`, el stop solo puede subir.
- **50–53:** espejo para cortos.

**Ejemplo** (`test_trailing_stop_moves_with_close`, `tests/unit/test_engine.py` líneas
105–111): entrada a 100 con stop 10 y trailing 10. Cierres 110, 120, 130 → stop 100, 110, 120.
La vela 6 abre en 130 y cae hasta 105: el stop de 120 se toca y la salida es a 120.

**[Diseño]** El trailing se actualiza con el **cierre** y en el paso 7, después de la
comprobación intravela. Usar el máximo de la vela sería más agresivo y crearía otra ambigüedad:
no se sabe si el máximo ocurrió antes o después del mínimo.

---

## 10.9 Apertura y cierre de una posición

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 285–333

```python
    def _open(
        self, acct: Account, pe: _PendingEntry, ref_price: float, i: int, ts: pd.Timestamp
    ) -> str | None:
        cfg = self.config
        fill = self.costs.fill_price(ref_price, pe.side)
        equity = acct.equity(ref_price)
        sizing = size_position(
            equity,
            acct.used_margin,
            fill,
            pe.stop_distance,
            cfg.risk,
            cfg.execution,
            cfg.costs,
            self.spec,
        )
        if sizing.qty <= 0:
            return sizing.reason
        qty = sizing.qty
        notional = qty * fill
        fee = self.costs.fee(notional)
        lev = cfg.execution.leverage
        mmr = cfg.execution.maintenance_margin_rate
        liq = None
        if cfg.execution.simulate_liquidation:
            liq = fill * (1 - 1 / lev + mmr) if pe.side > 0 else fill * (1 + 1 / lev - mmr)
        acct.cash -= fee
        acct.total_fees += fee
        acct.total_slippage += abs(fill - ref_price) * qty
        acct.traded_notional += notional
        acct.position = Position(
            side=pe.side,
            qty=qty,
            entry_price=fill,
            entry_time=ts,
            entry_bar=i,
            stop=fill - pe.side * pe.stop_distance,
            take_profit=fill + pe.side * pe.tp_distance if pe.tp_distance else None,
            trailing_distance=pe.trail_distance,
            liquidation_price=liq,
            margin=notional / lev,
            entry_fee=fee,
            entry_slippage=abs(fill - ref_price) * qty,
            conviction=pe.conviction,
            extreme=fill,
            equity_at_entry=equity,
            regime=pe.regime,
        )
        return None
```
<!-- fmt: on -->

- **289:** precio de ejecución con deslizamiento.
- **290:** la equity para dimensionar se mide al precio de referencia (la apertura).
- **291–302:** `size_position` (Módulo XI) devuelve la cantidad o un motivo de rechazo.
- **304–305:** nocional y comisión de entrada.
- **309–310:** precio de liquidación aproximado (Módulo XI).
- **311–314:** la comisión sale del efectivo **en el momento de entrar**; el deslizamiento no se
  resta aparte porque ya está dentro del precio.
- **321–322:** stop y objetivo se fijan **respecto al precio de ejecución**, no a la apertura.
- **325:** margen = nocional / apalancamiento.

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 335–382

```python
    def _close(
        self, acct: Account, risk: RiskManager, ex: ExitCheck, i: int, ts: pd.Timestamp
    ) -> TradeRecord:
        pos = acct.position
        assert pos is not None
        if ex.reason.startswith("liquidation"):
            # Margen aislado: se pierde el margen inicial completo (aproximación).
            fill = pos.entry_price - pos.side * pos.margin / pos.qty
        else:
            fill = self.costs.fill_price(ex.price, -pos.side)
        exit_slip = abs(fill - ex.price) * pos.qty
        exit_fee = self.costs.fee(pos.qty * fill)
        price_pnl = pos.side * (fill - pos.entry_price) * pos.qty
        acct.cash += price_pnl - exit_fee
        acct.realized_pnl += price_pnl
        acct.total_fees += exit_fee
        acct.total_slippage += exit_slip
        acct.traded_notional += pos.qty * fill
        entry_ref = pos.entry_price - pos.side * pos.entry_slippage / pos.qty
        gross = pos.side * (ex.price - entry_ref) * pos.qty
        fees = pos.entry_fee + exit_fee
        net = price_pnl - fees - pos.funding
        eq_entry = pos.equity_at_entry or acct.initial_capital
        record = TradeRecord(
            symbol=self.symbol,
            side="LONG" if pos.side > 0 else "SHORT",
            entry_time=pos.entry_time,
            exit_time=ts,
            entry_bar=pos.entry_bar,
            exit_bar=i,
            qty=pos.qty,
            entry_price=pos.entry_price,
            exit_price=fill,
            gross_pnl=gross,
            fees=fees,
            slippage_cost=pos.entry_slippage + exit_slip,
            funding=pos.funding,
            net_pnl=net,
            return_on_equity=net / eq_entry if eq_entry else 0.0,
            bars_held=i - pos.entry_bar + 1,
            exit_reason=ex.reason,
            conviction=pos.conviction,
            equity_at_entry=eq_entry,
            regime=pos.regime,
        )
        acct.position = None
        risk.on_trade_closed(i, ts, net)
        return record
```
<!-- fmt: on -->

Las magnitudes de una operación cerrada (con `L` = lado ±1, `q` = cantidad):

| Campo | Fórmula | Qué representa |
|---|---|---|
| `price_pnl` (línea 347) | `L · (salida_ejec − entrada_ejec) · q` | Resultado con los precios realmente obtenidos |
| `gross_pnl` (línea 354) | `L · (salida_ref − entrada_ref) · q` | Resultado **sin** deslizamiento ni comisiones |
| `slippage_cost` (línea 370) | desliz. entrada + desliz. salida | Pérdida por ejecutar peor que la referencia |
| `fees` (línea 355) | comisión entrada + comisión salida | |
| `funding` | suma de pagos durante la operación | Positivo = pagado |
| `net_pnl` (línea 356) | `price_pnl − fees − funding` | Lo que cambió el efectivo |

**Identidad contable** que comprueban las pruebas:

```text
net_pnl = gross_pnl − slippage_cost − fees − funding
```

- **353:** el precio de referencia de entrada se reconstruye deshaciendo el deslizamiento
  guardado.
- **348:** el efectivo recibe `price_pnl − comisión de salida`; la de entrada ya se descontó al
  abrir y el funding, al pagarse.
- **381:** el gestor de riesgo recibe el `net_pnl` para la racha de pérdidas.

**[Diseño] Liquidación (líneas 340–342).** Si la salida es por liquidación, el precio de salida
no es el nivel de liquidación más deslizamiento, sino el precio que hace perder **exactamente
el margen**: `entrada − L · margen / q`. Con margen aislado, eso equivale a
`entrada · (1 − L/apalancamiento)` (el llamado *precio de quiebra*). La diferencia entre el
precio de liquidación (que incluye el margen de mantenimiento) y ese precio queda contabilizada
en `slippage_cost`. Ejemplo verificado con el escenario de
`test_gap_through_liquidation_loses_isolated_margin_only` (sin costes, apalancamiento 10):
entrada 100, liquidación 90,5, precio de quiebra 90, cantidad 12,5 → `gross_pnl` = −118,75,
`slippage_cost` = 6,25 (0,5 × 12,5) y `net_pnl` = −125 = −margen. Ese "deslizamiento" es en
realidad el margen de mantenimiento perdido; al leer los totales de deslizamiento conviene
saberlo.

---

## 10.10 Una operación completa calculada a mano

Escenario: largo en BTCUSDT 1 h con la **configuración por defecto** (`configs/default.yaml`):
capital 10 000 USDT, riesgo 1 %, taker 0,055 %, deslizamiento 2 bps, apalancamiento 3,
liquidación simulada. Distancia de stop 600 USDT y objetivo 1200 USDT (como un stop de 2 ATR
con `take_profit_r = 2`). Un pago de funding del 0,01 % a las 08:00.

Datos (hora UTC):

| Vela | Hora | open | high | low | close | signal |
|---|---|---|---|---|---|---|
| 0 | 05:00 | 30 000 | 30 100 | 29 900 | 30 000 | 0 |
| 1 | 06:00 | 30 000 | 30 150 | 29 950 | 30 100 | **1** |
| 2 | 07:00 | 30 100 | 30 300 | 30 050 | 30 250 | 1 |
| 3 | 08:00 | 30 250 | 30 500 | 30 200 | 30 400 | 1 |
| 4 | 09:00 | 30 400 | 31 400 | 30 350 | 31 350 | 1 |
| 5 | 10:00 | 31 350 | 31 400 | 31 300 | 31 380 | 1 |

**Paso 1. Señal.** Al cierre de la vela 1, `signal` pasa de 0 a 1: es una transición. Se
programa una entrada para la apertura de la vela 2.

**Paso 2. Precio de entrada** (vela 2, referencia `open = 30 100`):

```text
entrada_ejec = 30 100 × (1 + 0,0002) = 30 106,02
```

**Paso 3. Tamaño** (detalle en el Módulo XI). Riesgo = 10 000 × 1 % = 100 USDT. Coste estimado
por unidad = stop + precio × 2 × (comisión + deslizamiento):

```text
por_unidad = 600 + 30 106,02 × 2 × (0,00055 + 0,0002) = 600 + 45,159 = 645,159
q_bruta    = 100 / 645,159 = 0,1550004
```

Topes: exposición 3 × 10 000 / 30 106,02 = 0,996; apalancamiento máximo 5 → 1,661; margen
disponible (reserva 20 %) 0,8 × 10 000 × 3 / 30 106,02 = 0,797. Ninguno es menor que 0,155.
Redondeo hacia abajo al paso 0,001 → **q = 0,155 BTC**.

**Paso 4. Costes de entrada.**

```text
nocional            = 0,155 × 30 106,02         = 4 666,4331
comisión entrada    = 4 666,4331 × 0,00055      = 2,5665382
desliz. entrada     = 0,155 × (30 106,02 − 30 100) = 0,155 × 6,02 = 0,933100
margen              = 4 666,4331 / 3            = 1 555,4777
stop                = 30 106,02 − 600           = 29 506,02
objetivo            = 30 106,02 + 1 200         = 31 306,02
liquidación         = 30 106,02 × (1 − 1/3 + 0,005) ≈ 20 221,21   (muy por debajo del stop)
efectivo            = 10 000 − 2,5665382         = 9 997,433462
```

**Paso 5. Valoración al cierre de la vela 2** (close 30 250):

```text
no_realizado = (30 250 − 30 106,02) × 0,155 = 143,98 × 0,155 = 22,3169
equity       = 9 997,433462 + 22,3169 = 10 019,750362
```

**Paso 6. Funding** (apertura de la vela 3, 08:00, `open = 30 250`, tasa 0,0001):

```text
pago     = (+1) × 0,155 × 30 250 × 0,0001 = 0,468875   (el largo paga)
efectivo = 9 997,433462 − 0,468875 = 9 996,964587
```

Al cierre de la vela 3 (close 30 400): no realizado = 293,98 × 0,155 = 45,5669; equity =
10 042,531487.

**Paso 7. Salida** (vela 4). El mínimo, 30 350, no toca el stop (29 506,02). El máximo, 31 400,
supera el objetivo (31 306,02). Salida `take_profit` con referencia 31 306,02:

```text
salida_ejec     = 31 306,02 × (1 − 0,0002) = 31 299,758796
desliz. salida  = 0,155 × (31 306,02 − 31 299,758796) = 0,155 × 6,261204 = 0,970487
comisión salida = 0,155 × 31 299,758796 × 0,00055 = 4 851,462613 × 0,00055 = 2,6683044
```

**Paso 8. Resultado de la operación.**

```text
price_pnl     = (31 299,758796 − 30 106,02) × 0,155 = 1 193,738796 × 0,155 = 185,029513
gross_pnl     = (31 306,02 − 30 100) × 0,155       = 1 206,02 × 0,155     = 186,933100
slippage_cost = 0,933100 + 0,970487                                      =   1,903587
fees          = 2,5665382 + 2,6683044                                    =   5,2348426
funding       =                                                              0,468875
net_pnl       = 185,029513 − 5,2348426 − 0,468875                        = 179,325796
comprobación  = 186,933100 − 1,903587 − 5,2348426 − 0,468875             = 179,325796
equity final  = 10 000 + 179,325796                                      = 10 179,325796
```

Los términos están redondeados; con todos los decimales, ambas sumas dan 179,3257957.

De 186,93 USDT de movimiento de precio, los costes se llevan 7,61 (un 4 %). Con objetivos más
cortos o temporalidades menores, la proporción crece (Módulo XII, sección de costes).

**Paso 9. Después.** La estrategia sigue en `signal = 1` en las velas 4 y 5, pero no hay
transición: el motor **no reabre**.

**Reproducción con el código real:**

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config.loader import load_config
from bybit_quant_lab.strategies.base import empty_signal_frame

idx = pd.date_range("2024-01-01 05:00", periods=6, freq="1h", tz="UTC", name="open_time")
datos = pd.DataFrame(
    {
        "open": [30000, 30000, 30100, 30250, 30400, 31350],
        "high": [30100, 30150, 30300, 30500, 31400, 31400],
        "low": [29900, 29950, 30050, 30200, 30350, 31300],
        "close": [30000, 30100, 30250, 30400, 31350, 31380],
        "volume": 100.0,
    },
    index=idx,
).astype(float)
senales = empty_signal_frame(idx)
senales["signal"] = [0, 1, 1, 1, 1, 1]
senales["conviction"] = [0.0, 1, 1, 1, 1, 1]
senales["stop_distance"] = 600.0
senales["take_profit_distance"] = 1200.0
funding = pd.Series([0.0001], index=[pd.Timestamp("2024-01-01 08:00", tz="UTC")])

res = run_backtest(datos, senales, load_config(), "BTCUSDT", "1h", funding=funding)
t = res.trades.iloc[0]
for campo in ["entry_time", "exit_time", "qty", "entry_price", "exit_price", "exit_reason"]:
    print(f"{campo:14s} {t[campo]}")
for campo in ["gross_pnl", "slippage_cost", "fees", "funding", "net_pnl"]:
    print(f"{campo:14s} {t[campo]:.6f}")
print()
print(res.equity[["equity", "cash", "unrealized", "position", "in_position"]].round(6).to_string())
print("equity final:", round(res.final_equity, 6))
print("advertencias:", res.warnings)
```
*Salida real:*

```text
entry_time     2024-01-01 07:00:00+00:00
exit_time      2024-01-01 09:00:00+00:00
qty            0.155
entry_price    30106.02
exit_price     31299.758796000002
exit_reason    take_profit
gross_pnl      186.933100
slippage_cost  1.903587
fees           5.234843
funding        0.468875
net_pnl        179.325796

                                 equity          cash  unrealized  position  in_position
open_time                                                                               
2024-01-01 05:00:00+00:00  10000.000000  10000.000000      0.0000     0.000        False
2024-01-01 06:00:00+00:00  10000.000000  10000.000000      0.0000     0.000        False
2024-01-01 07:00:00+00:00  10019.750362   9997.433462     22.3169     0.155         True
2024-01-01 08:00:00+00:00  10042.531487   9996.964587     45.5669     0.155         True
2024-01-01 09:00:00+00:00  10179.325796  10179.325796      0.0000     0.000        False
2024-01-01 10:00:00+00:00  10179.325796  10179.325796      0.0000     0.000        False
equity final: 10179.325796
advertencias: ['Especificaciones de BTCUSDT no verificadas con instruments-info (valores de referencia).']
```

Todo coincide con el cálculo a mano. Detalles que la tabla de equity enseña:

- En la vela 4 `in_position` es `False`: la posición se cerró **durante** la vela y la fila se
  registra al cierre. Para la métrica de exposición (Módulo XII), esa vela no cuenta como "en
  posición".
- La advertencia recuerda que las especificaciones de BTCUSDT (paso de cantidad, mínimos) son
  valores de referencia no verificados con la API (Módulo XI).
- **[Diseño]** La equity intermedia valora la posición al cierre **sin** descontar los costes
  de salida. Es la convención habitual (mark-to-market), pero hace la curva ligeramente más
  optimista que el valor de liquidar en ese momento.

**Comprobación.** Repite el cálculo con deslizamiento 0 y comisión 0. ¿Cuál sería `net_pnl`?

**Respuesta:**

Entrada 30 100, objetivo 31 300; por unidad = 600 → q = 100/600 = 0,16666 → 0,166.
`net = (31 300 − 30 100) × 0,166 − 0,166 × 30 250 × 0,0001 = 199,2 − 0,502 = 198,698`. El
tamaño cambia porque el dimensionamiento también incluye los costes estimados.

---

## 10.11 Reversiones y entradas rechazadas

Con `allow_reversal: true`, si la señal pasa de +1 a −1 el motor cierra el largo y abre el corto
**en la misma apertura** (primero la salida, luego la entrada; paso 4):

*Ejemplo ejecutable:*

```python
import sys

sys.path.insert(0, ".")  # para importar los ayudantes de tests/conftest.py

from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.risk.instruments import InstrumentSpec
from tests.conftest import make_bars, manual_signals, zero_cost_config

spec = InstrumentSpec(
    "TEST", tick_size=0.01, qty_step=0.001, min_qty=0.001, max_qty=1e9, min_notional=0.0
)
datos = make_bars([100, 100, 100, 104, 104, 100, 100])
senales = manual_signals(datos.index, {1: 1, 3: -1}, stop=5)
res = run_backtest(datos, senales, zero_cost_config(), "TEST", "1h", spec=spec)
columnas = [
    "side",
    "entry_time",
    "exit_time",
    "qty",
    "entry_price",
    "exit_price",
    "exit_reason",
    "net_pnl",
]
print(res.trades[columnas].to_string())
```
*Salida real:*

```text
    side                entry_time                 exit_time    qty  entry_price  exit_price     exit_reason  net_pnl
0   LONG 2024-01-01 02:00:00+00:00 2024-01-01 04:00:00+00:00  20.00        100.0       104.0  signal_reverse    80.00
1  SHORT 2024-01-01 04:00:00+00:00 2024-01-01 06:00:00+00:00  20.16        104.0       100.0     end_of_data    80.64
```

Lectura: señal larga en la vela 1 → entrada a la apertura de la 2 (100). Señal corta en la 3 →
en la apertura de la 4 se cierra el largo (`signal_reverse`, 104) y se abre el corto (104). El
corto se cierra al final de los datos (`end_of_data`). La segunda cantidad es mayor porque la
equity creció con la primera operación (riesgo 1 % de 10 080 sobre un stop de 5 → 20,16).

Las entradas rechazadas (por riesgo, por posición abierta o por tamaño insuficiente) se guardan
en `res.rejected_signals` con hora, lado y motivo. El informe HTML las resume (Módulo XV).

---

## 10.12 El resultado: `BacktestResult`

<!-- fmt: off -->
`src/bybit_quant_lab/backtesting/results.py` · líneas 11–46

```python
@dataclass
class BacktestResult:
    """Resultado completo de una simulación.

    ``equity``: una fila por vela simulada (cierre) con ``equity``, ``cash``, ``unrealized``,
    ``position`` (cantidad con signo), ``margin_used``, ``drawdown`` e ``in_position``.
    ``trades``: una fila por operación cerrada (ver ``TradeRecord``).
    """

    label: str
    symbol: str
    timeframe: str
    initial_capital: float
    equity: pd.DataFrame
    trades: pd.DataFrame
    risk_events: list[dict[str, Any]]
    rejected_signals: list[dict[str, Any]]
    totals: dict[str, float]
    funding_applied: bool
    warnings: list[str] = field(default_factory=list)
    params: dict[str, Any] = field(default_factory=dict)

    @property
    def final_equity(self) -> float:
        """Equity al cierre de la última vela."""
        return float(self.equity["equity"].iloc[-1]) if len(self.equity) else self.initial_capital

    @property
    def start(self) -> pd.Timestamp | None:
        """Primera vela simulada."""
        return self.equity.index[0] if len(self.equity) else None

    @property
    def end(self) -> pd.Timestamp | None:
        """Última vela simulada."""
        return self.equity.index[-1] if len(self.equity) else None
```
<!-- fmt: on -->

- `equity`: una fila por vela; incluye `drawdown = equity / máximo_acumulado − 1` (líneas 214–215
  de `engine.py`).
- `trades`: una fila por operación con los campos de `TradeRecord`
  (`portfolio/position.py`, líneas 56–83).
- `totals`: comisiones, deslizamiento, funding y nocional negociado **acumulados**.
- `funding_applied`: si se aplicó funding real. Si es `False`, el neto excluye el funding.
- `warnings`: advertencias que el informe muestra siempre.

---

## 10.13 Cómo las pruebas protegen el motor

| Prueba | Archivo | Qué impide |
|---|---|---|
| `test_signal_executes_at_next_open` | `test_engine.py` | Ejecutar al cierre de la señal |
| `test_fees_and_slippage_reduce_net_exactly` | `test_engine.py` | Costes mal sumados |
| `test_stop_and_target_same_bar_assumes_stop_first` | `test_engine.py` | Elegir el caso favorable |
| `test_gap_through_stop_fills_at_open` | `test_engine.py` | Ejecutar stops a precios que no existieron |
| `test_trailing_stop_moves_with_close` | `test_engine.py` | Trailing que retrocede |
| `test_funding_applied_only_when_data_present` | `test_engine.py` | Inventar funding |
| `test_backtest_is_deterministic` | `test_engine.py` | Resultados no reproducibles |
| `test_short_trade_with_fees_slippage_and_funding_by_hand` | `test_audit_engine.py` | Errores de signo en cortos |
| `test_gap_through_liquidation_loses_isolated_margin_only` | `test_audit_engine.py` | Pérdidas mayores que el margen (M-02) |
| `test_signal_on_last_bar_is_never_executed` | `test_audit_engine.py` | Ejecutar en una vela inexistente |
| `test_segment_start_does_not_enter_on_preexisting_signal` | `test_audit_engine.py` | Entradas artificiales al empezar un segmento |

La prueba de auditoría del corto calcula el resultado esperado con aritmética explícita,
independiente del motor:

<!-- fmt: off -->
`tests/unit/test_audit_engine.py` · líneas 49–81

```python
def test_short_trade_with_fees_slippage_and_funding_by_hand() -> None:
    # Velas: open[t] = close[t-1]. Señal SHORT al cierre de la vela 1, FLAT al cierre de la 3.
    df = make_bars([100, 100, 100, 95, 90, 90], spread=0.1)
    sig = manual_signals(df.index, {1: -1, 3: 0}, stop=20)
    fee, slip = 0.001, 0.001
    funding = pd.Series([0.0005], index=[df.index[3]])  # pago a las 03:00, posición abierta
    res = run_backtest(df, sig, _cfg(fee, 10.0), "TEST", "1h", spec=SPEC, funding=funding)
    t = res.trades.iloc[0]

    entry_ref, exit_ref = 100.0, 95.0  # open[2] y open[4]
    entry_fill = entry_ref * (1 - slip)  # venta: precio peor = más bajo
    exit_fill = exit_ref * (1 + slip)  # recompra: precio peor = más alto
    qty = _floor_qty(10_000 * 0.01 / (20 + entry_fill * 2 * (fee + slip)))
    fees = fee * qty * (entry_fill + exit_fill)
    funding_paid = -1 * qty * 100.0 * 0.0005  # el corto cobra con tasa positiva
    net = (entry_fill - exit_fill) * qty - fees - funding_paid

    assert t["side"] == "SHORT" and t["qty"] == pytest.approx(qty)
    assert t["entry_time"] == df.index[2] and t["exit_time"] == df.index[4]
    assert t["entry_price"] == pytest.approx(entry_fill)
    assert t["exit_price"] == pytest.approx(exit_fill)
    assert t["fees"] == pytest.approx(fees)
    assert t["funding"] == pytest.approx(funding_paid) and t["funding"] < 0
    assert t["gross_pnl"] == pytest.approx((entry_ref - exit_ref) * qty)
    assert t["slippage_cost"] == pytest.approx(
        qty * (entry_ref - entry_fill + exit_fill - exit_ref)
    )
    assert t["net_pnl"] == pytest.approx(net)
    assert t["net_pnl"] == pytest.approx(
        t["gross_pnl"] - t["fees"] - t["slippage_cost"] - t["funding"]
    )
    assert res.final_equity == pytest.approx(10_000 + net)
    assert res.totals["funding"] == pytest.approx(funding_paid)
```
<!-- fmt: on -->

---

## 10.14 Supuestos y limitaciones del motor

| Tema | Estado | Detalle |
|---|---|---|
| Ejecución a la siguiente apertura | [Diseño] | Evita usar el cierre conocido como precio de ejecución |
| Stop primero | [Diseño] | Conservador; no resuelve toda la ambigüedad intravela |
| Comisión siempre taker | [Supuesto] | Sin órdenes límite simuladas |
| Deslizamiento fijo en bps | [Supuesto] | No depende del tamaño, la volatilidad ni el libro |
| Liquidación con margen de mantenimiento fijo | [Limitación] | Bybit usa niveles por tamaño (Módulo XI) |
| Funding valorado a la apertura | [Supuesto] | Bybit usa el precio de marca |
| Precios no redondeados al tick | [Limitación] | `tick_size` existe en `InstrumentSpec` pero ningún módulo de `src` lo usa |
| Una posición por símbolo | [Diseño] | `max_open_positions` solo admite 1 |
| Huecos en los datos | [Limitación] | La posición se mantiene a través del hueco (M-06) |
| Margen de mantenimiento contado como deslizamiento en liquidaciones | [Hecho] | Sección 10.9 |
| Equity sin costes de salida | [Diseño] | Mark-to-market convencional |

### Comprobación final del módulo

Un largo tiene el stop en 95 y el objetivo en 110. La vela siguiente abre en 93, sube a 112 y
cierra en 108. ¿Cómo sale la operación y a qué precio de referencia?

**Respuesta:**

Por `stop_loss_gap` a 93. El paso 3 (gap) se evalúa en la apertura, antes que la comprobación
intravela: la apertura ya está por debajo del stop, así que la posición se cierra a 93 (más
deslizamiento) y el máximo de 112 ya no importa.

<div style="page-break-before: always;"></div>

# Módulo XI. Gestión del riesgo y contabilidad

El Módulo X mostró **qué** hace el motor en cada vela. Este módulo explica **cuánto** arriesga
en cada operación, **cuándo** deja de operar y **cómo** lleva las cuentas. El código está en
`src/bybit_quant_lab/risk/` (`sizing.py`, `limits.py`, `instruments.py`) y
`src/bybit_quant_lab/portfolio/account.py`.

> **[Hecho]** Estos mecanismos limitan pérdidas **dentro de la simulación**. No garantizan
> nada en una cuenta real: los precios reales pueden saltar más allá de cualquier stop, y la
> liquidación de Bybit no se calcula exactamente como aquí.

---

## 11.0 Tres capas de protección distintas

<!-- fmt: off -->
`src/bybit_quant_lab/risk/limits.py` · líneas 1–19

```python
"""Límites de riesgo del sistema, independientes de las estrategias.

Definiciones (todas evaluadas con equity *mark-to-market* al **cierre** de cada vela):

* **Pérdida diaria**: ``equity_cierre - equity_inicio_día_UTC``, donde ``equity_inicio_día``
  es la equity al cierre de la última vela del día UTC anterior (o el capital inicial). Incluye
  PnL realizado y no realizado. Si la pérdida alcanza ``max_daily_loss * equity_inicio_día``
  se bloquean nuevas entradas hasta el siguiente día UTC (``block``) o, además, se cierra la
  posición en la siguiente apertura (``close_and_block``).
* **Drawdown máximo**: ``1 - equity / máximo_histórico_equity``. Al alcanzar ``max_drawdown``
  se detienen las nuevas entradas durante el resto de la simulación (kill-switch).
* **Pérdidas consecutivas**: operaciones con PnL neto < 0 incrementan la racha, > 0 la
  reinician (== 0 no la modifica). Al llegar a ``max_consecutive_losses`` se pausan las
  entradas ``pause_bars_after_losses`` velas y la racha se reinicia. La pausa no anula
  ningún otro límite: al terminar, siguen aplicándose todos.

El stop de estrategia (por operación), estos límites del sistema y la liquidación del
exchange (simulada por el motor) son mecanismos distintos y se registran por separado.
"""
```
<!-- fmt: on -->

| Capa | Quién la define | Qué protege | Dónde |
|---|---|---|---|
| Stop de la estrategia | Cada estrategia (`stop_distance`) | Una operación | `engine.py`, `fills.py` |
| Límites del sistema | `RiskConfig` | La cuenta completa | `risk/limits.py` |
| Liquidación | El exchange (simulado) | El margen aislado de una posición | `engine.py`, `fills.py` |

**[Diseño]** Las tres son independientes y se registran por separado: una salida por stop se
anota como `stop_loss`, una por límite del sistema como `risk_limit_close` y una liquidación
como `liquidation` o `liquidation_gap`. Mezclarlas impediría saber qué falló.

**Analogía.** El stop es el cinturón de seguridad de un viaje; los límites del sistema, la
decisión de no volver a conducir hoy después de dos sustos; la liquidación, el airbag que el
fabricante dispara cuando el choque ya ocurrió. En el código, cada una corresponde a una
comprobación distinta del bucle (pasos 3, 5 y 6 de la sección 10.2).

---

## 11.1 Contabilidad de la cuenta

<!-- fmt: off -->
`src/bybit_quant_lab/portfolio/account.py` · líneas 1–48

```python
"""Cuenta de margen aislado con una posición como máximo por símbolo.

Contabilidad:

* ``cash`` = capital inicial + PnL realizado - comisiones - funding pagado.
* ``equity(price)`` = ``cash`` + PnL no realizado a ``price``.
* ``used_margin`` = nocional de entrada / apalancamiento.

El apalancamiento solo afecta al margen y al precio de liquidación, **no** al PnL de una
cantidad dada de contratos.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from bybit_quant_lab.portfolio.position import Position


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
<!-- fmt: on -->

**Términos.**

- **Efectivo (`cash`):** capital inicial + PnL realizado − comisiones − funding pagado. El
  motor descuenta la comisión de entrada al abrir, el funding al pagarse y suma
  `price_pnl − comisión de salida` al cerrar (sección 10.9).
- **PnL no realizado:** ganancia o pérdida de la posición abierta si se cerrara al precio
  actual, **sin** costes de salida (`Position.unrealized`).
- **Equity:** efectivo + no realizado. Es lo que "vale" la cuenta en cada momento.
- **Margen inicial (`used_margin`):** nocional de entrada / apalancamiento. Es la parte de la
  equity que el exchange bloquea como garantía.
- **Margen aislado:** cada posición tiene su propio margen; si se liquida, se pierde ese margen
  y nada más. (En margen **cruzado**, toda la cuenta respalda las posiciones.)

**[Hecho] El apalancamiento no cambia el PnL.** Con la misma cantidad de contratos, ganar o
perder 1 USDT por movimiento de 1 USDT no depende del apalancamiento; solo cambian el margen
bloqueado y el precio de liquidación (cabecera, líneas 9–10). Lo comprueba
`test_leverage_does_not_change_pnl` (`tests/unit/test_risk.py`, líneas 145–155): mismas
operaciones con apalancamiento 2 y 5 → mismo `net_pnl`.

**Error común.** Pensar que "con apalancamiento 10 gano diez veces más". Con apalancamiento 10
**puedes** abrir una posición diez veces mayor que tu margen, pero el tamaño lo decide el
dimensionamiento por riesgo (sección 11.2), no el apalancamiento.

**[Hallazgo]** `available_margin` (líneas 46–48) y `history` (línea 32) no se usan en ningún
módulo de `src`: el dimensionamiento calcula el margen disponible por su cuenta (sección 11.2).
Es código sin efecto, no un error (Módulo III, sección 3.7).

---

## 11.2 Dimensionamiento por riesgo

**Intuición.** En lugar de decidir "compro 0,1 BTC", se decide "estoy dispuesto a perder el 1 %
de la cuenta si salta el stop". La cantidad se deduce de esa pérdida máxima y de la distancia
al stop: si el stop está lejos, se compra menos; si está cerca, más.

<!-- fmt: off -->
`src/bybit_quant_lab/risk/sizing.py` · líneas 1–71

```python
"""Dimensionamiento de posición basado en riesgo.

``qty = (equity * risk_per_trade) / (stop_distance + costes_estimados_por_unidad)``

Los costes estimados por unidad incluyen comisión taker y slippage de entrada y salida. El
resultado se limita por exposición por símbolo, apalancamiento máximo, margen disponible
(respetando la reserva) y tamaño máximo del instrumento, y se redondea **hacia abajo**.
"""

from __future__ import annotations

from dataclasses import dataclass

from bybit_quant_lab.config.models import CostConfig, ExecutionConfig, RiskConfig
from bybit_quant_lab.risk.instruments import InstrumentSpec


@dataclass(frozen=True)
class SizingResult:
    """Resultado del dimensionamiento: ``qty > 0`` o ``qty == 0`` con motivo."""

    qty: float
    reason: str = "ok"
    capped_by: str | None = None


def liquidation_distance(price: float, leverage: float, mmr: float) -> float:
    """Distancia aproximada a liquidación con margen aislado: ``price * (1/lev - mmr)``."""
    return price * max(1.0 / leverage - mmr, 0.0)


def size_position(
    equity: float,
    used_margin: float,
    price: float,
    stop_distance: float,
    risk: RiskConfig,
    execution: ExecutionConfig,
    costs: CostConfig,
    spec: InstrumentSpec,
) -> SizingResult:
    """Cantidad de contratos para entrar a ``price`` con stop a ``stop_distance``."""
    if equity <= 0:
        return SizingResult(0.0, "equity_non_positive")
    if not stop_distance > 0 or price <= 0:
        return SizingResult(0.0, "invalid_stop")
    if execution.simulate_liquidation and stop_distance >= liquidation_distance(
        price, execution.leverage, execution.maintenance_margin_rate
    ):
        return SizingResult(0.0, "stop_beyond_liquidation")
    slip = costs.slippage_bps / 10_000
    per_unit = stop_distance + price * 2 * (costs.taker_fee + slip)
    qty = equity * risk.risk_per_trade / per_unit
    caps = {
        "symbol_exposure": equity * risk.max_symbol_exposure / price,
        "max_leverage": equity * risk.max_leverage / price,
        "available_margin": max(equity * (1 - risk.margin_reserve) - used_margin, 0.0)
        * execution.leverage
        / price,
        "instrument_max_qty": spec.max_qty,
    }
    capped_by = None
    for name, cap in caps.items():
        if cap < qty:
            qty, capped_by = cap, name
    qty = spec.round_qty(qty)
    if qty < spec.min_qty:
        return SizingResult(0.0, "below_min_qty", capped_by)
    if qty * price < spec.min_notional:
        return SizingResult(0.0, "below_min_notional", capped_by)
    return SizingResult(qty, "ok", capped_by)
```
<!-- fmt: on -->

**Fórmula base** (con `E` = equity, `r` = `risk_per_trade`, `d` = distancia al stop en USDT,
`P` = precio de ejecución, `f` = comisión taker, `s` = deslizamiento como fracción):

```text
coste_por_unidad = d + P · 2 · (f + s)          (salir por el stop + costes de entrada y salida)
q_bruta          = E · r / coste_por_unidad
```

**Por qué se suman los costes (línea 52).** Si el stop salta, la pérdida real no es solo
`d × q`: también se pagan dos comisiones y dos deslizamientos. Incluirlos hace que la pérdida
total al tocar el stop sea aproximadamente `E · r`, no algo mayor. Con `d = 600` y
`P ≈ 30 106` (sección 10.10), los costes añaden 45,16 USDT por unidad, un 7,5 % más.

**Topes (líneas 54–65).** La cantidad se reduce al menor de:

| Tope | Fórmula | Defecto (`default.yaml`) |
|---|---|---|
| `symbol_exposure` | `E · max_symbol_exposure / P` | nocional ≤ 3 × E |
| `max_leverage` | `E · max_leverage / P` | nocional ≤ 5 × E |
| `available_margin` | `(E · (1 − margin_reserve) − margen_usado) · apalancamiento / P` | nocional ≤ 0,8 × 3 × E = 2,4 × E |
| `instrument_max_qty` | `spec.max_qty` | 100 BTC |

**[Hecho] Con la configuración por defecto, solo el tope de margen puede actuar.** Sin posición
abierta, el tope de margen permite un nocional de 2,4 × E, menor que 3 × E y que 5 × E. Los topes
de exposición y apalancamiento máximo quedan siempre por encima. Solo actuarían si se cambia la
reserva o el apalancamiento.

**¿Cuándo actúa el tope?** Cuando el nocional deseado supera 2,4 × E, es decir, cuando
`E · r / (d + 2P(f + s)) × P > 2,4 E`. Con `r = 1 %` y costes de 0,15 % del precio:

```text
d/P + 0,0015 < 0,01 / 2,4 = 0,004167   →   d/P < 0,267 %
```

Con un stop más cercano que el 0,27 % del precio (habitual en velas de 5 minutos con stops de
1–2 ATR), la posición queda limitada por el margen y el riesgo real por operación es **menor**
que el 1 %.

**Redondeo y mínimos (líneas 66–70).** La cantidad se redondea **hacia abajo** al paso del
instrumento (nunca aumenta el riesgo). Si queda por debajo de la cantidad mínima o del nocional
mínimo, la entrada se rechaza con el motivo correspondiente.

**Stop más allá de la liquidación (líneas 47–50).** Si el stop está más lejos que el precio de
liquidación, el stop nunca se alcanzaría antes que la liquidación: la entrada se rechaza
(`stop_beyond_liquidation`).

Tres casos con la configuración por defecto, a 30 106,02 USDT:

*Ejemplo ejecutable:*

```python
from bybit_quant_lab.config.loader import load_config
from bybit_quant_lab.risk import size_position
from bybit_quant_lab.risk.instruments import get_spec

cfg = load_config()
spec = get_spec("BTCUSDT")
precio = 30_106.02
for stop in (600.0, 60.0, 15_000.0):
    r = size_position(10_000, 0.0, precio, stop, cfg.risk, cfg.execution, cfg.costs, spec)
    print(
        f"stop={stop:>8.0f}  qty={r.qty:<6}  motivo={r.reason:<24} tope={r.capped_by}  "
        f"nocional={r.qty * precio:,.2f}"
    )
```
*Salida real:*

```text
stop=     600  qty=0.155   motivo=ok                       tope=None  nocional=4,666.43
stop=      60  qty=0.797   motivo=ok                       tope=available_margin  nocional=23,994.50
stop=   15000  qty=0.0     motivo=stop_beyond_liquidation  tope=None  nocional=0.00
```

Lectura:

- **Stop 600:** el caso de la sección 10.10. Ningún tope actúa.
- **Stop 60 (0,2 % del precio):** la fórmula pediría 100 / (60 + 45,16) ≈ 0,951 BTC, pero el
  margen limita a 0,797 BTC (nocional 23 994,50 ≈ 2,4 × 10 000). Si salta el stop, la pérdida
  será ≈ 0,797 × 105,16 ≈ 83,8 USDT, no 100.
- **Stop 15 000:** con apalancamiento 3 la liquidación está a ≈ 32,8 % del precio
  (`1/3 − 0,005`), es decir, a ≈ 9 885 USDT. El stop está más lejos: entrada rechazada.

**Comprobación.** Con equity 10 000, riesgo 1 %, stop de 5 USDT, precio 100 y sin costes, ¿qué
cantidad sale? (`test_size_uses_stop_distance_and_costs`.)

**Respuesta:**

100 / 5 = 20 unidades. En la prueba se desactivan los topes (`max_symbol_exposure=100`,
`margin_reserve=0`, apalancamiento 10) para que ninguno actúe.

---

## 11.3 Especificaciones del instrumento

<!-- fmt: off -->
`src/bybit_quant_lab/risk/instruments.py` · líneas 1–67

```python
"""Especificaciones de instrumentos (precisión, tamaños mínimos y máximos).

Los valores por defecto son **referencias** para BTCUSDT y ETHUSDT lineales y deben
contrastarse con ``GET /v5/market/instruments-info`` (``BybitPublicClient.fetch_instrument_info``
y ``spec_from_bybit``), ya que Bybit puede modificarlos.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class InstrumentSpec:
    """Restricciones de cantidad y precio de un contrato lineal."""

    symbol: str
    tick_size: float
    qty_step: float
    min_qty: float
    max_qty: float
    min_notional: float = 5.0
    verified: bool = False

    def round_qty(self, qty: float) -> float:
        """Redondea hacia abajo al múltiplo de ``qty_step`` (nunca aumenta el riesgo)."""
        if qty <= 0:
            return 0.0
        steps = math.floor(qty / self.qty_step + 1e-9)
        decimals = max(0, -math.floor(math.log10(self.qty_step)))
        return round(steps * self.qty_step, decimals)


DEFAULT_SPECS: dict[str, InstrumentSpec] = {
    "BTCUSDT": InstrumentSpec(
        "BTCUSDT", tick_size=0.1, qty_step=0.001, min_qty=0.001, max_qty=100.0
    ),
    "ETHUSDT": InstrumentSpec(
        "ETHUSDT", tick_size=0.01, qty_step=0.01, min_qty=0.01, max_qty=1000.0
    ),
}


def get_spec(symbol: str) -> InstrumentSpec:
    """Especificación por defecto del símbolo (genérica y no verificada si no existe)."""
    spec = DEFAULT_SPECS.get(symbol.upper())
    if spec is not None:
        return spec
    return InstrumentSpec(
        symbol.upper(), tick_size=0.0001, qty_step=0.001, min_qty=0.001, max_qty=1e9
    )


def spec_from_bybit(info: dict[str, Any]) -> InstrumentSpec:
    """Construye la especificación a partir de un registro de ``instruments-info``."""
    lot, price = info["lotSizeFilter"], info["priceFilter"]
    return InstrumentSpec(
        symbol=str(info["symbol"]),
        tick_size=float(price["tickSize"]),
        qty_step=float(lot["qtyStep"]),
        min_qty=float(lot["minOrderQty"]),
        max_qty=float(lot.get("maxMktOrderQty") or lot["maxOrderQty"]),
        min_notional=float(lot.get("minNotionalValue") or 0.0),
        verified=True,
    )
```
<!-- fmt: on -->

- **`qty_step`:** incremento mínimo de cantidad (0,001 BTC).
- **`min_qty` / `max_qty`:** cantidad mínima y máxima por orden.
- **`min_notional`:** nocional mínimo (5 USDT por defecto).
- **`tick_size`:** incremento mínimo de precio.
- **`verified`:** `True` solo si la especificación se construyó con datos de la API
  (`spec_from_bybit`).

**Línea 31: el `+ 1e-9`.** `0,3 / 0,1` en coma flotante da `2,9999999999999996`
(Módulo II). Sin la pequeña tolerancia, `floor` daría 2 en lugar de 3 y se perdería un paso.
La línea 33 redondea al número de decimales del paso para eliminar residuos como
`0,15500000000000003`.

*Ejemplo ejecutable:*

```python
import math

from bybit_quant_lab.risk.instruments import get_spec

print("0.3 / 0.1 =", 0.3 / 0.1, "-> floor:", math.floor(0.3 / 0.1))
spec = get_spec("BTCUSDT")
for q in (0.3, 0.1550004, 0.0009):
    print(q, "->", spec.round_qty(q))
print("verificada:", spec.verified)
```
*Salida real:*

```text
0.3 / 0.1 = 2.9999999999999996 -> floor: 2
0.3 -> 0.3
0.1550004 -> 0.155
0.0009 -> 0.0
verificada: False
```

**[Limitación]** Las especificaciones por defecto (líneas 36–43) son **valores de referencia**
no verificados con la API, y el motor lo advierte en cada resultado (sección 10.10). Ninguna
orden de la CLI llama hoy a `spec_from_bybit` para sustituirlas. **[Limitación]** `tick_size`
no se usa: los precios de stop y objetivo no se redondean al tick (sección 10.14).

---

## 11.4 Liquidación aproximada

**Intuición.** Con margen aislado, si las pérdidas de la posición consumen el margen (menos un
pequeño colchón llamado **margen de mantenimiento**), el exchange cierra la posición a la fuerza.
Ese precio es el **precio de liquidación**.

**Fórmula usada** (`engine.py`, línea 310; `L` = lado, `A` = apalancamiento, `m` =
`maintenance_margin_rate`):

```text
largo: liq = entrada · (1 − 1/A + m)
corto: liq = entrada · (1 + 1/A − m)
```

**Derivación para un largo.** El margen es `entrada · q / A`. Se liquida cuando la pérdida
alcanza el margen menos el mantenimiento (`m · entrada · q`):

```text
(entrada − liq) · q = entrada · q / A − m · entrada · q
liq = entrada · (1 − 1/A + m)
```

**Ejemplo** (sección 10.10): entrada 30 106,02, A = 3, m = 0,005 →
`30 106,02 × 0,671667 ≈ 20 221,21`. El stop (29 506,02) está mucho más cerca: la liquidación
solo importaría con un gap enorme.

**Precio de quiebra.** El precio al que se pierde **exactamente** el margen:
`entrada · (1 − 1/A)` para un largo. El motor ejecuta las liquidaciones a ese precio
(sección 10.9), así que la pérdida es el margen completo.

**[Limitación]** En Bybit, la tasa de mantenimiento depende del **nivel de riesgo** (*risk
limit*) según el tamaño de la posición, y el cálculo real incluye otros términos. El
comentario de `configs/default.yaml` (línea 28) lo advierte: "aproximación; Bybit usa niveles
de riesgo". Con apalancamiento 3 y stops de pocos ATR, la liquidación casi nunca interviene;
con apalancamientos altos, la aproximación pesa más.

**Comprobación.** Con apalancamiento 10 y m = 0,005, ¿a qué distancia porcentual de la entrada
se liquida un largo?

**Respuesta:**

`1/10 − 0,005 = 0,095`: un 9,5 % por debajo de la entrada. Es el caso de la prueba de
auditoría M-02 (entrada 100, liquidación 90,5).

---

## 11.5 Límites del sistema: `RiskManager`

<!-- fmt: off -->
`src/bybit_quant_lab/risk/limits.py` · líneas 44–131

```python
@dataclass
class RiskManager:
    """Estado y reglas de los límites de riesgo."""

    config: RiskConfig
    initial_equity: float
    day: int | None = None
    day_start_equity: float = 0.0
    last_equity: float = 0.0
    peak_equity: float = 0.0
    consecutive_losses: int = 0
    pause_until_bar: int = -1
    daily_blocked: bool = False
    halted: bool = False
    events: list[RiskEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.day_start_equity = self.last_equity = self.peak_equity = self.initial_equity

    def on_bar_open(self, ts: pd.Timestamp, day: int | None = None) -> None:
        """Gestiona el cambio de día UTC (reinicia la referencia diaria y el bloqueo diario).

        ``day`` es un identificador entero del día UTC (opcional, para evitar recalcularlo).
        """
        if day is None:
            day = int(ts.floor("D").as_unit("s").value // 86_400)
        if self.day is None:
            self.day = day
            return
        if day != self.day:
            self.day = day
            self.day_start_equity = self.last_equity
            if self.daily_blocked:
                self.events.append(RiskEvent(str(ts), "daily_block_lifted", "nuevo día UTC"))
            self.daily_blocked = False

    def on_bar_close(self, ts: pd.Timestamp, equity: float) -> bool:
        """Actualiza límites con la equity al cierre. Devuelve ``True`` si hay que cerrar."""
        self.last_equity = equity
        self.peak_equity = max(self.peak_equity, equity)
        force_close = False
        daily_pnl = equity - self.day_start_equity
        if (
            not self.daily_blocked
            and daily_pnl <= -self.config.max_daily_loss * self.day_start_equity
        ):
            self.daily_blocked = True
            self.events.append(
                RiskEvent(
                    str(ts),
                    "daily_loss_limit",
                    f"pnl_dia={daily_pnl:.2f} ref={self.day_start_equity:.2f}",
                )
            )
            force_close |= self.config.daily_loss_action == "close_and_block"
        dd = 1 - equity / self.peak_equity if self.peak_equity > 0 else 0.0
        if not self.halted and dd >= self.config.max_drawdown:
            self.halted = True
            self.events.append(RiskEvent(str(ts), "max_drawdown_halt", f"drawdown={dd:.4f}"))
            force_close |= self.config.drawdown_action == "close_and_block"
        return force_close

    def on_trade_closed(self, bar_index: int, ts: pd.Timestamp, net_pnl: float) -> None:
        """Actualiza la racha de pérdidas y activa la pausa si corresponde."""
        if net_pnl < 0:
            self.consecutive_losses += 1
        elif net_pnl > 0:
            self.consecutive_losses = 0
        if self.consecutive_losses >= self.config.max_consecutive_losses:
            self.pause_until_bar = bar_index + self.config.pause_bars_after_losses
            self.events.append(
                RiskEvent(
                    str(ts),
                    "loss_streak_pause",
                    f"{self.consecutive_losses} pérdidas; pausa hasta vela {self.pause_until_bar}",
                )
            )
            self.consecutive_losses = 0

    def can_open(self, bar_index: int) -> tuple[bool, str]:
        """Indica si se permiten nuevas entradas decididas en la vela ``bar_index``."""
        if self.halted:
            return False, "max_drawdown_halt"
        if self.daily_blocked:
            return False, "daily_loss_limit"
        if bar_index < self.pause_until_bar:
            return False, "loss_streak_pause"
        return True, "ok"
```
<!-- fmt: on -->

### Pérdida diaria (líneas 63–98)

**Definición.**

```text
pnl_día = equity_cierre − equity_inicio_día
bloqueo si pnl_día ≤ −max_daily_loss · equity_inicio_día
```

- `equity_inicio_día` es la equity al cierre de la **última vela del día UTC anterior**
  (`on_bar_open`, línea 75, toma `last_equity`). En el primer día, el capital inicial.
- Incluye PnL **realizado y no realizado**: una posición abierta que pierde un 6 % bloquea
  aunque no se haya cerrado.
- `block` impide nuevas entradas hasta el siguiente día UTC; `close_and_block` además cierra la
  posición en la siguiente apertura (`risk_limit_close`).

**Ejemplo** (`test_daily_loss_blocks_until_next_utc_day`, líneas 96–105): equity de inicio 1000,
cierre a 940 → `pnl_día = −60 ≤ −0,05 × 1000 = −50` → bloqueo. Al empezar el día siguiente se
levanta el bloqueo y la nueva referencia es 940.

**[Diseño] Por qué "día UTC".** Bybit y la mayoría de los datos de criptomonedas usan UTC; es
una frontera fija e independiente del huso horario del usuario.

### Drawdown máximo (líneas 99–103)

```text
drawdown = 1 − equity / máximo_histórico_de_equity
```

Al alcanzar `max_drawdown` (15 %), `halted` pasa a `True` **para el resto de la simulación**
(kill-switch). No hay reactivación.

**Ejemplo** (`test_pause_does_not_override_other_limits`): capital 1000, equity 850 → drawdown
15 % ≥ 10 % configurado en la prueba → `halted`.

### Racha de pérdidas (líneas 106–121)

- `net_pnl < 0` suma 1 a la racha; `net_pnl > 0` la reinicia; exactamente 0 no la cambia.
- Al llegar a 3 (por defecto), las entradas se pausan `pause_bars_after_losses` velas (24) y la
  racha vuelve a 0.
- La racha usa el PnL **neto** (con comisiones y funding): una operación que gana 0,50 USDT de
  precio y paga 1 USDT de comisiones cuenta como pérdida.

### Orden de prioridad (líneas 123–131)

`can_open` devuelve el **primer** motivo que bloquea: drawdown, después pérdida diaria, después
pausa. La pausa no levanta ningún otro límite (cabecera, líneas 14–15).

### Ejemplo en el motor: tres stops seguidos

*Ejemplo ejecutable:*

```python
import sys

sys.path.insert(0, ".")  # ayudantes de tests/conftest.py

from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.risk.instruments import InstrumentSpec
from tests.conftest import make_bars, manual_signals, zero_cost_config

spec = InstrumentSpec(
    "TEST", tick_size=0.01, qty_step=0.001, min_qty=0.001, max_qty=1e9, min_notional=0.0
)
cierres = [100, 100, 100, 90, 100] * 5  # cinco caídas iguales
mapa = {}
for k in range(5):
    mapa[5 * k + 1], mapa[5 * k + 4] = 1, 0  # largo en 1, 6, 11...; FLAT en 4, 9, 14...
datos = make_bars(cierres, spread=0.1)
senales = manual_signals(datos.index, mapa, stop=5)
cfg = zero_cost_config(max_consecutive_losses=3, pause_bars_after_losses=100)
res = run_backtest(datos, senales, cfg, "TEST", "1h", spec=spec)
print(res.trades[["entry_bar", "exit_bar", "exit_reason", "qty", "net_pnl"]].to_string())
print("eventos:", res.risk_events)
print("rechazadas:", res.rejected_signals)
```
*Salida real:*

```text
   entry_bar  exit_bar exit_reason     qty  net_pnl
0          2         3   stop_loss  20.000  -100.00
1          7         8   stop_loss  19.800   -99.00
2         12        13   stop_loss  19.602   -98.01
eventos: [{'time': '2024-01-01 13:00:00+00:00', 'kind': 'loss_streak_pause', 'detail': '3 pérdidas; pausa hasta vela 113'}]
rechazadas: [{'time': '2024-01-01 16:00:00+00:00', 'side': 1, 'reason': 'loss_streak_pause'}, {'time': '2024-01-01 21:00:00+00:00', 'side': 1, 'reason': 'loss_streak_pause'}]
```

Lectura:

- Cada operación pierde el 1 % de la equity **del momento**: 100, 99, 98,01. El riesgo es
  proporcional a la equity, así que tras pérdidas las posiciones se reducen.
- La tercera pérdida se cierra en la vela 13 → pausa hasta la vela 13 + 100 = 113.
- Las señales de las velas 16 y 21 (transiciones a LONG) se rechazan con `loss_streak_pause`.
  Para el motor, una entrada decidida en la vela `i` se permite si `i ≥ pause_until_bar`.

**[Limitación] Límites evaluados solo al cierre.** El drawdown y la pérdida diaria se miden con
la equity al **cierre** de cada vela. Dentro de una vela la pérdida puede ser mayor, y una sola
vela (o un gap) puede llevar el drawdown mucho más allá del 15 % antes de que el límite
reaccione. El límite **no es un stop**: impide nuevas entradas; con `block` (por defecto) no
cierra la posición abierta.

---

## 11.6 Una prueba de regresión sobre el día UTC

<!-- fmt: off -->
`tests/unit/test_risk.py` · líneas 158–171

```python
@pytest.mark.parametrize("unit", ["ns", "us", "ms", "s"])
def test_daily_reference_resets_regardless_of_index_resolution(unit: str) -> None:
    # Regresión: el identificador de día no debe depender de la resolución del índice.
    # Día 1: -3 %; día 2: otro -3 %. Con reinicio diario correcto nunca se alcanza el 5 %
    # diario; sin reinicio la pérdida acumulada (~6 %) activaría el límite.
    closes = [100.0] * 24 + [97.0] * 24 + [94.0] * 24 + [94.0] * 4
    df = make_bars(closes, spread=0.01, freq="1h")
    df.index = df.index.as_unit(unit)
    sig = manual_signals(df.index, {1: 1}, stop=10)
    cfg = zero_cost_config(max_daily_loss=0.05, risk_per_trade=0.1)
    res = run_backtest(df, sig, cfg, "TEST", "1h", spec=SPEC)
    assert res.trades["qty"].iloc[0] == pytest.approx(100.0)
    assert res.final_equity == pytest.approx(10_000 - 100 * (100 - 94))
    assert not any(e["kind"] == "daily_loss_limit" for e in res.risk_events)
```
<!-- fmt: on -->

**Qué comprueba.** Dos días seguidos con una pérdida del 3 % cada uno. Con el reinicio diario
correcto, ningún día alcanza el 5 %; si el día no se reiniciara, la pérdida acumulada (~6 %)
activaría el límite. La prueba se repite con el índice en nanosegundos, microsegundos,
milisegundos y segundos (`@pytest.mark.parametrize`).

**Historia.** La prueba y el identificador entero de día se añadieron en el mismo commit
(`2f60aca`); en el historial confirmado no hay ninguna versión con el error. Es una prueba
**preventiva**: pandas 3 puede crear índices con resolución distinta de nanosegundos, y una
conversión que supusiera nanosegundos calcularía días erróneos (sección 10.3).

---

## 11.7 Validaciones de configuración

<!-- fmt: off -->
`src/bybit_quant_lab/config/models.py` · líneas 63–76

```python
class RiskConfig(_Strict):
    """Límites de riesgo del sistema (independientes de las estrategias)."""

    risk_per_trade: float = Field(0.01, gt=0, le=0.1)
    max_drawdown: float = Field(0.15, gt=0, le=1)
    drawdown_action: Literal["block", "close_and_block"] = "block"
    max_daily_loss: float = Field(0.05, gt=0, le=1)
    daily_loss_action: Literal["block", "close_and_block"] = "block"
    max_consecutive_losses: int = Field(3, ge=1)
    pause_bars_after_losses: int = Field(24, ge=1)
    max_open_positions: int = Field(1, ge=1, le=1)
    max_symbol_exposure: float = Field(3.0, gt=0, description="Nocional máximo / equity")
    max_leverage: float = Field(5.0, ge=1)
    margin_reserve: float = Field(0.2, ge=0, lt=1, description="Fracción de equity no usable")
```
<!-- fmt: on -->

- Los `Field(..., gt=0, le=0.1)` impiden, por ejemplo, un riesgo por operación del 50 %.
- `max_open_positions` solo admite 1 (`ge=1, le=1`): el motor no gestiona carteras.
- La validación cruzada de `AppConfig` (líneas 121–128) exige
  `execution.leverage ≤ risk.max_leverage` (`test_leverage_must_not_exceed_limit`).

**[Limitación]** Recuerda la sección 2.15: `model_copy(update=...)` no revalida. Las pruebas lo
usan para construir configuraciones extremas; desde YAML y la CLI siempre se valida.

---

## 11.8 Resumen

| Elemento | Valor por defecto | Etiqueta |
|---|---|---|
| Riesgo por operación | 1 % de la equity, incluidos costes estimados | [Diseño] |
| Tope efectivo de nocional | 2,4 × equity (margen con reserva del 20 %) | [Hecho] |
| Pérdida diaria | 5 % sobre equity de inicio del día UTC, mark-to-market | [Diseño] |
| Drawdown máximo | 15 %, kill-switch sin reactivación | [Diseño] |
| Racha de pérdidas | 3 → pausa de 24 velas | [Diseño] |
| Liquidación | Margen de mantenimiento fijo 0,5 % | [Limitación] |
| Especificaciones | Referencias no verificadas | [Pendiente] de contrastar con la API |
| Límites evaluados al cierre | Sin control intravela | [Limitación] |

### Comprobación final del módulo

Equity 20 000 USDT, riesgo 1 %, precio 2 000 USDT (ETHUSDT), stop a 10 USDT, comisión 0,055 %,
deslizamiento 2 bps, configuración por defecto. ¿Qué cantidad se abre y qué tope actúa?

**Respuesta:**

Precio de ejecución ≈ 2 000,4. Coste por unidad = 10 + 2 000,4 × 2 × 0,00075 ≈ 13,0006.
`q_bruta = 200 / 13,0006 ≈ 15,38`. Tope de margen = 20 000 × 0,8 × 3 / 2 000,4 ≈ 23,99: no
actúa. Redondeo al paso 0,01 de ETHUSDT → **15,38 ETH**, sin tope (nocional ≈ 30 766, es decir,
1,54 × equity).

<div style="page-break-before: always;"></div>

# Módulo XII. Métricas de rendimiento y riesgo

Una simulación produce una curva de equity y una lista de operaciones. Las **métricas** resumen
esas dos tablas en números comparables. Este módulo explica cada métrica del proyecto: qué
mide, cómo se calcula, cuándo no se calcula y cómo se malinterpreta.

Código: `src/bybit_quant_lab/analytics/metrics.py` y `analytics/breakdowns.py`. Documentación
de referencia: `docs/metrics.md`, coherente con el código en la versión actual.

> **[Hecho]** Todas las cifras de este módulo proceden de ejemplos construidos a mano o de
> datos **sintéticos**. Ninguna dice nada sobre la rentabilidad de una estrategia en Bybit.

---

## 12.1 La cabecera: todas las convenciones en un lugar

<!-- fmt: off -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 1–33

```python
"""Cálculo de métricas. Fórmulas y convenciones (ver ``docs/metrics.md``):

* Retornos por vela: ``r_t = E_t / E_{t-1} - 1`` sobre la equity al cierre, incluyendo las
  velas sin posición (retorno 0). El primer retorno usa el capital inicial como ``E_{-1}``.
* Anualización: mercado 24/7, año de 365 días -> ``N = 525600 / minutos_por_vela``.
* Sharpe = ``mean(r) / std(r, ddof=1) * sqrt(N)`` con tasa libre de riesgo 0.
* Sortino = ``mean(r) / DD * sqrt(N)`` con ``DD = sqrt(mean(min(r, 0)^2))``.
* CAGR = ``(E_final / E_0)^(365 / días) - 1`` solo si ``días >= min_days_for_cagr``.
* Profit factor = suma de ganancias netas / |suma de pérdidas netas|.
* Expectativa = media del PnL neto por operación.
* Exposición = fracción de velas con posición abierta al cierre.
* Rotación = nocional negociado total / equity media.

Las métricas que no pueden calcularse válidamente se devuelven como ``None`` y se añade una
advertencia. Una muestra pequeña de operaciones también genera advertencia.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

from bybit_quant_lab.backtesting.results import BacktestResult
from bybit_quant_lab.timeframes import bars_per_year

MIN_BARS_FOR_RATIOS = 30
#: Con menos operaciones (y exposición no continua) Sharpe/Sortino no se presentan: con
#: 1-9 operaciones la serie de retornos está dominada por unos pocos episodios.
MIN_TRADES_FOR_RATIOS = 10
CONTINUOUS_EXPOSURE = 0.9
```
<!-- fmt: on -->

Dos decisiones condicionan todo lo demás:

1. **Los retornos se calculan por vela sobre la equity**, no por operación. Incluyen las velas
   sin posición (retorno 0). El Sharpe mide la estrategia **completa**, incluido el tiempo en
   efectivo.
2. **El año tiene 525 600 minutos** (365 × 24 × 60), porque el mercado cripto no cierra:

<!-- fmt: off -->
`src/bybit_quant_lab/timeframes.py` · líneas 18–18

```python
MINUTES_PER_YEAR = 365 * 24 * 60  # mercado cripto 24/7, año de 365 días
```
<!-- fmt: on -->

<!-- fmt: off -->
`src/bybit_quant_lab/timeframes.py` · líneas 43–45

```python
def bars_per_year(timeframe: str) -> float:
    """Número de velas por año (365 días, 24 h)."""
    return MINUTES_PER_YEAR / timeframe_minutes(timeframe)
```
<!-- fmt: on -->

| Temporalidad | Velas por año (`N`) | √N |
|---|---|---|
| 5m | 105 120 | 324,22 |
| 15m | 35 040 | 187,19 |
| 1h | 8 760 | 93,59 |
| 4h | 2 190 | 46,80 |

**[Diseño]** En acciones se usan 252 días hábiles; aplicar ese número a cripto infravaloraría
la anualización. La tasa libre de riesgo se fija en 0.

---

## 12.2 Retornos por vela

<!-- fmt: off -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 36–40

```python
def bar_returns(equity: pd.Series, initial: float) -> pd.Series:
    """Retornos simples por vela, empezando desde el capital inicial."""
    prev = equity.shift(1)
    prev.iloc[0] = initial
    return equity / prev - 1
```
<!-- fmt: on -->

```text
r_t = E_t / E_{t−1} − 1,      con E_{−1} = capital inicial
```

`shift(1)` desplaza la serie una posición (Módulo V); el primer valor, que quedaría `NaN`, se
sustituye por el capital inicial.

**[Hecho]** La primera fila de equity de cualquier simulación es el capital inicial: en la
primera vela del segmento no puede haber posición, porque toda entrada se decide al cierre de
una vela y se ejecuta en la siguiente (Módulo X). El primer retorno es, por tanto, 0.

---

## 12.3 Sharpe y Sortino

**Intuición.** El **ratio de Sharpe** responde: "¿cuánto retorno obtengo por cada unidad de
variabilidad?". Dos estrategias que ganan lo mismo no son iguales si una lo hace con
oscilaciones enormes. El **Sortino** solo penaliza la variabilidad **a la baja**: subir mucho no
debería contar como riesgo.

**Fórmulas** (con `r` = retornos por vela, `n` = número de velas, `N` = velas por año):

```text
Sharpe  = media(r) / desv(r, ddof=1) · √N
Sortino = media(r) / DD · √N,      DD = √( media( min(r, 0)² ) )
```

- `ddof=1` divide entre `n − 1` (desviación muestral, Módulo VI).
- `DD` (*downside deviation*) promedia sobre **todas** las velas, poniendo 0 en las positivas.
- `√N` convierte un ratio por vela en anual, **suponiendo** retornos independientes entre velas.

<!-- fmt: off -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 95–111

```python
    sharpe = sortino = None
    exposure = float(result.equity["in_position"].mean()) if n_bars else 0.0
    few_trades = n_trades < MIN_TRADES_FOR_RATIOS and exposure < CONTINUOUS_EXPOSURE
    if few_trades:
        warnings.append(
            f"Solo {n_trades} operaciones (< {MIN_TRADES_FOR_RATIOS}) con exposición no "
            "continua: Sharpe/Sortino no se presentan por no ser representativos."
        )
    elif n_bars >= MIN_BARS_FOR_RATIOS:
        std = float(rets.std(ddof=1))
        if std > 0:
            sharpe = float(rets.mean() / std * math.sqrt(ann))
        downside = float(np.sqrt(np.mean(np.minimum(rets.to_numpy(), 0.0) ** 2)))
        if downside > 0:
            sortino = float(rets.mean() / downside * math.sqrt(ann))
    else:
        warnings.append(f"Menos de {MIN_BARS_FOR_RATIOS} velas: Sharpe/Sortino no calculados.")
```
<!-- fmt: on -->

**Cálculo a mano.** Cinco velas de 1 h con retornos `r = [0; 0,01; −0,01; 0,02; 0]`:

```text
media     = (0 + 0,01 − 0,01 + 0,02 + 0) / 5 = 0,004
desvíos   = −0,004; 0,006; −0,014; 0,016; −0,004
cuadrados = 16; 36; 196; 256; 16   (× 10⁻⁶)   → suma = 520 × 10⁻⁶
varianza  = 520 × 10⁻⁶ / 4 = 130 × 10⁻⁶       → desv = 0,0114018
Sharpe por vela = 0,004 / 0,0114018 = 0,35082
Sharpe anual    = 0,35082 × √8760 = 0,35082 × 93,5949 = 32,84

DD        = √( (0² + 0² + 0,01² + 0² + 0²) / 5 ) = √(2 × 10⁻⁵) = 0,0044721
Sortino   = 0,004 / 0,0044721 × 93,5949 = 83,71
```

*Ejemplo ejecutable:*

```python
import math

import numpy as np

r = np.array([0.0, 0.01, -0.01, 0.02, 0.0])
n_anual = 365 * 24
sharpe = r.mean() / r.std(ddof=1) * math.sqrt(n_anual)
dd = math.sqrt(np.mean(np.minimum(r, 0) ** 2))
sortino = r.mean() / dd * math.sqrt(n_anual)
print(f"Sharpe = {sharpe:.2f}   Sortino = {sortino:.2f}")
```
*Salida real:*

```text
Sharpe = 32.84   Sortino = 83.71
```

Un Sharpe de 32 es absurdo: cinco velas no permiten estimar nada. Por eso el código **no
calcula** los ratios:

- con menos de 30 velas (`MIN_BARS_FOR_RATIOS`, línea 29), o
- con menos de 10 operaciones **y** una exposición inferior al 90 % (líneas 97–102). Con pocas
  operaciones, la serie de retornos está dominada por unos pocos episodios. La excepción de
  exposición continua existe para los benchmarks como comprar y mantener, que tienen una sola
  "operación" pero están en el mercado todo el tiempo.

En esos casos la métrica vale `None` y se añade una advertencia. El informe muestra "n/d", no
un número.

**[Limitación]** `√N` supone retornos independientes. Las posiciones que duran varias velas
producen retornos autocorrelacionados, y el Sharpe anualizado puede quedar sesgado. No se
corrige (`docs/metrics.md`, "Validez y muestras pequeñas").

**Error común.** Comparar un Sharpe calculado por operación con uno calculado por vela, o uno de
5m con uno de 4h sin entender la anualización. Dentro del proyecto todos se calculan igual.

**Comprobación.** Si en el ejemplo se añaden 5 velas más con retorno 0 (sin posición), ¿sube o
baja el Sharpe?

**Respuesta:**

Baja. La media pasa de 0,004 a 0,002 (misma suma, el doble de velas); la desviación también
baja, pero menos (de 0,0114 a ≈ 0,0079). Resultado ≈ 23,7. El tiempo sin posición diluye el
retorno medio por vela.

---

## 12.4 Drawdown: profundidad, duración y recuperación

<!-- fmt: off -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 43–73

```python
def drawdown_stats(equity: pd.Series) -> dict[str, Any]:
    """Drawdown máximo, duración máxima (velas) y velas de recuperación del máximo drawdown."""
    if equity.empty:
        return {
            "max_drawdown": 0.0,
            "max_dd_duration_bars": 0,
            "max_dd_recovery_bars": None,
            "max_dd_start": None,
            "max_dd_trough": None,
            "max_dd_end": None,
        }
    values = equity.to_numpy(float)
    peak = np.maximum.accumulate(values)
    dd = values / peak - 1
    trough = int(np.argmin(dd))
    peak_idx = int(np.argmax(values[: trough + 1])) if trough > 0 else 0
    rec = np.nonzero(values[trough:] >= peak[trough])[0]
    recovery = int(rec[0]) if len(rec) else None
    longest, cur = 0, 0
    for under in dd < 0:
        cur = cur + 1 if under else 0
        longest = max(longest, cur)
    idx = equity.index
    return {
        "max_drawdown": max(0.0, float(-np.min(dd))),
        "max_dd_duration_bars": longest,
        "max_dd_recovery_bars": recovery,
        "max_dd_start": str(idx[peak_idx]),
        "max_dd_trough": str(idx[trough]),
        "max_dd_end": str(idx[trough + recovery]) if recovery is not None else None,
    }
```
<!-- fmt: on -->

**Términos.**

- **Drawdown** en `t`: `1 − E_t / máximo(E_0..E_t)`. Cuánto se ha caído desde el último máximo.
- **Máximo drawdown:** el mayor drawdown de toda la serie.
- **Duración máxima:** la racha más larga de velas **consecutivas** por debajo del máximo previo.
- **Recuperación:** velas desde el **valle** del máximo drawdown hasta volver al máximo previo.
  `None` si no se recupera dentro del período.

**Cálculo a mano** (`test_drawdown_duration_and_recovery_by_hand`):

| Vela | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Equity | 100 | 110 | 99 | 95 | 105 | 111 | 108 | 112 |
| Máximo previo | 100 | 110 | 110 | 110 | 110 | 111 | 111 | 112 |
| Drawdown | 0 | 0 | 10,0 % | **13,6 %** | 4,5 % | 0 | 2,7 % | 0 |

- Máximo drawdown = 1 − 95/110 = 13,64 %: pico en la vela 1, valle en la 3.
- Recuperación: desde la vela 3, el primer valor ≥ 110 es 111 en la vela 5 → **2 velas**.
- Duración máxima: velas 2, 3 y 4 bajo el máximo → **3**. (La vela 6 forma una racha de 1.)

*Ejemplo ejecutable:*

```python
import pandas as pd

from bybit_quant_lab.analytics import drawdown_stats

idx = pd.date_range("2024-01-01", periods=8, freq="1h", tz="UTC")
s = pd.Series([100, 110, 99, 95, 105, 111, 108, 112], index=idx, dtype=float)
for clave, valor in drawdown_stats(s).items():
    print(f"{clave:22s} {round(valor, 4) if isinstance(valor, float) else valor}")
```
*Salida real:*

```text
max_drawdown           0.1364
max_dd_duration_bars   3
max_dd_recovery_bars   2
max_dd_start           2024-01-01 01:00:00+00:00
max_dd_trough          2024-01-01 03:00:00+00:00
max_dd_end             2024-01-01 05:00:00+00:00
```

**Detalles del código.**

- **55:** `np.maximum.accumulate` es el máximo acumulado (como `cummax` en pandas).
- **58:** el pico es la **primera** posición del máximo antes del valle.
- **62–64:** la duración se calcula con un bucle de racha; **no** tiene por qué corresponder al
  episodio del máximo drawdown. Un drawdown poco profundo pero largo puede dar la duración
  máxima.

**Comprobación.** ¿Puede la duración máxima ser mayor que la distancia entre el pico y la
recuperación del máximo drawdown?

**Respuesta:**

Sí. Son dos medidas distintas: la duración es la racha más larga bajo el agua de **cualquier**
episodio; la recuperación se refiere solo al episodio del drawdown más profundo.

---

## 12.5 CAGR

```text
CAGR = (E_final / E_0)^(365 / días) − 1,      días = velas × minutos_por_vela / 1440
```

<!-- fmt: off -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 112–116

```python
    cagr = None
    if days >= min_days_for_cagr and final > 0:
        cagr = (final / init) ** (365.0 / days) - 1
    else:
        warnings.append(f"Período de {days:.0f} días < {min_days_for_cagr}: CAGR no calculado.")
```
<!-- fmt: on -->

**Intuición.** La tasa de crecimiento anual compuesta que habría producido el mismo resultado.

**Por qué exige 180 días.** Ganar un 5 % en 10 días, anualizado, da
`1,05^(36,5) − 1 ≈ 494 %`. Es una extrapolación sin sentido. Con menos de
`min_days_for_cagr` (180) días, la métrica es `None`.

**[Limitación]** `días` se calcula con el **número de velas**, no con el calendario. Si faltan
velas (huecos, M-06), los días se subestiman y el exponente `365/días` crece: el CAGR queda
inflado.

---

## 12.6 Métricas por operación

<!-- fmt: off -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 123–166

```python
    net = trades["net_pnl"].astype(float) if n_trades else pd.Series(dtype=float)
    wins, losses = net[net > 0], net[net < 0]
    gross_win, gross_loss = float(wins.sum()), float(-losses.sum())
    dd = drawdown_stats(eq)
    gross_total = float(trades["gross_pnl"].sum()) if n_trades else 0.0
    m: dict[str, Any] = {
        "label": result.label,
        "symbol": result.symbol,
        "timeframe": result.timeframe,
        "start": str(result.start) if result.start is not None else None,
        "end": str(result.end) if result.end is not None else None,
        "bars": n_bars,
        "days": round(days, 2),
        "initial_capital": init,
        "final_equity": final,
        "net_profit": final - init,
        "net_profit_pct": final / init - 1,
        "gross_profit_before_costs": gross_total,
        "cumulative_return": final / init - 1,
        "cagr": _safe(cagr) if cagr is not None else None,
        "sharpe": _safe(sharpe) if sharpe is not None else None,
        "sortino": _safe(sortino) if sortino is not None else None,
        **dd,
        "num_trades": n_trades,
        "win_rate": float((net > 0).mean()) if n_trades else None,
        "avg_win": float(wins.mean()) if len(wins) else None,
        "avg_loss": float(losses.mean()) if len(losses) else None,
        "profit_factor": (gross_win / gross_loss) if gross_loss > 0 else None,
        "expectancy": float(net.mean()) if n_trades else None,
        "expectancy_pct_equity": float(trades["return_on_equity"].mean()) if n_trades else None,
        "exposure": exposure,
        "turnover": result.totals["traded_notional"] / float(eq.mean()) if n_bars else 0.0,
        "total_fees": result.totals["fees"],
        "total_slippage": result.totals["slippage"],
        "total_costs": result.totals["fees"] + result.totals["slippage"],
        "total_funding": result.totals["funding"],
        "funding_applied": result.funding_applied,
        "avg_bars_in_trade": float(trades["bars_held"].mean()) if n_trades else None,
        "long_trades": int((trades["side"] == "LONG").sum()) if n_trades else 0,
        "short_trades": int((trades["side"] == "SHORT").sum()) if n_trades else 0,
        "rejected_signals": len(result.rejected_signals),
        "risk_events": len(result.risk_events),
        "warnings": warnings + list(result.warnings),
    }
```
<!-- fmt: on -->

**Cálculo a mano** con las doce operaciones de `test_metrics_match_hand_computation`:
`[50, −20, 30, −10, −40, 80, 15, −5, 25, −30, 60, −12]`.

```text
ganadoras  = 50 + 30 + 80 + 15 + 25 + 60 = 260     (6 operaciones)
perdedoras = 20 + 10 + 40 + 5 + 30 + 12  = 117     (6 operaciones)
win_rate      = 6 / 12 = 0,50
avg_win       = 260 / 6 = 43,33
avg_loss      = −117 / 6 = −19,50
profit_factor = 260 / 117 = 2,222
expectancy    = (260 − 117) / 12 = 11,917
```

**Relación entre ellas:** `expectancy = win_rate · avg_win + (1 − win_rate) · avg_loss =
0,5 · 43,33 + 0,5 · (−19,5) = 11,917`.

**Tasa de acierto de equilibrio.** Con ganancia media G y pérdida media P (en valor absoluto),
la expectativa es 0 cuando `win_rate = P / (G + P)`. Con G = 43,33 y P = 19,5: 31 %. Una
estrategia puede acertar solo un 37 % y ganar si sus ganadoras son grandes (sección 12.9).

**Detalles.**

- **147:** `win_rate` cuenta solo `net_pnl > 0`; una operación con PnL exactamente 0 no es
  ganadora.
- **150, 167–168:** sin perdedoras, el profit factor es `None` con advertencia (dividir entre 0).
- **152:** `expectancy_pct_equity` es la media de `net_pnl / equity_al_entrar`: permite comparar
  operaciones de épocas con distinto capital.
- **154:** `turnover = nocional negociado / equity media`. Un turnover de 70 significa que se
  negoció 70 veces el capital medio: mide cuánto trabajan los costes.
- **157:** `total_costs` = comisiones + deslizamiento; el funding va aparte.
- **160:** `avg_bars_in_trade` cuenta la vela de entrada y la de salida (`bars_held = salida −
  entrada + 1`; en la sección 10.10, 3 velas).

**Error común.** Mirar solo la tasa de acierto o solo el profit factor. Un PF de 3 con 4
operaciones no significa nada; una tasa de acierto del 80 % con pérdidas medias diez veces
mayores que las ganancias medias pierde dinero.

---

## 12.7 Exposición

```text
exposición = fracción de velas con posición abierta al CIERRE
```

**[Hecho]** Una operación abierta y cerrada dentro de la misma vela (stop intravela en la vela
de entrada) aporta 0 a la exposición, y la vela de salida tampoco cuenta (sección 10.10). La
exposición es, por tanto, una cota inferior del tiempo real en el mercado.

---

## 12.8 Desgloses

<!-- fmt: off -->
`src/bybit_quant_lab/analytics/breakdowns.py` · líneas 8–24

```python
def breakdown_trades(trades: pd.DataFrame, by: str) -> pd.DataFrame:
    """Agrega operaciones por la columna ``by`` (``side``, ``exit_reason``, ``regime``...)."""
    cols = ["trades", "net_pnl", "avg_net_pnl", "win_rate", "fees", "funding"]
    if trades.empty or by not in trades.columns:
        return pd.DataFrame(columns=cols)
    g = trades.groupby(by, dropna=False)
    out = pd.DataFrame(
        {
            "trades": g.size(),
            "net_pnl": g["net_pnl"].sum(),
            "avg_net_pnl": g["net_pnl"].mean(),
            "win_rate": g["net_pnl"].apply(lambda s: float((s > 0).mean())),
            "fees": g["fees"].sum(),
            "funding": g["funding"].sum(),
        }
    )
    return out.sort_values("net_pnl", ascending=False)
```
<!-- fmt: on -->

`groupby(by, dropna=False)` agrupa por dirección (`side`), motivo de salida (`exit_reason`) o
régimen al entrar (`regime`); `dropna=False` conserva un grupo para valores ausentes. El informe
HTML genera las tres tablas (`reporting/html.py`, línea 192).

---

## 12.9 Ejemplo completo sobre una simulación

Simulación de `donchian_breakout` con los parámetros del YAML sobre las 3600 primeras velas
(el segmento de entrenamiento) de la serie sintética de 6000 velas, semilla 42, configuración
por defecto. Después se recalcula el Sharpe a mano a partir de la equity:

*Ejemplo ejecutable:*

```python
import math

import numpy as np

from bybit_quant_lab.analytics import breakdown_trades, compute_metrics
from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
params = load_strategy_params("configs/strategies.yaml")["donchian_breakout"]
senales = create_strategy("donchian_breakout", params).generate_signals(datos)
cfg = load_config()
res = run_backtest(datos, senales, cfg, "BTCUSDT", "1h", end=datos.index[3599])
m = compute_metrics(res, cfg.backtest.min_trades_for_stats, cfg.backtest.min_days_for_cagr)

claves = [
    "bars",
    "days",
    "num_trades",
    "net_profit",
    "gross_profit_before_costs",
    "total_costs",
    "total_funding",
    "sharpe",
    "sortino",
    "max_drawdown",
    "max_dd_duration_bars",
    "max_dd_recovery_bars",
    "win_rate",
    "avg_win",
    "avg_loss",
    "profit_factor",
    "expectancy",
    "exposure",
    "turnover",
    "cagr",
]
for k in claves:
    v = m[k]
    print(f"{k:26s} {round(v, 4) if isinstance(v, float) else v}")
print("advertencias:")
for w in m["warnings"]:
    print("  -", w)

eq = res.equity["equity"].to_numpy()
r = np.r_[eq[0] / res.initial_capital - 1, eq[1:] / eq[:-1] - 1]
print("Sharpe recalculado a mano:", round(r.mean() / r.std(ddof=1) * math.sqrt(8760), 4))
print(breakdown_trades(res.trades, "exit_reason").round(2).to_string())
```
*Salida real:*

```text
bars                       3600
days                       150.0
num_trades                 87
net_profit                 1765.7616
gross_profit_before_costs  2363.5379
total_costs                597.7763
total_funding              0.0
sharpe                     2.171
sortino                    3.1519
max_drawdown               0.0888
max_dd_duration_bars       995
max_dd_recovery_bars       None
win_rate                   0.3678
avg_win                    200.8803
avg_loss                   -84.771
profit_factor              1.3787
expectancy                 20.2961
exposure                   0.585
turnover                   73.351
cagr                       None
advertencias:
  - Período de 150 días < 180: CAGR no calculado.
  - Sin datos históricos de funding: no se aplica (no se simula). El resultado neto excluye el coste/ingreso de funding.
  - Especificaciones de BTCUSDT no verificadas con instruments-info (valores de referencia).
Sharpe recalculado a mano: 2.171
                trades  net_pnl  avg_net_pnl  win_rate    fees  funding
exit_reason                                                            
signal_exit         25  2127.55        85.10      0.52  119.74      0.0
signal_reverse       8   527.47        65.93      0.62   42.65      0.0
stop_loss           54  -889.26       -16.47      0.26  275.97      0.0
```

Cómo leerlo:

1. **Contabilidad.** `gross_profit_before_costs − total_costs = net_profit` (sin funding,
   porque no hay datos de funding y la advertencia lo dice). Los costes se llevan una parte
   importante del resultado bruto; el turnover alto lo explica.
2. **Sharpe.** El valor recalculado coincide con el de `compute_metrics`.
3. **Tasa de acierto baja con profit factor > 1.** Es el perfil típico de las estrategias de
   ruptura: muchas pérdidas pequeñas y pocas ganancias grandes (sección 12.6).
4. **`stop_loss` con tasa de acierto > 0.** Con `trailing_atr_mult`, el "stop" puede haberse
   movido por encima de la entrada: algunas salidas por stop **protegen ganancias**. El motivo
   de salida no distingue stop inicial y trailing.
5. **CAGR `None`.** 150 días < 180.
6. **Recuperación `None`.** El máximo drawdown no se recuperó dentro del segmento.
7. **Lo que no dice.** El generador sintético (`data/synthetic.py`) alterna bloques de 300
   velas (`regime_length`): alcista con deriva de +0,08 % por vela, lateral, bajista con deriva
   de −0,08 % y lateral de alta volatilidad. La mitad del tiempo hay una deriva sostenida y
   artificial, un entorno favorable a las estrategias de tendencia. Este resultado **no** es evidencia de que la estrategia funcione en
   BTCUSDT; solo muestra cómo se calculan y leen las métricas. Además, es un resultado de
   **entrenamiento**: no sirve para seleccionar (Módulo XIII).

---

## 12.10 Resumen

| Métrica | Pregunta que responde | Cuándo no se calcula | Trampa principal |
|---|---|---|---|
| Sharpe | Retorno por unidad de variabilidad | < 30 velas; < 10 operaciones sin exposición continua | Autocorrelación; selección múltiple (DSR, Módulo XIII) |
| Sortino | Igual, solo variabilidad negativa | Igual | Parece mejor que el Sharpe casi siempre |
| Máx. drawdown | Peor caída desde un máximo | — | Medido al cierre; dentro de la vela puede ser peor |
| CAGR | Crecimiento anual equivalente | < 180 días | Huecos en datos lo inflan |
| Profit factor | Ganancias / pérdidas | Sin perdedoras | Inestable con pocas operaciones |
| Win rate | Frecuencia de acierto | Sin operaciones | No dice nada sin el tamaño de ganancias y pérdidas |
| Exposición | Tiempo en el mercado | — | Cota inferior |
| Turnover | Cuánto se negocia | — | Multiplica el efecto de los costes |

### Comprobación final del módulo

Una estrategia tiene 40 operaciones, tasa de acierto 30 %, ganancia media 300 y pérdida media
−100. ¿Cuál es su expectativa y su profit factor?

**Respuesta:**

Expectativa = 0,3 · 300 + 0,7 · (−100) = 90 − 70 = **20** por operación. Ganadoras: 12 × 300 =
3600; perdedoras: 28 × 100 = 2800; **PF = 3600 / 2800 ≈ 1,29**. Antes de concluir nada habría
que mirar el intervalo de confianza (bootstrap, Módulo XIII) y la dependencia de las mejores
operaciones.

<div style="page-break-before: always;"></div>

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

<!-- fmt: off -->
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
<!-- fmt: on -->

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

<!-- fmt: off -->
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
<!-- fmt: on -->

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

<!-- fmt: off -->
`src/bybit_quant_lab/validation/research.py` · líneas 188–193

```python
    def _score(self, m: dict[str, Any]) -> float:
        v = self.config.validation
        if (m.get("num_trades") or 0) < v.min_trades_selection:
            return float("-inf")
        val = m.get(v.selection_metric)
        return float(val) if val is not None and np.isfinite(val) else float("-inf")
```
<!-- fmt: on -->

<!-- fmt: off -->
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
<!-- fmt: on -->

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

*Ejemplo ejecutable:*

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
        print(
            f"  {s['name']:14s} Sharpe={s['validation_score']:.2f} "
            f"DSR={ds['dsr']:.2f} PSR(0)={ds['psr_vs_zero']:.2f} "
            f"IC95 media/op=[{ic[0]:.1f}, {ic[1]:.1f}] "
            f"cambia de signo sin top-3={top['sign_flips_without_top_k']}"
        )
    print(
        "SR0 por vela (máximo esperado por azar):",
        round(
            next(iter(st["selected_details"].values()))["deflated_sharpe"][
                "expected_max_sharpe_null"
            ],
            4,
        ),
    )
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
        print(
            f"  {nombre:14s} Sharpe {v['sharpe'].iloc[0]:6.2f} -> {mt['sharpe']:6.2f}   "
            f"retorno {v['net_profit_pct'].iloc[0]:6.2%} -> {mt['net_profit_pct']:6.2%}"
        )
    bh = r.metrics(ft["benchmarks"]["buy_and_hold"])
    print(f"  comprar y mantener en test: {bh['net_profit_pct']:.2%}")
    try:
        r.run_final_test(out.selection, combos)
    except FinalTestAlreadyEvaluatedError as e:
        print("\nsegundo test final:", type(e).__name__)
```
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

<!-- fmt: off -->
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
<!-- fmt: on -->

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

*Ejemplo ejecutable:*

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
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

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

<!-- fmt: off -->
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
<!-- fmt: on -->

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

<!-- fmt: off -->
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
<!-- fmt: on -->

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

<!-- fmt: off -->
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
<!-- fmt: on -->

| Benchmark | Qué responde | Detalle |
|---|---|---|
| `buy_and_hold` | ¿Supera la estrategia a simplemente comprar? | Compra 1× el capital con comisión y deslizamiento; sin funding (lo advierte) |
| `cash` | ¿Supera a no hacer nada? | Retorno 0 |
| `random` | ¿Supera a entrar al azar con la misma exposición y gestión? | Mismo motor, stops y costes; semilla fija |

<!-- fmt: off -->
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
<!-- fmt: on -->

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

<!-- fmt: off -->
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
<!-- fmt: on -->

- **Ventana móvil** (`anchored=False`): el entrenamiento tiene siempre `train_bars` velas y se
  desplaza `step` velas.
- **Ventana anclada** (`anchored=True`): el entrenamiento empieza siempre en 0 y crece.
- `step` es por defecto igual a `test_bars`: los tramos de prueba quedan contiguos.

<!-- fmt: off -->
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
<!-- fmt: on -->

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

*Ejemplo ejecutable:*

```python
import yaml

from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.validation.research import Researcher

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
raw = yaml.safe_load(open("configs/strategies.yaml"))
r = Researcher(
    datos,
    "BTCUSDT",
    "1h",
    load_config(),
    strategy_params=load_strategy_params("configs/strategies.yaml"),
)
wf = r.walk_forward("ema_crossover", raw["grids"]["ema_crossover"])
print("rejilla:", wf["grid_size"], "| datos usados:", wf["data_range"])
print("inicio del test final:", r.segments["test"].start)
tabla = wf["windows"][
    [
        "window",
        "test_start",
        "params",
        "selection_valid",
        "is_sharpe",
        "oos_net_profit",
        "oos_trades",
    ]
]
print(tabla.round(2).to_string())
print(
    f"fuera de muestra: retorno {wf['oos_total_return']:.2%}, "
    f"Sharpe {wf['oos_sharpe']:.2f}, drawdown {wf['oos_max_drawdown']:.2%}"
)
print(
    "estabilidad en entrenamiento:",
    {k: round(v, 3) if isinstance(v, float) else v for k, v in wf["stability"].items()},
)
```
*Salida real:*

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

<!-- fmt: off -->
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
<!-- fmt: on -->

- **Append-only:** solo se añaden líneas JSON (formato JSON Lines); nunca se reescriben.
- **`count_distinct_configs`:** cuenta pares (candidato, parámetros) evaluados en validación con
  el mismo hash de datos. Se acumula entre ejecuciones: si alguien prueba veinte variantes en
  días distintos, `N` lo refleja y el DSR se vuelve más exigente.

<!-- fmt: off -->
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
<!-- fmt: on -->

- **Corrección A-02:** la guarda bloquea cualquier evaluación con los **mismos datos y el mismo
  segmento de test**, no solo la misma selección. Antes, una selección con otro `top_k` tenía
  otro identificador y podía evaluarse sobre el mismo test: probar varias selecciones contra el
  test y quedarse con la mejor es seleccionar con el test.
- `--allow-repeat` permite repetir, pero el resultado queda marcado como no independiente.

**Corrección A-03 (selección congelada).** `run_final_test` (líneas 382–459) rechaza datos o
configuración distintos y reconstruye todas las estrategias con los `strategy_params`
**guardados**, no con el YAML vigente:

<!-- fmt: off -->
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
<!-- fmt: on -->

---

## 13.12 Sensibilidad de parámetros y tamaño de las rejillas

<!-- fmt: off -->
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
<!-- fmt: on -->

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

<!-- fmt: off -->
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
<!-- fmt: on -->

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

**Respuesta:**

- El segundo `compare` registra más evaluaciones: `N` crece y el DSR se vuelve más exigente
  (aunque las configuraciones repetidas no cuentan dos veces, porque se cuentan pares distintos).
- El primer `final-test` (segunda selección) se ejecuta y queda registrado.
- El segundo `final-test` (primera selección) se **rechaza**: mismos datos y mismo segmento de
  test, aunque el `selection_id` sea distinto (corrección A-02). Solo podría forzarse con
  `--allow-repeat`, y el informe lo marcaría como no independiente.
- Además, cambiar `top_k` **después de ver** la selección ya es una decisión tomada con la
  validación; el registro no lo detecta, pero es parte del sesgo de selección.

<div style="page-break-before: always;"></div>

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

*Ejemplo ejecutable:*

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
*Salida real:*

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

*Ejemplo ejecutable:*

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
*Salida real:*

```text
24 passed
```

---

## 14.7 Calidad estática: ruff y mypy

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

*Ejemplo ejecutable:*

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
*Salida real:*

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

**Respuesta:**

1. Las de **no look-ahead** (truncamiento y perturbación del futuro), añadiendo la estrategia a
   la parametrización: un Sharpe tan alto es el síntoma típico de usar información futura.
2. La comprobación del **contrato temporal** de las operaciones (sección 14.8, punto 4): que
   cada entrada se ejecuta en la apertura siguiente a una transición de la señal.

Si ambas pasan, el siguiente paso es estadístico: número de operaciones, DSR, Holm y
dependencia de las mejores operaciones (Módulo XIII).

<div style="page-break-before: always;"></div>

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

`pyproject.toml` · líneas 33–34

```toml
[project.scripts]
bql = "bybit_quant_lab.cli:main"
```

Es decir, `bql` ejecuta la función `main` de `bybit_quant_lab/cli.py`. `python -m
bybit_quant_lab.cli` es equivalente.

**[Hecho] Hay que ejecutar `bql` desde `bybit-quant-lab/`.** Las rutas por defecto son
relativas:

<!-- fmt: off -->
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
<!-- fmt: on -->

Si `configs/default.yaml` no existe en el directorio actual, se usan los valores por defecto del
código (línea 71) **sin aviso**. Si falta `configs/strategies.yaml`, se usan los parámetros por
defecto de cada estrategia y, como no hay combinaciones, una sola combinación `vote_all` con
`veto` (líneas 94–98; Módulo IX, sección 9.4). Los resultados cambiarían sin que nada lo
advierta.

---

## 15.2 Opciones globales y punto de entrada

<!-- fmt: off -->
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
<!-- fmt: on -->

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

*Ejemplo ejecutable:*

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
*Salida real:*

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

*Ejemplo ejecutable:*

```python
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def bql(tmp, *args):
    base = [
        sys.executable,
        "-m",
        "bybit_quant_lab.cli",
        "--data-dir",
        f"{tmp}/data",
        "--output-dir",
        f"{tmp}/outputs",
    ]
    p = subprocess.run([*base, *args], capture_output=True, text=True, check=False)
    texto = (p.stdout + p.stderr).replace(tmp, "<TMP>")
    lineas = [
        ln
        for ln in texto.splitlines()
        if not re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d+ ", ln)  # registro con hora
        and not ln.startswith("ADVERTENCIA:")  # aviso legal
    ]
    texto = "\n".join(lineas)
    texto = re.sub(r"\d{4}-\d\d-\d\dT[\d:.+]+", "<FECHA>", texto)
    texto = re.sub(r"selección [0-9a-f]{16}", "selección <ID>", texto)
    return p.returncode, texto


with tempfile.TemporaryDirectory() as tmp:
    pasos = [
        ("synth", "--symbol", "BTCUSDT", "--timeframe", "1h", "--bars", "6000"),
        ("validate-data", "--symbol", "BTCUSDT", "--timeframe", "1h"),
        (
            "backtest",
            "--symbol",
            "BTCUSDT",
            "--timeframe",
            "1h",
            "--strategy",
            "donchian_breakout",
            "--out",
            f"{tmp}/outputs/bt",
        ),
        ("compare", "--symbol", "BTCUSDT", "--timeframe", "1h", "--out", f"{tmp}/outputs/cmp"),
        (
            "final-test",
            "--selection",
            f"{tmp}/outputs/cmp/selection.json",
            "--out",
            f"{tmp}/outputs/ft",
        ),
        (
            "final-test",
            "--selection",
            f"{tmp}/outputs/cmp/selection.json",
            "--out",
            f"{tmp}/outputs/ft2",
        ),
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
*Salida real:*

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

<!-- fmt: off -->
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

**Respuesta:**

`configs/default.yaml` y `configs/strategies.yaml` no existen en el directorio actual, así que
se usan los valores por defecto del código (que coinciden con el YAML en costes y riesgo, pero
no tiene por qué ser siempre así), los parámetros por defecto de cada estrategia y **una sola
combinación**, `vote_all` con política `veto`. No se muestra ningún aviso. La solución es
ejecutar desde `bybit-quant-lab/` o pasar `--config` y `--strategies-config` explícitos.

<div style="page-break-before: always;"></div>

# Módulo XVI. Leer y modificar el proyecto con autonomía

El objetivo de este módulo es que puedas abrir cualquier archivo del proyecto, entender qué
hace, seguir una ejecución de principio a fin y hacer un cambio **sin romper nada**. Incluye un
ejemplo resuelto (una estrategia nueva) y una serie de ejercicios graduados con solución.

> **[Hecho]** Durante la elaboración de este curso **no se ha modificado el código de
> producción**. El ejemplo resuelto define su estrategia en un bloque de código aparte, y los
> ejercicios describen los cambios para que los hagas tú, en tu propia rama.

---

## 16.1 Cómo leer un módulo que no conoces

1. **Cabecera (docstring del módulo).** En este proyecto casi todos los archivos empiezan con
   un texto que resume convenciones y supuestos (por ejemplo, `engine.py` líneas 1–20,
   `metrics.py` líneas 1–16). Léela entera antes que el código.
2. **Firmas públicas.** Funciones y clases sin guion bajo inicial: qué reciben y qué devuelven
   (las anotaciones de tipo ayudan, Módulo II).
3. **Pruebas.** Busca el nombre de la función en `tests/`: las pruebas son ejemplos de uso con
   resultados esperados, a menudo calculados a mano.
4. **Quién la llama.** `grep -rn "nombre_funcion" src/` muestra desde dónde se usa. Si nadie la
   llama, puede ser código sin efecto (Módulo III, sección 3.7).
5. **Ejecutar un caso mínimo** en un intérprete o un script, como en los bloques de este curso.

**¿Dónde está cada cosa?**

| Pregunta | Archivo |
|---|---|
| ¿Cómo se descargan las velas? | `data/bybit_client.py`, `data/downloader.py` |
| ¿Cómo se calcula el RSI? | `indicators/core.py` |
| ¿Cuándo entra una estrategia? | `strategies/<nombre>.py` (`compute_events`) y `strategies/base.py` (`events_to_state`) |
| ¿A qué precio se ejecuta? | `backtesting/engine.py`, `execution/costs.py`, `execution/fills.py` |
| ¿Cuánto se compra? | `risk/sizing.py` |
| ¿Cuándo deja de operar? | `risk/limits.py` |
| ¿Cómo se calcula el Sharpe? | `analytics/metrics.py` |
| ¿Cómo se elige lo mejor? | `validation/research.py` (`_select`) |
| ¿Qué hace cada orden `bql`? | `cli.py` |
| ¿Qué valores usa por defecto? | `config/models.py`, `configs/default.yaml`, `configs/strategies.yaml` |

---

## 16.2 Seguir una ejecución de principio a fin: `bql backtest`

```text
bql backtest --symbol BTCUSDT --timeframe 1h --strategy ema_crossover
│
├─ cli.main                                  cli.py 692–707: parsea y despacha
├─ cmd_backtest                              cli.py 239–301
│   ├─ _load_cfg → load_config               configuración validada (Pydantic)
│   ├─ _load_data                            Parquet + validate_ohlcv
│   ├─ Researcher(...)                       research.py 116–138: régimen y segmentos
│   ├─ strategy_candidate("ema_crossover")   research.py 141–147
│   │   └─ create_strategy                   strategies/registry.py 35–37
│   │       └─ Strategy.generate_signals     strategies/base.py 111–146
│   │           ├─ EMACrossoverStrategy.compute_events   ema_crossover.py 52–74
│   │           └─ events_to_state                       base.py 173–217
│   ├─ simulate (neto y bruto)               research.py 149–181
│   │   └─ BacktestEngine.run                engine.py 71–243
│   ├─ compute_metrics                       analytics/metrics.py 80–169
│   ├─ export_result, _save_run, metadata    reporting/export.py, cli.py 533–548
│   └─ backtest_report                       reporting/html.py 108–220
```

El registro de estrategias:

<!-- fmt: off -->
`src/bybit_quant_lab/strategies/registry.py` · líneas 9–37

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


def get_strategy_class(name: str) -> type[Strategy]:
    """Clase de estrategia por nombre."""
    try:
        return _REGISTRY[name]
    except KeyError as exc:
        raise KeyError(
            f"Estrategia desconocida: {name!r}. Disponibles: {available_strategies()}"
        ) from exc


def create_strategy(name: str, params: dict[str, Any] | None = None) -> Strategy:
    """Instancia una estrategia registrada con parámetros validados."""
    return get_strategy_class(name)(params or {})
```
<!-- fmt: on -->

`@register` es un **decorador** (Módulo II, sección 2.12): al definirse la clase, la añade al
diccionario `_REGISTRY` con su `name`. `strategies/__init__.py` importa los diez módulos para
que se registren al importar el paquete.

**Ejercicio de lectura.** Sigue la misma cadena para `bql compare` y anota en qué línea se
decide qué segmento se usa para seleccionar.

**Respuesta:**

`cli.py` 304–345 → `Researcher.run_comparison` (`research.py` 244–299) →
`_select` (313–379). La línea 317 filtra `summary["segment"] == "validation"`.

---

## 16.3 Cómo hacer un cambio con seguridad

1. **Rama propia.** `git switch -c mi-cambio`. Nunca trabajes sobre la rama principal.
2. **¿Configuración o código?** Si el cambio se puede expresar en `configs/*.yaml` (parámetros,
   combinaciones, rejillas), hazlo ahí: no requiere tocar código y queda en los metadatos.
3. **Primero la prueba.** Escribe una prueba que **falle** con el código actual y describa el
   comportamiento deseado (como hizo la auditoría, Módulo XIV, sección 14.5).
4. **El cambio mínimo** que la haga pasar.
5. **Toda la suite y la calidad estática:** `pytest`, `ruff check .`, `ruff format --check .`,
   `mypy src`.
6. **Documentación.** Si cambia un comportamiento, actualiza la cabecera del módulo y el
   documento de `docs/` correspondiente. (Dos textos desactualizados sobre los umbrales de
   combinación muestran lo fácil que es olvidarlo, Módulo IX.)
7. **Resultados antiguos.** Un cambio en estrategias, costes o motor invalida las selecciones y
   resultados previos: el hash de configuración o de parámetros lo detecta en `final-test`,
   pero no en informes ya generados.

---

## 16.4 Ejemplo resuelto: una estrategia nueva sin tocar `src/`

Objetivo: añadir una estrategia de **momentum** (largo si el cierre supera el de hace N velas,
corto si es inferior) y comprobar que cumple el contrato y no mira el futuro. Se define en el
propio bloque, se registra en tiempo de ejecución y se simula en entrenamiento.

*Ejemplo ejecutable:*

```python
import pandas as pd
from pydantic import Field

from bybit_quant_lab.analytics import compute_metrics
from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config.loader import load_config
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import (
    Category,
    Events,
    Strategy,
    StrategyParams,
    available_strategies,
    register,
)


class MomentumParams(StrategyParams):  # hereda stop, TP, trailing, cooldown...
    lookback: int = Field(48, ge=2, le=1000)


@register
class MomentumStrategy(Strategy):
    name = "momentum_demo"
    category = Category.TREND
    description = "Demostración: retorno de N velas positivo o negativo"
    params_model = MomentumParams
    params: MomentumParams

    def warmup_bars(self) -> int:
        return self.params.lookback + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        c = data["close"]
        mom = c / c.shift(self.params.lookback) - 1  # solo datos pasados
        up, down = mom > 0, mom < 0
        return Events(
            long_entry=up & ~up.shift(1, fill_value=False),  # transición, no nivel
            short_entry=down & ~down.shift(1, fill_value=False),
            long_exit=down,
            short_exit=up,
            conviction=(mom.abs() * 10).clip(0, 1),
        )


print("registrada:", "momentum_demo" in available_strategies())
datos = generate_synthetic_ohlcv(bars=3000, seed=7)
estrategia = MomentumStrategy({"lookback": 48})
senales = estrategia.generate_signals(datos)
print("contrato:", list(senales.columns))

for t in (400, 1100, 2203):  # misma técnica que la suite
    parcial = estrategia.generate_signals(datos.iloc[: t + 1])
    pd.testing.assert_frame_equal(senales.iloc[: t + 1], parcial, check_freq=False)
print("no look-ahead en 3 cortes: ok")

cfg = load_config()
res = run_backtest(datos, senales, cfg, "BTCUSDT", "1h", end=datos.index[1799])
m = compute_metrics(res, cfg.backtest.min_trades_for_stats, cfg.backtest.min_days_for_cagr)
print(
    {
        k: round(m[k], 4) if isinstance(m[k], float) else m[k]
        for k in ("num_trades", "net_profit", "sharpe", "max_drawdown", "exposure")
    }
)
print("motivos de salida:", res.trades["exit_reason"].value_counts().to_dict())
print("velas con señal distinta de 0:", int((senales["signal"].iloc[:1800] != 0).sum()), "de 1800")
print(
    "entradas rechazadas:",
    pd.Series([r["reason"] for r in res.rejected_signals]).value_counts().to_dict(),
)
print("eventos de riesgo:", len(res.risk_events))
```
*Salida real:*

```text
registrada: True
contrato: ['signal', 'conviction', 'stop_distance', 'take_profit_distance', 'trailing_distance']
no look-ahead en 3 cortes: ok
{'num_trades': 62, 'net_profit': 592.6258, 'sharpe': 2.4225, 'max_drawdown': 0.0407, 'exposure': 0.1911}
motivos de salida: {'signal_reverse': 42, 'take_profit': 12, 'stop_loss': 7, 'end_of_data': 1}
velas con señal distinta de 0: 1752 de 1800
entradas rechazadas: {'loss_streak_pause': 31}
eventos de riesgo: 8
```

Lo que enseña el ejemplo:

- **Solo hay que escribir `compute_events`.** Stops, take profit, contrato de columnas, máquina
  de estados y anulación de entradas sin ATR válido los aporta la clase base.
- **La señal no es la exposición.** La estrategia quiere estar en el mercado casi siempre
  (señal distinta de 0 en casi todas las velas), pero la exposición real es del 19 %. Las
  causas se ven en la salida: el momentum cambia de signo a menudo, se acumulan rachas de tres
  pérdidas, el gestor de riesgo pausa las entradas 24 velas cada vez, y las entradas rechazadas
  **no se recuperan** porque el motor solo entra en transiciones (Módulos X y XI). Las salidas
  por stop o por objetivo (`take_profit_r` vale 2 por defecto en `StrategyParams`) también
  dejan la cuenta fuera hasta la siguiente transición.
- **[Hecho]** El resultado sobre datos sintéticos no dice nada sobre la estrategia (Módulo XII).
- **Para hacerla permanente**: crear `src/bybit_quant_lab/strategies/momentum_demo.py`,
  importarlo en `strategies/__init__.py`, añadir sus parámetros y rejilla al YAML y añadir su
  nombre a las pruebas. Ojo: `test_exactly_ten_strategies_registered` **fallará**, porque el
  encargo fija diez estrategias; habría que actualizar esa prueba conscientemente, no
  borrarla.
- El registro en tiempo de ejecución no persiste: la CLI no conoce `momentum_demo`.

---

## 16.5 Ejercicios graduados

Cada ejercicio indica el objetivo, los archivos, la prueba que deberías escribir primero y una
solución orientativa. Todos se refieren a hallazgos reales de este curso.

### Nivel 1. Lectura y configuración

**E1. ¿Dónde se decide "stop primero"?** Localiza la línea exacta y explica qué pasaría si se
invirtiera el orden de los dos `if`.

**Solución:**

`execution/fills.py`, `check_intrabar_exit`, líneas 69–74: primero se comprueba el nivel
adverso (`low <= level`) y solo después el objetivo. Si se invirtiera, una vela que toca ambos
se registraría como `take_profit`: el backtest elegiría siempre el caso favorable.

**E2. Cambiar un parámetro sin tocar código.** Ejecuta `bql backtest` de `donchian_breakout`
con `--params '{"channel": 40}'` sobre datos sintéticos y compara con el valor por defecto (20).
¿Dónde queda registrado el parámetro usado?

**Solución:**

En `metrics.json`/`run.json` (`params`), en `metadata.json` y en `outputs/experiments.jsonl`
(registro `evaluation` con `params`). Además, el informe HTML lo muestra en "Parámetros".

**E3. Cuantificar el veto de los pesos nulos (Módulo IX, sección 9.6).** Copia
`configs/strategies.yaml` a un archivo propio, añade `conflict_policy: net` a `weighted_train` y
ejecuta `bql --strategies-config mi.yaml compare ...`. Compara las velas en posición y el número
de operaciones de `weighted_train`.

**Solución:**

Es un cambio de configuración, no de código. Con `net`, los miembros con peso 0 dejan de vetar.
La sección 9.6 midió un efecto relacionado (quitar esos miembros: de 307 a 2483 velas en
posición); con `net` cabe esperar un aumento de la exposición, pero hay que medirlo. Recuerda
que es **otra configuración** evaluada: `N` aumenta para el DSR.

### Nivel 2. Documentación y pruebas

**E4. Corregir los textos desactualizados sobre los umbrales.** `validation/research.py`
(líneas 7–8) y `reporting/html.py` (líneas 280–281) dicen que los umbrales se eligen con
validación. Escribe primero una prueba que lo detecte y después corrige los textos.

**Solución:**

Prueba posible: leer `research.__doc__` y comprobar que no contiene "umbrales de la votación
ponderada se eligen **solo con validación**", y renderizar un informe de comparación para
comprobar que el texto no asocia "validación" a los umbrales. Cambio: "pesos, redundancia y
umbrales se ajustan con entrenamiento". Ninguna prueba numérica cambia.

**E5. Una prueba de contrato temporal.** Escribe una prueba que, para las diez estrategias y
datos sintéticos, compruebe en cada operación que `signal[entry_bar − 1]` es el lado de la
operación y que `entry_price == open[entry_bar] · (1 ± slip)`. (La auditoría lo hizo con un
script fuera de la suite; `docs/audit_report.md`, sección 6.)

**Solución:**

Recorre `res.trades`; mapea `side` a ±1; compara con `senales["signal"].iloc[entry_bar - 1]`
y con `datos["open"].iloc[entry_bar] * (1 + lado * slip)` usando `pytest.approx`. Excluye las
entradas que no sean por transición (no las hay: todas lo son).

### Nivel 3. Cambios de comportamiento (cada uno cambia resultados)

**E6. `require_hist_rising` sin efecto en `macd_momentum` (Módulo VIII, sección 8.7).**

**Solución:**

Prueba primero: con `require_hist_rising` verdadero y falso, las señales deben **diferir** en
la serie sintética (hoy son idénticas). Después, revisar la condición en `compute_events` para
que el parámetro intervenga, o eliminarlo del modelo y de la rejilla del YAML (línea 185) si se
decide que no aporta. Esta segunda opción también reduce el número de pruebas duplicadas.

**E7. Convicción constante en `donchian_breakout` (Módulo VIII, sección 8.5).**

**Solución:**

Prueba: la convicción en las entradas no debe ser siempre 1. Cambio: aplicar el factor antes
del `clip` (o redefinir la fórmula). Recuerda que la convicción **no** afecta al tamaño
(Módulo IX, sección 9.8): solo afecta a `weighted_vote` con `use_conviction`.

**E8. Filtro de régimen sobre eventos, no sobre estados (Módulo IX, sección 9.10).**

**Solución:**

Diseño: en lugar de forzar el **estado** a 0 fuera del régimen permitido, bloquear solo las
**entradas** en ese régimen y dejar que las posiciones abiertas salgan por sus propias reglas.
Prueba: con una estrategia en posición y un régimen que cambia a no permitido y vuelve, no debe
haber reentradas sin evento. Implica que `apply_regime_filter` trabaje sobre transiciones (o
que la combinación tenga su propia máquina de estados). Es un cambio de diseño: documéntalo.

**E9. Usar especificaciones verificadas (B-04).**

**Solución:**

Añadir una opción (por ejemplo, `--spec-file` o una sección del YAML) para cargar una
`InstrumentSpec` construida con `spec_from_bybit` y pasarla al motor (`BacktestEngine(...,
spec=...)`, que ya la admite). Prueba: con una especificación `verified=True`, el resultado no
debe incluir la advertencia de especificaciones no verificadas.

**E10. Redondear stops y objetivos al tick.**

**Solución:**

`InstrumentSpec` tiene `tick_size`, pero nadie lo usa. Añadir `round_price` (hacia el lado
conservador: stop de un largo hacia arriba, objetivo hacia abajo) y aplicarlo en `_open`
(`engine.py`, líneas 321–322). Prueba con `tick_size = 0.5` y distancias no múltiplos.

**E11. Huecos de datos (M-06).**

**Solución:**

Opción mínima: que `_load_data` rechace (o advierta en el informe) datasets con
`missing_bars > 0`, con una opción explícita para aceptarlos. Opción completa: reindexar a la
rejilla temporal y tratar las velas ausentes en el motor (sin operar en ellas). Prueba: un
dataset con un hueco debe producir la advertencia o el error.

---

## 16.6 Lista de comprobación antes de confiar en un cambio

- [ ] Hay una prueba que fallaba antes y pasa ahora.
- [ ] `pytest`, `ruff check .`, `ruff format --check .` y `mypy src` sin errores.
- [ ] Las pruebas de no look-ahead siguen pasando para todas las estrategias.
- [ ] La cabecera del módulo y `docs/` describen el comportamiento nuevo.
- [ ] Si el cambio afecta a resultados, se han vuelto a ejecutar `compare` (y no se ha reutilizado
  un test final ya evaluado).
- [ ] El commit explica **por qué**, no solo qué.

### Comprobación final del módulo

Quieres probar si `rsi_reversion` funciona mejor con `oversold: 25`. ¿Qué harías, en qué orden y
qué no harías?

**Respuesta:**

Haría: probarlo con `bql sensitivity --segment train` (o con un `--grid` pequeño), revisar la
estabilidad y, si se decide incluirlo, fijarlo en el YAML **antes** de `compare`. No haría:
mirar validación o test para decidir el valor, ni lanzar `final-test` con varias variantes. Cada
variante evaluada queda en el registro y aumenta `N`.

<div style="page-break-before: always;"></div>

# Módulo XVII. Limitaciones reales y camino a seguir

Este módulo reúne en un solo lugar todo lo que el curso ha etiquetado como **[Limitación]**,
**[Supuesto]**, **[Pendiente]**, **[Discrepancia]** o hallazgo, y propone un orden de trabajo.
Distingue tres cosas que no deben mezclarse:

- **Defectos corregidos:** errores reales, demostrados con una prueba que fallaba, y arreglados.
- **Defectos y limitaciones pendientes:** conocidos, documentados y sin corregir.
- **Supuestos sin verificar:** decisiones razonables que solo los datos reales pueden confirmar.

---

## 17.1 Qué es el sistema hoy

**[Hecho]**

- Un framework de **investigación y backtesting** para perpetuos lineales USDT de Bybit, con
  diez estrategias, cinco formas de combinarlas, un motor determinista con costes, funding,
  stops y liquidación aproximada, gestión de riesgo independiente, métricas, validación
  cronológica, walk-forward, controles de sobreajuste, informes y CLI.
- 231 pruebas automáticas superadas, `ruff` y `mypy` sin errores (Módulo XIV).
- **No** ejecuta órdenes, **no** usa claves ni endpoints autenticados, **no** tiene modo
  testnet ni real.
- **Nunca se ha ejecutado con datos reales de Bybit.** El 11 de octubre de 2026, desde el entorno
  donde se escribió este curso, `curl https://api.bybit.com/v5/market/time` sigue devolviendo
  `CONNECT tunnel failed, response 403` (bloqueo del proxy del entorno, no de Bybit ni del
  código). La conectividad real **no está probada**.
- Todos los resultados numéricos del curso proceden de datos **sintéticos** o construidos a
  mano. No dicen nada sobre la rentabilidad de ninguna estrategia en el mercado real.

---

## 17.2 Defectos corregidos (con prueba que lo demuestra)

| Id | Defecto | Commit | Módulo |
|---|---|---|---|
| A-01 | Walk-forward sobre el período de test | `a50ac62` | XIII |
| A-02 | Guarda del test final por selección, no por período | `a50ac62` | XIII |
| A-03 | Selección no congelada; sin control de configuración | `a50ac62` | XIII |
| M-01 | Umbral de `weighted_vote` ajustado en validación | `a50ac62` | IX |
| M-02 | Gap más allá de la liquidación ejecutado como stop | `a50ac62` | X |
| M-03 | Bucle infinito posible en la paginación del funding | `a50ac62` | IV |
| M-04 | Entradas ficticias tras el calentamiento del ATR | `697b6af` | VIII |
| B-01 | Dos combinaciones idénticas | `a50ac62` | IX |
| B-02 | Benchmark aleatorio calibrado con toda la serie | `a50ac62` | XIII |
| B-03 | Walk-forward sin selección válida no señalado | `697b6af` | XIII |

Las once pruebas correspondientes fallan con el código anterior (`fc4e578`) y pasan con el
actual; la evidencia se reprodujo para este curso (Módulo XIV, sección 14.5).

---

## 17.3 Defectos y limitaciones pendientes de la auditoría

| Id | Qué | Consecuencia | Módulo |
|---|---|---|---|
| M-05 | Redundancia medida con Pearson sobre estados; categoría `indicator` heterogénea | `dedup_vote` usa las diez estrategias; el consenso por categorías puede contar dos veces la tendencia | IX |
| M-06 | Huecos en los datos | Ventanas de indicadores más largas en tiempo; posición mantenida a través del hueco; CAGR inflado | IV, XII |
| B-04 | Especificaciones verificadas no conectadas al motor | Paso de cantidad y mínimos de referencia, no reales | XI |
| B-05 | Supuestos del DSR (`N` acumulado y `V` actual; sin autocorrelación) | DSR aproximado | XIII |
| B-06 | `model_copy` no revalida | Configuraciones inválidas posibles desde código (no desde YAML/CLI) | II, XI |
| 7.4 | Sin cierres parciales, órdenes maker, cartera multiactivo, niveles de riesgo, impacto por tamaño | Simplificaciones del motor | X, XI |

---

## 17.4 Hallazgos nuevos de este curso

Revisando el código para escribir el curso aparecieron hallazgos que la auditoría no recogía.
Ninguno se ha corregido (la consigna era no modificar el código de producción); todos están
verificados con la versión actual.

**Afectan a resultados:**

| Hallazgo | Evidencia | Módulo |
|---|---|---|
| En `weighted_vote` con `veto`, los miembros con peso 0 vetan y aportan stop | 307 frente a 2483 velas en posición | IX, 9.6 |
| El filtro de régimen actúa sobre estados: crea reentradas sin evento y salidas forzadas | 9 de 17 entradas sin cambio en la estrategia; 11 salidas forzadas | IX, 9.10 |
| El régimen de tendencia no tiene histéresis | 185 cambios `trend`↔`range` en 6000 velas | IX, 9.9 |
| En `regime_switch`, el filtro **aumenta** la exposición al eliminar vetos | 737 → 2988 velas en posición | IX, 9.13 |
| `require_hist_rising` de `macd_momentum` no tiene efecto | Señales idénticas; la rejilla del YAML duplica configuraciones | VIII, 8.7; XIII |
| La convicción de `donchian_breakout` vale siempre 1 | 165 de 165 entradas | VIII, 8.5 |
| Con la configuración por defecto, solo el tope de margen limita el tamaño | 2,4 × equity < 3 × y 5 × | XI, 11.2 |
| Sin `configs/` en el directorio actual, la CLI usa valores del código y una combinación `vote_all` con `veto`, sin aviso | `cli.py`, líneas 64–98 | XV, 15.1 |

**Contables o de presentación:**

| Hallazgo | Módulo |
|---|---|
| En una liquidación, el margen de mantenimiento perdido se contabiliza como `slippage_cost` | X, 10.9 |
| `tick_size` no se usa: precios de stop y objetivo sin redondear | X, XI |
| La exposición no cuenta la vela de salida ni las operaciones dentro de una vela | XII, 12.7 |
| El CAGR usa días calculados por número de velas | XII, 12.5 |
| `bql report` regenera el informe sin benchmarks ni comparación bruto/neto | XV, 15.3 |
| `run_final_test` recibe combinaciones que no usa | XV, 15.3 |

**Documentación desactualizada o discrepante:**

| Texto | Realidad | Módulo |
|---|---|---|
| Cabecera de `validation/research.py` (líneas 7–8): umbrales "solo con validación" | Se eligen con entrenamiento (M-01) | IX, XIII |
| Informe HTML de `compare` (`html.py`, líneas 280–281): "validación (umbrales)" | Ídem | IX |
| `docs/progress.md` (línea 13): "11 órdenes" | La CLI tiene 12 | XV |
| `docs/audit_report.md` (sección 7, punto 5): otro `--output-dir` burla la guarda | El hash de configuración incluye las rutas y rechaza ese `final-test` con la misma selección | XV, 15.6 |
| Valores de referencia del DSR (0,1132 y 0,9004) "citados de memoria" | Siguen sin confirmar con la fuente (la búsqueda no los devolvió); la implementación sí está validada por Monte Carlo | XIII, 13.6 |

**Código sin efecto** (Módulo III, sección 3.7): `same_bar_policy`, `max_open_positions`,
`data.symbols`/`data.timeframes`, `maker_fee`, `BQL_BYBIT_BASE_URL`, `log_event`,
`Account.available_margin`/`history`, `Position.notional_entry`, `warmup_bars()` (nunca se
llama), el enum `Signal` (sin uso en `src`).

**De protocolo** (el código lo permite y lo registra, pero no lo impide): `backtest --segment
full`, sensibilidad en validación, walk-forward solapado con la validación, y un selector que no
usa DSR, Holm ni la dependencia de pocas operaciones.

---

## 17.5 Supuestos que solo los datos reales pueden confirmar

| Supuesto | Valor actual | Cómo verificarlo |
|---|---|---|
| Comisión taker | 0,055 % (tarifa base no VIP) | Tarifa vigente de la cuenta en Bybit |
| Deslizamiento | 2 bps fijos | Medir diferencial y profundidad en los horarios y tamaños reales |
| Funding | Valorado a `open` de la vela | Comparar con el cobro real (precio de marca) |
| Intervalo de funding | 8 h | Leer las marcas descargadas; Bybit puede cambiarlo |
| Liquidación | Mantenimiento fijo 0,5 % | Niveles de riesgo y fórmula de Bybit para el tamaño usado |
| Especificaciones | `DEFAULT_SPECS` | `instruments-info` (B-04) |
| Semántica de la API (`end`, orden, paginación del funding) | Según la documentación consultada al escribir el código | Descarga real y `validate-data` (Módulo IV, sección 4.18) |
| Disponibilidad histórica | Desconocida | `launchTime` y huecos reales |

---

## 17.6 Mejoras necesarias antes de confiar en los resultados

En orden. Cada paso es requisito del siguiente.

1. **Conectividad y datos reales.** Ejecutar desde una red con acceso a la API pública, descargar
   velas y funding, y revisar `validate-data` y el `.meta.json` (peticiones, rango, huecos).
   Contrastar unas cuantas velas con otra fuente.
2. **Especificaciones reales (B-04).** Conectar `spec_from_bybit` al motor para que el tamaño,
   los mínimos y la advertencia reflejen el instrumento real (ejercicio E9).
3. **Política de huecos (M-06).** Decidir si se rechazan los datos con huecos o cómo se tratan
   (ejercicio E11). Sin esto, indicadores y CAGR pueden ser engañosos.
4. **Costes realistas.** Fijar la comisión de la cuenta y estimar el deslizamiento por
   temporalidad y tamaño. Repetir `compare` con costes pesimistas: si el resultado solo existe
   con costes optimistas, no existe.
5. **Decisiones de diseño pendientes en las combinaciones.** Política de conflictos de
   `weighted_train` (veto de pesos nulos), filtro de régimen sobre eventos o estados, histéresis
   del régimen y medida de redundancia (M-05). Decidirlas **antes** de mirar resultados
   reales y dejarlas fijadas en el YAML.
6. **Corregir la documentación desactualizada** (ejercicio E4) y los parámetros sin efecto
   (E6), para que el número de pruebas que cuenta el DSR no incluya duplicados.
7. **Protocolo de decisión escrito.** Antes de ejecutar `compare` con datos reales: qué
   candidatos, qué rejillas, qué umbral de DSR y de número de operaciones se exigirán, y qué
   resultado se consideraría un fracaso. Así el selector, que no filtra por DSR, se complementa
   con una regla decidida de antemano.
8. **Robustez fuera de un solo mercado.** `bql markets` con BTCUSDT y ETHUSDT en varias
   temporalidades (solo entrenamiento y validación); desconfiar de lo que funciona en un único
   mercado.
9. **Un único test final**, con la selección congelada, y aceptación de su resultado aunque sea
   negativo. Conservar `outputs/experiments.jsonl`.
10. **Aun así, prudencia.** Un test final positivo es **una** muestra. Antes de cualquier uso
    real harían falta períodos adicionales no vistos y una evaluación de riesgos que está fuera
    del alcance de este proyecto, que por diseño no ejecuta órdenes.

---

## 17.7 Mejoras opcionales

No son requisitos para confiar en los resultados, pero los harían más informativos o el
proyecto más cómodo.

| Mejora | Beneficio | Coste |
|---|---|---|
| Redondeo de precios al tick (E10) | Realismo en niveles | Bajo |
| Benchmark aleatorio con muchas semillas | Distribución de referencia, no un solo sorteo | Medio (tiempo de cálculo) |
| Sharpe ajustado por autocorrelación (por ejemplo, el método de Lo, 2002) | DSR y comparaciones más honestos | Medio |
| Validación cruzada combinatoria con purga (López de Prado) | Más de un camino fuera de muestra | Alto |
| Datos de menor temporalidad para resolver la ambigüedad intravela | Menos dependencia de "stop primero" | Alto (volumen de datos) |
| Deslizamiento dependiente del tamaño y la volatilidad | Costes más realistas en temporalidades cortas | Medio |
| Órdenes límite (maker), cierres parciales | Más estrategias modelables | Alto (cambia el motor) |
| Cartera multiactivo | Diversificación | Alto (el motor es de una posición) |
| Más registro (logging) en motor y estrategias | Depuración | Bajo |
| Bucle del motor acelerado (por ejemplo, compilado) | Rejillas más grandes | Medio; más pruebas implican más sobreajuste |
| Avisar cuando la CLI no encuentra `configs/` | Evita resultados silenciosamente distintos | Bajo |

---

## 17.8 Lo que este proyecto no debe hacer

Por diseño y por las condiciones del encargo:

- No ejecutar órdenes reales ni en testnet.
- No solicitar ni almacenar claves privadas; ninguna credencial en el código ni en Git.
- No usar endpoints autenticados.
- No presentar resultados de datos sintéticos como evidencia de rentabilidad.
- No afirmar que la conectividad real está probada mientras no lo esté.

---

### Comprobación final del curso

Un compañero te enseña un informe de `bql compare` sobre datos reales con un candidato de Sharpe
3,2 en validación y te pide opinión. Enumera, en orden, las cinco primeras cosas que mirarías.

**Respuesta:**

1. **Metadatos:** `data_synthetic` falso, commit sin cambios (`dirty`), hashes, rango de datos y
   advertencias (funding aplicado o no, especificaciones no verificadas).
2. **Número de operaciones** del candidato en validación y si el Sharpe se calculó (≥ 10
   operaciones, ≥ 30 velas).
3. **Neto frente a bruto** y costes supuestos (comisión, deslizamiento): ¿sobrevive con costes
   pesimistas?
4. **Controles estadísticos:** `n_trials`, DSR, Holm, intervalo bootstrap y dependencia de las
   tres mejores operaciones.
5. **Protocolo:** cuántas veces se ejecutó `compare` con esos datos (`experiments.jsonl`), si
   se usaron `--segment full`, sensibilidad en validación o un test final previo.

Solo después de todo eso tendría sentido hablar del Sharpe 3,2, y aun así sería una
hipótesis pendiente del test final.

<div style="page-break-before: always;"></div>

# Glosario

Definiciones breves de los términos del curso, en orden alfabético. Entre paréntesis, la
sección donde se explican con detalle y con el código correspondiente.

---

**ADX (Average Directional Index).** Indicador de la **fuerza** de una tendencia, sin dirección,
entre 0 y 100. Se calcula con dos suavizados de Wilder (7.11). Lo usan `adx_di` (8.10), filtros
de varias estrategias y el régimen de tendencia (9.9).

**Anualización.** Conversión de una métrica por vela a una anual multiplicando por `√N` (Sharpe)
o elevando a `365/días` (CAGR). El proyecto usa `N = 525 600 / minutos_por_vela` (12.1).

**Apalancamiento.** Relación entre el nocional de una posición y el margen que la respalda. No
cambia el PnL de una cantidad dada; cambia el margen y el precio de liquidación (11.1).

**API pública.** Endpoints de Bybit que no requieren claves: velas, funding, especificaciones.
Es lo único que usa el proyecto (1.7, 4.3).

**Asimetría (γ₃).** Medida de lo desequilibrada que es una distribución; negativa si las pérdidas
extremas son más probables que las ganancias extremas. Entra en el PSR (13.6).

**ATR (Average True Range).** Volatilidad media por vela medida con el rango verdadero. Las
estrategias lo usan para la distancia del stop (7.6, 8.0).

**Backoff.** Espera creciente entre reintentos de una petición fallida (4.6).

**Backtest.** Simulación de unas reglas sobre datos pasados, vela a vela, sin usar información
futura (1.4, Módulo X).

**Benchmark.** Referencia con la que se compara una estrategia: comprar y mantener, efectivo o
entradas aleatorias (13.9).

**Bonferroni / Holm.** Ajustes de p-valores para muchas pruebas a la vez. Holm es escalonado y
menos conservador (6.9, 13.7).

**Bootstrap.** Remuestreo con reemplazo para estimar la variabilidad de un estadístico, por
ejemplo, un intervalo de confianza de la expectativa por operación (6.10, 13.8).

**Bps (punto básico).** 0,01 % = 0,0001. El deslizamiento se expresa en bps (10.5).

**Bruto / neto.** Resultado sin costes frente a resultado con comisiones, deslizamiento y funding
(10.9, 12.6).

**CAGR.** Tasa de crecimiento anual compuesta; solo se calcula con al menos 180 días (12.5).

**Calentamiento (warm-up).** Velas iniciales en las que un indicador aún no tiene valor (`NaN`)
(5.7, 7.0).

**Causalidad (indicador causal).** El valor en `t` depende solo de datos hasta `t` (7.0, 14.3).

**Combinación.** Regla que convierte las señales de varias estrategias en una sola señal (Módulo
IX).

**Comisión maker / taker.** Maker: la orden añade liquidez al libro; taker: la consume. El
motor cobra siempre taker (10.5).

**Consenso mínimo (`min_consensus`).** Largo si al menos `k` estrategias votan largo y no
alcanzan `k` las que votan corto (9.5).

**Consenso por categorías.** Cuenta familias de estrategias en lugar de estrategias (9.7).

**Contrato de señales.** Columnas que toda estrategia y combinación entrega al motor: `signal`,
`conviction`, `stop_distance`, `take_profit_distance`, `trailing_distance` (8.0, 9.0).

**Convicción.** Número entre 0 y 1 asociado a una señal. Solo influye en `weighted_vote` con
`use_conviction`; no cambia el tamaño (9.8).

**Correlación (Pearson).** Medida de relación lineal entre dos series, entre −1 y 1 (6.4). Sobre
estados −1/0/1 subestima la redundancia (9.11).

**Curtosis (γ₄).** Medida del peso de las colas; 3 en la normal. Entra en el PSR (13.6).

**Deslizamiento (slippage).** Diferencia adversa entre el precio de referencia y el ejecutado
(10.5).

**DSR (Deflated Sharpe Ratio).** Probabilidad de que el Sharpe verdadero supere el máximo
esperable por azar tras `N` pruebas (13.6).

**Doble de prueba (fake).** Objeto que sustituye a una dependencia real (por ejemplo, la sesión
HTTP) en una prueba (4.17, 14.4).

**Donchian (canal).** Máximo y mínimo de las `n` velas **anteriores** (7.5, 8.5).

**Drawdown.** Caída desde el máximo previo de la equity. Máximo drawdown, duración y
recuperación (12.4). El límite de riesgo del 15 % actúa como kill-switch (11.5).

**Edge-triggered (entrada por transición).** El motor solo entra cuando la señal **cambia** a
+1 o −1, no mientras se mantiene (10.4).

**Embargo.** Velas sin usar entre segmentos (13.2).

**EMA / SMA.** Media móvil exponencial y simple (5.9, 5.10, 7.0).

**Equity.** Efectivo + PnL no realizado (11.1).

**Evento (de estrategia).** Booleanos de entrada y salida por vela que la máquina de estados
convierte en señal (8.0).

**Expectativa (expectancy).** PnL neto medio por operación (12.6).

**Exposición.** Fracción de velas con posición abierta al cierre (12.7).

**Fuga de información (leakage).** Uso, directo o indirecto, de datos que no se deberían conocer
en ese momento (13.1).

**Funding.** Pago periódico entre largos y cortos de un perpetuo (1.6, 4.15, 10.6).

**Gap.** Apertura de una vela más allá de un nivel (stop, objetivo, liquidación); se ejecuta a la
apertura (10.7).

**Hash.** Huella (SHA-256) de datos o configuración que permite detectar cambios (3.11, 15.6).

**Histéresis.** Usar umbrales distintos para entrar y salir (25 y 20 en `adx_di`) para evitar
oscilaciones (8.10, 9.9).

**Hueco (gap de datos).** Velas que faltan en la serie (4.12, 5.12; M-06 en 17.3).

**Índice temporal.** `DatetimeIndex` en UTC con la hora de apertura de cada vela (5.3).

**Kline.** Nombre que da Bybit a una vela OHLCV (4.3).

**Liquidación / precio de quiebra.** Cierre forzado cuando la pérdida consume el margen menos el
mantenimiento; el precio de quiebra pierde exactamente el margen (11.4, 10.9).

**Look-ahead (sesgo de anticipación).** Usar información futura en una decisión (7.0, 14.3).

**Margen aislado / cruzado.** Cada posición con su propio margen / toda la cuenta como garantía
(11.1).

**Margen de mantenimiento.** Colchón mínimo antes de la liquidación (0,5 % en la aproximación)
(11.4).

**Mark-to-market.** Valorar la posición abierta al precio actual (10.4, 11.1).

**Máquina de estados.** `events_to_state`: convierte eventos en estado −1/0/+1 con reglas de
reversión, conflicto, cooldown y duración máxima (8.0).

**Nocional.** Cantidad × precio; el valor de la posición (10.5).

**OBV (On-Balance Volume).** Volumen acumulado con el signo del cambio de precio (7.2, 8.2).

**OHLCV.** Apertura, máximo, mínimo, cierre y volumen de una vela (1.5).

**Paginación.** Reconstruir un rango largo con muchas peticiones de tamaño limitado (4.7).

**Parquet.** Formato de archivo columnar y tipado usado para guardar los datos (4.14).

**Perpetuo lineal.** Futuro sin vencimiento liquidado en USDT (1.6).

**Profit factor.** Suma de ganancias netas / suma de pérdidas netas (12.6).

**PSR (Probabilistic Sharpe Ratio).** Probabilidad de que el Sharpe verdadero supere un umbral,
corregida por asimetría y curtosis (13.6).

**p-valor.** Probabilidad de observar un resultado al menos tan extremo si la hipótesis nula es
cierta (6.7, 13.7).

**Pydantic.** Biblioteca de validación usada para toda la configuración y los parámetros (2.15).

**Redundancia.** Estrategias que transmiten la misma información (9.11, 9.12).

**Régimen de mercado.** Etiqueta de tendencia, volatilidad y liquidez por vela (9.9).

**Registro de experimentos.** `outputs/experiments.jsonl`: cada evaluación, append-only; cuenta
las pruebas y protege el test (13.11).

**Rejilla (grid).** Conjunto de combinaciones de parámetros; limitado a 200 (13.12).

**Retorno por vela.** `E_t / E_{t−1} − 1` sobre la equity (12.2).

**`retCode`.** Código de error de nivel de aplicación en las respuestas de Bybit (4.5).

**RSI.** Indicador de momentum entre 0 y 100 basado en subidas y bajadas suavizadas (7.7, 8.6).

**Segmentos (train / validation / test).** División cronológica: ajustar, seleccionar,
evaluar una vez (6.12, 13.2–13.3).

**Selección congelada.** `selection.json`: lo elegido en validación con hashes y parámetros,
entrada única de `final-test` (13.4, 13.11).

**Sensibilidad.** Evaluación de una rejilla para ver si el resultado depende de un ajuste fino
(13.12).

**Sesgo de selección.** El mejor de muchos resultados ruidosos está sesgado al alza (6.11).

**Sharpe / Sortino.** Retorno medio por unidad de variabilidad total / a la baja, anualizado
(12.3).

**Sobreajuste (overfitting).** Ajustar reglas al ruido de una muestra (13.1).

**Stop / take profit / trailing stop.** Salida por pérdida, por objetivo y stop que persigue al
precio (10.7, 10.8).

**Stop primero.** Si una vela toca stop y objetivo, se supone que tocó antes el stop (10.7).

**Tick / paso de cantidad.** Incremento mínimo de precio / de cantidad del instrumento (11.3).

**Turnover (rotación).** Nocional negociado / equity media (12.6).

**UTC.** Tiempo universal coordinado; todas las fechas del proyecto (4.4).

**Validación temprana (fail fast).** Rechazar configuraciones o datos inválidos al cargarlos
(3.6).

**Veto / net.** Políticas de conflicto de las combinaciones: cualquier voto contrario anula, o se
usa el neto (9.4).

**Votación simple / ponderada.** Combinar por voto neto / por puntuación ponderada con umbral
(9.4, 9.6).

**VWAP.** Precio medio ponderado por volumen, móvil o anclado a la sesión UTC (7.3, 8.3).

**Walk-forward.** Repetir "optimizar en el pasado, evaluar en el siguiente tramo" a lo largo del
tiempo (13.10).

**Win rate (tasa de acierto).** Fracción de operaciones con PnL neto > 0 (12.6).
