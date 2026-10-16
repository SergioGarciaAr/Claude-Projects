# Mapa de dependencias por capítulo

Generado automáticamente por `herramientas/verificar_indices.py` a partir de los índices detallados. No editar a mano.

Cada fila indica los capítulos de los que depende un capítulo (a nivel de capítulo, aunque el índice cite secciones). Las dependencias marcadas «(aplic.)» solo aportan ejemplos o aplicaciones.

## L1

Requisitos declarados en el plan: ninguno.

| Capítulo | Depende de |
|---|---|
| 1. Qué es una afirmación matemática | — |
| 2. Lógica proposicional y cuantificadores | L1 c. 1 |
| 3. Conjuntos, relaciones y funciones | L1 c. 2 |
| 4. Métodos de demostración | L1 c. 2, L1 c. 3 |
| 5. Números naturales y enteros | L1 c. 3, L1 c. 4 |
| 6. Números racionales | L1 c. 3, L1 c. 5 |
| 7. Números reales | L1 c. 3, L1 c. 4, L1 c. 6 |
| 8. Potencias, raíces y logaritmos (capítulo piloto) | L1 c. 4, L1 c. 6, L1 c. 7 |
| 9. Magnitudes, unidades, órdenes de magnitud y error | L1 c. 7, L1 c. 8 |
| 10. Polinomios | L1 c. 5, L1 c. 7, L1 c. 8 |
| 11. Ecuaciones e inecuaciones | L1 c. 7, L1 c. 8, L1 c. 10 |
| 12. Sistemas de ecuaciones | L1 c. 3, L1 c. 11 |
| 13. Modelización algebraica | L1 c. 9, L1 c. 11, L1 c. 12 |
| 14. Algoritmos y primeros programas en Python | L1 c. 5, L1 c. 8, L1 c. 9, L1 c. 11 |

## L2

Requisitos declarados en el plan: L1.

| Capítulo | Depende de |
|---|---|
| 1. El concepto de función | L1 c. 3, L1 c. 7 |
| 2. Funciones lineales y afines | L1 c. 12, L2 c. 1 |
| 3. Funciones cuadráticas y polinómicas | L1 c. 10, L1 c. 11, L2 c. 2 |
| 4. Funciones racionales y asíntotas | L1 c. 10, L1 c. 11, L2 c. 3 |
| 5. Transformaciones y simetrías | L2 c. 1, L2 c. 3 |
| 6. Sucesiones y sumas | L1 c. 4, L1 c. 10, L2 c. 1 |
| 7. Convergencia de sucesiones y el número *e* | L1 c. 2, L1 c. 7, L1 c. 8, L1 c. 10, L2 c. 6 |
| 8. Funciones exponenciales y logarítmicas | L1 c. 8, L2 c. 1, L2 c. 5, L2 c. 7 |
| 9. Geometría analítica del plano y cónicas | L1 c. 11, L2 c. 2, L2 c. 3 |
| 10. Trigonometría y funciones periódicas | L2 c. 5, L2 c. 9 |
| 11. Vectores en el plano y en el espacio | L1 c. 3, L2 c. 9, L2 c. 10 |
| 12. Números complejos | L1 c. 11, L2 c. 10, L2 c. 11 |
| 13. Exploración gráfica y numérica de funciones con Python | L1 c. 14, L2 c. 1, L2 c. 7, L2 c. 8 |

## L3

Requisitos declarados en el plan: L1, L2.

| Capítulo | Depende de |
|---|---|
| 1. Programas, intérpretes y entornos | L1 c. 14 |
| 2. Tipos, expresiones y aritmética de punto flotante | L1 c. 9, L3 c. 1 |
| 3. Control de flujo, funciones y recursión | L1 c. 2, L1 c. 4, L3 c. 2 |
| 4. Estructuras de datos | L1 c. 3, L3 c. 3 |
| 5. Corrección y complejidad de algoritmos | L1 c. 4, L2 c. 8, L3 c. 4 |
| 6. Errores, pruebas y depuración | L3 c. 5 |
| 7. Clases y objetos con fines científicos | L1 c. 8, L3 c. 6 |
| 8. Cálculo vectorial con NumPy | L2 c. 11, L3 c. 5 |
| 9. Series temporales y datos tabulares con pandas | L2 c. 8, L3 c. 8 |
| 10. Visualización científica honesta | L2 c. 13, L3 c. 9 |
| 11. Números pseudoaleatorios y reproducibilidad | L1 c. 5, L3 c. 8 |
| 12. Organización de un trabajo computacional reproducible | L3 c. 6, L3 c. 9, L3 c. 11 |

