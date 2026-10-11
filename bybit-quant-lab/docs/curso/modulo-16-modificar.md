# Módulo XVI. Leer y modificar el proyecto con autonomía

El objetivo de este módulo es que puedas abrir cualquier archivo del proyecto, entender qué
hace, seguir una ejecución de principio a fin y hacer un cambio **sin romper nada**. Incluye un
ejemplo resuelto (una estrategia nueva) y una serie de ejercicios graduados con solución.

> **[Hecho]** Durante la elaboración de este curso **no se ha modificado el código de
> producción**. El ejemplo resuelto define su estrategia en un bloque de código aparte, y los
> ejercicios describen los cambios para que los hagas tú, en tu propia rama.

---

## 16.1 Cómo leer un módulo que no conoces

1. **Cabecera (docstring del módulo).** En este proyecto casi todos los archivos empiezan con
   un texto que resume convenciones y supuestos (por ejemplo, `engine.py` líneas 1–20,
   `metrics.py` líneas 1–16). Léela entera antes que el código.
2. **Firmas públicas.** Funciones y clases sin guion bajo inicial: qué reciben y qué devuelven
   (las anotaciones de tipo ayudan, Módulo II).
3. **Pruebas.** Busca el nombre de la función en `tests/`: las pruebas son ejemplos de uso con
   resultados esperados, a menudo calculados a mano.
4. **Quién la llama.** `grep -rn "nombre_funcion" src/` muestra desde dónde se usa. Si nadie la
   llama, puede ser código sin efecto (Módulo III, sección 3.7).
5. **Ejecutar un caso mínimo** en un intérprete o un script, como en los bloques de este curso.

**¿Dónde está cada cosa?**

| Pregunta | Archivo |
|---|---|
| ¿Cómo se descargan las velas? | `data/bybit_client.py`, `data/downloader.py` |
| ¿Cómo se calcula el RSI? | `indicators/core.py` |
| ¿Cuándo entra una estrategia? | `strategies/<nombre>.py` (`compute_events`) y `strategies/base.py` (`events_to_state`) |
| ¿A qué precio se ejecuta? | `backtesting/engine.py`, `execution/costs.py`, `execution/fills.py` |
| ¿Cuánto se compra? | `risk/sizing.py` |
| ¿Cuándo deja de operar? | `risk/limits.py` |
| ¿Cómo se calcula el Sharpe? | `analytics/metrics.py` |
| ¿Cómo se elige lo mejor? | `validation/research.py` (`_select`) |
| ¿Qué hace cada orden `bql`? | `cli.py` |
| ¿Qué valores usa por defecto? | `config/models.py`, `configs/default.yaml`, `configs/strategies.yaml` |

---

## 16.2 Seguir una ejecución de principio a fin: `bql backtest`

```text
bql backtest --symbol BTCUSDT --timeframe 1h --strategy ema_crossover
│
├─ cli.main                                  cli.py 692–707: parsea y despacha
├─ cmd_backtest                              cli.py 239–301
│   ├─ _load_cfg → load_config               configuración validada (Pydantic)
│   ├─ _load_data                            Parquet + validate_ohlcv
│   ├─ Researcher(...)                       research.py 116–138: régimen y segmentos
│   ├─ strategy_candidate("ema_crossover")   research.py 141–147
│   │   └─ create_strategy                   strategies/registry.py 35–37
│   │       └─ Strategy.generate_signals     strategies/base.py 111–146
│   │           ├─ EMACrossoverStrategy.compute_events   ema_crossover.py 52–74
│   │           └─ events_to_state                       base.py 173–217
│   ├─ simulate (neto y bruto)               research.py 149–181
│   │   └─ BacktestEngine.run                engine.py 71–243
│   ├─ compute_metrics                       analytics/metrics.py 80–169
│   ├─ export_result, _save_run, metadata    reporting/export.py, cli.py 533–548
│   └─ backtest_report                       reporting/html.py 108–220
```

