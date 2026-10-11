# Módulo XII. Métricas de rendimiento y riesgo

Una simulación produce una curva de equity y una lista de operaciones. Las **métricas** resumen
esas dos tablas en números comparables. Este módulo explica cada métrica del proyecto: qué
mide, cómo se calcula, cuándo no se calcula y cómo se malinterpreta.

Código: `src/bybit_quant_lab/analytics/metrics.py` y `analytics/breakdowns.py`. Documentación
de referencia: `docs/metrics.md`, coherente con el código en la versión actual.

> **[Hecho]** Todas las cifras de este módulo proceden de ejemplos construidos a mano o de
> datos **sintéticos**. Ninguna dice nada sobre la rentabilidad de una estrategia en Bybit.

---

## 12.1 La cabecera: todas las convenciones en un lugar

<!-- cita: src/bybit_quant_lab/analytics/metrics.py#L1-L33 -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 1–33

```python
"""Cálculo de métricas. Fórmulas y convenciones (ver ``docs/metrics.md``):

* Retornos por vela: ``r_t = E_t / E_{t-1} - 1`` sobre la equity al cierre, incluyendo las
  velas sin posición (retorno 0). El primer retorno usa el capital inicial como ``E_{-1}``.
* Anualización: mercado 24/7, año de 365 días -> ``N = 525600 / minutos_por_vela``.
* Sharpe = ``mean(r) / std(r, ddof=1) * sqrt(N)`` con tasa libre de riesgo 0.
* Sortino = ``mean(r) / DD * sqrt(N)`` con ``DD = sqrt(mean(min(r, 0)^2))``.
* CAGR = ``(E_final / E_0)^(365 / días) - 1`` solo si ``días >= min_days_for_cagr``.
* Profit factor = suma de ganancias netas / |suma de pérdidas netas|.
* Expectativa = media del PnL neto por operación.
* Exposición = fracción de velas con posición abierta al cierre.
* Rotación = nocional negociado total / equity media.

Las métricas que no pueden calcularse válidamente se devuelven como ``None`` y se añade una
advertencia. Una muestra pequeña de operaciones también genera advertencia.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

from bybit_quant_lab.backtesting.results import BacktestResult
from bybit_quant_lab.timeframes import bars_per_year

MIN_BARS_FOR_RATIOS = 30
#: Con menos operaciones (y exposición no continua) Sharpe/Sortino no se presentan: con
#: 1-9 operaciones la serie de retornos está dominada por unos pocos episodios.
MIN_TRADES_FOR_RATIOS = 10
CONTINUOUS_EXPOSURE = 0.9
```

Dos decisiones condicionan todo lo demás:

1. **Los retornos se calculan por vela sobre la equity**, no por operación. Incluyen las velas
   sin posición (retorno 0). El Sharpe mide la estrategia **completa**, incluido el tiempo en
   efectivo.
2. **El año tiene 525 600 minutos** (365 × 24 × 60), porque el mercado cripto no cierra:

<!-- cita: src/bybit_quant_lab/timeframes.py#L18-L18 -->
`src/bybit_quant_lab/timeframes.py` · líneas 18–18

```python
MINUTES_PER_YEAR = 365 * 24 * 60  # mercado cripto 24/7, año de 365 días
```

<!-- cita: src/bybit_quant_lab/timeframes.py#L43-L45 -->
`src/bybit_quant_lab/timeframes.py` · líneas 43–45

```python
def bars_per_year(timeframe: str) -> float:
    """Número de velas por año (365 días, 24 h)."""
    return MINUTES_PER_YEAR / timeframe_minutes(timeframe)
```

| Temporalidad | Velas por año (`N`) | √N |
|---|---|---|
| 5m | 105 120 | 324,22 |
| 15m | 35 040 | 187,19 |
| 1h | 8 760 | 93,59 |
| 4h | 2 190 | 46,80 |

**[Diseño]** En acciones se usan 252 días hábiles; aplicar ese número a cripto infravaloraría
la anualización. La tasa libre de riesgo se fija en 0.

---

