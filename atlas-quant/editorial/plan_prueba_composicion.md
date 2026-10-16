# Plan de prueba de composición

Fase 2 · Versión 1.0 · 2026-10-16 · Para aprobación del director (decisión D-04)

Este plan propone cómo elegir el sistema con que se compondrán los libros, es decir, cómo se pasa del texto fuente a los PDF definitivos (y, si se aprueba, a una versión HTML). Mientras no se apruebe no se instala nada. Los PDF que se entregaron hasta ahora son documentos de trabajo generados con pandoc y Chromium. No sirven para los libros: no numeran teoremas ni ecuaciones, no resuelven referencias cruzadas por número, no generan índice analítico y no ejecutan código.

## 1. Requisitos de la composición

Los requisitos se derivan del `LIBRO_DE_ESTILO.md`. Los marcados con **(E)** son eliminatorios: una candidata que no los cumpla queda descartada.

| ID | Requisito |
|---|---|
| R-01 (E) | Entornos formales numerados (definición, teorema, lema, proposición, corolario, ejemplo, observación, ejercicio) y demostración con marca de fin, con referencias cruzadas por número («Teorema 8.3») dentro de un capítulo y entre capítulos |
| R-02 (E) | Ecuaciones numeradas por capítulo, con referencias cruzadas |
| R-03 (E) | Tipografía española: división silábica, comillas latinas, coma decimal en matemáticas sin espacio espurio (`0{,}5`), espacio fino como separador de millares, espacio antes de %, títulos de entornos en español |
| R-04 (E) | Bibliografía generada desde `bibliografia/atlas.bib`, con citas autor-año y términos en español |
| R-05 (E) | Ejecución del código Python del libro durante la compilación, con la salida insertada; una salida que no pueda regenerarse no se publica (regla de verificación del libro de estilo) |
| R-06 (E) | Compilación reproducible: versiones fijadas, instalación por guion y sin pasos manuales |
| R-07 | Calidad tipográfica de la matemática: fórmulas largas, matrices, alineaciones, sistemas por casos, sub- y superíndices anidados |
| R-08 | Solucionario desde la misma fuente: las soluciones viven junto a los ejercicios y se compilan en un volumen aparte |
| R-09 | Índice analítico generado desde marcas en el texto |
| R-10 | Figuras generadas por código con rotulación en español (coma decimal en los ejes) |
| R-11 | Bloques de código con resaltado, numeración opcional y salida diferenciada |
| R-12 | PDF accesible: texto etiquetado, marcadores, texto alternativo de figuras y fórmulas; idealmente PDF/UA |
| R-13 | Versión HTML con MathML, secundaria |
| R-14 | Fuentes con licencia que permita incrustarlas en una obra publicada (por ejemplo, SIL Open Font License) |
| R-15 | Tiempo de compilación de un libro de 400 páginas compatible con revisiones frecuentes |

## 2. Situación del entorno (medida el 2026-10-16)

| Origen | Acceso | Qué ofrece |
|---|---|---|
| conda-forge (`conda.anaconda.org`) | Accesible | Quarto 1.9.38, Typst 0.15.1, pandoc 3.12.1, texlive-core 2026-03-01 |
| Repositorio de Ubuntu 24.04 (`archive.ubuntu.com`) | Accesible | TeX Live empaquetado por Ubuntu (LuaLaTeX, idioma español, paquetes científicos), fuentes |
| PyPI (`pypi.org`, `files.pythonhosted.org`) | Accesible | Pila de Python (matplotlib, scipy, sympy, Jupyter) |
| `raw.githubusercontent.com` | Accesible | Estilos de cita CSL |
| `github.com`, `api.github.com`, descargas de versiones | Bloqueado | Instaladores oficiales de Quarto y Typst; el paquete `quarto-cli` de PyPI descarga desde aquí, así que tampoco sirve |
| `quarto.org`, `mirror.ctan.org`, `ctan.org` | Bloqueado | Instalador de Quarto; gestor de paquetes de TeX Live (`tlmgr`) |
| `packages.typst.org` (Typst Universe) | Bloqueado | Paquetes de Typst. Quarto usa uno de ellos (*theorion*) para los teoremas en Typst |
| Instalado | — | pandoc 3.1.3; Python 3.13 con numpy 2.5.3 y pandas 3.0.5; Node 22; Chromium; 30 GB libres en disco |

**Consecuencias.**

- Quarto, Typst y pandoc recientes pueden instalarse descargando directamente los paquetes de conda-forge y extrayéndolos en un directorio de herramientas fuera del repositorio, sin gestor de conda.
- TeX Live puede instalarse desde Ubuntu, pero sin `tlmgr`: solo estarán disponibles los paquetes que Ubuntu empaquete.
- No hay acceso a los paquetes de Typst Universe salvo que se amplíe la red (sección 9).