El registro de estrategias:

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/strategies/registry.py#L9-L37 -->
`src/bybit_quant_lab/strategies/registry.py` · líneas 9–37

```python
_REGISTRY: dict[str, type[Strategy]] = {}


def register(cls: type[Strategy]) -> type[Strategy]:
    """Decorador que registra una estrategia por su atributo ``name``."""
    if cls.name in _REGISTRY and _REGISTRY[cls.name] is not cls:
        raise ValueError(f"Estrategia duplicada: {cls.name}")
    _REGISTRY[cls.name] = cls
    return cls


def available_strategies() -> list[str]:
    """Nombres de estrategias registradas, en orden de registro."""
    return list(_REGISTRY)


def get_strategy_class(name: str) -> type[Strategy]:
    """Clase de estrategia por nombre."""
    try:
        return _REGISTRY[name]
    except KeyError as exc:
        raise KeyError(
            f"Estrategia desconocida: {name!r}. Disponibles: {available_strategies()}"
        ) from exc


def create_strategy(name: str, params: dict[str, Any] | None = None) -> Strategy:
    """Instancia una estrategia registrada con parámetros validados."""
    return get_strategy_class(name)(params or {})
```
<!-- fmt: on -->

`@register` es un **decorador** (Módulo II, sección 2.12): al definirse la clase, la añade al
diccionario `_REGISTRY` con su `name`. `strategies/__init__.py` importa los diez módulos para
que se registren al importar el paquete.

**Ejercicio de lectura.** Sigue la misma cadena para `bql compare` y anota en qué línea se
decide qué segmento se usa para seleccionar.

<details><summary>Ver respuesta</summary>

`cli.py` 304–345 → `Researcher.run_comparison` (`research.py` 244–299) →
`_select` (313–379). La línea 317 filtra `summary["segment"] == "validation"`.
</details>

---

## 16.3 Cómo hacer un cambio con seguridad

1. **Rama propia.** `git switch -c mi-cambio`. Nunca trabajes sobre la rama principal.
2. **¿Configuración o código?** Si el cambio se puede expresar en `configs/*.yaml` (parámetros,
   combinaciones, rejillas), hazlo ahí: no requiere tocar código y queda en los metadatos.
3. **Primero la prueba.** Escribe una prueba que **falle** con el código actual y describa el
   comportamiento deseado (como hizo la auditoría, Módulo XIV, sección 14.5).
4. **El cambio mínimo** que la haga pasar.
5. **Toda la suite y la calidad estática:** `pytest`, `ruff check .`, `ruff format --check .`,
   `mypy src`.
6. **Documentación.** Si cambia un comportamiento, actualiza la cabecera del módulo y el
   documento de `docs/` correspondiente. (Dos textos desactualizados sobre los umbrales de
   combinación muestran lo fácil que es olvidarlo, Módulo IX.)
7. **Resultados antiguos.** Un cambio en estrategias, costes o motor invalida las selecciones y
   resultados previos: el hash de configuración o de parámetros lo detecta en `final-test`,
   pero no en informes ya generados.

---

## 16.4 Ejemplo resuelto: una estrategia nueva sin tocar `src/`

Objetivo: añadir una estrategia de **momentum** (largo si el cierre supera el de hace N velas,
corto si es inferior) y comprobar que cumple el contrato y no mira el futuro. Se define en el
propio bloque, se registra en tiempo de ejecución y se simula en entrenamiento.

