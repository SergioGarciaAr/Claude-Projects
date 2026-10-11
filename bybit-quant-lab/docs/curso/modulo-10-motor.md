# Módulo X. El motor de backtesting

El motor es la pieza que convierte una serie de señales en operaciones, costes y una curva de
equity. Si el motor se equivoca, **todos** los resultados del proyecto son falsos, por buenas
que sean las estrategias. Por eso este módulo es el más detallado del curso: recorre el bucle
línea a línea, calcula una operación completa a mano y la reproduce con el código.

Archivos principales:

| Archivo | Papel |
|---|---|
| `src/bybit_quant_lab/backtesting/engine.py` | Bucle vela a vela, apertura y cierre de posiciones |
| `src/bybit_quant_lab/execution/costs.py` | Comisiones y deslizamiento |
| `src/bybit_quant_lab/execution/fills.py` | Stops, objetivos, gaps y liquidación con velas OHLC |
| `src/bybit_quant_lab/portfolio/position.py` | Posición abierta, trailing stop y registro de operación |
| `src/bybit_quant_lab/backtesting/results.py` | Contenedor de resultados |

El dimensionamiento, los límites de riesgo y la contabilidad de margen se tratan en el
Módulo XI; aquí se usan sus resultados.

---

## 10.1 Qué es un motor de backtesting y por qué uno "vela a vela"

**Intuición.** Un backtest responde a la pregunta: "si hubiera seguido estas reglas en el
pasado, ¿qué habría pasado con mi cuenta?". Para responderla sin hacer trampa hay que
reproducir el paso del tiempo: en cada momento solo se puede usar lo que ya se sabía.

**Dos familias de motores.**

- **Vectorizado:** calcula todo con operaciones sobre columnas completas
  (`posición × retorno`). Es rápido, pero modela mal los stops intravela, los costes que
  dependen del tamaño, los límites de riesgo que dependen de la equity y las salidas que
  dependen del camino recorrido.
- **Por eventos (vela a vela):** un bucle recorre las velas en orden y mantiene un **estado**
  (efectivo, posición, límites). Es más lento, pero cada decisión usa solo el estado anterior.

**[Diseño]** El proyecto usa un bucle explícito en Python (`for i in range(i0, i1 + 1)`). Es
más lento que una versión vectorizada, pero cada paso se puede leer y auditar.

**Término: determinista.** Con las mismas entradas produce exactamente las mismas salidas. El
motor no usa números aleatorios. `test_backtest_is_deterministic` lo comprueba ejecutando dos
veces y comparando equity y operaciones (`tests/unit/test_engine.py`, líneas 129–136).

---

## 10.2 El orden de los eventos dentro de una vela

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L1-L20 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 1–20

```python
"""Motor de backtesting determinista, vela a vela.

Orden de eventos dentro de cada vela ``i`` (índice = apertura de la vela):

1. Cambio de día UTC -> el gestor de riesgo reinicia la referencia diaria.
2. Funding: los pagos con marca de tiempo en ``(open[i-1], open[i]]`` se aplican a la
   posición mantenida al final de la vela ``i-1``, valorada a ``open[i]``.
3. Gap: si la apertura supera el stop/liquidación/objetivo, salida a la apertura.
4. Órdenes pendientes decididas al cierre de ``i-1``: primero salida, después entrada, ambas
   a ``open[i]`` con slippage adverso y comisión taker.
5. Intravela: stop/liquidación/objetivo con la regla *stop primero* (ver ``execution.fills``).
6. Cierre: valoración mark-to-market, registro de equity, límites de riesgo.
7. Trailing stop: se actualiza con el cierre y rige desde la vela siguiente.
8. Señal al cierre de ``i``: se programan órdenes para ``open[i+1]``. Nunca se ejecuta una
   señal al precio de la vela en que se generó.

Las entradas son *edge-triggered*: solo se abre posición cuando el objetivo de la estrategia
cambia a LONG/SHORT. Si un stop cierra la operación y la estrategia sigue en LONG, no se
reabre hasta una nueva transición. Las entradas rechazadas por riesgo no se difieren.
"""
```
<!-- fmt: on -->

**Por qué importa el orden.** Una vela OHLC resume una hora (o 5 minutos, o 4 horas) en cuatro
precios. Todo lo que ocurre dentro de ella ya pasó cuando se conoce el cierre. El motor tiene
que decidir **qué pudo hacerse y en qué momento**:

```text
open[i] ─────────────────────────────────────────────────── close[i]
  │ 1 día UTC  2 funding  3 gap  4 órdenes pendientes  5 intravela │ 6 valoración 7 trailing 8 señal
  └──────────────── precio disponible: open[i] ──────────────────┘   └──── se conoce close[i] ────┘
```

Los pasos 1–4 ocurren **en la apertura**; el 5, **durante** la vela; los 6–8, **al cierre**.
La señal calculada al cierre de `i` (paso 8) solo se ejecuta en la apertura de `i+1` (paso 4 de
la vela siguiente).

**[Hecho]** "Nunca se ejecuta una señal al precio de la vela en que se generó" (líneas 14–15).
Esta es la regla que impide el error más común de los backtests: decidir con el cierre y
comprar a ese mismo cierre, que en la realidad ya no está disponible cuando el cálculo termina.

**Comprobación.** Una estrategia calcula su señal con el cierre de la vela de las 10:00 (que
termina a las 10:59:59). ¿A qué precio entra el motor?

<details><summary>Ver respuesta</summary>

A la apertura de la vela de las 11:00, con deslizamiento adverso. Nunca al cierre de la vela
de las 10:00.
</details>

---

## 10.3 Preparación: entradas, segmento y arrays

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L71-L120 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 71–120

```python
    def run(
        self,
        data: pd.DataFrame,
        signals: pd.DataFrame,
        funding: pd.Series | None = None,
        start: pd.Timestamp | None = None,
        end: pd.Timestamp | None = None,
        regime: pd.Series | None = None,
        label: str = "",
        params: dict[str, Any] | None = None,
    ) -> BacktestResult:
        """Simula ``[start, end]`` (inclusive). Las señales deben estar alineadas con ``data``."""
        self._check_inputs(data, signals)
        idx = pd.DatetimeIndex(data.index)
        i0 = 0 if start is None else int(idx.searchsorted(start, side="left"))
        i1 = len(idx) - 1 if end is None else int(idx.searchsorted(end, side="right")) - 1
        warnings: list[str] = []
        if i1 < i0:
            raise ValueError("El segmento solicitado no contiene velas")
        cfg = self.config
        acct = Account(cfg.backtest.initial_capital)
        risk = RiskManager(cfg.risk, cfg.backtest.initial_capital)
        o = data["open"].to_numpy(float)
        h = data["high"].to_numpy(float)
        low = data["low"].to_numpy(float)
        c = data["close"].to_numpy(float)
        sig = signals["signal"].to_numpy(np.int64)
        conv = signals["conviction"].to_numpy(float)
        stop_d = signals["stop_distance"].to_numpy(float)
        tp_d = signals["take_profit_distance"].to_numpy(float)
        tr_d = signals["trailing_distance"].to_numpy(float)
        regimes = (
            regime.reindex(idx).fillna("unknown").astype(str).to_numpy()
            if regime is not None
            else None
        )
        funding_by_bar, funding_ok, fw = self._map_funding(funding, idx, i0, i1)
        stamps = list(idx[i0 : i1 + 1])
        # Identificador de día UTC independiente de la resolución del índice (ns, us, ms...).
        day_ids = (
            idx.floor("D").as_unit("s").tz_convert(None).to_numpy().astype("int64") // 86_400
        ).tolist()
        warnings.extend(fw)

        trades: list[TradeRecord] = []
        rejected: list[dict[str, Any]] = []
        rows: list[tuple[float, float, float, float, float, bool]] = []
        pending_exit: str | None = None
        pending_entry: _PendingEntry | None = None
        prev_target = int(sig[i0 - 1]) if i0 > 0 else 0
```
<!-- fmt: on -->

