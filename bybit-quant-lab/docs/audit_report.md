# Informe de auditoría técnica y cuantitativa — bybit-quant-lab

- **Fecha:** 2026-10-10.
- **Alcance:** motor de backtesting, diez estrategias, indicadores, validación estadística,
  capa de datos de Bybit y CLI.
- **Código auditado:** commit `fc4e578` (estado previo). Correcciones en `a50ac62` y
  `697b6af`; este informe se añade en el commit siguiente.
- **Entorno:** Python 3.13.16, pandas 3.0.6, numpy 2.5.3, pytest 9.1.1, ruff 0.17.0, mypy 2.4.0.

> **Advertencia.** Ninguna verificación de este informe usa datos reales de mercado. Todas
> las simulaciones usan datos sintéticos, y la API de Bybit se probó con dobles HTTP. Nada de
> lo aquí descrito indica que alguna estrategia sea rentable.

## 1. Resumen

| Severidad | Hallazgos | Corregidos | Pendientes (documentados) |
|---|---|---|---|
| Alta | 3 | 3 | 0 |
| Media | 6 | 4 | 2 |
| Baja | 6 | 3 | 3 |
| Informativa | 4 | — | 4 |

No se encontró **look-ahead** en las rutas de señales y ejecución. Los errores de severidad
alta eran fugas de información del **período de test** hacia decisiones de investigación, y
estaban en el flujo de validación, no en el motor.

**Evidencia general.** Las pruebas de auditoría actuales se ejecutaron sobre el código
anterior a la auditoría (`fc4e578`, en un worktree temporal). Fallaron exactamente las
**11 pruebas de regresión** de los hallazgos corregidos y pasaron las **139 pruebas de
verificación** (fórmulas, indicadores, contabilidad, peticiones de datos). Con las
correcciones pasan todas. Para reproducirlo:

```bash
git worktree add /tmp/preaudit fc4e578
cp -r bybit-quant-lab/tests/. /tmp/preaudit/bybit-quant-lab/tests/
# psr_from_moments es un refactor posterior sin cambio de comportamiento:
cp bybit-quant-lab/src/bybit_quant_lab/validation/overfitting.py \
   /tmp/preaudit/bybit-quant-lab/src/bybit_quant_lab/validation/
cd /tmp/preaudit/bybit-quant-lab
PYTHONPATH=src <ruta>/bybit-quant-lab/.venv/bin/pytest -p no:cacheprovider -rf \
  tests/unit/test_audit_engine.py tests/unit/test_audit_statistics.py \
  tests/unit/test_audit_data.py tests/unit/test_audit_indicators.py tests/unit/test_strategies.py
# Resultado obtenido: 11 failed, 139 passed
```

## 2. Hallazgos

### Severidad alta

**A-01. El walk-forward usaba el período de test final.**
- Afecta a `validation/research.py`, `Researcher.walk_forward`.
- Las ventanas se construían sobre toda la serie, de modo que el último tramo fuera de muestra
  caía dentro del test. Cualquier decisión tomada con el walk-forward contaminaba el test.
- Evidencia: `test_walk_forward_never_uses_test_segment` falla en `fc4e578` (el último
  `test_end` es posterior al inicio del test).
- Corrección: las ventanas se limitan a entrenamiento + validación, y el rango usado se
  informa en `data_range`.

**A-02. La guarda del test final funcionaba por selección y no por período.**
- Afecta a `validation/experiment_log.py` (`guard_final_test`) y a
  `validation/research.py` (`run_final_test`).
- Una selección distinta (por ejemplo, con otro `top_k`) tenía otro `selection_id` y podía
  evaluarse sobre el mismo período de test sin aviso. Probar varias selecciones contra el test
  equivale a seleccionar con el test.
- Evidencia: `test_final_test_period_can_only_be_used_once` falla en `fc4e578`.
- Corrección: el bloqueo se aplica a cualquier evaluación con el mismo hash de datos y el mismo
  segmento de test. El registro guarda `test_segment`. `--allow-repeat` sigue disponible y
  marca el resultado como no independiente.

