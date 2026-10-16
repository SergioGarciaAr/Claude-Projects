# L13. Derivados en tiempo discreto

Índice detallado · Versión 1.0 · Entrega 1c · 2026-10-16

## Ficha editorial

- **Serie:** III. Teoría financiera y modelización.
- **Requisitos:** L3, L5, L8, L10, L12.
- **Capítulos:** 9, más un apéndice.
- **Extensión estimada:** 260–320 páginas.

**Propósito.** Este libro desarrolla la valoración de derivados por arbitraje sin cálculo estocástico. Comienza con contratos a plazo, futuros y swaps, que se valoran por replicación estática; sigue con las cotas de arbitraje y la paridad put-call; y construye el modelo binomial de uno y varios períodos, con replicación dinámica, medida neutral al riesgo, martingalas discretas y opciones americanas como problema de parada óptima. Demuestra la convergencia del modelo de Cox-Ross-Rubinstein a la fórmula de Black-Scholes mediante el teorema central del límite de L8. El tratamiento en tiempo continuo se deja para L19.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro (NOTACION §8.3).

## Capítulos

### Capítulo 1. Contratos a plazo y futuros

**Prerrequisitos:** L10 c. 2, L10 c. 8, L5 §2.4, L5 c. 10, L8 c. 7.

**Objetivos:** describir pagos y posiciones de contratos a plazo; demostrar por replicación el precio a plazo de un activo sin ingresos, con dividendos conocidos y con rendimiento continuo; valorar un contrato existente; describir la marcación a mercado de los futuros; demostrar la igualdad de precios a plazo y futuros con tasas deterministas; calcular la razón de cobertura de mínima varianza; demostrar la paridad cubierta de tasas de interés.

**Secciones:**

- **1.1** Contratos a plazo: pago y posiciones.
- **1.2** Precio a plazo por replicación: costo de mantenimiento.
- **1.3** Valor de un contrato a plazo existente.
- **1.4** Futuros: marcación a mercado y márgenes.
- **1.5** Precio futuro y precio a plazo con tasas deterministas.
- **1.6** Base y cobertura con futuros; razón de cobertura de mínima varianza.
- **1.7** Contratos a plazo de divisas: paridad cubierta de tasas de interés y desvíos documentados (resultado empírico).

**Resultados principales:** fórmulas del precio a plazo; igualdad entre precios a plazo y futuros con tasas deterministas; paridad cubierta; razón de cobertura de mínima varianza.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** cobertura con futuros sobre datos simulados.

**Extensión estimada:** 30–36 páginas; 35–45 ejercicios.

### Capítulo 2. Swaps

**Prerrequisitos:** L13 c. 1, L5 c. 10.

**Objetivos:** describir la estructura de un swap de tasas de interés; valorarlo como diferencia de bonos y como cartera de acuerdos de tasa futura; calcular la tasa swap par; valorar swaps de divisas; identificar el riesgo de contraparte y las limitaciones de la valoración con una sola curva.

**Secciones:**

- **2.1** Swaps de tasas de interés: estructura y convenciones.
- **2.2** Valoración como diferencia de bonos.
- **2.3** Valoración como cartera de acuerdos de tasa futura.
- **2.4** Tasa swap par.
- **2.5** Swaps de divisas.
- **2.6** Riesgo de contraparte y valoración con varias curvas (anticipo de L22 c. 2).

**Resultados principales:** equivalencia de las dos representaciones de valoración; fórmula de la tasa swap par.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** valoración de swaps con una curva construida en L5 c. 10.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

### Capítulo 3. Opciones: cotas de arbitraje y paridad put-call

**Prerrequisitos:** L13 c. 1, L10 c. 8, L2 §1.7.

**Objetivos:** describir tipos de opciones, pagos y estrategias combinadas; demostrar cotas de arbitraje para opciones europeas y americanas; demostrar la paridad put-call; demostrar que no conviene ejercer anticipadamente una opción de compra americana sobre un activo sin dividendos; demostrar la convexidad del precio respecto del precio de ejercicio; obtener precios implícitos de estado mediante mariposas.

**Secciones:**

- **3.1** Opciones: tipos, pagos y posiciones.
- **3.2** Estrategias combinadas: diferenciales, cunas y mariposas.
- **3.3** Cotas de arbitraje para opciones europeas y americanas.
- **3.4** Paridad put-call.
- **3.5** Ejercicio anticipado de opciones de compra americanas sin dividendos.
- **3.6** Monotonía y convexidad del precio respecto del precio de ejercicio.
- **3.7** Precios implícitos de estado a partir de mariposas.

**Resultados principales:** cotas de arbitraje; paridad put-call; no optimalidad del ejercicio anticipado de la opción de compra; convexidad en el precio de ejercicio.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** verificación de cotas con precios observados (datos por verificar en 1e).

**Extensión estimada:** 28–34 páginas; 35–45 ejercicios.

### Capítulo 4. Modelo binomial de un período

**Prerrequisitos:** L13 c. 3, L10 c. 8.

**Objetivos:** formular el modelo binomial de un período; demostrar la condición de ausencia de arbitraje d < 1 + r < u; replicar un derivado y obtener su precio; construir la probabilidad neutral al riesgo; explicar por qué el precio no depende de la probabilidad real; mostrar que el modelo trinomial es incompleto y calcular su intervalo de precios.

**Secciones:**

- **4.1** El modelo y la condición de ausencia de arbitraje.
- **4.2** Replicación: delta y bono.
- **4.3** Probabilidad neutral al riesgo.
- **4.4** Por qué no interviene la probabilidad real.
- **4.5** Modelo trinomial: incompletitud e intervalo de precios.

