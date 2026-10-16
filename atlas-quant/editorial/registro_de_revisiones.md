# Registro de revisiones

Registro de hallazgos, su severidad y su resolución. Severidades definidas en `LIBRO_DE_ESTILO.md`, sección 17.

## Revisión R-0001 · Auditoría de prerrequisitos y cobertura del plan · 2026-10-15

Auditoría del plan editorial previa a la Fase 1, realizada razonando sobre los índices por capítulo (sin herramientas automáticas). Aprobada por la dirección editorial.

### Hallazgos críticos

| ID | Hallazgo | Resolución | Estado |
|---|---|---|---|
| C-01 | L2 definía *e* como límite sin fundamento de completitud; el capítulo de exponenciales precedía al de convergencia | Axioma del supremo en L1 c. 7; teorema del binomio en L1 c. 10; L2 reordenado (sucesiones c. 6, convergencia y *e* c. 7, exponenciales c. 8) | Resuelto en el plan |
| C-02 | L4 construía la exponencial en c. 6, antes de la integral, sin método definido y con riesgo de circularidad | Construcción trasladada a L4 c. 10, mediante ln x = ∫₁ˣ dt/t | Resuelto en el plan |
| C-03 | Ciclo L7–L8: la frontera media-varianza de L7 c. 11 requería varianzas de L8 | L7 c. 11 se limita al problema cuadrático con matriz dada; Markowitz en L10 c. 6 | Resuelto en el plan |
| C-04 | L8 citaba L7 c. 7 para integrales múltiples, que están en L7 c. 10 | Referencia corregida | Resuelto en el plan |
| C-05 | L12 c. 11 (diferencias finitas para EDP) requería L15 | Eliminado de L12; el tema queda en L15 c. 9 | Resuelto en el plan |
| C-06 | L12 c. 2 usaba la volatilidad implícita, que requiere L19 | Reemplazada por TIR y rendimiento de bonos | Resuelto en el plan |
| C-07 | L13 c. 8 requería un TCL para arreglos triangulares y un pago no acotado | TCL de Lindeberg para arreglos triangulares en L8 c. 11; límite para la opción de venta y paridad put-call | Resuelto en el plan |
| C-08 | L6 c. 11 y c. 13 usaban probabilidad | Covarianza muestral como objeto descriptivo; cadenas de Markov trasladadas a L8 | Resuelto en el plan |
| C-09 | L10 tenía contenido empírico sin declarar L9 | L9 declarado como requisito | Resuelto en el plan |
| C-10 | L15 usaba la teoría L² completa, que requiere L16 | Restricción a resultados de Riemann; resto admitido (RA-10) | Resuelto en el plan |
| C-11 | L3 no declaraba L2 | Declarado | Resuelto en el plan |
| C-12 | L5 declaraba L4 solo para c. 9–10; también lo requieren c. 4 y c. 6 | Declarado L4 para el libro; ruta temprana opcional documentada | Resuelto en el plan |
| C-13 | L23 no declaraba L17 ni L19 | Declarados (L19 solo para el caso de opciones) | Resuelto en el plan |

### Hallazgos importantes

| ID | Hallazgo | Resolución | Estado |
|---|---|---|---|
| I-01 | KKT sin teorema de separación disponible | Separación y lema de Farkas en L7 c. 7 | Resuelto en el plan |
| I-02 | Función implícita sin punto fijo disponible antes de L11 | Contracciones en Rⁿ en L7 c. 8 | Resuelto en el plan |
| I-03 | Faltaba la forma de Jordan para L15 | L6 c. 9 | Resuelto en el plan |
| I-04 | Faltaban el método delta, la función Gamma y la integral gaussiana | L9 c. 4; L4 c. 11; L7 c. 10 | Resuelto en el plan |
| I-05 | Lagunas de cobertura: cadenas de Markov finitas, Hoeffding, programación dinámica, MGM, filtro de Kalman, funciones características rigurosas, cambio de numerario, Itô con saltos, ecuación prospectiva de Kolmogorov, MCMC, bootstrap dependiente, estudios de eventos, estados contables | Capítulos y secciones nuevos según `PLAN_EDITORIAL.md` | Resuelto en el plan |