## L4

Requisitos declarados en el plan: L2, L3.

| Capítulo | Depende de |
|---|---|
| 1. Completitud y sucesiones | L1 c. 7, L2 c. 7 |
| 2. Límites de funciones | L1 c. 2, L2 c. 1, L2 c. 4, L2 c. 10, L4 c. 1 |
| 3. Continuidad | L4 c. 1, L4 c. 2 |
| 4. La derivada | L4 c. 2, L4 c. 3 |
| 5. Regla de la cadena, derivación implícita y derivada de la inversa | L4 c. 3, L4 c. 4 |
| 6. Teorema del valor medio y consecuencias | L4 c. 3, L4 c. 5 |
| 7. Optimización y método de Newton | L3 c. 3, L4 c. 6 |
| 8. La integral de Riemann | L4 c. 1, L4 c. 3 |
| 9. Teorema fundamental del cálculo y técnicas de integración | L1 c. 10, L4 c. 5, L4 c. 6, L4 c. 8 |
| 10. Construcción rigurosa del logaritmo y la exponencial | L1 c. 8, L2 c. 7, L4 c. 1, L4 c. 3, L4 c. 5, L4 c. 6, L4 c. 9 |
| 11. Integrales impropias y función Gamma | L4 c. 9, L4 c. 10 |
| 12. Series numéricas | L2 c. 7, L4 c. 1, L4 c. 11 |
| 13. Series de potencias y teorema de Taylor | L2 c. 12, L4 c. 6, L4 c. 9, L4 c. 10, L4 c. 12 |
| 14. Derivación e integración numéricas | L3 c. 2, L3 c. 8, L4 c. 8, L4 c. 13 |

## L5

Requisitos declarados en el plan: L3, L4.

| Capítulo | Depende de |
|---|---|
| 1. Valor temporal del dinero; interés simple y compuesto | L1 c. 6, L1 c. 8, L2 c. 6, L2 c. 8, L4 c. 3 |
| 2. Tasas nominales, efectivas, equivalentes y continuas | L4 c. 9, L4 c. 10, L5 c. 1 |
| 3. Ecuación de valor y descuento | L4 c. 3, L5 c. 2 |
| 4. Anualidades y perpetuidades | L2 c. 6, L4 c. 3, L4 c. 11, L4 c. 12, L5 c. 3 |
| 5. Sistemas de amortización | L3 c. 4, L5 c. 4 |
| 6. Valor presente neto y tasa interna de retorno | L1 c. 10, L4 c. 3, L4 c. 6, L4 c. 7, L5 c. 3, L5 c. 4 |
| 7. Inflación y tasas reales | L5 c. 2 |
| 8. Bonos | L5 c. 2, L5 c. 4, L5 c. 6 |
| 9. Duración y convexidad | L4 c. 4, L4 c. 13, L4 c. 14, L5 c. 8 |
| 10. Estructura temporal de tasas | L2 c. 2, L4 c. 10, L5 c. 8, L5 c. 9 |
| 11. Implementación y verificación computacional | L3 c. 6, L3 c. 7, L3 c. 9, L5 c. 10 |

## L6

Requisitos declarados en el plan: L2, L3.

| Capítulo | Depende de |
|---|---|
| 1. Sistemas lineales y eliminación gaussiana | L1 c. 12, L2 c. 11, L3 c. 5 |
| 2. Matrices, inversas y factorización LU | L6 c. 1 |
| 3. Espacios vectoriales y subespacios | L1 c. 3, L6 c. 2 |
| 4. Independencia lineal, bases y dimensión | L6 c. 3 |
| 5. Transformaciones lineales | L6 c. 4 |
| 6. Determinantes | L1 c. 3, L6 c. 5 |
| 7. Producto interno, Gram-Schmidt y factorización QR | L2 c. 11, L6 c. 4 |
| 8. Proyecciones ortogonales y mínimos cuadrados | L6 c. 7 |
| 9. Valores propios, diagonalización y forma de Jordan | L2 c. 12, L6 c. 6 |
| 10. Teorema espectral y formas cuadráticas | L6 c. 7, L6 c. 9 |
| 11. Descomposición en valores singulares y componentes principales | L5 c. 10 (aplic.), L6 c. 8, L6 c. 10 |
| 12. Álgebra lineal numérica | L1 c. 9, L3 c. 2, L3 c. 8, L6 c. 2, L6 c. 7, L6 c. 10, L6 c. 11 |
| 13. Aplicaciones a mercados de escenarios y carteras | L5 c. 9 (aplic.), L5 c. 10 (aplic.), L6 c. 5, L6 c. 8, L6 c. 10, L6 c. 12 |

