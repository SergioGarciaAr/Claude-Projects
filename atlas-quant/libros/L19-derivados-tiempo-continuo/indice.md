# L19. Valoración de derivados en tiempo continuo

Índice detallado · Versión 1.0 · Entrega 1d · 2026-10-16

## Ficha editorial

- **Serie:** IV. Matemática avanzada y tiempo continuo.
- **Requisitos:** L9, L12, L13, L15, L16, L18.
- **Capítulos:** 13, más un apéndice.
- **Extensión estimada:** 370–458 páginas.

**Propósito.** Este libro desarrolla la valoración de derivados en tiempo continuo: el mercado de Black-Scholes, la equivalencia entre replicación y valoración neutral al riesgo, la fórmula de Black-Scholes-Merton y sus extensiones, el cambio de numerario, las griegas y la cobertura, la volatilidad implícita, las opciones americanas y exóticas, los métodos numéricos, la volatilidad local, los modelos de Heston y de Merton con saltos, la calibración y los mercados incompletos. Las derivaciones se apoyan en L18; las convenciones y la evidencia empírica se presentan como tales.

**Aproximaciones.** Algunos resultados prácticos (error de cobertura con rebalanceo discreto, ajuste de Leland por costos) se presentan como aproximaciones con su derivación heurística y verificación por simulación, no como teoremas.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro (NOTACION §8.3).

## Capítulos

### Capítulo 1. El mercado de Black-Scholes y las estrategias autofinanciadas

**Prerrequisitos:** L18 c. 6, L18 c. 7, L13 c. 5.

**Objetivos:** formular el mercado de Black-Scholes con sus hipótesis; definir estrategias y su valor; derivar la condición de autofinanciamiento en tiempo continuo a partir del caso discreto; explicar por qué se necesitan restricciones de admisibilidad para excluir estrategias de duplicación; trabajar con precios descontados.

**Secciones:**

- **1.1** El modelo: cuenta bancaria y activo con movimiento browniano geométrico; hipótesis.
- **1.2** Estrategias y su valor.
- **1.3** Autofinanciamiento en tiempo continuo.
- **1.4** Arbitraje y estrategias admisibles.
- **1.5** Precios descontados.

**Resultados principales:** caracterización del autofinanciamiento mediante precios descontados.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** no corresponde.

**Extensión estimada:** 22–28 páginas; 20–30 ejercicios.

### Capítulo 2. Replicación y valoración neutral al riesgo

**Prerrequisitos:** L19 c. 1, L18 c. 8, L18 c. 9, L18 c. 10, L15 c. 8.

**Objetivos:** derivar la ecuación de Black-Scholes por replicación; construir la medida neutral al riesgo con el teorema de Girsanov; valorar como esperanza descontada; demostrar la equivalencia de ambos enfoques mediante Feynman-Kac; enunciar los teoremas fundamentales en tiempo continuo; demostrar la completitud del mercado mediante la representación de martingalas.

**Secciones:**

- **2.1** Replicación y ecuación de Black-Scholes.
- **2.2** Medida neutral al riesgo.
- **2.3** Valoración como esperanza descontada.
- **2.4** Equivalencia de los dos enfoques.
- **2.5** Teoremas fundamentales de valoración en tiempo continuo.
- **2.6** Completitud del mercado de Black-Scholes.

**Resultados principales:** ecuación de Black-Scholes; fórmula de valoración neutral al riesgo; completitud.

**Resultados admitidos:** RA-16 (en §2.6), RA-17 (en §2.2), RA-53 (en §2.5).

**Aplicaciones financieras:** todo el capítulo.

**Computación:** comparación entre ecuación y Monte Carlo.

**Extensión estimada:** 30–36 páginas; 25–35 ejercicios.

### Capítulo 3. Fórmula de Black-Scholes-Merton y extensiones

**Prerrequisitos:** L19 c. 2, L8 §5.6, L13 c. 8.

