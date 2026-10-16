# Libro de estilo de Atlas Quant

Versión 1.0 · Fase 1a · 2026-10-15 · Aprobado el 2026-10-16

Este documento fija las normas de redacción de toda la colección. Se revisará después del capítulo piloto; los cambios se registrarán en `editorial/registro_de_revisiones.md`.

---

## 1. Finalidad

El libro de estilo existe para que veintitrés libros escritos a lo largo de varios años, en sesiones distintas, se lean como una sola obra. Fija la voz, la estructura de los capítulos, los entornos formales, la notación numérica, el uso del código y el procedimiento de revisión. Cuando una norma entre en conflicto con la claridad de una explicación concreta, prevalece la claridad y la excepción se registra.

## 2. Lector y nivel

Cada capítulo se escribe para un lector que ha estudiado únicamente los prerrequisitos declarados de ese capítulo y nada más. Esto obliga a tres cosas:

1. No presuponer conocimientos que no estén en los prerrequisitos, aunque sean «de cultura general» matemática.
2. Recordar brevemente, con referencia precisa, los resultados previos que se usan, en lugar de citarlos de forma vaga.
3. Ajustar el tamaño de los pasos al nivel del libro. En L1 y L2 los pasos son más pequeños, hay más ejemplos por concepto, cada demostración va acompañada de un ejemplo numérico y se repasan explícitamente los conocimientos previos. En las Series III a V los pasos pueden ser mayores, pero nunca se omite un razonamiento esencial.

## 3. Voz, registro y tono

- **Voz.** Primera persona del plural académica: «definimos», «veremos», «demostramos». Al lector se lo menciona en tercera persona («el lector») cuando hace falta.
- **Enunciados de ejercicios.** Imperativo en forma de *usted*: «Demuestre que…», «Calcule…», «Explique por qué…».
- **Variedad lingüística.** Español latinoamericano neutro. Se prefieren los términos de uso general en América Latina: *tasa de interés* (no *tipo de interés*), *valor presente* (no *valor actual*), *computadora* (no *ordenador*), *punto flotante* (no *coma flotante*). La terminología fijada está en `GLOSARIO.md`.
- **Tono.** Sobrio y preciso. Sin entusiasmo retórico, sin promesas de rentabilidad ni de empleabilidad, sin frases de relleno.
- **Expresiones prohibidas** cuando el paso es relevante para aprender: «es evidente», «es fácil ver», «trivialmente», «se deja al lector» (salvo en ejercicios explícitos), «por cálculo directo» sin mostrar el cálculo. Si un paso es realmente inmediato, se dice por qué lo es.

## 4. Cierre de prerrequisitos y resultados admitidos

**Regla de cierre.** Todo término, símbolo, técnica o resultado usado en un capítulo cumple una de estas condiciones:

1. está definido o demostrado en el propio capítulo;
2. está en un capítulo declarado como prerrequisito, y se cita por libro, capítulo y número de elemento (por ejemplo, «L2, Teorema 7.4»);
3. es un **resultado admitido**.

**Resultados admitidos.** Un resultado puede usarse antes de demostrarse solo si:

1. se presenta en un entorno «Resultado admitido» con enunciado preciso;
2. se indica dónde se demuestra en la obra o, si la demostración está fuera del alcance de la colección, una referencia externa verificada;
3. se registra en `editorial/resultados_admitidos.md`;
4. su demostración posterior no usa ningún resultado que dependa de él.

Los ejemplos pueden usar resultados admitidos; las demostraciones también, siempre que la cadena de dependencias no sea circular.

**Demostraciones parciales.** Cuando una demostración completa excede el nivel del libro, se demuestra el caso que sí está al alcance (por ejemplo, un caso particular o bajo hipótesis más fuertes), se dice explícitamente qué falta y se remite al lugar donde se completa.

## 5. Estructura de un capítulo

Cada capítulo desarrolla, según corresponda a su contenido, los elementos siguientes, integrados en prosa continua y no como secciones obligatorias:

1. **Introducción conceptual:** el problema que motiva el capítulo y por qué importa.
2. **Desarrollo gradual** desde los fundamentos necesarios.
3. **Definiciones precisas** y notación coherente con `NOTACION.md`.
4. **Derivaciones y demostraciones** completas, cada una precedida por una explicación de su estrategia.
5. **Intuición** que complementa el rigor: gráficos, casos numéricos, interpretaciones.
6. **Ejemplos resueltos** paso a paso.
7. **Aplicaciones financieras** cuando correspondan.
8. **Hipótesis, limitaciones y fallos:** cuándo el método deja de valer y qué ocurre entonces.
9. **Errores frecuentes:** su causa y cómo detectarlos.
10. **Síntesis** del capítulo y conexiones con capítulos posteriores.
11. **Ejercicios** graduados.
12. **Bibliografía** comentada del capítulo.

