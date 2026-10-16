# L8. Probabilidad

Índice detallado · Versión 1.0 · Entrega 1b · 2026-10-16

## Ficha editorial

- **Serie:** II. Matemática para las finanzas.
- **Requisitos:** L3, L4, L6, L7.
- **Capítulos:** 14, más un apéndice.
- **Extensión estimada:** 424–518 páginas.

**Propósito.** Este libro desarrolla la teoría de la probabilidad sin teoría de la medida, con el rigor que permiten el cálculo y el álgebra lineal: espacios de probabilidad, variables y vectores aleatorios, esperanza, distribuciones fundamentales, esperanza condicional elemental, leyes de los grandes números, teorema central del límite para arreglos triangulares, colas pesadas, simulación y cadenas de Markov finitas. Señala con precisión qué resultados requieren la teoría de la medida y dónde se demuestran (L16). Las aplicaciones financieras incluyen la varianza de una cartera, la diversificación, la actualización bayesiana, las matrices de transición de calificaciones y el valor esperado de pagos de opciones.

**Fundamentos sin teoría de la medida.** La existencia de espacios de probabilidad que soportan variables con densidad dada y sucesiones de variables independientes se admite (RA-24) y se demuestra en L16. Las demostraciones del libro solo usan las propiedades enunciadas de esos espacios.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro (NOTACION §6).

## Capítulos

### Capítulo 1. Espacios de probabilidad

**Prerrequisitos:** L1 c. 3, L4 c. 12.

**Objetivos:** modelar experimentos aleatorios con espacios muestrales y eventos; deducir consecuencias de los axiomas de Kolmogorov; trabajar con espacios equiprobables; demostrar la continuidad de la probabilidad; distinguir interpretaciones de la probabilidad y explicitar supuestos de modelización.

**Secciones:**

- **1.1** Experimentos aleatorios, espacio muestral y eventos.
- **1.2** Axiomas de Kolmogorov. Tratamiento completo en espacios discretos; en espacios continuos, la familia de eventos se describe y su existencia se admite.
- **1.3** Consecuencias de los axiomas.
- **1.4** Espacios equiprobables.
- **1.5** Continuidad de la probabilidad.
- **1.6** Interpretaciones de la probabilidad y supuestos de modelización.
- **1.7** Escenarios y estados del mundo en finanzas.

**Resultados principales:** propiedades derivadas de los axiomas; continuidad de la probabilidad.

**Resultados admitidos:** RA-24 (en §1.2).

**Aplicaciones financieras:** escenarios de mercado.

**Computación:** no corresponde.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 2. Combinatoria

**Prerrequisitos:** L8 c. 1, L1 §10.7.

**Objetivos:** contar mediante el principio multiplicativo, permutaciones, variaciones y combinaciones; demostrar identidades combinatorias por doble conteo; aplicar el principio de inclusión y exclusión; contar trayectorias en un árbol binomial.

**Secciones:**

- **2.1** Principio multiplicativo.
- **2.2** Permutaciones y variaciones.
- **2.3** Combinaciones; identidades demostradas por doble conteo.
- **2.4** Coeficientes multinomiales.
- **2.5** Conteo con restricciones; principio de inclusión y exclusión.
- **2.6** Trayectorias en un árbol binomial (anticipo de L13).

**Resultados principales:** principio de inclusión y exclusión.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** número de trayectorias de precios en un árbol.

**Computación:** verificación de conteos por enumeración.

**Extensión estimada:** 24–30 páginas; 40–50 ejercicios.

### Capítulo 3. Probabilidad condicional, independencia y teorema de Bayes

**Prerrequisitos:** L8 c. 1, L8 c. 2.

**Objetivos:** calcular probabilidades condicionales; aplicar la regla del producto y la ley de probabilidad total; demostrar y aplicar el teorema de Bayes; distinguir independencia de a pares y mutua; identificar errores frecuentes de razonamiento probabilístico.

**Secciones:**