**Objetivos:** derivar la fórmula mediante la esperanza lognormal y comprobar su coincidencia con L15 c. 8 y L13 c. 8; incorporar dividendos continuos y discretos; valorar opciones sobre divisas y sobre futuros; demostrar propiedades de monotonía, convexidad y límites.

**Secciones:**

- **3.1** Derivación mediante la esperanza lognormal.
- **3.2** Coincidencia con la ecuación del calor y con el límite binomial.
- **3.3** Dividendos continuos y discretos.
- **3.4** Opciones sobre divisas: fórmula de Garman-Kohlhagen.
- **3.5** Opciones sobre futuros: fórmula de Black.
- **3.6** Propiedades: monotonía, convexidad y límites.

**Resultados principales:** fórmula de Black-Scholes-Merton y sus extensiones.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** implementación verificada de las fórmulas.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 4. Cambio de numerario

**Prerrequisitos:** L19 c. 2, L16 c. 12, L18 c. 9.

**Objetivos:** demostrar el teorema de cambio de numerario; valorar la opción de intercambio de Margrabe; definir la medida forward y relacionarla con los precios de bonos; derivar la fórmula de Black en la medida forward; rederivar Black-Scholes con el activo como numerario.

**Secciones:**

- **4.1** Numerarios y medidas asociadas; teorema de cambio de numerario.
- **4.2** Opción de intercambio de Margrabe.
- **4.3** Medida forward y precios de bonos.
- **4.4** Fórmula de Black en la medida forward.
- **4.5** Black-Scholes con el activo como numerario.

**Resultados principales:** teorema de cambio de numerario; fórmula de Margrabe.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** opciones de intercambio; preparación de los modelos de tasas (L22 c. 5).

**Computación:** verificación por simulación bajo distintas medidas.

**Extensión estimada:** 24–30 páginas; 20–30 ejercicios.

### Capítulo 5. Griegas y cobertura

**Prerrequisitos:** L19 c. 3, L13 c. 7.

**Objetivos:** derivar las griegas de Black-Scholes; relacionar theta y gamma mediante la ecuación; analizar el error de cobertura delta con rebalanceo discreto como aproximación verificada por simulación; construir coberturas delta-gamma y delta-vega; demostrar la fórmula de pérdidas y ganancias de cubrir con una volatilidad mal especificada; describir el ajuste por costos de transacción.

**Secciones:**

- **5.1** Griegas de Black-Scholes.
- **5.2** Relación entre theta y gamma.
- **5.3** Cobertura delta con rebalanceo discreto: error de cobertura.
- **5.4** Coberturas delta-gamma y delta-vega.
- **5.5** Cobertura con volatilidad mal especificada.
- **5.6** Costos de transacción: ajuste de Leland como aproximación.

**Resultados principales:** fórmulas de las griegas; fórmula de pérdidas y ganancias con volatilidad mal especificada.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** simulación de estrategias de cobertura.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

### Capítulo 6. Volatilidad implícita

**Prerrequisitos:** L19 c. 3, L12 c. 2, L13 c. 3.

**Objetivos:** demostrar la existencia y unicidad de la volatilidad implícita; calcularla de forma robusta; describir la sonrisa y la superficie de volatilidad como resultado empírico; derivar restricciones de no arbitraje sobre la superficie; demostrar la fórmula de Breeden-Litzenberger para la densidad neutral al riesgo; interpolar la superficie verificando las restricciones.

**Secciones:**

- **6.1** Definición, existencia y unicidad.
- **6.2** Cálculo numérico robusto.
- **6.3** Sonrisa y superficie de volatilidad (resultado empírico).
- **6.4** Restricciones de no arbitraje sobre la superficie.
- **6.5** Fórmula de Breeden-Litzenberger.
- **6.6** Interpolación de la superficie y verificación de las restricciones.

**Resultados principales:** existencia y unicidad de la volatilidad implícita; restricciones de no arbitraje; fórmula de Breeden-Litzenberger.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** construcción de una superficie con datos (fuente por verificar en 1e).

