# Plan editorial de la colección Atlas Quant

Versión 1.0 · Fase 1a · 2026-10-15
Estado: propuesta aprobada en principio por la dirección editorial; los índices detallados por sección se elaboran en las entregas 1b a 1d.

---

## 1. Propósito de la colección

Atlas Quant es una colección de libros de texto universitarios de Finanzas Cuantitativas escrita en español. Su objetivo es que un lector adulto sin formación matemática avanzada pueda alcanzar, mediante estudio autónomo, la competencia necesaria para comprender, demostrar, implementar y evaluar críticamente los modelos matemáticos, estadísticos y computacionales de las finanzas, y para realizar investigación cuantitativa reproducible.

La colección aspira a una profundidad comparable con la de una trayectoria universitaria rigurosa. No otorga credenciales académicas ni garantiza competencia profesional: distingue entre el conocimiento estudiado, la competencia demostrada mediante ejercicios y proyectos, y las credenciales formales, que esta obra no confiere.

## 2. Lector previsto y forma de uso

El lector previsto es una persona adulta que parte de la aritmética escolar y está dispuesta a estudiar de manera sostenida. No se presupone dominio del álgebra, del cálculo, de la probabilidad ni de la programación. Se presupone capacidad de lectura de textos técnicos en español y, a partir de la Serie III, lectura básica de inglés técnico, porque buena parte de la literatura de referencia está en ese idioma.

Cada libro declara sus prerrequisitos por capítulo. Las secciones marcadas con asterisco (\*) son opcionales en una primera lectura y su omisión no impide comprender el resto del libro.

## 3. Principios editoriales

1. **Prosa académica explicativa.** La exposición se desarrolla en párrafos que razonan. Las listas se reservan para contenido genuinamente enumerativo.
2. **Cierre de prerrequisitos.** Todo término, símbolo, técnica o resultado empleado en un capítulo está definido o demostrado en el propio capítulo, en un capítulo declarado como prerrequisito, o figura como resultado admitido con referencia (véase `LIBRO_DE_ESTILO.md`, sección 4).
3. **Rigor con intuición.** Las demostraciones son completas o se declaran parciales con su razón. La intuición acompaña al rigor y nunca lo sustituye.
4. **Las finanzas como aplicación y motivación,** desde el Libro 5, y antes como ejemplos elementales (porcentajes, interés compuesto). Las aplicaciones financieras se incluyen cuando corresponden; no se fuerzan en capítulos donde no aportan.
5. **Python como material didáctico** integrado en la exposición, desde el Libro 1, y tratado sistemáticamente en el Libro 3. El código ilustra, verifica y aplica la teoría; nunca reemplaza una demostración.
6. **Honestidad intelectual.** Se distinguen definición, teorema, aproximación, hipótesis de modelización, convención de mercado y resultado empírico. No se inventan referencias, datos ni resultados.

## 4. Estructura de la colección

La colección se organiza en cinco series y 23 libros. La numeración de los libros es un orden de lectura válido: cada libro solo requiere libros de número menor.

| Serie | Libros | Tema |
|---|---|---|
| I. Fundamentos | L1–L4 | Lenguaje matemático, álgebra, funciones, programación, cálculo |
| II. Matemática para las finanzas | L5–L9 | Matemática financiera, álgebra lineal, cálculo multivariable, probabilidad, estadística |
| III. Teoría financiera y modelización | L10–L14 | Mercados y valoración, análisis real, análisis numérico, derivados discretos, econometría |
| IV. Matemática avanzada y tiempo continuo | L15–L19 | Ecuaciones diferenciales, probabilidad con medida, carteras y riesgo, cálculo estocástico, derivados continuos |
| V. Investigación | L20–L23 | Metodología empírica, aprendizaje estadístico, tasas y crédito, estudios de caso |

### 4.1 Clasificación por prioridad

- **Formación general indispensable:** L1 a L21 y L23.
- **Especialización:** L22 (tasas de interés y riesgo de crédito).
- **Especializaciones sin libro propio por ahora:** control estocástico y ecuación de Hamilton-Jacobi-Bellman; procesos de Lévy generales; econometría de alta frecuencia y volatilidad realizada; matrices aleatorias para covarianzas de alta dimensión; diferencias finitas multidimensionales; aprendizaje profundo; aprendizaje por refuerzo; econometría bayesiana de series temporales. Se incorporarán como libros o apéndices solo si los capítulos previos muestran una necesidad justificada.
- **Fuera del alcance de la obra:** cálculo de Malliavin; caminos rugosos y volatilidad rugosa; análisis funcional general; normativa regulatoria detallada (se menciona con fecha de verificación); contabilidad, impuestos y derecho; particularidades de criptoactivos.

---

## 5. Índice provisional por libro

Índice a nivel de capítulo. Los índices por sección, con prerrequisitos por capítulo y extensión, son los entregables 1b (L1–L8), 1c (L9–L16) y 1d (L17–L23). Los textos de contraste se usarán para comparar cobertura y profundidad; sus metadatos se verificarán en la entrega 1e y aquí se consignan solo por autor y título.

