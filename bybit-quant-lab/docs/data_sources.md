# Fuentes de datos

## API pública de Bybit V5 (solo lectura)

Cliente: `data/bybit_client.py` (`BybitPublicClient`). No usa autenticación ni claves.

| Endpoint | Uso | Límite por petición |
|---|---|---|
| `GET /v5/market/kline` | Velas OHLCV (`category=linear`) | 1000 velas |
| `GET /v5/market/funding/history` | Tasas de funding históricas | 200 registros |
| `GET /v5/market/instruments-info` | Especificaciones del instrumento | — |

Formato de una vela (`result.list`): `[startTime(ms), open, high, low, close, volume,
turnover]`, en cadenas de texto. El cliente **ordena siempre** el resultado y no depende del
orden en que lo devuelva la API.

Intervalos usados: `5`, `15`, `60` y `240` (además de `1`, `30` y `D`, que también están
soportados).

### Paginación, límites y errores

- **Velas:** ventanas fijas de `limit · temporalidad` (≤ 1000 velas por petición), recorridas
  hacia delante. La vela en curso (no cerrada) se descarta.
- **Funding:** paginación hacia atrás desde `endTime` hasta cubrir `startTime`.
- **Límite de frecuencia:** la documentación de Bybit indica 600 peticiones cada 5 segundos
  por IP. El cliente espacia las peticiones (`min_request_interval`, 0,05 s por defecto), muy
  por debajo de ese límite.
- **Reintentos con backoff exponencial** (`backoff_seconds · 2^(n-1)`, hasta `max_retries`)
  ante:
  - errores de conexión o timeout;
  - HTTP 429, 500, 502, 503 y 504;
  - respuesta no JSON;
  - `retCode` 10000, 10006 y 10016.
- **HTTP 403:** según la documentación de Bybit indica un bloqueo de IP por exceso de
  frecuencia. No se reintenta, y el mensaje recomienda esperar al menos 10 minutos.
- **Sin reintento:** otros `retCode` distintos de 0 y respuestas con formato inesperado
  (velas con menos de 7 campos, marcas de tiempo no numéricas).

### Descarga incremental

`data/downloader.py` calcula los rangos que faltan respecto al Parquet local: cabecera, cola y
huecos internos. Solo descarga esos rangos si el dataset local es válido; si no lo es, o con
`--refresh`, descarga todo de nuevo. Un hueco interno que se vuelve a pedir y no devuelve datos
suele corresponder a una interrupción real del exchange: queda registrado y **no se rellena**.

### Disponibilidad histórica (limitaciones)

- El historial de velas de cada contrato empieza en su fecha de lanzamiento. Puede
  consultarse en el campo `launchTime` de `instruments-info`. No se fija aquí ninguna fecha
  sin verificar: si se pide un rango anterior, la API devuelve listas vacías y el resumen lo
  refleja.
- El funding se liquida normalmente cada 8 horas (00:00, 08:00 y 16:00 UTC), pero el intervalo
  puede variar según el contrato. El motor usa las marcas reales descargadas, no una
  periodicidad supuesta.
- El volumen es el de Bybit, no el agregado del mercado.
- Las velas OHLCV **no** permiten reconstruir el orden de los precios dentro de la vela ni la
  liquidez disponible. Ver las reglas de ejecución en `methodology.md`.
- **Estado de verificación:** el cliente se ha probado con respuestas HTTP simuladas que
  reproducen el formato documentado (paginación, orden descendente, errores, reintentos). La
  conexión real con `api.bybit.com` **no** pudo verificarse en el entorno de desarrollo, que
  bloqueaba el acceso. Antes de confiar en los datos descargados, el usuario debe ejecutar
  `bql download` y `bql validate-data` en su entorno.

## Almacenamiento y procedencia

- `data/processed/<SÍMBOLO>_<tf>.parquet`: velas limpias (índice `open_time` UTC; columnas
  `open, high, low, close, volume, turnover` en float64).
- `data/processed/<SÍMBOLO>_<tf>.meta.json`: fuente, endpoint, URL base, símbolo,
  temporalidad, historial de descargas (fecha, rango pedido, rangos obtenidos, número de
  peticiones), informe de calidad, filas, rango y SHA-256 del contenido.
- `data/processed/<SÍMBOLO>_funding.parquet`: funding descargado.

## Validación y limpieza (`data/validation.py`)

Comprobaciones:

- orden cronológico y duplicados;
- valores no numéricos y NaN;
- velas inválidas (`high < max(open, close)`, `low > min(open, close)`, precios ≤ 0);
- volumen negativo;
- marcas de tiempo no alineadas a la temporalidad;
- huecos, con su número de velas faltantes y sus rangos.

La limpieza normaliza a UTC, ordena, elimina duplicados (conserva el último) y descarta filas
inválidas. **Nunca inventa velas:** los huecos se reportan, no se rellenan.

## Importación (`bql import`)

Admite CSV o Parquet con columnas OHLCV y una columna temporal en ISO-8601 o epoch (en ms o s,
detectado automáticamente). El archivo se limpia, se valida y se guarda con
`source: import` y la ruta de origen en los metadatos.

## Datos sintéticos (`bql synth`)

Regímenes alternos (alcista, lateral, bajista y alta volatilidad), con un volumen
correlacionado con el movimiento y picos ocasionales. Son deterministas por semilla. Sirven
**solo** para probar la lógica. Los metadatos los marcan como `synthetic: true` y los informes
lo advierten.

## Fuentes futuras (interfaces sin implementar)

`data/interfaces.py` define protocolos para interés abierto (`OpenInterestSource`), bid/ask
(`QuoteSource`) y operaciones individuales (`TradeSource`). No hay implementación ni datos
simulados para ellos. El sistema no asume disponer de esa información.