**Extensión estimada:** 26–32 páginas; 20–30 ejercicios.

### Capítulo 7. Opciones americanas como problema de frontera libre

**Prerrequisitos:** L19 c. 2, L13 c. 6, L16 c. 10, L9 c. 8.

**Objetivos:** formular la valoración americana como parada óptima en tiempo continuo; describir el problema de frontera libre y la condición de contacto suave; valorar la opción de venta americana perpetua y verificar la solución; aplicar métodos numéricos (árboles, diferencias finitas con proyección y Longstaff-Schwartz); demostrar que la dualidad proporciona cotas superiores.

**Secciones:**

- **7.1** Formulación como parada óptima.
- **7.2** Frontera libre y contacto suave.
- **7.3** Opción de venta americana perpetua.
- **7.4** Métodos numéricos: árboles y diferencias finitas con proyección.
- **7.5** Método de Longstaff-Schwartz.
- **7.6** Cotas superiores por dualidad.

**Resultados principales:** solución de la opción perpetua con argumento de verificación; dualidad débil para cotas superiores.

**Resultados admitidos:** RA-20 (en §7.1 y §7.2), RA-54 (en §7.5).

**Aplicaciones financieras:** todo el capítulo.

**Computación:** comparación de métodos de valoración americana.

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

### Capítulo 8. Opciones exóticas

**Prerrequisitos:** L19 c. 3, L18 c. 4.

**Objetivos:** valorar opciones de barrera mediante el principio de reflexión y demostrar la paridad entre opciones *in* y *out*; valorar opciones *lookback*; demostrar la fórmula cerrada de la opción asiática geométrica y valorar la aritmética por simulación; valorar y analizar la cobertura de opciones digitales; describir opciones compuestas y de elección; identificar el riesgo de modelo en exóticas.

**Secciones:**

- **8.1** Opciones de barrera y paridad *in-out*.
- **8.2** Opciones *lookback*.
- **8.3** Opciones asiáticas geométricas y aritméticas.
- **8.4** Opciones digitales y su cobertura.
- **8.5** Opciones compuestas y de elección.
- **8.6** Riesgo de modelo en opciones exóticas.

**Resultados principales:** fórmulas de barrera, *lookback* y asiática geométrica.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** verificación de fórmulas por simulación.

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

### Capítulo 9. Métodos numéricos de valoración

**Prerrequisitos:** L19 c. 3, L12 c. 9, L12 c. 12, L15 c. 9, L16 c. 8.

**Objetivos:** valorar por Monte Carlo con reducción de varianza; estimar griegas por los métodos de la trayectoria y de la razón de verosimilitud; valorar por diferencias finitas y extraer griegas de la malla; derivar el método de Carr-Madan con sus condiciones de integrabilidad; describir el método COS; verificar cruzadamente los métodos.

**Secciones:**

- **9.1** Monte Carlo con reducción de varianza.
- **9.2** Griegas por Monte Carlo: método de la trayectoria y razón de verosimilitud.
- **9.3** Diferencias finitas para la ecuación de Black-Scholes.
- **9.4** Método de Carr-Madan.
- **9.5** Método COS (presentación).
- **9.6** Comparación y verificación cruzada.

**Resultados principales:** insesgamiento de los estimadores de griegas bajo condiciones explícitas; fórmula de Carr-Madan.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** implementación y comparación de los tres enfoques.

**Extensión estimada:** 30–36 páginas; 20–30 ejercicios.

### Capítulo 10. Volatilidad local

**Prerrequisitos:** L19 c. 6, L18 c. 8.

**Objetivos:** formular el modelo de volatilidad local; derivar la fórmula de Dupire a partir de la ecuación prospectiva bajo hipótesis de regularidad; analizar los problemas de calibración; describir la dinámica de la sonrisa que implica el modelo y su desajuste con la observada; implementar el modelo.

**Secciones:**

