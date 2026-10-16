# L17. Construcción de carteras y gestión del riesgo

Índice detallado · Versión 1.0 · Entrega 1d · 2026-10-16

## Ficha editorial

- **Serie:** IV. Matemática avanzada y tiempo continuo.
- **Requisitos:** L9, L10, L12, L14.
- **Uso como aplicación:** L16 (capítulo 8).
- **Capítulos:** 13, más un apéndice.
- **Extensión estimada:** 370–450 páginas.

**Propósito.** Este libro lleva la teoría de carteras de L10 a la práctica, donde los insumos se estiman con error, y desarrolla la medición y gestión cuantitativa del riesgo. Trata el error de estimación y sus remedios (contracción, restricciones, Black-Litterman), la paridad de riesgo, los modelos de factores de riesgo, las medidas de riesgo coherentes, la estimación y el backtesting del VaR y del Expected Shortfall, la teoría de valores extremos, las cópulas, las pruebas de estrés, el riesgo de liquidez y de modelo, y el rebalanceo. Las normas regulatorias se mencionan con fecha de verificación y nunca como contenido permanente.

**Convención del VaR.** En este libro, VaR_α y ES_α se definen sobre la pérdida L con α como nivel de confianza (por ejemplo, α = 0,99). La definición se fija en L17 §6.2.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro (NOTACION §8.2).

## Capítulos

### Capítulo 1. Error de estimación de los insumos

**Prerrequisitos:** L9 c. 13, L9 c. 14, L10 c. 6, L7 c. 4.

**Objetivos:** cuantificar el error de estimación de medias y covarianzas; relacionar el número de condición de la covarianza estimada con la inestabilidad de la cartera; derivar la sensibilidad de los pesos óptimos respecto de los insumos; demostrar por simulación que la optimización amplifica los errores; extraer consecuencias prácticas.

**Secciones:**

- **1.1** Los insumos de la optimización: **μ** y **Σ**.
- **1.2** Error de estimación de las medias.
- **1.3** Error de estimación de las covarianzas y número de condición.
- **1.4** Sensibilidad de los pesos óptimos respecto de los insumos.
- **1.5** La optimización como maximizadora del error: estudio por simulación.
- **1.6** Consecuencias prácticas.

**Resultados principales:** fórmula de la sensibilidad de los pesos óptimos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** simulación del error de optimización.

**Extensión estimada:** 24–30 páginas; 20–30 ejercicios.

### Capítulo 2. Inestabilidad de la optimización media-varianza y estimadores de contracción

**Prerrequisitos:** L17 c. 1, L9 §13.3, L9 §14.4, L12 c. 7.

**Objetivos:** demostrar el optimismo de las carteras optimizadas evaluadas dentro de la muestra; derivar la intensidad óptima de contracción de covarianzas para parámetros poblacionales conocidos; aplicar el estimador de Ledoit-Wolf; aplicar contracción a las medias; demostrar que la prohibición de ventas en corto actúa como contracción de la covarianza; comparar empíricamente con la cartera de mínima varianza global y la cartera igualitaria; describir la ley de Marchenko-Pastur.

**Secciones:**

- **2.1** Optimismo dentro de la muestra de las carteras optimizadas.
- **2.2** Contracción de covarianzas: intensidad óptima y estimador de Ledoit-Wolf.
- **2.3** Contracción de medias.
- **2.4** Las restricciones como regularización: el resultado de Jagannathan y Ma.
- **2.5** Cartera de mínima varianza global y cartera igualitaria (resultados empíricos).
- **2.6\*** Matrices aleatorias: ley de Marchenko-Pastur y limpieza de covarianzas.

**Resultados principales:** intensidad óptima de contracción (versión con parámetros conocidos); equivalencia entre la restricción de no negatividad y una covarianza contraída.

**Resultados admitidos:** RA-45 (en §2.2), RA-46 (en §2.6).

**Aplicaciones financieras:** todo el capítulo.

**Computación:** comparación fuera de muestra de estimadores de covarianza.

**Extensión estimada:** 30–36 páginas; 20–30 ejercicios.

### Capítulo 3. Modelo de Black-Litterman

**Prerrequisitos:** L17 c. 2, L9 c. 11, L8 §9.6, L10 c. 7.