Línea a línea:

- **83:** `_check_inputs` (líneas 246–256) exige las columnas de señal, el **mismo índice** en
  datos y señales, datos no vacíos y precios sin `NaN`. Un índice desalineado es un error
  inmediato (`test_misaligned_signals_rejected`), no un `reindex` silencioso.
- **85–86:** `searchsorted` convierte las fechas `start`/`end` en posiciones. `i0` es la primera
  vela con `open_time ≥ start`; `i1`, la última con `open_time ≤ end`. El segmento es
  **inclusivo** en ambos extremos.
- **91–92:** cada simulación empieza con una cuenta y un gestor de riesgo nuevos: los segmentos
  no comparten estado.
- **93–101:** las columnas se convierten a arrays de NumPy (`to_numpy`). Acceder a `o[i]` en un
  array es mucho más rápido que `df["open"].iloc[i]` dentro de un bucle (Módulo V).
- **102–106:** el régimen es solo una **etiqueta** que se copia a cada operación.
- **107:** el funding se traduce a "pagos por índice de vela" (sección 10.6).
- **110–112:** identificador entero del día UTC para cada vela (días desde 1970-01-01), usado
  por el límite de pérdida diaria. Se calcula una sola vez para todo el índice. `as_unit("s")`
  fija la unidad antes de convertir a entero: un índice puede guardarse internamente en
  nanosegundos, microsegundos o milisegundos, y dividir el entero bruto por 86 400 solo es
  correcto si la unidad es el segundo. Se introdujo en `2f60aca`; antes, `on_bar_open`
  comparaba objetos `Timestamp` (`ts.floor("D")`) en cada vela.
- **120:** `prev_target` empieza con la señal de la vela **anterior al segmento**. Si una
  estrategia ya estaba larga antes de `start`, no hay transición al empezar y el motor **no
  entra** (`test_segment_start_does_not_enter_on_preexisting_signal`). Así, un segmento de
  validación no empieza con una entrada artificial.

---

## 10.4 El bucle, paso a paso

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L122-L148 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 122–148

```python
        for i in range(i0, i1 + 1):
            ts = stamps[i - i0]
            risk.on_bar_open(ts, day_ids[i])
            pos = acct.position
            # 2. funding
            if pos is not None and i in funding_by_bar:
                payment = pos.side * pos.qty * o[i] * funding_by_bar[i]
                acct.cash -= payment
                acct.total_funding += payment
                pos.funding += payment
            # 3. gap
            if pos is not None:
                gap = check_gap_exit(
                    pos.side, o[i], pos.stop, pos.take_profit, pos.liquidation_price
                )
                if gap is not None:
                    trades.append(self._close(acct, risk, gap, i, ts))
                    pending_exit = None
            # 4. pending orders at open
            if pending_exit is not None and acct.position is not None:
                trades.append(self._close(acct, risk, ExitCheck(o[i], pending_exit), i, ts))
            pending_exit = None
            if pending_entry is not None and acct.position is None:
                rej = self._open(acct, pending_entry, o[i], i, ts)
                if rej:
                    rejected.append({"time": str(ts), "side": pending_entry.side, "reason": rej})
            pending_entry = None
```
<!-- fmt: on -->

- **124 (paso 1):** el gestor de riesgo detecta el cambio de día UTC (Módulo XI).
- **127–131 (paso 2, funding):** `payment = lado × cantidad × open[i] × tasa`. Para un largo
  (`lado = +1`) con tasa positiva, `payment > 0` y el efectivo **baja**: el largo paga. Para un
  corto, `payment < 0` y el efectivo **sube**: el corto cobra. Se acumula en la cuenta y en la
  posición.
- **133–139 (paso 3, gap):** si la apertura ya está más allá del stop, la liquidación o el
  objetivo, se cierra ahí (sección 10.7). Si había una salida pendiente, se descarta: la
  posición ya no existe.
- **141–143 (paso 4, salida pendiente):** se ejecuta a `open[i]`. Primero la salida...
- **144–148 (paso 4, entrada pendiente):** ...después la entrada, solo si no queda posición.
  Si el dimensionamiento devuelve 0 (por ejemplo, cantidad por debajo del mínimo), la entrada
  se registra como **rechazada** con el motivo.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L149-L176 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 149–176

```python
            # 5. intrabar
            pos = acct.position
            if pos is not None:
                hit = check_intrabar_exit(
                    pos.side, h[i], low[i], pos.stop, pos.take_profit, pos.liquidation_price
                )
                if hit is not None:
                    trades.append(self._close(acct, risk, hit, i, ts))
            # 6. close / mark to market
            pos = acct.position
            unreal = pos.unrealized(c[i]) if pos else 0.0
            equity = acct.cash + unreal
            rows.append(
                (
                    equity,
                    acct.cash,
                    unreal,
                    pos.side * pos.qty if pos else 0.0,
                    acct.used_margin,
                    pos is not None,
                )
            )
            force_close = risk.on_bar_close(ts, equity)
            # 7. trailing
            if pos is not None:
                pos.update_trailing(c[i])
            if i == i1:
                break
```
<!-- fmt: on -->

- **150–156 (paso 5, intravela):** con el máximo y el mínimo de la vela se comprueba si se tocó
  stop, liquidación u objetivo (sección 10.7).
- **158–170 (paso 6, valoración):** `equity = efectivo + PnL no realizado al cierre`. Se guarda
  una fila por vela con equity, efectivo, no realizado, posición con signo, margen y si hay
  posición abierta.
- **171:** el gestor de riesgo evalúa la pérdida diaria y el drawdown con esa equity; puede
  pedir un cierre forzado.
- **173–174 (paso 7):** el trailing stop se mueve con el cierre; el nuevo nivel rige desde la
  vela siguiente (sección 10.8).
- **175–176:** en la última vela no se decide nada: no existe una apertura posterior donde
  ejecutar (`test_signal_on_last_bar_is_never_executed`).

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L177-L202 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 177–202

