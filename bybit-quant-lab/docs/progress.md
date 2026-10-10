# Registro de progreso

Estado verificado ejecutando las pruebas de cada fase (no se marca ninguna fase como
terminada sin ejecutar sus pruebas). Resultados de rentabilidad: ninguno real; todas las
ejecuciones usan datos sintéticos.

| Fase | Contenido | Pruebas | Estado |
|---|---|---|---|
| 1. Corte vertical | Datos sintéticos, indicadores, EMA crossover, motor, riesgo, métricas | `test_engine.py`, `test_risk.py`, `test_indicators.py` | Completa |
| 2. Datos | Cliente Bybit V5 (mocks), descarga incremental, validación, Parquet, importación | `test_data.py` | Completa (red real pendiente) |
| 3. Estrategias | Las diez estrategias, registro, no look-ahead | `test_strategies.py` | Completa |
| 4. Combinación y validación | 5 modos de combinación, régimen, redundancia, splits, walk-forward, DSR, Holm, bootstrap, guarda de test, matriz de mercados | `test_signals.py`, `test_validation.py` | Completa |
| 5. Informes y CLI | HTML/CSV/JSON, metadatos, `bql` (11 órdenes) | `tests/integration/` | Completa |
| 6. Verificación | ruff, mypy, pytest, instalación desde venv limpio (`scripts/verify_clean_install.sh`) | — | Completa |

## Pendiente

1. **Descarga real desde `api.bybit.com`.** Bloqueada por el proxy del entorno de
   desarrollo (HTTP 403 en el túnel). El cliente construye la petición correcta y gestiona
   el error con reintentos y código de salida 2, pero ningún dato real se ha descargado ni
   validado. Verificación a realizar por el usuario:
   ```bash
   bql download --symbol BTCUSDT --timeframe 1h --start 2024-01-01 --end 2024-03-01 --funding
   bql validate-data --symbol BTCUSDT --timeframe 1h
   ```
   Comprobar además que `meta.json` registra las peticiones y que el funding descargado tiene
   marcas cada 8 horas (o el intervalo vigente del contrato).
2. **Especificaciones de instrumentos** verificadas con `instruments-info` (hoy son valores de
   referencia marcados como no verificados).
3. **Pruebas de integración con datos reales** (las actuales usan datos sintéticos y HTTP
   simulado; no sirven para evaluar rentabilidad).
4. No implementado (fuera del alcance inicial, documentado): cierres parciales, órdenes limit
   maker, cartera multiactivo simultánea, niveles de riesgo de liquidación de Bybit, fuentes
   de interés abierto, bid/ask y operaciones individuales (solo interfaces).
