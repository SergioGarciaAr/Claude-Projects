# Informe de la prueba de composición

Fase 2 · Versión 1.0 · 2026-10-16 · Ejecución del plan aprobado (D-04)

Este informe presenta los resultados de la prueba definida en `editorial/plan_prueba_composicion.md`: compilar con distintas cadenas una muestra que ejercita los requisitos R-01 a R-15. Con ellos se elige la cadena con que se compondrán los libros. La fuente, los guiones y los PDF resultantes están en `pruebas/composicion/`.

## 1. Instalación

Todo quedó en `~/atlas-herramientas/`, fuera del repositorio. El guion `herramientas/instalar_composicion.sh` reproduce la instalación, y `herramientas/versiones_composicion.txt` registra las versiones y las sumas SHA-256.

| Componente | Versión | Origen |
|---|---|---|
| Quarto | 1.9.38 | conda-forge, extraído con `herramientas/conda_extraer.py`; sus dependencias son pandoc 3.8.3, Typst 0.14.2, deno 2.4.5, dart-sass y esbuild |
| TeX Live | 2023 (paquetes de Ubuntu 2023.20240207) | Repositorio de Ubuntu 24.04: LuaLaTeX, español, paquetes científicos, fuentes; 902 MB de descarga |
| Python | numpy 2.5.4, pandas 3.0.6, matplotlib 3.11.2, scipy 1.18.1, sympy 1.14.0, ipykernel 7.4.0 | PyPI, entorno virtual |
| Fuentes | Libertinus Serif y Libertinus Math (licencia SIL OFL), DejaVu Sans Mono | TeX Live |

**Hallazgos de la instalación:**

- El paquete de Quarto para PyPI descarga el programa desde GitHub, que está bloqueado; por eso se usó conda-forge.
- La distribución de Quarto incluye los paquetes de Typst que necesita (*theorion* para teoremas y *orange-book* para libros), así que el bloqueo de `packages.typst.org` no afecta a C1.
- Estilo de cita: se usa APA 7 (`pruebas/composicion/estilos/apa.csl`, CC BY-SA 3.0), obtenido de `raw.githubusercontent.com`.

## 2. Muestra

La muestra es un libro de Quarto con dos capítulos breves:

- **Logaritmos, nivel L1:** definiciones, teoremas con demostración, un corolario, un recuadro de advertencia, una convención de mercado, un ejemplo financiero calculado por código, una tabla generada por código, una figura y tres ejercicios con solución.
- **Fórmula de Itô, nivel L18:** una alineación de varias líneas, una matriz, una definición por casos, un resultado admitido, una simulación de 100 000 trayectorias con semilla fija y referencias cruzadas al primer capítulo.

Además incluye créditos, bibliografía generada desde `bibliografia/atlas.bib`, índice analítico y solucionario compilado desde la misma fuente. La sintaxis es la del libro de estilo, más tres convenciones nuevas (sección 6 de este informe).

**Código propio escrito para la prueba:**

| Archivo | Función |
|---|---|
| `filtros/indice.lua` | Marcas de índice analítico |
| `filtros/solucionario.lua` | Separación de soluciones |
| `filtros/entornos.lua` | Entornos propios de la obra |
| `filtros/numeros.lua` | Coma decimal en Typst |
| `typst/indice.typ` | Índice analítico en Typst |
| `latex/preambulo.tex`, `latex/solucionario.tex` | Configuración de LaTeX |

## 3. Resultados por candidata

### C0. Línea base (pandoc → HTML → Chromium)

Descartada por R-01, R-02 y R-05: no numera teoremas ni ecuaciones y no ejecuta código. Se mantiene solo para los documentos de trabajo.

### C3 y C4. pandoc sin Quarto (→ Typst o → LuaLaTeX)

Al convertir la muestra con pandoc 3.8.3 sin Quarto, las referencias `@thm-…` y `@eq-…` se interpretan como citas bibliográficas inexistentes («citation thm-log-producto not found»). Además, no hay entornos de teorema numerados ni ejecución de código.

Cumplir R-01, R-02 y R-05 exigiría escribir y mantener lo que Quarto ya resuelve: numeración, referencias y ejecución de Jupyter. Quedan descartadas sin compilación completa, porque el resultado de esa compilación es conocido de antemano.

### C1. Quarto → Typst

Cumple:

- teoremas y ecuaciones numerados por capítulo, con referencias cruzadas entre capítulos, en el modo libro;
- bibliografía;
- ejecución de código;
- índice analítico, con 22 líneas de Typst propias;
- PDF etiquetado (`Tagged: yes`), un punto a favor de la accesibilidad (R-12);
- compilación muy rápida: 7 s la muestra y 28 s un libro de 263 páginas sin ejecutar código.

Defectos encontrados:

1. **Coma decimal.** Typst trata la coma de `0{,}5` como puntuación y añade un espacio («1, 301»). Se corrige con un filtro que convierte cada número decimal en un literal, aunque así se compone con la fuente del texto y no con la matemática.
2. **Localización.** La plantilla de libro (*orange-book* 0.7.1) escribe «Chapter 1.» en las cabeceras de página. Quarto no le pasa el idioma, y corregirlo exige sustituir la plantilla parcial.
3. **Fuente matemática.** La matemática se compone con New Computer Modern Math aunque el texto use Libertinus, y aparece una fuente de reserva (Unifont) para algún glifo.
4. **Solucionario.** No compila (R-08). Typst exige que toda referencia exista en el mismo documento y no tiene un mecanismo equivalente al paquete `xr` de LaTeX. Resolverlo requiere desarrollo propio: exportar las etiquetas del libro y reescribir las referencias.
5. **Diseño.** La plantilla impone un diseño (colores, recuadros de título) que habría que rehacer para la obra.