## 12.2 Retornos por vela

<!-- cita: src/bybit_quant_lab/analytics/metrics.py#L36-L40 -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 36–40

```python
def bar_returns(equity: pd.Series, initial: float) -> pd.Series:
    """Retornos simples por vela, empezando desde el capital inicial."""
    prev = equity.shift(1)
    prev.iloc[0] = initial
    return equity / prev - 1
```

```text
r_t = E_t / E_{t−1} − 1,      con E_{−1} = capital inicial
```

`shift(1)` desplaza la serie una posición (Módulo V); el primer valor, que quedaría `NaN`, se
sustituye por el capital inicial.

**[Hecho]** La primera fila de equity de cualquier simulación es el capital inicial: en la
primera vela del segmento no puede haber posición, porque toda entrada se decide al cierre de
una vela y se ejecuta en la siguiente (Módulo X). El primer retorno es, por tanto, 0.

---

## 12.3 Sharpe y Sortino

**Intuición.** El **ratio de Sharpe** responde: "¿cuánto retorno obtengo por cada unidad de
variabilidad?". Dos estrategias que ganan lo mismo no son iguales si una lo hace con
oscilaciones enormes. El **Sortino** solo penaliza la variabilidad **a la baja**: subir mucho no
debería contar como riesgo.

**Fórmulas** (con `r` = retornos por vela, `n` = número de velas, `N` = velas por año):

```text
Sharpe  = media(r) / desv(r, ddof=1) · √N
Sortino = media(r) / DD · √N,      DD = √( media( min(r, 0)² ) )
```

- `ddof=1` divide entre `n − 1` (desviación muestral, Módulo VI).
- `DD` (*downside deviation*) promedia sobre **todas** las velas, poniendo 0 en las positivas.
- `√N` convierte un ratio por vela en anual, **suponiendo** retornos independientes entre velas.

<!-- cita: src/bybit_quant_lab/analytics/metrics.py#L95-L111 -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 95–111

```python
    sharpe = sortino = None
    exposure = float(result.equity["in_position"].mean()) if n_bars else 0.0
    few_trades = n_trades < MIN_TRADES_FOR_RATIOS and exposure < CONTINUOUS_EXPOSURE
    if few_trades:
        warnings.append(
            f"Solo {n_trades} operaciones (< {MIN_TRADES_FOR_RATIOS}) con exposición no "
            "continua: Sharpe/Sortino no se presentan por no ser representativos."
        )
    elif n_bars >= MIN_BARS_FOR_RATIOS:
        std = float(rets.std(ddof=1))
        if std > 0:
            sharpe = float(rets.mean() / std * math.sqrt(ann))
        downside = float(np.sqrt(np.mean(np.minimum(rets.to_numpy(), 0.0) ** 2)))
        if downside > 0:
            sortino = float(rets.mean() / downside * math.sqrt(ann))
    else:
        warnings.append(f"Menos de {MIN_BARS_FOR_RATIOS} velas: Sharpe/Sortino no calculados.")
```

**Cálculo a mano.** Cinco velas de 1 h con retornos `r = [0; 0,01; −0,01; 0,02; 0]`:

```text
media     = (0 + 0,01 − 0,01 + 0,02 + 0) / 5 = 0,004
desvíos   = −0,004; 0,006; −0,014; 0,016; −0,004
cuadrados = 16; 36; 196; 256; 16   (× 10⁻⁶)   → suma = 520 × 10⁻⁶
varianza  = 520 × 10⁻⁶ / 4 = 130 × 10⁻⁶       → desv = 0,0114018
Sharpe por vela = 0,004 / 0,0114018 = 0,35082
Sharpe anual    = 0,35082 × √8760 = 0,35082 × 93,5949 = 32,84

DD        = √( (0² + 0² + 0,01² + 0² + 0²) / 5 ) = √(2 × 10⁻⁵) = 0,0044721
Sortino   = 0,004 / 0,0044721 × 93,5949 = 83,71
```

