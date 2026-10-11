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

**[Hecho]** No hay ninguna función en el repositorio que envíe órdenes a un exchange. El cliente
de Bybit solo implementa tres consultas públicas de datos de mercado (lo verás en la sección
1.8). No hay claves API, ni contraseñas, ni conexión a una cuenta.

### Comprobación

¿Puede `bybit-quant-lab`, tal como está, comprar bitcoin en tu cuenta de Bybit?

<details><summary>Ver respuesta</summary>

No. No contiene ningún endpoint de trading ni maneja credenciales. Solo lee datos públicos de
mercado y simula operaciones en memoria.
</details>

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

<details><summary>Ver respuesta</summary>

Sí. Con suficientes intentos, el azar produce algún resultado que parece excelente. Por eso el
proyecto cuenta cuántas configuraciones se han probado y corrige las métricas por ese número
(Deflated Sharpe Ratio y corrección de Holm, Módulo XIII).
</details>

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

<!-- cita: src/bybit_quant_lab/strategies/base.py#L1-L21 -->
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

Fíjate en la frase "Nunca se ejecuta en la misma vela": es la primera defensa contra el error
más grave del backtesting, que verás a continuación.

### Comprobación

Una estrategia devuelve `signal = 1` al cierre de la vela de las 10:00. ¿Significa que se compró
a ese precio de cierre?

<details><summary>Ver respuesta</summary>

No. `signal = 1` es una **intención** ("quiero estar largo"). El motor programa una orden que se
ejecuta en la **apertura de la vela siguiente**, con deslizamiento y comisión. Además, la entrada
puede rechazarse (por un límite de riesgo, por un tamaño demasiado pequeño, etc.).
</details>

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

<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L1-L20 -->
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

No necesitas entender aún cada paso; el Módulo X los explica uno por uno. Lo importante ahora es
el paso 8: **la decisión se toma al cierre de la vela `i` y se ejecuta en la apertura de `i+1`**.

### Comprobación

¿Por qué es peligroso que una regla use el precio de cierre de una vela para decidir y ejecute
la compra a ese mismo cierre?

<details><summary>Ver respuesta</summary>

Porque el precio de cierre solo se conoce cuando la vela ya terminó: en la realidad ya no
podrías comprar a ese precio. La simulación estaría usando información "del futuro" respecto al
momento de la orden y los resultados serían artificialmente buenos.
</details>

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

<!-- ejecutar -->
```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv

velas = generate_synthetic_ohlcv(bars=3, timeframe="1h", seed=42)
# to_string() imprime la tabla completa; se omite 'turnover' para que quepa en pantalla
print(velas[["open", "high", "low", "close", "volume"]].round(2).to_string())
```
<!-- salida -->
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

<details><summary>Ver respuesta</summary>

No: el cierre (98) es menor que el mínimo (99). El mínimo debe ser menor o igual que la apertura y
el cierre. `data/validation.py` la contaría como vela inválida y la limpieza la descartaría.
</details>

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

<details><summary>Ver respuesta</summary>

Ganas, porque un corto gana cuando el precio baja: 0,2 × (50.000 − 49.000) = 200 USDT.
</details>

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

<details><summary>Ver respuesta</summary>

El público devuelve información de mercado accesible para cualquiera, sin identificarse. El
privado actúa sobre una cuenta (órdenes, saldos) y exige claves de autenticación. El proyecto
solo usa públicos.
</details>

---

## 1.8 Qué partes son investigación y cuáles podrían tocar dinero real

**[Hecho]** Ninguna parte toca dinero real. El cliente HTTP declara exactamente qué endpoints usa:

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L1-L11 -->
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

Los tres son de la familia `/v5/market/`, que en la API de Bybit agrupa datos públicos de
mercado. Puedes comprobarlo tú mismo buscando cualquier otra ruta en el código:

<!-- ejecutar -->
```python
import pathlib
import re

rutas = set()
for archivo in pathlib.Path("src").rglob("*.py"):
    rutas.update(re.findall(r'"(/v5/[a-z/-]+)"', archivo.read_text(encoding="utf-8")))
print(sorted(rutas))
```
<!-- salida -->
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

<details><summary>Ver respuesta</summary>

`execution/costs.py` (y la sección `costs` de `configs/default.yaml`). No habría que tocar
ninguna estrategia: las estrategias no saben nada de comisiones.
</details>

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

<!-- ejecutar -->
```python
from bybit_quant_lab.analytics import compute_metrics
from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config import AppConfig
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=2000, timeframe="1h", seed=1)        # sustituye a pasos 1-4
senales = create_strategy("ema_crossover").generate_signals(datos)          # paso 5
resultado = run_backtest(datos, senales, AppConfig(), "BTCUSDT", "1h")      # pasos 6-7
metricas = compute_metrics(resultado)                                       # paso 8

print("velas simuladas:", len(resultado.equity))
print("operaciones:", metricas["num_trades"])
print("primera operación:")
print(resultado.trades.iloc[0][["side", "entry_time", "entry_price", "exit_reason", "net_pnl"]])
print("capital final:", round(metricas["final_equity"], 2))
print("advertencias:", len(metricas["warnings"]))
```
<!-- salida -->
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

<details><summary>Ver respuesta</summary>

(d) → (b) → (c) → (e) → (a).
</details>
