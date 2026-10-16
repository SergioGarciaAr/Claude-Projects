# L10. Mercados financieros y teoría de la valoración

Índice detallado · Versión 1.0 · Entrega 1c · 2026-10-16

## Ficha editorial

- **Serie:** III. Teoría financiera y modelización.
- **Requisitos:** L5, L6, L7, L8, L9.
- **Capítulos:** 13, más un apéndice.
- **Extensión estimada:** 370–450 páginas.

**Propósito.** Este libro presenta los mercados y los instrumentos financieros y desarrolla la teoría de la valoración en tiempo discreto: rendimientos, utilidad esperada, teoría de carteras, CAPM, arbitraje y precios de estado, factor de descuento estocástico y modelos de factores. Cada modelo se presenta con sus hipótesis, su derivación completa y la evidencia empírica disponible, que se distingue explícitamente de los resultados matemáticos. Los capítulos finales tratan la eficiencia de mercado, las fricciones y la información contable, como puente hacia la investigación empírica de la Serie V.

**Resultados empíricos.** Las afirmaciones empíricas de este libro (premios de riesgo, anomalías, contrastes del CAPM) se presentan como resultados empíricos con su fuente, período y muestra. Sus referencias se verificarán en la entrega 1e.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro (NOTACION §8.2).

## Capítulos

### Capítulo 1. Sistema financiero e intermediarios

**Prerrequisitos:** L5 c. 1.

**Objetivos:** describir las funciones del sistema financiero; distinguir los principales intermediarios y sus modelos de negocio; diferenciar mercados primarios y secundarios; describir el papel de los bancos centrales y de la regulación; explicar las particularidades de los mercados emergentes.

**Secciones:**

- **1.1** Funciones del sistema financiero.
- **1.2** Intermediarios: bancos, aseguradoras, fondos de inversión y de pensiones.
- **1.3** Mercados primarios y secundarios.
- **1.4** Bancos centrales y tasas de política monetaria.
- **1.5** Regulación financiera: objetivos y principales marcos (descripción con fecha de verificación).
- **1.6** Mercados emergentes: liquidez, concentración y riesgo cambiario.

**Resultados principales:** no corresponde; capítulo descriptivo.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** no corresponde.

**Extensión estimada:** 20–26 páginas; 15–25 ejercicios.

### Capítulo 2. Instrumentos financieros

**Prerrequisitos:** L10 c. 1, L5 c. 8.

**Objetivos:** describir los derechos asociados a acciones y los eventos corporativos que afectan sus precios; clasificar los instrumentos de renta fija; describir fondos e instrumentos cotizados; leer cotizaciones de divisas; describir contratos derivados; explicar la construcción y el rebalanceo de índices.

**Secciones:**

- **2.1** Acciones: derechos, dividendos y eventos corporativos.
- **2.2** Renta fija: bonos soberanos, corporativos e indexados.
- **2.3** Fondos de inversión e instrumentos cotizados.
- **2.4** Divisas: cotizaciones directas e indirectas, tipos cruzados.
- **2.5** Derivados: contratos a plazo, futuros, opciones y swaps (descripción; la valoración está en L13).
- **2.6** Índices bursátiles: ponderación y rebalanceo.

**Resultados principales:** ajuste de precios por eventos corporativos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** ajuste de una serie de precios por dividendos y desdoblamientos.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 3. Mecanismos de negociación y liquidez

**Prerrequisitos:** L10 c. 2.

**Objetivos:** describir los tipos de órdenes y el funcionamiento de un libro de órdenes; medir la liquidez mediante el diferencial de compraventa, la profundidad y el impacto; clasificar los costos de transacción; describir la compensación y liquidación; explicar la venta en corto, el préstamo de valores, el margen y el apalancamiento.

**Secciones:**

- **3.1** Órdenes de mercado y órdenes limitadas.
- **3.2** Libro de órdenes y subastas.
- **3.3** Diferencial de compraventa, profundidad e impacto.
- **3.4** Costos de transacción explícitos e implícitos.
- **3.5** Compensación y liquidación.
- **3.6** Venta en corto, préstamo de valores, margen y apalancamiento.

**Resultados principales:** no corresponde; capítulo descriptivo con cálculos de costos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** simulación de un libro de órdenes sencillo.

