# Módulo VIII. Las diez estrategias, una por una

Este módulo dedica un capítulo a cada estrategia. Antes, la sección 8.0 explica lo que todas
comparten: la clase base, los stops y cómo se convierte una señal en una operación simulada.

> **[Hecho] Advertencia general.** Que una estrategia produzca señales y pase sus pruebas solo
> demuestra que **implementa correctamente su regla**. No demuestra que la regla gane dinero. En
> este repositorio **ninguna** estrategia se ha evaluado con datos reales de mercado. Todos los
> ejemplos usan datos sintéticos o escenarios construidos a mano.

Las diez estrategias registradas (nombre interno, categoría y descripción):

<!-- ejecutar -->
```python
from bybit_quant_lab.strategies import available_strategies, get_strategy_class

for nombre in available_strategies():
    clase = get_strategy_class(nombre)
    print(f"{nombre:20s} {clase.category.value:10s} {clase.description}")
```
<!-- salida -->
```text
adx_di               indicator  Dirección por +DI/-DI cuando ADX indica tendencia suficiente
bollinger_reversion  indicator  Reversión tras reingreso confirmado en las bandas de Bollinger
donchian_breakout    trend      Ruptura del canal Donchian de velas anteriores con gestión ATR
ema_crossover        trend      Cruce EMA rápida/lenta con filtro de tendencia y de lateralidad
macd_momentum        indicator  Cambio de momentum por cruce MACD/señal confirmado por histograma
obv_trend            volume     Cruce del OBV sobre su EMA confirmado por pendiente y precio
rsi_reversion        indicator  Reversión a la media por salida de sobreventa/sobrecompra del RSI
stoch_rsi            indicator  Cruces del Stochastic RSI en zonas extremas con confirmación
volume_spike         volume     Pico de volumen confirmado por vela direccional y ruptura del rango previo
vwap_deviation       volume     Desviación del precio respecto a VWAP con régimen de volumen (reversión o continuación)
```

**[Hecho]** El orden en que aparecen es el orden de importación en `strategies/__init__.py`
(alfabético). Los capítulos siguen la numeración del encargo original (volumen, tendencia,
indicadores).

---

## 8.0 Lo que comparten todas las estrategias

### Del evento a la señal: `generate_signals`

Cada estrategia solo implementa `compute_events`, que devuelve cinco series: entrada larga,
entrada corta, salida larga, salida corta y convicción. El resto lo hace la clase base:

<!-- cita: src/bybit_quant_lab/strategies/base.py#L111-L146 -->
`src/bybit_quant_lab/strategies/base.py` · líneas 111–146

```python
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Devuelve el DataFrame de señales normalizadas (ver docstring del módulo)."""
        validate_input(data)
        if data.empty:
            return empty_signal_frame(data.index)
        ev = self.compute_events(data)
        p = self.params
        long_entry, short_entry = _clean_bool(ev.long_entry), _clean_bool(ev.short_entry)
        if not p.allow_short:
            short_entry = pd.Series(False, index=data.index)
        atr_ = atr(data, p.atr_period)
        stop = atr_ * p.stop_atr_mult
        # Sin stop válido (calentamiento del ATR) no se permite ENTRAR. Se aplica a los eventos,
        # antes de la máquina de estados, para no crear transiciones ficticias después.
        valid_stop = stop.notna() & (stop > 0)
        long_entry &= valid_stop
        short_entry &= valid_stop
        state = events_to_state(
            long_entry,
            short_entry,
            _clean_bool(ev.long_exit),
            _clean_bool(ev.short_exit),
            max_holding_bars=p.max_holding_bars,
            cooldown_bars=p.cooldown_bars,
        )
        out = pd.DataFrame(index=data.index)
        out["signal"] = state.astype("int64")
        conv = ev.conviction.reindex(data.index).astype("float64").clip(0, 1).fillna(0.0)
        out["conviction"] = conv.where(out["signal"] != 0, 0.0)
        out["stop_distance"] = stop
        out["take_profit_distance"] = stop * p.take_profit_r if p.take_profit_r else np.nan
        out["trailing_distance"] = atr_ * p.trailing_atr_mult if p.trailing_atr_mult else np.nan
        # Sin stop válido (ATR aún no disponible) no se permite abrir: se fuerza FLAT.
        out.loc[out["stop_distance"].isna() | (out["stop_distance"] <= 0), "signal"] = 0
        out.loc[out["signal"] == 0, "conviction"] = 0.0
        return out
```

- **113–115:** valida las columnas y el orden; con datos vacíos devuelve una tabla neutral.
- **116:** llama a la estrategia concreta (polimorfismo, Módulo II, sección 2.11).
- **118–120:** limpia los eventos (`NaN` → `False`) y, si `allow_short` es falso, anula los
  cortos.
- **121–127:** calcula el ATR y la distancia del stop (`ATR · stop_atr_mult`). Donde no hay stop
  válido (calentamiento del ATR), **anula las entradas antes de la máquina de estados**. Este
  orden se corrigió en la auditoría (commit `697b6af`, hallazgo M-04): antes se anulaba la señal
  **después**, y con un `atr_period` largo aparecía una entrada ficticia en la primera vela con
  ATR válido.
- **128–135:** convierte eventos en estado con `events_to_state` (explicada línea a línea en el
  Módulo II, sección 2.3).
- **136–145:** construye las cinco columnas del contrato. La convicción se recorta a [0, 1] y
  vale 0 cuando no hay posición deseada.

### Eventos "de nivel" y eventos "de cruce"

Dos tipos de condición aparecen en las estrategias:

- **Cruce:** verdadera solo en la vela en que algo **cambia** (la EMA rápida cruza la lenta).
- **Nivel:** verdadera **mientras** se cumple algo (el cierre está por encima del canal de
  Donchian).

Con la máquina de estados, ambos tipos funcionan: una vez en posición, una entrada repetida no
cambia nada. Pero el motor solo abre posición en la vela en que el estado **cambia** (entradas
"por transición", Módulo X). Consecuencia: si un stop cierra la operación y la condición de
nivel sigue cumpliéndose, **no** se vuelve a entrar hasta que el estado pase por FLAT y vuelva.

### Stops, objetivos y tiempo máximo por defecto

Los parámetros de salida comunes los define `StrategyParams` y cada estrategia cambia algunos.
Valores por defecto reales:

<!-- ejecutar -->
```python
from bybit_quant_lab.strategies import available_strategies, get_strategy_class

cols = ["atr_period", "stop_atr_mult", "take_profit_r", "trailing_atr_mult", "max_holding_bars", "cooldown_bars"]
print(f"{'estrategia':20s} " + " ".join(f"{c[:14]:>14s}" for c in cols))
for nombre in available_strategies():
    p = get_strategy_class(nombre).params_model()
    print(f"{nombre:20s} " + " ".join(f"{str(getattr(p, c)):>14s}" for c in cols))
```
<!-- salida -->
```text
estrategia               atr_period  stop_atr_mult  take_profit_r trailing_atr_m max_holding_ba  cooldown_bars
adx_di                           14            2.0           None            3.0           None              0
bollinger_reversion              14            2.0           None           None             48              0
donchian_breakout                14            2.0           None            3.0           None              0
ema_crossover                    14            2.0            2.0           None           None              0
macd_momentum                    14            2.0            2.0           None           None              0
obv_trend                        14            2.0            2.0           None           None              5
rsi_reversion                    14            2.0           None           None             48              0
stoch_rsi                        14            2.0            1.5           None             24              3
volume_spike                     14            2.0            2.0           None             48              0
vwap_deviation                   14            2.0           None           None           None              0
```

