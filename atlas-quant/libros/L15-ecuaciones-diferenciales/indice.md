# L15. Ecuaciones diferenciales

Índice detallado · Versión 1.0 · Entrega 1c · 2026-10-16

## Ficha editorial

- **Serie:** IV. Matemática avanzada y tiempo continuo.
- **Requisitos:** L6, L7, L11, L12.
- **Capítulos:** 9, más un apéndice.
- **Extensión estimada:** 268–332 páginas.

**Propósito.** Este libro desarrolla las ecuaciones diferenciales que necesita la valoración en tiempo continuo: existencia y unicidad de soluciones de ecuaciones ordinarias, sistemas lineales y exponencial de matrices, ecuaciones de Riccati, estabilidad, métodos numéricos, ecuación del calor, análisis de Fourier, principio del máximo y diferencias finitas para ecuaciones parabólicas. La ecuación de Black-Scholes aparece como objeto analítico dado, cuya derivación financiera se hace en L19.

**Teoría L².** La completitud de L² (teorema de Riesz-Fischer) requiere la integral de Lebesgue y se admite hasta L16 §4.3 (RA-10). Todos los demás resultados de Fourier del libro, incluida la identidad de Parseval para funciones integrables según Riemann, se demuestran.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro.

## Capítulos

### Capítulo 1. Ecuaciones de primer orden: existencia, unicidad y desigualdad de Gronwall

**Prerrequisitos:** L11 c. 3, L11 c. 7, L4 c. 9, L4 c. 10.

**Objetivos:** resolver ecuaciones separables, lineales de primer orden y exactas; reformular un problema de valor inicial como ecuación integral; demostrar el teorema de Picard-Lindelöf mediante el punto fijo de Banach; demostrar la desigualdad de Gronwall y la dependencia continua de los datos; reconocer la explosión en tiempo finito y la no unicidad sin la condición de Lipschitz.

**Secciones:**

- **1.1** Ecuaciones diferenciales: ejemplos, incluida la acumulación con fuerza de interés variable.
- **1.2** Ecuaciones separables, lineales de primer orden y exactas.
- **1.3** Problema de valor inicial y formulación integral.
- **1.4** Teorema de Picard-Lindelöf.
- **1.5** Desigualdad de Gronwall y dependencia continua de los datos iniciales.
- **1.6** Soluciones maximales y explosión en tiempo finito.
- **1.7** No unicidad sin la condición de Lipschitz: la ecuación y′ = √|y| (anticipo del modelo CIR, L22 c. 3).

**Resultados principales:** teorema de Picard-Lindelöf; desigualdad de Gronwall; dependencia continua.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** acumulación con fuerza de interés variable.

**Computación:** comparación de soluciones exactas y numéricas.

**Extensión estimada:** 30–36 páginas; 35–45 ejercicios.

### Capítulo 2. Sistemas lineales, exponencial de matrices y ecuaciones de Riccati

**Prerrequisitos:** L15 c. 1, L6 c. 9, L6 §12.1, L4 c. 12, L11 c. 7.

**Objetivos:** reducir ecuaciones de orden superior a sistemas; demostrar que el espacio de soluciones de un sistema lineal homogéneo tiene dimensión n; definir la exponencial de matrices por su serie y demostrar sus propiedades; calcularla mediante diagonalización y forma de Jordan; resolver sistemas no homogéneos por variación de parámetros; resolver ecuaciones de Riccati escalares mediante linealización.

**Secciones:**

- **2.1** Sistemas lineales; reducción de ecuaciones de orden superior.
- **2.2** Espacio de soluciones y wronskiano.
- **2.3** Exponencial de matrices: definición, convergencia y propiedades.
- **2.4** Cálculo mediante diagonalización y forma de Jordan.
- **2.5** Sistemas no homogéneos: fórmula de variación de parámetros.
- **2.6** Ecuaciones de Riccati escalares y su linealización (preparación para modelos afines, L19 c. 11 y L22 c. 3).

**Resultados principales:** dimensión del espacio de soluciones; propiedades de la exponencial de matrices, incluida e^(A+B) = e^A e^B para matrices que conmutan; fórmula de variación de parámetros.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** ecuaciones de Riccati de los modelos afines de tasas.

**Computación:** exponencial de matrices con bibliotecas y verificación.

**Extensión estimada:** 30–36 páginas; 30–40 ejercicios.

### Capítulo 3. Estabilidad y comportamiento cualitativo

**Prerrequisitos:** L15 c. 2, L7 c. 5.