**A-03. La selección congelada no estaba realmente congelada.**
- Afecta a `validation/research.py` (`_select` y `run_final_test`).
- El test final reconstruía las combinaciones con los parámetros **vigentes** del YAML, no con
  los usados al seleccionar, y no comprobaba el hash de configuración: costes o riesgo podían
  cambiar entre selección y test.
- Evidencia: fallan en `fc4e578` `test_final_test_uses_frozen_member_params` (la equity del
  test cambia al modificar parámetros tras la selección) y
  `test_final_test_rejects_changed_config`.
- Corrección: `selection.json` guarda `strategy_params` de todas las estrategias individuales,
  y el test final rechaza una configuración o unos datos distintos. Las selecciones antiguas
  sin `strategy_params` se rechazan con un mensaje explícito.

### Severidad media

**M-01. Doble uso del segmento de validación.**
- Afecta a `validation/research.py`, `Researcher.build_combinations`.
- El umbral de `weighted_vote` se elegía con validación y después la misma validación servía
  para seleccionar candidatos, lo que da una ventaja optimista a esa combinación.
- Evidencia: `test_combination_thresholds_not_tuned_on_validation` falla en `fc4e578` (los
  ensayos `combo_trial` se registran en `validation`).
- Corrección: el umbral se elige en entrenamiento, y la validación queda solo para la selección.

**M-02. Un gap más allá de la liquidación se ejecutaba como stop.**
- Afecta a `execution/fills.py`, `check_gap_exit`.
- Si la apertura saltaba por debajo del precio de liquidación de un largo con el stop más
  cerca, se cerraba a la apertura como `stop_loss_gap`, con una pérdida mayor que el margen
  aislado. Era conservador, pero inconsistente con el modelo de margen aislado.
- Evidencia: `test_gap_through_liquidation_loses_isolated_margin_only` falla en `fc4e578`. Con
  entrada a 100, apalancamiento 10, liquidación en 90,5, stop en 92 y apertura en 80, se
  registraba `stop_loss_gap` con una pérdida de 20·qty en lugar de 10·qty.
- Corrección: si la apertura supera la liquidación, se registra `liquidation_gap` y la pérdida
  es igual al margen.

**M-03. Bucle infinito en la paginación del funding.**
- Afecta a `data/bybit_client.py`, `fetch_funding_history`.
- Si la API no respetaba `endTime` y devolvía siempre la misma página completa, el cursor no
  avanzaba y el bucle no terminaba.
- Evidencia: `test_funding_pagination_stops_if_api_does_not_advance` falla en `fc4e578`
  (corte de seguridad a las 50 llamadas).
- Corrección: si la marca más antigua no retrocede, se lanza `BybitAPIError`. **No se ha
  verificado** cómo pagina realmente la API, porque no hay conectividad.

**M-04. Entradas ficticias tras el calentamiento del ATR.**
- Afecta a `strategies/base.py`, `Strategy.generate_signals`.
- La señal se forzaba a FLAT sin stop válido **después** de la máquina de estados. Con un
  `atr_period` mayor que el calentamiento de los indicadores, en la primera vela con ATR
  válido aparecía una transición FLAT→LONG/SHORT sin evento de entrada.
- Evidencia: `test_no_spurious_entry_when_atr_warmup_exceeds_indicator_warmup` falla en
  `fc4e578` (con `ema_crossover`, `fast=3`, `slow=6`, `atr_period=80`: entrada sin cruce en
  la vela 79). Con los parámetros por defecto no se manifestaba, y la prueba parametrizada
  de las diez estrategias pasaba también antes de la corrección.
- Corrección: los eventos de entrada se anulan antes de la máquina de estados.

**M-05. Medida de redundancia débil y categorías no homogéneas (pendiente).**
- Afecta a `signals/redundancy.py` y `signals/combiners.py` (`category_consensus`), y a la
  combinación `dedup_vote`.
