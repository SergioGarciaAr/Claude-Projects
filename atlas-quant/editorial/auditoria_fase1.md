# Auditoría de coherencia de la Fase 1

Entrega 1e · Versión 1.0 · 2026-10-16 · Revisión R-0006

Esta auditoría cierra la Fase 1 (diseño editorial). Comprueba que los documentos de la fase sean coherentes entre sí: plan, libro de estilo, notación, glosario, registros, los 23 índices detallados y la bibliografía. También presenta la bibliografía verificada, las fuentes de datos, la resolución de las verificaciones pendientes V-01 a V-03 y la comparación de extensiones entre los índices y el plan.

## 1. Alcance y método

| Objeto | Método | Resultado |
|---|---|---|
| Prerrequisitos, numeración, número de capítulos y resultados admitidos de los 23 índices | `herramientas/verificar_indices.py` (comprobaciones 1 a 5) | 0 errores |
| Extensión declarada en la ficha de cada libro | Nueva comprobación 6 del verificador: suma de capítulos + 20 páginas de preliminares + 10 a 20 páginas por apéndice | 23 fichas corregidas; 0 errores (hallazgo H-29) |
| Referencias cruzadas (L*n* §*c.s*, L*n* c. *c*, L*n* ap. *X*) en `NOTACION.md`, `GLOSARIO.md`, `editorial/resultados_admitidos.md`, `PLAN_EDITORIAL.md` y `bibliografia/atlas.bib` | Lectura con el analizador del verificador | 639 referencias; ninguna apunta a un elemento inexistente |
| Cobertura bibliográfica de los resultados admitidos | `herramientas/bib_a_md.py` | Los 48 resultados admitidos con referencia externa tienen al menos una entrada bibliográfica |
| Metadatos bibliográficos | Búsqueda web, una consulta por obra (sección 3) | 178 entradas: 145 verificadas y 33 parciales |
| Fuentes de datos de L20 y L23 | Búsqueda web de condiciones de uso | `bibliografia/fuentes_de_datos.md` |
| V-01 a V-03 | Búsqueda web restringida a los sitios oficiales | Resueltas (sección 6) |

**Limitación del método.** El entorno de trabajo bloquea `doi.org`, `api.crossref.org`, OpenAlex, Open Library, JSTOR, `rae.es` y `quarto.org`. Toda verificación se hizo a partir de los resultados del buscador, que muestran fragmentos de las páginas oficiales (editoriales, Project Euclid, IDEAS/RePEc, Econometric Society, catálogos de bibliotecas) pero no permiten abrirlas. Una entrada se marcó «verificada» solo cuando una fuente identificable mostraba los datos. En los demás casos se marcó «parcial» y se anotó qué faltaba. Ningún DOI se registró sin que una fuente lo mostrara.

## 2. Coherencia entre documentos

1. **Índices frente al plan.** Hay 23 libros y 277 capítulos, igual que en el plan. Todo prerrequisito es anterior a su capítulo y está en la clausura transitiva de los requisitos declarados, o en la columna de aplicación. Sigue vigente el aviso esperado L4 c. 13 → L4 §9.8\*, ya registrado en R-0003.
2. **Resultados admitidos.** Los 60 identificadores citados en los índices existen en el registro. Los 48 que se admiten con referencia externa (RA-07, RA-11 a RA-21, RA-23, RA-25, RA-27 a RA-60) tienen referencia en `atlas.bib`. Los demás se cierran dentro de la obra (RA-01 a RA-06, RA-08 a RA-10, RA-22, RA-24, RA-26).
3. **Notación y glosario.** Las tablas de primera aparición de `NOTACION.md` (secciones 11 a 13) y de `GLOSARIO.md` citan 243 lugares, todos existentes.
4. **Bibliografía frente a índices.** El campo `uso` de cada entrada cita capítulos existentes (186 referencias). En esta entrega se revisó a mano su correspondencia con el contenido: 60 entradas se reasignaron al capítulo que efectivamente trata el tema; por ejemplo, Merton (1974) pasó de L22 c. 8 a L22 c. 6 y Dupire (1994) de L19 c. 9 a L19 c. 10.
5. **Plan frente a bibliografía.** El plan cita los textos de contraste por autor y título. Ahora remite a `atlas.bib` para los datos completos. La 11.ª edición de Hull, que una referencia previa del proyecto fechaba en 2021, tiene copyright 2022 según las fuentes (entrada `hull2022`).

