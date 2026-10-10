# bybit-quant-lab

Framework en Python para **investigar y hacer backtesting** de estrategias sistemáticas sobre
futuros perpetuos lineales USDT de Bybit (inicialmente BTCUSDT y ETHUSDT, temporalidades 5m,
15m, 1h y 4h).

> **Advertencia.** Los resultados de backtesting tienen fines exclusivos de investigación. Los
> resultados históricos no garantizan resultados futuros. Este software no ejecuta órdenes
> reales ni constituye recomendación de inversión. Los límites de riesgo por defecto son
> referencias de investigación, no garantías de seguridad.

## Qué hace

- Descarga velas OHLCV y funding histórico desde la **API pública V5 de Bybit** (solo
  lectura, sin credenciales), con paginación, reintentos, validación y almacenamiento
  incremental en Parquet con metadatos de procedencia.
- Importa CSV/Parquet externos y genera datos sintéticos deterministas para pruebas.
- Implementa **diez estrategias** en tres categorías (volumen, tendencia e indicadores)
  con una interfaz común de señales normalizadas (LONG / SHORT / FLAT + convicción).
- Combina señales mediante votación simple, votación ponderada, consenso mínimo, consenso
  por categorías y filtro de régimen.
- Simula con un **motor determinista** vela a vela: ejecución en la apertura siguiente,
  comisiones, slippage, funding (si existe), stop-loss, take-profit, trailing stop,
  apalancamiento, margen aislado y liquidación aproximada, con regla conservadora
  *stop primero* para velas que tocan stop y objetivo.
- Aplica gestión de riesgo independiente: riesgo por operación, pérdida diaria, drawdown
  máximo, pausa tras pérdidas consecutivas, exposición, apalancamiento y reserva de margen.
- Evalúa con separación cronológica train/validación/test, walk-forward, sensibilidad de
  parámetros, benchmarks, Deflated Sharpe Ratio, ajuste de Holm, bootstrap y análisis de
  dependencia de las mejores operaciones. El test final se evalúa **una sola vez**.
- Genera informes HTML con gráficos, CSV y JSON con metadatos reproducibles (commit de git,
  hash de los datos, configuración y semilla).

## Qué no hace

- **No envía órdenes** a Bybit (ni real ni testnet), no usa endpoints autenticados y no
  solicita ni almacena claves API.
- No reconstruye el orden real de precios dentro de una vela: usa reglas conservadoras
  documentadas.
- No simula funding, libro de órdenes, interés abierto ni operaciones individuales si esos
  datos no se han obtenido. Las interfaces existen (`data/interfaces.py`), los datos no se
  inventan.
- No reproduce los niveles de riesgo (*risk limit tiers*) de Bybit: la liquidación es una
  aproximación con una tasa de mantenimiento fija.
- No declara ninguna estrategia rentable: los informes muestran métricas y advertencias.

## Arquitectura

```
src/bybit_quant_lab/
├── config/        Modelos Pydantic y carga de YAML
├── data/          Cliente Bybit V5, descarga incremental, validación, Parquet, importación,
│                  datos sintéticos, interfaces para fuentes futuras
├── indicators/    Indicadores causales (EMA, ATR, RSI, MACD, Bollinger, StochRSI, ADX, OBV,
│                  VWAP, Donchian, temporalidad superior sin anticipación)
├── strategies/    Interfaz común, registro y las diez estrategias
├── signals/       Combinadores, régimen de mercado y redundancia
├── execution/     Costes y resolución de stops/objetivos/liquidación con OHLC
├── risk/          Instrumentos, dimensionamiento y límites del sistema
├── portfolio/     Posición, operación cerrada y cuenta
├── backtesting/   Motor y resultados
├── validation/    Segmentos, walk-forward, benchmarks, sobreajuste, registro de
│                  experimentos y flujos de investigación
├── analytics/     Métricas y desgloses
├── reporting/     Gráficos, HTML, CSV/JSON y metadatos
└── cli.py         Orden `bql`
```

Detalle en [`docs/architecture.md`](docs/architecture.md).

## Requisitos

- Python **3.11 o superior** (verificado con 3.13).
- Linux, macOS o Windows. Unos 300 MB para el entorno virtual.
- Acceso HTTPS a `api.bybit.com` solo para descargar datos reales (opcional).

## Instalación

