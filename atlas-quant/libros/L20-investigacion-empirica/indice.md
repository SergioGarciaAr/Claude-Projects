# L20. Investigación empírica en finanzas: metodología, backtesting y microestructura

Índice detallado · Versión 1.0 · Entrega 1d · 2026-10-16

## Ficha editorial

- **Serie:** V. Investigación.
- **Requisitos:** L9, L10, L12, L14, L17.
- **Uso como aplicación:** L15 (capítulo 10).
- **Capítulos:** 12, más un apéndice.
- **Extensión estimada:** 330–410 páginas.

**Propósito.** Este libro enseña a hacer investigación empírica en finanzas que resista el escrutinio: formular hipótesis antes de mirar los datos, construir bases de datos sin sesgos de supervivencia ni de anticipación, construir señales y carteras, diseñar estudios de eventos y backtests realistas, controlar el sobreajuste y las pruebas múltiples, validar con datos temporales sin fugas, evaluar el desempeño con su incertidumbre, entender la microestructura y la ejecución, gestionar el riesgo operativo y comunicar resultados de forma reproducible. Los resultados empíricos citados se presentan con su fuente y se verifican en la entrega 1e.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro.

## Capítulos

### Capítulo 1. El método científico aplicado a las finanzas

**Prerrequisitos:** L9 c. 6, L9 c. 7, L10 c. 11.

**Objetivos:** formular preguntas investigables; distinguir hipótesis económicas y estadísticas y exigir falsabilidad; diseñar un estudio y su plan de análisis antes de mirar los datos; reconocer los grados de libertad del investigador; distinguir significación estadística y económica; describir la evidencia sobre la replicabilidad de la investigación financiera.

**Secciones:**

- **1.1** Preguntas investigables en finanzas.
- **1.2** Hipótesis económicas y estadísticas; falsabilidad.
- **1.3** Diseño previo: plan de análisis y preregistro.
- **1.4** Grados de libertad del investigador.
- **1.5** Significación económica.
- **1.6** Replicabilidad de la investigación financiera (resultados empíricos).

**Resultados principales:** no corresponde; capítulo metodológico.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** no corresponde.

**Extensión estimada:** 22–28 páginas; 15–25 ejercicios.

### Capítulo 2. Datos financieros

**Prerrequisitos:** L20 c. 1, L10 c. 2, L10 c. 13, L3 c. 12.

**Objetivos:** evaluar fuentes de datos y sus licencias; ajustar precios por eventos corporativos; detectar y corregir el sesgo de supervivencia; evitar el sesgo de anticipación usando fechas de publicación, versiones de datos y bases en tiempo real; detectar errores de datos; construir universos de inversión; documentar la procedencia.

**Secciones:**

- **2.1** Fuentes de datos y licencias.
- **2.2** Ajustes corporativos y precios ajustados.
- **2.3** Sesgo de supervivencia.
- **2.4** Sesgo de anticipación: fechas de publicación, revisiones y datos en tiempo real.
- **2.5** Errores de datos y su detección.
- **2.6** Construcción de universos de inversión.
- **2.7** Documentación de procedencia.

**Resultados principales:** cuantificación del sesgo de supervivencia en un modelo sencillo.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** limpieza y validación de una base de datos.

**Extensión estimada:** 28–34 páginas; 15–25 ejercicios.

### Capítulo 3. Señales y carteras de investigación

**Prerrequisitos:** L20 c. 2, L14 c. 12, L9 c. 13, L17 c. 5.

**Objetivos:** definir y normalizar señales; construir carteras ordenadas y carteras largas-cortas; comparar ponderaciones; neutralizar señales respecto de factores; medir rotación y decaimiento; combinar señales.

**Secciones:**

- **3.1** Señales: definición y normalización robusta.
- **3.2** Carteras ordenadas por cuantiles y carteras largas-cortas.
- **3.3** Ponderación igualitaria y por capitalización.
- **3.4** Neutralización respecto de factores.
- **3.5** Rotación y decaimiento de la señal.
- **3.6** Combinación de señales.

**Resultados principales:** equivalencia entre la cartera larga-corta lineal en el rango y una regresión de corte transversal.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** construcción de carteras de investigación.

**Extensión estimada:** 26–32 páginas; 15–25 ejercicios.

### Capítulo 4. Estudios de eventos

**Prerrequisitos:** L20 c. 2, L9 c. 8, L14 c. 2.

**Objetivos:** diseñar ventanas de estimación y de evento; calcular rendimientos anormales con distintos modelos de rendimiento normal; agregar mediante rendimientos anormales acumulados y de compra y mantenimiento, y derivar sus estadísticos bajo supuestos explícitos; tratar el agrupamiento de eventos; reconocer los problemas de los estudios de largo plazo.

