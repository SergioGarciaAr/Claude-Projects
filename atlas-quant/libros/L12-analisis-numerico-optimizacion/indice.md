# L12. Análisis numérico, optimización y simulación

Índice detallado · Versión 1.0 · Entrega 1c · 2026-10-16

## Ficha editorial

- **Serie:** III. Teoría financiera y modelización.
- **Requisitos:** L3, L4, L6, L7, L8.
- **Uso como aplicación:** L5, L10.
- **Capítulos:** 12, más un apéndice.
- **Extensión estimada:** 350–432 páginas.

**Propósito.** Este libro estudia los métodos numéricos que sostienen la práctica cuantitativa: ecuaciones no lineales, sistemas lineales, interpolación, cuadratura, optimización sin restricciones y convexa, calibración, Monte Carlo con reducción de varianza, cuasi-Monte Carlo, programación dinámica y transformada rápida de Fourier. Cada método se presenta con su derivación, su análisis de convergencia o de error, sus condiciones de falla y una implementación verificada. Los métodos numéricos para ecuaciones diferenciales se estudian en L15.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; versiones de las bibliotecas usadas.

## Capítulos

### Capítulo 1. Condicionamiento y estabilidad

**Prerrequisitos:** L3 c. 2, L4 c. 14, L6 c. 12.

**Objetivos:** clasificar las fuentes de error de un cálculo; calcular números de condición de problemas escalares y vectoriales; distinguir estabilidad hacia adelante y hacia atrás; elegir algoritmos estables para la varianza muestral y las sumas largas; usar funciones especiales precisas; informar resultados numéricos con su precisión.

**Secciones:**

- **1.1** Fuentes de error: modelo, datos, truncamiento y redondeo.
- **1.2** Número de condición de un problema.
- **1.3** Estabilidad de algoritmos hacia adelante y hacia atrás.
- **1.4** Ejemplos: varianza muestral en una o dos pasadas; suma compensada de Kahan.
- **1.5** Evaluación precisa de funciones: log1p y expm1.
- **1.6** Cómo informar resultados numéricos.

**Resultados principales:** cota del error de la suma compensada; análisis de los algoritmos de varianza.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** cálculo preciso de rendimientos pequeños y de varianzas de carteras.

**Computación:** todo el capítulo.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 2. Ecuaciones no lineales

**Prerrequisitos:** L12 c. 1, L4 §3.4, L4 §7.5, L7 c. 3.

**Objetivos:** aplicar bisección, regula falsi, iteración de punto fijo, Newton y secante; demostrar la convergencia lineal de la iteración de punto fijo y la cuadrática local de Newton; globalizar Newton mediante amortiguamiento; resolver sistemas no lineales con Newton multivariante; diseñar criterios de parada y diagnosticar fallas.

**Secciones:**

- **2.1** Bisección y regula falsi.
- **2.2** Iteración de punto fijo y convergencia lineal.
- **2.3** Método de Newton: convergencia local y globalización.
- **2.4** Método de la secante y método de Brent.
- **2.5** Sistemas no lineales: Newton multivariante.
- **2.6** Aplicaciones: tasa interna de retorno y rendimiento de bonos con flujos irregulares.
- **2.7** Criterios de parada y diagnóstico.

**Resultados principales:** convergencia de la iteración de punto fijo; convergencia cuadrática local de Newton en varias variables.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** TIR; rendimiento al vencimiento.

**Usa como aplicación:** L5 §6.4, L5 §8.3.

**Computación:** implementación y comparación de métodos.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 3. Sistemas lineales numéricos

**Prerrequisitos:** L12 c. 1, L6 c. 12.

**Objetivos:** aplicar LU con pivoteo y Cholesky estimando su costo; resolver sistemas tridiagonales y demostrar la estabilidad del algoritmo de Thomas para matrices diagonalmente dominantes; demostrar la convergencia de Jacobi y Gauss-Seidel en ese caso; derivar el gradiente conjugado y demostrar su terminación finita y su cota de convergencia; elegir un método según la estructura del problema.