- **10.1** El modelo de volatilidad local.
- **10.2** Fórmula de Dupire.
- **10.3** Calibración y mal planteamiento.
- **10.4** Dinámica de la sonrisa.
- **10.5** Implementación.

**Resultados principales:** fórmula de Dupire bajo hipótesis explícitas.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** calibración de una superficie de volatilidad local.

**Extensión estimada:** 22–28 páginas; 15–25 ejercicios.

### Capítulo 11. Modelos de Heston y de Merton con saltos

**Prerrequisitos:** L19 c. 9, L18 c. 2, L18 c. 7, L15 §2.6.

**Objetivos:** formular el modelo de Heston y enunciar sus condiciones de existencia y de positividad; derivar su función característica mediante ecuaciones de Riccati con un argumento de verificación; valorar por métodos de Fourier; formular el modelo de Merton con saltos, discutir la elección de la medida en un mercado incompleto y demostrar su fórmula en serie; comparar las sonrisas que generan; situar otros modelos.

**Secciones:**

- **11.1** Modelo de Heston: dinámica, existencia y condición de Feller.
- **11.2** Función característica afín y ecuaciones de Riccati.
- **11.3** Valoración por métodos de Fourier.
- **11.4** Modelo de Merton con saltos: medida neutral al riesgo y fórmula en serie.
- **11.5** Sonrisas generadas por cada modelo.
- **11.6** Otros modelos: SABR y la frontera de la investigación (presentación).

**Resultados principales:** función característica de Heston (con verificación); fórmula de Merton en serie.

**Resultados admitidos:** RA-18 (en §11.1), RA-55 (en §11.1).

**Aplicaciones financieras:** todo el capítulo.

**Computación:** valoración por Fourier y verificación por simulación.

**Extensión estimada:** 30–36 páginas; 20–30 ejercicios.

### Capítulo 12. Calibración y riesgo de modelo

**Prerrequisitos:** L19 c. 11, L12 c. 8, L9 c. 4.

**Objetivos:** plantear la calibración como problema inverso con funciones objetivo explícitas; evaluar la estabilidad temporal de los parámetros y su identificabilidad; cuantificar el riesgo de modelo comparando precios de exóticas bajo modelos calibrados a los mismos datos; describir cotas independientes del modelo y reservas.

**Secciones:**

- **12.1** La calibración como problema inverso.
- **12.2** Estabilidad temporal de los parámetros.
- **12.3** Identificabilidad.
- **12.4** Riesgo de modelo en opciones exóticas.
- **12.5** Cotas independientes del modelo y reservas.

**Resultados principales:** no corresponde; capítulo de métodos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** calibración de varios modelos a los mismos datos.

**Extensión estimada:** 22–28 páginas; 15–25 ejercicios.

### Capítulo 13. Mercados incompletos

**Prerrequisitos:** L19 c. 11, L16 c. 12, L13 §7.5.

**Objetivos:** identificar las fuentes de incompletitud; describir el conjunto de medidas martingala equivalentes y el intervalo de precios sin arbitraje; enunciar la dualidad de la súper replicación; formular la cobertura de mínima varianza cuadrática; introducir la valoración por indiferencia con utilidad exponencial; discutir la elección de medida mediante calibración.

**Secciones:**

- **13.1** Fuentes de incompletitud.
- **13.2** Medidas martingala equivalentes e intervalo de precios.
- **13.3** Súper replicación y su dualidad.
- **13.4** Cobertura de mínima varianza cuadrática.
- **13.5** Valoración por indiferencia con utilidad exponencial.
- **13.6** Elección de la medida en la práctica.

**Resultados principales:** caracterización del intervalo de precios sin arbitraje en modelos con espacio finito (con L16 c. 12); precio de indiferencia exponencial en un modelo de un período.

**Resultados admitidos:** RA-56 (en §13.3).

**Aplicaciones financieras:** todo el capítulo.

**Computación:** cálculo de intervalos de precios en un modelo trinomial de varios períodos.

**Extensión estimada:** 24–30 páginas; 15–25 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