**Objetivos:** obtener los rendimientos implícitos de equilibrio por optimización inversa; expresar opiniones del inversor como observaciones con ruido; derivar la distribución posterior mediante la condicional de la normal multivariante; interpretar el parámetro de escala y la confianza en las opiniones; implementar el modelo y reconocer sus trampas.

**Secciones:**

- **3.1** Rendimientos implícitos de equilibrio.
- **3.2** Opiniones como observaciones con ruido.
- **3.3** Derivación de la distribución posterior.
- **3.4** Interpretación del parámetro de escala y de la confianza.
- **3.5** Implementación y errores frecuentes.

**Resultados principales:** fórmula posterior de Black-Litterman.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** implementación del modelo.

**Extensión estimada:** 22–28 páginas; 15–25 ejercicios.

### Capítulo 4. Paridad de riesgo y contribuciones al riesgo

**Prerrequisitos:** L10 c. 6, L7 §4.4, L12 c. 7.

**Objetivos:** descomponer el riesgo de una cartera en contribuciones mediante el teorema de Euler; demostrar la existencia y unicidad de la cartera de paridad de riesgo mediante un problema convexo; calcularla numéricamente; medir la diversificación; discutir el apalancamiento que exige.

**Secciones:**

- **4.1** Contribuciones al riesgo y teorema de Euler.
- **4.2** Cartera de paridad de riesgo: existencia y unicidad.
- **4.3** Cálculo numérico.
- **4.4** Medidas de diversificación.
- **4.5** Apalancamiento y limitaciones.

**Resultados principales:** suma de contribuciones; existencia y unicidad de la paridad de riesgo.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** cálculo de carteras de paridad de riesgo.

**Extensión estimada:** 22–28 páginas; 20–30 ejercicios.

### Capítulo 5. Modelos de factores de riesgo

**Prerrequisitos:** L10 c. 10, L14 c. 12, L9 c. 13.

**Objetivos:** expresar la covarianza mediante una estructura factorial; construir modelos fundamentales, estadísticos y macroeconómicos; estimar el riesgo específico; descomponer el riesgo de una cartera por factores; medir y neutralizar exposiciones.

**Secciones:**

- **5.1** Estructura factorial de la covarianza.
- **5.2** Modelos fundamentales: regresiones de corte transversal por período.
- **5.3** Modelos estadísticos: componentes principales.
- **5.4** Modelos macroeconómicos.
- **5.5** Riesgo específico y su estimación.
- **5.6** Descomposición del riesgo de una cartera por factores.
- **5.7** Exposiciones y neutralización.

**Resultados principales:** descomposición de la varianza de una cartera en componentes factorial y específica.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** construcción de un modelo de factores con datos.

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

### Capítulo 6. Medidas de riesgo coherentes

**Prerrequisitos:** L8 §5.7, L8 c. 6, L7 c. 7.

**Objetivos:** fijar la definición del VaR y mostrar que no es subaditivo; enunciar los axiomas de coherencia; definir el Expected Shortfall, representarlo como promedio de cuantiles y como solución de un problema de minimización convexa, y demostrar su coherencia; describir medidas espectrales; explicar la falta de elicitabilidad del Expected Shortfall y sus consecuencias; describir su uso regulatorio con fecha de verificación.

**Secciones:**

- **6.1** Medidas de riesgo: propósito; varianza y desviación.
- **6.2** VaR: definición, propiedades y falla de la subaditividad.
- **6.3** Axiomas de coherencia.
- **6.4** Expected Shortfall: representación por cuantiles, representación de Rockafellar-Uryasev y coherencia.
- **6.5** Medidas espectrales y de distorsión.
- **6.6** Elicitabilidad y consecuencias para el backtesting.
- **6.7** Uso regulatorio (descripción con fecha de verificación).

**Resultados principales:** contraejemplo de subaditividad del VaR; representación de Rockafellar-Uryasev; coherencia del Expected Shortfall.

**Resultados admitidos:** RA-47 (en §6.6).

**Aplicaciones financieras:** todo el capítulo.

**Computación:** cálculo de VaR y ES para distribuciones conocidas.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

### Capítulo 7. Estimación del VaR y del Expected Shortfall