```python
            # 8. decision at close
            target = int(sig[i])
            if force_close and acct.position is not None:
                pending_exit = "risk_limit_close"
            elif acct.position is not None and target != acct.position.side:
                pending_exit = "signal_exit" if target == 0 else "signal_reverse"
            is_edge = target not in (0, prev_target)
            prev_target = target
            if is_edge:
                can_reverse = acct.position is None or (
                    pending_exit is not None and cfg.execution.allow_reversal
                )
                allowed, reason = risk.can_open(i)
                if not can_reverse:
                    rejected.append({"time": str(ts), "side": target, "reason": "position_open"})
                elif not allowed:
                    rejected.append({"time": str(ts), "side": target, "reason": reason})
                else:
                    pending_entry = _PendingEntry(
                        side=target,
                        stop_distance=float(stop_d[i]),
                        tp_distance=_nan_to_none(tp_d[i]),
                        trail_distance=_nan_to_none(tr_d[i]),
                        conviction=float(conv[i]),
                        regime=str(regimes[i]) if regimes is not None else "",
                    )
```
<!-- fmt: on -->

- **178:** `target` es el estado objetivo de la estrategia al cierre de `i`.
- **179–182:** se programa una salida si el riesgo lo exige o si el objetivo ya no coincide con
  el lado de la posición (a 0: `signal_exit`; al lado contrario: `signal_reverse`).
- **183 (entrada por transición):** `is_edge` es verdadero solo si el objetivo es +1 o −1
  **y** distinto del de la vela anterior. Mantener `signal = 1` durante 50 velas produce **una**
  entrada, no 50.
- **186–188:** se puede entrar si no hay posición, o si la hay pero se va a cerrar en la misma
  apertura y `allow_reversal` está activo (por defecto, sí).
- **189–193:** el gestor de riesgo puede vetar la entrada. La entrada vetada **se pierde**: no
  se reintenta en la vela siguiente, porque la siguiente no es una transición.
- **195–202:** la entrada queda pendiente con la distancia de stop, el objetivo, el trailing,
  la convicción y el régimen **de la vela de la señal**.

**[Diseño] Consecuencias de las entradas por transición.**

1. Si un stop cierra la operación y la estrategia sigue en +1, **no se reabre**. Hay que
   esperar a que la estrategia pase por 0 (o −1) y vuelva a +1.
2. Una entrada rechazada por riesgo no se aplaza (pregunta final del Módulo VIII).
3. La alternativa (entrar siempre que el objetivo sea +1 y no haya posición) reabriría
   posiciones justo después de cada stop, en la misma dirección que acaba de fallar.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L203-L207 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 203–207

```python
        # final
        if acct.position is not None and cfg.execution.close_at_end:
            trades.append(self._close(acct, risk, ExitCheck(c[i1], "end_of_data"), i1, idx[i1]))
            final_equity = acct.cash
            rows[-1] = (final_equity, acct.cash, 0.0, 0.0, 0.0, rows[-1][5])
```
<!-- fmt: on -->

- **204–207:** con `close_at_end` (por defecto activo), la posición abierta al final se cierra
  al **cierre** de la última vela con deslizamiento y comisión (`end_of_data`). La última fila
  de equity se sustituye por el efectivo final. Así, el resultado final siempre incluye el coste
  de salir.

---

## 10.5 Costes: comisión y deslizamiento

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/execution/costs.py#L1-L39 -->
`src/bybit_quant_lab/execution/costs.py` · líneas 1–39

```python
"""Modelo de costes: comisiones y slippage.

Todas las ejecuciones simuladas son órdenes a mercado o stops/TP disparados que se ejecutan
a mercado (comportamiento por defecto de TP/SL en Bybit), por lo que pagan comisión taker y
sufren slippage adverso de ``slippage_bps``.
"""

from __future__ import annotations

from dataclasses import dataclass

from bybit_quant_lab.config.models import CostConfig


@dataclass(frozen=True)
class CostModel:
    """Comisiones y slippage."""

    taker_fee: float
    maker_fee: float
    slippage_bps: float

    @classmethod
    def from_config(cls, cfg: CostConfig) -> CostModel:
        """Construye el modelo desde ``CostConfig``."""
        return cls(cfg.taker_fee, cfg.maker_fee, cfg.slippage_bps)

    @property
    def slip(self) -> float:
        """Slippage como fracción."""
        return self.slippage_bps / 10_000

    def fill_price(self, reference: float, direction: int) -> float:
        """Precio con slippage adverso; ``direction`` = +1 compra, -1 venta."""
        return reference * (1 + self.slip * direction)

    def fee(self, notional: float, taker: bool = True) -> float:
        """Comisión sobre el nocional (``qty * precio_ejecución``)."""
        return abs(notional) * (self.taker_fee if taker else self.maker_fee)
```
<!-- fmt: on -->

**Términos.**

- **Comisión taker:** la que cobra el exchange a la orden que **consume** liquidez (orden a
  mercado). **Maker:** la que **añade** liquidez (orden límite que espera en el libro).
- **Deslizamiento (slippage):** diferencia entre el precio de referencia y el precio realmente
  obtenido. Se expresa en **puntos básicos** (bps): 1 bp = 0,01 % = 0,0001.
- **Nocional:** cantidad × precio. Es el valor de la posición, no el dinero aportado.

**Fórmulas** (con `s = slippage_bps / 10 000` y `d = +1` al comprar, `−1` al vender):

```text
precio_ejecución = referencia × (1 + s · d)
comisión         = |cantidad × precio_ejecución| × taker_fee
```

Al comprar, `d = +1` y se paga **más**; al vender, `d = −1` y se recibe **menos**. El
deslizamiento siempre perjudica.

**[Hecho]** Todas las ejecuciones simuladas pagan comisión **taker**: entradas y salidas por
señal son órdenes a mercado, y los stops y objetivos se modelan como órdenes que se ejecutan a
mercado al dispararse. `maker_fee` existe en la configuración, pero el motor nunca llama a
`fee(..., taker=False)` (Módulo III, sección 3.7).

**[Supuesto]** 0,055 % (taker) es la tarifa base publicada por Bybit para perpetuos USDT sin
nivel VIP en el momento de escribir el código; 2 bps de deslizamiento es una estimación, no
una medición. Ambos deben contrastarse con la cuenta y el mercado reales (Módulo XVII).

---

## 10.6 Funding: cómo se asigna cada pago a una vela

**Intuición.** En un perpetuo, cada 8 horas (habitualmente a las 00:00, 08:00 y 16:00 UTC) los
largos pagan a los cortos o al revés, según la **tasa de funding**. Es lo que mantiene el precio
del perpetuo cerca del índice al contado.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L258-L283 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 258–283

```python
    def _map_funding(
        self, funding: pd.Series | None, idx: pd.DatetimeIndex, i0: int, i1: int
    ) -> tuple[dict[int, float], bool, list[str]]:
        if not self.config.costs.use_funding:
            return {}, False, ["Funding desactivado en la configuración."]
        if funding is None or funding.empty:
            return (
                {},
                False,
                [
                    "Sin datos históricos de funding: no se aplica (no se simula). El resultado "
                    "neto excluye el coste/ingreso de funding."
                ],
            )
        seg_start, seg_end = idx[i0], idx[i1]
        warnings = []
        if funding.index.min() > seg_start + FUNDING_INTERVAL or funding.index.max() < (
            seg_end - FUNDING_INTERVAL
        ):
            warnings.append("El funding disponible no cubre todo el período simulado.")
        out: dict[int, float] = {}
        positions = idx.searchsorted(pd.DatetimeIndex(funding.index), side="left")
        for j, rate in zip(positions, funding.to_numpy(float), strict=True):
            if i0 < j <= i1 and not np.isnan(rate):
                out[int(j)] = out.get(int(j), 0.0) + float(rate)
        return out, True, warnings
```
<!-- fmt: on -->