**Secciones:**

- **4.1** Diseño: ventanas de estimación y de evento.
- **4.2** Rendimientos anormales y modelos de rendimiento normal.
- **4.3** Agregación y estadísticos de prueba.
- **4.4** Agrupamiento de eventos y dependencia.
- **4.5** Estudios de largo plazo y el problema del modelo.
- **4.6** Ejemplo: anuncios de resultados.

**Resultados principales:** distribución de los estadísticos de rendimiento anormal acumulado bajo supuestos explícitos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** estudio de eventos con datos.

**Extensión estimada:** 24–30 páginas; 15–25 ejercicios.

### Capítulo 5. Diseño de backtests

**Prerrequisitos:** L20 c. 3, L10 c. 3, L17 c. 12.

**Objetivos:** distinguir lo que un backtest puede y no puede mostrar; simular la ejecución con precios y retrasos realistas; incorporar costos explícitos, diferencial e impacto; estimar la capacidad de una estrategia; incorporar restricciones de préstamo y margen; diseñar una arquitectura reproducible; aplicar una lista de verificación de errores frecuentes.

**Secciones:**

- **5.1** Qué es un backtest y qué no.
- **5.2** Simulación de la ejecución.
- **5.3** Costos: comisiones, diferencial e impacto.
- **5.4** Capacidad de una estrategia.
- **5.5** Restricciones: préstamo de valores y margen.
- **5.6** Arquitectura de un backtest reproducible.
- **5.7** Errores frecuentes: lista de verificación.

**Resultados principales:** no corresponde; capítulo de métodos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** implementación de un motor de backtest con pruebas.

**Extensión estimada:** 30–36 páginas; 15–25 ejercicios.

### Capítulo 6. Sobreajuste y pruebas múltiples en backtests

**Prerrequisitos:** L20 c. 5, L9 c. 7, L14 c. 7.

**Objetivos:** demostrar el sesgo del máximo de índices de Sharpe estimados bajo independencia y normalidad; derivar el índice de Sharpe deflactado bajo sus supuestos; aplicar el *reality check* de White y la prueba SPA de Hansen; estimar la probabilidad de sobreajuste del backtest; controlar la tasa de falsos descubrimientos en la búsqueda de factores.

**Secciones:**

- **6.1** Selección de la mejor estrategia: sesgo del máximo.
- **6.2** Índice de Sharpe deflactado.
- **6.3** *Reality check* de White.
- **6.4** Prueba SPA de Hansen.
- **6.5** Probabilidad de sobreajuste del backtest.
- **6.6** Control de falsos descubrimientos en factores.

**Resultados principales:** esperanza del máximo de estadísticos bajo la hipótesis nula (caso independiente normal).

**Resultados admitidos:** RA-36 (en §6.3), RA-57 (en §6.3 y §6.4).

**Aplicaciones financieras:** todo el capítulo.

**Computación:** simulación de búsquedas y aplicación de las correcciones.

**Extensión estimada:** 28–34 páginas; 15–25 ejercicios.

### Capítulo 7. Validación progresiva, purga y embargo

**Prerrequisitos:** L20 c. 6, L14 c. 7, L9 c. 12.

**Objetivos:** explicar por qué la validación cruzada estándar falla con series temporales; aplicar validación progresiva con distintas ventanas; purgar observaciones cuyas etiquetas se superponen; aplicar embargo; describir la validación cruzada combinatoria purgada; reservar datos para la evaluación final.

**Secciones:**

- **7.1** Por qué falla la validación cruzada estándar.
- **7.2** Validación progresiva.
- **7.3** Etiquetas superpuestas en el tiempo: purga.
- **7.4** Embargo.
- **7.5** Validación cruzada combinatoria purgada.
- **7.6** Evaluación final con datos reservados.

**Resultados principales:** no corresponde; capítulo de métodos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** implementación de particiones purgadas con pruebas.

**Extensión estimada:** 22–28 páginas; 15–25 ejercicios.

### Capítulo 8. Evaluación del desempeño

**Prerrequisitos:** L20 c. 6, L9 c. 4, L14 c. 2, L10 c. 10.

**Objetivos:** calcular medidas de desempeño y de caídas; obtener el error estándar del índice de Sharpe con rendimientos independientes y con autocorrelación; comparar índices de Sharpe; atribuir el desempeño a factores e inferir sobre alfas; estudiar caídas por simulación; distinguir habilidad y suerte.

**Secciones:**

