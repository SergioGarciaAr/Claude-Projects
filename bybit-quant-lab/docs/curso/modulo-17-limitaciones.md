# Módulo XVII. Limitaciones reales y camino a seguir

Este módulo reúne en un solo lugar todo lo que el curso ha etiquetado como **[Limitación]**,
**[Supuesto]**, **[Pendiente]**, **[Discrepancia]** o hallazgo, y propone un orden de trabajo.
Distingue tres cosas que no deben mezclarse:

- **Defectos corregidos:** errores reales, demostrados con una prueba que fallaba, y arreglados.
- **Defectos y limitaciones pendientes:** conocidos, documentados y sin corregir.
- **Supuestos sin verificar:** decisiones razonables que solo los datos reales pueden confirmar.

---

## 17.1 Qué es el sistema hoy

**[Hecho]**

- Un framework de **investigación y backtesting** para perpetuos lineales USDT de Bybit, con
  diez estrategias, cinco formas de combinarlas, un motor determinista con costes, funding,
  stops y liquidación aproximada, gestión de riesgo independiente, métricas, validación
  cronológica, walk-forward, controles de sobreajuste, informes y CLI.
- 231 pruebas automáticas superadas, `ruff` y `mypy` sin errores (Módulo XIV).
- **No** ejecuta órdenes, **no** usa claves ni endpoints autenticados, **no** tiene modo
  testnet ni real.
- **Nunca se ha ejecutado con datos reales de Bybit.** El 11 de octubre de 2026, desde el entorno
  donde se escribió este curso, `curl https://api.bybit.com/v5/market/time` sigue devolviendo
  `CONNECT tunnel failed, response 403` (bloqueo del proxy del entorno, no de Bybit ni del
  código). La conectividad real **no está probada**.
- Todos los resultados numéricos del curso proceden de datos **sintéticos** o construidos a
  mano. No dicen nada sobre la rentabilidad de ninguna estrategia en el mercado real.

---

## 17.2 Defectos corregidos (con prueba que lo demuestra)

| Id | Defecto | Commit | Módulo |
|---|---|---|---|
| A-01 | Walk-forward sobre el período de test | `a50ac62` | XIII |
| A-02 | Guarda del test final por selección, no por período | `a50ac62` | XIII |
| A-03 | Selección no congelada; sin control de configuración | `a50ac62` | XIII |
| M-01 | Umbral de `weighted_vote` ajustado en validación | `a50ac62` | IX |
| M-02 | Gap más allá de la liquidación ejecutado como stop | `a50ac62` | X |
| M-03 | Bucle infinito posible en la paginación del funding | `a50ac62` | IV |
| M-04 | Entradas ficticias tras el calentamiento del ATR | `697b6af` | VIII |
| B-01 | Dos combinaciones idénticas | `a50ac62` | IX |
| B-02 | Benchmark aleatorio calibrado con toda la serie | `a50ac62` | XIII |
| B-03 | Walk-forward sin selección válida no señalado | `697b6af` | XIII |

Las once pruebas correspondientes fallan con el código anterior (`fc4e578`) y pasan con el
actual; la evidencia se reprodujo para este curso (Módulo XIV, sección 14.5).

---

## 17.3 Defectos y limitaciones pendientes de la auditoría

| Id | Qué | Consecuencia | Módulo |
|---|---|---|---|
| M-05 | Redundancia medida con Pearson sobre estados; categoría `indicator` heterogénea | `dedup_vote` usa las diez estrategias; el consenso por categorías puede contar dos veces la tendencia | IX |
| M-06 | Huecos en los datos | Ventanas de indicadores más largas en tiempo; posición mantenida a través del hueco; CAGR inflado | IV, XII |
| B-04 | Especificaciones verificadas no conectadas al motor | Paso de cantidad y mínimos de referencia, no reales | XI |
| B-05 | Supuestos del DSR (`N` acumulado y `V` actual; sin autocorrelación) | DSR aproximado | XIII |
| B-06 | `model_copy` no revalida | Configuraciones inválidas posibles desde código (no desde YAML/CLI) | II, XI |
| 7.4 | Sin cierres parciales, órdenes maker, cartera multiactivo, niveles de riesgo, impacto por tamaño | Simplificaciones del motor | X, XI |

---

## 17.4 Hallazgos nuevos de este curso

Revisando el código para escribir el curso aparecieron hallazgos que la auditoría no recogía.
Ninguno se ha corregido (la consigna era no modificar el código de producción); todos están
verificados con la versión actual.

**Afectan a resultados:**