- **261–271:** sin funding activado o sin datos, no se aplica y se añade una **advertencia**
  explícita. El resultado neto queda sin ese coste o ingreso; no se inventa una tasa.
- **274–277:** si la serie de funding no cubre el segmento, otra advertencia.
- **279:** `searchsorted(..., side="left")` devuelve, para cada marca de funding `t`, la primera
  vela con `open_time ≥ t`. Un pago en `(open[j−1], open[j]]` se asigna a la vela `j`.
- **281:** `i0 < j`: un pago asignado a la primera vela del segmento se ignora, porque el
  segmento empieza sin posición. `j ≤ i1`: los pagos posteriores al segmento, también.
- **282:** si dos pagos caen en la misma vela (temporalidades largas), se suman.

**Ejemplo.** Velas de 1 h; pago a las 08:00. La vela de las 08:00 tiene `open_time = 08:00`, así
que `j` es esa vela. En el paso 2 de esa vela se cobra a la posición que estaba abierta **al
final de la vela de las 07:00**, valorada a `open` de las 08:00. Una entrada ejecutada en la
apertura de las 08:00 (paso 4, después del funding) no paga ese pago.

**[Supuesto]** El pago se valora a `cantidad × open[j]`. En Bybit se usa el precio de marca
(mark price) en el momento del cobro; la apertura de la vela es una aproximación.

---

## 10.7 Stops, objetivos, gaps y liquidación con velas OHLC

**El problema.** Una vela dice que el precio estuvo entre `low` y `high`, pero no **en qué
orden**. Si una vela toca a la vez el stop y el objetivo, no se sabe cuál ocurrió primero.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/execution/fills.py#L1-L74 -->
`src/bybit_quant_lab/execution/fills.py` · líneas 1–74

```python
"""Resolución de stops, objetivos y liquidación con velas OHLC.

Las velas OHLC no revelan el orden real de los precios dentro de la vela. Reglas aplicadas:

1. **Gap en apertura**: si la apertura ya está más allá de un nivel (stop, liquidación u
   objetivo), la orden se ejecuta a la apertura (precio realmente disponible).
2. **Intravela, stop primero**: si en la misma vela se tocan el nivel adverso (stop o
   liquidación) y el objetivo, se asume que se tocó **primero el adverso**. Nunca se asume
   el resultado más favorable.
3. **Gap más allá de la liquidación**: se liquida (pérdida = margen aislado), aunque el
   stop estuviera más cerca de la entrada.
4. **Liquidación frente a stop**: el nivel adverso efectivo es el más cercano al precio de
   entrada (para largos, ``max(stop, liquidación)``). Si ambos coinciden prevalece la
   liquidación.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExitCheck:
    """Salida detectada: precio de referencia (antes de slippage) y motivo."""

    price: float
    reason: str


def _adverse(side: int, stop: float | None, liq: float | None) -> tuple[float | None, str]:
    levels = [
        (lvl, name) for lvl, name in ((liq, "liquidation"), (stop, "stop_loss")) if lvl is not None
    ]
    if not levels:
        return None, ""
    # Largo: el nivel más alto se toca primero al caer; corto: el más bajo.
    best = max(levels, key=lambda x: x[0]) if side > 0 else min(levels, key=lambda x: x[0])
    return best


def check_gap_exit(
    side: int, open_: float, stop: float | None, take_profit: float | None, liq: float | None
) -> ExitCheck | None:
    """Comprueba si la apertura ya ha superado algún nivel.

    Si la apertura supera el precio de liquidación, la posición se liquida aunque el stop
    estuviera más cerca: con margen aislado la pérdida queda limitada al margen y nunca se
    ejecuta un stop a un precio peor que la liquidación.
    """
    if liq is not None and (open_ <= liq if side > 0 else open_ >= liq):
        return ExitCheck(liq, "liquidation_gap")
    level, name = _adverse(side, stop, liq)
    if level is not None and (open_ <= level if side > 0 else open_ >= level):
        return ExitCheck(open_, f"{name}_gap")
    if take_profit is not None and (open_ >= take_profit if side > 0 else open_ <= take_profit):
        return ExitCheck(open_, "take_profit_gap")
    return None


def check_intrabar_exit(
    side: int,
    high: float,
    low: float,
    stop: float | None,
    take_profit: float | None,
    liq: float | None,
) -> ExitCheck | None:
    """Comprueba la vela con la regla conservadora *stop primero*."""
    level, name = _adverse(side, stop, liq)
    if level is not None and (low <= level if side > 0 else high >= level):
        return ExitCheck(level, name)
    if take_profit is not None and (high >= take_profit if side > 0 else low <= take_profit):
        return ExitCheck(take_profit, "take_profit")
    return None
```
<!-- fmt: on -->

Reglas, en lenguaje llano:

1. **Gap en apertura** (`check_gap_exit`, líneas 41–57): si el precio **abre** más allá del stop
   (por ejemplo, el stop está en 95 y la vela abre en 90), no hubo ningún momento en que se
   pudiera vender a 95. Se ejecuta a la apertura, 90. Lo mismo con el objetivo: un gap
   favorable se ejecuta a la apertura, no al objetivo
   (`test_take_profit_gap_fills_at_open_not_at_target`).
2. **Stop primero** (`check_intrabar_exit`, líneas 60–74): si en la vela se tocan el nivel
   adverso y el objetivo, se asume que se tocó **primero el adverso**. Es la hipótesis
   pesimista: nunca se atribuye al backtest el mejor caso posible.
3. **Nivel adverso efectivo** (`_adverse`, líneas 30–38): entre stop y liquidación, cuenta el
   que se alcanza antes. Para un largo, el más alto; para un corto, el más bajo.
4. **Gap más allá de la liquidación** (líneas 50–51): se liquida aunque el stop estuviera más
   cerca. Corrección M-02 de la auditoría (`a50ac62`): antes se ejecutaba como stop a la
   apertura, con una pérdida mayor que el margen aislado.

**Ejemplo de stop primero** (`tests/unit/test_engine.py`, líneas 67–76): largo a 100, stop en
95, objetivo en 105; la vela 3 tiene `high = 120` y `low = 80`. Toca ambos. El motor registra
`stop_loss` a 95, con pérdida.

**Ejemplo de gap** (líneas 88–94 del mismo archivo): stop en 95, la vela abre en 90. Salida
`stop_loss_gap` a 90.

**[Limitación]** "Stop primero" es conservador para la **salida**, pero no resuelve todo:
con velas largas (4 h), una entrada y su stop pueden ocurrir en la misma vela de un modo que el
modelo no ve. Los datos de menor temporalidad son la única forma de reducir esa ambigüedad.