- **3.1** Probabilidad condicional y regla del producto.
- **3.2** Ley de probabilidad total.
- **3.3** Teorema de Bayes.
- **3.4** Independencia de eventos: a pares y mutua.
- **3.5** Errores frecuentes: falacia del fiscal y olvido de la tasa base.
- **3.6** Aplicaciones: pruebas diagnósticas, evaluación de un gestor, probabilidad de incumplimiento.

**Resultados principales:** ley de probabilidad total; teorema de Bayes.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** actualización de creencias sobre la habilidad de un gestor; incumplimiento.

**Computación:** simulación de pruebas diagnósticas.

**Extensión estimada:** 28–34 páginas; 40–50 ejercicios.

### Capítulo 4. Variables aleatorias discretas

**Prerrequisitos:** L8 c. 3, L4 c. 12, L4 §10.6.

**Objetivos:** definir variables aleatorias discretas, su función de masa y su función de distribución; calcular esperanzas con atención a la convergencia absoluta; trabajar con las distribuciones de Bernoulli, binomial, geométrica, binomial negativa, de Poisson e hipergeométrica; demostrar la aproximación de la binomial por la Poisson.

**Secciones:**

- **4.1** Variables aleatorias y función de masa.
- **4.2** Función de distribución.
- **4.3** Esperanza de una variable discreta; condición de convergencia absoluta.
- **4.4** Distribuciones de Bernoulli y binomial.
- **4.5** Distribuciones geométrica y binomial negativa; falta de memoria.
- **4.6** Distribución de Poisson; límite de la binomial.
- **4.7** Distribución hipergeométrica.

**Resultados principales:** falta de memoria de la geométrica; convergencia de la binomial a la Poisson.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** número de incumplimientos en una cartera de créditos independientes.

**Computación:** funciones de masa y simulación.

**Extensión estimada:** 28–34 páginas; 40–55 ejercicios.

### Capítulo 5. Variables aleatorias continuas

**Prerrequisitos:** L8 c. 4, L4 c. 9, L4 §11.4, L7 §10.6.

**Objetivos:** trabajar con densidades y funciones de distribución; estudiar las distribuciones uniforme, exponencial, Gamma, normal y lognormal; demostrar la normalización de la densidad normal; estandarizar; definir cuantiles mediante la inversa generalizada.

**Secciones:**

- **5.1** Densidades y funciones de distribución.
- **5.2** Distribución uniforme.
- **5.3** Distribución exponencial; falta de memoria.
- **5.4** Distribución Gamma.
- **5.5** Distribución normal: normalización mediante la integral gaussiana; estandarización.
- **5.6** Distribución lognormal y su uso para precios.
- **5.7** Cuantiles y función cuantil.

**Resultados principales:** caracterización de la exponencial por la falta de memoria; normalización de la densidad normal.

**Resultados admitidos:** RA-24.

**Aplicaciones financieras:** modelo lognormal de precios como hipótesis de modelización.

**Computación:** densidades y cuantiles con Python.

**Extensión estimada:** 30–36 páginas; 40–50 ejercicios.

### Capítulo 6. Esperanza, momentos y desigualdades

**Prerrequisitos:** L8 c. 4, L8 c. 5, L4 §6.4.

**Objetivos:** calcular esperanzas de variables continuas y de funciones de variables aleatorias; calcular varianza, momentos, asimetría y curtosis; demostrar las desigualdades de Markov, Chebyshev y Jensen; interpretar media y varianza de rendimientos.

**Secciones:**

- **6.1** Esperanza de variables continuas; existencia.
- **6.2** Esperanza de funciones de una variable aleatoria. Demostración para el caso discreto y para funciones monótonas por tramos en el caso continuo.
- **6.3** Varianza, desviación estándar y momentos; asimetría y curtosis.
- **6.4** Desigualdades de Markov y Chebyshev.
- **6.5** Desigualdad de Jensen.
- **6.6** Media y varianza de rendimientos: interpretación y limitaciones.

