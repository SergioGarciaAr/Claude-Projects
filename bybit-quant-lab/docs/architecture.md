# Arquitectura

## Flujo de datos

```
Bybit V5 (público) ─┐
CSV / Parquet ──────┼─> data/ (validación, limpieza, Parquet + metadatos)
Sintéticos ─────────┘          │
                               v
                    indicators/ (causales)
                               │
                               v
                    strategies/ ── eventos ──> estado objetivo (signal, conviction, stops)
                               │
                               v
                    signals/ (combinación, régimen, redundancia)   [opcional]
                               │
                               v
            backtesting/engine ── execution/ (costes, fills) ── risk/ (tamaño, límites)
                               │                                 portfolio/ (cuenta)
                               v
                    BacktestResult (equity, operaciones, eventos)
                               │
              ┌────────────────┼──────────────────┐
              v                v                  v
        analytics/       validation/         reporting/
        (métricas)   (segmentos, WF, DSR,   (HTML, CSV, JSON,
                      benchmarks, log)       metadatos)
```

## Decisiones de diseño

1. **Las estrategias no conocen el motor.** Devuelven un DataFrame con el contrato
   `SIGNAL_COLUMNS`. Las combinaciones devuelven el mismo contrato, así que el motor trata
   igual una estrategia individual y una combinación.
2. **Eventos frente a estados.** Las estrategias expresan eventos (cruces, rupturas). La clase
   base los convierte en un estado persistente con reglas explícitas y comunes, lo que permite
   votar sobre el estado ("la estrategia está en LONG").
3. **Entradas por transición.** El motor solo entra cuando el estado cambia. Así se evita
   reentrar de forma repetida tras un stop mientras la estrategia sigue en LONG.
4. **Riesgo separado.** `RiskManager` y `size_position` no dependen de ninguna estrategia.
   El motor los consulta en cada decisión y al ejecutar.
5. **Señales calculadas una vez.** Al ser causales, se calculan sobre toda la serie y los
   segmentos se simulan por separado. Las pruebas de truncamiento garantizan la equivalencia.
6. **Configuración separada del código.** Modelos Pydantic congelados (`extra="forbid"`)
   cargados desde YAML. Los errores de configuración son explícitos.
7. **Corrección antes que velocidad.** Indicadores vectorizados con pandas y motor en un bucle
   Python explícito y legible. Un backtest de unas 6000 velas tarda del orden de décimas de
   segundo, y `bql compare` sobre 6000 velas, unos 2–3 s. Con datos de 5m de varios años, la
   comparación completa puede tardar varios minutos.
8. **Reproducibilidad.** Semilla fija, hash de datos y de configuración, commit de git y
   registro de experimentos en JSONL.
9. **Solo lectura.** No existe módulo de ejecución real. Una futura integración debería vivir
   en un paquete separado (p. ej. `live/`), deshabilitado por defecto y fuera del flujo de
   `bql`.

## Interfaces principales

| Interfaz | Archivo | Firma |
|---|---|---|
| Estrategia | `strategies/base.py` | `Strategy.generate_signals(data) -> DataFrame[SIGNAL_COLUMNS]`; subclases: `compute_events(data) -> Events`, `warmup_bars()` |
| Registro | `strategies/registry.py` | `@register`, `create_strategy(name, params)`, `available_strategies()` |
| Combinación | `signals/combiners.py` | `combine_signals(frames, categories, CombinationConfig, regime) -> DataFrame` |
| Motor | `backtesting/engine.py` | `BacktestEngine(config, symbol, timeframe, spec).run(data, signals, funding, start, end, regime, label, params) -> BacktestResult` |
| Riesgo | `risk/` | `size_position(...) -> SizingResult`, `RiskManager.can_open(i)` |
| Métricas | `analytics/metrics.py` | `compute_metrics(result, min_trades, min_days_for_cagr) -> dict` |
| Investigación | `validation/research.py` | `Researcher.run_comparison`, `.run_final_test`, `.walk_forward`, `.sensitivity` |
| Fuentes de datos | `data/interfaces.py` | Protocolos `FundingSource`, `OpenInterestSource`, `QuoteSource`, `TradeSource` |

## Cómo añadir una estrategia

1. Crea `strategies/mi_estrategia.py` con una subclase de `StrategyParams` y otra de
   `Strategy` decorada con `@register`. Implementa `warmup_bars` y `compute_events` usando
   solo indicadores causales.
2. Impórtala en `strategies/__init__.py`.
3. Añade sus parámetros a `configs/strategies.yaml`.
4. Las pruebas parametrizadas de `tests/unit/test_strategies.py` la cubren automáticamente
   (contrato, no look-ahead y límites). Ajusta la prueba que exige exactamente diez
   estrategias y añade casos conocidos propios.

## Estructura de pruebas

- `tests/unit/`: indicadores, datos (HTTP simulado), estrategias, motor, riesgo, señales y
  validación.
- `tests/integration/`: CLI completa con datos sintéticos en un directorio temporal.
- No hay pruebas con red. Las pruebas con datos reales de Bybit quedan pendientes para el
  entorno del usuario (ver `README.md`).