<!-- ejecutar -->
```python
import math

import numpy as np

r = np.array([0.0, 0.01, -0.01, 0.02, 0.0])
n_anual = 365 * 24
sharpe = r.mean() / r.std(ddof=1) * math.sqrt(n_anual)
dd = math.sqrt(np.mean(np.minimum(r, 0) ** 2))
sortino = r.mean() / dd * math.sqrt(n_anual)
print(f"Sharpe = {sharpe:.2f}   Sortino = {sortino:.2f}")
```
<!-- salida -->
```text
Sharpe = 32.84   Sortino = 83.71
```

Un Sharpe de 32 es absurdo: cinco velas no permiten estimar nada. Por eso el código **no
calcula** los ratios:

- con menos de 30 velas (`MIN_BARS_FOR_RATIOS`, línea 29), o
- con menos de 10 operaciones **y** una exposición inferior al 90 % (líneas 97–102). Con pocas
  operaciones, la serie de retornos está dominada por unos pocos episodios. La excepción de
  exposición continua existe para los benchmarks como comprar y mantener, que tienen una sola
  "operación" pero están en el mercado todo el tiempo.

En esos casos la métrica vale `None` y se añade una advertencia. El informe muestra "n/d", no
un número.

**[Limitación]** `√N` supone retornos independientes. Las posiciones que duran varias velas
producen retornos autocorrelacionados, y el Sharpe anualizado puede quedar sesgado. No se
corrige (`docs/metrics.md`, "Validez y muestras pequeñas").

**Error común.** Comparar un Sharpe calculado por operación con uno calculado por vela, o uno de
5m con uno de 4h sin entender la anualización. Dentro del proyecto todos se calculan igual.

**Comprobación.** Si en el ejemplo se añaden 5 velas más con retorno 0 (sin posición), ¿sube o
baja el Sharpe?

<details><summary>Ver respuesta</summary>

Baja. La media pasa de 0,004 a 0,002 (misma suma, el doble de velas); la desviación también
baja, pero menos (de 0,0114 a ≈ 0,0079). Resultado ≈ 23,7. El tiempo sin posición diluye el
retorno medio por vela.
</details>

---

## 12.4 Drawdown: profundidad, duración y recuperación

<!-- cita: src/bybit_quant_lab/analytics/metrics.py#L43-L73 -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 43–73

```python
def drawdown_stats(equity: pd.Series) -> dict[str, Any]:
    """Drawdown máximo, duración máxima (velas) y velas de recuperación del máximo drawdown."""
    if equity.empty:
        return {
            "max_drawdown": 0.0,
            "max_dd_duration_bars": 0,
            "max_dd_recovery_bars": None,
            "max_dd_start": None,
            "max_dd_trough": None,
            "max_dd_end": None,
        }
    values = equity.to_numpy(float)
    peak = np.maximum.accumulate(values)
    dd = values / peak - 1
    trough = int(np.argmin(dd))
    peak_idx = int(np.argmax(values[: trough + 1])) if trough > 0 else 0
    rec = np.nonzero(values[trough:] >= peak[trough])[0]
    recovery = int(rec[0]) if len(rec) else None
    longest, cur = 0, 0
    for under in dd < 0:
        cur = cur + 1 if under else 0
        longest = max(longest, cur)
    idx = equity.index
    return {
        "max_drawdown": max(0.0, float(-np.min(dd))),
        "max_dd_duration_bars": longest,
        "max_dd_recovery_bars": recovery,
        "max_dd_start": str(idx[peak_idx]),
        "max_dd_trough": str(idx[trough]),
        "max_dd_end": str(idx[trough + recovery]) if recovery is not None else None,
    }
```

**Términos.**

- **Drawdown** en `t`: `1 − E_t / máximo(E_0..E_t)`. Cuánto se ha caído desde el último máximo.
- **Máximo drawdown:** el mayor drawdown de toda la serie.
- **Duración máxima:** la racha más larga de velas **consecutivas** por debajo del máximo previo.
- **Recuperación:** velas desde el **valle** del máximo drawdown hasta volver al máximo previo.
  `None` si no se recupera dentro del período.