| Hallazgo | Evidencia | Módulo |
|---|---|---|
| En `weighted_vote` con `veto`, los miembros con peso 0 vetan y aportan stop | 307 frente a 2483 velas en posición | IX, 9.6 |
| El filtro de régimen actúa sobre estados: crea reentradas sin evento y salidas forzadas | 9 de 17 entradas sin cambio en la estrategia; 11 salidas forzadas | IX, 9.10 |
| El régimen de tendencia no tiene histéresis | 185 cambios `trend`↔`range` en 6000 velas | IX, 9.9 |
| En `regime_switch`, el filtro **aumenta** la exposición al eliminar vetos | 737 → 2988 velas en posición | IX, 9.13 |
| `require_hist_rising` de `macd_momentum` no tiene efecto | Señales idénticas; la rejilla del YAML duplica configuraciones | VIII, 8.7; XIII |
| La convicción de `donchian_breakout` vale siempre 1 | 165 de 165 entradas | VIII, 8.5 |
| Con la configuración por defecto, solo el tope de margen limita el tamaño | 2,4 × equity < 3 × y 5 × | XI, 11.2 |
| Sin `configs/` en el directorio actual, la CLI usa valores del código y una combinación `vote_all` con `veto`, sin aviso | `cli.py`, líneas 64–98 | XV, 15.1 |

**Contables o de presentación:**

| Hallazgo | Módulo |
|---|---|
| En una liquidación, el margen de mantenimiento perdido se contabiliza como `slippage_cost` | X, 10.9 |
| `tick_size` no se usa: precios de stop y objetivo sin redondear | X, XI |
| La exposición no cuenta la vela de salida ni las operaciones dentro de una vela | XII, 12.7 |
| El CAGR usa días calculados por número de velas | XII, 12.5 |
| `bql report` regenera el informe sin benchmarks ni comparación bruto/neto | XV, 15.3 |
| `run_final_test` recibe combinaciones que no usa | XV, 15.3 |

**Documentación desactualizada o discrepante:**

| Texto | Realidad | Módulo |
|---|---|---|
| Cabecera de `validation/research.py` (líneas 7–8): umbrales "solo con validación" | Se eligen con entrenamiento (M-01) | IX, XIII |
| Informe HTML de `compare` (`html.py`, líneas 280–281): "validación (umbrales)" | Ídem | IX |
| `docs/progress.md` (línea 13): "11 órdenes" | La CLI tiene 12 | XV |
| `docs/audit_report.md` (sección 7, punto 5): otro `--output-dir` burla la guarda | El hash de configuración incluye las rutas y rechaza ese `final-test` con la misma selección | XV, 15.6 |
| Valores de referencia del DSR (0,1132 y 0,9004) "citados de memoria" | Siguen sin confirmar con la fuente (la búsqueda no los devolvió); la implementación sí está validada por Monte Carlo | XIII, 13.6 |

**Código sin efecto** (Módulo III, sección 3.7): `same_bar_policy`, `max_open_positions`,
`data.symbols`/`data.timeframes`, `maker_fee`, `BQL_BYBIT_BASE_URL`, `log_event`,
`Account.available_margin`/`history`, `Position.notional_entry`, `warmup_bars()` (nunca se
llama), el enum `Signal` (sin uso en `src`).

**De protocolo** (el código lo permite y lo registra, pero no lo impide): `backtest --segment
full`, sensibilidad en validación, walk-forward solapado con la validación, y un selector que no
usa DSR, Holm ni la dependencia de pocas operaciones.

---

## 17.5 Supuestos que solo los datos reales pueden confirmar

| Supuesto | Valor actual | Cómo verificarlo |
|---|---|---|
| Comisión taker | 0,055 % (tarifa base no VIP) | Tarifa vigente de la cuenta en Bybit |
| Deslizamiento | 2 bps fijos | Medir diferencial y profundidad en los horarios y tamaños reales |
| Funding | Valorado a `open` de la vela | Comparar con el cobro real (precio de marca) |
| Intervalo de funding | 8 h | Leer las marcas descargadas; Bybit puede cambiarlo |
| Liquidación | Mantenimiento fijo 0,5 % | Niveles de riesgo y fórmula de Bybit para el tamaño usado |
| Especificaciones | `DEFAULT_SPECS` | `instruments-info` (B-04) |
| Semántica de la API (`end`, orden, paginación del funding) | Según la documentación consultada al escribir el código | Descarga real y `validate-data` (Módulo IV, sección 4.18) |
| Disponibilidad histórica | Desconocida | `launchTime` y huecos reales |

---

## 17.6 Mejoras necesarias antes de confiar en los resultados

En orden. Cada paso es requisito del siguiente.

1. **Conectividad y datos reales.** Ejecutar desde una red con acceso a la API pública, descargar
   velas y funding, y revisar `validate-data` y el `.meta.json` (peticiones, rango, huecos).
   Contrastar unas cuantas velas con otra fuente.
2. **Especificaciones reales (B-04).** Conectar `spec_from_bybit` al motor para que el tamaño,
   los mínimos y la advertencia reflejen el instrumento real (ejercicio E9).