**Resultados principales:** condición de ausencia de arbitraje; fórmula de valoración de un período.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** no corresponde.

**Extensión estimada:** 20–26 páginas; 25–35 ejercicios.

### Capítulo 5. Modelo binomial de varios períodos y martingalas discretas

**Prerrequisitos:** L13 c. 4, L8 c. 2, L8 c. 9, L8 c. 14, L3 c. 6.

**Objetivos:** construir árboles recombinantes; definir estrategias autofinanciadas; valorar por inducción hacia atrás y obtener la fórmula cerrada para opciones europeas; demostrar que los precios descontados son martingalas bajo la medida neutral al riesgo; valorar opciones dependientes de la trayectoria; implementar y verificar el modelo.

**Secciones:**

- **5.1** Árbol recombinante.
- **5.2** Estrategias autofinanciadas y replicación dinámica.
- **5.3** Valoración por inducción hacia atrás; fórmula cerrada para opciones europeas.
- **5.4** Martingalas en el árbol.
- **5.5** Opciones dependientes de la trayectoria.
- **5.6** Implementación y verificación.

**Resultados principales:** existencia y unicidad de la estrategia replicante; propiedad de martingala de los precios descontados; fórmula binomial cerrada.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** implementación del árbol con pruebas.

**Extensión estimada:** 30–36 páginas; 30–40 ejercicios.

### Capítulo 6. Opciones americanas como problema de parada óptima

**Prerrequisitos:** L13 c. 5, L12 c. 11.

**Objetivos:** formular la valoración americana como parada óptima; calcular la envolvente de Snell en el árbol; describir la frontera de ejercicio; demostrar que puede ser óptimo ejercer anticipadamente una opción de venta americana con tasas positivas; construir la estrategia de súper replicación; implementar y verificar.

**Secciones:**

- **6.1** Formulación como problema de parada óptima.
- **6.2** Envolvente de Snell en el árbol.
- **6.3** Frontera de ejercicio.
- **6.4** Ejercicio anticipado de la opción de venta americana.
- **6.5** Cobertura de una opción americana: súper replicación.
- **6.6** Implementación y verificación.

**Resultados principales:** el precio americano es el valor de la envolvente de Snell; tiempo de parada óptimo; estrategia de súper replicación.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** valoración de opciones americanas en árboles.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

### Capítulo 7. Cobertura en tiempo discreto

**Prerrequisitos:** L13 c. 5, L8 c. 7, L8 §9.5.

**Objetivos:** construir la cobertura delta exacta en el árbol; cuantificar por simulación el error de cobertura con rebalanceo discreto cuando el modelo no coincide con la realidad; relacionar gamma y frecuencia de rebalanceo; incorporar costos de transacción; calcular coberturas de mínima varianza en mercados incompletos de un período.

**Secciones:**

- **7.1** Cobertura delta en el árbol.
- **7.2** Error de cobertura con rebalanceo discreto.
- **7.3** Gamma y frecuencia de rebalanceo.
- **7.4** Costos de transacción en la cobertura.
- **7.5** Cobertura de mínima varianza en mercados incompletos.

**Resultados principales:** exactitud de la cobertura en el árbol; fórmula de la cobertura de mínima varianza.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** simulación de estrategias de cobertura.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

### Capítulo 8. Convergencia del modelo de Cox-Ross-Rubinstein a la fórmula de Black-Scholes

**Prerrequisitos:** L13 c. 5, L13 §3.4, L8 c. 11, L4 c. 10.

**Objetivos:** parametrizar el árbol de Cox-Ross-Rubinstein; obtener la distribución del logaritmo del precio terminal bajo la medida neutral al riesgo; aplicar el teorema central del límite para arreglos triangulares para demostrar la convergencia a una lognormal; demostrar la convergencia del precio de la opción de venta y deducir la de la opción de compra mediante la paridad; obtener la fórmula de Black-Scholes; explicar qué no demuestra este límite.

**Secciones:**

- **8.1** Parametrización de Cox-Ross-Rubinstein.
- **8.2** Distribución del logaritmo del precio terminal.
- **8.3** Convergencia en distribución mediante el teorema central del límite para arreglos triangulares.
- **8.4** Convergencia del precio de la opción de venta (pago acotado y continuo) y de la opción de compra (paridad).
- **8.5** La fórmula de Black-Scholes como límite.
- **8.6** Velocidad de convergencia y oscilaciones: observación numérica.
- **8.7** Qué no demuestra este límite: la teoría en tiempo continuo (L19).

**Resultados principales:** convergencia del precio binomial al de Black-Scholes.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** convergencia numérica del árbol.

**Extensión estimada:** 24–30 páginas; 20–30 ejercicios.

### Capítulo 9. Opciones exóticas en árboles y límites del modelo

**Prerrequisitos:** L13 c. 6, L13 c. 8, L12 c. 9.

**Objetivos:** valorar opciones de barrera en árboles y explicar sus problemas de convergencia; tratar opciones asiáticas y justificar el uso de Monte Carlo; construir árboles para dos activos; describir la calibración de árboles a precios observados; enumerar los límites del modelo binomial.

**Secciones:**

- **9.1** Opciones de barrera en árboles.
- **9.2** Opciones asiáticas: dependencia de la trayectoria y Monte Carlo.
- **9.3** Opciones sobre dos activos: árboles multidimensionales.
- **9.4** Calibración de árboles a precios observados.
- **9.5** Límites del modelo binomial: volatilidad constante y mercado completo.

**Resultados principales:** no corresponde; capítulo de métodos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** valoración de exóticas por árbol y por simulación.

**Extensión estimada:** 22–28 páginas; 20–30 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