- La correlación de Pearson sobre estados −1/0/1 con muchos ceros subestima la redundancia.
  En el entrenamiento sintético (6000 velas, semilla 42), la correlación máxima entre pares
  fue 0,65 (`adx_di`–`donchian_breakout`), así que el umbral 0,7 no descartó **ninguna**
  estrategia y `dedup_vote` usó las diez. En cambio, la coincidencia direccional cuando ambas
  están activas superaba 0,9 entre las estrategias de tendencia.
- Además, la categoría `indicator` mezcla hipótesis de tendencia (`macd_momentum`, `adx_di`)
  y de reversión (`rsi_reversion`, `bollinger_reversion`, `stoch_rsi`). `category_consensus`
  puede contar dos veces información de tendencia (categorías `trend` + `indicator`).
- Estado: no se corrige porque la clasificación A/B/C viene del encargo. Se documenta y se
  recomienda usar `signal_agreement` o miembros explícitos.

**M-06. Huecos de datos (pendiente).**
- Afecta a `indicators/core.py` y `backtesting/engine.py`.
- Los indicadores usan ventanas por número de filas: tras eliminar velas inválidas o con
  huecos del exchange, una ventana "de 20 velas" puede abarcar más tiempo. El motor mantiene
  la posición a través del hueco, y el primer precio tras él se trata como un gap normal.
  `validate-data` informa de los huecos, pero no impide simular.
- Estado: limitación documentada. Revisa los huecos antes de interpretar resultados.

### Severidad baja

**B-01. Combinaciones idénticas.**
- Afecta a `configs/strategies.yaml`.
- `vote_all` (`simple_vote`, margen 3, veto) es matemáticamente idéntica a `consensus_3`
  (n ≥ 3 en una dirección y 0 en la contraria). Inflaba el número de pruebas sin aportar
  información.
- Evidencia: `test_configured_combinations_are_not_equivalent` falla en `fc4e578`, y
  `test_simple_vote_veto_equals_min_consensus_veto` demuestra la equivalencia.
- Corrección: `vote_all` usa `conflict_policy: net`.

**B-02. Benchmark aleatorio.**
- Afecta a `validation/benchmarks.py` (`random_signals`, `random_benchmark`).
- Se calibraba con las señales de toda la serie (incluido el test) y su etiqueta no indicaba
  la estrategia de referencia, mientras la documentación decía "la estrategia evaluada".
- Evidencia: `test_random_benchmark_calibrated_only_on_simulated_segment` falla en `fc4e578`.
- Corrección: se calibra solo con el segmento simulado, la etiqueta es
  `benchmark_random_<referencia>_seed<semilla>` y la documentación es exacta.

**B-03. Walk-forward sin selección válida.**
- Afecta a `Researcher.walk_forward`.
- Si ninguna configuración alcanzaba `min_trades_selection`, se usaba la primera de la rejilla
  sin indicarlo.
- Evidencia: `test_walk_forward_flags_windows_without_valid_selection` falla en `fc4e578`.
- Corrección: columna `selection_valid`.

**B-04. Especificaciones verificadas no conectadas al motor (pendiente).**
- Afecta a `risk/instruments.py` (`get_spec`) y `cli.py`.
- `spec_from_bybit` existe, pero la CLI siempre usa los valores de referencia de
  `DEFAULT_SPECS`. No hay forma de usar las especificaciones verificadas sin código propio.
- Estado: pendiente. Los informes advierten que las especificaciones no están verificadas.

**B-05. Supuestos del DSR (pendiente, documentado).**
- Afecta a `validation/overfitting.py` y `Researcher._select`.
- `n_trials` cuenta las configuraciones distintas de **todas** las ejecuciones registradas,
  pero la varianza de los Sharpe usa solo los candidatos de la ejecución actual. El DSR asume
  retornos i.i.d. y no corrige la autocorrelación.