**Cálculo a mano** (`test_drawdown_duration_and_recovery_by_hand`):

| Vela | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Equity | 100 | 110 | 99 | 95 | 105 | 111 | 108 | 112 |
| Máximo previo | 100 | 110 | 110 | 110 | 110 | 111 | 111 | 112 |
| Drawdown | 0 | 0 | 10,0 % | **13,6 %** | 4,5 % | 0 | 2,7 % | 0 |

- Máximo drawdown = 1 − 95/110 = 13,64 %: pico en la vela 1, valle en la 3.
- Recuperación: desde la vela 3, el primer valor ≥ 110 es 111 en la vela 5 → **2 velas**.
- Duración máxima: velas 2, 3 y 4 bajo el máximo → **3**. (La vela 6 forma una racha de 1.)

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.analytics import drawdown_stats

idx = pd.date_range("2024-01-01", periods=8, freq="1h", tz="UTC")
s = pd.Series([100, 110, 99, 95, 105, 111, 108, 112], index=idx, dtype=float)
for clave, valor in drawdown_stats(s).items():
    print(f"{clave:22s} {round(valor, 4) if isinstance(valor, float) else valor}")
```
<!-- salida -->
```text
max_drawdown           0.1364
max_dd_duration_bars   3
max_dd_recovery_bars   2
max_dd_start           2024-01-01 01:00:00+00:00
max_dd_trough          2024-01-01 03:00:00+00:00
max_dd_end             2024-01-01 05:00:00+00:00
```

**Detalles del código.**

- **55:** `np.maximum.accumulate` es el máximo acumulado (como `cummax` en pandas).
- **58:** el pico es la **primera** posición del máximo antes del valle.
- **62–64:** la duración se calcula con un bucle de racha; **no** tiene por qué corresponder al
  episodio del máximo drawdown. Un drawdown poco profundo pero largo puede dar la duración
  máxima.

**Comprobación.** ¿Puede la duración máxima ser mayor que la distancia entre el pico y la
recuperación del máximo drawdown?

<details><summary>Ver respuesta</summary>

Sí. Son dos medidas distintas: la duración es la racha más larga bajo el agua de **cualquier**
episodio; la recuperación se refiere solo al episodio del drawdown más profundo.
</details>

---

## 12.5 CAGR

```text
CAGR = (E_final / E_0)^(365 / días) − 1,      días = velas × minutos_por_vela / 1440
```

<!-- cita: src/bybit_quant_lab/analytics/metrics.py#L112-L116 -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 112–116

```python
    cagr = None
    if days >= min_days_for_cagr and final > 0:
        cagr = (final / init) ** (365.0 / days) - 1
    else:
        warnings.append(f"Período de {days:.0f} días < {min_days_for_cagr}: CAGR no calculado.")