```bash
git clone <url-del-repositorio>
cd Claude-Projects/bybit-quant-lab

# 1. Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Instalar el paquete y las herramientas de desarrollo
pip install --upgrade pip
pip install -e ".[dev]"

# 3. Comprobar la instalación
bql list-strategies
```

Todas las órdenes se ejecutan desde el directorio `bybit-quant-lab/`, que es donde se
encuentran `configs/default.yaml` y `configs/strategies.yaml`.

## Datos

### Descargar datos reales de Bybit

```bash
bql download --symbol BTCUSDT --timeframe 5m 15m 1h 4h --start 2023-01-01 --end 2024-12-31 --funding
bql download --symbol ETHUSDT --timeframe 1h 4h --start 2023-01-01 --end 2024-12-31 --funding
bql validate-data --symbol BTCUSDT --timeframe 1h
```

Las descargas posteriores solo piden los intervalos que faltan. Usa `--refresh` para
descargarlo todo de nuevo. Los datos se guardan en `data/processed/` como
`BTCUSDT_1h.parquet` y `BTCUSDT_1h.meta.json`. Límites y disponibilidad en
[`docs/data_sources.md`](docs/data_sources.md).

### Importar un CSV o Parquet propio

```bash
bql import --symbol BTCUSDT --timeframe 1h --file mis_velas.csv
```

El archivo debe tener las columnas `open, high, low, close, volume` y una columna temporal
(`open_time`, `timestamp`, `time`, `date`...) en ISO-8601 o epoch (ms o s).

### Datos sintéticos (solo para probar la lógica)

```bash
bql synth --symbol BTCUSDT --timeframe 1h --bars 6000 --seed 42
```

Los datos sintéticos **no** sirven para evaluar rentabilidad. Los informes lo indican.

## Configuración

- `configs/default.yaml`: datos, costes, ejecución, riesgo, backtest y validación.
- `configs/strategies.yaml`: parámetros de las diez estrategias, combinaciones y rejillas
  de búsqueda.

Ambos archivos se validan con Pydantic: un parámetro desconocido o fuera de rango produce
un error explícito. Para un cambio puntual sin editar el YAML:

```bash
bql backtest --symbol BTCUSDT --timeframe 1h --strategy ema_crossover --params '{"fast": 8, "slow": 50}'
```

## Primer backtest

```bash
bql backtest --symbol BTCUSDT --timeframe 1h --strategy donchian_breakout --segment train
```

`--segment` acepta `train` (por defecto), `validation` o `full`. Este último incluye el
período de test y queda marcado con una advertencia: no lo uses para seleccionar
estrategias. El resultado se guarda en `outputs/backtest_<símbolo>_<tf>_<estrategia>_<fecha>/`:

| Archivo | Contenido |
|---|---|
| `report.html` | Informe con resumen, parámetros, métricas, gráficos, costes, desgloses y operaciones |
| `equity.csv` / `trades.csv` | Curva de equity por vela y operaciones |
| `metrics.json` / `risk_events.json` | Métricas, eventos de riesgo y señales rechazadas |
| `metadata.json` / `run.json` | Versión del código, hash de datos, configuración y semilla |

## Comparar las diez estrategias

```bash
bql compare --symbol BTCUSDT --timeframe 1h
```

Evalúa las diez estrategias, las seis combinaciones de `strategies.yaml` y tres benchmarks
(buy-and-hold, efectivo y entradas aleatorias), en entrenamiento y validación, con y sin
costes. Selecciona candidatos **solo con validación** y congela la selección en
`selection.json`. El período de test no se toca.

## Test final (una sola vez)

```bash
bql final-test --selection outputs/compare_BTCUSDT_1h_<fecha>/selection.json
```

Evalúa la selección congelada en el período de test. Si se intenta repetir, la orden se
niega (código de salida 3), salvo que se use `--allow-repeat`. En ese caso el informe marca
el resultado como no independiente.

## Walk-forward y sensibilidad

```bash
bql walkforward --symbol BTCUSDT --timeframe 1h --strategy ema_crossover
bql sensitivity --symbol BTCUSDT --timeframe 1h --strategy rsi_reversion --segment train
bql walkforward --symbol BTCUSDT --timeframe 1h --strategy donchian_breakout --grid '{"channel": [20, 40]}'
```

Las rejillas por defecto están en `configs/strategies.yaml` (`grids`) y se limitan a
`validation.max_grid_size` combinaciones.

