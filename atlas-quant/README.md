# Atlas Quant

*Curso universitario de Finanzas Cuantitativas* (título provisional).

Atlas Quant es una colección de libros de texto universitarios, escrita en español, que lleva al lector desde la matemática elemental hasta la investigación cuantitativa avanzada. El producto de este proyecto son los libros: manuscritos completos, sus solucionarios y el código complementario que acompaña la exposición. Todo lo demás que contiene este directorio es material interno de control editorial.

## Estado

La obra está en la **Fase 1 (diseño editorial)**. Todavía no existe ningún capítulo redactado. El estado detallado, las decisiones tomadas y el próximo paso exacto se registran en [`ESTADO.md`](ESTADO.md), que es el primer archivo que debe leerse al reanudar el trabajo.

## Organización del directorio

| Ruta | Contenido | Naturaleza |
|---|---|---|
| `PLAN_EDITORIAL.md` | Alcance de la colección, los 23 libros, índices por capítulo, prerrequisitos justificados y estimaciones | Interna |
| `LIBRO_DE_ESTILO.md` | Normas de redacción, estructura de capítulos, entornos formales, convenciones numéricas y de código | Interna |
| `NOTACION.md` | Convenciones de notación comunes a toda la colección | Interna |
| `GLOSARIO.md` | Terminología española fijada y su equivalente en inglés | Interna |
| `ESTADO.md` | Avance, decisiones aprobadas, pendientes y próximo paso | Interna |
| `editorial/` | Registro de revisiones, resultados admitidos, mapa de dependencias por capítulo (generado) y auditoría de la Fase 1 | Interna |
| `libros/` | Un directorio por libro; por ahora contiene los índices detallados (`indice.md`) de los 23 libros | **Producto** |
| `bibliografia/` | Bibliografía verificada (`atlas.bib`, fuente; `bibliografia.md`, versión legible generada) y registro de fuentes de datos y licencias (`fuentes_de_datos.md`) | **Producto** |
| `pdf/` | Versión PDF de todos los documentos, generada desde las fuentes Markdown; `pdf/entregas/` reúne cada entrega en un solo archivo | Entrega |
| `herramientas/` | Generación de los PDF de trabajo, verificador de coherencia de los índices (`verificar_indices.py`) y generador de la bibliografía legible (`bib_a_md.py`) | Interna |

## Principios

1. El centro de la obra es el libro. El código, los registros y las verificaciones existen para servir a la escritura.
2. Cada capítulo es comprensible para quien haya estudiado únicamente sus prerrequisitos declarados.
3. Ningún resultado se usa sin demostración salvo que esté declarado como resultado admitido, con referencia.
4. Ninguna referencia bibliográfica, cifra o salida de código se incluye sin verificación.
5. La obra se produce por etapas, con aprobación del director editorial en cada capítulo durante la primera etapa de producción.

## Autoría

Los créditos editoriales definitivos están pendientes. La propuesta aprobada en principio es la que figura en `PLAN_EDITORIAL.md`, sección 9.