### Hallazgos menores

| ID | Hallazgo | Resolución | Estado |
|---|---|---|---|
| M-01 | L11 c. 10 anticipaba el movimiento browniano como dependencia | Queda como comentario, sin dependencia | Resuelto en el plan |
| M-02 | Requisitos incompletos en L22 | Completados | Resuelto en el plan |

## Revisión R-0002 · Ajustes al incorporar la auditoría en el plan escrito · 2026-10-15

Al redactar `PLAN_EDITORIAL.md` (entrega 1a), la ubicación de algunos capítulos nuevos se fijó de forma distinta a la indicada en la propuesta aprobada. Ningún ajuste cambia el contenido aprobado. Aprobados por la dirección editorial el 2026-10-16.

| ID | Ajuste | Motivo |
|---|---|---|
| A-01 | L8: el capítulo nuevo de paseos aleatorios y cadenas de Markov es el c. 14 | Conserva la numeración citada (TCL en c. 11) y no necesita el TCL |
| A-02 | L9: densidades por núcleos y estimación robusta se agrupan con la estadística multivariante en el c. 13 nuevo, no como secciones de c. 4 y c. 12; el problema de estimar rendimientos esperados pasa a c. 14 | Agrupación temática más coherente; el método delta sigue en c. 4 |
| A-03 | L10: el capítulo nuevo de estados contables es el c. 13 | Conserva la numeración citada (Markowitz c. 6, arbitraje c. 8) |
| A-04 | L12: programación dinámica ocupa el c. 11, en lugar de las diferencias finitas eliminadas | Previsto en la propuesta |
| A-05 | L14: MGM es el c. 13, el contraste de modelos de valoración pasa a c. 14 y el filtro de Kalman es el c. 15 | El contraste de modelos usa el MGM |
| A-06 | L16: las funciones características pasan a c. 8; esperanza condicional c. 9; martingalas c. 10–11; cambio de medida c. 12 | La convergencia en distribución sigue lógicamente a la ley fuerte. El piloto avanzado alternativo pasa a ser L16 c. 9 |
| A-07 | L19: cambio de numerario es el c. 4; los capítulos siguientes se desplazan una posición (métodos numéricos pasa a c. 9) | Debe preceder a las griegas y a los modelos de tasas |
| A-08 | L20: estudios de eventos es el c. 4; purga y embargo pasa a c. 7 | Metodología antes del diseño de backtests |
| A-09 | L23: el caso de opciones es el c. 5 (la propuesta lo llamaba «caso 4») | Corrección de numeración |

## Revisión R-0003 · Índices detallados de L1–L8 · 2026-10-16

Hallazgos surgidos al redactar los índices por sección de L1 a L8 (entrega 1b) y al ejecutar `herramientas/verificar_indices.py`, que comprueba la existencia y el orden de todos los prerrequisitos citados. Resultado final del verificador: 8 libros, 102 capítulos, 0 errores, 1 aviso esperado (L4 c. 13 depende de la sección opcional L4 §9.8 para cerrar RA-22).

