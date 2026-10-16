# L18. Procesos estocásticos y cálculo estocástico

Índice detallado · Versión 1.0 · Entrega 1d · 2026-10-16

## Ficha editorial

- **Serie:** IV. Matemática avanzada y tiempo continuo.
- **Requisitos:** L7, L11, L12, L15, L16.
- **Capítulos:** 11, más un apéndice.
- **Extensión estimada:** 336–412 páginas.

**Propósito.** Este libro desarrolla el cálculo estocástico con demostraciones, sobre la base de la teoría de la medida de L16, el análisis de L11 y las ecuaciones diferenciales de L15. Estudia cadenas de Markov, procesos de Poisson y de saltos, movimiento browniano, martingalas en tiempo continuo, la integral de Itô, la fórmula de Itô, las ecuaciones diferenciales estocásticas, su relación con las ecuaciones en derivadas parciales, el teorema de Girsanov, la representación de martingalas y la simulación. Cada resultado que se admite tiene justificación de alcance y referencia; los centrales (isometría, fórmula de Itô, existencia y unicidad bajo Lipschitz, Feynman-Kac, Girsanov) se demuestran.

**Rutas de lectura.** Los capítulos 1 y 2 pueden leerse después del capítulo 7 si el interés principal es la valoración por difusiones; el capítulo 2 es necesario para los modelos con saltos y de crédito (L19 c. 11, L22 c. 7).

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro (NOTACION §6 y §8.3).

## Capítulos

### Capítulo 1. Cadenas de Markov en espacios numerables y en tiempo continuo

**Prerrequisitos:** L8 c. 14, L16 c. 10, L15 c. 2.

**Objetivos:** clasificar estados como recurrentes o transitorios; demostrar el teorema ergódico para cadenas numerables irreducibles y positivamente recurrentes; definir cadenas en tiempo continuo mediante su generador; resolver las ecuaciones de Kolmogorov en espacios finitos con la exponencial de matrices; construir cadenas en tiempo continuo con tiempos exponenciales; aplicar a calificaciones y regímenes.

**Secciones:**

- **1.1** Recurrencia y transitoriedad en espacios numerables.
- **1.2** Distribuciones estacionarias y teorema ergódico.
- **1.3** Cadenas en tiempo continuo: generador y ecuaciones de Kolmogorov en espacios finitos.
- **1.4** Construcción mediante tiempos exponenciales.
- **1.5** Aplicaciones: calificaciones en tiempo continuo y regímenes.

**Resultados principales:** criterio de recurrencia; teorema ergódico; P(t) = e^(tQ) en espacios finitos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** migración de calificaciones en tiempo continuo.

**Computación:** estimación de generadores y simulación.

**Extensión estimada:** 30–36 páginas; 25–35 ejercicios.

### Capítulo 2. Procesos de Poisson, procesos con saltos y cambio de variables con saltos

**Prerrequisitos:** L18 c. 1, L16 c. 6, L8 §5.3, L11 c. 6.

**Objetivos:** demostrar la equivalencia de las definiciones del proceso de Poisson; demostrar sus propiedades de superposición y adelgazamiento; trabajar con procesos de Poisson compuestos y sus martingalas compensadas; integrar respecto de procesos de variación finita con saltos; demostrar la fórmula de cambio de variables para esos procesos; aplicar a modelos de incumplimiento y de pérdidas agregadas.

**Secciones:**

- **2.1** Proceso de Poisson: definiciones equivalentes.
- **2.2** Incrementos independientes, superposición y adelgazamiento.
- **2.3** Proceso de Poisson compuesto.
- **2.4** Martingalas compensadas.
- **2.5** Integración respecto de procesos de variación finita con saltos.
- **2.6** Fórmula de cambio de variables con saltos.
- **2.7** Aplicaciones: tiempos de incumplimiento y pérdidas agregadas.

