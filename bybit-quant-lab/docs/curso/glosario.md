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
