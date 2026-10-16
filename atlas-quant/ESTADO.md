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
| 1e | Bibliografía verificada, fuentes de datos y auditoría de coherencia | Entregada (2026-10-16); pendiente de revisión |
| 2 | Plan de prueba de composición; capítulo piloto L1 c. 8 | No iniciada |

No existe ningún capítulo redactado.

## 2. Próximo paso exacto

1. Obtener la revisión de la entrega 1e (revisión R-0006): `bibliografia/atlas.bib` y su versión legible `bibliografia/bibliografia.md`, `bibliografia/fuentes_de_datos.md` y `editorial/auditoria_fase1.md`. También obtener las decisiones D-05 y D-06.
2. Con la aprobación, iniciar la Fase 2 presentando el plan de prueba de composición (D-04). No se instala nada antes de su aprobación.
3. Después, redactar el capítulo piloto L1 c. 8.
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
| Piloto | L1 c. 8, «Potencias, raíces y logaritmos»; después, un piloto avanzado (L18 c. 6 o L16 c. 9) | 2026-10-15 |

## 4. Pendientes que requieren decisión del director

| ID | Asunto |
|---|---|
| D-01 | Nombre que figurará en los créditos editoriales |
| D-02 | Licencia de la obra (todos los derechos reservados o Creative Commons, por ejemplo CC BY-NC-SA 4.0) |
| D-03 | Hitos con revisión humana externa (propuesta: piloto, primer capítulo de cada serie, capítulos de L16, L18 y L19) |
| D-04 | Aprobación del plan de prueba de composición (se presentará al inicio de la Fase 2) |
| D-05 | Política de datos de la obra y casos de L23 que dependen de datos con licencia restringida (`bibliografia/fuentes_de_datos.md`; auditoría, H-31 y H-32) |
| D-06 | Verificación en fuente primaria de las 33 entradas bibliográficas parciales: ampliar la red del entorno a `doi.org` y `api.crossref.org`, o verificación manual antes de componer cada libro |

## 5. Restricciones del entorno de trabajo

Observadas el 2026-10-15:

- El contenedor es efímero: todo trabajo debe guardarse con commit y push al cerrar cada sesión.
- Disponible: Python 3.13 con numpy y pandas; pandoc 3.1.3; Chromium y Playwright para Node (usados para generar los PDF de trabajo); búsqueda web.
- No disponible: LaTeX, Quarto, scipy, sympy, matplotlib (su instalación requiere aprobación).
- Red: `github.com` accesible. La política de red del entorno bloquea `quarto.org`, `www.rae.es`, `mirror.ctan.org`, `doi.org`, `api.crossref.org`, `openlibrary.org`, OpenAlex, JSTOR y los sitios de datos (FRED, Kenneth French). Consecuencias: (a) la verificación bibliográfica de la entrega 1e se hizo mediante búsqueda web (D-06); (b) la instalación de LaTeX desde CTAN no es posible con la política actual, lo que debe resolverse en el plan de prueba de composición; (c) los datos de los capítulos empíricos no pueden descargarse desde el entorno, lo que el plan de la Fase 2 deberá considerar.

## 6. Verificaciones pendientes

V-01 a V-03 quedaron resueltas en R-0006. Quedan abiertas las 33 entradas bibliográficas parciales (H-34, decisión D-06), cuya causa se registra en `bibliografia/atlas.bib`.