| ID | Severidad | Hallazgo | Resolución | Estado |
|---|---|---|---|---|
| H-01 | Importante | La exponencial de matrices figuraba en L6 c. 9 y en L15 c. 2; en L6 requería series (L4), que no es requisito de L6 | Ajuste A-10: se estudia solo en L15 c. 2; L6 c. 9 desarrolla la forma de Jordan, las potencias de matrices y Cayley-Hamilton | Resuelto |
| H-02 | Importante | La desigualdad de Hoeffding estaba en L8 c. 6, pero trata sumas de variables independientes, que se definen en L8 c. 7 | Ajuste A-11: pasa a L8 c. 10, junto con el lema de Slutsky | Resuelto |
| H-03 | Importante | L7 c. 3 usa sensibilidades a tasas cero de L5 sin que L5 figurara como aplicación de L7 (detectado por el verificador) | L5 agregado en la columna «Aplicación» de L7 en el plan | Resuelto |
| H-04 | Importante | La ruta temprana de L5 incluía el capítulo 8, que depende del capítulo 6, que usa L4 | Ruta temprana corregida: capítulos 1–3, 5 y 7 | Resuelto |
| H-05 | Importante | Siete resultados usados en L1–L8 no estaban registrados: medida de ángulos y trigonometría geométrica, regla de Descartes, existencia de espacios de probabilidad, geometría euclídea elemental, esperanza de funciones en el caso continuo general, Berry-Esseen, leyes estables | Registrados como RA-22 a RA-28 con ubicación de uso y de demostración | Resuelto |
| H-06 | Menor | RA-01 (raíces n-ésimas) puede demostrarse en L1 | Demostración en L1 §8.4\* (opcional) y de nuevo en L4 §3.7; RA-01 deja de ser admitido | Resuelto |
| H-07 | Menor | La desigualdad de Bernoulli estaba prevista en L1 c. 4, antes de los números reales | Trasladada a L1 §8.7, donde además motiva la comparación entre interés simple y compuesto | Resuelto |
| H-08 | Menor | L1 c. 6 a c. 13 usan cálculos con Python antes de L1 c. 14 | Apéndice A de L1: Python como calculadora, utilizable desde el capítulo 6 | Resuelto |
| H-09 | Menor | La notación O(·) aparece en L3 §5.3, antes de L4 | Corregida la primera aparición en `NOTACION.md` | Resuelto |
| H-10 | Menor | La integral gaussiana dependía del cambio de variables general (admitido) | L7 §10.6 la demuestra con Fubini y una sustitución en una variable | Resuelto |

Ajustes A-10 y A-11 aprobados por la dirección editorial el 2026-10-16, junto con la entrega 1b.

## Revisión R-0004 · Índices detallados de L9–L16 · 2026-10-16

Hallazgos surgidos al redactar los índices por sección de L9 a L16 (entrega 1c). Resultado final de `herramientas/verificar_indices.py` sobre L1–L16: 16 libros, 196 capítulos, 0 errores, 1 aviso esperado (el mismo de R-0003).

| ID | Severidad | Hallazgo | Resolución | Estado |
|---|---|---|---|---|
| H-11 | Importante | RA-10 admitía toda la teoría L² de Fourier en L15, aunque la identidad de Parseval para funciones integrables según Riemann puede demostrarse con las herramientas de L11 | L15 §6.4–6.5 demuestran Fejér y Parseval; solo se admite el teorema de Riesz-Fischer, que L16 §4.3 demuestra; descripción de L15 c. 6 actualizada en el plan | Resuelto |
| H-12 | Importante | RA-08 (cambio de variables general) quedaba como referencia externa | L16 §5.5\* lo demuestra (sección opcional); RA-08 queda cerrado en la obra | Resuelto |
| H-13 | Importante | L16 c. 12 usa el arbitraje en un período de L10 sin que L10 figurara como aplicación de L16 | L10 agregado a la columna «Aplicación» de L16 en el plan | Resuelto |
| H-14 | Importante | Dieciséis resultados usados en L9–L15 no estaban registrados (teoría asintótica de datos dependientes, bootstrap, BFGS, Koksma-Hlawka, Lax, Runge-Kutta y otros) | Registrados como RA-29 a RA-44; en cada caso se demuestra la versión accesible (un parámetro, caso bivariado, condiciones simplificadas) cuando existe | Resuelto |
| H-15 | Menor | L13 declaraba L3 como requisito sin que ningún capítulo lo citara (detectado por el verificador) | L13 c. 5 cita L3 c. 6, que usa en su sección de implementación con pruebas | Resuelto |
| H-16 | Menor | La función continua no derivable en ningún punto estaba prevista en L11 c. 5, pero su demostración usa convergencia uniforme (L11 c. 7) | Trasladada a L11 §7.7\* | Resuelto |
| H-17 | Menor | La completitud de ℓ^p para p general requiere Hölder y Minkowski, que están en L11 c. 9 | L11 §8.2 trata p = 1, 2, ∞; el caso general está en L11 §9.4 | Resuelto |
| H-18 | Menor | La inferencia estadística sobre parámetros calibrados requiere L9, que no es requisito de L12 | L12 c. 8 se limita a los aspectos numéricos; la inferencia se trata en L14 y L19 c. 12 | Resuelto |
| H-19 | Menor | La convergencia de las soluciones en serie de la ecuación del calor (L15 c. 5) precedía a la teoría de Fourier (L15 c. 6) | L15 §5.4 la justifica para coeficientes absolutamente sumables mediante el criterio M (L11 §7.5) | Resuelto |
| H-20 | Menor | La demostración de Bernstein del teorema de aproximación de Weierstrass usa probabilidad (L8), que no es requisito de L11 | L11 §7.6 usa núcleos de Landau | Resuelto |

