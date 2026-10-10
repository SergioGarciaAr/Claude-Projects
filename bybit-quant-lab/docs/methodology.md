# Metodología

Este documento describe las decisiones que afectan a la interpretación de los resultados.

## 1. Convenciones temporales

- Todas las marcas de tiempo están en **UTC**. El índice `open_time` marca la **apertura** de
  cada vela.
- Una señal de la vela `t` se calcula con datos hasta su **cierre** (incluido `C[t]`).
- Esa señal se ejecuta en la **apertura de `t+1`** (`O[t+1]`), con slippage adverso y comisión
  taker. Nunca se ejecuta al precio de la vela que la generó.
- Indicadores causales: solo `rolling`/`ewm` hacia atrás, EMAs recursivas (`adjust=False`),
  sin `center` ni relleno hacia atrás. Los canales y medias que deben excluir la vela actual se
  desplazan una vela (Donchian, media de volumen, desviación típica del z-score VWAP).
- La temporalidad superior solo se expone cuando la vela superior ha cerrado (ver estrategia 5).
- No hay normalizaciones globales: ningún indicador usa estadísticas de toda la serie.

Verificación automática (`tests/unit/test_strategies.py`, `test_signals.py`): para cada
estrategia y para el clasificador de régimen, calcular con la serie truncada en `t` produce
exactamente los mismos valores hasta `t`, y perturbar el futuro no altera el pasado.

## 2. Modelo de ejecución

Orden de eventos dentro de cada vela `i` (`backtesting/engine.py`):

1. **Cambio de día UTC.** El gestor de riesgo reinicia la referencia diaria.
2. **Funding.** Los pagos con marca en `(open[i-1], open[i]]` se aplican a la posición
   mantenida al final de `i-1`, valorados a `open[i]`. Un largo paga si la tasa es positiva.
3. **Gap.** Si la apertura ya supera el stop, la liquidación o el objetivo, la posición se
   cierra a la apertura (el precio realmente disponible).
4. **Órdenes pendientes** decididas al cierre de `i-1`: primero la salida y después la
   entrada, ambas a `open[i]`.
5. **Intravela, con la regla *stop primero*.** Si en la misma vela se tocan el nivel adverso
   (stop o liquidación) y el objetivo, se asume que se tocó **primero el adverso**. Nunca se
   supone el resultado más favorable.
6. **Cierre.** Valoración mark-to-market, registro de equity y evaluación de límites de riesgo.
7. **Trailing stop.** Se actualiza con el cierre y rige desde la vela siguiente (solo puede
   mejorar el stop).
8. **Decisión.** Se lee la señal al cierre y se programan órdenes para `open[i+1]`.

Supuestos de órdenes:

- Entradas y salidas por señal: a mercado en la apertura, como taker, con `slippage_bps`
  adverso.
- Stop-loss y take-profit: órdenes condicionales que, al dispararse, se ejecutan a mercado
  (el comportamiento por defecto de TP/SL en Bybit). Se ejecutan al nivel con slippage adverso
  y comisión taker. Si hay gap, se ejecutan a la apertura.
- Las entradas son *edge-triggered*: solo se abre posición cuando el estado objetivo cambia a
  LONG o SHORT. Si un stop cierra la posición y la estrategia sigue en LONG, no se reabre hasta
  una nueva transición.
- Una entrada rechazada por riesgo (pausa, límite diario, margen, tamaño mínimo) no se difiere
  a velas posteriores.
- Al final de los datos, la posición abierta se cierra al último cierre (`end_of_data`).
- Liquidación (margen aislado, aproximación):
  `P_liq = entrada · (1 - 1/apalancamiento + mmr)` para largos (simétrico para cortos). Al
  liquidarse se pierde el margen inicial completo. Si la distancia del stop es mayor o igual
  que la distancia a la liquidación, la entrada se rechaza (`stop_beyond_liquidation`).

## 3. Modelo de costes

| Concepto | Defecto | Notas |
|---|---|---|
| Comisión taker | 0,055 % | Tarifa base publicada por Bybit para perpetuos USDT (no VIP). Verificar la tarifa de la cuenta. |
| Comisión maker | 0,02 % | Configurable; el simulador actual ejecuta todo como taker. |
| Slippage | 2 pb | Adverso en cada ejecución. No depende del tamaño. |
| Funding | según datos | Solo si se ha descargado `/v5/market/funding/history`. Si no, se excluye con advertencia. |

Las comisiones se calculan sobre el nocional (`cantidad · precio de ejecución`).
**Resultado bruto** frente a **neto**:

- Cada operación registra `gross_pnl` (a precios de referencia sin slippage), `fees`,
  `slippage_cost` y `funding`, de modo que
  `net_pnl = gross_pnl - fees - slippage_cost - funding`. Esta identidad está verificada en
  `tests/unit/test_engine.py`.