```

**Intuición.** La tasa de crecimiento anual compuesta que habría producido el mismo resultado.

**Por qué exige 180 días.** Ganar un 5 % en 10 días, anualizado, da
`1,05^(36,5) − 1 ≈ 494 %`. Es una extrapolación sin sentido. Con menos de
`min_days_for_cagr` (180) días, la métrica es `None`.

**[Limitación]** `días` se calcula con el **número de velas**, no con el calendario. Si faltan
velas (huecos, M-06), los días se subestiman y el exponente `365/días` crece: el CAGR queda
inflado.

---

## 12.6 Métricas por operación

<!-- cita: src/bybit_quant_lab/analytics/metrics.py#L123-L166 -->
`src/bybit_quant_lab/analytics/metrics.py` · líneas 123–166

```python
    net = trades["net_pnl"].astype(float) if n_trades else pd.Series(dtype=float)
    wins, losses = net[net > 0], net[net < 0]
    gross_win, gross_loss = float(wins.sum()), float(-losses.sum())
    dd = drawdown_stats(eq)
    gross_total = float(trades["gross_pnl"].sum()) if n_trades else 0.0
    m: dict[str, Any] = {
        "label": result.label,
        "symbol": result.symbol,
        "timeframe": result.timeframe,
        "start": str(result.start) if result.start is not None else None,
        "end": str(result.end) if result.end is not None else None,
        "bars": n_bars,
        "days": round(days, 2),
        "initial_capital": init,
        "final_equity": final,
        "net_profit": final - init,
        "net_profit_pct": final / init - 1,
        "gross_profit_before_costs": gross_total,
        "cumulative_return": final / init - 1,
        "cagr": _safe(cagr) if cagr is not None else None,
        "sharpe": _safe(sharpe) if sharpe is not None else None,
        "sortino": _safe(sortino) if sortino is not None else None,
        **dd,
        "num_trades": n_trades,
        "win_rate": float((net > 0).mean()) if n_trades else None,
        "avg_win": float(wins.mean()) if len(wins) else None,
        "avg_loss": float(losses.mean()) if len(losses) else None,
        "profit_factor": (gross_win / gross_loss) if gross_loss > 0 else None,
        "expectancy": float(net.mean()) if n_trades else None,
        "expectancy_pct_equity": float(trades["return_on_equity"].mean()) if n_trades else None,
        "exposure": exposure,
        "turnover": result.totals["traded_notional"] / float(eq.mean()) if n_bars else 0.0,
        "total_fees": result.totals["fees"],
        "total_slippage": result.totals["slippage"],
        "total_costs": result.totals["fees"] + result.totals["slippage"],
        "total_funding": result.totals["funding"],
        "funding_applied": result.funding_applied,
        "avg_bars_in_trade": float(trades["bars_held"].mean()) if n_trades else None,
        "long_trades": int((trades["side"] == "LONG").sum()) if n_trades else 0,
        "short_trades": int((trades["side"] == "SHORT").sum()) if n_trades else 0,
        "rejected_signals": len(result.rejected_signals),
        "risk_events": len(result.risk_events),
        "warnings": warnings + list(result.warnings),
    }
```

**Cálculo a mano** con las doce operaciones de `test_metrics_match_hand_computation`:
`[50, −20, 30, −10, −40, 80, 15, −5, 25, −30, 60, −12]`.

```text
ganadoras  = 50 + 30 + 80 + 15 + 25 + 60 = 260     (6 operaciones)
perdedoras = 20 + 10 + 40 + 5 + 30 + 12  = 117     (6 operaciones)
win_rate      = 6 / 12 = 0,50
avg_win       = 260 / 6 = 43,33
avg_loss      = −117 / 6 = −19,50
profit_factor = 260 / 117 = 2,222
expectancy    = (260 − 117) / 12 = 11,917
```

**Relación entre ellas:** `expectancy = win_rate · avg_win + (1 − win_rate) · avg_loss =
0,5 · 43,33 + 0,5 · (−19,5) = 11,917`.

**Tasa de acierto de equilibrio.** Con ganancia media G y pérdida media P (en valor absoluto),
la expectativa es 0 cuando `win_rate = P / (G + P)`. Con G = 43,33 y P = 19,5: 31 %. Una
estrategia puede acertar solo un 37 % y ganar si sus ganadoras son grandes (sección 12.9).

**Detalles.**

- **147:** `win_rate` cuenta solo `net_pnl > 0`; una operación con PnL exactamente 0 no es
  ganadora.
- **150, 167–168:** sin perdedoras, el profit factor es `None` con advertencia (dividir entre 0).
- **152:** `expectancy_pct_equity` es la media de `net_pnl / equity_al_entrar`: permite comparar
  operaciones de épocas con distinto capital.
- **154:** `turnover = nocional negociado / equity media`. Un turnover de 70 significa que se
  negoció 70 veces el capital medio: mide cuánto trabajan los costes.
- **157:** `total_costs` = comisiones + deslizamiento; el funding va aparte.
- **160:** `avg_bars_in_trade` cuenta la vela de entrada y la de salida (`bars_held = salida −
  entrada + 1`; en la sección 10.10, 3 velas).

**Error común.** Mirar solo la tasa de acierto o solo el profit factor. Un PF de 3 con 4
operaciones no significa nada; una tasa de acierto del 80 % con pérdidas medias diez veces
mayores que las ganancias medias pierde dinero.

---

## 12.7 Exposición

```text
exposición = fracción de velas con posición abierta al CIERRE
```

**[Hecho]** Una operación abierta y cerrada dentro de la misma vela (stop intravela en la vela
de entrada) aporta 0 a la exposición, y la vela de salida tampoco cuenta (sección 10.10). La
exposición es, por tanto, una cota inferior del tiempo real en el mercado.

---

## 12.8 Desgloses

<!-- cita: src/bybit_quant_lab/analytics/breakdowns.py#L8-L24 -->
`src/bybit_quant_lab/analytics/breakdowns.py` · líneas 8–24

```python
def breakdown_trades(trades: pd.DataFrame, by: str) -> pd.DataFrame:
    """Agrega operaciones por la columna ``by`` (``side``, ``exit_reason``, ``regime``...)."""
    cols = ["trades", "net_pnl", "avg_net_pnl", "win_rate", "fees", "funding"]
    if trades.empty or by not in trades.columns:
        return pd.DataFrame(columns=cols)
    g = trades.groupby(by, dropna=False)
    out = pd.DataFrame(
        {
            "trades": g.size(),
            "net_pnl": g["net_pnl"].sum(),
            "avg_net_pnl": g["net_pnl"].mean(),
            "win_rate": g["net_pnl"].apply(lambda s: float((s > 0).mean())),
            "fees": g["fees"].sum(),
            "funding": g["funding"].sum(),
        }
    )
    return out.sort_values("net_pnl", ascending=False)