### Serie I. Fundamentos

#### L1. Lenguaje matemático, números y álgebra (14 capítulos)

Incluye prefacio y guía del lector: cómo estudiar matemáticas, cómo leer una demostración, cómo usar los ejercicios.

1. Qué es una afirmación matemática: definición, enunciado, demostración, contraejemplo.
2. Lógica proposicional y cuantificadores; negación de enunciados.
3. Conjuntos, relaciones y funciones (versión elemental).
4. Métodos de demostración: directa, contrarrecíproco, absurdo, casos, inducción; desigualdad de Bernoulli.
5. Números naturales y enteros: divisibilidad, división euclídea, algoritmo de Euclides.
6. Números racionales: fracciones, razones, proporciones, porcentajes y variaciones porcentuales.
7. Números reales: axiomas de cuerpo ordenado, valor absoluto, desigualdades, axioma del supremo, propiedad arquimediana, existencia e irracionalidad de la raíz cuadrada de 2.
8. Potencias, raíces y logaritmos: leyes de exponentes enteros y racionales demostradas; exponentes reales y logaritmos como resultados admitidos; interés compuesto, tiempo de duplicación y regla del 72. **Capítulo piloto.**
9. Magnitudes, unidades, órdenes de magnitud y error; representación de números en una computadora.
10. Polinomios: operaciones, factorización, división, teorema del resto, teorema del binomio.
11. Ecuaciones e inecuaciones; fórmula cuadrática; soluciones extrañas.
12. Sistemas de ecuaciones e interpretación geométrica.
13. Modelización algebraica de problemas.
14. Algoritmos y primeros programas en Python.

Textos de contraste: Velleman, *How to Prove It*; Spivak, *Calculus* (capítulos iniciales).

#### L2. Funciones, trigonometría y geometría analítica (13 capítulos)

1. Función: dominio, codominio, imagen, gráfico, composición, inversa.
2. Funciones lineales y afines.
3. Funciones cuadráticas y polinómicas.
4. Funciones racionales y asíntotas.
5. Transformaciones y simetrías.
6. Sucesiones y sumas: progresiones, notación sigma, inducción en sumas, suma geométrica; la anualidad como suma geométrica.
7. Convergencia de sucesiones: definición con ε y N, álgebra de límites, convergencia monótona deducida del axioma del supremo, el número *e*.
8. Funciones exponenciales y logarítmicas: base *e*, logaritmo natural, crecimiento y escalas, rendimientos logarítmicos (introducción).
9. Geometría analítica del plano y cónicas.
10. Trigonometría y funciones periódicas.
11. Vectores en el plano y el espacio; producto escalar.
12. Números complejos: forma binómica y polar, fórmula de De Moivre.
13. Exploración gráfica y numérica de funciones con Python.

#### L3. Programación en Python para la matemática aplicada (12 capítulos)

1. Programas, intérpretes y entornos.
2. Tipos y expresiones; aritmética de punto flotante (IEEE 754) y sus consecuencias.
3. Control de flujo, funciones y recursión.
4. Estructuras de datos y costo de sus operaciones.
5. Corrección y complejidad de algoritmos: invariantes, notación O, búsqueda y ordenamiento.
6. Errores, pruebas y depuración.
7. Clases y objetos con fines científicos.
8. Cálculo vectorial con NumPy.
9. Series temporales y datos tabulares con pandas; trampas de alineación.
10. Visualización científica honesta.
11. Números pseudoaleatorios, semillas y reproducibilidad.
12. Organización de un trabajo computacional reproducible.

#### L4. Cálculo en una variable (14 capítulos)

1. Completitud y sucesiones: repaso de L2, Bolzano-Weierstrass, sucesiones de Cauchy, límites superior e inferior.
2. Límites de funciones (definición ε-δ).
3. Continuidad: teoremas de Bolzano y de Weierstrass; método de bisección.
4. La derivada y sus reglas, demostradas.
5. Regla de la cadena, derivación implícita, derivada de la función inversa.
6. Teorema del valor medio, monotonía, convexidad, regla de L'Hôpital.
7. Optimización y método de Newton.
8. La integral de Riemann.
9. Teorema fundamental del cálculo y técnicas de integración.
10. Construcción rigurosa del logaritmo y la exponencial: ln x = ∫₁ˣ dt/t, exponencial como inversa, a^x = exp(x ln a), coherencia con L1 y L2; capitalización continua.
11. Integrales impropias; función Gamma; valor presente de flujos continuos.
12. Series numéricas; perpetuidades.
13. Series de potencias, Taylor con resto, fórmula de Euler.
14. Derivación e integración numéricas: error de truncamiento y de redondeo.

Textos de contraste: Spivak, *Calculus*; Apostol, *Calculus*, vol. 1.

### Serie II. Matemática para las finanzas

#### L5. Matemática financiera (11 capítulos)