**[Hecho] El precio de salida de un stop es el nivel, más deslizamiento.** En `_close`
(sección 10.9) el precio de referencia `ex.price` (el nivel del stop) pasa por
`fill_price` con dirección contraria a la posición: un largo que sale por stop a 95 con 2 bps
vende a `95 × (1 − 0,0002)`.

---

## 10.8 Trailing stop

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/portfolio/position.py#L38-L53 -->
`src/bybit_quant_lab/portfolio/position.py` · líneas 38–53

```python
    def unrealized(self, price: float) -> float:
        """PnL no realizado a ``price`` (sin costes de salida)."""
        return self.side * (price - self.entry_price) * self.qty

    def update_trailing(self, close: float) -> None:
        """Actualiza el trailing stop con el cierre (solo puede mejorar el stop)."""
        if self.trailing_distance is None:
            return
        if self.side > 0:
            self.extreme = max(self.extreme, close)
            candidate = self.extreme - self.trailing_distance
            self.stop = candidate if self.stop is None else max(self.stop, candidate)
        else:
            self.extreme = min(self.extreme, close)
            candidate = self.extreme + self.trailing_distance
            self.stop = candidate if self.stop is None else min(self.stop, candidate)
```
<!-- fmt: on -->

**Intuición.** Un trailing stop "persigue" al precio: para un largo, se coloca a una distancia
fija por debajo del **máximo cierre** alcanzado y nunca baja.

- **47:** `extreme` guarda el cierre más favorable (empieza en el precio de entrada).
- **48–49:** el candidato es `extreme − distancia`; con `max`, el stop solo puede subir.
- **50–53:** espejo para cortos.

**Ejemplo** (`test_trailing_stop_moves_with_close`, `tests/unit/test_engine.py` líneas
105–111): entrada a 100 con stop 10 y trailing 10. Cierres 110, 120, 130 → stop 100, 110, 120.
La vela 6 abre en 130 y cae hasta 105: el stop de 120 se toca y la salida es a 120.

**[Diseño]** El trailing se actualiza con el **cierre** y en el paso 7, después de la
comprobación intravela. Usar el máximo de la vela sería más agresivo y crearía otra ambigüedad:
no se sabe si el máximo ocurrió antes o después del mínimo.

---

## 10.9 Apertura y cierre de una posición

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L285-L333 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 285–333

```python
    def _open(
        self, acct: Account, pe: _PendingEntry, ref_price: float, i: int, ts: pd.Timestamp
    ) -> str | None:
        cfg = self.config
        fill = self.costs.fill_price(ref_price, pe.side)
        equity = acct.equity(ref_price)
        sizing = size_position(
            equity,
            acct.used_margin,
            fill,
            pe.stop_distance,
            cfg.risk,
            cfg.execution,
            cfg.costs,
            self.spec,
        )
        if sizing.qty <= 0:
            return sizing.reason
        qty = sizing.qty
        notional = qty * fill
        fee = self.costs.fee(notional)
        lev = cfg.execution.leverage
        mmr = cfg.execution.maintenance_margin_rate
        liq = None
        if cfg.execution.simulate_liquidation:
            liq = fill * (1 - 1 / lev + mmr) if pe.side > 0 else fill * (1 + 1 / lev - mmr)
        acct.cash -= fee
        acct.total_fees += fee
        acct.total_slippage += abs(fill - ref_price) * qty
        acct.traded_notional += notional
        acct.position = Position(
            side=pe.side,
            qty=qty,
            entry_price=fill,
            entry_time=ts,
            entry_bar=i,
            stop=fill - pe.side * pe.stop_distance,
            take_profit=fill + pe.side * pe.tp_distance if pe.tp_distance else None,
            trailing_distance=pe.trail_distance,
            liquidation_price=liq,
            margin=notional / lev,
            entry_fee=fee,
            entry_slippage=abs(fill - ref_price) * qty,
            conviction=pe.conviction,
            extreme=fill,
            equity_at_entry=equity,
            regime=pe.regime,
        )
        return None
```
<!-- fmt: on -->

- **289:** precio de ejecución con deslizamiento.
- **290:** la equity para dimensionar se mide al precio de referencia (la apertura).
- **291–302:** `size_position` (Módulo XI) devuelve la cantidad o un motivo de rechazo.
- **304–305:** nocional y comisión de entrada.
- **309–310:** precio de liquidación aproximado (Módulo XI).
- **311–314:** la comisión sale del efectivo **en el momento de entrar**; el deslizamiento no se
  resta aparte porque ya está dentro del precio.
- **321–322:** stop y objetivo se fijan **respecto al precio de ejecución**, no a la apertura.
- **325:** margen = nocional / apalancamiento.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/backtesting/engine.py#L335-L382 -->
`src/bybit_quant_lab/backtesting/engine.py` · líneas 335–382

```python
    def _close(
        self, acct: Account, risk: RiskManager, ex: ExitCheck, i: int, ts: pd.Timestamp
    ) -> TradeRecord:
        pos = acct.position
        assert pos is not None
        if ex.reason.startswith("liquidation"):
            # Margen aislado: se pierde el margen inicial completo (aproximación).
            fill = pos.entry_price - pos.side * pos.margin / pos.qty
        else:
            fill = self.costs.fill_price(ex.price, -pos.side)
        exit_slip = abs(fill - ex.price) * pos.qty
        exit_fee = self.costs.fee(pos.qty * fill)
        price_pnl = pos.side * (fill - pos.entry_price) * pos.qty
        acct.cash += price_pnl - exit_fee
        acct.realized_pnl += price_pnl
        acct.total_fees += exit_fee
        acct.total_slippage += exit_slip
        acct.traded_notional += pos.qty * fill
        entry_ref = pos.entry_price - pos.side * pos.entry_slippage / pos.qty
        gross = pos.side * (ex.price - entry_ref) * pos.qty
        fees = pos.entry_fee + exit_fee
        net = price_pnl - fees - pos.funding
        eq_entry = pos.equity_at_entry or acct.initial_capital
        record = TradeRecord(
            symbol=self.symbol,
            side="LONG" if pos.side > 0 else "SHORT",
            entry_time=pos.entry_time,
            exit_time=ts,
            entry_bar=pos.entry_bar,
            exit_bar=i,
            qty=pos.qty,
            entry_price=pos.entry_price,
            exit_price=fill,
            gross_pnl=gross,
            fees=fees,
            slippage_cost=pos.entry_slippage + exit_slip,
            funding=pos.funding,
            net_pnl=net,
            return_on_equity=net / eq_entry if eq_entry else 0.0,
            bars_held=i - pos.entry_bar + 1,
            exit_reason=ex.reason,
            conviction=pos.conviction,
            equity_at_entry=eq_entry,
            regime=pos.regime,
        )
        acct.position = None
        risk.on_trade_closed(i, ts, net)
        return record
```
<!-- fmt: on -->

Las magnitudes de una operación cerrada (con `L` = lado ±1, `q` = cantidad):