## 3. Bibliografía

### 3.1 Contenido

| Sección de `atlas.bib` | Entradas |
|---|---|
| Textos de contraste del plan (sección 5) | 32 |
| Referencias externas de los resultados admitidos | 55 |
| Fuentes originales de modelos, métodos y resultados empíricos citados en los índices | 88 |
| Convenciones de mercado y hechos institucionales | 3 |
| **Total** | **178** |

`bibliografia/bibliografia.md` es la versión legible, generada por `herramientas/bib_a_md.py`. Cada entrada registra la URL de la fuente de verificación, la fecha y, cuando corresponde, una nota con la discrepancia encontrada.

### 3.2 Entradas parciales (33)

| Motivo | Entradas |
|---|---|
| Páginas no confirmadas o discrepantes entre fuentes | `cox1985`, `breeden1978`, `carr1999`, `garman1983`, `harvey2016`, `kyle1985`, `almgren2000`, `bailey2017`, `jagannathan2003`, `rockafellar2000`, `ho1986`, `hagan2002`, `black1972`, `delbaen1994`, `donsker1951` |
| Datos confirmados solo por fuentes secundarias | `yamada1971`, `wang2004`, `ljung1978`, `feller1951`, `vasicek1977`, `margrabe1978`, `kupiec1995`, `isda2006`, `arrc2017` |
| Edición, año, ISBN, DOI o número de serie por precisar | `apostol1967`, `ross2019`, `luenberger2013`, `glasserman2003`, `hull2022`, `hastie2009`, `hairer1993`, `follmer1981`, `nelson1987` |

Ninguna afecta al contenido matemático de los índices. Deben resolverse antes de la composición final de cada libro que las cite, consultando la fuente primaria (D-06).

### 3.3 Hallazgos con efecto en la redacción

- **Correcciones publicadas que deben citarse junto con el original:**
  - Andrews (1993): corrigendum en *Econometrica*, 2003.
  - Fissler y Ziegel (2016): corrección en *The Annals of Statistics* 49(1), 2021.
  - Jagannathan y Ma (2003): nota de corrección en *The Journal of Finance* 74(5), 2019.
- **Clément, Lamberton y Protter (2002):** un trabajo de 2019 (Liu, Schellhorn y Peng) señala un vacío en la demostración y lo completa. La referencia de RA-54 en L19 c. 7 debe incluir ese trabajo, cuyos datos aún no están en la bibliografía.
- **Leland (1985):** la literatura posterior señala un error en el teorema principal. Esto es coherente con H-28: L19 c. 5 ya presenta el ajuste de Leland como aproximación.
- **Föllmer y Schied:** existe una quinta edición (2025). Se elegirá la edición al redactar.
- **Kyle (1985) y Cox, Ingersoll y Ross (1985):** la paginación difiere entre JSTOR y la Econometric Society. Se registra la de JSTOR o RePEc y se anota la discrepancia.

## 4. Fuentes de datos

El detalle está en `bibliografia/fuentes_de_datos.md`. Hallazgos principales:

- **FRED.** Los términos vigentes desde junio de 2024 prohíben usar el contenido o la API para desarrollar o entrenar sistemas de aprendizaje automático. FRED queda excluida de L21 y de L23 c. 6 (H-30).
- **Kenneth R. French Data Library.** Los datos llevan aviso de copyright y derivan en gran parte de CRSP. No se encontraron términos de redistribución. El libro no redistribuirá archivos; el código los descargará.
- **Réplicas de L23 c. 2 y c. 3.** Requieren datos de acciones individuales (CRSP, Compustat), que son comerciales. Se propone replicar con las carteras y factores publicados por French y enseñar la construcción con datos sintéticos (H-31).
- **Datos de opciones.** No hay fuente gratuita con licencia verificable. Para L23 c. 5 se propone usar datos sintéticos generados por un modelo calibrado a parámetros publicados (H-32).
- **Política propuesta.** La obra no redistribuye datos de terceros. Toda cifra empírica impresa lleva fecha y el código que la regenera. Requiere revisión legal antes de publicar (D-05).

## 5. Extensiones: índices frente al plan