**Resultados principales:** desigualdades de Markov, Chebyshev y Jensen.

**Resultados admitidos:** RA-26 (en §6.2, caso general).

**Aplicaciones financieras:** aversión al riesgo y desigualdad de Jensen (anticipo de L10 c. 5).

**Computación:** momentos muestrales frente a momentos teóricos.

**Extensión estimada:** 30–36 páginas; 40–50 ejercicios.

### Capítulo 7. Vectores aleatorios

**Prerrequisitos:** L8 c. 6, L7 c. 10, L6 c. 10, L6 §12.4.

**Objetivos:** trabajar con distribuciones conjuntas, marginales e independencia; demostrar que la esperanza del producto de variables independientes es el producto de las esperanzas; calcular covarianzas y correlaciones; demostrar que la matriz de covarianzas es semidefinida positiva y que Var(**w**ᵀ**X**) = **w**ᵀ**Σ****w**; definir la normal multivariante y demostrar sus propiedades; construir ejemplos de variables incorrelacionadas y dependientes.

**Secciones:**

- **7.1** Distribuciones conjuntas discretas y continuas; marginales.
- **7.2** Independencia de variables aleatorias.
- **7.3** Esperanza de funciones de varias variables; esperanza del producto bajo independencia.
- **7.4** Covarianza y correlación; |ρ| ≤ 1.
- **7.5** Vector de medias y matriz de covarianzas; varianza de combinaciones lineales y de carteras.
- **7.6** Normal multivariante: definición mediante transformaciones lineales de normales independientes; densidad; marginales y combinaciones lineales; incorrelación e independencia en la normal conjunta.
- **7.7** Incorrelación no implica independencia: ejemplos.

**Resultados principales:** semidefinición positiva de la covarianza; varianza de una cartera; propiedades de la normal multivariante.

**Resultados admitidos:** ninguno. La densidad de la normal multivariante usa solo el cambio de variables lineal de L7 §10.5.

**Aplicaciones financieras:** varianza de una cartera; diversificación.

**Computación:** simulación de normales multivariantes mediante Cholesky.

**Extensión estimada:** 32–38 páginas; 40–55 ejercicios.

### Capítulo 8. Transformaciones, funciones generadoras y funciones características

**Prerrequisitos:** L8 c. 7, L7 c. 10, L4 §13.8.

**Objetivos:** obtener la distribución de transformaciones de una o varias variables; calcular la distribución de sumas de variables independientes por convolución; usar funciones generadoras de momentos y funciones características; identificar distribuciones mediante la propiedad de unicidad; obtener las distribuciones chi-cuadrado y t como transformaciones de normales.

**Secciones:**

- **8.1** Transformaciones de una variable: métodos de la distribución y de la densidad.
- **8.2** Transformaciones de vectores aleatorios; jacobiano.
- **8.3** Suma de variables independientes: convolución.
- **8.4** Función generadora de momentos.
- **8.5** Función característica: definición mediante partes real e imaginaria; propiedades.
- **8.6** Unicidad e identificación de distribuciones: sumas de normales y de variables de Poisson independientes.
- **8.7** Distribuciones chi-cuadrado y t como transformaciones de normales (preparación para L9).

**Resultados principales:** fórmula de la densidad de una transformación; fórmula de convolución; propiedades de las funciones generadoras y características.

**Resultados admitidos:** RA-08 (en §8.2), RA-09 (en §8.6).

**Aplicaciones financieras:** suma de rendimientos logarítmicos independientes.

**Computación:** verificación de convoluciones por simulación.

**Extensión estimada:** 30–36 páginas; 35–45 ejercicios.

### Capítulo 9. Esperanza condicional elemental

**Prerrequisitos:** L8 c. 7, L8 c. 3.

**Objetivos:** calcular distribuciones condicionales en los casos discreto y con densidades; definir la esperanza condicional como variable aleatoria; demostrar la ley de la esperanza total, la extracción de lo conocido y la ley de la varianza total; demostrar que la esperanza condicional es el mejor predictor cuadrático; derivar la distribución condicional de la normal multivariante.