1. Valor temporal del dinero; interés simple y compuesto.
2. Tasas nominales, efectivas, equivalentes y continuas; convenciones de conteo de días.
3. Ecuación de valor y descuento.
4. Anualidades y perpetuidades: constantes, crecientes, continuas.
5. Sistemas de amortización.
6. Valor presente neto y tasa interna de retorno: existencia, unicidad, TIR múltiples, cálculo numérico.
7. Inflación y ecuación de Fisher (exacta y aproximada).
8. Bonos: precio, rendimiento al vencimiento, interés corrido, precio limpio y sucio.
9. Duración, convexidad e inmunización (teorema de Redington).
10. Estructura temporal de tasas: tasas cero, tasas a plazo, factores de descuento, *bootstrapping*, interpolación.
11. Implementación y verificación computacional de los cálculos del libro.

Ruta temprana opcional: los capítulos 1–3, 5, 7 y 8 pueden leerse después de L2.

Texto de contraste: Kellison, *The Theory of Interest*.

#### L6. Álgebra lineal (13 capítulos)

1. Sistemas lineales y eliminación gaussiana.
2. Matrices, inversas, factorización LU.
3. Espacios vectoriales y subespacios.
4. Independencia lineal, bases y dimensión.
5. Transformaciones lineales; núcleo, imagen, teorema de la dimensión.
6. Determinantes y permutaciones.
7. Producto interno, Gram-Schmidt, factorización QR.
8. Proyecciones ortogonales y mínimos cuadrados.
9. Valores y vectores propios, diagonalización, forma de Jordan (demostración opcional), exponencial de matrices.
10. Teorema espectral, formas cuadráticas, matrices definidas positivas.
11. Descomposición en valores singulares y componentes principales (versión algebraica); aplicación a curvas de tasas.
12. Álgebra lineal numérica: condicionamiento, factorización de Cholesky.
13. Aplicaciones: replicación lineal de pagos y precios de estado, carteras como vectores, matriz de covarianza muestral como objeto descriptivo.

Textos de contraste: Strang, *Introduction to Linear Algebra*; Axler, *Linear Algebra Done Right*.

#### L7. Cálculo en varias variables y optimización (11 capítulos)

1. Topología de Rⁿ: normas, abiertos, cerrados, compactos, completitud.
2. Límites y continuidad.
3. Diferenciabilidad, gradiente, matriz jacobiana.
4. Regla de la cadena.
5. Taylor en varias variables; matriz hessiana.
6. Optimización libre.
7. Conjuntos y funciones convexas; teorema de separación; lema de Farkas.
8. Contracciones en Rⁿ; teoremas de la función inversa e implícita; multiplicadores de Lagrange.
9. Condiciones de Karush-Kuhn-Tucker y dualidad elemental.
10. Integrales múltiples, Fubini, cambio de variables (demostración parcial), integral gaussiana.
11. Optimización cuadrática con restricciones lineales (forma algebraica del problema de Markowitz); utilidad determinista.

#### L8. Probabilidad (14 capítulos)

1. Espacios de probabilidad (versión elemental).
2. Combinatoria.
3. Probabilidad condicional, independencia, teorema de Bayes.
4. Variables aleatorias discretas.
5. Variables aleatorias continuas: uniforme, exponencial, Gamma, normal, lognormal.
6. Esperanza y momentos; desigualdades de Markov, Chebyshev, Jensen y Hoeffding.
7. Vectores aleatorios, covarianza, correlación, normal multivariante.
8. Transformaciones de variables; funciones generadoras de momentos y funciones características (unicidad admitida).
9. Esperanza condicional (versión elemental).
10. Modos de convergencia y leyes débiles de los grandes números.
11. Teorema central del límite para arreglos triangulares bajo condición de tercer momento (método de Lindeberg).
12. Colas pesadas y dependencia más allá de la correlación.
13. Simulación y método Monte Carlo.
14. Paseos aleatorios y cadenas de Markov finitas; convergencia al equilibrio por acoplamiento.

Textos de contraste: Ross, *A First Course in Probability*; Blitzstein y Hwang, *Introduction to Probability*.

#### L9. Estadística e inferencia (14 capítulos)

1. Datos, muestras y estadística descriptiva de rendimientos.
2. Estimadores: sesgo, varianza, error cuadrático medio, consistencia.
3. Distribuciones muestrales: chi-cuadrado, t, F.
4. Método de momentos y máxima verosimilitud; propiedades asintóticas; información de Fisher, cota de Cramér-Rao; método delta.
5. Intervalos de confianza.
6. Contrastes de hipótesis, potencia, interpretación correcta del valor p.
7. Pruebas múltiples: Bonferroni, Holm, Benjamini-Hochberg.
8. Regresión lineal y teorema de Gauss-Markov.
9. Inferencia y diagnóstico en regresión.
10. Bootstrap y remuestreo.
11. Inferencia bayesiana introductoria.
12. Validación y sobreajuste.
13. Estadística multivariante, no paramétrica y robusta: estimación de covarianzas, componentes principales estadísticos, densidades por núcleos, estimadores robustos.
14. El problema de estimar rendimientos esperados.