<!-- ejecutar -->
```python
import pandas as pd
from pydantic import Field

from bybit_quant_lab.analytics import compute_metrics
from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config.loader import load_config
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import (
    Category,
    Events,
    Strategy,
    StrategyParams,
    available_strategies,
    register,
)


class MomentumParams(StrategyParams):  # hereda stop, TP, trailing, cooldown...
    lookback: int = Field(48, ge=2, le=1000)


@register
class MomentumStrategy(Strategy):
    name = "momentum_demo"
    category = Category.TREND
    description = "Demostración: retorno de N velas positivo o negativo"
    params_model = MomentumParams
    params: MomentumParams

    def warmup_bars(self) -> int:
        return self.params.lookback + 1

    def compute_events(self, data: pd.DataFrame) -> Events:
        c = data["close"]
        mom = c / c.shift(self.params.lookback) - 1  # solo datos pasados
        up, down = mom > 0, mom < 0
        return Events(
            long_entry=up & ~up.shift(1, fill_value=False),  # transición, no nivel
            short_entry=down & ~down.shift(1, fill_value=False),
            long_exit=down,
            short_exit=up,
            conviction=(mom.abs() * 10).clip(0, 1),
        )


print("registrada:", "momentum_demo" in available_strategies())
datos = generate_synthetic_ohlcv(bars=3000, seed=7)
estrategia = MomentumStrategy({"lookback": 48})
senales = estrategia.generate_signals(datos)
print("contrato:", list(senales.columns))

for t in (400, 1100, 2203):  # misma técnica que la suite
    parcial = estrategia.generate_signals(datos.iloc[: t + 1])
    pd.testing.assert_frame_equal(senales.iloc[: t + 1], parcial, check_freq=False)
print("no look-ahead en 3 cortes: ok")

cfg = load_config()
res = run_backtest(datos, senales, cfg, "BTCUSDT", "1h", end=datos.index[1799])
m = compute_metrics(res, cfg.backtest.min_trades_for_stats, cfg.backtest.min_days_for_cagr)
print(
    {
        k: round(m[k], 4) if isinstance(m[k], float) else m[k]
        for k in ("num_trades", "net_profit", "sharpe", "max_drawdown", "exposure")
    }
)
print("motivos de salida:", res.trades["exit_reason"].value_counts().to_dict())
print("velas con señal distinta de 0:", int((senales["signal"].iloc[:1800] != 0).sum()), "de 1800")
print(
    "entradas rechazadas:",
    pd.Series([r["reason"] for r in res.rejected_signals]).value_counts().to_dict(),
)
print("eventos de riesgo:", len(res.risk_events))
```
<!-- salida -->
```text
registrada: True
contrato: ['signal', 'conviction', 'stop_distance', 'take_profit_distance', 'trailing_distance']
no look-ahead en 3 cortes: ok
{'num_trades': 62, 'net_profit': 592.6258, 'sharpe': 2.4225, 'max_drawdown': 0.0407, 'exposure': 0.1911}
motivos de salida: {'signal_reverse': 42, 'take_profit': 12, 'stop_loss': 7, 'end_of_data': 1}
velas con señal distinta de 0: 1752 de 1800
entradas rechazadas: {'loss_streak_pause': 31}
eventos de riesgo: 8
```

Lo que enseña el ejemplo:

- **Solo hay que escribir `compute_events`.** Stops, take profit, contrato de columnas, máquina
  de estados y anulación de entradas sin ATR válido los aporta la clase base.
- **La señal no es la exposición.** La estrategia quiere estar en el mercado casi siempre
  (señal distinta de 0 en casi todas las velas), pero la exposición real es del 19 %. Las
  causas se ven en la salida: el momentum cambia de signo a menudo, se acumulan rachas de tres
  pérdidas, el gestor de riesgo pausa las entradas 24 velas cada vez, y las entradas rechazadas
  **no se recuperan** porque el motor solo entra en transiciones (Módulos X y XI). Las salidas
  por stop o por objetivo (`take_profit_r` vale 2 por defecto en `StrategyParams`) también
  dejan la cuenta fuera hasta la siguiente transición.
- **[Hecho]** El resultado sobre datos sintéticos no dice nada sobre la estrategia (Módulo XII).
- **Para hacerla permanente**: crear `src/bybit_quant_lab/strategies/momentum_demo.py`,
  importarlo en `strategies/__init__.py`, añadir sus parámetros y rejilla al YAML y añadir su
  nombre a las pruebas. Ojo: `test_exactly_ten_strategies_registered` **fallará**, porque el
  encargo fija diez estrategias; habría que actualizar esa prueba conscientemente, no
  borrarla.