El plan (sección 8) estima las páginas de los capítulos como capítulos × 25–40 páginas y suma aparte unas 20 páginas de preliminares por libro. Los índices dan una extensión por capítulo y otra para el libro. La auditoría encontró que la extensión de la ficha de cada libro no derivaba de una regla única: la diferencia con la suma de sus capítulos iba de 6 páginas (L1) a 78 (L18) (H-29).

La regla adoptada para la ficha es: suma de capítulos + 20 páginas de preliminares + 10 a 20 páginas por apéndice. Ahora el verificador la comprueba en cada ejecución.

| Libro | Caps. | Ap. | Plan (capítulos) | Suma de capítulos | Ficha anterior | Ficha recalculada |
|---|---|---|---|---|---|---|
| L1 | 14 | 2 | 350–560 | 384–468 | 390–470 | 424–528 |
| L2 | 13 | 1 | 325–520 | 324–402 | 340–420 | 354–442 |
| L3 | 12 | 1 | 300–480 | 296–368 | 300–380 | 326–408 |
| L4 | 14 | 1 | 350–560 | 386–470 | 420–500 | 416–510 |
| L5 | 11 | 1 | 275–440 | 284–350 | 290–360 | 314–390 |
| L6 | 13 | 1 | 325–520 | 352–430 | 370–450 | 382–470 |
| L7 | 11 | 1 | 275–440 | 292–358 | 320–400 | 322–398 |
| L8 | 14 | 1 | 350–560 | 394–478 | 400–480 | 424–518 |
| L9 | 14 | 1 | 350–560 | 372–456 | 400–480 | 402–496 |
| L10 | 13 | 1 | 325–520 | 344–422 | 370–450 | 374–462 |
| L11 | 10 | 1 | 250–400 | 262–322 | 290–360 | 292–362 |
| L12 | 12 | 1 | 300–480 | 320–392 | 340–420 | 350–432 |
| L13 | 9 | 1 | 225–360 | 226–280 | 260–320 | 256–320 |
| L14 | 15 | 1 | 375–600 | 406–496 | 430–520 | 436–536 |
| L15 | 9 | 1 | 225–360 | 238–292 | 260–320 | 268–332 |
| L16 | 12 | 1 | 300–480 | 324–396 | 340–420 | 354–436 |
| L17 | 13 | 1 | 325–520 | 334–412 | 370–450 | 364–452 |
| L18 | 11 | 1 | 275–440 | 306–372 | 370–450 | 336–412 |
| L19 | 13 | 1 | 325–520 | 340–418 | 370–450 | 370–458 |
| L20 | 12 | 1 | 300–480 | 300–372 | 330–410 | 330–412 |
| L21 | 13 | 1 | 325–520 | 316–394 | 360–440 | 346–434 |
| L22 | 10 | 1 | 250–400 | 252–312 | 280–350 | 282–352 |
| L23 | 9 | 1 | 225–360 | 208–262 | 250–310 | 238–302 |
| **Total** | **277** | | **6 925–11 080** | **7 260–8 922** | **7850–9610** | **7 960–9 862** |

«Plan (capítulos)» es el intervalo de la sección 8 del plan, que excluye preliminares y apéndices. «Suma de capítulos» es la suma de las extensiones por capítulo de los índices, y la ficha recalculada añade preliminares y apéndices. Totales de ficha: los anteriores sumaban 7850–9610 páginas y los recalculados suman 7 960–9 862.

**Lectura.**

- La suma de capítulos (7 260–8 922) queda dentro del intervalo del plan y reduce su amplitud de 4155 a 1662 páginas (40 % de la original).
- En cuatro libros la suma queda por debajo del extremo inferior del plan: L2 (1 página), L3 (4), L21 (9) y L23 (17). Se debe a que varios capítulos se estimaron por debajo del mínimo de 25 páginas que supone el plan: por ejemplo, L2 c. 5 (18–24), L3 c. 1 y c. 10 (20–26), L21 c. 3, c. 5 y c. 13 (20–26) y L23 c. 1 (20–26) y c. 9 (16–22).
- El verificador lo informa como aviso, no como error. Se considera aceptable: el plan presenta sus cifras como escenarios y la medición real llegará con el capítulo piloto.
- Ejercicios: la suma de los intervalos declarados por capítulo es de 7280 a 10 050. En L23 solo el capítulo 1 tiene ejercicios (10–15); los capítulos 2 a 8 son proyectos guiados y el 9 no tiene ejercicios. L21 c. 13 también es un proyecto guiado.