Textos de contraste: Casella y Berger, *Statistical Inference*; Wasserman, *All of Statistics*.

### Serie III. Teoría financiera y modelización

#### L10. Mercados financieros y teoría de la valoración (13 capítulos)

1. Sistema financiero e intermediarios.
2. Instrumentos financieros.
3. Mecanismos de negociación y liquidez.
4. Rendimientos simples y logarítmicos; agregación temporal y entre activos.
5. Utilidad esperada y aversión al riesgo.
6. Teoría de carteras de Markowitz.
7. CAPM: derivación, hipótesis y evidencia.
8. Arbitraje en un período: precios de estado, primer teorema fundamental en mercados finitos, completitud.
9. Factor de descuento estocástico.
10. APT y modelos de factores.
11. Eficiencia de mercado y anomalías: hipótesis frente a evidencia.
12. Fricciones y límites al arbitraje.
13. Estados contables, valoración por flujos descontados y variables contables en la investigación.

Textos de contraste: Cochrane, *Asset Pricing*; Luenberger, *Investment Science*.

#### L11. Análisis real (10 capítulos)

1. Construcción de los números reales.
2. Espacios métricos, compacidad, conexión.
3. Espacios completos; teorema del punto fijo de Banach.
4. Continuidad uniforme.
5. Diferenciabilidad rigurosa.
6. Integral de Riemann-Stieltjes y funciones de variación acotada.
7. Convergencia uniforme e intercambio de límites.
8. Espacios normados y con producto interno.
9. Funciones convexas; desigualdades de Jensen, Hölder y Minkowski.
10. Variación cuadrática de funciones deterministas.

Textos de contraste: Rudin, *Principles of Mathematical Analysis*; Abbott, *Understanding Analysis*.

#### L12. Análisis numérico, optimización y simulación (12 capítulos)

1. Condicionamiento y estabilidad.
2. Ecuaciones no lineales: bisección, Newton, secante; TIR y rendimiento de bonos.
3. Sistemas lineales numéricos.
4. Interpolación y *splines*; curvas de tasas.
5. Derivación e integración numéricas.
6. Optimización sin restricciones.
7. Optimización convexa, programación lineal y cuadrática; subgradientes y métodos proximales.
8. Calibración por mínimos cuadrados no lineales.
9. Monte Carlo y reducción de varianza.
10. Cuasi-Monte Carlo.
11. Programación dinámica y parada óptima en tiempo discreto.
12. Transformada discreta de Fourier y FFT.

Textos de contraste: Glasserman, *Monte Carlo Methods in Financial Engineering*; Nocedal y Wright, *Numerical Optimization*.

#### L13. Derivados en tiempo discreto (9 capítulos)

1. Contratos a plazo y futuros.
2. Swaps.
3. Opciones, cotas de arbitraje, paridad put-call.
4. Modelo binomial de un período.
5. Modelo binomial de varios períodos; martingalas discretas.
6. Opciones americanas como problema de parada óptima.
7. Cobertura en tiempo discreto.
8. Convergencia del modelo de Cox-Ross-Rubinstein a la fórmula de Black-Scholes (vía L8 c. 11 y paridad put-call).
9. Opciones exóticas en árboles y límites del modelo.

Textos de contraste: Hull, *Options, Futures, and Other Derivatives*; Shreve, *Stochastic Calculus for Finance I*.

#### L14. Econometría y series temporales financieras (15 capítulos)

1. Hechos estilizados de los rendimientos.
2. Regresión matricial, mínimos cuadrados generalizados, heterocedasticidad, errores HAC.
3. Endogeneidad, variables instrumentales y causalidad.
4. Procesos en tiempo discreto: estacionariedad, ergodicidad; ecuaciones en diferencias lineales.
5. Modelos ARMA.
6. Raíces unitarias y regresiones espurias.
7. Pronóstico, validación temporal y bootstrap para datos dependientes.
8. Volatilidad condicional: ARCH y GARCH.
9. VAR y causalidad de Granger.
10. Cointegración y modelos de corrección de errores.
11. Rupturas estructurales y cambios de régimen.
12. Regresiones de corte transversal y procedimiento de Fama-MacBeth.
13. Método generalizado de momentos.
14. Contraste de modelos de valoración de activos.
15. Modelos de espacio de estados y filtro de Kalman.

Textos de contraste: Hamilton, *Time Series Analysis*; Tsay, *Analysis of Financial Time Series*; Campbell, Lo y MacKinlay, *The Econometrics of Financial Markets*.

### Serie IV. Matemática avanzada y tiempo continuo

#### L15. Ecuaciones diferenciales (9 capítulos)