**Resultados principales:** equivalencia de definiciones; propiedades de martingala compensada; fórmula de cambio de variables con saltos de variación finita.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** modelos de incumplimiento (anticipo de L22 c. 7); pérdidas operativas.

**Computación:** simulación de procesos de Poisson compuestos.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

### Capítulo 3. Movimiento browniano

**Prerrequisitos:** L16 c. 6, L16 c. 8, L11 c. 10, L8 §7.6.

**Objetivos:** definir el movimiento browniano como proceso gaussiano; construirlo mediante la serie de Lévy y demostrar la convergencia uniforme casi segura; demostrar sus invariancias y la propiedad de Markov; demostrar la convergencia de su variación cuadrática; demostrar que sus trayectorias no son derivables y tienen variación no acotada; relacionarlo con el paseo aleatorio.

**Secciones:**

- **3.1** Definición; procesos gaussianos.
- **3.2** Construcción de Lévy.
- **3.3** Invariancias y propiedad de Markov.
- **3.4** Variación cuadrática.
- **3.5** No derivabilidad y variación no acotada.
- **3.6** El movimiento browniano como límite del paseo aleatorio: convergencia de distribuciones finito-dimensionales y teorema de Donsker.

**Resultados principales:** existencia del movimiento browniano; variación cuadrática igual a t; no derivabilidad; convergencia finito-dimensional del paseo aleatorio normalizado.

**Resultados admitidos:** RA-49 (en §3.6).

**Aplicaciones financieras:** el modelo de Bachelier y su motivación.

**Computación:** simulación de trayectorias y de variaciones cuadráticas.

**Extensión estimada:** 32–38 páginas; 25–35 ejercicios.

### Capítulo 4. Martingalas en tiempo continuo y principio de reflexión

**Prerrequisitos:** L18 c. 3, L16 c. 10, L16 c. 11.

**Objetivos:** trabajar con la filtración browniana aumentada y demostrar la ley 0-1 de Blumenthal; reconocer martingalas brownianas; definir tiempos de parada en tiempo continuo y demostrar la propiedad fuerte de Markov del movimiento browniano; demostrar el muestreo opcional en tiempo continuo para martingalas continuas; demostrar el principio de reflexión y obtener la distribución del máximo; calcular distribuciones de tiempos de llegada y probabilidades de ruina con deriva.

**Secciones:**

- **4.1** Filtración browniana aumentada; ley 0-1 de Blumenthal.
- **4.2** Martingalas continuas; martingalas brownianas.
- **4.3** Tiempos de parada; propiedad fuerte de Markov.
- **4.4** Muestreo opcional en tiempo continuo.
- **4.5** Principio de reflexión y distribución del máximo.
- **4.6** Tiempos de llegada y ruina con deriva mediante la martingala exponencial.

**Resultados principales:** propiedad fuerte de Markov; principio de reflexión; distribución de tiempos de llegada.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** probabilidades de alcanzar barreras (anticipo de L19 c. 8 y L22 c. 6).

**Computación:** verificación por simulación de la distribución del máximo.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

### Capítulo 5. La integral de Itô

**Prerrequisitos:** L18 c. 3, L18 c. 4, L16 c. 4, L11 c. 10.

**Objetivos:** explicar por qué la integral de Stieltjes no sirve para el movimiento browniano; definir la integral de procesos simples y demostrar la isometría de Itô; demostrar la densidad de los procesos simples y extender la integral; demostrar sus propiedades de martingala y su variación cuadrática; extender por localización; interpretar la integral como ganancias de una estrategia; comparar con la integral de Stratonovich.

**Secciones:**

- **5.1** Por qué no sirve la integral de Stieltjes.
- **5.2** Procesos simples e isometría de Itô.
- **5.3** Extensión a procesos progresivamente medibles de cuadrado integrable.
- **5.4** Propiedades: martingala y variación cuadrática.
- **5.5** Extensión por localización.
- **5.6** La integral como ganancias de una estrategia en tiempo continuo.
- **5.7** Integral de Stratonovich: definición y comparación.

