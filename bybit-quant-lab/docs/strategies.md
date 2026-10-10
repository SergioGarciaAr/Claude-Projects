# Estrategias

Las diez estrategias implementan la misma interfaz (`strategies/base.py`) y no conocen el motor
de backtesting. Cada una produce **eventos** (entrada larga, entrada corta, salida larga,
salida corta) a partir de indicadores causales. La base los convierte en un **estado objetivo**
por vela.

## Contrato común

Salida de `Strategy.generate_signals(data)` (una fila por vela, mismo índice que `data`):

| Columna | Significado |
|---|---|
| `signal` | Exposición objetivo al **cierre** de la vela: `1` LONG, `-1` SHORT, `0` FLAT. Se ejecuta en la apertura siguiente. |
| `conviction` | Intensidad del setup en `[0, 1]`, definida por cada estrategia. **No** es una probabilidad. Vale 0 en FLAT. |
| `stop_distance` | `ATR(atr_period) * stop_atr_mult` (en unidades de precio). |
| `take_profit_distance` | `stop_distance * take_profit_r`, o NaN si no hay objetivo. |
| `trailing_distance` | `ATR * trailing_atr_mult`, o NaN si no hay trailing. |

Reglas de la máquina de estados (`events_to_state`), evaluadas al cierre en este orden:

1. En LONG, una entrada SHORT provoca una reversión directa. Una salida LONG, o llegar a
   `max_holding_bars`, pasa a FLAT. Lo mismo, de forma simétrica, en SHORT.
2. En FLAT, si coinciden entradas LONG y SHORT en la misma vela, se ignoran (conflicto). Si
   no, se entra cuando han pasado más de `cooldown_bars` velas desde la última salida.
3. Si en la misma vela hay una entrada y una salida del mismo lado, prevalece la salida.

Otras reglas comunes:

- Mientras el ATR no esté disponible (calentamiento) no hay stop válido y la señal se fuerza a
  FLAT.
- Datos ausentes (NaN): las comparaciones con NaN son falsas, de modo que no se generan eventos.
  Los indicadores recursivos ignoran los NaN.
- `allow_short: false` elimina las entradas cortas.

Parámetros comunes (`StrategyParams`):

| Parámetro | Defecto | Descripción |
|---|---|---|
| `atr_period` | 14 | Período del ATR de Wilder |
| `stop_atr_mult` | 2.0 | Distancia del stop en ATR |
| `take_profit_r` | 2.0 | Objetivo en múltiplos de la distancia del stop (`null` = sin objetivo) |
| `trailing_atr_mult` | null | Trailing stop en ATR |
| `max_holding_bars` | null | Velas máximas en posición |
| `cooldown_bars` | 0 | Velas de espera tras una salida |
| `allow_short` | true | Permitir cortos |

Los valores por defecto de cada estrategia figuran en `configs/strategies.yaml`. No están
optimizados: son puntos de partida convencionales.

Notación: `C, O, H, L, V` = cierre, apertura, máximo, mínimo y volumen de la vela `t`;
`X[t-1]` = valor de la vela anterior; `cross_up(a, b)` = `a[t] > b[t]` y `a[t-1] <= b[t-1]`.

---

## A. Volumen

### 1. Volume Spike + Price Confirmation (`volume_spike`)

**Hipótesis.** Un volumen anormal **acompañado** de una vela direccional fuerte que rompe el
rango anterior indica participación en esa dirección. El volumen por sí solo no indica
dirección.

**Fórmulas.**
- `vol_ma[t] = SMA(V, volume_window)[t-1]`: solo velas anteriores.
- `ratio = V / vol_ma`; pico si `ratio > spike_mult`.
- `body_ratio = |C - O| / (H - L)`; vela fuerte si `body_ratio >= min_body_ratio`.
- Filtro de volatilidad: `min_atr_pct <= ATR/C <= max_atr_pct`.

**Entrada LONG:** pico, `C > O`, vela fuerte, filtro de volatilidad y, si
`require_range_break`, `C > H[t-1]`. **Entrada SHORT:** simétrica (`C < O`, `C < L[t-1]`).

**Salida o invalidación:** LONG si `C < EMA(C, exit_ema)`; SHORT si `C > EMA`. También al
alcanzar `max_holding_bars` (48 por defecto), por stop u objetivo.

**Convicción:** `clip(ratio / (2·spike_mult), 0, 1) · body_ratio`.

| Parámetro | Defecto |
|---|---|
| `volume_window` | 20 |
| `spike_mult` | 2.5 |
| `min_body_ratio` | 0.5 |
| `require_range_break` | true |
| `min_atr_pct` / `max_atr_pct` | 0 / null |
| `exit_ema` | 20 |
| `max_holding_bars` | 48 |