1. EDO de primer orden: existencia y unicidad (Picard), desigualdad de Gronwall.
2. EDO lineales y sistemas; exponencial de matrices.
3. Estabilidad y comportamiento cualitativo.
4. Métodos numéricos para EDO.
5. La ecuación del calor; separación de variables.
6. Series y transformada de Fourier; solución fundamental (resultados de Riemann; teoría L² admitida).
7. Ecuaciones parabólicas: principio del máximo y unicidad.
8. Reducción de la ecuación de Black-Scholes a la ecuación del calor (la derivación financiera se hace en L19).
9. Diferencias finitas para ecuaciones parabólicas: esquemas explícito, implícito y de Crank-Nicolson; estabilidad de von Neumann.

#### L16. Probabilidad con teoría de la medida y martingalas (12 capítulos)

1. σ-álgebras y medidas; teorema de extensión de Carathéodory.
2. Funciones medibles y variables aleatorias.
3. Integral de Lebesgue y teoremas de convergencia.
4. Espacios L^p y su completitud.
5. Medida producto; teorema de Fubini-Tonelli.
6. Independencia, lemas de Borel-Cantelli, ley 0-1 de Kolmogorov.
7. Modos de convergencia; ley fuerte de los grandes números.
8. Convergencia en distribución, funciones características, teorema de continuidad de Lévy, teorema central del límite de Lindeberg-Feller.
9. Esperanza condicional respecto de una σ-álgebra; teorema de Radon-Nikodym.
10. Filtraciones, martingalas en tiempo discreto, tiempos de parada, muestreo opcional.
11. Convergencia de martingalas; desigualdades de Doob.
12. Cambio de medida; teorema fundamental de valoración en tiempo discreto (caso finito de Harrison-Pliska demostrado; caso general de Dalang-Morton-Willinger enunciado).

Textos de contraste: Williams, *Probability with Martingales*; Durrett, *Probability: Theory and Examples*.

#### L17. Construcción de carteras y gestión del riesgo (13 capítulos)

1. Error de estimación de los insumos.
2. Inestabilidad de la optimización media-varianza; estimadores de contracción.
3. Modelo de Black-Litterman.
4. Paridad de riesgo y contribuciones al riesgo.
5. Modelos de factores de riesgo.
6. Medidas de riesgo coherentes.
7. Estimación de VaR y Expected Shortfall.
8. Teoría de valores extremos.
9. Cópulas.
10. Backtesting de modelos de riesgo: pruebas de Kupiec y Christoffersen.
11. Escenarios y pruebas de estrés.
12. Riesgo de liquidez y riesgo de modelo.
13. Rebalanceo.

Texto de contraste: McNeil, Frey y Embrechts, *Quantitative Risk Management*.

#### L18. Procesos estocásticos y cálculo estocástico (11 capítulos)

1. Cadenas de Markov en espacios numerables y en tiempo continuo.
2. Procesos de Poisson y procesos con saltos; fórmula de Itô con saltos de variación finita.
3. Movimiento browniano: construcción de Lévy, propiedades, variación cuadrática.
4. Martingalas en tiempo continuo; principio de reflexión.
5. Construcción de la integral de Itô.
6. Fórmula de Itô.
7. Ecuaciones diferenciales estocásticas: existencia y unicidad; movimiento browniano geométrico; proceso de Ornstein-Uhlenbeck.
8. Generador infinitesimal, teorema de Feynman-Kac, ecuaciones retrospectiva y prospectiva de Kolmogorov.
9. Teorema de Girsanov.
10. Representación de martingalas.
11. Simulación de EDE: esquemas de Euler-Maruyama y Milstein.

Textos de contraste: Shreve, *Stochastic Calculus for Finance II*; Øksendal, *Stochastic Differential Equations*.

#### L19. Valoración de derivados en tiempo continuo (13 capítulos)

1. El mercado de Black-Scholes; estrategias autofinanciadas.
2. Valoración por replicación y por medida neutral al riesgo; equivalencia.
3. Fórmula de Black-Scholes-Merton y extensiones (dividendos, divisas, futuros).
4. Cambio de numerario: opción de intercambio de Margrabe, medidas forward, modelo de Black.
5. Griegas y cobertura.
6. Volatilidad implícita y su superficie.
7. Opciones americanas como problema de frontera libre.
8. Opciones exóticas.
9. Métodos numéricos: Monte Carlo, diferencias finitas, métodos de Fourier.
10. Volatilidad local (Dupire).
11. Modelos de Heston y de Merton con saltos.
12. Calibración y riesgo de modelo.
13. Mercados incompletos.

Texto de contraste: Björk, *Arbitrage Theory in Continuous Time*.

### Serie V. Investigación

#### L20. Investigación empírica en finanzas: metodología, backtesting y microestructura (12 capítulos)

1. El método científico aplicado a las finanzas.
2. Datos financieros: calidad, ajustes, sesgo de supervivencia y de anticipación.
3. Construcción de señales y carteras de investigación.
4. Estudios de eventos.
5. Diseño de backtests: costos, deslizamiento, capacidad.
6. Sobreajuste y pruebas múltiples: *reality check* de White, prueba SPA de Hansen.
7. Validación progresiva (*walk-forward*), purga y embargo.
8. Evaluación del desempeño; error estándar del índice de Sharpe.
9. Microestructura: modelos de Roll, Kyle y Glosten-Milgrom; nociones de equilibrio con información asimétrica.
10. Impacto de mercado y ejecución óptima (Almgren-Chriss).
11. Riesgo operativo de los sistemas.
12. Reproducibilidad y comunicación de resultados.