## L7

Requisitos declarados en el plan: L4, L6.

| Capítulo | Depende de |
|---|---|
| 1. Topología de ℝⁿ | L4 c. 1, L6 c. 7, L6 c. 12 |
| 2. Límites y continuidad | L4 c. 2, L4 c. 3, L7 c. 1 |
| 3. Diferenciabilidad | L4 c. 4, L5 c. 10 (aplic.), L6 c. 5, L7 c. 2 |
| 4. Regla de la cadena | L4 c. 6, L7 c. 3 |
| 5. Teorema de Taylor y matriz hessiana | L4 c. 13, L6 c. 10, L7 c. 4 |
| 6. Optimización sin restricciones | L6 c. 8, L7 c. 2, L7 c. 5 |
| 7. Convexidad, separación y lema de Farkas | L4 c. 6, L6 c. 7, L6 c. 10, L7 c. 1, L7 c. 6 |
| 8. Funciones inversa e implícita; multiplicadores de Lagrange | L6 c. 5, L7 c. 1, L7 c. 2, L7 c. 4 |
| 9. Condiciones de Karush-Kuhn-Tucker y dualidad | L7 c. 7, L7 c. 8 |
| 10. Integrales múltiples | L4 c. 8, L4 c. 9, L4 c. 11, L6 c. 6, L7 c. 2 |
| 11. Optimización cuadrática y utilidad determinista | L6 c. 10, L7 c. 8, L7 c. 9 |

## L8

Requisitos declarados en el plan: L3, L4, L6, L7.

| Capítulo | Depende de |
|---|---|
| 1. Espacios de probabilidad | L1 c. 3, L4 c. 12 |
| 2. Combinatoria | L1 c. 10, L8 c. 1 |
| 3. Probabilidad condicional, independencia y teorema de Bayes | L8 c. 1, L8 c. 2 |
| 4. Variables aleatorias discretas | L4 c. 10, L4 c. 12, L8 c. 3 |
| 5. Variables aleatorias continuas | L4 c. 9, L4 c. 11, L7 c. 10, L8 c. 4 |
| 6. Esperanza, momentos y desigualdades | L4 c. 6, L8 c. 4, L8 c. 5 |
| 7. Vectores aleatorios | L6 c. 10, L6 c. 12, L7 c. 10, L8 c. 6 |
| 8. Transformaciones, funciones generadoras y funciones características | L4 c. 13, L7 c. 10, L8 c. 7 |
| 9. Esperanza condicional elemental | L8 c. 3, L8 c. 7 |
| 10. Modos de convergencia, leyes débiles y concentración | L4 c. 1, L8 c. 6, L8 c. 7, L8 c. 8 |
| 11. Teorema central del límite | L4 c. 13, L8 c. 5, L8 c. 10 |
| 12. Colas pesadas y dependencia más allá de la correlación | L8 c. 7, L8 c. 8, L8 c. 11 |
| 13. Simulación y método Monte Carlo | L3 c. 11, L8 c. 7, L8 c. 10, L8 c. 11 |
| 14. Paseos aleatorios y cadenas de Markov finitas | L6 c. 9, L7 c. 1, L8 c. 3, L8 c. 9, L8 c. 10 |

## L9

Requisitos declarados en el plan: L3, L6, L7, L8.