**Resultados principales:** isometría de Itô; densidad de los procesos simples; propiedades de la integral.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** proceso de ganancias.

**Computación:** aproximación de integrales de Itô por sumas y comparación con Stratonovich.

**Extensión estimada:** 32–38 páginas; 25–35 ejercicios.

### Capítulo 6. Fórmula de Itô

**Prerrequisitos:** L18 c. 5, L7 §5.3, L11 §10.5.

**Objetivos:** enunciar y demostrar la fórmula de Itô en una dimensión; definir procesos de Itô y aplicar su fórmula; demostrar la versión multidimensional con covariaciones; aplicarla al movimiento browniano geométrico, a la exponencial estocástica y a la integración por partes; relacionarla con la fórmula de Föllmer.

**Secciones:**

- **6.1** Enunciado y heurística.
- **6.2** Demostración.
- **6.3** Procesos de Itô y su fórmula.
- **6.4** Fórmula multidimensional y covariación.
- **6.5** Aplicaciones: movimiento browniano geométrico, exponencial estocástica, integración por partes.
- **6.6** Relación con la fórmula de Föllmer.

**Resultados principales:** fórmula de Itô en una y varias dimensiones.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** dinámica del logaritmo del precio; valor de carteras autofinanciadas.

**Computación:** verificación numérica de la fórmula de Itô sobre trayectorias simuladas.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 7. Ecuaciones diferenciales estocásticas

**Prerrequisitos:** L18 c. 6, L15 c. 1.

**Objetivos:** definir soluciones fuertes; demostrar existencia y unicidad bajo coeficientes de Lipschitz mediante iteración de Picard y la desigualdad de Gronwall; resolver el movimiento browniano geométrico, el proceso de Ornstein-Uhlenbeck y las ecuaciones lineales; describir las ecuaciones sin coeficientes de Lipschitz; enunciar la propiedad de Markov de las soluciones.

**Secciones:**

- **7.1** Soluciones fuertes.
- **7.2** Existencia y unicidad bajo coeficientes de Lipschitz.
- **7.3** Movimiento browniano geométrico.
- **7.4** Proceso de Ornstein-Uhlenbeck: solución, distribución y estacionariedad.
- **7.5** Ecuaciones lineales generales.
- **7.6** Coeficientes que no son de Lipschitz: el proceso de raíz cuadrada.
- **7.7** Propiedad de Markov de las soluciones.

**Resultados principales:** teorema de existencia y unicidad; soluciones explícitas de las ecuaciones lineales.

**Resultados admitidos:** RA-18 (en §7.6), RA-50 (en §7.7).

**Aplicaciones financieras:** modelos de precios y de tasas.

**Computación:** comparación de soluciones exactas y simuladas.

**Extensión estimada:** 30–36 páginas; 25–35 ejercicios.

### Capítulo 8. Generador infinitesimal, Feynman-Kac y ecuaciones de Kolmogorov

**Prerrequisitos:** L18 c. 7, L15 c. 5, L15 c. 7.

**Objetivos:** definir el generador de una difusión y demostrar la fórmula de Dynkin; demostrar el teorema de Feynman-Kac en su forma de representación; enunciar la existencia de soluciones clásicas; derivar la ecuación retrospectiva de Kolmogorov y, bajo hipótesis de regularidad de la densidad, la ecuación prospectiva; verificar las densidades del movimiento browniano y del proceso de Ornstein-Uhlenbeck.

**Secciones:**

- **8.1** Generador infinitesimal y fórmula de Dynkin.
- **8.2** Teorema de Feynman-Kac: representación de soluciones como esperanzas.
- **8.3** Existencia de soluciones clásicas a partir de la esperanza.
- **8.4** Ecuación retrospectiva de Kolmogorov.
- **8.5** Ecuación prospectiva de Kolmogorov bajo hipótesis de regularidad.
- **8.6** Ejemplos: movimiento browniano y proceso de Ornstein-Uhlenbeck.