**B-06. `model_copy` evita la validación del apalancamiento (pendiente).**
- Afecta a `config/models.py`.
- Copiar una configuración con `model_copy(update=...)` no revalida
  `execution.leverage ≤ risk.max_leverage`. No es alcanzable desde YAML o CLI, que sí validan,
  y el dimensionamiento limita igualmente el nocional por `max_leverage`.

### Informativos

- **I-01. Inicialización de Wilder y EMA.** Se siembran con el primer valor válido
  (`ewm(adjust=False)`), no con la media simple de las primeras n velas como TA-Lib. Los
  valores iniciales difieren y convergen después. Está verificado que la implementación cumple
  su propia definición documentada.
- **I-02. Exposición.** Se mide al cierre: una operación abierta y cerrada dentro de la misma
  vela no cuenta como exposición.
- **I-03. Parámetros por defecto.** Son convencionales o arbitrarios y no se han optimizado.
  Convencionales: 12/26/9, 14, 20/2σ, 30/70, 20/80. Arbitrarios: `spike_mult` 2.5,
  `entry_z` 2.0, `max_rel_volume` 1.5, umbrales ADX 20/25/30, `max_holding_bars`, múltiplos de
  ATR y `cooldown_bars`. Cualquier resultado depende de estas elecciones.
- **I-04. Ejecución.** Slippage fijo sin impacto por tamaño, TP ejecutado a mercado con
  slippage y funding valorado a la apertura. Un pago de funding con marca dentro de la última
  vela del segmento no se aplica.

## 3. Verificaciones realizadas sin hallazgos

| Área | Verificación | Prueba |
|---|---|---|
| No retroactividad | En 1067 operaciones de las 10 estrategias (4000 velas sintéticas), toda entrada se ejecuta en `open[t+1]` tras una transición de señal en `t`, con slippage adverso; toda salida por señal también. 0 violaciones. | Script de propiedades (sección 6) y `test_signal_executes_at_next_open` |
| Look-ahead en señales | Truncar la serie o alterar el futuro no cambia ninguna señal pasada (10 estrategias y régimen). | `test_no_lookahead_*`, `test_regime_is_causal` |
| Temporalidad superior | Alterar el futuro no cambia el pasado, y la vela base `t` ve exactamente la última vela de 4h con cierre ≤ `t + 1h`. | `test_higher_timeframe_uses_only_closed_bars` |
| Corto calculado a mano | Precios de ejecución, cantidad, comisiones, slippage, funding (el corto cobra con tasa positiva), PnL bruto y neto, y equity final. | `test_short_trade_with_fees_slippage_and_funding_by_hand` |
| Largo, dimensionamiento y margen | Cantidad = mínimo entre riesgo y límites, redondeada hacia abajo; margen = nocional / apalancamiento; stop dentro de la liquidación. | `test_long_sizing_margin_and_liquidation_price_by_hand` |
| Stops, objetivos y gaps | Stop primero en largos y cortos, TP con gap a la apertura, gap de stop a la apertura, trailing. | `test_audit_engine.py`, `test_engine.py` |
| Bordes temporales | Una señal en la última vela no se ejecuta; un segmento no entra con una señal previa a su inicio. | `test_signal_on_last_bar_is_never_executed`, `test_segment_start_does_not_enter_on_preexisting_signal` |
| Indicadores | ATR, EMA, RSI, ADX/±DI, MACD, Bollinger, OBV, VWAP de sesión, Donchian y StochRSI coinciden con referencias en bucles puros (tolerancia 1e-9). | `test_audit_indicators.py` |
| Métricas | Sharpe, Sortino, drawdown máximo, duración y recuperación, profit factor, tasa de acierto, expectativa, CAGR y rotación frente a cálculo a mano. | `test_metrics_match_hand_computation`, `test_drawdown_duration_and_recovery_by_hand` |
| DSR / PSR | Reproduce el ejemplo numérico de Bailey y López de Prado (2014): SR0 = 0,1132 y DSR = 0,9004 con N = 100, V = 0,5/250, T = 1250, γ3 = −3, γ4 = 10. **Los valores de referencia se citan de memoria: no pude acceder al artículo desde este entorno.** Verificación independiente: el máximo esperado coincide con Monte Carlo (error relativo < 3 % para N = 10, 100 y 1000) y el PSR está calibrado bajo la nula (P(PSR > 0,95) ∈ [3,5 %, 6,5 %] en 2000 simulaciones). | `test_dsr_reproduces_worked_example`, `test_expected_max_sharpe_matches_monte_carlo`, `test_psr_is_calibrated_under_null` |
| Holm | Ajuste escalonado calculado a mano (0,02 / 0,03 / 0,06 / 0,06). | `test_holm_step_down_by_hand` |
| Bootstrap | Cobertura empírica del IC del 95 % entre 89 % y 98 % (300 réplicas). Supuesto i.i.d. | `test_bootstrap_ci_coverage` |
| Separación de datos | Segmentos disjuntos y ordenados; comparación y sensibilidad sin test; selección solo con validación. | `test_validation.py` |
| Peticiones a Bybit | `/v5/market/kline` con `category=linear`, símbolo en mayúsculas, intervalos 5, 15, 60 y 240, `limit=1000`, ventanas contiguas sin solape, salida en UTC ordenada, sin duplicados y alineada; inicio no alineado redondeado hacia arriba. | `test_kline_request_shape_per_timeframe`, `test_unaligned_start_is_rounded_up_to_bar_boundary` |
| Funding frente a velas | El funding usa solo `/v5/market/funding/history` (sin `interval`), se guarda en `<SÍMBOLO>_funding.parquet` y no modifica el dataset de velas (hash idéntico). | `test_funding_uses_its_own_endpoint_and_file` |
| Sintaxis de la CLI | Las 35 órdenes `bql` de los bloques de código de README y `docs/` (incluidas las de la sección 8 de este informe) se analizan sin error. | `test_every_documented_cli_command_parses` |