**Secciones:**

- **9.1** Distribuciones condicionales discretas y con densidades.
- **9.2** E[X | Y = y] y E[X | Y] como variable aleatoria.
- **9.3** Propiedades: ley de la esperanza total y extracción de lo conocido.
- **9.4** Ley de la varianza total.
- **9.5** La esperanza condicional como mejor predictor cuadrático.
- **9.6** Distribución condicional de la normal multivariante.
- **9.7** Juegos equitativos secuenciales: primera idea de martingala.

**Resultados principales:** ley de la esperanza total; ley de la varianza total; optimalidad cuadrática; condicional de la normal multivariante.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** pronóstico óptimo; actualización de expectativas (anticipo de Black-Litterman y Kalman).

**Computación:** no corresponde.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 10. Modos de convergencia, leyes débiles y concentración

**Prerrequisitos:** L8 c. 6, L8 c. 7, L8 §8.4, L4 c. 1.

**Objetivos:** distinguir convergencia en probabilidad, en media cuadrática y en distribución, y demostrar las implicaciones elementales entre ellas; demostrar la ley débil de los grandes números; demostrar la desigualdad de Hoeffding; demostrar el lema de Slutsky; analizar la diversificación y sus límites.

**Secciones:**

- **10.1** Sucesiones de variables aleatorias independientes.
- **10.2** Convergencia en probabilidad, en media cuadrática y en distribución; implicaciones.
- **10.3** Ley débil de los grandes números.
- **10.4** Desigualdad de Hoeffding y concentración de promedios.
- **10.5** La interpretación frecuentista a la luz de la ley de los grandes números.
- **10.6** Lema de Slutsky.
- **10.7** Diversificación con activos independientes y sus límites cuando hay correlación.

**Resultados principales:** ley débil de los grandes números; desigualdad de Hoeffding; lema de Slutsky.

**Resultados admitidos:** RA-24 (en §10.1).

**Aplicaciones financieras:** diversificación; error de estimación de una media.

**Computación:** ilustración de la concentración por simulación.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 11. Teorema central del límite

**Prerrequisitos:** L8 c. 10, L8 §5.5, L4 §13.2.

**Objetivos:** enunciar e interpretar el teorema central del límite; demostrar que la convergencia de esperanzas de funciones suaves implica convergencia en distribución; demostrar el teorema central del límite para arreglos triangulares con condición de tercer momento mediante el método de Lindeberg; deducir los casos clásicos; discutir la calidad de la aproximación normal y sus fallas.

**Secciones:**

- **11.1** Enunciado, significado y antecedentes históricos.
- **11.2** Convergencia en distribución mediante funciones de prueba suaves.
- **11.3** Método de reemplazo de Lindeberg: demostración para arreglos triangulares con condición de tercer momento.
- **11.4** Corolarios: teorema central del límite para variables idénticamente distribuidas con tercer momento finito; teorema de De Moivre-Laplace.
- **11.5** Velocidad de convergencia: cota de Berry-Esseen.
- **11.6** La aproximación normal en la práctica y sus fallas con colas pesadas.
- **11.7** Ilustración por simulación.

**Resultados principales:** criterio de convergencia en distribución por funciones suaves; teorema central del límite para arreglos triangulares (versión de tercer momento).

**Resultados admitidos:** RA-27 (en §11.5).

**Aplicaciones financieras:** aproximación normal de la suma de rendimientos y sus límites; error de Monte Carlo (anticipo de L8 c. 13).

**Computación:** simulación de sumas normalizadas.

**Extensión estimada:** 30–36 páginas; 30–40 ejercicios.

### Capítulo 12. Colas pesadas y dependencia más allá de la correlación

**Prerrequisitos:** L8 c. 8, L8 c. 11, L8 c. 7.