| Capítulo | Depende de |
|---|---|
| 1. Datos, muestras y estadística descriptiva de rendimientos | L2 c. 8, L3 c. 9, L3 c. 10, L5 c. 2 (aplic.), L8 c. 6, L8 c. 7 |
| 2. Estimadores | L8 c. 10, L9 c. 1 |
| 3. Distribuciones muestrales | L6 c. 7, L6 c. 10, L8 c. 7, L8 c. 8, L9 c. 2 |
| 4. Método de los momentos y máxima verosimilitud | L7 c. 5, L7 c. 6, L8 c. 10, L8 c. 11, L9 c. 3 |
| 5. Intervalos de confianza | L9 c. 4 |
| 6. Contrastes de hipótesis | L9 c. 5 |
| 7. Pruebas múltiples | L8 c. 3, L9 c. 6 |
| 8. Regresión lineal y teorema de Gauss-Markov | L6 c. 8, L8 c. 9, L9 c. 3 |
| 9. Inferencia y diagnóstico en regresión | L9 c. 4, L9 c. 6, L9 c. 8 |
| 10. Bootstrap y remuestreo | L3 c. 11, L8 c. 13, L9 c. 5 |
| 11. Inferencia bayesiana introductoria | L8 c. 3, L8 c. 9, L9 c. 4 |
| 12. Validación y sobreajuste | L9 c. 7, L9 c. 8 |
| 13. Estadística multivariante, no paramétrica y robusta | L6 c. 11, L8 c. 7, L9 c. 4, L9 c. 6 |
| 14. El problema de estimar rendimientos esperados | L9 c. 5, L9 c. 10, L9 c. 11, L9 c. 13 |

## L10

Requisitos declarados en el plan: L5, L6, L7, L8, L9.

| Capítulo | Depende de |
|---|---|
| 1. Sistema financiero e intermediarios | L5 c. 1 |
| 2. Instrumentos financieros | L5 c. 8, L10 c. 1 |
| 3. Mecanismos de negociación y liquidez | L10 c. 2 |
| 4. Rendimientos | L2 c. 8, L8 c. 6, L8 c. 7, L9 c. 1, L10 c. 2 |
| 5. Utilidad esperada y aversión al riesgo | L4 c. 6, L4 c. 13, L7 c. 6, L8 c. 6, L8 c. 8 |
| 6. Teoría de carteras de Markowitz | L7 c. 11, L8 c. 7, L10 c. 4, L10 c. 5 |
| 7. CAPM | L9 c. 8, L9 c. 9, L10 c. 6 |
| 8. Arbitraje en un período | L6 c. 13, L7 c. 7, L7 c. 9, L8 c. 1 |
| 9. Factor de descuento estocástico | L6 c. 7, L8 c. 9, L10 c. 5, L10 c. 8 |
| 10. APT y modelos de factores | L6 c. 11, L9 c. 8, L9 c. 13, L10 c. 7, L10 c. 9 |
| 11. Eficiencia de mercado y anomalías | L8 c. 9, L8 c. 14, L9 c. 6, L9 c. 7, L10 c. 7, L10 c. 10 |
| 12. Fricciones y límites al arbitraje | L10 c. 3, L10 c. 8 |
| 13. Estados contables y valoración por flujos descontados | L4 c. 12, L5 c. 4, L5 c. 6, L10 c. 2, L10 c. 7 |

## L11

Requisitos declarados en el plan: L4, L6, L7.

| Capítulo | Depende de |
|---|---|
| 1. Construcción de los números reales | L1 c. 3, L1 c. 6, L1 c. 7, L4 c. 1 |
| 2. Espacios métricos, compacidad y conexión | L1 c. 3, L7 c. 1 |
| 3. Espacios completos y teorema del punto fijo de Banach | L4 c. 1, L11 c. 2 |
| 4. Continuidad y continuidad uniforme | L4 c. 3, L11 c. 2 |
| 5. Diferenciabilidad rigurosa | L7 c. 3, L7 c. 8, L11 c. 3, L11 c. 4 |
| 6. Integral de Riemann-Stieltjes y variación acotada | L4 c. 8, L4 c. 9, L11 c. 4 |
| 7. Convergencia uniforme e intercambio de límites | L4 c. 13, L11 c. 3, L11 c. 6 |
| 8. Espacios normados y con producto interno | L6 c. 7, L11 c. 3, L11 c. 7 |
| 9. Funciones convexas y desigualdades | L4 c. 6, L7 c. 7, L11 c. 8 |
| 10. Variación cuadrática de funciones deterministas | L4 c. 6, L7 c. 5, L11 c. 6, L11 c. 7 |

## L12

Requisitos declarados en el plan: L3, L4, L6, L7, L8.

