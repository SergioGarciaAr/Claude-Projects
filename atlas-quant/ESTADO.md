# Estado del proyecto Atlas Quant

Última actualización: 2026-10-16\
Rama de trabajo: `claude/magical-shannon-afvwc6`

**Leer este archivo primero al reanudar el trabajo.**

## 1. Situación actual

| Fase | Entrega | Estado |
|---|---|---|
| 0 | Auditoría del entorno y propuesta editorial | Aprobada |
| 1a | Plan editorial, libro de estilo, notación, glosario, registros internos | Aprobada (2026-10-16) |
| 1b | Índices detallados por sección de L1–L8 | Aprobada (2026-10-16) |
| 1c | Índices detallados de L9–L16 | Aprobada (2026-10-16) |
| 1d | Índices detallados de L17–L23 | Aprobada (2026-10-16) |
| 1e | Bibliografía verificada, fuentes de datos y auditoría de coherencia | Aprobada (2026-10-16) |
| 2 | Plan de prueba de composición; capítulo piloto L1 c. 8 | **En curso**: plan de prueba presentado (`editorial/plan_prueba_composicion.md`), pendiente de aprobación (D-04) |

No existe ningún capítulo redactado.

## 2. Próximo paso exacto

1. Obtener la aprobación del plan de prueba de composición (D-04) y, opcionalmente, la ampliación de red (D-07).
2. Con la aprobación, ejecutar la prueba: guion de instalación versionado, muestra en `pruebas/composicion/`, compilación con las candidatas C1–C4, informe comparativo `editorial/informe_composicion.md` y propuesta de decisión D-04b.
3. Con la cadena aprobada, redactar el capítulo piloto L1 c. 8.
4. Al cerrar cada entrega: ejecutar `herramientas/verificar_indices.py` y `herramientas/bib_a_md.py`, regenerar los PDF con `herramientas/generar_pdf.mjs`, hacer commit y push.

## 3. Decisiones aprobadas

| Decisión | Contenido | Fecha |
|---|---|---|
| Producto | Colección de libros de texto universitarios; el código es material didáctico | 2026-10-15 |
| Estructura | 23 libros en 5 series, 277 capítulos; correcciones de la auditoría R-0001 | 2026-10-15 |
| Regla de resultados admitidos | `LIBRO_DE_ESTILO.md`, sección 4 | 2026-10-15 |
| Ubicación | `atlas-quant/` dentro del repositorio existente | 2026-10-15 |
| Idioma y números | Español latinoamericano; coma decimal en la prosa, punto en el código; espacio fino como separador de millares (sujeto a V-01) | 2026-10-15 |
| Solucionarios | Volúmenes separados; soluciones completas para demostraciones y aplicaciones; respuesta y paso clave para ejercicios rutinarios; orientaciones para problemas abiertos; selección dentro de cada libro | 2026-10-15 |
| Composición | Quarto como opción principal, a evaluar; no se instala nada hasta aprobar el plan de prueba | 2026-10-15 |
| Créditos | Texto de `PLAN_EDITORIAL.md`, sección 9, con nombre pendiente | 2026-10-15 |
| Revisión | Procedimiento de `LIBRO_DE_ESTILO.md`, sección 17; revisor adversarial autorizado para el piloto | 2026-10-15 |
| Aprobación | Capítulo por capítulo durante la primera etapa de producción | 2026-10-15 |
| Ajustes A-01 a A-09 | Reubicación de capítulos nuevos (`editorial/registro_de_revisiones.md`, R-0002) | 2026-10-16 |
| Entrega 1b y ajustes A-10, A-11 | Índices de L1–L8; revisión R-0003 | 2026-10-16 |
| Entrega 1c | Índices de L9–L16; revisión R-0004 | 2026-10-16 |
| Entrega 1d | Índices de L17–L23; revisión R-0005 | 2026-10-16 |
| Formato de entrega | Todo entregable se entrega en PDF, generado desde las fuentes Markdown con `herramientas/generar_pdf.mjs` (pandoc y Chromium) y guardado en `pdf/`. Los PDF de trabajo no son la composición final de los libros, que sigue pendiente del plan de prueba de la Fase 2 | 2026-10-16 |
| Entrega 1e | Bibliografía, fuentes de datos y auditoría de la Fase 1; revisión R-0006 | 2026-10-16 |
| Política de datos (D-05) | Aprobada la política de `bibliografia/fuentes_de_datos.md`, sección 3: la obra no redistribuye datos de terceros; cifras empíricas fechadas y regenerables; datos sintéticos con semilla fija cuando no hay fuente libre con licencia verificable; FRED excluida del aprendizaje automático. Aplicada al índice de L23 (c. 2, c. 3 y c. 5). Requisito previo a la publicación: revisión legal | 2026-10-16 |
| Piloto | L1 c. 8, «Potencias, raíces y logaritmos»; después, un piloto avanzado (L18 c. 6 o L16 c. 9) | 2026-10-15 |

## 4. Pendientes que requieren decisión del director

| ID | Asunto |
|---|---|
| D-01 | Nombre que figurará en los créditos editoriales |
| D-02 | Licencia de la obra (todos los derechos reservados o Creative Commons, por ejemplo CC BY-NC-SA 4.0) |
| D-03 | Hitos con revisión humana externa (propuesta: piloto, primer capítulo de cada serie, capítulos de L16, L18 y L19) |
| D-04 | Aprobación del plan de prueba de composición (`editorial/plan_prueba_composicion.md`), incluidas las instalaciones de su sección 5 |
| D-06 | Verificación en fuente primaria de las 33 entradas bibliográficas parciales: ampliar la red del entorno a `doi.org` y `api.crossref.org`, o verificación manual antes de componer cada libro |
| D-07 | Ampliación opcional de la red del entorno: `packages.typst.org`, `github.com` y sus dominios de descarga, `doi.org` y `api.crossref.org` (plan de prueba, sección 9) |

## 5. Restricciones del entorno de trabajo

Observadas el 2026-10-15:

- El contenedor es efímero: todo trabajo debe guardarse con commit y push al cerrar cada sesión.
- Disponible: Python 3.13 con numpy 2.5.3 y pandas 3.0.5; pandoc 3.1.3; Chromium y Playwright para Node (usados para generar los PDF de trabajo); búsqueda web.
- No disponible: LaTeX, Quarto, scipy, sympy, matplotlib (su instalación requiere aprobación).
- Red (medida de nuevo el 2026-10-16): accesibles conda-forge (`conda.anaconda.org`), el repositorio de Ubuntu, PyPI, npm y `raw.githubusercontent.com`. Bloqueados: `github.com` (web, API y descargas de versiones), `quarto.org`, `packages.typst.org`, `www.rae.es`, `mirror.ctan.org`, `doi.org`, `api.crossref.org`, `openlibrary.org`, OpenAlex, JSTOR y los sitios de datos (FRED, Kenneth French). Consecuencias: (a) la verificación bibliográfica se hizo mediante búsqueda web (D-06); (b) las herramientas de composición se instalarán desde conda-forge y Ubuntu (plan de prueba, sección 2); (c) los datos de los capítulos empíricos no pueden descargarse desde el entorno.

## 6. Verificaciones pendientes

V-01 a V-03 quedaron resueltas en R-0006. Quedan abiertas las 33 entradas bibliográficas parciales (H-34, decisión D-06), cuya causa se registra en `bibliografia/atlas.bib`.

## 7. Requisitos previos a la publicación

- Revisión legal de la política de datos (redistribución y reproducción de cifras) según la licencia que se elija en D-02.