| Campo | Fórmula | Qué representa |
|---|---|---|
| `price_pnl` (línea 347) | `L · (salida_ejec − entrada_ejec) · q` | Resultado con los precios realmente obtenidos |
| `gross_pnl` (línea 354) | `L · (salida_ref − entrada_ref) · q` | Resultado **sin** deslizamiento ni comisiones |
| `slippage_cost` (línea 370) | desliz. entrada + desliz. salida | Pérdida por ejecutar peor que la referencia |
| `fees` (línea 355) | comisión entrada + comisión salida | |
| `funding` | suma de pagos durante la operación | Positivo = pagado |
| `net_pnl` (línea 356) | `price_pnl − fees − funding` | Lo que cambió el efectivo |

**Identidad contable** que comprueban las pruebas:

```text
net_pnl = gross_pnl − slippage_cost − fees − funding
```

- **353:** el precio de referencia de entrada se reconstruye deshaciendo el deslizamiento
  guardado.
- **348:** el efectivo recibe `price_pnl − comisión de salida`; la de entrada ya se descontó al
  abrir y el funding, al pagarse.
- **381:** el gestor de riesgo recibe el `net_pnl` para la racha de pérdidas.

**[Diseño] Liquidación (líneas 340–342).** Si la salida es por liquidación, el precio de salida
no es el nivel de liquidación más deslizamiento, sino el precio que hace perder **exactamente
el margen**: `entrada − L · margen / q`. Con margen aislado, eso equivale a
`entrada · (1 − L/apalancamiento)` (el llamado *precio de quiebra*). La diferencia entre el
precio de liquidación (que incluye el margen de mantenimiento) y ese precio queda contabilizada
en `slippage_cost`. Ejemplo verificado con el escenario de
`test_gap_through_liquidation_loses_isolated_margin_only` (sin costes, apalancamiento 10):
entrada 100, liquidación 90,5, precio de quiebra 90, cantidad 12,5 → `gross_pnl` = −118,75,
`slippage_cost` = 6,25 (0,5 × 12,5) y `net_pnl` = −125 = −margen. Ese "deslizamiento" es en
realidad el margen de mantenimiento perdido; al leer los totales de deslizamiento conviene
saberlo.

---

## 10.10 Una operación completa calculada a mano

Escenario: largo en BTCUSDT 1 h con la **configuración por defecto** (`configs/default.yaml`):
capital 10 000 USDT, riesgo 1 %, taker 0,055 %, deslizamiento 2 bps, apalancamiento 3,
liquidación simulada. Distancia de stop 600 USDT y objetivo 1200 USDT (como un stop de 2 ATR
con `take_profit_r = 2`). Un pago de funding del 0,01 % a las 08:00.

Datos (hora UTC):

| Vela | Hora | open | high | low | close | signal |
|---|---|---|---|---|---|---|
| 0 | 05:00 | 30 000 | 30 100 | 29 900 | 30 000 | 0 |
| 1 | 06:00 | 30 000 | 30 150 | 29 950 | 30 100 | **1** |
| 2 | 07:00 | 30 100 | 30 300 | 30 050 | 30 250 | 1 |
| 3 | 08:00 | 30 250 | 30 500 | 30 200 | 30 400 | 1 |
| 4 | 09:00 | 30 400 | 31 400 | 30 350 | 31 350 | 1 |
| 5 | 10:00 | 31 350 | 31 400 | 31 300 | 31 380 | 1 |

**Paso 1. Señal.** Al cierre de la vela 1, `signal` pasa de 0 a 1: es una transición. Se
programa una entrada para la apertura de la vela 2.

**Paso 2. Precio de entrada** (vela 2, referencia `open = 30 100`):

```text
entrada_ejec = 30 100 × (1 + 0,0002) = 30 106,02
```

**Paso 3. Tamaño** (detalle en el Módulo XI). Riesgo = 10 000 × 1 % = 100 USDT. Coste estimado
por unidad = stop + precio × 2 × (comisión + deslizamiento):

```text
por_unidad = 600 + 30 106,02 × 2 × (0,00055 + 0,0002) = 600 + 45,159 = 645,159
q_bruta    = 100 / 645,159 = 0,1550004
```

Topes: exposición 3 × 10 000 / 30 106,02 = 0,996; apalancamiento máximo 5 → 1,661; margen
disponible (reserva 20 %) 0,8 × 10 000 × 3 / 30 106,02 = 0,797. Ninguno es menor que 0,155.
Redondeo hacia abajo al paso 0,001 → **q = 0,155 BTC**.

**Paso 4. Costes de entrada.**

```text
nocional            = 0,155 × 30 106,02         = 4 666,4331
comisión entrada    = 4 666,4331 × 0,00055      = 2,5665382
desliz. entrada     = 0,155 × (30 106,02 − 30 100) = 0,155 × 6,02 = 0,933100
margen              = 4 666,4331 / 3            = 1 555,4777
stop                = 30 106,02 − 600           = 29 506,02
objetivo            = 30 106,02 + 1 200         = 31 306,02
liquidación         = 30 106,02 × (1 − 1/3 + 0,005) ≈ 20 221,21   (muy por debajo del stop)
efectivo            = 10 000 − 2,5665382         = 9 997,433462
```

**Paso 5. Valoración al cierre de la vela 2** (close 30 250):

```text
no_realizado = (30 250 − 30 106,02) × 0,155 = 143,98 × 0,155 = 22,3169
equity       = 9 997,433462 + 22,3169 = 10 019,750362
```

**Paso 6. Funding** (apertura de la vela 3, 08:00, `open = 30 250`, tasa 0,0001):

```text
pago     = (+1) × 0,155 × 30 250 × 0,0001 = 0,468875   (el largo paga)
efectivo = 9 997,433462 − 0,468875 = 9 996,964587
```

Al cierre de la vela 3 (close 30 400): no realizado = 293,98 × 0,155 = 45,5669; equity =
10 042,531487.

**Paso 7. Salida** (vela 4). El mínimo, 30 350, no toca el stop (29 506,02). El máximo, 31 400,
supera el objetivo (31 306,02). Salida `take_profit` con referencia 31 306,02:

```text
salida_ejec     = 31 306,02 × (1 − 0,0002) = 31 299,758796
desliz. salida  = 0,155 × (31 306,02 − 31 299,758796) = 0,155 × 6,261204 = 0,970487
comisión salida = 0,155 × 31 299,758796 × 0,00055 = 4 851,462613 × 0,00055 = 2,6683044
```

**Paso 8. Resultado de la operación.**

```text
price_pnl     = (31 299,758796 − 30 106,02) × 0,155 = 1 193,738796 × 0,155 = 185,029513
gross_pnl     = (31 306,02 − 30 100) × 0,155       = 1 206,02 × 0,155     = 186,933100
slippage_cost = 0,933100 + 0,970487                                      =   1,903587
fees          = 2,5665382 + 2,6683044                                    =   5,2348426
funding       =                                                              0,468875
net_pnl       = 185,029513 − 5,2348426 − 0,468875                        = 179,325796
comprobación  = 186,933100 − 1,903587 − 5,2348426 − 0,468875             = 179,325796
equity final  = 10 000 + 179,325796                                      = 10 179,325796
```

Los términos están redondeados; con todos los decimales, ambas sumas dan 179,3257957.