| Capítulo | Depende de |
|---|---|
| 1. Condicionamiento y estabilidad | L3 c. 2, L4 c. 14, L6 c. 12 |
| 2. Ecuaciones no lineales | L4 c. 3, L4 c. 7, L5 c. 6 (aplic.), L5 c. 8 (aplic.), L7 c. 3, L12 c. 1 |
| 3. Sistemas lineales numéricos | L6 c. 12, L12 c. 1 |
| 4. Interpolación y *splines* | L1 c. 10, L4 c. 13, L5 c. 10 (aplic.), L12 c. 3 |
| 5. Derivación e integración numéricas | L4 c. 14, L12 c. 4 |
| 6. Optimización sin restricciones | L7 c. 6, L7 c. 7, L12 c. 2 |
| 7. Optimización convexa | L7 c. 9, L10 c. 6 (aplic.), L12 c. 6 |
| 8. Calibración por mínimos cuadrados no lineales | L5 c. 10 (aplic.), L6 c. 8, L6 c. 11, L12 c. 6 |
| 9. Monte Carlo y reducción de varianza | L8 c. 9, L8 c. 11, L8 c. 13, L12 c. 5 |
| 10. Cuasi-Monte Carlo | L12 c. 5, L12 c. 9 |
| 11. Programación dinámica y parada óptima en tiempo discreto | L7 c. 6, L7 c. 8, L8 c. 9, L8 c. 14 |
| 12. Transformada discreta de Fourier y FFT | L2 c. 12, L3 c. 5, L4 c. 13, L6 c. 7 |

## L13

Requisitos declarados en el plan: L3, L5, L8, L10, L12.

| Capítulo | Depende de |
|---|---|
| 1. Contratos a plazo y futuros | L5 c. 2, L5 c. 10, L8 c. 7, L10 c. 2, L10 c. 8 |
| 2. Swaps | L5 c. 10, L13 c. 1 |
| 3. Opciones: cotas de arbitraje y paridad put-call | L2 c. 1, L10 c. 8, L13 c. 1 |
| 4. Modelo binomial de un período | L10 c. 8, L13 c. 3 |
| 5. Modelo binomial de varios períodos y martingalas discretas | L3 c. 6, L8 c. 2, L8 c. 9, L8 c. 14, L13 c. 4 |
| 6. Opciones americanas como problema de parada óptima | L12 c. 11, L13 c. 5 |
| 7. Cobertura en tiempo discreto | L8 c. 7, L8 c. 9, L13 c. 5 |
| 8. Convergencia del modelo de Cox-Ross-Rubinstein a la fórmula de Black-Scholes | L4 c. 10, L8 c. 11, L13 c. 3, L13 c. 5 |
| 9. Opciones exóticas en árboles y límites del modelo | L12 c. 9, L13 c. 6, L13 c. 8 |

## L14

Requisitos declarados en el plan: L3, L6, L9, L10, L12.

| Capítulo | Depende de |
|---|---|
| 1. Hechos estilizados de los rendimientos financieros | L3 c. 9, L9 c. 1, L9 c. 13, L10 c. 4 |
| 2. Regresión matricial, mínimos cuadrados generalizados y errores HAC | L6 c. 10, L9 c. 8, L9 c. 9 |
| 3. Endogeneidad, variables instrumentales y causalidad | L14 c. 2 |
| 4. Procesos estocásticos en tiempo discreto | L2 c. 12, L6 c. 9, L8 c. 10, L9 c. 2 |
| 5. Modelos ARMA | L9 c. 4, L9 c. 12, L14 c. 4 |
| 6. Raíces unitarias y regresiones espurias | L12 c. 9, L14 c. 5 |
| 7. Pronóstico, validación temporal y bootstrap para datos dependientes | L8 c. 9, L9 c. 10, L9 c. 12, L14 c. 5 |
| 8. Volatilidad condicional: ARCH y GARCH | L9 c. 4, L12 c. 6, L14 c. 5 |
| 9. Vectores autorregresivos y causalidad de Granger | L6 c. 9, L14 c. 5 |
| 10. Cointegración | L14 c. 6, L14 c. 9 |
| 11. Rupturas estructurales y cambios de régimen | L8 c. 3, L8 c. 14, L12 c. 6, L14 c. 5 |
| 12. Regresiones de corte transversal y procedimiento de Fama-MacBeth | L10 c. 7, L10 c. 10, L14 c. 2 |
| 13. Método generalizado de momentos | L9 c. 4, L12 c. 6, L14 c. 2 |
| 14. Contraste de modelos de valoración de activos | L9 c. 3, L10 c. 9, L14 c. 12, L14 c. 13 |
| 15. Modelos de espacio de estados y filtro de Kalman | L8 c. 9, L9 c. 4, L12 c. 6, L14 c. 4 |

## L15

Requisitos declarados en el plan: L6, L7, L11, L12.