**Secciones:**

- **3.1** LU con pivoteo y Cholesky: costo y uso.
- **3.2** Matrices en banda y tridiagonales; algoritmo de Thomas.
- **3.3** Métodos iterativos de Jacobi y Gauss-Seidel.
- **3.4** Gradiente conjugado y terminación finita.
- **3.5\*** Cota de convergencia del gradiente conjugado mediante polinomios de Chebyshev.
- **3.6** Precondicionamiento.
- **3.7** Elección del método.

**Resultados principales:** estabilidad del algoritmo de Thomas; convergencia de Jacobi y Gauss-Seidel para matrices diagonalmente dominantes; propiedades del gradiente conjugado.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** sistemas tridiagonales de *splines* y de diferencias finitas (L15 c. 9).

**Computación:** implementación del algoritmo de Thomas y del gradiente conjugado.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

### Capítulo 4. Interpolación y *splines*

**Prerrequisitos:** L12 c. 3, L4 §13.2, L1 c. 10.

**Objetivos:** demostrar la existencia y unicidad del polinomio interpolador y construirlo en las formas de Lagrange y Newton; demostrar la fórmula del error de interpolación y explicar el fenómeno de Runge; usar nodos de Chebyshev; demostrar la existencia, unicidad y propiedad de mínima curvatura de los *splines* cúbicos; describir *splines* que preservan la monotonía; evaluar el efecto de la interpolación sobre las tasas a plazo.

**Secciones:**

- **4.1** Interpolación polinómica: formas de Lagrange y de Newton.
- **4.2** Error de interpolación; fenómeno de Runge.
- **4.3** Nodos de Chebyshev.
- **4.4** *Splines* cúbicos: existencia, unicidad y mínima curvatura.
- **4.5** Interpolación que preserva la monotonía.
- **4.6** Interpolación de curvas de tasas y su efecto sobre las tasas a plazo.

**Resultados principales:** fórmula del error de interpolación; propiedad de mínima curvatura de los *splines* cúbicos naturales.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** construcción de curvas de tasas.

**Usa como aplicación:** L5 §10.4.

**Computación:** comparación de métodos de interpolación sobre curvas de tasas.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 5. Derivación e integración numéricas

**Prerrequisitos:** L12 c. 4, L4 c. 14.

**Objetivos:** derivar fórmulas de diferenciación a partir de la interpolación; aplicar cuadraturas de Newton-Cotes compuestas; construir cuadraturas de Gauss y demostrar su exactitud; aplicar cuadratura adaptativa; tratar integrales impropias y singularidades; explicar por qué la cuadratura determinista se vuelve impracticable en dimensión alta.

**Secciones:**

- **5.1** Diferenciación numérica mediante interpolación.
- **5.2** Cuadraturas de Newton-Cotes compuestas.
- **5.3** Polinomios ortogonales y cuadratura de Gauss.
- **5.4** Cuadratura adaptativa.
- **5.5** Integrales impropias y singularidades.
- **5.6** Integración en varias dimensiones: el costo crece exponencialmente con la dimensión.

**Resultados principales:** exactitud de grado 2n − 1 de la cuadratura de Gauss; cotas del error de las fórmulas compuestas.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** valor esperado de pagos bajo densidades conocidas.

**Computación:** comparación de cuadraturas.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

### Capítulo 6. Optimización sin restricciones

**Prerrequisitos:** L12 c. 2, L7 c. 6, L7 c. 7.

**Objetivos:** demostrar las tasas de convergencia del descenso del gradiente para funciones convexas suaves y fuertemente convexas; aplicar búsquedas lineales con condiciones de Armijo y Wolfe; aplicar el método de Newton y los métodos cuasi-Newton; abordar problemas no convexos; comparar la diferenciación automática con las diferencias finitas.

**Secciones:**

- **6.1** Descenso del gradiente: convergencia para funciones convexas suaves y fuertemente convexas.
- **6.2** Búsqueda lineal: condiciones de Armijo y de Wolfe.
- **6.3** Método de Newton para optimización.
- **6.4** Métodos cuasi-Newton: BFGS.
- **6.5** Problemas no convexos: mínimos locales e inicios múltiples.
- **6.6** Diferenciación automática y diferencias finitas.