De 186,93 USDT de movimiento de precio, los costes se llevan 7,61 (un 4 %). Con objetivos más
cortos o temporalidades menores, la proporción crece (Módulo XII, sección de costes).

**Paso 9. Después.** La estrategia sigue en `signal = 1` en las velas 4 y 5, pero no hay
transición: el motor **no reabre**.

**Reproducción con el código real:**

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.config.loader import load_config
from bybit_quant_lab.strategies.base import empty_signal_frame

idx = pd.date_range("2024-01-01 05:00", periods=6, freq="1h", tz="UTC", name="open_time")
datos = pd.DataFrame(
    {
        "open": [30000, 30000, 30100, 30250, 30400, 31350],
        "high": [30100, 30150, 30300, 30500, 31400, 31400],
        "low": [29900, 29950, 30050, 30200, 30350, 31300],
        "close": [30000, 30100, 30250, 30400, 31350, 31380],
        "volume": 100.0,
    },
    index=idx,
).astype(float)
senales = empty_signal_frame(idx)
senales["signal"] = [0, 1, 1, 1, 1, 1]
senales["conviction"] = [0.0, 1, 1, 1, 1, 1]
senales["stop_distance"] = 600.0
senales["take_profit_distance"] = 1200.0
funding = pd.Series([0.0001], index=[pd.Timestamp("2024-01-01 08:00", tz="UTC")])

res = run_backtest(datos, senales, load_config(), "BTCUSDT", "1h", funding=funding)
t = res.trades.iloc[0]
for campo in ["entry_time", "exit_time", "qty", "entry_price", "exit_price", "exit_reason"]:
    print(f"{campo:14s} {t[campo]}")
for campo in ["gross_pnl", "slippage_cost", "fees", "funding", "net_pnl"]:
    print(f"{campo:14s} {t[campo]:.6f}")
print()
print(res.equity[["equity", "cash", "unrealized", "position", "in_position"]].round(6).to_string())
print("equity final:", round(res.final_equity, 6))
print("advertencias:", res.warnings)
```
<!-- salida -->
```text
entry_time     2024-01-01 07:00:00+00:00
exit_time      2024-01-01 09:00:00+00:00
qty            0.155
entry_price    30106.02
exit_price     31299.758796000002
exit_reason    take_profit
gross_pnl      186.933100
slippage_cost  1.903587
fees           5.234843
funding        0.468875
net_pnl        179.325796

                                 equity          cash  unrealized  position  in_position
open_time                                                                               
2024-01-01 05:00:00+00:00  10000.000000  10000.000000      0.0000     0.000        False
2024-01-01 06:00:00+00:00  10000.000000  10000.000000      0.0000     0.000        False
2024-01-01 07:00:00+00:00  10019.750362   9997.433462     22.3169     0.155         True
2024-01-01 08:00:00+00:00  10042.531487   9996.964587     45.5669     0.155         True
2024-01-01 09:00:00+00:00  10179.325796  10179.325796      0.0000     0.000        False
2024-01-01 10:00:00+00:00  10179.325796  10179.325796      0.0000     0.000        False
equity final: 10179.325796
advertencias: ['Especificaciones de BTCUSDT no verificadas con instruments-info (valores de referencia).']
```

Todo coincide con el cálculo a mano. Detalles que la tabla de equity enseña:

- En la vela 4 `in_position` es `False`: la posición se cerró **durante** la vela y la fila se
  registra al cierre. Para la métrica de exposición (Módulo XII), esa vela no cuenta como "en
  posición".
- La advertencia recuerda que las especificaciones de BTCUSDT (paso de cantidad, mínimos) son
  valores de referencia no verificados con la API (Módulo XI).
- **[Diseño]** La equity intermedia valora la posición al cierre **sin** descontar los costes
  de salida. Es la convención habitual (mark-to-market), pero hace la curva ligeramente más
  optimista que el valor de liquidar en ese momento.

**Comprobación.** Repite el cálculo con deslizamiento 0 y comisión 0. ¿Cuál sería `net_pnl`?

<details><summary>Ver respuesta</summary>

Entrada 30 100, objetivo 31 300; por unidad = 600 → q = 100/600 = 0,16666 → 0,166.
`net = (31 300 − 30 100) × 0,166 − 0,166 × 30 250 × 0,0001 = 199,2 − 0,502 = 198,698`. El
tamaño cambia porque el dimensionamiento también incluye los costes estimados.
</details>

---

## 10.11 Reversiones y entradas rechazadas

Con `allow_reversal: true`, si la señal pasa de +1 a −1 el motor cierra el largo y abre el corto
**en la misma apertura** (primero la salida, luego la entrada; paso 4):

<!-- ejecutar -->
```python
import sys

sys.path.insert(0, ".")  # para importar los ayudantes de tests/conftest.py

from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.risk.instruments import InstrumentSpec
from tests.conftest import make_bars, manual_signals, zero_cost_config

spec = InstrumentSpec(
    "TEST", tick_size=0.01, qty_step=0.001, min_qty=0.001, max_qty=1e9, min_notional=0.0
)
datos = make_bars([100, 100, 100, 104, 104, 100, 100])
senales = manual_signals(datos.index, {1: 1, 3: -1}, stop=5)
res = run_backtest(datos, senales, zero_cost_config(), "TEST", "1h", spec=spec)
columnas = [
    "side",
    "entry_time",
    "exit_time",
    "qty",
    "entry_price",
    "exit_price",
    "exit_reason",
    "net_pnl",
]
print(res.trades[columnas].to_string())
```
<!-- salida -->
```text
    side                entry_time                 exit_time    qty  entry_price  exit_price     exit_reason  net_pnl
0   LONG 2024-01-01 02:00:00+00:00 2024-01-01 04:00:00+00:00  20.00        100.0       104.0  signal_reverse    80.00
1  SHORT 2024-01-01 04:00:00+00:00 2024-01-01 06:00:00+00:00  20.16        104.0       100.0     end_of_data    80.64
```

Lectura: señal larga en la vela 1 → entrada a la apertura de la 2 (100). Señal corta en la 3 →
en la apertura de la 4 se cierra el largo (`signal_reverse`, 104) y se abre el corto (104). El
corto se cierra al final de los datos (`end_of_data`). La segunda cantidad es mayor porque la
equity creció con la primera operación (riesgo 1 % de 10 080 sobre un stop de 5 → 20,16).

Las entradas rechazadas (por riesgo, por posición abierta o por tamaño insuficiente) se guardan
en `res.rejected_signals` con hora, lado y motivo. El informe HTML las resume (Módulo XV).

---

## 10.12 El resultado: `BacktestResult`

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/backtesting/results.py#L11-L46 -->
`src/bybit_quant_lab/backtesting/results.py` · líneas 11–46

```python
@dataclass
class BacktestResult:
    """Resultado completo de una simulación.

    ``equity``: una fila por vela simulada (cierre) con ``equity``, ``cash``, ``unrealized``,
    ``position`` (cantidad con signo), ``margin_used``, ``drawdown`` e ``in_position``.
    ``trades``: una fila por operación cerrada (ver ``TradeRecord``).
    """

    label: str
    symbol: str
    timeframe: str
    initial_capital: float
    equity: pd.DataFrame
    trades: pd.DataFrame
    risk_events: list[dict[str, Any]]
    rejected_signals: list[dict[str, Any]]
    totals: dict[str, float]
    funding_applied: bool
    warnings: list[str] = field(default_factory=list)
    params: dict[str, Any] = field(default_factory=dict)

    @property
    def final_equity(self) -> float:
        """Equity al cierre de la última vela."""
        return float(self.equity["equity"].iloc[-1]) if len(self.equity) else self.initial_capital

    @property
    def start(self) -> pd.Timestamp | None:
        """Primera vela simulada."""
        return self.equity.index[0] if len(self.equity) else None

    @property
    def end(self) -> pd.Timestamp | None:
        """Última vela simulada."""
        return self.equity.index[-1] if len(self.equity) else None