Cada capítulo comienza con una página de presentación que contiene sus prerrequisitos exactos (libro, capítulo y sección) y sus objetivos de aprendizaje, formulados como capacidades verificables («demostrar…», «calcular…», «decidir si…»).

Cada sección comienza planteando la pregunta que responde y termina conectando con la siguiente. Las listas solo se usan para contenido genuinamente enumerativo: hipótesis de un teorema, pasos de un algoritmo, casos de una definición.

**Extensión orientativa:** entre 25 y 40 páginas por capítulo, ejercicios incluidos. La extensión es consecuencia del contenido, no un objetivo.

## 6. Entornos formales

### 6.1 Tipos de entorno

| Entorno | Uso | Numeración |
|---|---|---|
| Definición | Introduce un término con significado preciso | Por capítulo |
| Teorema | Resultado central del capítulo | Por capítulo |
| Proposición | Resultado de importancia intermedia | Por capítulo |
| Lema | Resultado auxiliar para otra demostración | Por capítulo |
| Corolario | Consecuencia inmediata de un resultado previo | Por capítulo |
| Ejemplo | Ejemplo resuelto | Por capítulo |
| Ejercicio | Ejercicio de final de capítulo o intercalado | Por capítulo |
| Observación | Comentario, advertencia o matiz | Sin numerar |
| Demostración | Prueba de un enunciado; termina con ∎ | Sin numerar |
| Hipótesis de modelización | Supuesto que define un modelo, no un hecho matemático ni empírico | Por capítulo |
| Resultado empírico | Regularidad observada en datos, con fuente y período | Por capítulo |
| Resultado admitido | Véase la sección 4 | Por capítulo |
| Convención de mercado | Práctica estandarizada del mercado (conteo de días, cotización) | Sin numerar |

La distinción entre teorema, hipótesis de modelización, resultado empírico y convención de mercado es obligatoria. Un resultado empírico nunca se presenta como teorema ni una correlación como causalidad.

### 6.2 Sintaxis en el archivo fuente

La sintaxis sigue las convenciones de libros de Quarto para referencias cruzadas. Su funcionamiento en la composición a PDF se verificará en la prueba de composición de la Fase 2; hasta entonces, esta sección es provisional.

```markdown
::: {#def-interes-compuesto}
## Interés compuesto
Texto de la definición.
:::

::: {#thm-leyes-exponentes}
## Leyes de los exponentes enteros
Enunciado.
:::

::: {.proof}
Texto de la demostración.
:::

$$
C_n = C_0 (1 + i)^n
$$ {#eq-capital-compuesto}

Como muestra la @eq-capital-compuesto, …
```

Prefijos de etiqueta: `def`, `thm`, `prp`, `lem`, `cor`, `exm`, `exr`, `eq`, `sec`, `fig`, `tbl`. Las etiquetas usan minúsculas, sin tildes y con guiones, nunca guiones bajos (los guiones bajos causan problemas en la composición con LaTeX). Los entornos sin equivalente nativo en Quarto (Hipótesis de modelización, Resultado empírico, Resultado admitido, Convención de mercado) se marcan provisionalmente con las clases `.hipotesis`, `.empirico`, `.admitido` y `.convencion`; su presentación final se resolverá en la prueba de composición.

## 7. Demostraciones

1. Se enuncian todas las hipótesis en el enunciado, no dentro de la demostración.
2. Antes de una demostración no trivial, un párrafo explica la estrategia: qué se va a probar, por qué camino y por qué ese camino funciona.
3. Cada paso no inmediato se justifica citando el resultado o la propiedad que lo autoriza.
4. Las demostraciones largas se dividen en pasos con nombre.
5. Después de un teorema importante se discute qué ocurre si se elimina cada hipótesis, con contraejemplos cuando sea posible.
6. Las simulaciones nunca sustituyen una demostración. Cuando se usan, se dice qué muestran y qué no pueden mostrar.

## 8. Ecuaciones

- Se numeran solo las ecuaciones que se citan.
- Las ecuaciones forman parte de la oración y se puntúan como tal.
- Toda variable de una fórmula se define en el texto inmediato, con sus unidades cuando las tenga.
- En las fórmulas financieras se indica la convención temporal (anual, periódica, continua) y la unidad (tasa por período, años, unidades monetarias).

## 9. Ejemplos resueltos

