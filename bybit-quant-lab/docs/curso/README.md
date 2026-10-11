# Curso: bybit-quant-lab de cero a avanzado

Manual de aprendizaje y libro de referencia técnica construido sobre **el código real** de
este repositorio. Cada capítulo explica primero la idea con palabras sencillas, después la
terminología técnica, y finalmente el código que la implementa, con la ruta exacta del archivo
y los números de línea.

> Este curso es material educativo sobre un software de **investigación**. Nada de lo que
> contiene es una recomendación de inversión. El sistema no envía órdenes a ningún exchange y
> ninguna estrategia se ha validado con datos reales de mercado (ver Módulo XVII).

## Cómo leer este curso

- **Si empiezas desde cero:** lee los módulos en orden. Cada uno usa lo aprendido en el anterior.
- **Si buscas algo concreto:** usa el índice de abajo o el [glosario](glosario.md).
- **Si estás cansado:** cada lección empieza con una sección *La idea* que puedes leer sola.
  La profundidad técnica viene después y puedes volver a ella más tarde.
- **Tras cada concepto** hay una *Comprobación*: una pregunta o un ejercicio corto. La
  respuesta está plegada debajo (haz clic en "Ver respuesta"). Intenta responder antes de mirar.

## Convenciones

### Etiquetas de certeza

El curso distingue con cuidado entre lo que el código **demuestra** y lo que **supone**:

| Etiqueta | Significado |
|---|---|
| **[Hecho]** | Comportamiento comprobable leyendo el código o ejecutando las pruebas del repositorio. |
| **[Diseño]** | Una elección deliberada entre varias alternativas razonables. Se explica el porqué. |
| **[Supuesto]** | Algo que el código da por cierto pero que no se ha comprobado (por ejemplo, el formato real de la API de Bybit). |
| **[Limitación]** | Algo que el sistema no hace o hace de forma aproximada. |
| **[Pendiente]** | Algo que debe verificarse o implementarse antes de confiar en los resultados. |

### Citas de código verificadas

Los fragmentos de código del repositorio aparecen así:

```text
<!-- cita: src/bybit_quant_lab/<archivo>.py#L<inicio>-L<fin> -->
```

(con números de línea reales) seguido del bloque con esas líneas exactas. Ese comentario HTML
no se ve en un visor de Markdown; encima de cada cita el texto indica igualmente el archivo y
las líneas. Todas las rutas son relativas a la carpeta
`bybit-quant-lab/`. Las citas **no están copiadas a mano**: las rellena y las comprueba el
script `scripts/curso_citas.py`.

```bash
python scripts/curso_citas.py --check   # ¿siguen coincidiendo las citas con el código?
python scripts/curso_citas.py --fill    # actualiza citas y salidas tras cambiar el código
```

Si cambias el código, `--check` te dirá qué partes del curso quedaron desfasadas.

### Ejemplos ejecutables

Los bloques marcados como ejecutables se han ejecutado de verdad con el entorno del proyecto.
Su salida, que aparece debajo, es la salida real, no una salida inventada. Puedes copiarlos en
un archivo y ejecutarlos con `python archivo.py` desde la carpeta `bybit-quant-lab/`, con el
entorno virtual activado.

### Estado del repositorio que describe el curso

- Rama `claude/festive-franklin-jqcjz2`; el curso se escribió sobre el commit `30debc4`.
- Python 3.13, pandas 3.0, numpy 2.5 y pydantic 2.14 en el entorno donde se verificó.
- 231 pruebas superadas, ruff y mypy sin errores (las secciones 14.6, 14.7 y 14.10 explican qué significa eso).

## Índice

| Módulo | Contenido |
|---|---|
| [I. Entender el sistema](modulo-01-sistema.md) | Qué problema resuelve, vocabulario del trading sistemático, mapa de la arquitectura, recorrido de una vela |
| [II. Python aplicado al proyecto](modulo-02-python.md) | Tipos, funciones, clases, herencia, type hints, dataclasses, enumeraciones, excepciones, entornos virtuales |
| [III. Arquitectura e ingeniería de software](modulo-03-arquitectura.md) | Capas, dependencias, configuración, validación, errores, logging, CLI, persistencia |
| [IV. Conectividad con Bybit e ingeniería de datos](modulo-04-datos-bybit.md) | HTTP, el endpoint de velas, paginación, validación, Parquet, pruebas con respuestas simuladas |
| [V. pandas, NumPy y series temporales](modulo-05-pandas.md) | DataFrame, índices temporales, `shift`, `rolling`, NaN, huecos |
| [VI. Matemáticas y estadística](modulo-06-estadistica.md) | Rendimientos, dispersión, correlación, probabilidad, contrastes, bootstrap, sesgo de selección |
| [VII. Indicadores](modulo-07-indicadores.md) | EMA, ATR, RSI, MACD, Bollinger, StochRSI, ADX, OBV, VWAP, Donchian, volumen relativo |
| [VIII. Las diez estrategias](modulo-08-estrategias.md) | Hipótesis, reglas, código, ejemplos y limitaciones de cada estrategia |
| [IX. Combinación y regímenes](modulo-09-combinacion.md) | Votaciones, consenso, regímenes de mercado, redundancia |
| [X. El motor de backtesting](modulo-10-motor.md) | Señal frente a ejecución, costes, stops, gaps, una operación completa calculada a mano |
| [XI. Riesgo y contabilidad](modulo-11-riesgo.md) | Dimensionamiento, apalancamiento, margen, liquidación, límites diarios y drawdown |
| [XII. Métricas](modulo-12-metricas.md) | Sharpe, Sortino, drawdown, profit factor, CAGR y cómo no malinterpretarlos |
| [XIII. Validación y sobreajuste](modulo-13-validacion.md) | Train/validación/test, walk-forward, DSR, Holm, bootstrap, los errores de la auditoría |
| [XIV. Tests, calidad y depuración](modulo-14-tests.md) | Pruebas unitarias y de integración, mocks, ruff, mypy, escribir la prueba antes del arreglo |
| [XV. CLI, informes y uso práctico](modulo-15-cli.md) | Todas las órdenes `bql`, archivos que generan y un flujo completo de investigación |
| [XVI. Modificar el proyecto con autonomía](modulo-16-modificar.md) | Ejercicios guiados: parámetros, estrategias, indicadores, métricas, pruebas, git |
| [XVII. Limitaciones y camino a un sistema más riguroso](modulo-17-limitaciones.md) | Qué está corregido, qué falta, qué hay que verificar antes de confiar |
| [Glosario](glosario.md) | Todos los términos técnicos, con el módulo donde se explican |

## Ruta mínima si tienes poco tiempo

1. Módulo I completo (el mapa mental de todo lo demás).
2. Módulo X, secciones 10.1 a 10.6 (cómo se simula una operación).
3. Módulo XIII, secciones 13.1 a 13.4 (por qué un buen resultado histórico puede ser falso).
4. Módulo XVII (qué no debes creer todavía).