## Rendimiento por símbolo y temporalidad

```bash
bql markets --symbols BTCUSDT ETHUSDT --timeframes 1h 4h --segment validation
```

Evalúa cada estrategia, con los parámetros configurados y sin optimizarla por mercado, en el
segmento elegido de cada dataset disponible (los que faltan se omiten con un aviso). Genera
`matrix.csv`, `consistency.csv` (fracción de mercados con resultado positivo, mediana y peor
caso) y `report.html`. No usa el período de test.

## Informes

Cada orden genera su propio `report.html`. Para regenerar el informe de un backtest a
partir de sus archivos exportados:

```bash
bql report --run-dir outputs/backtest_BTCUSDT_1h_donchian_breakout_<fecha>
```

Todas las evaluaciones quedan registradas en `outputs/experiments.jsonl`. Ese registro
permite contar las configuraciones probadas, un dato necesario para el Deflated Sharpe.

## Ejemplo completo reproducible

```bash
python examples/full_workflow.py
```

Ejecuta el flujo completo con datos sintéticos en un directorio temporal.

## Pruebas y calidad

```bash
pytest                 # pruebas unitarias e integración (sin red)
ruff check .           # lint
ruff format --check .  # formato
mypy src               # tipos
```

## Solución de problemas

| Síntoma | Causa y solución |
|---|---|
| `No existe data/processed/...parquet` | Descarga (`bql download`), importa (`bql import`) o genera (`bql synth`) los datos primero. |
| `HTTP 403` al descargar | IP bloqueada por exceso de peticiones o red que bloquea Bybit. Espera al menos 10 minutos; comprueba proxy o cortafuegos. |
| `Reintentos agotados` | Red inestable o API caída. Reintenta más tarde; ajusta `data.max_retries`. |
| `Datos inválidos` | Ejecuta `bql validate-data`; reimporta o vuelve a descargar con `--refresh`. |
| `Segmento ... vacío` | Muy pocas velas para la separación train/validación/test; usa más datos. |
| `La rejilla tiene N combinaciones` | Reduce la rejilla o sube `validation.max_grid_size`, sabiendo que cada prueba adicional aumenta el riesgo de sobreajuste. |
| `ya se evaluó en el período de test` | Protección intencionada. Ver [`docs/methodology.md`](docs/methodology.md). |
| `bql: command not found` | Activa el entorno virtual o ejecuta `python -m bybit_quant_lab.cli`. |

## Limitaciones del modelo

- Velas OHLC: el orden intravela es desconocido. Se asume siempre el stop antes que el
  objetivo, y los gaps se ejecutan a la apertura.
- Todas las órdenes se simulan como *taker* con slippage fijo en puntos básicos; no se
  modela el impacto de mercado según el tamaño.
- Liquidación aproximada (margen aislado, tasa de mantenimiento fija): se pierde el margen
  inicial completo.
- Funding: se aplica solo si se ha descargado, valorado a la apertura de la vela del pago.
- Una posición a la vez por símbolo. Sin cierres parciales ni cartera multiactivo.
- Especificaciones de instrumentos por defecto marcadas como no verificadas. Contrástalas
  con `instruments-info`.
- Las pruebas del proyecto usan datos sintéticos y respuestas HTTP simuladas. **La
  descarga contra la API real no se ha verificado en el entorno de desarrollo**, que
  bloqueaba el acceso a Bybit; debe comprobarse en el entorno del usuario.

Ver [`docs/methodology.md`](docs/methodology.md), [`docs/metrics.md`](docs/metrics.md) y
[`docs/risk_management.md`](docs/risk_management.md).

## Documentación

- [`docs/user_guide.md`](docs/user_guide.md): guía de uso paso a paso.
- [`docs/architecture.md`](docs/architecture.md): diseño e interfaces.
- [`docs/strategies.md`](docs/strategies.md): las diez estrategias, con fórmulas y parámetros.
- [`docs/methodology.md`](docs/methodology.md): convenciones temporales, ejecución,
  validación y control del sobreajuste.
- [`docs/risk_management.md`](docs/risk_management.md): límites de riesgo.
- [`docs/metrics.md`](docs/metrics.md): fórmulas de las métricas.
- [`docs/data_sources.md`](docs/data_sources.md): API de Bybit, disponibilidad y calidad de datos.
- [`docs/progress.md`](docs/progress.md): estado verificado de cada fase y tareas pendientes.