Cada ejemplo resuelto sigue, en prosa, este recorrido: planteamiento del problema; elección del método y su justificación; desarrollo con todos los pasos relevantes; verificación del resultado (sustitución, caso límite, orden de magnitud o cálculo alternativo); interpretación. Los ejemplos se ordenan de menor a mayor dificultad. Todo valor numérico de un ejemplo se reproduce con un script de verificación interno antes de aprobar el capítulo.

## 10. Ejercicios y soluciones

**Cantidad:** entre 30 y 60 por capítulo.

**Tipo,** indicado con una etiqueta:

| Etiqueta | Tipo |
|---|---|
| [C] | Comprensión conceptual, explicación con palabras propias |
| [P] | Procedimiento y cálculo |
| [D] | Demostración |
| [A] | Aplicación financiera |
| [N] | Computación con Python |
| [E] | Detección de errores en una solución ajena |
| [S] | Síntesis y transferencia a situaciones nuevas |
| [I] | Problema abierto o de investigación |

**Dificultad:** ★ (aplicación directa), ★★ (requiere combinar ideas), ★★★ (exigente o abierto).

**Recuperación:** cada capítulo incluye algunos ejercicios que retoman contenidos de capítulos anteriores.

**Soluciones:** van en el solucionario del libro. Las demostraciones y aplicaciones reciben solución completa y razonada; los ejercicios rutinarios, respuesta y paso clave; los problemas abiertos, orientaciones. El libro incluye una selección de soluciones. Los ejercicios clásicos adaptados de otras obras se atribuyen a su fuente.

## 11. Aplicaciones financieras

- Las convenciones de mercado se presentan como convenciones, con la fuente y la fecha de verificación cuando dependen de una norma que puede cambiar.
- Los ejemplos con montos usan «u. m.» (unidades monetarias) salvo que el contexto exija una moneda concreta, en cuyo caso se usa su código ISO 4217 (USD, ARS, MXN…).
- Los datos reales se usan solo con fuente identificada y licencia compatible. Los datos hipotéticos se declaran como tales.
- Ningún ejemplo sugiere que un método garantiza rentabilidad.

## 12. Números, unidades y tipografía

| Norma | Regla | Ejemplo |
|---|---|---|
| Signo decimal en la prosa y en las fórmulas | Coma | 0,05; 3,1416 |
| Signo decimal en el código y en sus salidas | Punto | `0.05` |
| Separador de millares | Espacio fino no separable (U+202F) en números de más de cuatro cifras; sin separador en los de cuatro cifras | 2458; 12 345; 1 250 000 |
| Porcentaje | Espacio entre la cifra y el símbolo | 5 %; 12,5 % |
| Tuplas e intervalos numéricos | Punto y coma como separador cuando los componentes son numéricos | (0,5; 1,2); [0; 1] |
| Tuplas e intervalos simbólicos | Coma | (a, b); [x, y] |
| Coma decimal en LaTeX | `{,}` para evitar el espacio que LaTeX añade tras la coma | `0{,}05` |
| Separador de millares en LaTeX | `\,` | `12\,345` |
| Tasas en las fórmulas | Como fracción decimal; en la prosa, como porcentaje | i = 0,05 equivale a una tasa del 5 % |
| Fechas en la prosa | Forma completa | 15 de octubre de 2026 |
| Fechas en datos y código | ISO 8601 | `2026-10-15` |
| Extranjerismos no adaptados | Cursiva | *bootstrapping*, *swap* |

Cuando el libro muestra una salida de programa, advierte la primera vez en cada libro que en el código el separador decimal es el punto.

Fundamento: la coma decimal es válida según la normativa académica del español, que recomienda el punto pero admite ambos signos; la elección de la coma es una decisión editorial de la colección. Las normas sobre el separador de millares y el espacio antes de % se tomaron de la *Ortografía de la lengua española* (2010) y del *Diccionario panhispánico de dudas*; la verificación en la fuente primaria está pendiente (véase `ESTADO.md`).

## 13. Terminología

- La terminología fijada está en `GLOSARIO.md`. Un término fijado no se alterna con sinónimos.
- La primera vez que un término técnico aparece en cada libro se da su equivalente en inglés entre paréntesis y en cursiva: «cobertura (*hedging*)».
- Cuando no existe un término español establecido, se usa el inglés en cursiva y se registra en el glosario.
- Las siglas se desarrollan en su primera aparición en cada libro: «tasa interna de retorno (TIR)».

## 14. Código