## 4. Riesgo de sobreajuste (evidencia estructural con datos sintéticos)

`Researcher.run_comparison` con la configuración por defecto, sobre 6000 velas sintéticas de
1h (semilla 42). Las cifras ilustran el riesgo; **no** describen ningún mercado real.

- **Muestras pequeñas:** 7 de 16 candidatos tienen menos de 30 operaciones en validación, y 3
  tienen menos de 10.
- **Pruebas múltiples:** Holm no rechaza la hipótesis nula (expectativa ≤ 0) para ningún
  candidato.
- **DSR de los seleccionados:** `stoch_rsi` 0,80, `obv_trend` 0,39 y `regime_switch` 0,26.
- **Dependencia de pocas operaciones:** `obv_trend` y `regime_switch` cambian de signo al
  quitar sus 3 mejores operaciones.
- **El selector no filtra por estas señales de alarma.** Elige por la métrica de validación
  con un mínimo de operaciones; el DSR, Holm y la dependencia se **informan**, pero no
  bloquean la selección. Antes de dar por buena una selección, revísalos.
- En demostraciones anteriores con estos mismos datos sintéticos, los candidatos elegidos en
  validación perdieron en el test. Es el comportamiento esperable con datos sin estructura
  explotable.

## 5. Qué puede probarse con mocks y qué requiere datos reales

| Se verifica con mocks o sintéticos (hecho) | Requiere conectividad o datos reales (pendiente) |
|---|---|
| Forma de las peticiones, paginación por ventanas, reintentos, errores HTTP y `retCode`, 403, respuestas mal formadas | Que la API real devuelva las velas en `[start, end]` con la semántica supuesta |
| Recorte de la vela no cerrada, UTC, orden y duplicados | Paginación real del funding (`startTime` + `endTime` simultáneos) |
| Descarga incremental y detección de huecos | Disponibilidad histórica por símbolo (`launchTime`) y huecos reales del exchange |
| Separación entre funding y velas | Intervalo real de funding (normalmente 8 h, puede variar) |
| Toda la lógica de estrategias, motor, riesgo, métricas y validación | Especificaciones reales (`instruments-info`) y su uso en el motor (B-04) |
| | Cualquier evaluación de rendimiento de estrategias |