**Prerrequisitos:** L17 c. 6, L14 c. 8, L9 §13.4, L12 c. 9, L8 c. 11.

**Objetivos:** estimar VaR y ES por simulación histórica, métodos paramétricos, Monte Carlo y simulación histórica filtrada con GARCH; analizar el escalamiento temporal y sus fallas; demostrar la normalidad asintótica del cuantil muestral y cuantificar el error de estimación de cuantiles extremos.

**Secciones:**

- **7.1** Simulación histórica.
- **7.2** Métodos paramétricos: normal, t y delta-normal para carteras.
- **7.3** Monte Carlo.
- **7.4** Simulación histórica filtrada con GARCH.
- **7.5** Horizonte: escalamiento por la raíz del tiempo y sus fallas.
- **7.6** Error de estimación de cuantiles: normalidad asintótica del cuantil muestral.

**Resultados principales:** normalidad asintótica del cuantil muestral.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** estimación comparada con datos.

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

### Capítulo 8. Teoría de valores extremos

**Prerrequisitos:** L17 c. 7, L8 c. 10, L8 c. 12, L9 c. 4.

**Objetivos:** normalizar máximos de muestras; enunciar el teorema de Fisher-Tippett-Gnedenko y demostrarlo para colas de tipo Pareto; estimar la distribución de valores extremos generalizada por bloques; enunciar el teorema de Pickands-Balkema-de Haan y ajustar la distribución de Pareto generalizada a excesos; demostrar la consistencia del estimador de Hill para colas Pareto exactas; calcular VaR y ES con colas modeladas; elegir el umbral.

**Secciones:**

- **8.1** Máximos de muestras y normalización.
- **8.2** Teorema de Fisher-Tippett-Gnedenko: enunciado y demostración para colas de tipo Pareto.
- **8.3** Distribución de valores extremos generalizada y método de bloques.
- **8.4** Excesos sobre un umbral: teorema de Pickands-Balkema-de Haan y distribución de Pareto generalizada.
- **8.5** Estimador de Hill.
- **8.6** VaR y ES con colas modeladas.
- **8.7** Elección del umbral y dependencia temporal.

**Resultados principales:** caso Pareto de Fisher-Tippett-Gnedenko; consistencia del estimador de Hill para colas Pareto exactas; fórmulas de VaR y ES con colas de Pareto generalizada.

**Resultados admitidos:** RA-15 (en §8.2 y §8.4), RA-48 (en §8.5).

**Aplicaciones financieras:** todo el capítulo.

**Usa como aplicación:** L16 c. 8.

**Computación:** ajuste de colas con datos de pérdidas.

**Extensión estimada:** 30–36 páginas; 20–30 ejercicios.

### Capítulo 9. Cópulas

**Prerrequisitos:** L8 c. 7, L8 c. 12, L9 c. 4.

**Objetivos:** definir cópulas y demostrar el teorema de Sklar para marginales continuas; demostrar las cotas de Fréchet-Hoeffding; trabajar con cópulas gaussiana, t y arquimedianas; calcular coeficientes de dependencia en las colas y demostrar que la cópula gaussiana no tiene dependencia en las colas; estimar cópulas por máxima verosimilitud en dos etapas; simular; discutir sus limitaciones.

**Secciones:**

- **9.1** Cópulas y teorema de Sklar.
- **9.2** Cotas de Fréchet-Hoeffding.
- **9.3** Cópulas gaussiana, t y arquimedianas.
- **9.4** Dependencia en las colas.
- **9.5** Estimación: pseudo-observaciones y máxima verosimilitud en dos etapas.
- **9.6** Simulación.
- **9.7** Limitaciones y lecciones históricas.

**Resultados principales:** teorema de Sklar (marginales continuas); cotas de Fréchet-Hoeffding; ausencia de dependencia en las colas de la cópula gaussiana.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** agregación de riesgos; dependencia entre pérdidas.

**Computación:** estimación y simulación de cópulas.

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

### Capítulo 10. Backtesting de modelos de riesgo

**Prerrequisitos:** L17 c. 7, L9 c. 6, L8 c. 14.