El contenedor es efímero y lo instalado se pierde al reciclarlo. Por eso la instalación será un guion versionado (`herramientas/instalar_composicion.sh`) que fija versiones y sumas de verificación. Opcionalmente, ese guion puede usarse como guion de preparación del entorno.

## 3. Candidatas

| ID | Cadena | Componentes | Instalable hoy |
|---|---|---|---|
| C0 | Línea base actual: pandoc → HTML → Chromium | Ya instalada | Sí |
| C1 | Quarto → Typst | Quarto 1.9.38 con su Typst incluido; Jupyter para ejecutar código | Sí, salvo los paquetes de Typst Universe |
| C2 | Quarto → LuaLaTeX | Quarto 1.9.38; TeX Live de Ubuntu; Jupyter | Sí |
| C3 | pandoc → Typst, sin Quarto | pandoc 3.12.1; Typst 0.15.1; plantilla y filtros Lua propios; ejecutor de código propio | Sí |
| C4 | pandoc → LuaLaTeX, sin Quarto | pandoc 3.12.1; TeX Live de Ubuntu; filtros Lua propios; ejecutor de código propio | Sí |

C0 no cumple R-01, R-02 ni R-05 y se mantiene solo como referencia de comparación. La decisión aprobada en la Fase 0 situaba a Quarto como opción principal, por lo que C1 y C2 son las candidatas centrales. C3 y C4 miden cuánto cuesta prescindir de Quarto: exigen escribir y mantener un ejecutor de código y filtros para entornos y referencias cruzadas.

**Hipótesis previa, que la prueba debe confirmar o refutar.**

- C2 debería dar la mejor tipografía matemática y el índice analítico y la bibliografía más maduros, a cambio de compilaciones más lentas.
- C1 debería compilar mucho más rápido, pero en este entorno sus teoremas dependen de un paquete inaccesible (*theorion*), salvo que Quarto lo incluya en su distribución, lo que la prueba verificará.

## 4. Documento de prueba

Se escribirá un documento de muestra en `pruebas/composicion/` con dos capítulos breves (unas 20 páginas en total). Su objetivo es ejercitar todos los requisitos, no adelantar el piloto.

- **Capítulo A**, de nivel L1:
  - definiciones, un teorema con demostración y un corolario sobre logaritmos;
  - números con coma decimal y separador de millares, porcentajes;
  - una tabla numérica alineada por la coma;
  - una figura generada con Python;
  - ejercicios con solución.
- **Capítulo B**, de nivel L18:
  - el enunciado y la demostración abreviada de la fórmula de Itô;
  - una alineación de varias líneas, una matriz y un sistema por casos;
  - una simulación con su salida;
  - referencias cruzadas al capítulo A.
- **Elementos comunes:**
  - portada y página de créditos con el texto aprobado sobre la asistencia de IA;
  - índice general, citas de `atlas.bib` y bibliografía, notas al pie;
  - un recuadro de advertencia;
  - entradas de índice analítico;
  - un volumen de soluciones generado desde la misma fuente.

El texto de la muestra es material de prueba. No forma parte de ningún libro ni pasa por el procedimiento de revisión de capítulos.

## 5. Procedimiento

1. **Instalación** con el guion versionado:
   - Quarto y sus dependencias (deno, dart-sass, esbuild, pandoc, typst), en las versiones declaradas en los metadatos del paquete de conda-forge, que se leerán antes de instalar;
   - pandoc 3.12.1 y Typst 0.15.1 por separado para C3;
   - TeX Live de Ubuntu: `texlive-luatex`, `texlive-latex-extra`, `texlive-lang-spanish`, `texlive-science`, `texlive-bibtex-extra`, `biber` y las fuentes elegidas;
   - un entorno virtual de Python con matplotlib, scipy, sympy y Jupyter (nbclient, ipykernel).
   - Antes de instalar se medirá el tamaño de descarga (`apt-get --print-uris`) y se informará si supera 3 GB.
   - Todo queda fuera del repositorio, en `~/atlas-herramientas/`. Las versiones exactas se registran en `herramientas/versiones_composicion.txt`.