## 6. Verificaciones pendientes V-01 a V-03

| ID | Asunto | Resolución |
|---|---|---|
| V-01 | Separador de millares | Resuelta. La entrada «números» del *Diccionario panhispánico de dudas* (rae.es/dpd/números, mostrada por el buscador) admite el espacio como separador de millares y lo considera opcional en números de cuatro cifras, donde lo habitual es omitirlo. La convención de la obra (espacio fino desde cinco cifras; sin separador en cuatro cifras) es conforme |
| V-02 | Espacio entre cifra y % | Resuelta. La entrada «porcentajes» del *Diccionario panhispánico de dudas* (rae.es/dpd/porcentajes) indica que el signo % se escribe precedido de un espacio, como los demás símbolos pospuestos. El *Libro de estilo de la lengua española* (rae.es) coincide |
| V-03 | Sintaxis de Quarto para teoremas y referencias cruzadas | Resuelta en cuanto a sintaxis. La documentación oficial (quarto.org/docs/authoring/cross-references.html) define los prefijos reservados `thm`, `lem`, `cor`, `prp`, `cnj`, `def`, `exm`, `exr` y la creación de un teorema referenciable con un div `#thm-`. La salida a PDF se probará en la Fase 2, según el plan de prueba de composición (D-04) |

## 7. Hallazgos de esta revisión

| ID | Severidad | Hallazgo | Resolución | Estado |
|---|---|---|---|---|
| H-29 | Menor | La extensión de la ficha de cada libro no derivaba de una regla (diferencias de 6 a 78 páginas respecto de la suma de capítulos) | Regla única y comprobación automática 6 del verificador; 23 fichas recalculadas | Resuelto |
| H-30 | Importante | Los términos de FRED prohíben usar sus datos para entrenar sistemas de aprendizaje automático | FRED excluida de L21 y de L23 c. 6; registrado en `fuentes_de_datos.md` | Resuelto |
| H-31 | Importante | Las réplicas de L23 c. 2 y c. 3 requieren datos comerciales de acciones individuales | Aprobado en D-05: carteras y factores de French y datos sintéticos para la construcción. Índice de L23 actualizado (versión 1.1) | Resuelto |
| H-32 | Importante | No hay fuente gratuita y con licencia verificable de datos de opciones para L23 c. 5 | Aprobado en D-05: datos sintéticos de un modelo calibrado; capítulo retitulado y reestructurado en el índice de L23 | Resuelto |
| H-33 | Menor | Tres artículos citados tienen correcciones publicadas y uno tiene un vacío de demostración señalado en la literatura | Registrados en las notas de `atlas.bib`; se citarán junto con el original | Resuelto |
| H-34 | Menor | 33 entradas bibliográficas no pudieron verificarse por completo por las restricciones de red | Marcadas como parciales, con la causa; resolución antes de la composición (D-06) | Abierto |
| H-35 | Menor | En el campo `uso` de la bibliografía, 60 entradas apuntaban a capítulos no idóneos | Reasignadas tras revisar los títulos de capítulo de los índices | Resuelto |

## 8. Decisiones que se solicitan

| ID | Asunto | Propuesta |
|---|---|---|
| D-05 | Política de datos y casos de L23 | **Aprobada el 2026-10-16.** Política de la sección 3 de `fuentes_de_datos.md`, réplicas de L23 c. 2 y c. 3 con datos de French y sintéticos, y datos sintéticos para L23 c. 5. La revisión legal queda como requisito antes de la publicación |
| D-06 | Verificación bibliográfica en fuente primaria | Ampliar la política de red del entorno a `doi.org` y `api.crossref.org`, o hacer la verificación manual antes de la composición de cada libro |

## 9. Conclusión

La Fase 1 queda completa y coherente con las salvedades indicadas: la decisión D-06 y las 33 entradas parciales. D-05 se aprobó el 2026-10-16 y se aplicó al índice de L23. El siguiente paso es la Fase 2, que empieza con el plan de prueba de composición (D-04). Ese plan se presentará para aprobación antes de instalar nada.