Textos de contraste: Harris, *Trading and Exchanges*; López de Prado, *Advances in Financial Machine Learning*.

#### L21. Aprendizaje estadístico en finanzas (13 capítulos)

1. Riesgo, sesgo-varianza y generalización.
2. Regularización: ridge, lasso, red elástica.
3. Validación con datos dependientes.
4. Clasificación y calibración.
5. Árboles de decisión.
6. Ensambles y *boosting*.
7. Métodos de núcleo (\*).
8. Aprendizaje no supervisado.
9. Fundamentos de redes neuronales.
10. Interpretabilidad y estabilidad.
11. Métodos bayesianos y MCMC (Metropolis-Hastings).
12. Aplicaciones, con escepticismo metodológico.
13. Replicación crítica de un artículo.

Texto de contraste: Hastie, Tibshirani y Friedman, *The Elements of Statistical Learning*.

#### L22. Tasas de interés y riesgo de crédito (especialización; 10 capítulos)

1. Instrumentos de tasa.
2. Construcción de curvas en la práctica.
3. Modelos de tasa corta: Vasicek, CIR, Hull-White.
4. Marco de Heath-Jarrow-Morton.
5. Medidas forward, modelo de Black para *caps* y *swaptions*, modelo de mercado LIBOR.
6. Modelo estructural de Merton.
7. Modelos de intensidad.
8. Valoración de CDS.
9. Riesgo de crédito de cartera; cópula gaussiana.
10. Introducción al CVA.

Texto de contraste: Brigo y Mercurio, *Interest Rate Models*.

#### L23. Investigación cuantitativa aplicada: estudios de caso y replicación (9 capítulos)

1. Cómo leer un artículo académico.
2. Caso: factores al estilo Fama-French.
3. Caso: *momentum* según Jegadeesh-Titman.
4. Caso: volatilidad y VaR de una cartera.
5. Caso: valoración y cobertura de opciones con datos reales.
6. Caso: aprendizaje automático sin fuga de información.
7. Diseño de una investigación original.
8. Redacción y defensa del informe.
9. Rutas de especialización.

Los datos de los casos dependen de la disponibilidad de fuentes con licencia verificable.

---

## 6. Prerrequisitos justificados

**Reglas.** Un libro A requiere un libro B si algún capítulo de A usa una definición, resultado o técnica que solo se desarrolla en B. Las dependencias que solo aportan ejemplos o motivación se marcan como «aplicación» y no impiden la lectura. Todo requisito tiene número menor que el libro que lo usa; por construcción, el grafo no tiene ciclos. Los resultados usados antes de su demostración se rigen por `LIBRO_DE_ESTILO.md`, sección 4, y se registran en `editorial/resultados_admitidos.md`. En la columna «Aplicación», el capítulo indicado entre paréntesis es el del libro de la fila que usa esa aplicación.