**Resultados principales:** tasas de convergencia del descenso del gradiente; existencia de pasos que satisfacen las condiciones de Wolfe.

**Resultados admitidos:** RA-34 (en §6.4).

**Aplicaciones financieras:** maximización de verosimilitudes de modelos financieros.

**Computación:** implementación y comparación de métodos.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

### Capítulo 7. Optimización convexa

**Prerrequisitos:** L12 c. 6, L7 c. 9.

**Objetivos:** formular problemas convexos en forma estándar; demostrar que el óptimo de un programa lineal se alcanza en un vértice y que el método símplex con la regla de Bland termina; resolver programas cuadráticos mediante conjuntos activos; usar la dualidad para certificar optimalidad; describir los métodos de punto interior; aplicar subgradientes y métodos proximales al lasso; optimizar carteras con restricciones.

**Secciones:**

- **7.1** Problemas convexos y formas estándar.
- **7.2** Programación lineal: geometría, soluciones básicas y método símplex.
- **7.3** Programación cuadrática; métodos de conjunto activo.
- **7.4** Dualidad y certificados de optimalidad.
- **7.5** Métodos de punto interior: idea de la barrera logarítmica.
- **7.6** Subgradientes y métodos proximales; el lasso por descenso coordenado y por gradiente proximal.
- **7.7** Optimización de carteras con restricciones.

**Resultados principales:** optimalidad en vértices; terminación del símplex con la regla de Bland; convergencia del gradiente proximal.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** carteras con restricciones de peso, sector y rotación.

**Usa como aplicación:** L10 c. 6.

**Computación:** resolución de programas lineales y cuadráticos.

**Extensión estimada:** 32–38 páginas; 30–40 ejercicios.

### Capítulo 8. Calibración por mínimos cuadrados no lineales

**Prerrequisitos:** L12 c. 6, L6 c. 8, L6 c. 11.

**Objetivos:** formular un problema de calibración; derivar el método de Gauss-Newton y su convergencia local en problemas de residuo nulo; aplicar Levenberg-Marquardt; diagnosticar falta de identificabilidad y mal condicionamiento mediante valores singulares; regularizar con Tikhonov; calibrar la curva de Nelson-Siegel.

**Secciones:**

- **8.1** El problema de calibración.
- **8.2** Método de Gauss-Newton.
- **8.3** Método de Levenberg-Marquardt.
- **8.4** Identificabilidad y mal condicionamiento.
- **8.5** Regularización de Tikhonov.
- **8.6** Calibración de la curva de Nelson-Siegel.

**Resultados principales:** convergencia local de Gauss-Newton en problemas de residuo nulo.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** ajuste de curvas de tasas.

**Usa como aplicación:** L5 §10.7.

**Computación:** calibración con datos de tasas.

**Extensión estimada:** 24–30 páginas; 20–30 ejercicios.

### Capítulo 9. Monte Carlo y reducción de varianza

**Prerrequisitos:** L12 c. 5, L8 c. 11, L8 c. 13, L8 §9.4.

**Objetivos:** analizar el error y el costo de un estimador Monte Carlo; demostrar la reducción de varianza de las variables antitéticas para funciones monótonas, de las variables de control con coeficiente óptimo, del muestreo por importancia con densidad óptima y de la estratificación con asignación proporcional; aplicar el condicionamiento; estimar sensibilidades con números aleatorios comunes.

**Secciones:**

- **9.1** Error, costo y eficiencia de Monte Carlo.
- **9.2** Variables antitéticas.
- **9.3** Variables de control.
- **9.4** Muestreo por importancia.
- **9.5** Estratificación.
- **9.6** Muestreo condicional.
- **9.7** Sensibilidades por diferencias finitas con números aleatorios comunes.
- **9.8** Valor esperado de pagos dependientes de la trayectoria.