```
<!-- fmt: on -->

- `equity`: una fila por vela; incluye `drawdown = equity / máximo_acumulado − 1` (líneas 214–215
  de `engine.py`).
- `trades`: una fila por operación con los campos de `TradeRecord`
  (`portfolio/position.py`, líneas 56–83).
- `totals`: comisiones, deslizamiento, funding y nocional negociado **acumulados**.
- `funding_applied`: si se aplicó funding real. Si es `False`, el neto excluye el funding.
- `warnings`: advertencias que el informe muestra siempre.

---

## 10.13 Cómo las pruebas protegen el motor

| Prueba | Archivo | Qué impide |
|---|---|---|
| `test_signal_executes_at_next_open` | `test_engine.py` | Ejecutar al cierre de la señal |
| `test_fees_and_slippage_reduce_net_exactly` | `test_engine.py` | Costes mal sumados |
| `test_stop_and_target_same_bar_assumes_stop_first` | `test_engine.py` | Elegir el caso favorable |
| `test_gap_through_stop_fills_at_open` | `test_engine.py` | Ejecutar stops a precios que no existieron |
| `test_trailing_stop_moves_with_close` | `test_engine.py` | Trailing que retrocede |
| `test_funding_applied_only_when_data_present` | `test_engine.py` | Inventar funding |
| `test_backtest_is_deterministic` | `test_engine.py` | Resultados no reproducibles |
| `test_short_trade_with_fees_slippage_and_funding_by_hand` | `test_audit_engine.py` | Errores de signo en cortos |
| `test_gap_through_liquidation_loses_isolated_margin_only` | `test_audit_engine.py` | Pérdidas mayores que el margen (M-02) |
| `test_signal_on_last_bar_is_never_executed` | `test_audit_engine.py` | Ejecutar en una vela inexistente |
| `test_segment_start_does_not_enter_on_preexisting_signal` | `test_audit_engine.py` | Entradas artificiales al empezar un segmento |

La prueba de auditoría del corto calcula el resultado esperado con aritmética explícita,
independiente del motor:

<!-- fmt: off -->
<!-- cita: tests/unit/test_audit_engine.py#L49-L81 -->
`tests/unit/test_audit_engine.py` · líneas 49–81

```python
def test_short_trade_with_fees_slippage_and_funding_by_hand() -> None:
    # Velas: open[t] = close[t-1]. Señal SHORT al cierre de la vela 1, FLAT al cierre de la 3.
    df = make_bars([100, 100, 100, 95, 90, 90], spread=0.1)
    sig = manual_signals(df.index, {1: -1, 3: 0}, stop=20)
    fee, slip = 0.001, 0.001
    funding = pd.Series([0.0005], index=[df.index[3]])  # pago a las 03:00, posición abierta
    res = run_backtest(df, sig, _cfg(fee, 10.0), "TEST", "1h", spec=SPEC, funding=funding)
    t = res.trades.iloc[0]

    entry_ref, exit_ref = 100.0, 95.0  # open[2] y open[4]
    entry_fill = entry_ref * (1 - slip)  # venta: precio peor = más bajo
    exit_fill = exit_ref * (1 + slip)  # recompra: precio peor = más alto
    qty = _floor_qty(10_000 * 0.01 / (20 + entry_fill * 2 * (fee + slip)))
    fees = fee * qty * (entry_fill + exit_fill)
    funding_paid = -1 * qty * 100.0 * 0.0005  # el corto cobra con tasa positiva
    net = (entry_fill - exit_fill) * qty - fees - funding_paid

    assert t["side"] == "SHORT" and t["qty"] == pytest.approx(qty)
    assert t["entry_time"] == df.index[2] and t["exit_time"] == df.index[4]
    assert t["entry_price"] == pytest.approx(entry_fill)
    assert t["exit_price"] == pytest.approx(exit_fill)
    assert t["fees"] == pytest.approx(fees)
    assert t["funding"] == pytest.approx(funding_paid) and t["funding"] < 0
    assert t["gross_pnl"] == pytest.approx((entry_ref - exit_ref) * qty)
    assert t["slippage_cost"] == pytest.approx(
        qty * (entry_ref - entry_fill + exit_fill - exit_ref)
    )
    assert t["net_pnl"] == pytest.approx(net)
    assert t["net_pnl"] == pytest.approx(
        t["gross_pnl"] - t["fees"] - t["slippage_cost"] - t["funding"]
    )
    assert res.final_equity == pytest.approx(10_000 + net)
    assert res.totals["funding"] == pytest.approx(funding_paid)
```
<!-- fmt: on -->

---

## 10.14 Supuestos y limitaciones del motor

| Tema | Estado | Detalle |
|---|---|---|
| Ejecución a la siguiente apertura | [Diseño] | Evita usar el cierre conocido como precio de ejecución |
| Stop primero | [Diseño] | Conservador; no resuelve toda la ambigüedad intravela |
| Comisión siempre taker | [Supuesto] | Sin órdenes límite simuladas |
| Deslizamiento fijo en bps | [Supuesto] | No depende del tamaño, la volatilidad ni el libro |
| Liquidación con margen de mantenimiento fijo | [Limitación] | Bybit usa niveles por tamaño (Módulo XI) |
| Funding valorado a la apertura | [Supuesto] | Bybit usa el precio de marca |
| Precios no redondeados al tick | [Limitación] | `tick_size` existe en `InstrumentSpec` pero ningún módulo de `src` lo usa |
| Una posición por símbolo | [Diseño] | `max_open_positions` solo admite 1 |
| Huecos en los datos | [Limitación] | La posición se mantiene a través del hueco (M-06) |
| Margen de mantenimiento contado como deslizamiento en liquidaciones | [Hecho] | Sección 10.9 |
| Equity sin costes de salida | [Diseño] | Mark-to-market convencional |

### Comprobación final del módulo

Un largo tiene el stop en 95 y el objetivo en 110. La vela siguiente abre en 93, sube a 112 y
cierra en 108. ¿Cómo sale la operación y a qué precio de referencia?

<details><summary>Ver respuesta</summary>

Por `stop_loss_gap` a 93. El paso 3 (gap) se evalúa en la apertura, antes que la comprobación
intravela: la apertura ya está por debajo del stop, así que la posición se cierra a 93 (más
deslizamiento) y el máximo de 112 ya no importa.
</details>
