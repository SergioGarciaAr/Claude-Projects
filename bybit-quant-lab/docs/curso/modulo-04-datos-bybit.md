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

<!-- ejecutar -->
```python
import requests

parametros = {"category": "linear", "symbol": "BTCUSDT", "interval": "60",
              "start": 1704067200000, "end": 1707667199999, "limit": 1000}
peticion = requests.Request("GET", "https://api.bybit.com/v5/market/kline", params=parametros).prepare()
print(peticion.method)
print(peticion.url)
```
<!-- salida -->
```text
GET
https://api.bybit.com/v5/market/kline?category=linear&symbol=BTCUSDT&interval=60&start=1704067200000&end=1707667199999&limit=1000
```

---

## 4.3 El endpoint de velas y sus parámetros

El cliente construye exactamente estos parámetros para cada petición de velas:

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L157-L165 -->
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

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L45-L50 -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 45–50

```python
def _to_ms(ts: pd.Timestamp) -> int:
    return (
        int(ts.tz_convert("UTC").timestamp() * 1000)
        if ts.tzinfo
        else int(ts.tz_localize("UTC").timestamp() * 1000)
    )
```

Si la fecha no tiene zona (`tzinfo` vacío), se **supone** UTC (`tz_localize("UTC")`); si la
tiene, se **convierte** a UTC (`tz_convert("UTC")`). Son operaciones distintas: localizar
declara en qué zona estaba expresada una hora; convertir cambia la hora de reloj sin cambiar el
instante.

Alineación de fechas al borde de una vela:

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L238-L240 -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 238–240

```python
def _align(ts: pd.Timestamp, delta: pd.Timedelta, ceil: bool) -> pd.Timestamp:
    ts = ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")
    return ts.ceil(delta) if ceil else ts.floor(delta)
```

`ceil` redondea hacia arriba al múltiplo de la duración de vela y `floor` hacia abajo.

<!-- ejecutar -->
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
<!-- salida -->
```text
2024-01-01 00:00:00+00:00
2023-12-31 21:00:00-03:00
True
2024-01-01 01:00:00+00:00 2024-01-01 00:00:00+00:00
```

### Comprobación

Si pides velas de 1h desde las 00:30, ¿cuál será la primera vela descargada y por qué?

<details><summary>Ver respuesta</summary>

La de las 01:00. `fetch_klines` alinea el inicio con `ceil` (redondeo hacia arriba), porque la
vela de las 00:00 empezó antes del inicio pedido. Lo verifica la prueba
`test_unaligned_start_is_rounded_up_to_bar_boundary` (`tests/unit/test_audit_data.py`).
</details>

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

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L85-L131 -->
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

<details><summary>Ver respuesta</summary>

El HTTP 200 pasa las comprobaciones de estado, el JSON tiene `retCode`, y 10001 no está en
`RETRYABLE_RET_CODES`, así que lanza `BybitAPIError("retCode 10001: params error")` sin
reintentar. Lo verifica `test_non_retryable_and_exhausted_errors` en `tests/unit/test_data.py`.
</details>

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

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L79-L83 -->
`src/bybit_quant_lab/data/bybit_client.py` · líneas 79–83

```python
    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.min_request_interval:
            self._sleep(self.min_request_interval - elapsed)
        self._last_request = time.monotonic()
```

Con `min_request_interval = 0.05` s, el cliente hace como máximo 20 peticiones por segundo, es
decir, 100 cada 5 segundos: una sexta parte del límite documentado.

Este ejemplo usa una **sesión simulada** que falla tres veces y luego responde bien, y una
función de espera falsa que, en lugar de dormir, anota cuánto habría esperado:

<!-- ejecutar -->
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
        self.guion = [requests.ConnectionError("red caída"),
                      Respuesta(503, {}),
                      Respuesta(200, {"retCode": 10006, "retMsg": "Too many visits"}),
                      Respuesta(200, {"retCode": 0, "result": {"list": []}})]
    def get(self, url, params, timeout):
        paso = self.guion.pop(0)
        if isinstance(paso, Exception):
            raise paso
        return paso