- `bql compare` ejecuta además cada candidato **sin costes** (configuración bruta). Como el
  dimensionamiento incluye los costes estimados, el tamaño de las posiciones y la secuencia de
  operaciones pueden diferir ligeramente entre ambas versiones.

## 4. Separación de datos y protocolo anti-fuga

1. **Segmentos cronológicos.** Entrenamiento (60 %), validación (20 %) y test (20 %), con
   `embargo_bars` opcional entre segmentos. Los segmentos no se solapan, y esto se comprueba en
   el código y en las pruebas.
2. Las señales se calculan una vez sobre toda la serie. Al ser causales, el valor en `t` no
   depende de datos futuros. Cada segmento se simula por separado y empieza sin posición.
3. **Ajustes con entrenamiento:** la selección de estrategias no redundantes (correlación de
   señales en train) y los pesos de la votación ponderada (Sharpe de train, no negativos).
4. **Ajustes con validación:** el umbral de la votación ponderada (rejilla de 4 valores, que se
   registra) y la **selección de candidatos** (top-K por `selection_metric`, con un mínimo de
   operaciones).
5. **Test final.** Solo se evalúa la selección congelada en `selection.json`, una vez. El
   registro `experiments.jsonl` bloquea una segunda evaluación salvo con `--allow-repeat`, y
   entonces el informe advierte que el resultado ya no es independiente. Si los datos cambian
   (otro hash), la evaluación se rechaza.
6. La sensibilidad de parámetros no admite el segmento de test.

## 5. Walk-forward

Ventanas de `wf_train_bars` y `wf_test_bars`, desplazadas `wf_step_bars` (por defecto, el
tamaño del test). Pueden ser deslizantes o ancladas (`wf_anchored`). En cada ventana se evalúa
la rejilla en entrenamiento, se elige la mejor configuración por `selection_metric` (con un
mínimo de operaciones; los empates se resuelven por el orden de la rejilla) y se simula en la
ventana de test siguiente. Los retornos fuera de muestra se encadenan. La tabla in-sample
completa se exporta para analizar la estabilidad.

## 6. Control del sobreajuste y pruebas múltiples

- **Registro de configuraciones:** cada evaluación queda en `experiments.jsonl`. El número de
  configuraciones distintas evaluadas en validación con los mismos datos (en todas las
  ejecuciones, no solo la actual) se usa como número de pruebas.
- **Deflated Sharpe Ratio** (Bailey y López de Prado, 2014). Se estima el Sharpe máximo
  esperado por azar entre `N` pruebas con varianza `V` de sus Sharpe:
  `SR0 = sqrt(V) · ((1-γ)·Φ⁻¹(1-1/N) + γ·Φ⁻¹(1-1/(N·e)))`. Después,
  `DSR = PSR(SR0) = Φ((SR - SR0)·sqrt(T-1) / sqrt(1 - asimetría·SR + (curtosis-1)/4·SR²))`,
  con SR por vela. *Supuestos:* retornos estacionarios y sin autocorrelación (no se corrige).
- **Holm-Bonferroni** sobre los p-valores unilaterales de la expectativa por operación (H0:
  media ≤ 0). Usa una aproximación normal del estadístico t; con menos de 30 operaciones se
  marca como poco fiable.
- **Bootstrap i.i.d.** (semilla fija) del PnL neto por operación: intervalo percentil del 95 %.
  Ignora la dependencia temporal.
- **Dependencia de pocas operaciones:** resultado sin las k mejores operaciones y sin el 5 %
  superior, e indicación de si el signo cambia.
- **Estabilidad de la rejilla:** fracción de configuraciones positivas, mediana frente a la
  mejor y dispersión.
- **Benchmarks:** buy-and-hold 1x con costes, efectivo (la referencia neutral para sistemas
  long/short) y entradas aleatorias con semilla fija. Estas últimas tienen la misma fracción de
  velas activas y una duración media similar, y se simulan con los mismos stops y costes.
- **Redundancia:** correlación y coincidencia de señales en entrenamiento. Las combinaciones
  pueden excluir miembros redundantes (`dedup_vote`) y la votación por categorías evita el
  doble conteo de información de la misma familia.

Ninguna estrategia se declara rentable por su tasa de acierto. La lectura debe considerar
expectativa neta, distribución, costes, drawdown, DSR, dependencia de las mejores
operaciones y estabilidad fuera de muestra.

## 7. Reproducibilidad

- El motor es determinista: sin aleatoriedad salvo el benchmark aleatorio y el bootstrap, que
  usan una semilla fija (`backtest.seed`).
- Los informes incluyen: versión del paquete, commit de git y si hay cambios sin confirmar,
  SHA-256 del contenido de los datos, hash y volcado completo de la configuración, semilla,
  versión de Python y plataforma.
- Pruebas de reproducibilidad: dos ejecuciones idénticas producen la misma equity y las mismas
  operaciones (motor), el mismo resumen y la misma selección (comparación), y métricas y CSV
  idénticos (CLI).
