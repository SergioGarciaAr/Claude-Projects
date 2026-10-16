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
| 2 | Plan de prueba de composición; capítulo piloto L1 c. 8 | **En curso**: prueba de composición ejecutada y cadena elegida (D-04b, `editorial/informe_composicion.md`); siguiente: piloto L1 c. 8 |

No existe ningún capítulo redactado.

## 2. Próximo paso exacto

1. Montar la plantilla común de composición en `composicion/`, a partir de `pruebas/composicion/`: filtros, preámbulo, estilo de cita adaptado y módulo de código común del lector.
2. Crear el proyecto del libro L1 y redactar el capítulo piloto L1 c. 8, «Potencias, raíces y logaritmos», según su índice. Después, revisarlo según el libro de estilo (sección 17), componerlo con la cadena C2, registrar la revisión y entregar el PDF.
3. Continuar la producción según el modo de trabajo de la sección 4.
4. Al cerrar cada entrega: ejecutar `herramientas/verificar_indices.py` y `herramientas/bib_a_md.py`, regenerar los PDF de trabajo con `herramientas/generar_pdf.mjs`, componer los capítulos con Quarto, hacer commit y push. Las herramientas se reinstalan con `herramientas/instalar_composicion.sh` si el contenedor se recicló.

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
| Cadena de composición (D-04b) | Quarto 1.9.38 → LuaLaTeX (TeX Live 2023), Libertinus Serif y Libertinus Math; solucionario desde la misma fuente con `xr`; sintaxis definitiva en `LIBRO_DE_ESTILO.md` §6.2 (`editorial/informe_composicion.md`) | 2026-10-16 |
| Créditos | Texto de `PLAN_EDITORIAL.md`, sección 9, con nombre pendiente | 2026-10-15 |
| Revisión | Procedimiento de `LIBRO_DE_ESTILO.md`, sección 17; revisor adversarial autorizado para el piloto | 2026-10-15 |
| Aprobación | Capítulo por capítulo durante la primera etapa de producción (sustituida el 2026-10-16 por producción continua; sección 4) | 2026-10-15 |
| Ajustes A-01 a A-09 | Reubicación de capítulos nuevos (`editorial/registro_de_revisiones.md`, R-0002) | 2026-10-16 |
| Entrega 1b y ajustes A-10, A-11 | Índices de L1–L8; revisión R-0003 | 2026-10-16 |
| Entrega 1c | Índices de L9–L16; revisión R-0004 | 2026-10-16 |
| Entrega 1d | Índices de L17–L23; revisión R-0005 | 2026-10-16 |
| Formato de entrega | Todo entregable se entrega en PDF, generado desde las fuentes Markdown con `herramientas/generar_pdf.mjs` (pandoc y Chromium) y guardado en `pdf/`. Los PDF de trabajo no son la composición final de los libros, que sigue pendiente del plan de prueba de la Fase 2 | 2026-10-16 |
| Entrega 1e | Bibliografía, fuentes de datos y auditoría de la Fase 1; revisión R-0006 | 2026-10-16 |
| Política de datos (D-05) | Aprobada la política de `bibliografia/fuentes_de_datos.md`, sección 3: la obra no redistribuye datos de terceros; cifras empíricas fechadas y regenerables; datos sintéticos con semilla fija cuando no hay fuente libre con licencia verificable; FRED excluida del aprendizaje automático. Aplicada al índice de L23 (c. 2, c. 3 y c. 5). Requisito previo a la publicación: revisión legal | 2026-10-16 |
| Piloto | L1 c. 8, «Potencias, raíces y logaritmos»; después, un piloto avanzado (L18 c. 6 o L16 c. 9) | 2026-10-15 |

## 4. Decisiones del 2026-10-16 y modo de trabajo

El director aprobó todas las decisiones pendientes e indicó que no se le consulte más. En consecuencia:

| ID | Resolución |
|---|---|
| D-01 | Aprobado el texto de créditos. El nombre del director es un dato que solo él puede aportar: se mantiene el marcador «[nombre del director de la obra]» hasta antes de la publicación (sección 7) |
| D-02 | Licencia provisional: todos los derechos reservados. Es la opción reversible; una licencia Creative Commons, una vez publicada, no puede revocarse para las copias distribuidas. Puede cambiarse antes de la publicación |
| D-03 | Aprobados los hitos propuestos de revisión humana externa: piloto, primer capítulo de cada serie y capítulos de L16, L18 y L19. Se registran como requisito previo a la publicación de esos capítulos (sección 7) |
| D-04 | Aprobado el plan de prueba de composición; la prueba se ejecutó (`editorial/informe_composicion.md`) |
| D-06 | Verificación en fuente primaria de las entradas parciales antes de componer cada libro que las cite; si la red del entorno se amplía, se hará por consulta a Crossref |
| D-07 | Aprobada la ampliación de red, que solo el director puede ejecutar en la configuración del entorno. Mientras no se haga, el trabajo continúa con los orígenes accesibles |
| Modo de trabajo | Se sustituye la aprobación capítulo por capítulo por producción continua: cada capítulo se redacta, se revisa según `LIBRO_DE_ESTILO.md`, sección 17, se compone, se registra y se entrega en PDF sin esperar respuesta. El director puede intervenir en cualquier momento |

## 5. Restricciones del entorno de trabajo

Observadas el 2026-10-15:

- El contenedor es efímero: todo trabajo debe guardarse con commit y push al cerrar cada sesión.
- Disponible: Python 3.13 con numpy 2.5.3 y pandas 3.0.5; pandoc 3.1.3; Chromium y Playwright para Node (usados para generar los PDF de trabajo); búsqueda web.
- No disponible: LaTeX, Quarto, scipy, sympy, matplotlib (su instalación requiere aprobación).
- Red (medida de nuevo el 2026-10-16): accesibles conda-forge (`conda.anaconda.org`), el repositorio de Ubuntu, PyPI, npm y `raw.githubusercontent.com`. Bloqueados: `github.com` (web, API y descargas de versiones), `quarto.org`, `packages.typst.org`, `www.rae.es`, `mirror.ctan.org`, `doi.org`, `api.crossref.org`, `openlibrary.org`, OpenAlex, JSTOR y los sitios de datos (FRED, Kenneth French). Consecuencias: (a) la verificación bibliográfica se hizo mediante búsqueda web (D-06); (b) las herramientas de composición se instalarán desde conda-forge y Ubuntu (plan de prueba, sección 2); (c) los datos de los capítulos empíricos no pueden descargarse desde el entorno.

## 6. Verificaciones pendientes

V-01 a V-03 quedaron resueltas en R-0006. Quedan abiertas las 33 entradas bibliográficas parciales (H-34, decisión D-06), cuya causa se registra en `bibliografia/atlas.bib`.

## 7. Requisitos previos a la publicación

- Nombre del director en los créditos (D-01) y confirmación de la licencia (D-02).
- Revisión humana externa de los hitos de D-03.
- Revisión legal de la política de datos (redistribución y reproducción de cifras) según la licencia que se elija en D-02.
