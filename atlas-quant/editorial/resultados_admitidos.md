# Registro de resultados admitidos

Versión 1.3 · Entrega 1d · 2026-10-16

Un resultado admitido es un enunciado que la obra usa antes de demostrarlo, o cuya demostración completa está fuera del alcance de la colección. Las reglas están en `LIBRO_DE_ESTILO.md`, sección 4. Todas las ubicaciones están confirmadas por los índices detallados de las entregas 1b, 1c y 1d. Las referencias externas se fijaron y verificaron en la entrega 1e: cada resultado de la última fila tiene al menos una entrada en `bibliografia/atlas.bib` cuyo campo `uso` lo cita (comprobación automática de `herramientas/bib_a_md.py`).

**Estados:** *previsto* (identificado en el diseño, ubicación por confirmar); *confirmado* (ubicaciones fijadas en los índices detallados); *cerrado en el diseño* (ya no es un resultado admitido porque el diseño incluye su demostración antes de usarlo); *en uso* (aparece en un capítulo redactado); *cerrado* (la demostración está redactada y verificada).

## Resultados usados en L1–L16 (continuación de la tabla en la sección siguiente)

| ID | Enunciado (resumen) | Se usa en | Se demuestra en | Estado |
|---|---|---|---|---|
| RA-01 | Existencia y unicidad de la raíz n-ésima positiva de un real positivo | L1 §8.3 | L1 §8.4\* (sección opcional) y de nuevo en L4 §3.7 | Cerrado en el diseño |
| RA-02 | Existencia, continuidad y monotonía de x ↦ aˣ para x real y a > 0; leyes de los exponentes reales | L1 §8.8, L1 §11.7, L2 §8.1, ejemplos de L4 c. 4–9 | L4 §10.4 | Confirmado |
| RA-03 | Existencia del logaritmo en base a como inversa de la exponencial | L1 §8.9, L1 §11.7, L2 §8.3 | L4 §10.4 | Confirmado |
| RA-04 | (1 + x/n)ⁿ → eˣ para todo x real | L2 §7.10, L2 c. 8 | L4 §10.6 | Confirmado |
| RA-05 | ln(1 + x) ≤ x para x > −1, y cota del error de la regla del 72 | L1 §8.10 (exploración numérica) | L4 §10.8 (desigualdad) y L4 §13.3 (cota) | Confirmado |
| RA-06 | Derivadas de exp y ln | Ejemplos de L4 c. 4–9 | L4 §10.7 | Confirmado |
| RA-07 | Teorema fundamental del álgebra | L6 §9.2 (y a través de él, L6 §10.1) | Fuera del alcance (requiere análisis complejo); referencia externa | Confirmado |
| RA-08 | Teorema de cambio de variables en integrales múltiples para transformaciones no lineales | L7 §10.5, L8 §8.2, L8 §13.4 | Caso lineal en L7 §10.5; caso general en L16 §5.5\* (sección opcional) | Confirmado |
| RA-09 | Una distribución queda determinada por su función característica (y por su función generadora de momentos cuando existe en un entorno de 0) | L8 §8.6 | L16 §8.4 | Confirmado |
| RA-22 | Medida de ángulos en radianes como longitud de arco y propiedades geométricas de seno y coseno (incluido el argumento de áreas para sen x / x → 1) | L2 c. 10, L4 §2.6, L4 §4.5 | L4 §9.8\* (longitud de arco) y L4 §13.7 (definición analítica y coherencia) | Confirmado |
| RA-23 | Regla de los signos de Descartes | L5 §6.3 | Referencia externa | Confirmado |
| RA-24 | Existencia de espacios de probabilidad que soportan variables con densidad dada y sucesiones de variables independientes con distribuciones dadas | L8 §1.2, L8 c. 5, L8 §10.1 y capítulos posteriores | L16 §1.7, L16 §5.6 y L16 §6.2 | Confirmado |
| RA-25 | Geometría euclídea elemental: teorema de Pitágoras y semejanza de triángulos | L2 §2.3, L2 c. 9, L2 c. 10, L6 §6.6 | Fuera del alcance (la colección no desarrolla axiomáticamente la geometría euclídea); referencia externa | Confirmado |
| RA-26 | Fórmula de la esperanza de una función de una variable aleatoria continua para funciones generales | L8 §6.2 | L16 §3.6 (caso discreto y funciones monótonas por tramos demostrados en L8 §6.2) | Confirmado |
| RA-27 | Cota de Berry-Esseen | L8 §11.5 | Referencia externa | Confirmado |
| RA-28 | Distribuciones estables y teorema central del límite generalizado | L8 §12.4\* | Referencia externa | Confirmado |
| RA-10 | Teorema de Riesz-Fischer: completitud de L² (y, con él, la completitud del sistema trigonométrico en L²) | L15 §6.5 | L16 §4.3 | Confirmado |
| RA-11 | Distribución asintótica del estadístico de Dickey-Fuller como funcional del movimiento browniano | L14 §6.4 | Fuera del alcance (requiere el teorema central del límite funcional); referencia externa; valores críticos obtenidos por simulación en el libro | Confirmado |
| RA-12 | Consistencia de los estimadores de varianza HAC (Newey-West) | L14 §2.5 | Referencia externa | Confirmado |
| RA-13 | Leyes de los grandes números y teorema central del límite para procesos estacionarios débilmente dependientes; teorema ergódico | L14 §4.5 y capítulos posteriores de L14 | Referencia externa | Confirmado |
| RA-14 | Consistencia y normalidad asintótica de la máxima verosimilitud bajo condiciones generales | L9 §4.5, L14 | Condiciones simplificadas en L9 §4.5; caso general: referencia externa | Confirmado |
| RA-19 | Teorema fundamental de valoración en tiempo discreto, caso general (Dalang-Morton-Willinger) | L16 §12.6 | Referencia externa; el caso finito se demuestra en L16 §12.4 | Confirmado |
| RA-29 | Distribución asintótica chi-cuadrado de la razón de verosimilitud en el caso multiparamétrico (teorema de Wilks) | L9 §6.5 | Caso de un parámetro demostrado en L9 §6.5; caso general: referencia externa | Confirmado |
| RA-30 | Consistencia del bootstrap no paramétrico para estadísticos suaves de la media | L9 §10.3 | Referencia externa | Confirmado |
| RA-31 | Distribución asintótica del estadístico de Kolmogorov-Smirnov | L9 §13.6 | Referencia externa (la distribución libre bajo la hipótesis nula se demuestra) | Confirmado |
| RA-32 | Densidad de la distribución de Wishart | L9 §13.1 | Referencia externa | Confirmado |
| RA-33 | APT asintótica (versiones de Ross y Huberman) | L10 §10.3 | Referencia externa; la APT exacta se demuestra en L10 §10.2 | Confirmado |
| RA-34 | Convergencia superlineal del método BFGS | L12 §6.4 | Referencia externa | Confirmado |
| RA-35 | Desigualdad de Koksma-Hlawka | L12 §10.2 | Referencia externa | Confirmado |
| RA-36 | Consistencia del bootstrap por bloques móviles y del bootstrap estacionario | L14 §7.5 | Referencia externa | Confirmado |
| RA-37 | Consistencia y normalidad asintótica de la cuasi máxima verosimilitud en modelos GARCH | L14 §8.4 | Referencia externa | Confirmado |
| RA-38 | Teorema de representación de Granger, caso general | L14 §10.2 | Caso bivariado demostrado en L14 §10.2; caso general: referencia externa | Confirmado |
| RA-39 | Distribución asintótica de los estadísticos de supremo para rupturas con fecha desconocida (Andrews) | L14 §11.3 | Referencia externa | Confirmado |
| RA-40 | Teoría asintótica del MGM bajo condiciones generales | L14 §13.3 | Condiciones simplificadas en L14 §13.3; caso general: referencia externa | Confirmado |
| RA-41 | Distribuciones asintóticas de estadísticos de diagnóstico y comparación: Ljung-Box, KPSS, Diebold-Mariano y prueba J | L14 §5.6, L14 §6.5, L14 §7.4, L14 §13.5 | Referencia externa | Confirmado |
| RA-42 | Teorema de equivalencia de Lax | L15 §9.4 | Referencia externa | Confirmado |
| RA-43 | Orden 4 del método de Runge-Kutta clásico | L15 §4.2 | Referencia externa; verificación simbólica como comprobación, no como demostración | Confirmado |
| RA-44 | Ejemplo de Tychonoff de no unicidad para la ecuación del calor en la recta | L15 §7.3 | Referencia externa | Confirmado |