**Extensión estimada:** 24–30 páginas; 20–30 ejercicios.

### Capítulo 4. Rendimientos

**Prerrequisitos:** L10 c. 2, L2 §8.7, L8 c. 7, L8 §6.5, L9 c. 1.

**Objetivos:** calcular rendimientos simples y logarítmicos con dividendos; demostrar que los rendimientos logarítmicos se agregan en el tiempo y los simples entre activos; calcular rendimientos en exceso; comparar las medias aritmética y geométrica; comparar carteras con rebalanceo y de compra y mantenimiento; anualizar explicitando los supuestos.

**Secciones:**

- **4.1** Rendimientos simples y logarítmicos con dividendos.
- **4.2** Agregación temporal y entre activos.
- **4.3** Rendimientos en exceso.
- **4.4** Media aritmética y media geométrica; relación mediante la desigualdad de Jensen.
- **4.5** Carteras con rebalanceo y de compra y mantenimiento.
- **4.6** Anualización y sus supuestos.

**Resultados principales:** reglas de agregación; desigualdad entre media geométrica y aritmética; aproximación de la media geométrica mediante la varianza.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** cálculo de rendimientos y comparaciones de rebalanceo.

**Extensión estimada:** 24–30 páginas; 30–40 ejercicios.

### Capítulo 5. Utilidad esperada y aversión al riesgo

**Prerrequisitos:** L8 §6.5, L8 §8.4, L7 c. 6, L4 c. 6, L4 §13.2.

**Objetivos:** enunciar los axiomas de la utilidad esperada y, en la sección opcional, demostrar el teorema de representación para loterías finitas; relacionar aversión al riesgo y concavidad; calcular equivalentes ciertos, primas de riesgo y coeficientes de Arrow-Pratt; resolver el problema de cartera con un activo riesgoso; demostrar la compatibilidad entre media-varianza y utilidad exponencial con rendimientos normales; describir la evidencia contraria a la utilidad esperada.

**Secciones:**

- **5.1** Preferencias bajo incertidumbre; axiomas de von Neumann y Morgenstern.
- **5.2\*** Teorema de representación para loterías finitas.
- **5.3** Aversión al riesgo y concavidad; equivalente cierto y prima de riesgo.
- **5.4** Coeficientes de Arrow-Pratt; utilidades CARA y CRRA; aproximación de la prima de riesgo.
- **5.5** Cartera con un activo riesgoso: existencia de la solución y estática comparativa.
- **5.6** Cuándo es compatible el criterio media-varianza con la utilidad esperada.
- **5.7** Evidencia contraria: paradoja de Allais y finanzas conductuales (resultados empíricos).

**Resultados principales:** teorema de representación (loterías finitas); aproximación de Arrow-Pratt; equivalencia entre utilidad CARA con normalidad y media-varianza.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** elección de cartera con un activo riesgoso.

**Computación:** cálculo numérico de equivalentes ciertos.

**Extensión estimada:** 30–36 páginas; 35–45 ejercicios.

### Capítulo 6. Teoría de carteras de Markowitz

**Prerrequisitos:** L10 c. 4, L10 c. 5, L7 c. 11, L8 §7.5.

**Objetivos:** calcular la media y la varianza de una cartera; analizar la diversificación con dos activos; derivar la frontera de mínima varianza con n activos y demostrar el teorema de los dos fondos; incorporar un activo libre de riesgo y demostrar el teorema de separación; resolver el problema con prohibición de ventas en corto; identificar los supuestos que la práctica viola.

**Secciones:**

- **6.1** Media y varianza de una cartera.
- **6.2** Dos activos: frontera y diversificación.
- **6.3** n activos riesgosos: frontera de mínima varianza y teorema de los dos fondos.
- **6.4** Activo libre de riesgo: línea del mercado de capitales, cartera tangente y teorema de separación.
- **6.5** Prohibición de ventas en corto.
- **6.6** Supuestos y límites: parámetros conocidos (anticipo de L17).

**Resultados principales:** teorema de los dos fondos; teorema de separación.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** cálculo de fronteras con datos.

**Extensión estimada:** 30–36 páginas; 35–45 ejercicios.

### Capítulo 7. CAPM

**Prerrequisitos:** L10 c. 6, L9 c. 8, L9 c. 9.

