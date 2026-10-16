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

## Pendientes de verificación

| ID | Asunto | Situación |
|---|---|---|
| V-01 | Normas sobre separador de millares (espacio, sin separador en cuatro cifras) | Verificado solo en fuentes secundarias; el sitio de la RAE no es accesible desde el entorno de trabajo |
| V-02 | Espacio entre cifra y % | Verificado mediante resultado de búsqueda que reproduce la entrada «porcentajes» del *Diccionario panhispánico de dudas*, 2.ª edición; acceso directo bloqueado |
| V-03 | Sintaxis de entornos y referencias cruzadas de Quarto | Prefijos de etiqueta confirmados en la documentación de Quarto mediante búsqueda; acceso directo a quarto.org bloqueado; comportamiento en PDF por probar en la Fase 2 |