**Resultados principales:** reducciones de varianza demostradas para cada técnica.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** valor esperado de pagos de opciones asiáticas y de barrera bajo un modelo dado.

**Computación:** todo el capítulo.

**Extensión estimada:** 32–38 páginas; 25–35 ejercicios.

### Capítulo 10. Cuasi-Monte Carlo

**Prerrequisitos:** L12 c. 9, L12 c. 5.

**Objetivos:** definir la discrepancia; enunciar la desigualdad de Koksma-Hlawka; construir sucesiones de Halton y de Sobol; estimar el error mediante cuasi-Monte Carlo aleatorizado; explicar el papel de la dimensión efectiva.

**Secciones:**

- **10.1** Discrepancia.
- **10.2** Desigualdad de Koksma-Hlawka.
- **10.3** Sucesiones de Halton y de Sobol.
- **10.4** Cuasi-Monte Carlo aleatorizado y estimación del error.
- **10.5** Dimensión efectiva: cuándo conviene.

**Resultados principales:** cota de discrepancia de la sucesión de Van der Corput.

**Resultados admitidos:** RA-35 (en §10.2).

**Aplicaciones financieras:** valoración por simulación en dimensión moderada.

**Computación:** comparación empírica entre Monte Carlo y cuasi-Monte Carlo.

**Extensión estimada:** 20–26 páginas; 15–25 ejercicios.

### Capítulo 11. Programación dinámica y parada óptima en tiempo discreto

**Prerrequisitos:** L8 c. 9, L8 c. 14, L7 c. 6, L7 §8.1.

**Objetivos:** demostrar el principio de optimalidad de Bellman; resolver problemas de horizonte finito por inducción hacia atrás; demostrar la optimalidad de la programación dinámica en problemas estocásticos con estados finitos; demostrar que el operador de Bellman con descuento es una contracción y aplicar iteración de valores y de políticas; resolver problemas de parada óptima mediante la envolvente de Snell.

**Secciones:**

- **11.1** Decisiones secuenciales deterministas; principio de optimalidad.
- **11.2** Horizonte finito: inducción hacia atrás.
- **11.3** Problemas estocásticos con estados finitos.
- **11.4** Horizonte infinito con descuento: el operador de Bellman como contracción; iteración de valores y de políticas.
- **11.5** Parada óptima en horizonte finito: envolvente de Snell.
- **11.6** Aplicaciones: problema de la secretaria, consumo y ahorro, ejercicio anticipado (anticipo de L13 c. 6).

**Resultados principales:** principio de optimalidad; contracción del operador de Bellman; optimalidad de la envolvente de Snell.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** decisiones de consumo e inversión; ejercicio anticipado.

**Computación:** implementación de iteración de valores y de envolventes de Snell.

**Extensión estimada:** 30–36 páginas; 25–35 ejercicios.

### Capítulo 12. Transformada discreta de Fourier y FFT

**Prerrequisitos:** L2 c. 12, L4 §13.8, L6 c. 7, L3 c. 5.

**Objetivos:** interpretar la transformada discreta de Fourier como cambio de base unitario en ℂⁿ; demostrar el teorema de convolución circular y la identidad de Parseval; derivar el algoritmo de Cooley-Tukey y demostrar su costo n log n; explicar el *aliasing*; aplicar la FFT a convoluciones y productos de polinomios.

**Secciones:**

- **12.1** La transformada discreta de Fourier como cambio de base unitario en ℂⁿ.
- **12.2** Convolución circular e identidad de Parseval.
- **12.3** Algoritmo de Cooley-Tukey y su costo.
- **12.4** Muestreo y *aliasing*.
- **12.5** Aplicaciones: convolución rápida, productos de polinomios y preparación para los métodos de Fourier de L19.

**Resultados principales:** unitariedad de la transformada; teorema de convolución; costo de la FFT.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** convolución de distribuciones de pérdidas.

**Computación:** implementación de la FFT y comparación con bibliotecas.

**Extensión estimada:** 22–28 páginas; 20–30 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice analítico.