**Objetivos:** enunciar los supuestos del CAPM; derivar la relación entre beta y rendimiento esperado; distinguir riesgo sistemático e idiosincrático; estimar el modelo de mercado; describir los contrastes empíricos de series temporales y de corte transversal y sus resultados; explicar la crítica de Roll y la inestabilidad de las betas.

**Secciones:**

- **7.1** Supuestos del equilibrio.
- **7.2** Derivación: la cartera de mercado es la cartera tangente; relación beta-rendimiento esperado.
- **7.3** Línea del mercado de valores.
- **7.4** Riesgo sistemático e idiosincrático.
- **7.5** El modelo de mercado como regresión.
- **7.6** Contrastes empíricos: alfas de series temporales y regresiones de corte transversal (resultados empíricos con fuentes).
- **7.7** Críticas: la cartera de mercado no observable y la inestabilidad de las betas.

**Resultados principales:** relación beta-rendimiento esperado.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** costo de capital; evaluación de desempeño.

**Computación:** estimación de betas y alfas.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 8. Arbitraje en un período

**Prerrequisitos:** L6 c. 13, L7 §7.6, L7 §9.7, L8 c. 1.

**Objetivos:** formular un mercado de un período con escenarios finitos; demostrar que la ley del precio único implica precios lineales; clasificar oportunidades de arbitraje; demostrar el primer teorema fundamental (ausencia de arbitraje equivale a precios de estado estrictamente positivos); construir la medida neutral al riesgo; demostrar la caracterización de la completitud; calcular el intervalo de precios sin arbitraje en mercados incompletos mediante programación lineal.

**Secciones:**

- **8.1** Mercado de un período con escenarios finitos.
- **8.2** Ley del precio único y linealidad de los precios.
- **8.3** Oportunidades de arbitraje.
- **8.4** Primer teorema fundamental de valoración en un período.
- **8.5** Medida neutral al riesgo en un período.
- **8.6** Completitud y unicidad de la medida neutral al riesgo.
- **8.7** Mercados incompletos: intervalo de precios sin arbitraje mediante dualidad.
- **8.8** Cotas de arbitraje para opciones (anticipo de L13 c. 3).

**Resultados principales:** primer y segundo teoremas fundamentales en un período; intervalo de precios sin arbitraje.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** búsqueda de arbitraje y cálculo de cotas mediante programación lineal.

**Extensión estimada:** 30–36 páginas; 30–40 ejercicios.

### Capítulo 9. Factor de descuento estocástico

**Prerrequisitos:** L10 c. 5, L10 c. 8, L8 c. 9, L6 c. 7.

**Objetivos:** escribir la ecuación fundamental de valoración con un factor de descuento estocástico; demostrar su existencia bajo ausencia de arbitraje; derivarlo de las condiciones de optimalidad de un inversor; interpretar la valoración como proyección en el espacio de pagos; demostrar la cota de Hansen-Jagannathan; demostrar la equivalencia entre un factor de descuento lineal en un factor y una representación beta; describir el rompecabezas de la prima de riesgo de las acciones.

**Secciones:**

- **9.1** Ecuación fundamental de valoración p = 𝔼[m x].
- **9.2** Existencia del factor de descuento estocástico bajo ausencia de arbitraje.
- **9.3** El factor de descuento y la utilidad marginal.
- **9.4** Geometría de la valoración: proyección en el espacio de pagos.
- **9.5** Cota de Hansen-Jagannathan.
- **9.6** Factores de descuento lineales y modelos beta.
- **9.7** El rompecabezas de la prima de riesgo de las acciones (resultado empírico).

**Resultados principales:** existencia del factor de descuento; cota de Hansen-Jagannathan; equivalencia con modelos beta.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** cálculo de la cota de Hansen-Jagannathan con datos.

**Extensión estimada:** 30–36 páginas; 25–35 ejercicios.

### Capítulo 10. APT y modelos de factores

**Prerrequisitos:** L10 c. 7, L10 c. 9, L6 c. 11, L9 c. 8, L9 c. 13.

**Objetivos:** formular modelos de factores para rendimientos; demostrar la APT con estructura factorial exacta; enunciar la versión asintótica; distinguir factores macroeconómicos, estadísticos y característicos; describir los modelos de Fama-French y su evidencia; explicar la proliferación de factores como problema de pruebas múltiples.