- `take_profit_r = 2.0` significa un objetivo a **2 veces la distancia del stop** ("2R").
  `None` significa sin objetivo fijo: la salida la decide la regla de la estrategia, el stop o
  el trailing.
- `trailing_atr_mult = 3.0` activa un stop que persigue al precio a 3 ATR del extremo alcanzado.
- `max_holding_bars` fuerza la salida tras ese número de velas.
- `cooldown_bars` impone una espera tras cada salida.

**[Limitación]** Todos estos valores son **convencionales o arbitrarios**: ninguno se ha
optimizado ni validado con datos reales (Módulo XVII).

### De la señal a la operación simulada

<!-- ejecutar -->
```python
from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config import AppConfig
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=3000, seed=7)
senales = create_strategy("ema_crossover").generate_signals(datos)
resultado = run_backtest(datos, senales, AppConfig(), "BTCUSDT", "1h")
op = resultado.trades.iloc[0]
i = datos.index.get_loc(op["entry_time"])
print("señal al cierre de la vela", i - 1, "->", int(senales["signal"].iloc[i - 1]),
      "| vela anterior:", int(senales["signal"].iloc[i - 2]))
print("entrada en la apertura de la vela", i, ":", round(datos["open"].iloc[i], 2),
      "-> ejecutada a", round(op["entry_price"], 2))
print("stop a", round(senales["stop_distance"].iloc[i - 1], 2), "de distancia |",
      "salida:", op["exit_reason"], "| resultado neto:", round(op["net_pnl"], 2))
```
<!-- salida -->
```text
señal al cierre de la vela 222 -> -1 | vela anterior: 0
entrada en la apertura de la vela 223 : 29387.94 -> ejecutada a 29382.07
stop a 599.27 de distancia | salida: take_profit | resultado neto: 179.99
```

El recorrido completo es:

1. **Cierre de la vela `i−1`:** la estrategia pasa de 0 a ±1.
2. **El motor** ve la transición y comprueba los límites de riesgo. Si puede, programa una orden.
3. **Apertura de la vela `i`:** compra (o vende) al precio de apertura con deslizamiento adverso
   (2 puntos básicos por defecto) y paga comisión. El tamaño depende de la distancia del stop
   (Módulo XI).
4. **Velas siguientes:** se vigilan stop, objetivo, trailing y liquidación; la regla de salida de
   la estrategia también puede cerrar la posición (Módulo X).

### Pruebas comunes a las diez estrategias

En `tests/unit/test_strategies.py`, parametrizadas para las diez:

| Prueba | Qué verifica |
|---|---|
| `test_output_contract` | Columnas, índice, señales en {−1, 0, 1}, convicción en [0, 1], stops positivos cuando hay señal |
| `test_no_lookahead_truncation` | Recortar los datos en `t` no cambia ninguna señal hasta `t` |
| `test_no_lookahead_future_perturbation` | Alterar precios y volumen posteriores a `t` no cambia nada hasta `t` |
| `test_empty_and_short_data` | Datos vacíos y series más cortas que el calentamiento |
| `test_missing_values_do_not_crash` | `NaN` intercalados |
| `test_missing_column_raises`, `test_invalid_params_rejected` | Errores claros con datos o parámetros inválidos |
| `test_long_only_mode` | `allow_short=False` elimina los cortos |
| `test_every_entry_coincides_with_an_entry_event` | Toda entrada tiene un evento de entrada detrás (regresión de M-04) |

---

## 8.1 Volume Spike + Price Confirmation (`volume_spike`)

**Hipótesis.** Un volumen anormalmente alto, **acompañado** de una vela fuerte que rompe el rango
de la vela anterior, indica una participación decidida en esa dirección. El volumen por sí solo no
dice hacia dónde.

**Condiciones.**

| Evento | Condición (todas a la vez) |
|---|---|
| Entrada larga | volumen relativo > `spike_mult`; cierre > apertura; cuerpo ≥ `min_body_ratio` del rango; cierre > máximo anterior (si `require_range_break`); ATR % dentro de los límites |
| Entrada corta | lo mismo en espejo: cierre < apertura, cierre < mínimo anterior |
| Salida larga | cierre < EMA(`exit_ema`) |
| Salida corta | cierre > EMA(`exit_ema`) |

**Código.**

<!-- cita: src/bybit_quant_lab/strategies/volume_spike.py#L46-L72 -->
`src/bybit_quant_lab/strategies/volume_spike.py` · líneas 46–72

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        o, h, low, c, v = (data[k] for k in ("open", "high", "low", "close", "volume"))
        vol_ma = sma(v, p.volume_window).shift(1)  # solo velas anteriores
        ratio = v / vol_ma.replace(0, np.nan)
        spike = ratio > p.spike_mult
        rng = (h - low).replace(0, np.nan)
        body_ratio = (c - o).abs() / rng
        strong = body_ratio >= p.min_body_ratio
        atr_pct = atr(data, p.atr_period) / c
        vol_ok = atr_pct >= p.min_atr_pct
        if p.max_atr_pct is not None:
            vol_ok &= atr_pct <= p.max_atr_pct
        bull = (c > o) & strong
        bear = (c < o) & strong
        if p.require_range_break:
            bull &= c > h.shift(1)
            bear &= c < low.shift(1)
        trend_exit = ema(c, p.exit_ema)
        conviction = (ratio / (2 * p.spike_mult)).clip(0, 1) * body_ratio.fillna(0)
        return Events(
            long_entry=spike & bull & vol_ok,
            short_entry=spike & bear & vol_ok,
            long_exit=c < trend_exit,
            short_exit=c > trend_exit,
            conviction=conviction,
        )
```

- **52–54:** la "fuerza" de la vela es su cuerpo (`|cierre − apertura|`) dividido entre su rango
  (`máximo − mínimo`). Un cuerpo del 50 % o más es una vela decidida; un doji (cuerpo casi nulo)
  no lo es.
- **65:** convicción: volumen relativo dividido entre `2·spike_mult`, recortado y multiplicado
  por la fuerza del cuerpo.

**Parámetros.**

<!-- cita: src/bybit_quant_lab/strategies/volume_spike.py#L19-L29 -->
`src/bybit_quant_lab/strategies/volume_spike.py` · líneas 19–29

```python
class VolumeSpikeParams(StrategyParams):
    """Parámetros de Volume Spike."""

    volume_window: int = Field(20, ge=2, le=1000)
    spike_mult: float = Field(2.5, gt=1, le=50)
    min_body_ratio: float = Field(0.5, ge=0, le=1)
    require_range_break: bool = True
    min_atr_pct: float = Field(0.0, ge=0)
    max_atr_pct: float | None = Field(None, gt=0)
    exit_ema: int = Field(20, ge=2, le=500)
    max_holding_bars: int | None = Field(48, ge=1)
```

**Ejemplos controlados.** Una serie plana de 60 velas con volumen 100; en la vela 50 se coloca
una vela concreta y se mira la señal en esa vela:

<!-- ejecutar -->
```python
import numpy as np
import pandas as pd

from bybit_quant_lab.strategies import create_strategy