## Resultados usados en L17–L23

| ID | Enunciado (resumen) | Se usa en | Se demuestra en | Estado |
|---|---|---|---|---|
| RA-15 | Teoremas de Fisher-Tippett-Gnedenko y de Pickands-Balkema-de Haan | L17 §8.2, L17 §8.4 | Caso de colas de tipo Pareto demostrado en L17 §8.2; caso general: referencia externa | Confirmado |
| RA-16 | Teorema de representación de martingalas brownianas (cierre de la demostración general) | L18 §10.2, L19 §2.6 | Representación de exponenciales estocásticas y densidad de su espacio generado en L18 §10.2; cierre general: referencia externa | Confirmado |
| RA-17 | Condición de Novikov | L18 §9.4, L19 §2.2 | Referencia externa | Confirmado |
| RA-18 | Existencia y unicidad fuerte de soluciones para EDE de raíz cuadrada (Yamada-Watanabe) | L18 §7.6, L19 §11.1, L22 §3.3 | Referencia externa | Confirmado |
| RA-20 | Caracterización de la opción americana en tiempo continuo como problema de parada óptima y de frontera libre | L19 §7.1, L19 §7.2 | Referencia externa; caso perpetuo demostrado en L19 §7.3 | Confirmado |
| RA-21 | Convergencia del descenso de gradiente estocástico | L21 §9.4 | Referencia externa | Confirmado |
| RA-45 | Consistencia del estimador de contracción de Ledoit-Wolf | L17 §2.2 | Intensidad óptima con parámetros conocidos demostrada en L17 §2.2; consistencia: referencia externa | Confirmado |
| RA-46 | Ley de Marchenko-Pastur | L17 §2.6\* | Referencia externa | Confirmado |
| RA-47 | El Expected Shortfall no es elicitable; el par (VaR, ES) es conjuntamente elicitable | L17 §6.6, L17 §10.5 | Referencia externa | Confirmado |
| RA-48 | Consistencia del estimador de Hill bajo variación regular | L17 §8.5 | Caso de colas Pareto exactas demostrado en L17 §8.5; caso general: referencia externa | Confirmado |
| RA-49 | Teorema de Donsker (principio de invariancia) | L18 §3.6 | Convergencia finito-dimensional demostrada en L18 §3.6; convergencia funcional: referencia externa | Confirmado |
| RA-50 | Propiedad de Markov de las soluciones de EDE con coeficientes de Lipschitz | L18 §7.7 | Referencia externa | Confirmado |
| RA-51 | Existencia de soluciones clásicas de la ecuación asociada a una difusión (regularidad de la esperanza) | L18 §8.3 | Referencia externa; la representación de Feynman-Kac (dirección inversa) se demuestra en L18 §8.2 | Confirmado |
| RA-52 | Orden débil 1 de Euler-Maruyama y orden fuerte 1 de Milstein | L18 §11.2, L18 §11.3 | Referencia externa; orden fuerte 1/2 de Euler-Maruyama demostrado en L18 §11.2 | Confirmado |
| RA-53 | Teoremas fundamentales de valoración en tiempo continuo (Delbaen-Schachermayer) | L19 §2.5 | Referencia externa; caso finito en L16 §12.4 | Confirmado |
| RA-54 | Convergencia del método de Longstaff-Schwartz | L19 §7.5 | Referencia externa | Confirmado |
| RA-55 | Condición de Feller para la positividad estricta del proceso de raíz cuadrada | L19 §11.1, L22 §3.3 | Referencia externa | Confirmado |
| RA-56 | Representación dual del precio de súper replicación en tiempo continuo | L19 §13.3 | Referencia externa; caso de un período en L10 §8.7 | Confirmado |
| RA-57 | Validez asintótica del *reality check* de White y de la prueba SPA de Hansen | L20 §6.3, L20 §6.4 | Referencia externa | Confirmado |
| RA-58 | Cotas de generalización basadas en la dimensión de Vapnik-Chervonenkis | L21 §1.5 | Referencia externa; cota para clases finitas demostrada en L21 §1.4 | Confirmado |
| RA-59 | Teorema de aproximación universal para redes neuronales | L21 §9.2 | Referencia externa | Confirmado |
| RA-60 | Convergencia de Metropolis-Hastings en espacios generales | L21 §11.3 | Referencia externa; caso finito demostrado en L21 §11.3 con L8 §14.6 | Confirmado |

## Resumen

| Categoría | Resultados |
|---|---|
| Cerrados en el diseño: la obra los demuestra antes de usarlos | RA-01 |
| Demostrados más adelante en la obra, en un lugar identificado | RA-02 a RA-06, RA-08 a RA-10, RA-22, RA-24, RA-26 |
| Admitidos con referencia externa, total o parcialmente (con la versión accesible demostrada cuando existe) | RA-07, RA-11 a RA-21, RA-23, RA-25, RA-27 a RA-60 |

Las referencias externas se fijaron y verificaron en la entrega 1e: cada resultado de la última fila tiene al menos una entrada en `bibliografia/atlas.bib` cuyo campo `uso` lo cita (comprobación automática de `herramientas/bib_a_md.py`).