- El registro en tiempo de ejecución no persiste: la CLI no conoce `momentum_demo`.

---

## 16.5 Ejercicios graduados

Cada ejercicio indica el objetivo, los archivos, la prueba que deberías escribir primero y una
solución orientativa. Todos se refieren a hallazgos reales de este curso.

### Nivel 1. Lectura y configuración

**E1. ¿Dónde se decide "stop primero"?** Localiza la línea exacta y explica qué pasaría si se
invirtiera el orden de los dos `if`.

<details><summary>Solución</summary>

`execution/fills.py`, `check_intrabar_exit`, líneas 69–74: primero se comprueba el nivel
adverso (`low <= level`) y solo después el objetivo. Si se invirtiera, una vela que toca ambos
se registraría como `take_profit`: el backtest elegiría siempre el caso favorable.
</details>

**E2. Cambiar un parámetro sin tocar código.** Ejecuta `bql backtest` de `donchian_breakout`
con `--params '{"channel": 40}'` sobre datos sintéticos y compara con el valor por defecto (20).
¿Dónde queda registrado el parámetro usado?

<details><summary>Solución</summary>

En `metrics.json`/`run.json` (`params`), en `metadata.json` y en `outputs/experiments.jsonl`
(registro `evaluation` con `params`). Además, el informe HTML lo muestra en "Parámetros".
</details>

**E3. Cuantificar el veto de los pesos nulos (Módulo IX, sección 9.6).** Copia
`configs/strategies.yaml` a un archivo propio, añade `conflict_policy: net` a `weighted_train` y
ejecuta `bql --strategies-config mi.yaml compare ...`. Compara las velas en posición y el número
de operaciones de `weighted_train`.

<details><summary>Solución</summary>

Es un cambio de configuración, no de código. Con `net`, los miembros con peso 0 dejan de vetar.
La sección 9.6 midió un efecto relacionado (quitar esos miembros: de 307 a 2483 velas en
posición); con `net` cabe esperar un aumento de la exposición, pero hay que medirlo. Recuerda
que es **otra configuración** evaluada: `N` aumenta para el DSR.
</details>

### Nivel 2. Documentación y pruebas

**E4. Corregir los textos desactualizados sobre los umbrales.** `validation/research.py`
(líneas 7–8) y `reporting/html.py` (líneas 280–281) dicen que los umbrales se eligen con
validación. Escribe primero una prueba que lo detecte y después corrige los textos.

<details><summary>Solución</summary>

Prueba posible: leer `research.__doc__` y comprobar que no contiene "umbrales de la votación
ponderada se eligen **solo con validación**", y renderizar un informe de comparación para
comprobar que el texto no asocia "validación" a los umbrales. Cambio: "pesos, redundancia y
umbrales se ajustan con entrenamiento". Ninguna prueba numérica cambia.
</details>

**E5. Una prueba de contrato temporal.** Escribe una prueba que, para las diez estrategias y
datos sintéticos, compruebe en cada operación que `signal[entry_bar − 1]` es el lado de la
operación y que `entry_price == open[entry_bar] · (1 ± slip)`. (La auditoría lo hizo con un
script fuera de la suite; `docs/audit_report.md`, sección 6.)

<details><summary>Solución</summary>

Recorre `res.trades`; mapea `side` a ±1; compara con `senales["signal"].iloc[entry_bar - 1]`
y con `datos["open"].iloc[entry_bar] * (1 + lado * slip)` usando `pytest.approx`. Excluye las
entradas que no sean por transición (no las hay: todas lo son).
</details>

### Nivel 3. Cambios de comportamiento (cada uno cambia resultados)

**E6. `require_hist_rising` sin efecto en `macd_momentum` (Módulo VIII, sección 8.7).**

<details><summary>Solución</summary>