Conectividad comprobada durante la auditoría:
`curl https://api.bybit.com/v5/market/time` → `CONNECT tunnel failed, response 403` (proxy del
entorno). **No se ha probado la conectividad real.**

## 6. Resultados reales de las pruebas

Tras las correcciones, en el entorno indicado arriba:

```
tests/unit/test_audit_engine.py       9 passed
tests/unit/test_audit_indicators.py  11 passed
tests/unit/test_audit_statistics.py  14 passed
tests/unit/test_audit_data.py         8 passed
tests/unit (total)                  224 passed
tests/integration                     7 passed
TOTAL                               231 passed
ruff check .           -> All checks passed!
ruff format --check .  -> 89 files already formatted
mypy src               -> Success: no issues found in 62 source files
```

- Las 178 pruebas previas se conservan sin modificar; no se eliminó ni se debilitó ninguna.
- Se añadieron 53: 42 en los cuatro archivos `test_audit_*.py` y 11 en `test_strategies.py`.
- Script de propiedades de ejecución (no forma parte de la suite): para cada operación
  comprueba que `signal[entry_bar-1] == lado`, que `entry_price == open[entry_bar]·(1 ± slip)`
  y la condición equivalente en las salidas por señal. Resultado: `violaciones: 0` en 1067
  operaciones.

## 7. Limitaciones pendientes

1. Conectividad real con Bybit sin verificar: velas, funding e `instruments-info` (sección 5).
2. M-05 (medida de redundancia y categorías heterogéneas) y M-06 (huecos de datos).
3. B-04 (especificaciones verificadas no conectadas), B-05 (supuestos del DSR) y B-06
   (`model_copy`).
4. No soportado: cierres parciales, órdenes limit maker, cartera multiactivo, niveles de
   riesgo de liquidación de Bybit, impacto de mercado por tamaño.
5. El registro `outputs/experiments.jsonl` es la única barrera contra la reutilización del
   test. Si se borra o se usa otro `--output-dir`, la guarda no puede detectarlo.

## 8. Primer backtest con datos reales (cuando haya conectividad)

Desde `bybit-quant-lab/`, con el entorno virtual activado. Ninguna orden usa credenciales ni
envía operaciones.

```bash
# 1. Comprobar conectividad con la API pública
curl -sS "https://api.bybit.com/v5/market/time"

# 2. Descargar velas y funding (solo lectura)
bql download --symbol BTCUSDT --timeframe 1h --start 2022-01-01 --end 2025-01-01 --funding

# 3. Validar los datos y revisar huecos
bql validate-data --symbol BTCUSDT --timeframe 1h

# 4. Consultar las especificaciones reales (B-04: el motor aún usa las de referencia)
python -c "from bybit_quant_lab.data.bybit_client import BybitPublicClient; from bybit_quant_lab.risk.instruments import spec_from_bybit; print(spec_from_bybit(BybitPublicClient().fetch_instrument_info('BTCUSDT')))"

# 5. Primer backtest, solo en entrenamiento
bql backtest --symbol BTCUSDT --timeframe 1h --strategy ema_crossover --segment train

# 6. Comparación en entrenamiento y validación (el test no se usa)
bql compare --symbol BTCUSDT --timeframe 1h

# 7. Solo cuando la selección esté decidida, y una única vez
bql final-test --selection outputs/compare_BTCUSDT_1h_<fecha>/selection.json
```

Antes del paso 5, comprueba en `data/processed/BTCUSDT_1h.meta.json` el número de peticiones,
el rango obtenido y los huecos. Comprueba también que `BTCUSDT_funding.parquet` contiene
marcas con el intervalo esperado.