rng = np.random.default_rng(1)
cierres = 100 + rng.normal(0, 0.05, 60)
aperturas = np.r_[cierres[0], cierres[:-1]]
base = pd.DataFrame({"open": aperturas, "high": np.maximum(aperturas, cierres) + 0.2,
                     "low": np.minimum(aperturas, cierres) - 0.2, "close": cierres, "volume": 100.0},
                    index=pd.date_range("2024-01-01", periods=60, freq="1h", tz="UTC"))
estrategia = create_strategy("volume_spike", {"spike_mult": 3.0})

def senal_en_vela_50(open_, high, low, close, volume):
    datos = base.copy()
    datos.iloc[50] = [open_, high, low, close, volume]
    return int(estrategia.generate_signals(datos)["signal"].iloc[50])

print("vela alcista fuerte, volumen x10:", senal_en_vela_50(100, 103.2, 99.9, 103.0, 1000))
print("vela bajista fuerte, volumen x10:", senal_en_vela_50(100, 100.1, 96.8, 97.0, 1000))
print("doji, volumen x10:              ", senal_en_vela_50(100, 101.0, 99.0, 100.01, 1000))
print("vela alcista, volumen normal:   ", senal_en_vela_50(100, 103.2, 99.9, 103.0, 100))
```
<!-- salida -->
```text
vela alcista fuerte, volumen x10: 1
vela bajista fuerte, volumen x10: -1
doji, volumen x10:               0
vela alcista, volumen normal:    0
```

Cálculo de la vela alcista: volumen relativo `1000 / 100 = 10 > 3`; cuerpo
`(103 − 100) / (103,2 − 99,9) = 0,91 ≥ 0,5`; cierre 103 por encima del máximo anterior (≈100,2).
Se cumplen todas las condiciones. El doji tiene el mismo volumen, pero su cuerpo es casi 0: sin
dirección no hay señal.

**Casos sin señal.** Volumen alto con vela indecisa; vela fuerte sin volumen; vela fuerte que no
rompe el rango anterior; y además, **[Hecho] detalle sutil**: si el cierre de la vela alcista
queda por debajo de su EMA de salida, la entrada y la salida coinciden en la misma vela y la regla
3 de `events_to_state` (la salida prevalece) impide entrar. En la práctica funciona como un filtro
implícito: no compra picos alcistas que ocurren por debajo de la EMA de 20 velas.

**Calentamiento.** `volume_window + 1` velas para el volumen relativo; 14 para el ATR; 20 para la
EMA de salida.

**Pruebas específicas.** `test_volume_spike_requires_price_confirmation`.

**Limitaciones.** Un solo exchange de volumen; los umbrales (2,5 veces, 50 % de cuerpo) son
arbitrarios; los picos de volumen son poco frecuentes, así que se esperan **pocas operaciones**, y
con pocas operaciones cualquier métrica es muy incierta (Módulo VI, sección 6.6).

---

## 8.2 OBV Trend Confirmation (`obv_trend`)

**Hipótesis.** Cuando el OBV cruza por encima de su media, con pendiente positiva, y el precio
está por encima de su propia media, el volumen **confirma** la tendencia alcista del precio (y en
espejo para la bajista).

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | OBV cruza al alza su EMA(`obv_ema`); OBV[t] − OBV[t−`slope_window`] > 0; cierre > EMA(`price_ema`) |
| Entrada corta | Espejo |
| Salida larga | OBV cruza a la baja su EMA **o** cierre < EMA del precio |
| Salida corta | Espejo |

**Código.**

<!-- cita: src/bybit_quant_lab/strategies/obv_trend.py#L42-L58 -->
`src/bybit_quant_lab/strategies/obv_trend.py` · líneas 42–58

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        o = obv(c, data["volume"])
        o_ma = ema(o, p.obv_ema)
        slope = o - o.shift(p.slope_window)
        price_ma = ema(c, p.price_ema)
        dev = o - o_ma
        scale = o.diff().abs().rolling(p.obv_ema, min_periods=p.obv_ema).mean()
        conviction = (dev.abs() / (scale * np.sqrt(p.obv_ema)).replace(0, np.nan)).clip(0, 1)
        return Events(
            long_entry=crossover(o, o_ma) & (slope > 0) & (c > price_ma),
            short_entry=crossunder(o, o_ma) & (slope < 0) & (c < price_ma),
            long_exit=crossunder(o, o_ma) | (c < price_ma),
            short_exit=crossover(o, o_ma) | (c > price_ma),
            conviction=conviction,
        )
```

- **47:** la pendiente es la variación del OBV en las últimas `slope_window` velas.
- **49–51:** convicción: distancia entre el OBV y su media, dividida entre el cambio absoluto
  medio del OBV multiplicado por `√obv_ema`. **[Limitación]** Es una normalización arbitraria,
  sin interpretación estadística.

**Parámetros:** `obv_ema` 20, `price_ema` 50, `slope_window` 5, `cooldown_bars` 5 (líneas 19–25).
El enfriamiento evita reentrar en la vela siguiente a una salida, cuando el OBV oscila alrededor
de su media.

**Anatomía de una señal real** (datos sintéticos):

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.indicators import ema, obv
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=3000, seed=7)
s = create_strategy("obv_trend").generate_signals(datos)["signal"]
o = obv(datos["close"], datos["volume"])
tabla = pd.DataFrame({"OBV": o, "EMA20(OBV)": ema(o, 20), "pendiente5": o - o.shift(5),
                      "cierre": datos["close"], "EMA50(cierre)": ema(datos["close"], 50), "senal": s})
for lado in (1, -1):
    t = int(((s == lado) & (s.shift(1, fill_value=0) != lado)).to_numpy().argmax())
    print("primera entrada", "LARGA" if lado == 1 else "CORTA", "en la vela", t)
    print(tabla.iloc[t - 1 : t + 1].round(1).to_string())
```
<!-- salida -->
```text
primera entrada LARGA en la vela 70
                              OBV  EMA20(OBV)  pendiente5   cierre  EMA50(cierre)  senal
open_time                                                                               
2023-01-03 21:00:00+00:00 -3460.1     -3240.4       345.5  29044.1        28937.5      0
2023-01-03 22:00:00+00:00 -1410.6     -3066.1      3153.0  29180.3        28947.0      1
primera entrada CORTA en la vela 99
                              OBV  EMA20(OBV)  pendiente5   cierre  EMA50(cierre)  senal