| Capítulo | Depende de |
|---|---|
| 1. Ecuaciones de primer orden: existencia, unicidad y desigualdad de Gronwall | L4 c. 9, L4 c. 10, L11 c. 3, L11 c. 7 |
| 2. Sistemas lineales, exponencial de matrices y ecuaciones de Riccati | L4 c. 12, L6 c. 9, L6 c. 12, L11 c. 7, L15 c. 1 |
| 3. Estabilidad y comportamiento cualitativo | L7 c. 5, L15 c. 2 |
| 4. Métodos numéricos para ecuaciones ordinarias | L4 c. 13, L12 c. 1, L15 c. 1 |
| 5. La ecuación del calor y la separación de variables | L4 c. 13, L7 c. 5, L11 c. 7, L15 c. 2 |
| 6. Series y transformada de Fourier | L4 c. 11, L11 c. 7, L11 c. 8, L15 c. 5 |
| 7. Ecuaciones parabólicas: principio del máximo | L7 c. 6, L15 c. 5, L15 c. 6 |
| 8. Reducción de la ecuación de Black-Scholes a la ecuación del calor | L7 c. 4, L15 c. 6, L15 c. 7 |
| 9. Diferencias finitas para ecuaciones parabólicas | L12 c. 3, L15 c. 4, L15 c. 5, L15 c. 7, L15 c. 8 |

## L16

Requisitos declarados en el plan: L8, L11.

| Capítulo | Depende de |
|---|---|
| 1. σ-álgebras, medidas y teorema de extensión de Carathéodory | L4 c. 12, L8 c. 1, L11 c. 2 |
| 2. Funciones medibles y variables aleatorias | L8 c. 5, L16 c. 1 |
| 3. Integral de Lebesgue | L4 c. 8, L16 c. 2 |
| 4. Espacios L^p | L11 c. 8, L11 c. 9, L16 c. 3 |
| 5. Medida producto y teorema de Fubini-Tonelli | L7 c. 10, L16 c. 1, L16 c. 3 |
| 6. Independencia, lemas de Borel-Cantelli y ley 0-1 | L16 c. 2, L16 c. 5 |
| 7. Modos de convergencia y ley fuerte de los grandes números | L16 c. 4, L16 c. 6 |
| 8. Convergencia en distribución y funciones características | L8 c. 8, L8 c. 11, L11 c. 7, L16 c. 5, L16 c. 7 |
| 9. Esperanza condicional y teorema de Radon-Nikodym | L8 c. 9, L16 c. 4, L16 c. 5 |
| 10. Martingalas en tiempo discreto y tiempos de parada | L8 c. 9, L8 c. 14, L16 c. 9 |
| 11. Convergencia de martingalas y desigualdades de Doob | L16 c. 7, L16 c. 10 |
| 12. Cambio de medida y teorema fundamental de valoración en tiempo discreto | L7 c. 7, L10 c. 8 (aplic.), L13 c. 5 (aplic.), L16 c. 9, L16 c. 10 |

## L17

Requisitos declarados en el plan: L9, L10, L12, L14.

| Capítulo | Depende de |
|---|---|
| 1. Error de estimación de los insumos | L7 c. 4, L9 c. 13, L9 c. 14, L10 c. 6 |
| 2. Inestabilidad de la optimización media-varianza y estimadores de contracción | L9 c. 13, L9 c. 14, L12 c. 7, L17 c. 1 |
| 3. Modelo de Black-Litterman | L8 c. 9, L9 c. 11, L10 c. 7, L17 c. 2 |
| 4. Paridad de riesgo y contribuciones al riesgo | L7 c. 4, L10 c. 6, L12 c. 7 |
| 5. Modelos de factores de riesgo | L9 c. 13, L10 c. 10, L14 c. 12 |
| 6. Medidas de riesgo coherentes | L7 c. 7, L8 c. 5, L8 c. 6 |
| 7. Estimación del VaR y del Expected Shortfall | L8 c. 11, L9 c. 13, L12 c. 9, L14 c. 8, L17 c. 6 |
| 8. Teoría de valores extremos | L8 c. 10, L8 c. 12, L9 c. 4, L16 c. 8 (aplic.), L17 c. 7 |
| 9. Cópulas | L8 c. 7, L8 c. 12, L9 c. 4 |
| 10. Backtesting de modelos de riesgo | L8 c. 14, L9 c. 6, L17 c. 7 |
| 11. Escenarios y pruebas de estrés | L8 c. 9, L17 c. 5, L17 c. 7 |
| 12. Riesgo de liquidez y riesgo de modelo | L10 c. 3, L10 c. 12, L17 c. 7 |
| 13. Rebalanceo | L10 c. 4, L12 c. 11, L17 c. 2 |