**Limitaciones.** El volumen de Bybit es el de un único exchange. Los picos de volumen al
inicio de la serie no se detectan hasta disponer de `volume_window` velas.

### 2. OBV Trend Confirmation (`obv_trend`)

**Hipótesis.** Cuando el OBV cruza su media con pendiente positiva y el precio está sobre su
media, el volumen confirma la tendencia.

**Fórmulas.** `OBV[t] = OBV[t-1] + sign(C[t] - C[t-1]) · V[t]`, con `OBV[0] = 0`.
`slope = OBV[t] - OBV[t - slope_window]`.

**Entrada LONG:** `cross_up(OBV, EMA(OBV, obv_ema))`, `slope > 0` y `C > EMA(C, price_ema)`.
**SHORT:** simétrica.

**Salida:** LONG si OBV cruza por debajo de su EMA o si `C < EMA(C, price_ema)`; SHORT de
forma simétrica.

**Anti-redundancia:** `cooldown_bars = 5` por defecto.

**Convicción:** `|OBV - EMA(OBV)| / (media(|ΔOBV|, obv_ema) · sqrt(obv_ema))`, recortada a
`[0, 1]`.

| Parámetro | Defecto |
|---|---|
| `obv_ema` | 20 |
| `price_ema` | 50 |
| `slope_window` | 5 |
| `cooldown_bars` | 5 |

**Limitaciones.** El valor absoluto del OBV depende del inicio de la serie; solo se usan sus
cruces y su pendiente, que no dependen de ese origen.

### 3. VWAP Deviation + Volume Regime (`vwap_deviation`)

**Hipótesis (dos hipótesis separadas, elegidas con `mode`; nunca se mezclan):**

- `reversion`: hay una desviación extrema respecto al VWAP con volumen **no elevado**. Se
  espera un retorno hacia el VWAP.
- `continuation`: hay una desviación extrema con volumen **elevado**. Se espera continuación.

**VWAP.** El precio típico es `TP = (H + L + C) / 3`.
- `rolling`: `Σ(TP·V) / ΣV` sobre `vwap_window` velas.
- `session`: acumulado que se reinicia en cada frontera de sesión UTC de duración `session`
  (por defecto `1D`, es decir, 00:00–24:00 UTC). El mercado opera 24/7, así que la sesión es
  una convención: el VWAP de las primeras velas de cada sesión se basa en pocos datos.

**Desviación normalizada.** `z = (C - VWAP) / std(C - VWAP, dev_window)[t-1]`.
**Volumen relativo.** `rel_vol = V / SMA(V, volume_window)[t-1]`.

| Modo | Entrada LONG | Entrada SHORT | Salida LONG | Salida SHORT |
|---|---|---|---|---|
| reversion | `z <= -entry_z` y `rel_vol <= max_rel_volume` | `z >= entry_z` y volumen tranquilo | `z >= -exit_z` | `z <= exit_z` |
| continuation | `z >= entry_z` y `rel_vol >= min_rel_volume` | `z <= -entry_z` y volumen activo | `z <= exit_z` | `z >= -exit_z` |

**Convicción:** `clip((|z| - entry_z) / entry_z, 0, 1)`.

| Parámetro | Defecto |
|---|---|
| `mode` | reversion |
| `vwap_type` | rolling |
| `vwap_window` | 96 |
| `session` | 1D |
| `dev_window` | 100 |
| `entry_z` / `exit_z` | 2.0 / 0.5 |
| `volume_window` | 50 |
| `max_rel_volume` / `min_rel_volume` | 1.5 / 1.5 |
| `take_profit_r` | null |

---

## B. Tendencia

### 4. EMA Crossover + Trend Filter (`ema_crossover`)

**Hipótesis.** Un cruce de una EMA rápida sobre una lenta, alineado con la tendencia larga y
con fuerza suficiente, captura tendencias.

**Entrada LONG:** `cross_up(EMA_fast, EMA_slow)`, `C > EMA(trend_ema)` (si está definida) y
un filtro de régimen:
- `adx`: `ADX >= adx_min`;
- `atr`: `ATR/C >= atr_pct_min`;
- `none`: sin filtro.

**SHORT:** simétrica. **Salida:** el cruce contrario de las EMAs.
**Convicción:** `clip(ADX / 50, 0, 1)`.

| Parámetro | Defecto |
|---|---|
| `fast` / `slow` | 12 / 26 (`fast < slow` obligatorio) |
| `trend_ema` | 200 |
| `regime_filter` | adx |
| `adx_period` / `adx_min` | 14 / 20 |
| `atr_pct_min` | 0.002 |