open_time                                                                               
2023-01-05 02:00:00+00:00  1110.8      -143.0       162.0  29631.9        29310.6      1
2023-01-05 03:00:00+00:00  -603.8      -186.9     -2865.4  29295.7        29310.0     -1
```

Comprueba en cada caso: en la vela `t−1` el OBV estaba al otro lado de su EMA; en `t` la cruza, la
pendiente tiene el signo correcto y el cierre está del lado correcto de su EMA de 50.

**Pruebas específicas.** `test_obv_no_shorts_in_steady_uptrend`.

**Limitaciones.** El OBV es una aproximación tosca (Módulo VII, sección 7.2); la condición de
precio sobre EMA(50) se solapa con las estrategias de tendencia (redundancia, Módulo IX).

---

## 8.3 VWAP Deviation + Volume Regime (`vwap_deviation`)

**Hipótesis (dos, mutuamente excluyentes, elegidas con `mode`).**

- **`reversion`:** un precio muy alejado del VWAP **con volumen normal** está "estirado" sin
  respaldo y tiende a volver.
- **`continuation`:** un precio muy alejado del VWAP **con volumen alto** refleja una presión real
  que tiende a continuar.

**[Diseño]** Las dos lógicas nunca se mezclan: una ejecución usa una u otra. Mezclarlas sin una
regla que decida cuándo aplicar cada una produciría señales contradictorias.

**Condiciones** (`z` es la desviación normalizada respecto al VWAP, `vol_rel` el volumen
relativo):

| Modo | Entrada larga | Entrada corta | Salida larga | Salida corta |
|---|---|---|---|---|
| reversion | `z ≤ −entry_z` y `vol_rel ≤ max_rel_volume` | `z ≥ entry_z` y volumen tranquilo | `z ≥ −exit_z` | `z ≤ exit_z` |
| continuation | `z ≥ entry_z` y `vol_rel ≥ min_rel_volume` | `z ≤ −entry_z` y volumen activo | `z ≤ exit_z` | `z ≥ −exit_z` |

**Código.**

<!-- cita: src/bybit_quant_lab/strategies/vwap_deviation.py#L61-L90 -->
`src/bybit_quant_lab/strategies/vwap_deviation.py` · líneas 61–90

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c, v = data["close"], data["volume"]
        vw = (
            vwap_rolling(data, p.vwap_window)
            if p.vwap_type == "rolling"
            else vwap_session(data, p.session)
        )
        dev = c - vw
        std = dev.rolling(p.dev_window, min_periods=p.dev_window).std().shift(1)
        z = dev / std.replace(0, np.nan)
        rel_vol = v / sma(v, p.volume_window).shift(1).replace(0, np.nan)
        conviction = ((z.abs() - p.entry_z) / p.entry_z).clip(0, 1)
        if p.mode == "reversion":
            quiet = rel_vol <= p.max_rel_volume
            return Events(
                long_entry=(z <= -p.entry_z) & quiet,
                short_entry=(z >= p.entry_z) & quiet,
                long_exit=z >= -p.exit_z,
                short_exit=z <= p.exit_z,
                conviction=conviction,
            )
        active = rel_vol >= p.min_rel_volume
        return Events(
            long_entry=(z >= p.entry_z) & active,
            short_entry=(z <= -p.entry_z) & active,
            long_exit=z <= p.exit_z,
            short_exit=z >= -p.exit_z,
            conviction=conviction,
        )
```

- **70–71:** el z-score usa la desviación de las `dev_window` velas **anteriores** (`shift(1)`):
  la vela actual no infla su propia normalización.
- **72:** volumen relativo, como en la sección 8.1.

**Parámetros** (líneas 28–41): `mode` reversion, `vwap_type` rolling, `vwap_window` 96,
`session` "1D", `dev_window` 100, `entry_z` 2,0, `exit_z` 0,5, `volume_window` 50,
`max_rel_volume` y `min_rel_volume` 1,5, sin objetivo fijo.

**Ejemplo controlado.** 300 velas casi planas; en la vela 280 el precio cae de 100 a 95:

<!-- ejecutar -->
```python
import numpy as np
import pandas as pd

from bybit_quant_lab.strategies import create_strategy

rng = np.random.default_rng(1)
cierres = 100 + rng.normal(0, 0.2, 300)
aperturas = np.r_[cierres[0], cierres[:-1]]
datos = pd.DataFrame({"open": aperturas, "high": np.maximum(aperturas, cierres) + 0.2,
                      "low": np.minimum(aperturas, cierres) - 0.2, "close": cierres, "volume": 100.0},
                     index=pd.date_range("2024-01-01", periods=300, freq="1h", tz="UTC"))
datos.iloc[280, :4] = [100, 100.2, 94.8, 95]
parametros = {"vwap_window": 50, "dev_window": 50}
for volumen in (100.0, 1000.0):
    datos.iloc[280, 4] = volumen
    rev = create_strategy("vwap_deviation", {**parametros, "mode": "reversion"}).generate_signals(datos)
    con = create_strategy("vwap_deviation", {**parametros, "mode": "continuation"}).generate_signals(datos)
    print(f"volumen {volumen:6.0f}: reversion -> {int(rev['signal'].iloc[280]):2d} | "
          f"continuation -> {int(con['signal'].iloc[280]):2d}")
```
<!-- salida -->
```text
volumen    100: reversion ->  1 | continuation ->  0
volumen   1000: reversion ->  0 | continuation -> -1
```

Con volumen normal, solo la hipótesis de reversión actúa (compra esperando el regreso al VWAP).
Con volumen diez veces mayor, solo actúa la de continuación (vende siguiendo la caída). Es la
prueba `test_vwap_hypotheses_are_separate`.

**Calentamiento.** En modo móvil, `vwap_window` + `dev_window` velas (unas 196 por defecto).
**Limitaciones.** El VWAP de sesión se basa en muy pocas velas al principio de cada día UTC
(Módulo VII, sección 7.3); `entry_z = 2` no implica una probabilidad del 5 %, porque las
desviaciones no son normales.

---

## 8.4 EMA Crossover + Trend Filter (`ema_crossover`)

**Hipótesis.** Un cruce de una EMA rápida sobre una lenta, en la dirección de la tendencia de
fondo y con fuerza de tendencia suficiente, marca el inicio de un movimiento sostenido.

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | EMA(`fast`) cruza al alza EMA(`slow`); cierre > EMA(`trend_ema`) (si está activa); filtro de régimen (ADX ≥ `adx_min`, ATR % ≥ `atr_pct_min` o ninguno) |
| Entrada corta | Espejo |
| Salida larga / corta | El cruce contrario |

**Código y parámetros:** `strategies/ema_crossover.py`, líneas 20–74, explicado línea a línea en
el Módulo II (sección 2.11). Por defecto: 12/26, EMA de tendencia 200, filtro ADX ≥ 20, objetivo
2R.

**Anatomía de una señal real:**

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.indicators import adx, ema
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=3000, seed=7)
c = datos["close"]
s = create_strategy("ema_crossover").generate_signals(datos)["signal"]
tabla = pd.DataFrame({"EMA12": ema(c, 12), "EMA26": ema(c, 26), "cierre": c, "EMA200": ema(c, 200),
                      "ADX": adx(datos, 14)["adx"], "senal": s})
t = int(((s == 1) & (s.shift(1, fill_value=0) != 1)).to_numpy().argmax())
print("primera entrada larga en la vela", t)
print(tabla.iloc[t - 1 : t + 1].round(2).to_string())
print("velas con señal sin filtros:",
      int((create_strategy("ema_crossover", {"trend_ema": None, "regime_filter": "none"})
           .generate_signals(datos)["signal"] != 0).sum()),
      "| con filtros:", int((s != 0).sum()))
```
<!-- salida -->
```text
primera entrada larga en la vela 986
                              EMA12     EMA26    cierre    EMA200    ADX  senal