Sin ajustes de numeración respecto del plan aprobado.

## Revisión R-0005 · Índices detallados de L17–L23 · 2026-10-16

Hallazgos surgidos al redactar los índices por sección de L17 a L23 (entrega 1d). Resultado final de `herramientas/verificar_indices.py` sobre toda la colección: 23 libros, 277 capítulos (igual al plan), 0 errores, 1 aviso esperado (el de R-0003).

| ID | Severidad | Hallazgo | Resolución | Estado |
|---|---|---|---|---|
| H-21 | Importante | Dieciséis resultados usados en L17–L23 no estaban registrados (consistencia de Ledoit-Wolf, Marchenko-Pastur, elicitabilidad del ES, estimador de Hill, Donsker, propiedad de Markov de las EDE, regularidad en Feynman-Kac, órdenes de Euler-Maruyama y Milstein, teoremas fundamentales en tiempo continuo, Longstaff-Schwartz, condición de Feller, dualidad de la súper replicación, validez del *reality check*, cotas VC, aproximación universal, convergencia de Metropolis-Hastings) | Registrados como RA-45 a RA-60; en cada caso se demuestra la versión accesible cuando existe | Resuelto |
| H-22 | Importante | L17 c. 2 usa el teorema de James-Stein, que estaba en una sección opcional de L9 (detectado por el verificador) | L9 §14.4 pasa a ser obligatoria | Resuelto |
| H-23 | Importante | Los métodos de núcleo (L21 c. 7) requerían espacios de Hilbert generales (L11), que no están en la clausura de requisitos de L21 | L21 c. 7 se desarrolla en espacios de características de dimensión finita con L6 y L7; el capítulo sigue siendo opcional | Resuelto |
| H-24 | Menor | La explicación de por qué la integral de Stieltjes no sirve para el browniano (L18 §5.1) citaba la sección opcional L11 §10.3 | La referencia pasa a L11 c. 10; el resultado de la sección opcional se presenta como complemento | Resuelto |
| H-25 | Menor | La convención del nivel α del VaR estaba pendiente | Fijada en L17 §6.2: pérdida L, α nivel de confianza; actualizada en `NOTACION.md` | Resuelto |
| H-26 | Menor | La propiedad fuerte de Markov del browniano y la ley 0-1 de Blumenthal parecían requerir referencia externa | Se demuestran en L18 §4.1 y L18 §4.3 | Resuelto |
| H-27 | Menor | El caso de opciones de L23 depende de L19, que no es requisito de L23 | Se declara como aplicación (L23 c. 5) y la ficha del libro indica que el capítulo puede omitirse | Resuelto |
| H-28 | Menor | Algunas fórmulas prácticas de L19 (error de cobertura discreta, ajuste de Leland) no son teoremas | Se presentan como aproximaciones con derivación heurística y verificación por simulación | Resuelto |

Sin ajustes de numeración respecto del plan aprobado.

## Pendientes de verificación

| ID | Asunto | Situación |
|---|---|---|
| V-01 | Normas sobre separador de millares (espacio, sin separador en cuatro cifras) | Verificado solo en fuentes secundarias; el sitio de la RAE no es accesible desde el entorno de trabajo |
| V-02 | Espacio entre cifra y % | Verificado mediante resultado de búsqueda que reproduce la entrada «porcentajes» del *Diccionario panhispánico de dudas*, 2.ª edición; acceso directo bloqueado |
| V-03 | Sintaxis de entornos y referencias cruzadas de Quarto | Prefijos de etiqueta confirmados en la documentación de Quarto mediante búsqueda; acceso directo a quarto.org bloqueado; comportamiento en PDF por probar en la Fase 2 |