| Libro | Requisitos | Justificación | Aplicación |
|---|---|---|---|
| L1 | — | — | — |
| L2 | L1 | Lógica y demostración (c. 2–4); reales y axioma del supremo (c. 7); potencias (c. 8); binomio (c. 10) | — |
| L3 | L1, L2 | Funciones (L2 c. 1); logaritmos para la notación O (L2 c. 8); vectores (L2 c. 11); números en la computadora (L1 c. 9) | — |
| L4 | L2, L3 | Sucesiones y convergencia monótona (L2 c. 6–7); funciones elementales (L2 c. 1–8); Python para secciones computacionales y c. 14 (L3 c. 1–4, 8) | — |
| L5 | L3, L4 | Anualidades continuas (L4 c. 9–11); existencia y cálculo de la TIR (L4 c. 3, 7); duración y convexidad (L4 c. 13); cálculo numérico (L3) | — |
| L6 | L2, L3 | Vectores (L2 c. 11); complejos para valores propios (L2 c. 12); demostración (L1); computación (L3 c. 8) | L5 (c. 11 y 13) |
| L7 | L4, L6 | Cálculo en una variable; matrices, formas cuadráticas y teorema espectral (L6 c. 10) | — |
| L8 | L3, L4, L6, L7 | Integrales (L4 c. 9–11); covarianza y normal multivariante (L6 c. 10, 12); integrales múltiples y cambio de variables (L7 c. 10); simulación (L3) | — |
| L9 | L3, L6, L7, L8 | Probabilidad, incluidos TCL (L8 c. 10–11) y esperanza condicional (L8 c. 9); verosimilitud multivariante (L7 c. 3, 5–6); proyección y formas cuadráticas (L6 c. 8, 10); bootstrap (L3) | L5 |
| L10 | L5, L6, L7, L8, L9 | Descuento (L5); lema de Farkas (L7 c. 7); Lagrange (L7 c. 8); varianza de cartera (L8 c. 7); contrastes empíricos (L9 c. 8–9) | — |
| L11 | L4, L6, L7 | Cálculo riguroso (L4); producto interno (L6 c. 7); topología de Rⁿ (L7 c. 1) | — |
| L12 | L3, L4, L6, L7, L8 | Errores de truncamiento (L4 c. 14); álgebra lineal numérica (L6 c. 12); KKT (L7 c. 9); error Monte Carlo (L8 c. 11); esperanza condicional (L8 c. 9) | L5, L10 |
| L13 | L3, L5, L8, L10, L12 | Descuento y curvas (L5 c. 3, 10); arbitraje (L10 c. 8); TCL para arreglos triangulares (L8 c. 11); paseo aleatorio (L8 c. 14); parada óptima (L12 c. 11) | — |
| L14 | L3, L6, L9, L10, L12 | Inferencia asintótica (L9); polinomios de rezagos y matriz compañera (L6 c. 9; L2 c. 12); verosimilitud numérica y simulación (L12); modelos de valoración (L10) | — |
| L15 | L6, L7, L11, L12 | Jordan y exponencial de matrices (L6 c. 9); punto fijo y convergencia uniforme (L11 c. 3, 7); producto interno (L11 c. 8); sistemas tridiagonales (L12 c. 3) | — |
| L16 | L8, L11 | Probabilidad elemental; análisis riguroso y completitud (L11) | L13 (c. 12) |
| L17 | L9, L10, L12, L14 | Contracción de covarianzas (L9); Markowitz (L10); optimización convexa (L12 c. 7); GARCH y factores (L14 c. 8, 12) | L16 (c. 8, valores extremos) |
| L18 | L7, L11, L12, L15, L16 | Stieltjes y variación cuadrática (L11 c. 6, 10); L², martingalas, Borel-Cantelli (L16); Gronwall y Picard (L15 c. 1); EDP (L15 c. 5, 7); esquemas numéricos (L12) | — |
| L19 | L9, L12, L13, L15, L16, L18 | Tiempo discreto (L13); Itô y Girsanov (L18); EDP y diferencias finitas (L15); funciones características (L16 c. 8); FFT (L12 c. 12); regresión para Longstaff-Schwartz (L9) | — |
| L20 | L9, L10, L12, L14, L17 | Pruebas múltiples (L9 c. 7); HAC y bootstrap dependiente (L14 c. 2, 7); factores (L10); riesgo y costos (L17) | L15 (c. 10) |
| L21 | L6, L7, L9, L12, L14, L20 | Valores singulares (L6 c. 11); convexidad (L7 c. 7); inferencia (L9); subgradientes (L12 c. 7); dependencia temporal (L14); purga y embargo (L20 c. 7) | — |
| L22 | L5, L12, L13, L17, L18, L19 | Instrumentos (L5, L13); EDE de tasa corta (L18); cambio de numerario (L19 c. 4); cópulas (L17 c. 9); *splines* (L12 c. 4) | — |
| L23 | L9, L14, L17, L20, L21 | Metodología (L20); aprendizaje estadístico (L21); Fama-MacBeth (L14 c. 12); VaR (L17) | L19 (solo caso 5) |

**Ruta crítica:** L1 → L2 → L4 → L11 → L16 → L18 → L19.

**Cadenas transversales:**

- *Fourier:* L2 c. 12 → L4 c. 13 → L12 c. 12 → L15 c. 6 → L8 c. 8 (unicidad admitida) → L16 c. 8 → L19 c. 9.
- *Valoración de derivados:* L5 → L10 c. 8 → L13 → L16 c. 12 → L18 → L19 → L22.
- *Ecuaciones diferenciales:* L4 → L7 → L11 → L15 → L18 c. 8 → L19.
- *Optimización:* L4 c. 7 → L7 c. 6–9 → L12 c. 6–8, 11 → L10, L13, L17, L21.
- *Econometría:* L8 → L9 → L14 → L17, L20, L21.

**Fundamento del número *e*.** L1 c. 7 enuncia el axioma del supremo y deduce la propiedad arquimediana; L1 c. 10 demuestra el teorema del binomio. L2 c. 7 demuestra la convergencia monótona a partir del axioma del supremo y, con el binomio y la suma geométrica de L2 c. 6, prueba que (1 + 1/n)^n es creciente y acotada por 3. La convergencia de (1 + x/n)^n a e^x para x real y la existencia de exponentes reales y logaritmos son resultados admitidos hasta L4 c. 10, cuyas demostraciones no dependen de ellos.

---

## 7. Formato editorial

**Partes de cada libro.** Portada; página de créditos con datos provisionales; prefacio; a quién está dirigido; prerrequisitos y guía de lectura; notación; capítulos con secciones numeradas; apéndices; bibliografía; índice de símbolos; índice analítico.