**Objetivos:** encontrar puntos de equilibrio; demostrar el criterio de estabilidad de sistemas lineales por valores propios; demostrar la estabilidad asintótica por linealización cuando los valores propios tienen parte real negativa; demostrar el método directo de Lyapunov; trazar diagramas de fase en el plano; analizar modelos deterministas de reversión a la media.

**Secciones:**

- **3.1** Puntos de equilibrio.
- **3.2** Estabilidad de sistemas lineales.
- **3.3** Linealización: estabilidad asintótica por el método indirecto de Lyapunov.
- **3.4** Funciones de Lyapunov: método directo.
- **3.5** Diagramas de fase en el plano.
- **3.6** Modelos deterministas de reversión a la media.

**Resultados principales:** criterio espectral de estabilidad; métodos indirecto y directo de Lyapunov.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** reversión a la media de tasas en ausencia de ruido (anticipo de Vasicek).

**Computación:** diagramas de fase.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

### Capítulo 4. Métodos numéricos para ecuaciones ordinarias

**Prerrequisitos:** L15 c. 1, L12 c. 1, L4 §13.2.

**Objetivos:** demostrar la convergencia de orden uno del método de Euler; aplicar métodos de Runge-Kutta y verificar el orden del método de segundo orden; analizar la estabilidad absoluta y la rigidez; aplicar Euler implícito y métodos de paso adaptativo; verificar empíricamente el orden de convergencia.

**Secciones:**

- **4.1** Método de Euler: error local y global.
- **4.2** Métodos de Runge-Kutta; orden del método de segundo orden.
- **4.3** Estabilidad absoluta y rigidez; Euler implícito.
- **4.4** Métodos de paso adaptativo.
- **4.5** Verificación empírica del orden de convergencia.

**Resultados principales:** convergencia del método de Euler; orden del método de Runge-Kutta de segundo orden; región de estabilidad de Euler explícito e implícito.

**Resultados admitidos:** RA-43 (en §4.2, orden 4 del método clásico).

**Aplicaciones financieras:** integración numérica de ecuaciones de Riccati.

**Computación:** implementación y verificación de órdenes.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

### Capítulo 5. La ecuación del calor y la separación de variables

**Prerrequisitos:** L15 c. 2, L7 c. 5, L4 c. 13, L11 §7.5.

**Objetivos:** clasificar ecuaciones lineales de segundo orden en derivadas parciales; derivar la ecuación del calor como modelo de difusión; resolver problemas de contorno por separación de variables y justificar la convergencia para datos iniciales con coeficientes absolutamente sumables; demostrar la unicidad mediante el método de energía; explicar por qué la ecuación del calor hacia atrás está mal planteada.

**Secciones:**

- **5.1** Clasificación de las ecuaciones lineales de segundo orden.
- **5.2** La ecuación del calor como modelo de difusión; relación informal con el paseo aleatorio.
- **5.3** Problemas de contorno en un intervalo; separación de variables.
- **5.4** Soluciones en serie de senos y su convergencia.
- **5.5** Unicidad mediante el método de energía.
- **5.6** Problemas bien planteados; la ecuación del calor hacia atrás.

**Resultados principales:** existencia por separación de variables bajo hipótesis explícitas; unicidad por energía; inestabilidad del problema hacia atrás.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** por qué la valoración se plantea hacia atrás en el tiempo y con condición terminal.

**Computación:** sumas parciales de la solución en serie.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 6. Series y transformada de Fourier

**Prerrequisitos:** L15 c. 5, L11 c. 7, L11 c. 8, L4 c. 11.

**Objetivos:** calcular coeficientes de Fourier y aplicar la desigualdad de Bessel; demostrar la convergencia puntual para funciones suaves a trozos y la convergencia uniforme bajo regularidad; demostrar el teorema de Fejér y la densidad de los polinomios trigonométricos; demostrar la identidad de Parseval para funciones integrables según Riemann; definir la transformada de Fourier en ℝ, calcular la de la gaussiana y demostrar la fórmula de inversión para funciones suaves de decaimiento rápido; obtener la solución fundamental de la ecuación del calor.

**Secciones:**

- **6.1** Series de Fourier y desigualdad de Bessel.
- **6.2** Convergencia puntual para funciones suaves a trozos: núcleo de Dirichlet.
- **6.3** Convergencia uniforme bajo regularidad.
- **6.4** Sumabilidad de Fejér y densidad de los polinomios trigonométricos.
- **6.5** Identidad de Parseval para funciones integrables según Riemann; la completitud de L² (Riesz-Fischer) como resultado admitido.
- **6.6** Transformada de Fourier en ℝ; transformada de la gaussiana.
- **6.7** Fórmula de inversión y convolución.
- **6.8** Solución fundamental de la ecuación del calor en la recta.