## L18

Requisitos declarados en el plan: L7, L11, L12, L15, L16.

| Capítulo | Depende de |
|---|---|
| 1. Cadenas de Markov en espacios numerables y en tiempo continuo | L8 c. 14, L15 c. 2, L16 c. 10 |
| 2. Procesos de Poisson, procesos con saltos y cambio de variables con saltos | L8 c. 5, L11 c. 6, L16 c. 6, L18 c. 1 |
| 3. Movimiento browniano | L8 c. 7, L11 c. 10, L16 c. 6, L16 c. 8 |
| 4. Martingalas en tiempo continuo y principio de reflexión | L16 c. 10, L16 c. 11, L18 c. 3 |
| 5. La integral de Itô | L11 c. 10, L16 c. 4, L18 c. 3, L18 c. 4 |
| 6. Fórmula de Itô | L7 c. 5, L11 c. 10, L18 c. 5 |
| 7. Ecuaciones diferenciales estocásticas | L15 c. 1, L18 c. 6 |
| 8. Generador infinitesimal, Feynman-Kac y ecuaciones de Kolmogorov | L15 c. 5, L15 c. 7, L18 c. 7 |
| 9. Teorema de Girsanov | L16 c. 9, L16 c. 12, L18 c. 6 |
| 10. Representación de martingalas | L18 c. 5, L18 c. 9 |
| 11. Simulación de ecuaciones diferenciales estocásticas | L12 c. 9, L15 c. 4, L18 c. 7 |

## L19

Requisitos declarados en el plan: L9, L12, L13, L15, L16, L18.

| Capítulo | Depende de |
|---|---|
| 1. El mercado de Black-Scholes y las estrategias autofinanciadas | L13 c. 5, L18 c. 6, L18 c. 7 |
| 2. Replicación y valoración neutral al riesgo | L15 c. 8, L18 c. 8, L18 c. 9, L18 c. 10, L19 c. 1 |
| 3. Fórmula de Black-Scholes-Merton y extensiones | L8 c. 5, L13 c. 8, L19 c. 2 |
| 4. Cambio de numerario | L16 c. 12, L18 c. 9, L19 c. 2 |
| 5. Griegas y cobertura | L13 c. 7, L19 c. 3 |
| 6. Volatilidad implícita | L12 c. 2, L13 c. 3, L19 c. 3 |
| 7. Opciones americanas como problema de frontera libre | L9 c. 8, L13 c. 6, L16 c. 10, L19 c. 2 |
| 8. Opciones exóticas | L18 c. 4, L19 c. 3 |
| 9. Métodos numéricos de valoración | L12 c. 9, L12 c. 12, L15 c. 9, L16 c. 8, L19 c. 3 |
| 10. Volatilidad local | L18 c. 8, L19 c. 6 |
| 11. Modelos de Heston y de Merton con saltos | L15 c. 2, L18 c. 2, L18 c. 7, L19 c. 9 |
| 12. Calibración y riesgo de modelo | L9 c. 4, L12 c. 8, L19 c. 11 |
| 13. Mercados incompletos | L13 c. 7, L16 c. 12, L19 c. 11 |

## L20

Requisitos declarados en el plan: L9, L10, L12, L14, L17.

| Capítulo | Depende de |
|---|---|
| 1. El método científico aplicado a las finanzas | L9 c. 6, L9 c. 7, L10 c. 11 |
| 2. Datos financieros | L3 c. 12, L10 c. 2, L10 c. 13, L20 c. 1 |
| 3. Señales y carteras de investigación | L9 c. 13, L14 c. 12, L17 c. 5, L20 c. 2 |
| 4. Estudios de eventos | L9 c. 8, L14 c. 2, L20 c. 2 |
| 5. Diseño de backtests | L10 c. 3, L17 c. 12, L20 c. 3 |
| 6. Sobreajuste y pruebas múltiples en backtests | L9 c. 7, L14 c. 7, L20 c. 5 |
| 7. Validación progresiva, purga y embargo | L9 c. 12, L14 c. 7, L20 c. 6 |
| 8. Evaluación del desempeño | L9 c. 4, L10 c. 10, L14 c. 2, L20 c. 6 |
| 9. Microestructura del mercado | L7 c. 6, L8 c. 3, L8 c. 9, L10 c. 3, L20 c. 2 |
| 10. Impacto de mercado y ejecución óptima | L7 c. 11, L12 c. 11, L15 c. 2 (aplic.), L17 c. 12, L20 c. 9 |
| 11. Riesgo operativo de los sistemas cuantitativos | L3 c. 12, L20 c. 5 |
| 12. Reproducibilidad y comunicación de resultados | L3 c. 12, L20 c. 5, L20 c. 8 |