**Solucionarios.** Un volumen complementario por libro. Las demostraciones y aplicaciones reciben solución completa y razonada; los ejercicios rutinarios, respuesta y paso clave; los problemas abiertos de investigación, orientaciones. Cada libro incluye además una selección de soluciones.

**Elementos numerados por capítulo.** Definición, Teorema, Lema, Proposición, Corolario, Ejemplo, Ejercicio y ecuaciones citadas. Elementos identificados sin numeración obligatoria: Observación, Demostración, Hipótesis de modelización, Resultado empírico, Resultado admitido. Las normas de uso están en `LIBRO_DE_ESTILO.md`.

**Ejercicios.** Entre 30 y 60 por capítulo, marcados por tipo y por dificultad.

**Código.** Fragmentos breves en el texto, explicados línea por línea, con la salida real de su ejecución; versiones completas como material complementario del libro.

**Formato fuente y composición.** Markdown con matemáticas LaTeX, siguiendo las convenciones de libros de Quarto. La composición en PDF se evaluará en la Fase 2 mediante un plan de prueba que se presentará para aprobación antes de instalar nada.

---

## 8. Estimaciones

Las cifras siguientes son escenarios, no compromisos de producción. El capítulo piloto proporcionará la primera medición real y las estimaciones se recalcularán con ella.

**Fórmulas.** Páginas = capítulos × páginas por capítulo + preliminares (unas 20 por libro). Palabras = páginas × palabras por página. Sesiones = capítulos × sesiones por capítulo + revisiones por libro.

| Supuesto | Valor | Incertidumbre |
|---|---|---|
| Capítulos | 277 | Baja (±5 % en la Fase 1) |
| Páginas por capítulo | 25–40 | Media |
| Palabras por página | 300–380 | Alta: depende del formato de página |
| Solucionarios | 40 %–70 % del texto principal | Alta |
| Sesiones por capítulo, con verificación | 2–5 | Muy alta: sin datos todavía |
| Rondas de revisión por capítulo | 1–3 | Alta |

| Libro | Caps. | Páginas | Libro | Caps. | Páginas |
|---|---|---|---|---|---|
| L1 | 14 | 350–560 | L13 | 9 | 225–360 |
| L2 | 13 | 325–520 | L14 | 15 | 375–600 |
| L3 | 12 | 300–480 | L15 | 9 | 225–360 |
| L4 | 14 | 350–560 | L16 | 12 | 300–480 |
| L5 | 11 | 275–440 | L17 | 13 | 325–520 |
| L6 | 13 | 325–520 | L18 | 11 | 275–440 |
| L7 | 11 | 275–440 | L19 | 13 | 325–520 |
| L8 | 14 | 350–560 | L20 | 12 | 300–480 |
| L9 | 14 | 350–560 | L21 | 13 | 325–520 |
| L10 | 13 | 325–520 | L22 | 10 | 250–400 |
| L11 | 10 | 250–400 | L23 | 9 | 225–360 |
| L12 | 12 | 300–480 | **Total** | **277** | **6925–11 080** |

Escenario agregado: texto principal de 6900 a 11 100 páginas más unas 460 de preliminares; entre 2,2 y 4,4 millones de palabras; solucionarios de 3000 a 8000 páginas; entre 600 y 1500 sesiones de trabajo; entre 3500 y 4500 horas de estudio para el lector.

---

## 9. Datos editoriales provisionales

**Título de la colección:** Atlas Quant. Curso universitario de Finanzas Cuantitativas (provisional).

**Créditos (texto aprobado en principio; falta el nombre):**

> Dirección editorial, alcance y aprobación de contenidos: [nombre del director de la obra].
> Redacción con asistencia de inteligencia artificial (Claude, de Anthropic) bajo dicha dirección.

Cada libro incluirá en su prefacio una «Nota sobre la elaboración de esta obra» que describa el método de verificación, sus límites y la forma de reportar erratas.

**Licencia:** pendiente de decisión (todos los derechos reservados o una licencia Creative Commons, por ejemplo CC BY-NC-SA 4.0).

---

## 10. Método de producción

1. **Fase 1. Diseño editorial.** Entregas 1a (este plan, libro de estilo, notación, glosario), 1b a 1d (índices detallados) y 1e (bibliografía verificada y auditoría de coherencia).
2. **Fase 2. Composición y piloto.** Plan de prueba de composición, presentado para aprobación; capítulo piloto L1 c. 8 con texto, ejemplos, ejercicios, solucionario y código verificados; revisión crítica; ajuste del libro de estilo. Después, un piloto avanzado (L18 c. 6 o L16 c. 9) antes de autorizar la producción a escala.
3. **Fase 3. Producción secuencial,** capítulo por capítulo con aprobación individual durante la primera etapa, siguiendo el orden de lectura y priorizando las Series I y II.
4. **Fase 4. Integración y auditoría final.**

El procedimiento de revisión de cada capítulo está descrito en `LIBRO_DE_ESTILO.md`, sección 17.