open_time                                                                      
2023-02-11 01:00:00+00:00  22245.80  22248.51  22135.06  21369.72  28.77      0
2023-02-11 02:00:00+00:00  22267.52  22258.77  22386.98  21379.84  27.69      1
velas con señal sin filtros: 2945 | con filtros: 464
```

En `t−1` la EMA12 está por debajo de la EMA26 y en `t` por encima: hay cruce. El cierre supera la
EMA200 y el ADX supera 20. La última línea muestra el efecto de los filtros: el número de velas en
posición se reduce mucho.

**Pruebas específicas.** `test_ema_crossover_v_shape_goes_long`,
`test_ema_crossover_regime_filter_blocks_range`.

**Limitaciones.** Las medias se retrasan; en mercados laterales los cruces se repiten (los
filtros los reducen, no los eliminan); la EMA200 exige 200 velas de historia. Con los filtros
activos, el número de operaciones puede ser pequeño.

---

## 8.5 Donchian Breakout + ATR (`donchian_breakout`)

**Hipótesis.** Un cierre fuera del rango de las últimas `channel` velas inicia un movimiento
direccional (la idea clásica de los sistemas de "tortugas").

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | cierre > máximo de las `channel` velas **anteriores**; filtro de temporalidad superior (opcional) |
| Entrada corta | cierre < mínimo de las `channel` velas anteriores |
| Salida larga | cierre < mínimo de las `exit_channel` velas anteriores |
| Salida corta | cierre > máximo de las `exit_channel` velas anteriores |

**Código.**

<!-- cita: src/bybit_quant_lab/strategies/donchian_breakout.py#L58-L83 -->
`src/bybit_quant_lab/strategies/donchian_breakout.py` · líneas 58–83

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        ch = donchian(data, p.channel)
        ex = donchian(data, p.exit_channel)
        up_ok = pd.Series(True, index=c.index)
        dn_ok = pd.Series(True, index=c.index)
        if p.htf is not None and len(data) >= 2:
            htf = higher_timeframe(
                data,
                infer_bar_delta(pd.DatetimeIndex(data.index)),
                pd.Timedelta(p.htf),
                ema_period=p.htf_ema,
            )
            up_ok = htf["close"] > htf["ema"]
            dn_ok = htf["close"] < htf["ema"]
        width = (ch["upper"] - ch["lower"]).where(lambda w: w > 0)
        conviction = ((c - ch["mid"]).abs() / width).clip(0, 1) * 2
        a = atr(data, p.atr_period)
        return Events(
            long_entry=(c > ch["upper"]) & up_ok & a.notna(),
            short_entry=(c < ch["lower"]) & dn_ok & a.notna(),
            long_exit=c < ex["lower"],
            short_exit=c > ex["upper"],
            conviction=conviction,
        )
```

- **65–73:** filtro opcional de temporalidad superior (por ejemplo, `htf: "4h"`): solo largos si
  el cierre de la última vela de 4h **cerrada** está por encima de su EMA. La alineación sin
  anticipación se explicó en el Módulo VII (sección 7.12).
- **78–79:** `a.notna()` exige un ATR válido. **[Hecho]** Desde la corrección M-04 la clase base
  ya lo garantiza; la condición es redundante, aunque inofensiva.

**Parámetros** (líneas 25–41): `channel` 20, `exit_channel` 10 (no puede superar a `channel`),
`htf` desactivado, `htf_ema` 50, **sin objetivo** y **trailing de 3 ATR**: la estrategia deja
correr las tendencias y sale por el canal corto o por el trailing.

**Ejemplos controlados** (prueba `test_donchian_uses_previous_bars_only`):

<!-- ejecutar -->
```python
import numpy as np
import pandas as pd

from bybit_quant_lab.strategies import create_strategy

rng = np.random.default_rng(1)
cierres = 100 + rng.normal(0, 0.1, 40)
aperturas = np.r_[cierres[0], cierres[:-1]]
base = pd.DataFrame({"open": aperturas, "high": np.maximum(aperturas, cierres) + 0.2,
                     "low": np.minimum(aperturas, cierres) - 0.2, "close": cierres, "volume": 100.0},
                    index=pd.date_range("2024-01-01", periods=40, freq="1h", tz="UTC"))
estrategia = create_strategy("donchian_breakout", {"channel": 20, "exit_channel": 10, "atr_period": 5})
maximo_previo = base["high"].iloc[15:35].max()
minimo_previo = base["low"].iloc[15:35].min()
print("máximo de las 20 velas anteriores:", round(maximo_previo, 3))
for nombre, cierre, extremo in (("ruptura al alza", maximo_previo + 0.01, maximo_previo + 0.02),
                                ("ruptura a la baja", minimo_previo - 0.01, minimo_previo - 0.02),
                                ("dentro del canal", 100.0, 100.1)):
    datos = base.copy()
    columna = "high" if cierre > 100 else "low"
    datos.loc[datos.index[35], ["close", columna]] = [cierre, extremo]
    print(f"{nombre:18s} -> señal en la vela 35:",
          int(estrategia.generate_signals(datos)["signal"].iloc[35]))
```
<!-- salida -->
```text
máximo de las 20 velas anteriores: 100.412
ruptura al alza    -> señal en la vela 35: 1
ruptura a la baja  -> señal en la vela 35: -1
dentro del canal   -> señal en la vela 35: 0
```

Basta con superar el máximo previo en un céntimo. Esta sensibilidad tiene su contrapartida: en
mercados laterales, las rupturas falsas son frecuentes, y el stop de 2 ATR las convierte en
pequeñas pérdidas repetidas.

**[Hecho] Hallazgo de revisión (nuevo, no recogido en la auditoría): la convicción no informa.**
La línea 75 calcula `(|cierre − medio| / ancho).clip(0, 1) * 2`. En una ruptura el cierre está
fuera del canal, la fracción es al menos 0,5 y, multiplicada por 2, llega a 1 o más; la clase base
la recorta a 1. Con 6.000 velas sintéticas, la convicción valía exactamente 1 en las 165 entradas.
Solo afecta a las combinaciones que ponderan por convicción (`use_conviction`, Módulo IX), que
por defecto no lo hacen.

**Pruebas específicas.** `test_donchian_uses_previous_bars_only`,
`test_donchian_htf_filter_runs_without_lookahead`.

---

## 8.6 RSI Mean Reversion (`rsi_reversion`)

**Hipótesis.** Tras una sobreventa (RSI < 30), el **regreso** del RSI por encima de 30 indica que
la presión vendedora se agota y el precio tiende a rebotar (en espejo para la sobrecompra).

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | RSI cruza al alza `oversold` (30); filtro de tendencia |
| Entrada corta | RSI cruza a la baja `overbought` (70); filtro de tendencia |
| Salida larga | RSI ≥ `exit_level` (50) |
| Salida corta | RSI ≤ `exit_level` |

**[Diseño]** Tocar la zona no basta: se exige **salir** de ella. Comprar mientras el RSI sigue
cayendo por debajo de 30 sería "intentar atrapar un cuchillo que cae".

**Código.**

<!-- cita: src/bybit_quant_lab/strategies/rsi_reversion.py#L60-L81 -->
`src/bybit_quant_lab/strategies/rsi_reversion.py` · líneas 60–81

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        r = rsi(c, p.rsi_period)
        long_ok = pd.Series(True, index=c.index)
        short_ok = pd.Series(True, index=c.index)
        if p.trend_filter == "ema":
            t = ema(c, p.trend_ema)
            long_ok, short_ok = c > t, c < t
        elif p.trend_filter == "adx":
            weak = adx(data, p.adx_period)["adx"] < p.adx_max
            long_ok, short_ok = weak, weak
        depth_long = (p.oversold - r.rolling(5, min_periods=1).min()) / p.oversold
        depth_short = (r.rolling(5, min_periods=1).max() - p.overbought) / (100 - p.overbought)
        conviction = depth_long.clip(lower=0).combine(depth_short.clip(lower=0), max) * 2
        return Events(
            long_entry=crossover(r, p.oversold) & long_ok,
            short_entry=crossunder(r, p.overbought) & short_ok,
            long_exit=r >= p.exit_level,
            short_exit=r <= p.exit_level,
            conviction=conviction,
        )