esperas = []
cliente = BybitPublicClient(session=SesionSimulada(), sleep=esperas.append,
                            backoff_seconds=1.0, min_request_interval=0)
print(cliente.get("/v5/market/kline", {}))
print("esperas de backoff:", esperas, "| peticiones:", cliente.request_count)
```
<!-- salida -->
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

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L134-L174 -->
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

<!-- ejecutar -->
```python
import math

import pandas as pd

inicio, fin = pd.Timestamp("2022-01-01", tz="UTC"), pd.Timestamp("2025-01-01", tz="UTC")
for tf, minutos in (("5m", 5), ("1h", 60), ("4h", 240)):
    velas = int((fin - inicio) / pd.Timedelta(minutes=minutos))
    print(f"{tf}: {velas} velas -> {math.ceil(velas / 1000)} peticiones")
```
<!-- salida -->
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

<details><summary>Ver respuesta</summary>

Tres: 1000, 1000 y 500. Lo comprueba `test_fetch_klines_paginates_and_sorts`
(`tests/unit/test_data.py`, línea 101).
</details>

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

<!-- ejecutar -->
```python
import pandas as pd

ahora = pd.Timestamp("2024-01-01 05:30", tz="UTC")
aperturas = pd.date_range("2024-01-01 03:00", periods=3, freq="1h", tz="UTC")
cerradas = aperturas + pd.Timedelta("1h") <= ahora
for apertura, cerrada in zip(aperturas, cerradas):
    print(apertura.strftime("%H:%M"), "cerrada" if cerrada else "ABIERTA (se descarta)")
```
<!-- salida -->
```text
03:00 cerrada
04:00 cerrada
05:00 ABIERTA (se descarta)
```

---

## 4.9 Normalización: de lista de textos a tabla tipada

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L249-L269 -->
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

<!-- ejecutar -->
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
            filas.append([str(t), f"{p}", f"{p + 15}", f"{p - 12}", f"{p + 5}", "3.5", f"{3.5 * p:.2f}"])
            t += paso
        return Respuesta({"retCode": 0, "retMsg": "OK",
                          "result": {"category": "linear", "symbol": params["symbol"], "list": filas[::-1]}})

carpeta = Path(tempfile.mkdtemp())
api = BybitSimulado()
cliente = BybitPublicClient(session=api, min_request_interval=0,
                            clock=lambda: pd.Timestamp("2026-01-01", tz="UTC"))
resumen = download_ohlcv(cliente, "BTCUSDT", "1h", pd.Timestamp("2024-01-01", tz="UTC"),
                         pd.Timestamp("2024-03-01", tz="UTC"), carpeta)
print("peticiones:", resumen.requests, "| velas:", resumen.rows)
tabla = load_dataset(dataset_path(carpeta, "BTCUSDT", "1h"))
print(tabla.head(3).to_string())
print("tipos:", sorted(set(map(str, tabla.dtypes))), "| índice:", tabla.index.dtype)
print("ordenada:", tabla.index.is_monotonic_increasing, "| duplicados:", int(tabla.index.duplicated().sum()))
print("calidad válida:", load_metadata(dataset_path(carpeta, "BTCUSDT", "1h"))["quality"]["is_valid"])
senales = create_strategy("donchian_breakout").generate_signals(tabla)
print("señales con el mismo índice:", senales.index.equals(tabla.index))
```
<!-- salida -->
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

<!-- cita: src/bybit_quant_lab/data/validation.py#L20-L50 -->
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

`is_valid` es `True` solo si no hay **errores estructurales**. **[Diseño]** Los huecos
(`gaps`) **no** invalidan los datos: se informan, porque pueden ser interrupciones reales del
exchange y no hay forma honesta de rellenarlos.

Las comprobaciones de cada vela:

<!-- cita: src/bybit_quant_lab/data/validation.py#L86-L94 -->
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