2. **Escritura de la muestra** en la sintaxis común de pandoc y Quarto (divs `::: {#thm-...}`), para que C1–C4 compilen la misma fuente con adaptaciones mínimas y documentadas.
3. **Compilación** de la muestra y del solucionario con cada candidata, en limpio, tres veces. Se registran tiempo, tamaño del PDF, fuentes incrustadas (`pdffonts`), etiquetado y errores o avisos.
4. **Prueba de escala.** La muestra se replica hasta unas 400 páginas para medir el tiempo de compilación de un libro completo (R-15).
5. **Revisión visual** con una lista de 30 comprobaciones derivada de la sección 1. Se acompaña de capturas de las páginas críticas: teoremas, ecuaciones largas, tabla, figura, código, bibliografía, índice analítico y solucionario.
6. **Informe comparativo** con la evaluación de la sección 6 y una recomendación.

## 6. Evaluación

Primero se descartan las candidatas que no cumplen un requisito eliminatorio. Las restantes se puntúan de 0 a 5 en cada criterio.

| Criterio | Peso |
|---|---|
| Calidad tipográfica de la matemática y del texto (R-03, R-07, R-14) | 25 % |
| Facilidad de instalación y mantenimiento con la red actual (R-06) | 15 % |
| Legibilidad y estabilidad de la fuente para la redacción diaria | 15 % |
| Solucionario e índice analítico (R-08, R-09) | 15 % |
| Accesibilidad y versión HTML (R-12, R-13) | 10 % |
| Madurez, documentación y comunidad | 10 % |
| Tiempo de compilación (R-15) | 10 % |

Si dos candidatas quedan a menos de 0,2 puntos de distancia, se prefiere la que tenga menos código propio que mantener.

## 7. Entregables de la prueba

- `pruebas/composicion/`: fuente de la muestra, configuración por candidata y guion de compilación.
- `herramientas/instalar_composicion.sh` y `herramientas/versiones_composicion.txt`.
- PDF de la muestra y del solucionario por candidata, más el informe comparativo con mediciones y capturas: `editorial/informe_composicion.md`, en PDF.
- Una propuesta de decisión D-04b (cadena elegida) y de las modificaciones consiguientes del libro de estilo (sintaxis definitiva de entornos, referencias e índice). Ningún cambio al libro de estilo se aplica sin aprobación.

## 8. Riesgos

| Riesgo | Mitigación |
|---|---|
| El paquete de conda-forge de Quarto depende de componentes que no se instalan bien fuera de conda | Leer los metadatos y probar primero la extracción. Si falla, pedir que se amplíe la red al instalador oficial (sección 9) |
| Los teoremas de Quarto en Typst requieren *theorion*, alojado en un registro bloqueado | Verificar si Quarto lo incluye. Si no, usar una plantilla de teoremas propia en Typst o descartar C1 por R-01 |
| A TeX Live de Ubuntu le falta algún paquete necesario | Lista de paquetes verificada antes de instalar. Sustituir por equivalentes disponibles o incluir el paquete en el repositorio si su licencia lo permite |
| Pérdida de lo instalado al reciclarse el contenedor | Guion de instalación versionado y reproducible |
| La muestra no representa bien los capítulos reales | La prueba se repetirá sobre el capítulo piloto L1 c. 8 antes de aprobarlo |

## 9. Lo que se solicita

1. **Aprobación de este plan (D-04)**, incluidas las instalaciones de la sección 5, todas fuera del repositorio.
2. **Ampliación opcional de la red del entorno** (D-07). No es necesaria para empezar, pero mejora la prueba:
   - `packages.typst.org`, para los paquetes de Typst que usa Quarto;
   - `github.com` y sus dominios de descarga, para los instaladores oficiales de Quarto y Typst;
   - `doi.org` y `api.crossref.org`, que además resolverían D-06.
   - El cambio lo hace el director en la configuración del entorno: menú del entorno en la barra de título de la sesión → Edit → Network access, nivel de acceso o dominios permitidos. Instrucciones: <https://code.claude.com/docs/en/cloud-environments#network-access>.

Con la aprobación se ejecuta la prueba completa. Después se entrega el informe con la recomendación para decidir la cadena antes de redactar el piloto L1 c. 8.

## 10. Fuentes

- Quarto, formato Typst y teoremas con *theorion*: <https://quarto.org/docs/output-formats/typst.html>; notas de la versión 1.9: <https://quarto.org/docs/blog/posts/2026-03-24-1.9-release>.
- Quarto, referencias cruzadas: <https://quarto.org/docs/authoring/cross-references.html>.
- Typst 0.15 (MathML en la exportación HTML): <https://typst.app/blog/2026/typst-0.15>.
- Disponibilidad de paquetes: índice de conda-forge (`conda.anaconda.org/conda-forge/linux-64/current_repodata.json`) y PyPI (`pypi.org/pypi/quarto-cli/json`), consultados el 2026-10-16.