```

- **66–71:** filtro de tendencia. Con `ema`, solo largos por encima de la EMA200 (comprar caídas
  dentro de una tendencia alcista). Con `adx` (por defecto), solo se opera si el ADX < 25, es
  decir, cuando **no** hay tendencia fuerte: la reversión a la media tiene más sentido en un
  mercado lateral.
- **72–74:** convicción: profundidad de la incursión en la zona en las últimas 5 velas,
  multiplicada por 2.

**Parámetros** (líneas 24–42): validación `oversold < exit_level < overbought`; sin objetivo
fijo; máximo 48 velas.

**Ejemplo controlado:** 30 velas planas, una caída de 100 a 80 y un rebote:

<!-- ejecutar -->
```python
import numpy as np
import pandas as pd

from bybit_quant_lab.indicators import rsi
from bybit_quant_lab.strategies import create_strategy

rng = np.random.default_rng(1)
cierres = np.r_[np.full(30, 100.0), np.linspace(100, 80, 20), np.linspace(80, 84, 6)] + rng.normal(0, 0.02, 56)
aperturas = np.r_[cierres[0], cierres[:-1]]
datos = pd.DataFrame({"open": aperturas, "high": np.maximum(aperturas, cierres) + 0.1,
                      "low": np.minimum(aperturas, cierres) - 0.1, "close": cierres, "volume": 100.0},
                     index=pd.date_range("2024-01-01", periods=56, freq="1h", tz="UTC"))
s = create_strategy("rsi_reversion", {"trend_filter": "none"}).generate_signals(datos)["signal"]
r = rsi(datos["close"], 14)
for t in range(48, 56):
    print(t, round(r.iloc[t], 1), int(s.iloc[t]))
```
<!-- salida -->
```text
48 0.4 0
49 0.3 0
50 0.3 0
51 7.8 0
52 15.0 0
53 21.3 0
54 27.4 0
55 32.6 1
```

Durante la caída el RSI se hunde muy por debajo de 30 sin señal; la entrada larga aparece en la
vela en que el RSI **vuelve a cruzar** por encima de 30.

**Pruebas específicas.** `test_rsi_reversion_long_after_oversold_exit`.

**Limitaciones.** En tendencias fuertes, la reversión pierde repetidamente (de ahí el filtro). Sin
objetivo fijo y con salida en RSI 50, el beneficio por operación suele ser pequeño y **sensible a
los costes**. Es una de las estrategias con menos operaciones en los datos sintéticos.

---

## 8.7 MACD Momentum (`macd_momentum`)

**Hipótesis.** El cruce de la línea MACD sobre su señal marca una aceleración del impulso. Un
filtro direccional opcional exige que ese impulso vaya a favor de la tendencia de fondo.

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | MACD cruza al alza la señal; histograma creciente (si `require_hist_rising`); filtro direccional (`ema`: cierre > EMA200; `zero_line`: MACD > 0; `none`) |
| Entrada corta | Espejo |
| Salida | El cruce contrario |

**Código.**

<!-- cita: src/bybit_quant_lab/strategies/macd_momentum.py#L53-L76 -->
`src/bybit_quant_lab/strategies/macd_momentum.py` · líneas 53–76

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        c = data["close"]
        m = macd(c, p.fast, p.slow, p.signal_period)
        hist = m["hist"]
        rising, falling = hist > hist.shift(1), hist < hist.shift(1)
        if not p.require_hist_rising:
            rising = falling = pd.Series(True, index=c.index)
        if p.direction_filter == "ema":
            t = ema(c, p.trend_ema)
            up_ok, dn_ok = c > t, c < t
        elif p.direction_filter == "zero_line":
            up_ok, dn_ok = m["macd"] > 0, m["macd"] < 0
        else:
            up_ok = dn_ok = pd.Series(True, index=c.index)
        scale = hist.abs().rolling(100, min_periods=20).max()
        conviction = (hist.abs() / scale).clip(0, 1)
        return Events(
            long_entry=crossover(m["macd"], m["signal"]) & rising & up_ok,
            short_entry=crossunder(m["macd"], m["signal"]) & falling & dn_ok,
            long_exit=crossunder(m["macd"], m["signal"]),
            short_exit=crossover(m["macd"], m["signal"]),
            conviction=conviction,
        )
```

**[Hecho] Hallazgo de revisión (nuevo, no recogido en la auditoría): `require_hist_rising` no
tiene ningún efecto.** El histograma es `MACD − señal`. Un cruce al alza en `t` exige
`MACD[t] > señal[t]` (histograma positivo) y `MACD[t−1] ≤ señal[t−1]` (histograma ≤ 0). Por tanto
`hist[t] > 0 ≥ hist[t−1]`: el histograma **siempre** sube en un cruce al alza. La condición de la
línea 58 es matemáticamente redundante:

<!-- ejecutar -->
```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=6000, seed=11)
for filtro in ("none", "ema", "zero_line"):
    con = create_strategy("macd_momentum", {"require_hist_rising": True, "direction_filter": filtro})
    sin = create_strategy("macd_momentum", {"require_hist_rising": False, "direction_filter": filtro})
    print(filtro, "señales idénticas:",
          con.generate_signals(datos)["signal"].equals(sin.generate_signals(datos)["signal"]))
```
<!-- salida -->
```text
none señales idénticas: True
ema señales idénticas: True
zero_line señales idénticas: True
```

**Consecuencia:** la rejilla de búsqueda de `configs/strategies.yaml` (línea 185) incluye
`require_hist_rising: [true, false]` y **duplica** configuraciones que producen exactamente las
mismas operaciones. El registro de experimentos las cuenta como pruebas distintas, lo que infla
el número de pruebas del Deflated Sharpe (Módulo XIII), en la dirección conservadora. Es el mismo
tipo de problema que el hallazgo B-01 de la auditoría (dos combinaciones idénticas).

**Contribución incremental del filtro direccional.** Para medir si un filtro aporta algo hay que
comparar variantes **en entrenamiento**, nunca en el test:

```bash
bql sensitivity --symbol BTCUSDT --timeframe 1h --strategy macd_momentum \
  --grid '{"direction_filter": ["none", "ema", "zero_line"]}'
```

**Pruebas específicas.** `test_macd_v_shape_goes_long`. **Limitaciones.** Los cruces del MACD
son frecuentes y se retrasan; en mercados laterales generan muchas entradas y salidas.

---

## 8.8 Bollinger Bands Reversion (`bollinger_reversion`)

**Hipótesis.** Un cierre **fuera** de la banda seguido de un cierre de **regreso** dentro de ella
indica que el exceso se corrige: el precio tiende a volver a la media.

**[Diseño]** Es una hipótesis de **reversión**, separada de la de **ruptura** de bandas (que
diría lo contrario: salir de la banda es el inicio de un movimiento). Tocar la banda no basta.

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | cierre[t−1] < banda inferior[t−1] **y** cierre[t] > banda inferior[t]; vela alcista (si `confirm_candle`); ADX < `adx_max` (si está definido) |
| Entrada corta | Espejo con la banda superior |
| Salida larga | cierre ≥ media (objetivo alcanzado) **o** cierre < banda inferior (invalidación: el setup falló) |
| Salida corta | Espejo |