## L21

Requisitos declarados en el plan: L6, L7, L9, L12, L14, L20.

| Capítulo | Depende de |
|---|---|
| 1. Riesgo, sesgo-varianza y generalización | L8 c. 10, L9 c. 12 |
| 2. Regularización: ridge, lasso y red elástica | L6 c. 11, L9 c. 11, L12 c. 7, L21 c. 1 |
| 3. Validación con datos dependientes | L14 c. 7, L20 c. 7, L21 c. 2 |
| 4. Clasificación y calibración | L9 c. 4, L12 c. 6, L21 c. 1 |
| 5. Árboles de decisión | L21 c. 1, L21 c. 4 |
| 6. Ensambles y *boosting* | L12 c. 6, L21 c. 5 |
| 7. Métodos de núcleo (\*) | L6 c. 10, L7 c. 9, L21 c. 2 |
| 8. Aprendizaje no supervisado | L6 c. 11, L9 c. 13, L21 c. 1 |
| 9. Fundamentos de redes neuronales | L7 c. 4, L12 c. 6, L21 c. 1 |
| 10. Interpretabilidad y estabilidad | L21 c. 6, L21 c. 9 |
| 11. Métodos bayesianos y MCMC | L8 c. 14, L9 c. 11, L12 c. 9, L21 c. 2 |
| 12. Aplicaciones con escepticismo metodológico | L20 c. 8, L21 c. 3, L21 c. 6 |
| 13. Replicación crítica de un artículo | L20 c. 12, L21 c. 12 |

## L22

Requisitos declarados en el plan: L5, L12, L13, L17, L18, L19.

| Capítulo | Depende de |
|---|---|
| 1. Instrumentos de tasa de interés | L5 c. 10, L13 c. 2 |
| 2. Construcción de curvas en la práctica | L12 c. 4, L12 c. 8, L22 c. 1 |
| 3. Modelos de tasa corta y estructura afín | L15 c. 2, L18 c. 7, L18 c. 8, L19 c. 4 |
| 4. Marco de Heath-Jarrow-Morton | L18 c. 9, L22 c. 3 |
| 5. Medidas forward, fórmula de Black y modelo de mercado | L19 c. 4, L22 c. 4 |
| 6. Modelo estructural de Merton | L5 c. 8, L19 c. 3, L19 c. 8 |
| 7. Modelos de intensidad | L18 c. 2, L22 c. 3 |
| 8. Swaps de incumplimiento crediticio | L22 c. 7 |
| 9. Riesgo de crédito de cartera | L8 c. 11, L17 c. 9, L22 c. 7 |
| 10. Riesgo de contraparte y CVA | L19 c. 9, L22 c. 8 |

## L23

Requisitos declarados en el plan: L9, L14, L17, L20, L21.

| Capítulo | Depende de |
|---|---|
| 1. Cómo leer un artículo académico | L9 c. 6, L20 c. 1 |
| 2. Caso: factores al estilo Fama-French | L14 c. 12, L17 c. 5, L20 c. 3, L23 c. 1 |
| 3. Caso: *momentum* según Jegadeesh-Titman | L20 c. 3, L20 c. 5, L20 c. 8, L23 c. 1 |
| 4. Caso: volatilidad y VaR de una cartera | L14 c. 8, L17 c. 7, L17 c. 10, L23 c. 1 |
| 5. Caso: valoración y cobertura de opciones con datos reales | L9 c. 4, L19 c. 5 (aplic.), L19 c. 6 (aplic.), L23 c. 1 |
| 6. Caso: aprendizaje automático sin fuga de información | L20 c. 7, L21 c. 3, L21 c. 12, L23 c. 1 |
| 7. Diseño de una investigación original | L20 c. 1, L23 c. 6 |
| 8. Redacción y defensa del informe | L20 c. 12, L23 c. 7 |
| 9. Rutas de especialización | L23 c. 8 |