**Objetivos:** describir los hechos empíricos sobre las colas de los rendimientos, distinguiéndolos de resultados matemáticos; clasificar colas ligeras y pesadas; obtener la distribución t como mezcla de normales; describir las distribuciones estables; construir ejemplos de dependencia en las colas con correlación baja; explicar las consecuencias para la medición del riesgo.

**Secciones:**

- **12.1** Las colas de los rendimientos financieros como resultado empírico (con fuentes).
- **12.2** Colas ligeras y pesadas; índice de cola.
- **12.3** La distribución t como mezcla de normales.
- **12.4\*** Distribuciones estables y teorema central del límite generalizado.
- **12.5** Dependencia en las colas; ejemplos con correlación baja.
- **12.6** Consecuencias para la medición del riesgo (anticipo de L17).

**Resultados principales:** representación de la t como mezcla de normales.

**Resultados admitidos:** RA-28 (en §12.4).

**Aplicaciones financieras:** todo el capítulo.

**Computación:** comparación por simulación de colas normales y pesadas.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 13. Simulación y método Monte Carlo

**Prerrequisitos:** L8 c. 10, L8 c. 11, L8 §7.6, L3 c. 11.

**Objetivos:** explicitar la hipótesis de modelización de un generador uniforme ideal; demostrar la validez de los métodos de inversión, de aceptación y rechazo y de Box-Muller; simular normales multivariantes; construir estimadores Monte Carlo con su error estándar e intervalo aproximado; planificar el tamaño de la simulación; calcular el valor esperado de un pago de opción bajo un modelo lognormal.

**Secciones:**

- **13.1** Simulación de uniformes: la hipótesis del generador ideal.
- **13.2** Método de inversión.
- **13.3** Método de aceptación y rechazo.
- **13.4** Normales: método de Box-Muller; normales multivariantes mediante Cholesky.
- **13.5** Estimador Monte Carlo: insesgamiento, error estándar e intervalo aproximado.
- **13.6** Tamaño de la simulación y costo computacional.
- **13.7** Valor esperado de un pago de opción bajo un modelo lognormal (sin teoría de valoración, que llega en L13 y L19).

**Resultados principales:** validez de los métodos de inversión, aceptación y rechazo, y Box-Muller; propiedades del estimador Monte Carlo.

**Resultados admitidos:** RA-08 (en §13.4).

**Aplicaciones financieras:** valor esperado de pagos de opciones; distribución simulada del valor de una cartera.

**Computación:** todo el capítulo.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

### Capítulo 14. Paseos aleatorios y cadenas de Markov finitas

**Prerrequisitos:** L8 c. 3, L8 c. 9, L8 c. 10, L6 c. 9, L7 §1.5.

**Objetivos:** estudiar el paseo aleatorio simple y la distribución de su posición; resolver el problema de la ruina del jugador; definir cadenas de Markov finitas y usar las ecuaciones de Chapman-Kolmogorov; clasificar estados; demostrar la existencia de distribuciones estacionarias y la convergencia al equilibrio mediante acoplamiento; aplicar matrices de transición a calificaciones crediticias.

**Secciones:**

- **14.1** Paseo aleatorio simple: trayectorias y distribución de la posición.
- **14.2** Ruina del jugador.
- **14.3** Cadenas de Markov finitas: matriz de transición y ecuaciones de Chapman-Kolmogorov.
- **14.4** Clasificación de estados: irreducibilidad y aperiodicidad.
- **14.5** Distribución estacionaria: existencia mediante promedios y compacidad.
- **14.6** Convergencia al equilibrio mediante acoplamiento.
- **14.7** Aplicaciones: matrices de transición de calificaciones crediticias; regímenes de mercado.

**Resultados principales:** probabilidades de ruina; existencia de la distribución estacionaria; convergencia al equilibrio para cadenas irreducibles y aperiódicas.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** migración de calificaciones; regímenes de mercado.

**Computación:** potencias de matrices de transición y simulación de trayectorias.

**Extensión estimada:** 30–36 páginas; 30–40 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; tablas de la distribución normal estándar; índice de símbolos; índice analítico.