- **8.1** Medidas: Sharpe, Sortino, caída máxima y Calmar.
- **8.2** Error estándar del índice de Sharpe.
- **8.3** Comparación de índices de Sharpe.
- **8.4** Atribución a factores e inferencia sobre alfas.
- **8.5** Caídas: estudio por simulación.
- **8.6** Habilidad y suerte (resultados empíricos).

**Resultados principales:** varianza asintótica del índice de Sharpe estimado (independiente y con autocorrelación).

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** evaluación de una estrategia con intervalos.

**Extensión estimada:** 26–32 páginas; 20–30 ejercicios.

### Capítulo 9. Microestructura del mercado

**Prerrequisitos:** L20 c. 2, L10 c. 3, L8 c. 3, L8 §9.6, L7 c. 6.

**Objetivos:** describir la formación de precios; derivar el diferencial implícito de Roll; introducir las nociones de equilibrio con información asimétrica; derivar el diferencial de selección adversa de Glosten-Milgrom; derivar el equilibrio lineal de Kyle; calcular medidas empíricas de liquidez; reconocer los problemas de los datos de alta frecuencia.

**Secciones:**

- **9.1** Formación de precios: participantes e información.
- **9.2** Modelo de Roll.
- **9.3** Nociones de equilibrio con información asimétrica.
- **9.4** Modelo de Glosten-Milgrom.
- **9.5** Modelo de Kyle.
- **9.6** Medidas empíricas de liquidez: lambda de Kyle e iliquidez de Amihud.
- **9.7** Datos de alta frecuencia: rebote entre compra y venta y negociación asincrónica.

**Resultados principales:** estimador de Roll; diferencial de Glosten-Milgrom; equilibrio lineal de Kyle.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** simulación de los modelos de microestructura.

**Extensión estimada:** 30–36 páginas; 15–25 ejercicios.

### Capítulo 10. Impacto de mercado y ejecución óptima

**Prerrequisitos:** L20 c. 9, L17 c. 12, L7 c. 11, L12 c. 11.

**Objetivos:** distinguir impacto temporal y permanente y describir la evidencia empírica; derivar la solución del modelo de Almgren-Chriss en tiempo discreto y su límite continuo; construir la frontera eficiente de ejecución; describir algoritmos de ejecución estándar; medir el costo de implementación.

**Secciones:**

- **10.1** Impacto temporal y permanente: modelos y evidencia.
- **10.2** Modelo de Almgren-Chriss en tiempo discreto.
- **10.3** Límite en tiempo continuo.
- **10.4** Frontera eficiente de ejecución.
- **10.5** Algoritmos de ejecución: TWAP y VWAP.
- **10.6** Medición del costo de implementación.

**Resultados principales:** trayectoria óptima de Almgren-Chriss.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Usa como aplicación:** L15 c. 2.

**Computación:** cálculo de trayectorias óptimas y simulación de costos.

**Extensión estimada:** 24–30 páginas; 15–25 ejercicios.

### Capítulo 11. Riesgo operativo de los sistemas cuantitativos

**Prerrequisitos:** L20 c. 5, L3 c. 12.

**Objetivos:** analizar fallas documentadas de sistemas; diseñar controles previos a la negociación; monitorizar la deriva entre el backtest y la ejecución real; gestionar versiones de modelos y datos; preparar planes de contingencia; documentar y gobernar sistemas.

**Secciones:**

- **11.1** Fallas de sistemas: casos documentados.
- **11.2** Controles previos a la negociación.
- **11.3** Monitorización: métricas, alertas y deriva.
- **11.4** Versiones de modelos y datos.
- **11.5** Planes de contingencia.
- **11.6** Gobierno y documentación.

**Resultados principales:** no corresponde; capítulo de práctica profesional.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** monitorización de una estrategia simulada.

**Extensión estimada:** 20–26 páginas; 10–20 ejercicios.

### Capítulo 12. Reproducibilidad y comunicación de resultados

**Prerrequisitos:** L20 c. 5, L20 c. 8, L3 c. 12.

**Objetivos:** aplicar principios de reproducibilidad computacional; estructurar un informe de investigación; comunicar la incertidumbre; presentar gráficos y tablas honestos; organizar revisiones internas; reconocer cuestiones éticas.

**Secciones:**

- **12.1** Reproducibilidad computacional.
- **12.2** Estructura de un informe de investigación.
- **12.3** Comunicación de la incertidumbre.
- **12.4** Gráficos y tablas honestos.
- **12.5** Revisión interna y lista de verificación.
- **12.6** Ética: conflictos de interés y uso de datos.

**Resultados principales:** no corresponde; capítulo metodológico.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** informe reproducible de ejemplo.

**Extensión estimada:** 20–26 páginas; 10–20 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice analítico.