Prueba primero: con `require_hist_rising` verdadero y falso, las señales deben **diferir** en
la serie sintética (hoy son idénticas). Después, revisar la condición en `compute_events` para
que el parámetro intervenga, o eliminarlo del modelo y de la rejilla del YAML (línea 185) si se
decide que no aporta. Esta segunda opción también reduce el número de pruebas duplicadas.
</details>

**E7. Convicción constante en `donchian_breakout` (Módulo VIII, sección 8.5).**

<details><summary>Solución</summary>

Prueba: la convicción en las entradas no debe ser siempre 1. Cambio: aplicar el factor antes
del `clip` (o redefinir la fórmula). Recuerda que la convicción **no** afecta al tamaño
(Módulo IX, sección 9.8): solo afecta a `weighted_vote` con `use_conviction`.
</details>

**E8. Filtro de régimen sobre eventos, no sobre estados (Módulo IX, sección 9.10).**

<details><summary>Solución</summary>

Diseño: en lugar de forzar el **estado** a 0 fuera del régimen permitido, bloquear solo las
**entradas** en ese régimen y dejar que las posiciones abiertas salgan por sus propias reglas.
Prueba: con una estrategia en posición y un régimen que cambia a no permitido y vuelve, no debe
haber reentradas sin evento. Implica que `apply_regime_filter` trabaje sobre transiciones (o
que la combinación tenga su propia máquina de estados). Es un cambio de diseño: documéntalo.
</details>

**E9. Usar especificaciones verificadas (B-04).**

<details><summary>Solución</summary>

Añadir una opción (por ejemplo, `--spec-file` o una sección del YAML) para cargar una
`InstrumentSpec` construida con `spec_from_bybit` y pasarla al motor (`BacktestEngine(...,
spec=...)`, que ya la admite). Prueba: con una especificación `verified=True`, el resultado no
debe incluir la advertencia de especificaciones no verificadas.
</details>

**E10. Redondear stops y objetivos al tick.**

<details><summary>Solución</summary>

`InstrumentSpec` tiene `tick_size`, pero nadie lo usa. Añadir `round_price` (hacia el lado
conservador: stop de un largo hacia arriba, objetivo hacia abajo) y aplicarlo en `_open`
(`engine.py`, líneas 321–322). Prueba con `tick_size = 0.5` y distancias no múltiplos.
</details>

**E11. Huecos de datos (M-06).**

<details><summary>Solución</summary>

Opción mínima: que `_load_data` rechace (o advierta en el informe) datasets con
`missing_bars > 0`, con una opción explícita para aceptarlos. Opción completa: reindexar a la
rejilla temporal y tratar las velas ausentes en el motor (sin operar en ellas). Prueba: un
dataset con un hueco debe producir la advertencia o el error.
</details>

---

## 16.6 Lista de comprobación antes de confiar en un cambio

- [ ] Hay una prueba que fallaba antes y pasa ahora.
- [ ] `pytest`, `ruff check .`, `ruff format --check .` y `mypy src` sin errores.
- [ ] Las pruebas de no look-ahead siguen pasando para todas las estrategias.
- [ ] La cabecera del módulo y `docs/` describen el comportamiento nuevo.
- [ ] Si el cambio afecta a resultados, se han vuelto a ejecutar `compare` (y no se ha reutilizado
  un test final ya evaluado).
- [ ] El commit explica **por qué**, no solo qué.

### Comprobación final del módulo

Quieres probar si `rsi_reversion` funciona mejor con `oversold: 25`. ¿Qué harías, en qué orden y
qué no harías?

<details><summary>Ver respuesta</summary>

Haría: probarlo con `bql sensitivity --segment train` (o con un `--grid` pequeño), revisar la
estabilidad y, si se decide incluirlo, fijarlo en el YAML **antes** de `compare`. No haría:
mirar validación o test para decidir el valor, ni lanzar `final-test` con varias variantes. Cada
variante evaluada queda en el registro y aumenta `N`.
</details>