**Resultados principales:** teoremas de convergencia de Dirichlet y Fejér; identidad de Parseval; fórmula de inversión; solución fundamental.

**Resultados admitidos:** RA-10 (en §6.5).

**Aplicaciones financieras:** preparación de los métodos de Fourier de L19 c. 9.

**Computación:** fenómeno de Gibbs y sumas de Fejér.

**Extensión estimada:** 34–40 páginas; 30–40 ejercicios.

### Capítulo 7. Ecuaciones parabólicas: principio del máximo

**Prerrequisitos:** L15 c. 5, L15 c. 6, L7 c. 6.

**Objetivos:** demostrar el principio del máximo débil en dominios acotados; deducir unicidad y estabilidad; explicar la necesidad de condiciones de crecimiento en la recta mediante el ejemplo de Tychonoff; demostrar el principio de comparación para ecuaciones con coeficientes variables y término de orden cero; extraer consecuencias para la monotonía de precios.

**Secciones:**

- **7.1** Principio del máximo débil en dominios acotados.
- **7.2** Unicidad y estabilidad.
- **7.3** La recta: condiciones de crecimiento y el ejemplo de no unicidad de Tychonoff.
- **7.4** Principio de comparación con coeficientes variables.
- **7.5** Consecuencia: monotonía de precios respecto de los pagos (anticipo de L19).

**Resultados principales:** principio del máximo débil; principio de comparación.

**Resultados admitidos:** RA-44 (en §7.3).

**Aplicaciones financieras:** monotonía de precios de derivados.

**Computación:** no corresponde.

**Extensión estimada:** 22–28 páginas; 20–30 ejercicios.

### Capítulo 8. Reducción de la ecuación de Black-Scholes a la ecuación del calor

**Prerrequisitos:** L15 c. 6, L15 c. 7, L7 c. 4.

**Objetivos:** transformar la ecuación de Black-Scholes en la ecuación del calor mediante cambios de variables; resolverla con la solución fundamental y obtener la fórmula para una opción de compra; formular condiciones terminales y de crecimiento que garantizan la unicidad; extender la reducción a dividendos continuos y coeficientes dependientes del tiempo.

**Secciones:**

- **8.1** La ecuación de Black-Scholes como ecuación dada (su derivación financiera está en L19 c. 2).
- **8.2** Cambios de variables: x = ln S y τ = T − t; eliminación de términos.
- **8.3** Solución mediante la solución fundamental; fórmula para la opción de compra.
- **8.4** Condiciones terminales y de crecimiento; unicidad en la clase adecuada.
- **8.5** Extensiones: dividendos continuos y coeficientes dependientes del tiempo.

**Resultados principales:** equivalencia entre la ecuación de Black-Scholes y la ecuación del calor; fórmula cerrada para la opción de compra; unicidad.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** verificación numérica de la fórmula.

**Extensión estimada:** 20–26 páginas; 20–30 ejercicios.

### Capítulo 9. Diferencias finitas para ecuaciones parabólicas

**Prerrequisitos:** L15 c. 4, L15 c. 5, L15 c. 7, L15 c. 8, L12 §3.2.

**Objetivos:** discretizar la ecuación del calor con el esquema explícito y demostrar su consistencia; analizar la estabilidad por von Neumann y por el principio del máximo discreto; aplicar los esquemas implícito y de Crank-Nicolson con sistemas tridiagonales; enunciar el teorema de equivalencia de Lax; tratar condiciones de contorno y truncamiento del dominio; corregir las oscilaciones de Crank-Nicolson con pagos no suaves; verificar la convergencia contra la fórmula cerrada.

**Secciones:**

- **9.1** Esquema explícito y consistencia.
- **9.2** Estabilidad: análisis de von Neumann y principio del máximo discreto.
- **9.3** Esquemas implícito y de Crank-Nicolson.
- **9.4** Teorema de equivalencia de Lax.
- **9.5** Condiciones de contorno y truncamiento del dominio.
- **9.6** Pagos no suaves: oscilaciones de Crank-Nicolson y arranque de Rannacher.
- **9.7** Aplicación a la ecuación de Black-Scholes transformada.

**Resultados principales:** consistencia y estabilidad del esquema explícito bajo la condición λ ≤ 1/2; estabilidad incondicional del esquema implícito.

**Resultados admitidos:** RA-42 (en §9.4).

**Aplicaciones financieras:** valoración numérica de opciones europeas.

**Computación:** implementación de los tres esquemas y estudio de convergencia.

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