```

`groupby(by, dropna=False)` agrupa por dirección (`side`), motivo de salida (`exit_reason`) o
régimen al entrar (`regime`); `dropna=False` conserva un grupo para valores ausentes. El informe
HTML genera las tres tablas (`reporting/html.py`, línea 192).

---

## 12.9 Ejemplo completo sobre una simulación

Simulación de `donchian_breakout` con los parámetros del YAML sobre las 3600 primeras velas
(el segmento de entrenamiento) de la serie sintética de 6000 velas, semilla 42, configuración
por defecto. Después se recalcula el Sharpe a mano a partir de la equity:

<!-- ejecutar -->
```python
import math

import numpy as np

from bybit_quant_lab.analytics import breakdown_trades, compute_metrics
from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
params = load_strategy_params("configs/strategies.yaml")["donchian_breakout"]
senales = create_strategy("donchian_breakout", params).generate_signals(datos)
cfg = load_config()
res = run_backtest(datos, senales, cfg, "BTCUSDT", "1h", end=datos.index[3599])
m = compute_metrics(res, cfg.backtest.min_trades_for_stats, cfg.backtest.min_days_for_cagr)

claves = ["bars", "days", "num_trades", "net_profit", "gross_profit_before_costs",
          "total_costs", "total_funding", "sharpe", "sortino", "max_drawdown",
          "max_dd_duration_bars", "max_dd_recovery_bars", "win_rate", "avg_win", "avg_loss",
          "profit_factor", "expectancy", "exposure", "turnover", "cagr"]
for k in claves:
    v = m[k]
    print(f"{k:26s} {round(v, 4) if isinstance(v, float) else v}")
print("advertencias:")
for w in m["warnings"]:
    print("  -", w)

eq = res.equity["equity"].to_numpy()
r = np.r_[eq[0] / res.initial_capital - 1, eq[1:] / eq[:-1] - 1]
print("Sharpe recalculado a mano:", round(r.mean() / r.std(ddof=1) * math.sqrt(8760), 4))
print(breakdown_trades(res.trades, "exit_reason").round(2).to_string())
```
<!-- salida -->
```text
bars                       3600
days                       150.0
num_trades                 87
net_profit                 1765.7616
gross_profit_before_costs  2363.5379
total_costs                597.7763
total_funding              0.0
sharpe                     2.171
sortino                    3.1519
max_drawdown               0.0888
max_dd_duration_bars       995
max_dd_recovery_bars       None
win_rate                   0.3678
avg_win                    200.8803
avg_loss                   -84.771
profit_factor              1.3787
expectancy                 20.2961
exposure                   0.585
turnover                   73.351
cagr                       None
advertencias:
  - Período de 150 días < 180: CAGR no calculado.
  - Sin datos históricos de funding: no se aplica (no se simula). El resultado neto excluye el coste/ingreso de funding.
  - Especificaciones de BTCUSDT no verificadas con instruments-info (valores de referencia).