- **87:** una vela es inválida si el máximo es menor que el mínimo, la apertura o el cierre; si
  el mínimo es mayor que la apertura o el cierre; o si algún precio es cero o negativo.
- **93–94:** una marca de tiempo está **desalineada** si no cae en un borde exacto de vela desde
  la época Unix (por ejemplo, una vela de 1h a las 10:07).

La limpieza normaliza, ordena, elimina duplicados y descarta filas inválidas, y **después**
vuelve a validar:

<!-- cita: src/bybit_quant_lab/data/validation.py#L115-L139 -->
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

<!-- ejecutar -->
```python
import numpy as np
import pandas as pd

from bybit_quant_lab.data.validation import clean_ohlcv, validate_ohlcv

idx = pd.date_range("2024-01-01", periods=6, freq="1h", tz="UTC")
velas = pd.DataFrame({"open": [100, 101, 102, 103, 104, 105.0],
                      "high": [101, 102, 103, 104, 105, 106.0],
                      "low": [99, 100, 101, 102, 103, 104.0],
                      "close": [101, 102, 103, 104, 105, 105.5],
                      "volume": [10, 11, 12, 13, 14, 15.0]}, index=idx)
velas.iloc[2, velas.columns.get_loc("high")] = 90.0       # máximo imposible
velas.iloc[4, velas.columns.get_loc("close")] = np.nan    # dato ausente
velas = velas.drop(idx[3])                                # una vela que falta
informe = validate_ohlcv(velas, "1h")
print("válido:", informe.is_valid, "| problemas:", informe.issues)
limpia, informe_limpio = clean_ohlcv(velas, "1h")
print("filas:", len(velas), "->", len(limpia), "| válido tras limpiar:", informe_limpio.is_valid)
print("huecos:", informe_limpio.gaps, "| velas faltantes:", informe_limpio.missing_bars)
```
<!-- salida -->
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

<!-- cita: src/bybit_quant_lab/data/downloader.py#L38-L60 -->
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

Tres tipos de tramo pendiente: la **cabecera** (antes de la primera vela guardada), los **huecos
internos** y la **cola** (después de la última vela guardada).

El proceso completo:

<!-- cita: src/bybit_quant_lab/data/downloader.py#L78-L96 -->
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

- **80–84:** si existe un archivo local y no se pidió `--refresh`, se carga; si no supera la
  validación, se ignora y se descarga todo de nuevo.
- **86:** calcula los tramos que faltan.
- **89–91:** descarga solo esos tramos.
- **95–96:** une lo antiguo con lo nuevo y limpia el conjunto.

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.data.downloader import missing_ranges

guardadas = pd.date_range("2024-01-01 02:00", periods=8, freq="1h", tz="UTC").delete([3, 4])
tramos = missing_ranges(guardadas, pd.Timestamp("2024-01-01", tz="UTC"),
                        pd.Timestamp("2024-01-01 12:00", tz="UTC"), "1h")
for a, b in tramos:
    print(a.strftime("%H:%M"), "->", b.strftime("%H:%M"))
```
<!-- salida -->
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

<!-- cita: src/bybit_quant_lab/data/storage.py#L34-L69 -->
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

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L177-L223 -->
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

<!-- cita: src/bybit_quant_lab/data/importers.py#L15-L41 -->
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

<!-- cita: src/bybit_quant_lab/data/bybit_client.py#L56-L76 -->
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

Y las pruebas definen un exchange simulado que imita el formato documentado, incluido el orden
descendente:

<!-- cita: tests/unit/test_data.py#L36-L72 -->
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

<details><summary>Ver respuesta</summary>

Que las pruebas demuestran que el código maneja correctamente las respuestas **simuladas**, que
imitan el formato documentado. No demuestran que la API real responda así: el orden de los
campos, la semántica de `end`, la paginación del funding y los códigos de error reales solo se
confirman con una descarga real seguida de `bql validate-data`.
</details>