**Código.**

<!-- cita: src/bybit_quant_lab/strategies/bollinger_reversion.py#L47-L70 -->
`src/bybit_quant_lab/strategies/bollinger_reversion.py` · líneas 47–70

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        o, c = data["open"], data["close"]
        bb = bollinger(c, p.period, p.num_std)
        below_prev = c.shift(1) < bb["lower"].shift(1)
        above_prev = c.shift(1) > bb["upper"].shift(1)
        long_setup = below_prev & (c > bb["lower"])
        short_setup = above_prev & (c < bb["upper"])
        if p.confirm_candle:
            long_setup &= c > o
            short_setup &= c < o
        if p.adx_max is not None:
            weak = adx(data, p.adx_period)["adx"] < p.adx_max
            long_setup &= weak
            short_setup &= weak
        width = (bb["upper"] - bb["lower"]).where(lambda w: w > 0)
        conviction = ((bb["mid"] - c).abs() / (width / 2)).clip(0, 1)
        return Events(
            long_entry=long_setup,
            short_entry=short_setup,
            long_exit=(c >= bb["mid"]) | (c < bb["lower"]),
            short_exit=(c <= bb["mid"]) | (c > bb["upper"]),
            conviction=conviction,
        )
```

**Ejemplo controlado** (prueba `test_bollinger_touch_is_not_signal_but_reentry_is`):

<!-- ejecutar -->
```python
import numpy as np
import pandas as pd

from bybit_quant_lab.indicators import bollinger
from bybit_quant_lab.strategies import create_strategy

rng = np.random.default_rng(1)
cierres = 100 + rng.normal(0, 0.3, 80)
aperturas = np.r_[cierres[0], cierres[:-1]]
base = pd.DataFrame({"open": aperturas, "high": np.maximum(aperturas, cierres) + 0.1,
                     "low": np.minimum(aperturas, cierres) - 0.1, "close": cierres, "volume": 100.0},
                    index=pd.date_range("2024-01-01", periods=80, freq="1h", tz="UTC"))
estrategia = create_strategy("bollinger_reversion", {"adx_max": None, "confirm_candle": True})

toque = base.copy()
toque.loc[toque.index[60], "low"] = 95.0                       # la mecha toca, el cierre no sale
print("toque de banda -> señales en velas 58-62:",
      estrategia.generate_signals(toque)["signal"].iloc[58:63].tolist())

reingreso = base.copy()
reingreso.loc[reingreso.index[60], ["open", "close", "low", "high"]] = [100.0, 97.0, 96.9, 100.1]
reingreso.loc[reingreso.index[61], ["open", "close", "low", "high"]] = [97.0, 99.5, 96.95, 99.6]
bandas = bollinger(reingreso["close"], 20, 2.0)
for t in (60, 61):
    print(t, "cierre", reingreso["close"].iloc[t], "| banda inferior", round(bandas["lower"].iloc[t], 2),
          "| señal", int(estrategia.generate_signals(reingreso)["signal"].iloc[t]))
```
<!-- salida -->
```text
toque de banda -> señales en velas 58-62: [0, 0, 0, 0, 0]
60 cierre 97.0 | banda inferior 98.47 | señal 0
61 cierre 99.5 | banda inferior 98.45 | señal 1
```

En la vela 60 el cierre (97) queda **por debajo** de la banda inferior; en la 61 vuelve a entrar
(99,5 por encima de la banda) con una vela alcista: entrada larga.

**Limitaciones.** En tendencias fuertes el precio "camina" por la banda y la reversión falla (de
ahí el filtro de ADX < 30). La salida en la media ofrece un recorrido limitado frente a un stop de
2 ATR: la relación entre ganancia y pérdida por operación puede ser desfavorable incluso con un
alto porcentaje de aciertos (Módulo XII).

---

## 8.9 Stochastic RSI (`stoch_rsi`)

**Hipótesis.** Un cruce de %K sobre %D **dentro** de la zona extrema (%K < 20) con una vela de
confirmación indica un giro de corto plazo.

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | %K cruza al alza %D con %K[t−1] < `lower`; vela alcista (si `confirm_candle`); cierre > EMA(`trend_ema`) (si se define); **rearmado** |
| Entrada corta | Espejo con `upper` |
| Salida larga | %K cruza a la baja %D con %K > `rearm_level` |
| Salida corta | Espejo |

**Código.**

<!-- cita: src/bybit_quant_lab/strategies/stoch_rsi.py#L63-L88 -->
`src/bybit_quant_lab/strategies/stoch_rsi.py` · líneas 63–88

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        o, c = data["open"], data["close"]
        st = stoch_rsi(c, p.rsi_period, p.stoch_period, p.k_smooth, p.d_smooth)
        k, d = st["k"], st["d"]
        long_raw = crossover(k, d) & (k.shift(1) < p.lower)
        short_raw = crossunder(k, d) & (k.shift(1) > p.upper)
        if p.confirm_candle:
            long_raw &= c > o
            short_raw &= c < o
        if p.trend_ema:
            t = ema(c, p.trend_ema)
            long_raw &= c > t
            short_raw &= c < t
        long_entry = rearm_events(long_raw, k > p.rearm_level)
        short_entry = rearm_events(short_raw, k < p.rearm_level)
        conviction = ((p.lower - k.shift(1)).clip(lower=0) / p.lower).combine(
            ((k.shift(1) - p.upper).clip(lower=0) / (100 - p.upper)), max
        )
        return Events(
            long_entry=long_entry,
            short_entry=short_entry,
            long_exit=crossunder(k, d) & (k > p.rearm_level),
            short_exit=crossover(k, d) & (k < p.rearm_level),
            conviction=conviction,
        )
```

**El rearmado (líneas 77–78).** El Stochastic RSI oscila mucho: dentro de una misma zona de
sobreventa puede cruzar %D varias veces en pocas velas. Contar cada cruce como una señal nueva
sobrerrepresentaría un único movimiento. `rearm_events` (`strategies/base.py`, líneas 220–235)
solo acepta un nuevo evento largo si %K ha pasado por encima de `rearm_level` (50) desde el
último aceptado.

<!-- ejecutar -->
```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.indicators import crossover, stoch_rsi
from bybit_quant_lab.strategies.base import rearm_events

datos = generate_synthetic_ohlcv(bars=3000, seed=7)
st = stoch_rsi(datos["close"])
k, d = st["k"], st["d"]
crudos = crossover(k, d) & (k.shift(1) < 20) & (datos["close"] > datos["open"])
rearmados = rearm_events(crudos, k > 50)
print("cruces alcistas en zona extrema:", int(crudos.sum()), "| tras el rearmado:", int(rearmados.sum()))
```
<!-- salida -->
```text
cruces alcistas en zona extrema: 156 | tras el rearmado: 95
```

**Parámetros** (líneas 25–45): 14/14/3/3, zonas 20/80, rearmado en 50, objetivo 1,5R, máximo 24
velas y enfriamiento de 3.

**Pruebas específicas.** `test_stoch_rsi_counts_one_signal_per_move` (comprueba que entre dos
entradas largas %K superó el nivel de rearmado), `test_rearm_events_deduplicates`.

**Limitaciones.** Es la estrategia con más operaciones en los datos sintéticos, y por tanto la más
expuesta a los **costes**. Cuatro parámetros de suavizado y tres niveles dan muchas combinaciones
posibles: un riesgo alto de sobreajuste si se optimizan todos.