Sharpe recalculado a mano: 2.171
                trades  net_pnl  avg_net_pnl  win_rate    fees  funding
exit_reason                                                            
signal_exit         25  2127.55        85.10      0.52  119.74      0.0
signal_reverse       8   527.47        65.93      0.62   42.65      0.0
stop_loss           54  -889.26       -16.47      0.26  275.97      0.0
```

Cómo leerlo:

1. **Contabilidad.** `gross_profit_before_costs − total_costs = net_profit` (sin funding,
   porque no hay datos de funding y la advertencia lo dice). Los costes se llevan una parte
   importante del resultado bruto; el turnover alto lo explica.
2. **Sharpe.** El valor recalculado coincide con el de `compute_metrics`.
3. **Tasa de acierto baja con profit factor > 1.** Es el perfil típico de las estrategias de
   ruptura: muchas pérdidas pequeñas y pocas ganancias grandes (sección 12.6).
4. **`stop_loss` con tasa de acierto > 0.** Con `trailing_atr_mult`, el "stop" puede haberse
   movido por encima de la entrada: algunas salidas por stop **protegen ganancias**. El motivo
   de salida no distingue stop inicial y trailing.
5. **CAGR `None`.** 150 días < 180.
6. **Recuperación `None`.** El máximo drawdown no se recuperó dentro del segmento.
7. **Lo que no dice.** El generador sintético (`data/synthetic.py`) alterna bloques de 300
   velas (`regime_length`): alcista con deriva de +0,08 % por vela, lateral, bajista con deriva
   de −0,08 % y lateral de alta volatilidad. La mitad del tiempo hay una deriva sostenida y
   artificial, un entorno favorable a las estrategias de tendencia. Este resultado **no** es evidencia de que la estrategia funcione en
   BTCUSDT; solo muestra cómo se calculan y leen las métricas. Además, es un resultado de
   **entrenamiento**: no sirve para seleccionar (Módulo XIII).

---

## 12.10 Resumen

| Métrica | Pregunta que responde | Cuándo no se calcula | Trampa principal |
|---|---|---|---|
| Sharpe | Retorno por unidad de variabilidad | < 30 velas; < 10 operaciones sin exposición continua | Autocorrelación; selección múltiple (DSR, Módulo XIII) |
| Sortino | Igual, solo variabilidad negativa | Igual | Parece mejor que el Sharpe casi siempre |
| Máx. drawdown | Peor caída desde un máximo | — | Medido al cierre; dentro de la vela puede ser peor |
| CAGR | Crecimiento anual equivalente | < 180 días | Huecos en datos lo inflan |
| Profit factor | Ganancias / pérdidas | Sin perdedoras | Inestable con pocas operaciones |
| Win rate | Frecuencia de acierto | Sin operaciones | No dice nada sin el tamaño de ganancias y pérdidas |
| Exposición | Tiempo en el mercado | — | Cota inferior |
| Turnover | Cuánto se negocia | — | Multiplica el efecto de los costes |

### Comprobación final del módulo

Una estrategia tiene 40 operaciones, tasa de acierto 30 %, ganancia media 300 y pérdida media
−100. ¿Cuál es su expectativa y su profit factor?

<details><summary>Ver respuesta</summary>

Expectativa = 0,3 · 300 + 0,7 · (−100) = 90 − 70 = **20** por operación. Ganadoras: 12 × 300 =
3600; perdedoras: 28 × 100 = 2800; **PF = 3600 / 2800 ≈ 1,29**. Antes de concluir nada habría
que mirar el intervalo de confianza (bootstrap, Módulo XIII) y la dependencia de las mejores
operaciones.
</details>