**Secciones:**

- **10.1** Modelos de factores para rendimientos.
- **10.2** APT con estructura factorial exacta.
- **10.3** APT asintótica: enunciado e interpretación.
- **10.4** Factores macroeconómicos, estadísticos y característicos.
- **10.5** Modelos de Fama-French (resultados empíricos con fuentes).
- **10.6** Proliferación de factores y pruebas múltiples.

**Resultados principales:** APT exacta.

**Resultados admitidos:** RA-33 (en §10.3).

**Aplicaciones financieras:** todo el capítulo.

**Computación:** estimación de modelos de factores con datos.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 11. Eficiencia de mercado y anomalías

**Prerrequisitos:** L10 c. 7, L10 c. 10, L9 c. 6, L9 c. 7, L8 §9.7, L8 §14.1.

**Objetivos:** formular la hipótesis de eficiencia y el problema de la hipótesis conjunta; distinguir martingala y paseo aleatorio como modelos de precios; describir la evidencia de predictibilidad y las anomalías documentadas; evaluar las explicaciones por riesgo, comportamiento, fricciones y minería de datos; describir el decaimiento de las anomalías tras su publicación.

**Secciones:**

- **11.1** Hipótesis de eficiencia; problema de la hipótesis conjunta.
- **11.2** Martingala y paseo aleatorio: qué implican y qué no.
- **11.3** Evidencia de predictibilidad (resultados empíricos).
- **11.4** Anomalías documentadas: *momentum*, valor y tamaño (resultados empíricos).
- **11.5** Explicaciones: riesgo, comportamiento, fricciones y minería de datos.
- **11.6** Decaimiento de las anomalías tras su publicación (resultado empírico).

**Resultados principales:** distinción formal entre martingala, paseo aleatorio e independencia de incrementos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** replicación sencilla de una anomalía.

**Extensión estimada:** 26–32 páginas; 20–30 ejercicios.

### Capítulo 12. Fricciones y límites al arbitraje

**Prerrequisitos:** L10 c. 3, L10 c. 8.

**Objetivos:** derivar bandas de no arbitraje con costos de transacción; analizar el efecto de las restricciones a la venta en corto; explicar por qué el riesgo de ruido y el horizonte limitan el arbitraje; describir casos documentados de desvíos persistentes; describir la liquidez como factor de riesgo; extraer consecuencias para la investigación cuantitativa.

**Secciones:**

- **12.1** Costos de transacción y bandas de no arbitraje.
- **12.2** Restricciones a la venta en corto.
- **12.3** Riesgo de ruido y horizonte de los arbitrajistas.
- **12.4** Casos documentados de desvíos persistentes (resultados empíricos).
- **12.5** La liquidez como factor de riesgo (resultado empírico).
- **12.6** Consecuencias para la investigación cuantitativa.

**Resultados principales:** bandas de no arbitraje con costos proporcionales.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** no corresponde.

**Extensión estimada:** 22–28 páginas; 20–30 ejercicios.

### Capítulo 13. Estados contables y valoración por flujos descontados

**Prerrequisitos:** L5 c. 4, L5 c. 6, L10 c. 2, L10 c. 7, L4 §12.2.

**Objetivos:** leer la estructura de los estados contables; derivar el flujo de caja libre a partir de la información contable; valorar acciones con el modelo de dividendos y el modelo de Gordon; valorar empresas por flujos de caja libres descontados al costo de capital; relacionar múltiplos y flujos descontados; construir variables contables para la investigación respetando las fechas de publicación.

**Secciones:**

- **13.1** Estados contables: balance, estado de resultados y estado de flujos de efectivo.
- **13.2** Del resultado contable al flujo de caja libre.
- **13.3** Modelo de descuento de dividendos y modelo de Gordon.
- **13.4** Valoración por flujos de caja libres; costo de capital.
- **13.5** Múltiplos y su relación con los flujos descontados.
- **13.6** Variables contables en la investigación: valor contable sobre valor de mercado, rentabilidad, inversión; fechas de publicación y sesgo de anticipación (anticipo de L20 c. 2).

**Resultados principales:** equivalencia entre valoración por dividendos y por flujos de caja libres bajo supuestos explícitos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** modelo de valoración por flujos descontados.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