**Resultados principales:** fórmula de Dynkin; teorema de representación de Feynman-Kac; ecuaciones de Kolmogorov bajo hipótesis explícitas.

**Resultados admitidos:** RA-51 (en §8.3).

**Aplicaciones financieras:** valoración por ecuaciones en derivadas parciales (L19 c. 2).

**Computación:** comparación entre solución numérica de la ecuación y Monte Carlo.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

### Capítulo 9. Teorema de Girsanov

**Prerrequisitos:** L18 c. 6, L16 c. 9, L16 c. 12.

**Objetivos:** demostrar la caracterización de Lévy del movimiento browniano; cambiar de medida con una densidad exponencial; demostrar el teorema de Girsanov; enunciar la condición de Novikov; eliminar la deriva de un proceso; interpretar el precio de mercado del riesgo.

**Secciones:**

- **9.1** Caracterización de Lévy del movimiento browniano.
- **9.2** Cambio de medida con densidad exponencial.
- **9.3** Teorema de Girsanov.
- **9.4** Condición de Novikov.
- **9.5** Eliminación de la deriva.
- **9.6** Precio de mercado del riesgo (anticipo de L19 c. 2).

**Resultados principales:** caracterización de Lévy; teorema de Girsanov.

**Resultados admitidos:** RA-17 (en §9.4).

**Aplicaciones financieras:** medida neutral al riesgo en tiempo continuo.

**Computación:** verificación por muestreo de importancia.

**Extensión estimada:** 24–30 páginas; 20–30 ejercicios.

### Capítulo 10. Representación de martingalas

**Prerrequisitos:** L18 c. 9, L18 c. 5.

**Objetivos:** enunciar el teorema de representación de martingalas brownianas; demostrar la representación para exponenciales estocásticas y la densidad de su espacio generado; obtener representaciones explícitas mediante la fórmula de Itô; explicar la consecuencia para la completitud del mercado de Black-Scholes.

**Secciones:**

- **10.1** Enunciado.
- **10.2** Demostración para exponenciales estocásticas y densidad de su espacio generado.
- **10.3** Representaciones explícitas mediante la fórmula de Itô.
- **10.4** Consecuencia: completitud del mercado de Black-Scholes (anticipo de L19 c. 2).

**Resultados principales:** representación para exponenciales estocásticas; densidad de su espacio generado.

**Resultados admitidos:** RA-16 (en §10.2, cierre de la demostración general).

**Aplicaciones financieras:** existencia de estrategias de replicación.

**Computación:** no corresponde.

**Extensión estimada:** 20–26 páginas; 15–25 ejercicios.

### Capítulo 11. Simulación de ecuaciones diferenciales estocásticas

**Prerrequisitos:** L18 c. 7, L12 c. 9, L15 c. 4.

**Objetivos:** implementar el esquema de Euler-Maruyama; demostrar su convergencia fuerte de orden 1/2 bajo coeficientes de Lipschitz; enunciar su orden débil; derivar el esquema de Milstein; simular exactamente el movimiento browniano geométrico y el proceso de Ornstein-Uhlenbeck; tratar la positividad del proceso de raíz cuadrada; describir Monte Carlo multinivel.

**Secciones:**

- **11.1** Esquema de Euler-Maruyama.
- **11.2** Convergencia fuerte de orden 1/2; orden débil.
- **11.3** Esquema de Milstein.
- **11.4** Simulación exacta del movimiento browniano geométrico y del proceso de Ornstein-Uhlenbeck.
- **11.5** El proceso de raíz cuadrada: esquemas que preservan la positividad.
- **11.6** Monte Carlo multinivel (presentación).

**Resultados principales:** convergencia fuerte de orden 1/2 de Euler-Maruyama.

**Resultados admitidos:** RA-52 (en §11.2 y §11.3).

**Aplicaciones financieras:** valoración por simulación.

**Computación:** estudio empírico de órdenes de convergencia.

**Extensión estimada:** 26–32 páginas; 20–30 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