**Objetivos:** modelar las violaciones del VaR como variables de Bernoulli; aplicar la prueba de cobertura incondicional de Kupiec, la de independencia de Christoffersen y la de cobertura condicional; describir enfoques de backtesting del Expected Shortfall; describir las reglas regulatorias de semáforo con fecha de verificación; estudiar por simulación la potencia de las pruebas.

**Secciones:**

- **10.1** Violaciones del VaR como variables de Bernoulli.
- **10.2** Prueba de cobertura incondicional de Kupiec.
- **10.3** Prueba de independencia de Christoffersen.
- **10.4** Cobertura condicional.
- **10.5** Backtesting del Expected Shortfall.
- **10.6** Reglas regulatorias de semáforo (descripción con fecha de verificación).
- **10.7** Potencia de las pruebas: estudio por simulación.

**Resultados principales:** distribución exacta del número de violaciones bajo el modelo correcto.

**Resultados admitidos:** RA-29 (en §10.3 y §10.4), RA-47 (en §10.5).

**Aplicaciones financieras:** todo el capítulo.

**Computación:** backtesting de los modelos de L17 c. 7.

**Extensión estimada:** 24–30 páginas; 20–30 ejercicios.

### Capítulo 11. Escenarios y pruebas de estrés

**Prerrequisitos:** L17 c. 5, L17 c. 7, L8 §9.6.

**Objetivos:** explicar el propósito de las pruebas de estrés; construir escenarios históricos e hipotéticos consistentes con un modelo de factores; formular pruebas de estrés inversas como problemas de optimización; propagar choques por factores; identificar limitaciones y requisitos de gobierno.

**Secciones:**

- **11.1** Propósito de las pruebas de estrés.
- **11.2** Escenarios históricos.
- **11.3** Escenarios hipotéticos consistentes: choques condicionales en un modelo de factores.
- **11.4** Pruebas de estrés inversas.
- **11.5** Propagación de choques por factores.
- **11.6** Limitaciones y gobierno.

**Resultados principales:** distribución condicional de los factores no estresados.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** escenarios sobre una cartera de ejemplo.

**Extensión estimada:** 22–28 páginas; 15–25 ejercicios.

### Capítulo 12. Riesgo de liquidez y riesgo de modelo

**Prerrequisitos:** L17 c. 7, L10 c. 3, L10 c. 12.

**Objetivos:** estimar el costo de liquidación y el VaR ajustado por liquidez; describir la liquidez de financiamiento y las espirales de apalancamiento; clasificar las fuentes de riesgo de modelo; cuantificarlo mediante conjuntos de modelos y análisis de peor caso; describir prácticas de gobierno de modelos con fecha de verificación.

**Secciones:**

- **12.1** Liquidez de mercado: costo de liquidación y VaR ajustado por liquidez.
- **12.2** Liquidez de financiamiento y espirales de apalancamiento.
- **12.3** Riesgo de modelo: especificación, parámetros e implementación.
- **12.4** Cuantificación mediante conjuntos de modelos y peor caso.
- **12.5** Gobierno de modelos (descripción con fecha de verificación).

**Resultados principales:** fórmula del VaR ajustado por un costo de liquidación lineal.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** comparación de VaR bajo modelos alternativos.

**Extensión estimada:** 24–30 páginas; 15–25 ejercicios.

### Capítulo 13. Rebalanceo

**Prerrequisitos:** L17 c. 2, L10 c. 4, L12 c. 11.

**Objetivos:** explicar la deriva de los pesos; comparar rebalanceo por calendario y por bandas; describir la región de no transacción con costos proporcionales y calcularla numéricamente por programación dinámica; formular la optimización multiperíodo con costos como problema convexo; evaluar reglas de rebalanceo con datos.

**Secciones:**

- **13.1** Por qué rebalancear: deriva de los pesos.
- **13.2** Rebalanceo por calendario y por bandas.
- **13.3** Costos proporcionales y región de no transacción: cálculo por programación dinámica.
- **13.4** Optimización multiperíodo con costos.
- **13.5** Restricciones prácticas.
- **13.6** Evaluación empírica de reglas de rebalanceo.

**Resultados principales:** convexidad del problema multiperíodo con costos proporcionales.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** comparación de reglas por simulación y con datos.

**Extensión estimada:** 24–30 páginas; 15–25 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
