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