---

## 8.10 ADX + DI Directional System (`adx_di`)

**Hipótesis.** Cuando la tendencia es fuerte (ADX alto), su dirección la marca el diferencial
entre +DI y −DI.

**Condiciones.**

| Evento | Condición |
|---|---|
| Entrada larga | **transición** a: ADX ≥ `adx_threshold` (25) y +DI − (−DI) > `di_margin` (2) |
| Entrada corta | Transición a: ADX ≥ 25 y −DI − (+DI) > 2 |
| Salida larga | +DI < −DI, **o** ADX < `adx_exit` (20) si `exit_on_weak_trend` |
| Salida corta | Espejo |

**Comportamiento con fuerza insuficiente.** Con ADX < 25 no se abre nada. Una posición abierta se
cierra si el ADX cae por debajo de 20. La diferencia entre 25 (entrar) y 20 (salir) es una
**histéresis**: evita que un ADX que oscila alrededor de 25 provoque entradas y salidas en cada
vela.

**Código.**

<!-- cita: src/bybit_quant_lab/strategies/adx_di.py#L53-L71 -->
`src/bybit_quant_lab/strategies/adx_di.py` · líneas 53–71

```python
    def compute_events(self, data: pd.DataFrame) -> Events:
        p = self.params
        a = adx(data, p.adx_period)
        strong = a["adx"] >= p.adx_threshold
        if p.require_adx_rising:
            strong &= a["adx"] > a["adx"].shift(1)
        spread = a["plus_di"] - a["minus_di"]
        bull = strong & (spread > p.di_margin)
        bear = strong & (spread < -p.di_margin)
        weak = a["adx"] < p.adx_exit if p.exit_on_weak_trend else pd.Series(False, index=a.index)
        bull_edge = bull & ~bull.shift(1, fill_value=False)
        bear_edge = bear & ~bear.shift(1, fill_value=False)
        return Events(
            long_entry=bull_edge,
            short_entry=bear_edge,
            long_exit=(spread < 0) | weak,
            short_exit=(spread > 0) | weak,
            conviction=(a["adx"] / 50).clip(0, 1),
        )
```

- **63–64:** los eventos de entrada son **transiciones** (`bull` y no `bull` en la vela anterior),
  no niveles.

**Anatomía de una señal real:**

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.indicators import adx
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=3000, seed=7)
a = adx(datos, 14)
s = create_strategy("adx_di").generate_signals(datos)["signal"]
tabla = pd.DataFrame({"ADX": a["adx"], "+DI": a["plus_di"], "-DI": a["minus_di"], "senal": s})
for lado in (1, -1):
    t = int(((s == lado) & (s.shift(1, fill_value=0) != lado)).to_numpy().argmax())
    print("primera entrada", "LARGA" if lado == 1 else "CORTA", "en la vela", t)
    print(tabla.iloc[t - 1 : t + 1].round(1).to_string())
print("velas en posición con ADX < 20:", int(((s != 0) & (a["adx"] < 20)).sum()))
```
<!-- salida -->
```text
primera entrada LARGA en la vela 44
                            ADX   +DI   -DI  senal
open_time                                         
2023-01-02 19:00:00+00:00  30.3  14.0  19.6     -1
2023-01-02 20:00:00+00:00  28.5  19.2  17.1      1
primera entrada CORTA en la vela 27
                            ADX   +DI   -DI  senal
open_time                                         
2023-01-02 02:00:00+00:00   NaN  16.4  31.9      0
2023-01-02 03:00:00+00:00  37.4  15.2  33.4     -1
velas en posición con ADX < 20: 0
```

Lectura de la salida:

- **Vela 27 (CORTA).** En la vela 26 el ADX todavía es `NaN` (calentamiento de los dos
  suavizados de Wilder). En la 27 aparece por primera vez: 37,4 ≥ 25 y −DI − (+DI) =
  33,4 − 15,2 = 18,2 > 2. `bear` pasa de falso a verdadero, hay transición y se entra corto.
  Que la primera entrada coincida con el primer ADX válido es habitual: el `NaN` previo cuenta
  como "no `bear`", así que el primer valor fuerte siempre es una transición.
- **Vela 44 (LARGA).** No es una entrada desde FLAT, sino una **reversión**: la señal previa era
  −1. En la 44, +DI (19,2) supera a −DI (17,1) por 2,1 > 2 con ADX 28,5, y la regla 1 de
  `events_to_state` (`base.py`, líneas 203–206) cambia de −1 a +1 en la misma vela. Con
  `execution.allow_reversal: true` (valor por defecto, `configs/default.yaml` línea 27) el motor
  cierra el corto y abre el largo en la apertura de la vela 45 (Módulo X).
- **0 velas en posición con ADX < 20:** la salida por tendencia débil funciona en esta serie.

**Pruebas específicas.** `test_adx_no_entries_when_trend_weak` (toda entrada ocurre con ADX ≥
umbral y no hay posición con ADX < 20), `test_adx_long_in_strong_uptrend`.

**Limitaciones.** El ADX se retrasa (dos suavizados de Wilder); cuando confirma la tendencia, una
parte del movimiento ya ocurrió. Los umbrales 20/25 son convenciones.

---

## 8.11 Resumen crítico de las diez estrategias

| Estrategia | Tipo de hipótesis | Riesgo principal | Hallazgos de revisión |
|---|---|---|---|
| volume_spike | Participación + dirección | Muy pocas operaciones | Filtro implícito por la EMA de salida |
| obv_trend | Confirmación por volumen | Solapamiento con las de tendencia | Convicción arbitraria |
| vwap_deviation | Reversión **o** continuación | Sesión UTC convencional | — |
| ema_crossover | Tendencia | Retraso, señales en lateral | Pocas operaciones con filtros |
| donchian_breakout | Ruptura de tendencia | Rupturas falsas | Convicción siempre 1; `a.notna()` redundante |
| rsi_reversion | Reversión | Tendencias fuertes; costes | — |
| macd_momentum | Impulso | Retraso, lateral | `require_hist_rising` sin efecto |
| bollinger_reversion | Reversión | Caminar por la banda | — |
| stoch_rsi | Giro de corto plazo | Muchas operaciones y costes; sobreajuste | — |
| adx_di | Tendencia con fuerza | Retraso | — |

**Redundancia esperable.** Cinco de las diez estrategias (ema_crossover, donchian_breakout,
macd_momentum, adx_di y, en parte, obv_trend) apuestan por la **continuación de tendencias**;
cuatro (rsi_reversion, bollinger_reversion, stoch_rsi y vwap_deviation en modo reversión) por la
**reversión**. Combinarlas no suma diez opiniones independientes (Módulo IX).

### Comprobación final del módulo

La estrategia RSI genera `signal = 1` en la vela 52. El motor rechaza la entrada por la pausa
tras tres pérdidas. En la vela 53 la estrategia sigue en `signal = 1` y la pausa ya terminó.
¿Entra el motor en la vela 54?

<details><summary>Ver respuesta</summary>

No. El motor solo entra en la **transición** de la señal a LONG (de 0 a 1 en la vela 52). La
entrada rechazada no se aplaza: en la vela 53 la señal sigue en 1, no hay transición, y el motor
no hace nada hasta que la estrategia pase por FLAT y vuelva a LONG. Es una regla de diseño del
motor (Módulo X), documentada en su cabecera.
</details>