### C2. Quarto → LuaLaTeX

Cumple todos los requisitos eliminatorios y R-07 a R-11:

- teoremas, ecuaciones, tablas y figuras numerados por capítulo («Teorema 1.2», «Ecuación 2.3»), con referencias entre capítulos;
- títulos de los entornos en español;
- coma decimal correcta con `{,}`;
- espacio fino de millares y espacio antes de %;
- índice analítico nativo (`imakeidx`);
- bibliografía APA 7 en español;
- figuras vectoriales con la tipografía del texto y coma decimal en los ejes;
- código con resaltado y corte de líneas largas.

El solucionario compila desde la misma fuente. Conserva capítulos, ejercicios con su numeración y soluciones, y resuelve las referencias al libro («por el Teorema 1.1», «la Ecuación 1.4») con el paquete `xr`, que lee el archivo `.aux` del libro.

Defectos encontrados y corregidos durante la prueba:

| Defecto | Corrección |
|---|---|
| Títulos de sección en sans serif | Fuente del texto en los títulos (KOMA) |
| Punto final en los números de sección, añadido por el español de babel | `\autodot` vacío |
| Líneas de código que desbordan el margen | `fvextra` con corte de líneas |
| Guion en lugar de signo menos en tablas y figuras | Formateador con U+2212 |
| Glifos ausentes en la fuente de código | DejaVu Sans Mono |
| Error de babel (bidi) en LuaLaTeX al usar `amsthm` con nota opcional en entornos sin numerar | Entornos propios definidos como lista con título en línea |

Defectos abiertos:

1. **PDF sin etiquetar (R-12).** El etiquetado automático de LaTeX es posterior a TeX Live 2023, la versión que ofrece Ubuntu 24.04. Esta afirmación debe verificarse antes de decidir cómo cumplir R-12. Quarto 1.9 ofrece la opción `pdf-standard`, que no se probó.
2. **Lentitud relativa.** 18 s la muestra y 66 s un libro de 260 páginas sin ejecutar código. Es aceptable para R-15.
3. **APA 7 usa «&» entre autores.** Se adaptará el estilo a «y» en una copia propia (la licencia CC BY-SA lo permite).

## 4. Tiempos

Medidos en el contenedor de trabajo; detalle en `pruebas/composicion/resultados/tiempos.txt`.

| Compilación | C1 Typst | C2 LuaLaTeX |
|---|---|---|
| Muestra, libro (2 capítulos, con ejecución de código) | 7 s | 18 s |
| Muestra, solucionario | No produce PDF | 15 s |
| 80 capítulos (≈ 260 páginas), con ejecución de código | 228 s (263 p.) | 267 s (260 p.) |
| 80 capítulos, código congelado (solo composición) | 28 s | 66 s |

En un libro completo predomina la ejecución del código: unos 200 s por la simulación repetida 40 veces. Quarto puede congelar los resultados (`freeze`) para que las compilaciones de revisión no reejecuten el código.

## 5. Evaluación

| Criterio (peso) | C1 Typst | C2 LuaLaTeX |
|---|---|---|
| Calidad tipográfica (25 %) | 3 | 5 |
| Instalación y mantenimiento (15 %) | 4 | 3 |
| Legibilidad de la fuente (15 %) | 4 | 4 |
| Solucionario e índice analítico (15 %) | 2 | 5 |
| Accesibilidad y HTML (10 %) | 4 | 2 |
| Madurez (10 %) | 3 | 5 |
| Tiempo de compilación (10 %) | 5 | 3 |
| **Puntuación ponderada** | **3,45** | **4,05** |

C0, C3 y C4 se descartaron por requisitos eliminatorios. La diferencia entre C1 y C2 (0,60) supera el umbral de 0,2 del plan.

## 6. Decisión D-04b y consecuencias

**Cadena elegida: C2, Quarto 1.9.38 → LuaLaTeX (TeX Live 2023), con Libertinus Serif y Libertinus Math.** El director delegó las decisiones el 2026-10-16, y la elección se registra en `ESTADO.md`. La misma fuente sirve para una futura salida Typst o HTML, de modo que la decisión puede revisarse sin reescribir los libros.

Consecuencias para la producción:

1. **Sintaxis definitiva**, que se incorpora al libro de estilo (sección 6.2):
   - marcas de índice `[término]{.idx}` o `[]{.idx entrada="término"}`;
   - soluciones en `::: {.solucion}` inmediatamente después de su ejercicio;
   - entornos propios `.hipotesis`, `.empirico`, `.admitido` y `.convencion` con título opcional en un encabezado interno.
2. **Estructura de cada libro.** Cada libro es un proyecto de libro de Quarto con perfiles `libro` y `solucionario`. Los filtros y el preámbulo de la prueba pasan a ser la plantilla común, en `composicion/`.
3. **Código común del lector.** Un módulo de formato numérico y de estilo de figuras, compartido por todos los capítulos y publicado con el código complementario.
4. **Pendientes de la plantilla común:** adaptar APA 7 a «y», diseñar la portada y las cabeceras, y comprobar el etiquetado PDF (R-12).
5. **Documentos de trabajo.** Los PDF de los documentos editoriales siguen generándose con C0. Los capítulos se componen con C2 desde el piloto L1 c. 8.