**Limitaciones.** Con la EMA de 200 se necesitan al menos 200 velas de calentamiento. En
mercados laterales el filtro reduce las señales, pero no las elimina.

### 5. Donchian Breakout + ATR (`donchian_breakout`)

**Hipótesis.** Un cierre fuera del canal de las `channel` velas **anteriores** inicia un
movimiento direccional.

**Fórmulas.** `upper[t] = max(H[t-channel .. t-1])` y `lower[t] = min(L[t-channel .. t-1])`.
El canal excluye la vela actual (desplazamiento de una vela).

**Entrada LONG:** `C > upper`. **SHORT:** `C < lower`. La señal se decide al cierre y se
ejecuta en la apertura siguiente.
**Salida:** LONG si `C < lower(exit_channel)`; SHORT si `C > upper(exit_channel)`. El trailing
stop está activo por defecto (3 ATR) y no hay objetivo fijo.

**Filtro de temporalidad superior (`htf`, p. ej. `"4h"`).** Las velas base se agregan a la
temporalidad superior. Una vela superior que abre en `T` solo está disponible al cerrar, en
`T + htf`. La vela base `t` usa la última vela superior que cumpla `T + htf <= t + base`. Las
velas superiores incompletas (con huecos o al final de la serie) se descartan. LONG solo si
`close_htf > EMA(close_htf, htf_ema)`; SHORT de forma simétrica.

**Convicción:** `clip(2 · |C - mid| / (upper - lower), 0, 1)`.

| Parámetro | Defecto |
|---|---|
| `channel` | 20 |
| `exit_channel` | 10 |
| `htf` | null |
| `htf_ema` | 50 |
| `take_profit_r` | null |
| `trailing_atr_mult` | 3.0 |

---

## C. Indicadores técnicos

### 6. RSI Mean Reversion (`rsi_reversion`)

**Hipótesis.** El regreso del RSI desde la zona de sobreventa (o sobrecompra) indica
agotamiento. Tocar la zona no basta: se exige el cruce de salida.

**Fórmula.** RSI de Wilder:
`RSI = 100 - 100 / (1 + media_W(ganancias) / media_W(pérdidas))`. Sin pérdidas vale 100; sin
movimiento, 50.

**Entrada LONG:** `cross_up(RSI, oversold)`. **SHORT:** `cross_down(RSI, overbought)`.
**Salida:** LONG si `RSI >= exit_level`; SHORT si `RSI <= exit_level`. También por
`max_holding_bars` (48).

**Filtro de tendencia (`trend_filter`):**
- `adx`: solo opera si `ADX < adx_max` (tendencia débil).
- `ema`: largos solo sobre la EMA larga y cortos solo bajo ella.
- `none`: sin filtro.

**Convicción:** profundidad de la incursión en la zona en las últimas 5 velas, recortada a
`[0, 1]`.

| Parámetro | Defecto |
|---|---|
| `rsi_period` | 14 |
| `oversold` / `overbought` | 30 / 70 |
| `exit_level` | 50 (`oversold < exit_level < overbought`) |
| `trend_filter` | adx |
| `trend_ema` | 200 |
| `adx_max` | 25 |
| `take_profit_r` | null |
| `max_holding_bars` | 48 |

### 7. MACD Momentum (`macd_momentum`)

**Fórmulas.** `MACD = EMA(fast) - EMA(slow)`, `señal = EMA(MACD, signal_period)` e
`histograma = MACD - señal`.

**Entrada LONG:** `cross_up(MACD, señal)`, histograma creciente (si `require_hist_rising`) y
filtro direccional:
- `ema`: `C > EMA(trend_ema)`;
- `zero_line`: `MACD > 0`;
- `none`: sin filtro.

**SHORT:** simétrica. **Salida:** el cruce contrario.

**Contribución incremental de los filtros.** Se mide comparando variantes con la orden de
sensibilidad, sin asumir que el filtro mejora el resultado:

```bash
bql sensitivity --symbol BTCUSDT --timeframe 1h --strategy macd_momentum \
  --grid '{"direction_filter": ["none", "ema", "zero_line"]}'
```

**Convicción:** `|hist| / max(|hist|, 100 velas)`.

| Parámetro | Defecto |
|---|---|
| `fast` / `slow` / `signal_period` | 12 / 26 / 9 |
| `require_hist_rising` | true |
| `direction_filter` | ema |
| `trend_ema` | 200 |

### 8. Bollinger Bands Reversion (`bollinger_reversion`)