- **Función.** El código es material didáctico: ilustra, verifica y aplica la teoría. Nunca reemplaza una demostración.
- **Lenguaje.** Python. La versión y las bibliotecas se fijarán en la Fase 2 y se declararán en el prefacio de cada libro.
- **Extensión.** Los fragmentos en el texto tienen como máximo unas 40 líneas. Las versiones completas van al material complementario del libro.
- **Explicación.** Cada fragmento va precedido de su objetivo y seguido de una explicación de sus partes relevantes, línea por línea cuando el lector es principiante (L1 a L4).
- **Salidas.** Se muestra la salida real de la ejecución, sin retoques. Un fragmento no ejecutado se marca expresamente como no verificado.
- **Estilo.** Nombres propios en español sin tildes ni eñes (`tasa`, `valor_presente`, `periodos`); comentarios en español; funciones con documentación breve; semillas aleatorias fijadas cuando haya aleatoriedad.
- **Prohibido:** claves, credenciales o datos personales en el código.

## 15. Figuras y tablas

Cada figura tiene un propósito explicativo que se enuncia en el texto, un pie de figura autosuficiente y se cita antes de aparecer. Las figuras generadas por código se producen con scripts guardados en el material complementario, para que puedan regenerarse. Las tablas llevan unidades en el encabezado.

## 16. Referencias bibliográficas

- Citas en formato autor-año.
- Toda referencia se verifica (autor, título, edición, editorial o revista, año e ISBN o DOI) antes de citarse; su estado se registra en la bibliografía.
- No se citan páginas, capítulos ni frases textuales sin haberlos comprobado.
- La exposición es propia: no se reproduce texto de otras obras. Los resultados y ejercicios clásicos se atribuyen.
- Cada capítulo distingue entre bibliografía fundamental, complementaria y avanzada.

## 17. Procedimiento de revisión de cada capítulo

Ningún revisor garantiza la corrección; la revisión aumenta la probabilidad de encontrar errores.

1. **Ficha de diseño** (interna, previa a la redacción): pregunta central, prerrequisitos exactos, resultados a demostrar, ejemplos y ejercicios previstos, conexiones posteriores.
2. **Autorrevisión** con la lista de verificación de la sección 18.
3. **Verificación independiente del texto:** todos los valores numéricos de ejemplos y soluciones se recalculan con scripts; el código se ejecuta; las derivaciones se comprueban simbólicamente cuando es posible.
4. **Revisión adversarial** por un agente con contexto limpio, cuando esté autorizada (autorizada para el piloto). Recibe solo el capítulo y sus prerrequisitos; su tarea es encontrar errores e intentar romper cada demostración, no calificar el texto. Cada hallazgo se resuelve contra la derivación, el cálculo o la fuente.
5. **Revisión del director editorial** y aprobación del capítulo.
6. **Revisión humana externa** en los hitos que se decidan.
7. **Registro** de hallazgos, severidad y resolución en `editorial/registro_de_revisiones.md`.

**Severidad de los hallazgos:**

- *Crítico:* error matemático o financiero que produce un resultado incorrecto; demostración inválida; dependencia circular; referencia inexistente; salida de código no ejecutada presentada como real.
- *Importante:* hipótesis omitida; prerrequisito no cubierto; ejercicio sin relación con los objetivos; solución insuficiente; límite de un modelo no declarado.
- *Menor:* notación inconsistente, redacción, formato.

Ningún capítulo se aprueba con hallazgos críticos abiertos.

## 18. Lista de verificación del capítulo

- [ ] La página de presentación declara prerrequisitos exactos y objetivos verificables, coherentes con el índice detallado del libro.
- [ ] `herramientas/verificar_indices.py` no informa errores.
- [ ] Todo término y símbolo está definido en el capítulo o en sus prerrequisitos.
- [ ] Los resultados admitidos están marcados, referenciados y registrados.
- [ ] Cada teorema enuncia todas sus hipótesis; cada demostración está completa o declarada parcial.
- [ ] Ninguna demostración depende de un resultado posterior que dependa de ella.
- [ ] Cada variable de una fórmula está definida, con unidades.
- [ ] Todos los valores numéricos fueron verificados con un script.
- [ ] Todo el código fue ejecutado y sus salidas son reales.
- [ ] Teoremas, hipótesis de modelización, resultados empíricos y convenciones están distinguidos.
- [ ] Hay discusión de limitaciones y errores frecuentes.
- [ ] Los ejercicios cubren los objetivos, con tipos y dificultades variados, e incluyen recuperación.
- [ ] Las soluciones están completas según la política de la sección 10.
- [ ] Las referencias están verificadas.
- [ ] La notación y la terminología coinciden con `NOTACION.md` y `GLOSARIO.md`.
- [ ] Las normas numéricas de la sección 12 se cumplen.
- [ ] No hay listas donde corresponde prosa ni frases de relleno.
