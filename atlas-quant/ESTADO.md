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
| 1c | Índices detallados de L9–L16 | **Entregada; pendiente de revisión** |
| 1d | Índices detallados de L17–L23 | No iniciada |
| 1e | Bibliografía verificada y auditoría de coherencia | No iniciada |
| 2 | Plan de prueba de composición; capítulo piloto L1 c. 8 | No iniciada |

No existe ningún capítulo redactado.

## 2. Próximo paso exacto

1. Obtener la revisión de la entrega 1c (índices de L9–L16, revisión R-0004).
2. Con la aprobación, iniciar la entrega 1d: índices detallados de L17 a L23 con el mismo formato, verificados con `herramientas/verificar_indices.py`; confirmar las entradas RA-15 a RA-18, RA-20 y RA-21; extender los registros de primera aparición de `NOTACION.md` y `GLOSARIO.md`.
3. Al cerrar cada entrega: ejecutar el verificador, regenerar los PDF con `herramientas/generar_pdf.mjs`, hacer commit y push.

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
| Formato de entrega | Todo entregable se entrega en PDF, generado desde las fuentes Markdown con `herramientas/generar_pdf.mjs` (pandoc y Chromium) y guardado en `pdf/`. Los PDF de trabajo no son la composición final de los libros, que sigue pendiente del plan de prueba de la Fase 2 | 2026-10-16 |
| Piloto | L1 c. 8, «Potencias, raíces y logaritmos»; después, un piloto avanzado (L18 c. 6 o L16 c. 9) | 2026-10-15 |

## 4. Pendientes que requieren decisión del director

| ID | Asunto |
|---|---|
| D-01 | Nombre que figurará en los créditos editoriales |
| D-02 | Licencia de la obra (todos los derechos reservados o Creative Commons, por ejemplo CC BY-NC-SA 4.0) |
| D-03 | Hitos con revisión humana externa (propuesta: piloto, primer capítulo de cada serie, capítulos de L16, L18 y L19) |
| D-04 | Aprobación del plan de prueba de composición (se presentará al inicio de la Fase 2) |

## 5. Restricciones del entorno de trabajo

Observadas el 2026-10-15:

- El contenedor es efímero: todo trabajo debe guardarse con commit y push al cerrar cada sesión.
- Disponible: Python 3.13 con numpy y pandas; pandoc 3.1.3; Chromium y Playwright para Node (usados para generar los PDF de trabajo); búsqueda web.
- No disponible: LaTeX, Quarto, scipy, sympy, matplotlib (su instalación requiere aprobación).
- Red: `github.com` accesible; `quarto.org`, `www.rae.es`, `mirror.ctan.org`, `doi.org`, `api.crossref.org` y `openlibrary.org` bloqueados por la política de red del entorno. Consecuencias: (a) la verificación bibliográfica de la entrega 1e se hará mediante búsqueda web, salvo que se amplíe la política de red; (b) la instalación de LaTeX desde CTAN no es posible con la política actual, lo que debe resolverse en el plan de prueba de composición.

## 6. Verificaciones pendientes

Véase la sección «Pendientes de verificación» de `editorial/registro_de_revisiones.md` (V-01 a V-03).