**Hipótesis de reversión,** separada de la de ruptura de bandas. Un cierre **fuera** de la
banda seguido de un cierre de **regreso** dentro de ella anticipa el retorno a la media.
Tocar la banda no genera señal.

**Fórmulas.** `mid = SMA(C, period)` y `upper/lower = mid ± num_std · σ`, con σ poblacional
(ddof = 0).

**Entrada LONG:** `C[t-1] < lower[t-1]` y `C[t] > lower[t]`, con vela alcista si
`confirm_candle` y `ADX < adx_max` si este está definido. **SHORT:** simétrica.

**Salida:** al llegar a la media (LONG: `C >= mid`). **Invalidación:** un nuevo cierre fuera
de la banda en contra (LONG: `C < lower`).

**Convicción:** `|mid - C| / (ancho / 2)`.

| Parámetro | Defecto |
|---|---|
| `period` | 20 |
| `num_std` | 2.0 |
| `confirm_candle` | true |
| `adx_max` | 30 |
| `take_profit_r` | null |
| `max_holding_bars` | 48 |

### 9. Stochastic RSI (`stoch_rsi`)

**Fórmulas.** `raw = 100 · (RSI - min(RSI, n)) / (max(RSI, n) - min(RSI, n))`, con 50 si el
rango es 0. `%K = SMA(raw, k_smooth)` y `%D = SMA(%K, d_smooth)`.

**Entrada LONG:** `cross_up(%K, %D)` con `%K[t-1] < lower`, vela alcista si `confirm_candle`
y `C > EMA(trend_ema)` si esta está definida. **SHORT:** simétrica (`%K[t-1] > upper`).

**Anti-duplicados (rearmado).** Una nueva entrada LONG exige que `%K` haya superado
`rearm_level` desde la última entrada LONG conservada (`rearm_events`). Así, varios cruces
dentro de la misma zona extrema cuentan como una sola señal. Además, `cooldown_bars = 3`.

**Salida:** LONG si `%K` cruza por debajo de `%D` con `%K > rearm_level`; SHORT de forma
simétrica. Hay objetivo de 1,5 R y un máximo de 24 velas.

| Parámetro | Defecto |
|---|---|
| `rsi_period` / `stoch_period` | 14 / 14 |
| `k_smooth` / `d_smooth` | 3 / 3 |
| `lower` / `upper` | 20 / 80 |
| `rearm_level` | 50 |
| `confirm_candle` | true |
| `trend_ema` | null |
| `take_profit_r` | 1.5 |
| `max_holding_bars` | 24 |
| `cooldown_bars` | 3 |

### 10. ADX + DI Directional System (`adx_di`)

**Fórmulas.** Movimiento direccional de Wilder: `+DM` y `-DM`, `+DI = 100 · W(+DM) / ATR`,
`-DI` análogo, `DX = 100 · |+DI - -DI| / (+DI + -DI)` y `ADX = W(DX)`.

**Entrada LONG:** transición a `ADX >= adx_threshold` y `+DI - -DI > di_margin`, con ADX
creciente si `require_adx_rising`. **SHORT:** simétrica.

**Comportamiento con fuerza insuficiente.** Con `ADX < adx_threshold` no se abren posiciones.
Si `exit_on_weak_trend` está activo, una posición abierta se cierra cuando `ADX < adx_exit`;
la histéresis entre 25 y 20 evita entradas y salidas alternadas. También se sale cuando el
diferencial de DI cambia de signo.

| Parámetro | Defecto |
|---|---|
| `adx_period` | 14 |
| `adx_threshold` / `adx_exit` | 25 / 20 |
| `di_margin` | 2 |
| `require_adx_rising` | false |
| `exit_on_weak_trend` | true |
| `take_profit_r` | null |
| `trailing_atr_mult` | 3.0 |

---

## Pruebas por estrategia

En `tests/unit/test_strategies.py`:

- **Contrato:** columnas, dominio de la señal, convicción y stops.
- **No look-ahead:** se comprueba por truncamiento (calcular con datos hasta `t` produce las
  mismas señales hasta `t`) y por perturbación (alterar los precios y el volumen posteriores
  a `t` no cambia nada hasta `t`).
- **Condiciones límite:** datos vacíos, menos velas que el calentamiento, NaN intercalados,
  columnas ausentes, parámetros inválidos y modo solo largos.
- **Casos conocidos:** un pico de volumen con doji no genera señal; las hipótesis VWAP son
  excluyentes según el volumen; Donchian excluye la vela actual; tocar la banda de Bollinger
  no es señal y el reingreso sí; el ADX no entra con tendencia débil; el Stochastic RSI emite
  una sola señal por movimiento; el OBV no abre cortos en una tendencia alcista sostenida.