3. **Política de huecos (M-06).** Decidir si se rechazan los datos con huecos o cómo se tratan
   (ejercicio E11). Sin esto, indicadores y CAGR pueden ser engañosos.
4. **Costes realistas.** Fijar la comisión de la cuenta y estimar el deslizamiento por
   temporalidad y tamaño. Repetir `compare` con costes pesimistas: si el resultado solo existe
   con costes optimistas, no existe.
5. **Decisiones de diseño pendientes en las combinaciones.** Política de conflictos de
   `weighted_train` (veto de pesos nulos), filtro de régimen sobre eventos o estados, histéresis
   del régimen y medida de redundancia (M-05). Decidirlas **antes** de mirar resultados
   reales y dejarlas fijadas en el YAML.
6. **Corregir la documentación desactualizada** (ejercicio E4) y los parámetros sin efecto
   (E6), para que el número de pruebas que cuenta el DSR no incluya duplicados.
7. **Protocolo de decisión escrito.** Antes de ejecutar `compare` con datos reales: qué
   candidatos, qué rejillas, qué umbral de DSR y de número de operaciones se exigirán, y qué
   resultado se consideraría un fracaso. Así el selector, que no filtra por DSR, se complementa
   con una regla decidida de antemano.
8. **Robustez fuera de un solo mercado.** `bql markets` con BTCUSDT y ETHUSDT en varias
   temporalidades (solo entrenamiento y validación); desconfiar de lo que funciona en un único
   mercado.
9. **Un único test final**, con la selección congelada, y aceptación de su resultado aunque sea
   negativo. Conservar `outputs/experiments.jsonl`.
10. **Aun así, prudencia.** Un test final positivo es **una** muestra. Antes de cualquier uso
    real harían falta períodos adicionales no vistos y una evaluación de riesgos que está fuera
    del alcance de este proyecto, que por diseño no ejecuta órdenes.

---

## 17.7 Mejoras opcionales

No son requisitos para confiar en los resultados, pero los harían más informativos o el
proyecto más cómodo.

| Mejora | Beneficio | Coste |
|---|---|---|
| Redondeo de precios al tick (E10) | Realismo en niveles | Bajo |
| Benchmark aleatorio con muchas semillas | Distribución de referencia, no un solo sorteo | Medio (tiempo de cálculo) |
| Sharpe ajustado por autocorrelación (por ejemplo, el método de Lo, 2002) | DSR y comparaciones más honestos | Medio |
| Validación cruzada combinatoria con purga (López de Prado) | Más de un camino fuera de muestra | Alto |
| Datos de menor temporalidad para resolver la ambigüedad intravela | Menos dependencia de "stop primero" | Alto (volumen de datos) |
| Deslizamiento dependiente del tamaño y la volatilidad | Costes más realistas en temporalidades cortas | Medio |
| Órdenes límite (maker), cierres parciales | Más estrategias modelables | Alto (cambia el motor) |
| Cartera multiactivo | Diversificación | Alto (el motor es de una posición) |
| Más registro (logging) en motor y estrategias | Depuración | Bajo |
| Bucle del motor acelerado (por ejemplo, compilado) | Rejillas más grandes | Medio; más pruebas implican más sobreajuste |
| Avisar cuando la CLI no encuentra `configs/` | Evita resultados silenciosamente distintos | Bajo |

---

## 17.8 Lo que este proyecto no debe hacer

Por diseño y por las condiciones del encargo:

- No ejecutar órdenes reales ni en testnet.
- No solicitar ni almacenar claves privadas; ninguna credencial en el código ni en Git.
- No usar endpoints autenticados.
- No presentar resultados de datos sintéticos como evidencia de rentabilidad.
- No afirmar que la conectividad real está probada mientras no lo esté.

---

### Comprobación final del curso

Un compañero te enseña un informe de `bql compare` sobre datos reales con un candidato de Sharpe
3,2 en validación y te pide opinión. Enumera, en orden, las cinco primeras cosas que mirarías.

<details><summary>Ver respuesta</summary>

1. **Metadatos:** `data_synthetic` falso, commit sin cambios (`dirty`), hashes, rango de datos y
   advertencias (funding aplicado o no, especificaciones no verificadas).
2. **Número de operaciones** del candidato en validación y si el Sharpe se calculó (≥ 10
   operaciones, ≥ 30 velas).
3. **Neto frente a bruto** y costes supuestos (comisión, deslizamiento): ¿sobrevive con costes
   pesimistas?
4. **Controles estadísticos:** `n_trials`, DSR, Holm, intervalo bootstrap y dependencia de las
   tres mejores operaciones.
5. **Protocolo:** cuántas veces se ejecutó `compare` con esos datos (`experiments.jsonl`), si
   se usaron `--segment full`, sensibilidad en validación o un test final previo.

Solo después de todo eso tendría sentido hablar del Sharpe 3,2, y aun así sería una
hipótesis pendiente del test final.
</details>
