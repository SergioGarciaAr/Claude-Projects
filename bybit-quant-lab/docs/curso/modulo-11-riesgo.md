# Módulo XI. Gestión del riesgo y contabilidad

El Módulo X mostró **qué** hace el motor en cada vela. Este módulo explica **cuánto** arriesga
en cada operación, **cuándo** deja de operar y **cómo** lleva las cuentas. El código está en
`src/bybit_quant_lab/risk/` (`sizing.py`, `limits.py`, `instruments.py`) y
`src/bybit_quant_lab/portfolio/account.py`.

> **[Hecho]** Estos mecanismos limitan pérdidas **dentro de la simulación**. No garantizan
> nada en una cuenta real: los precios reales pueden saltar más allá de cualquier stop, y la
> liquidación de Bybit no se calcula exactamente como aquí.

---

## 11.0 Tres capas de protección distintas

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/risk/limits.py#L1-L19 -->
`src/bybit_quant_lab/risk/limits.py` · líneas 1–19

```python
"""Límites de riesgo del sistema, independientes de las estrategias.

Definiciones (todas evaluadas con equity *mark-to-market* al **cierre** de cada vela):

* **Pérdida diaria**: ``equity_cierre - equity_inicio_día_UTC``, donde ``equity_inicio_día``
  es la equity al cierre de la última vela del día UTC anterior (o el capital inicial). Incluye
  PnL realizado y no realizado. Si la pérdida alcanza ``max_daily_loss * equity_inicio_día``
  se bloquean nuevas entradas hasta el siguiente día UTC (``block``) o, además, se cierra la
  posición en la siguiente apertura (``close_and_block``).
* **Drawdown máximo**: ``1 - equity / máximo_histórico_equity``. Al alcanzar ``max_drawdown``
  se detienen las nuevas entradas durante el resto de la simulación (kill-switch).
* **Pérdidas consecutivas**: operaciones con PnL neto < 0 incrementan la racha, > 0 la
  reinician (== 0 no la modifica). Al llegar a ``max_consecutive_losses`` se pausan las
  entradas ``pause_bars_after_losses`` velas y la racha se reinicia. La pausa no anula
  ningún otro límite: al terminar, siguen aplicándose todos.

El stop de estrategia (por operación), estos límites del sistema y la liquidación del
exchange (simulada por el motor) son mecanismos distintos y se registran por separado.
"""
```
<!-- fmt: on -->

| Capa | Quién la define | Qué protege | Dónde |
|---|---|---|---|
| Stop de la estrategia | Cada estrategia (`stop_distance`) | Una operación | `engine.py`, `fills.py` |
| Límites del sistema | `RiskConfig` | La cuenta completa | `risk/limits.py` |
| Liquidación | El exchange (simulado) | El margen aislado de una posición | `engine.py`, `fills.py` |

**[Diseño]** Las tres son independientes y se registran por separado: una salida por stop se
anota como `stop_loss`, una por límite del sistema como `risk_limit_close` y una liquidación
como `liquidation` o `liquidation_gap`. Mezclarlas impediría saber qué falló.

**Analogía.** El stop es el cinturón de seguridad de un viaje; los límites del sistema, la
decisión de no volver a conducir hoy después de dos sustos; la liquidación, el airbag que el
fabricante dispara cuando el choque ya ocurrió. En el código, cada una corresponde a una
comprobación distinta del bucle (pasos 3, 5 y 6 de la sección 10.2).

---

## 11.1 Contabilidad de la cuenta

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/portfolio/account.py#L1-L48 -->
`src/bybit_quant_lab/portfolio/account.py` · líneas 1–48

```python
"""Cuenta de margen aislado con una posición como máximo por símbolo.

Contabilidad:

* ``cash`` = capital inicial + PnL realizado - comisiones - funding pagado.
* ``equity(price)`` = ``cash`` + PnL no realizado a ``price``.
* ``used_margin`` = nocional de entrada / apalancamiento.

El apalancamiento solo afecta al margen y al precio de liquidación, **no** al PnL de una
cantidad dada de contratos.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from bybit_quant_lab.portfolio.position import Position


@dataclass
class Account:
    """Estado contable de la simulación."""

    initial_capital: float
    cash: float = 0.0
    position: Position | None = None
    total_fees: float = 0.0
    total_slippage: float = 0.0
    total_funding: float = 0.0
    traded_notional: float = 0.0
    realized_pnl: float = 0.0
    history: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.cash = self.initial_capital

    @property
    def used_margin(self) -> float:
        """Margen inicial bloqueado por la posición abierta."""
        return self.position.margin if self.position else 0.0

    def equity(self, price: float) -> float:
        """Equity mark-to-market."""
        return self.cash + (self.position.unrealized(price) if self.position else 0.0)

    def available_margin(self, price: float) -> float:
        """Equity menos margen usado."""
        return self.equity(price) - self.used_margin
```
<!-- fmt: on -->

**Términos.**

- **Efectivo (`cash`):** capital inicial + PnL realizado − comisiones − funding pagado. El
  motor descuenta la comisión de entrada al abrir, el funding al pagarse y suma
  `price_pnl − comisión de salida` al cerrar (sección 10.9).
- **PnL no realizado:** ganancia o pérdida de la posición abierta si se cerrara al precio
  actual, **sin** costes de salida (`Position.unrealized`).
- **Equity:** efectivo + no realizado. Es lo que "vale" la cuenta en cada momento.
- **Margen inicial (`used_margin`):** nocional de entrada / apalancamiento. Es la parte de la
  equity que el exchange bloquea como garantía.
- **Margen aislado:** cada posición tiene su propio margen; si se liquida, se pierde ese margen
  y nada más. (En margen **cruzado**, toda la cuenta respalda las posiciones.)

**[Hecho] El apalancamiento no cambia el PnL.** Con la misma cantidad de contratos, ganar o
perder 1 USDT por movimiento de 1 USDT no depende del apalancamiento; solo cambian el margen
bloqueado y el precio de liquidación (cabecera, líneas 9–10). Lo comprueba
`test_leverage_does_not_change_pnl` (`tests/unit/test_risk.py`, líneas 145–155): mismas
operaciones con apalancamiento 2 y 5 → mismo `net_pnl`.

**Error común.** Pensar que "con apalancamiento 10 gano diez veces más". Con apalancamiento 10
**puedes** abrir una posición diez veces mayor que tu margen, pero el tamaño lo decide el
dimensionamiento por riesgo (sección 11.2), no el apalancamiento.

**[Hallazgo]** `available_margin` (líneas 46–48) y `history` (línea 32) no se usan en ningún
módulo de `src`: el dimensionamiento calcula el margen disponible por su cuenta (sección 11.2).
Es código sin efecto, no un error (Módulo III, sección 3.7).

---

## 11.2 Dimensionamiento por riesgo

**Intuición.** En lugar de decidir "compro 0,1 BTC", se decide "estoy dispuesto a perder el 1 %
de la cuenta si salta el stop". La cantidad se deduce de esa pérdida máxima y de la distancia
al stop: si el stop está lejos, se compra menos; si está cerca, más.

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/risk/sizing.py#L1-L71 -->
`src/bybit_quant_lab/risk/sizing.py` · líneas 1–71

```python
"""Dimensionamiento de posición basado en riesgo.

``qty = (equity * risk_per_trade) / (stop_distance + costes_estimados_por_unidad)``

Los costes estimados por unidad incluyen comisión taker y slippage de entrada y salida. El
resultado se limita por exposición por símbolo, apalancamiento máximo, margen disponible
(respetando la reserva) y tamaño máximo del instrumento, y se redondea **hacia abajo**.
"""

from __future__ import annotations

from dataclasses import dataclass

from bybit_quant_lab.config.models import CostConfig, ExecutionConfig, RiskConfig
from bybit_quant_lab.risk.instruments import InstrumentSpec


@dataclass(frozen=True)
class SizingResult:
    """Resultado del dimensionamiento: ``qty > 0`` o ``qty == 0`` con motivo."""

    qty: float
    reason: str = "ok"
    capped_by: str | None = None


def liquidation_distance(price: float, leverage: float, mmr: float) -> float:
    """Distancia aproximada a liquidación con margen aislado: ``price * (1/lev - mmr)``."""
    return price * max(1.0 / leverage - mmr, 0.0)


def size_position(
    equity: float,
    used_margin: float,
    price: float,
    stop_distance: float,
    risk: RiskConfig,
    execution: ExecutionConfig,
    costs: CostConfig,
    spec: InstrumentSpec,
) -> SizingResult:
    """Cantidad de contratos para entrar a ``price`` con stop a ``stop_distance``."""
    if equity <= 0:
        return SizingResult(0.0, "equity_non_positive")
    if not stop_distance > 0 or price <= 0:
        return SizingResult(0.0, "invalid_stop")
    if execution.simulate_liquidation and stop_distance >= liquidation_distance(
        price, execution.leverage, execution.maintenance_margin_rate
    ):
        return SizingResult(0.0, "stop_beyond_liquidation")
    slip = costs.slippage_bps / 10_000
    per_unit = stop_distance + price * 2 * (costs.taker_fee + slip)
    qty = equity * risk.risk_per_trade / per_unit
    caps = {
        "symbol_exposure": equity * risk.max_symbol_exposure / price,
        "max_leverage": equity * risk.max_leverage / price,
        "available_margin": max(equity * (1 - risk.margin_reserve) - used_margin, 0.0)
        * execution.leverage
        / price,
        "instrument_max_qty": spec.max_qty,
    }
    capped_by = None
    for name, cap in caps.items():
        if cap < qty:
            qty, capped_by = cap, name
    qty = spec.round_qty(qty)
    if qty < spec.min_qty:
        return SizingResult(0.0, "below_min_qty", capped_by)
    if qty * price < spec.min_notional:
        return SizingResult(0.0, "below_min_notional", capped_by)
    return SizingResult(qty, "ok", capped_by)
```
<!-- fmt: on -->

**Fórmula base** (con `E` = equity, `r` = `risk_per_trade`, `d` = distancia al stop en USDT,
`P` = precio de ejecución, `f` = comisión taker, `s` = deslizamiento como fracción):

```text
coste_por_unidad = d + P · 2 · (f + s)          (salir por el stop + costes de entrada y salida)
q_bruta          = E · r / coste_por_unidad
```

**Por qué se suman los costes (línea 52).** Si el stop salta, la pérdida real no es solo
`d × q`: también se pagan dos comisiones y dos deslizamientos. Incluirlos hace que la pérdida
total al tocar el stop sea aproximadamente `E · r`, no algo mayor. Con `d = 600` y
`P ≈ 30 106` (sección 10.10), los costes añaden 45,16 USDT por unidad, un 7,5 % más.

**Topes (líneas 54–65).** La cantidad se reduce al menor de:

| Tope | Fórmula | Defecto (`default.yaml`) |
|---|---|---|
| `symbol_exposure` | `E · max_symbol_exposure / P` | nocional ≤ 3 × E |
| `max_leverage` | `E · max_leverage / P` | nocional ≤ 5 × E |
| `available_margin` | `(E · (1 − margin_reserve) − margen_usado) · apalancamiento / P` | nocional ≤ 0,8 × 3 × E = 2,4 × E |
| `instrument_max_qty` | `spec.max_qty` | 100 BTC |

**[Hecho] Con la configuración por defecto, solo el tope de margen puede actuar.** Sin posición
abierta, el tope de margen permite un nocional de 2,4 × E, menor que 3 × E y que 5 × E. Los topes
de exposición y apalancamiento máximo quedan siempre por encima. Solo actuarían si se cambia la
reserva o el apalancamiento.

**¿Cuándo actúa el tope?** Cuando el nocional deseado supera 2,4 × E, es decir, cuando
`E · r / (d + 2P(f + s)) × P > 2,4 E`. Con `r = 1 %` y costes de 0,15 % del precio:

```text
d/P + 0,0015 < 0,01 / 2,4 = 0,004167   →   d/P < 0,267 %
```

Con un stop más cercano que el 0,27 % del precio (habitual en velas de 5 minutos con stops de
1–2 ATR), la posición queda limitada por el margen y el riesgo real por operación es **menor**
que el 1 %.

**Redondeo y mínimos (líneas 66–70).** La cantidad se redondea **hacia abajo** al paso del
instrumento (nunca aumenta el riesgo). Si queda por debajo de la cantidad mínima o del nocional
mínimo, la entrada se rechaza con el motivo correspondiente.

**Stop más allá de la liquidación (líneas 47–50).** Si el stop está más lejos que el precio de
liquidación, el stop nunca se alcanzaría antes que la liquidación: la entrada se rechaza
(`stop_beyond_liquidation`).

Tres casos con la configuración por defecto, a 30 106,02 USDT:

<!-- ejecutar -->
```python
from bybit_quant_lab.config.loader import load_config
from bybit_quant_lab.risk import size_position
from bybit_quant_lab.risk.instruments import get_spec

cfg = load_config()
spec = get_spec("BTCUSDT")
precio = 30_106.02
for stop in (600.0, 60.0, 15_000.0):
    r = size_position(10_000, 0.0, precio, stop, cfg.risk, cfg.execution, cfg.costs, spec)
    print(
        f"stop={stop:>8.0f}  qty={r.qty:<6}  motivo={r.reason:<24} tope={r.capped_by}  "
        f"nocional={r.qty * precio:,.2f}"
    )
```
<!-- salida -->
```text
stop=     600  qty=0.155   motivo=ok                       tope=None  nocional=4,666.43
stop=      60  qty=0.797   motivo=ok                       tope=available_margin  nocional=23,994.50
stop=   15000  qty=0.0     motivo=stop_beyond_liquidation  tope=None  nocional=0.00
```

Lectura:

- **Stop 600:** el caso de la sección 10.10. Ningún tope actúa.
- **Stop 60 (0,2 % del precio):** la fórmula pediría 100 / (60 + 45,16) ≈ 0,951 BTC, pero el
  margen limita a 0,797 BTC (nocional 23 994,50 ≈ 2,4 × 10 000). Si salta el stop, la pérdida
  será ≈ 0,797 × 105,16 ≈ 83,8 USDT, no 100.
- **Stop 15 000:** con apalancamiento 3 la liquidación está a ≈ 32,8 % del precio
  (`1/3 − 0,005`), es decir, a ≈ 9 885 USDT. El stop está más lejos: entrada rechazada.

**Comprobación.** Con equity 10 000, riesgo 1 %, stop de 5 USDT, precio 100 y sin costes, ¿qué
cantidad sale? (`test_size_uses_stop_distance_and_costs`.)

<details><summary>Ver respuesta</summary>

100 / 5 = 20 unidades. En la prueba se desactivan los topes (`max_symbol_exposure=100`,
`margin_reserve=0`, apalancamiento 10) para que ninguno actúe.
</details>

---

## 11.3 Especificaciones del instrumento

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/risk/instruments.py#L1-L67 -->
`src/bybit_quant_lab/risk/instruments.py` · líneas 1–67

```python
"""Especificaciones de instrumentos (precisión, tamaños mínimos y máximos).

Los valores por defecto son **referencias** para BTCUSDT y ETHUSDT lineales y deben
contrastarse con ``GET /v5/market/instruments-info`` (``BybitPublicClient.fetch_instrument_info``
y ``spec_from_bybit``), ya que Bybit puede modificarlos.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class InstrumentSpec:
    """Restricciones de cantidad y precio de un contrato lineal."""

    symbol: str
    tick_size: float
    qty_step: float
    min_qty: float
    max_qty: float
    min_notional: float = 5.0
    verified: bool = False

    def round_qty(self, qty: float) -> float:
        """Redondea hacia abajo al múltiplo de ``qty_step`` (nunca aumenta el riesgo)."""
        if qty <= 0:
            return 0.0
        steps = math.floor(qty / self.qty_step + 1e-9)
        decimals = max(0, -math.floor(math.log10(self.qty_step)))
        return round(steps * self.qty_step, decimals)


DEFAULT_SPECS: dict[str, InstrumentSpec] = {
    "BTCUSDT": InstrumentSpec(
        "BTCUSDT", tick_size=0.1, qty_step=0.001, min_qty=0.001, max_qty=100.0
    ),
    "ETHUSDT": InstrumentSpec(
        "ETHUSDT", tick_size=0.01, qty_step=0.01, min_qty=0.01, max_qty=1000.0
    ),
}


def get_spec(symbol: str) -> InstrumentSpec:
    """Especificación por defecto del símbolo (genérica y no verificada si no existe)."""
    spec = DEFAULT_SPECS.get(symbol.upper())
    if spec is not None:
        return spec
    return InstrumentSpec(
        symbol.upper(), tick_size=0.0001, qty_step=0.001, min_qty=0.001, max_qty=1e9
    )


def spec_from_bybit(info: dict[str, Any]) -> InstrumentSpec:
    """Construye la especificación a partir de un registro de ``instruments-info``."""
    lot, price = info["lotSizeFilter"], info["priceFilter"]
    return InstrumentSpec(
        symbol=str(info["symbol"]),
        tick_size=float(price["tickSize"]),
        qty_step=float(lot["qtyStep"]),
        min_qty=float(lot["minOrderQty"]),
        max_qty=float(lot.get("maxMktOrderQty") or lot["maxOrderQty"]),
        min_notional=float(lot.get("minNotionalValue") or 0.0),
        verified=True,
    )
```
<!-- fmt: on -->

- **`qty_step`:** incremento mínimo de cantidad (0,001 BTC).
- **`min_qty` / `max_qty`:** cantidad mínima y máxima por orden.
- **`min_notional`:** nocional mínimo (5 USDT por defecto).
- **`tick_size`:** incremento mínimo de precio.
- **`verified`:** `True` solo si la especificación se construyó con datos de la API
  (`spec_from_bybit`).

**Línea 31: el `+ 1e-9`.** `0,3 / 0,1` en coma flotante da `2,9999999999999996`
(Módulo II). Sin la pequeña tolerancia, `floor` daría 2 en lugar de 3 y se perdería un paso.
La línea 33 redondea al número de decimales del paso para eliminar residuos como
`0,15500000000000003`.

<!-- ejecutar -->
```python
import math

from bybit_quant_lab.risk.instruments import get_spec

print("0.3 / 0.1 =", 0.3 / 0.1, "-> floor:", math.floor(0.3 / 0.1))
spec = get_spec("BTCUSDT")
for q in (0.3, 0.1550004, 0.0009):
    print(q, "->", spec.round_qty(q))
print("verificada:", spec.verified)
```
<!-- salida -->
```text
0.3 / 0.1 = 2.9999999999999996 -> floor: 2
0.3 -> 0.3
0.1550004 -> 0.155
0.0009 -> 0.0
verificada: False
```

**[Limitación]** Las especificaciones por defecto (líneas 36–43) son **valores de referencia**
no verificados con la API, y el motor lo advierte en cada resultado (sección 10.10). Ninguna
orden de la CLI llama hoy a `spec_from_bybit` para sustituirlas. **[Limitación]** `tick_size`
no se usa: los precios de stop y objetivo no se redondean al tick (sección 10.14).

---

## 11.4 Liquidación aproximada

**Intuición.** Con margen aislado, si las pérdidas de la posición consumen el margen (menos un
pequeño colchón llamado **margen de mantenimiento**), el exchange cierra la posición a la fuerza.
Ese precio es el **precio de liquidación**.

**Fórmula usada** (`engine.py`, línea 310; `L` = lado, `A` = apalancamiento, `m` =
`maintenance_margin_rate`):

```text
largo: liq = entrada · (1 − 1/A + m)
corto: liq = entrada · (1 + 1/A − m)
```

**Derivación para un largo.** El margen es `entrada · q / A`. Se liquida cuando la pérdida
alcanza el margen menos el mantenimiento (`m · entrada · q`):

```text
(entrada − liq) · q = entrada · q / A − m · entrada · q
liq = entrada · (1 − 1/A + m)
```

**Ejemplo** (sección 10.10): entrada 30 106,02, A = 3, m = 0,005 →
`30 106,02 × 0,671667 ≈ 20 221,21`. El stop (29 506,02) está mucho más cerca: la liquidación
solo importaría con un gap enorme.

**Precio de quiebra.** El precio al que se pierde **exactamente** el margen:
`entrada · (1 − 1/A)` para un largo. El motor ejecuta las liquidaciones a ese precio
(sección 10.9), así que la pérdida es el margen completo.

**[Limitación]** En Bybit, la tasa de mantenimiento depende del **nivel de riesgo** (*risk
limit*) según el tamaño de la posición, y el cálculo real incluye otros términos. El
comentario de `configs/default.yaml` (línea 28) lo advierte: "aproximación; Bybit usa niveles
de riesgo". Con apalancamiento 3 y stops de pocos ATR, la liquidación casi nunca interviene;
con apalancamientos altos, la aproximación pesa más.

**Comprobación.** Con apalancamiento 10 y m = 0,005, ¿a qué distancia porcentual de la entrada
se liquida un largo?

<details><summary>Ver respuesta</summary>

`1/10 − 0,005 = 0,095`: un 9,5 % por debajo de la entrada. Es el caso de la prueba de
auditoría M-02 (entrada 100, liquidación 90,5).
</details>

---

## 11.5 Límites del sistema: `RiskManager`

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/risk/limits.py#L44-L131 -->
`src/bybit_quant_lab/risk/limits.py` · líneas 44–131

```python
@dataclass
class RiskManager:
    """Estado y reglas de los límites de riesgo."""

    config: RiskConfig
    initial_equity: float
    day: int | None = None
    day_start_equity: float = 0.0
    last_equity: float = 0.0
    peak_equity: float = 0.0
    consecutive_losses: int = 0
    pause_until_bar: int = -1
    daily_blocked: bool = False
    halted: bool = False
    events: list[RiskEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.day_start_equity = self.last_equity = self.peak_equity = self.initial_equity

    def on_bar_open(self, ts: pd.Timestamp, day: int | None = None) -> None:
        """Gestiona el cambio de día UTC (reinicia la referencia diaria y el bloqueo diario).

        ``day`` es un identificador entero del día UTC (opcional, para evitar recalcularlo).
        """
        if day is None:
            day = int(ts.floor("D").as_unit("s").value // 86_400)
        if self.day is None:
            self.day = day
            return
        if day != self.day:
            self.day = day
            self.day_start_equity = self.last_equity
            if self.daily_blocked:
                self.events.append(RiskEvent(str(ts), "daily_block_lifted", "nuevo día UTC"))
            self.daily_blocked = False

    def on_bar_close(self, ts: pd.Timestamp, equity: float) -> bool:
        """Actualiza límites con la equity al cierre. Devuelve ``True`` si hay que cerrar."""
        self.last_equity = equity
        self.peak_equity = max(self.peak_equity, equity)
        force_close = False
        daily_pnl = equity - self.day_start_equity
        if (
            not self.daily_blocked
            and daily_pnl <= -self.config.max_daily_loss * self.day_start_equity
        ):
            self.daily_blocked = True
            self.events.append(
                RiskEvent(
                    str(ts),
                    "daily_loss_limit",
                    f"pnl_dia={daily_pnl:.2f} ref={self.day_start_equity:.2f}",
                )
            )
            force_close |= self.config.daily_loss_action == "close_and_block"
        dd = 1 - equity / self.peak_equity if self.peak_equity > 0 else 0.0
        if not self.halted and dd >= self.config.max_drawdown:
            self.halted = True
            self.events.append(RiskEvent(str(ts), "max_drawdown_halt", f"drawdown={dd:.4f}"))
            force_close |= self.config.drawdown_action == "close_and_block"
        return force_close

    def on_trade_closed(self, bar_index: int, ts: pd.Timestamp, net_pnl: float) -> None:
        """Actualiza la racha de pérdidas y activa la pausa si corresponde."""
        if net_pnl < 0:
            self.consecutive_losses += 1
        elif net_pnl > 0:
            self.consecutive_losses = 0
        if self.consecutive_losses >= self.config.max_consecutive_losses:
            self.pause_until_bar = bar_index + self.config.pause_bars_after_losses
            self.events.append(
                RiskEvent(
                    str(ts),
                    "loss_streak_pause",
                    f"{self.consecutive_losses} pérdidas; pausa hasta vela {self.pause_until_bar}",
                )
            )
            self.consecutive_losses = 0

    def can_open(self, bar_index: int) -> tuple[bool, str]:
        """Indica si se permiten nuevas entradas decididas en la vela ``bar_index``."""
        if self.halted:
            return False, "max_drawdown_halt"
        if self.daily_blocked:
            return False, "daily_loss_limit"
        if bar_index < self.pause_until_bar:
            return False, "loss_streak_pause"
        return True, "ok"
```
<!-- fmt: on -->

### Pérdida diaria (líneas 63–98)

**Definición.**

```text
pnl_día = equity_cierre − equity_inicio_día
bloqueo si pnl_día ≤ −max_daily_loss · equity_inicio_día
```

- `equity_inicio_día` es la equity al cierre de la **última vela del día UTC anterior**
  (`on_bar_open`, línea 75, toma `last_equity`). En el primer día, el capital inicial.
- Incluye PnL **realizado y no realizado**: una posición abierta que pierde un 6 % bloquea
  aunque no se haya cerrado.
- `block` impide nuevas entradas hasta el siguiente día UTC; `close_and_block` además cierra la
  posición en la siguiente apertura (`risk_limit_close`).

**Ejemplo** (`test_daily_loss_blocks_until_next_utc_day`, líneas 96–105): equity de inicio 1000,
cierre a 940 → `pnl_día = −60 ≤ −0,05 × 1000 = −50` → bloqueo. Al empezar el día siguiente se
levanta el bloqueo y la nueva referencia es 940.

**[Diseño] Por qué "día UTC".** Bybit y la mayoría de los datos de criptomonedas usan UTC; es
una frontera fija e independiente del huso horario del usuario.

### Drawdown máximo (líneas 99–103)

```text
drawdown = 1 − equity / máximo_histórico_de_equity
```

Al alcanzar `max_drawdown` (15 %), `halted` pasa a `True` **para el resto de la simulación**
(kill-switch). No hay reactivación.

**Ejemplo** (`test_pause_does_not_override_other_limits`): capital 1000, equity 850 → drawdown
15 % ≥ 10 % configurado en la prueba → `halted`.

### Racha de pérdidas (líneas 106–121)

- `net_pnl < 0` suma 1 a la racha; `net_pnl > 0` la reinicia; exactamente 0 no la cambia.
- Al llegar a 3 (por defecto), las entradas se pausan `pause_bars_after_losses` velas (24) y la
  racha vuelve a 0.
- La racha usa el PnL **neto** (con comisiones y funding): una operación que gana 0,50 USDT de
  precio y paga 1 USDT de comisiones cuenta como pérdida.

### Orden de prioridad (líneas 123–131)

`can_open` devuelve el **primer** motivo que bloquea: drawdown, después pérdida diaria, después
pausa. La pausa no levanta ningún otro límite (cabecera, líneas 14–15).

### Ejemplo en el motor: tres stops seguidos

<!-- ejecutar -->
```python
import sys

sys.path.insert(0, ".")  # ayudantes de tests/conftest.py

from bybit_quant_lab.backtesting import run_backtest
from bybit_quant_lab.risk.instruments import InstrumentSpec
from tests.conftest import make_bars, manual_signals, zero_cost_config

spec = InstrumentSpec(
    "TEST", tick_size=0.01, qty_step=0.001, min_qty=0.001, max_qty=1e9, min_notional=0.0
)
cierres = [100, 100, 100, 90, 100] * 5  # cinco caídas iguales
mapa = {}
for k in range(5):
    mapa[5 * k + 1], mapa[5 * k + 4] = 1, 0  # largo en 1, 6, 11...; FLAT en 4, 9, 14...
datos = make_bars(cierres, spread=0.1)
senales = manual_signals(datos.index, mapa, stop=5)
cfg = zero_cost_config(max_consecutive_losses=3, pause_bars_after_losses=100)
res = run_backtest(datos, senales, cfg, "TEST", "1h", spec=spec)
print(res.trades[["entry_bar", "exit_bar", "exit_reason", "qty", "net_pnl"]].to_string())
print("eventos:", res.risk_events)
print("rechazadas:", res.rejected_signals)
```
<!-- salida -->
```text
   entry_bar  exit_bar exit_reason     qty  net_pnl
0          2         3   stop_loss  20.000  -100.00
1          7         8   stop_loss  19.800   -99.00
2         12        13   stop_loss  19.602   -98.01
eventos: [{'time': '2024-01-01 13:00:00+00:00', 'kind': 'loss_streak_pause', 'detail': '3 pérdidas; pausa hasta vela 113'}]
rechazadas: [{'time': '2024-01-01 16:00:00+00:00', 'side': 1, 'reason': 'loss_streak_pause'}, {'time': '2024-01-01 21:00:00+00:00', 'side': 1, 'reason': 'loss_streak_pause'}]
```

Lectura:

- Cada operación pierde el 1 % de la equity **del momento**: 100, 99, 98,01. El riesgo es
  proporcional a la equity, así que tras pérdidas las posiciones se reducen.
- La tercera pérdida se cierra en la vela 13 → pausa hasta la vela 13 + 100 = 113.
- Las señales de las velas 16 y 21 (transiciones a LONG) se rechazan con `loss_streak_pause`.
  Para el motor, una entrada decidida en la vela `i` se permite si `i ≥ pause_until_bar`.

**[Limitación] Límites evaluados solo al cierre.** El drawdown y la pérdida diaria se miden con
la equity al **cierre** de cada vela. Dentro de una vela la pérdida puede ser mayor, y una sola
vela (o un gap) puede llevar el drawdown mucho más allá del 15 % antes de que el límite
reaccione. El límite **no es un stop**: impide nuevas entradas; con `block` (por defecto) no
cierra la posición abierta.

---

## 11.6 Una prueba de regresión sobre el día UTC

<!-- fmt: off -->
<!-- cita: tests/unit/test_risk.py#L158-L171 -->
`tests/unit/test_risk.py` · líneas 158–171

```python
@pytest.mark.parametrize("unit", ["ns", "us", "ms", "s"])
def test_daily_reference_resets_regardless_of_index_resolution(unit: str) -> None:
    # Regresión: el identificador de día no debe depender de la resolución del índice.
    # Día 1: -3 %; día 2: otro -3 %. Con reinicio diario correcto nunca se alcanza el 5 %
    # diario; sin reinicio la pérdida acumulada (~6 %) activaría el límite.
    closes = [100.0] * 24 + [97.0] * 24 + [94.0] * 24 + [94.0] * 4
    df = make_bars(closes, spread=0.01, freq="1h")
    df.index = df.index.as_unit(unit)
    sig = manual_signals(df.index, {1: 1}, stop=10)
    cfg = zero_cost_config(max_daily_loss=0.05, risk_per_trade=0.1)
    res = run_backtest(df, sig, cfg, "TEST", "1h", spec=SPEC)
    assert res.trades["qty"].iloc[0] == pytest.approx(100.0)
    assert res.final_equity == pytest.approx(10_000 - 100 * (100 - 94))
    assert not any(e["kind"] == "daily_loss_limit" for e in res.risk_events)
```
<!-- fmt: on -->

**Qué comprueba.** Dos días seguidos con una pérdida del 3 % cada uno. Con el reinicio diario
correcto, ningún día alcanza el 5 %; si el día no se reiniciara, la pérdida acumulada (~6 %)
activaría el límite. La prueba se repite con el índice en nanosegundos, microsegundos,
milisegundos y segundos (`@pytest.mark.parametrize`).

**Historia.** La prueba y el identificador entero de día se añadieron en el mismo commit
(`2f60aca`); en el historial confirmado no hay ninguna versión con el error. Es una prueba
**preventiva**: pandas 3 puede crear índices con resolución distinta de nanosegundos, y una
conversión que supusiera nanosegundos calcularía días erróneos (sección 10.3).

---

## 11.7 Validaciones de configuración

<!-- fmt: off -->
<!-- cita: src/bybit_quant_lab/config/models.py#L63-L76 -->
`src/bybit_quant_lab/config/models.py` · líneas 63–76

```python
class RiskConfig(_Strict):
    """Límites de riesgo del sistema (independientes de las estrategias)."""

    risk_per_trade: float = Field(0.01, gt=0, le=0.1)
    max_drawdown: float = Field(0.15, gt=0, le=1)
    drawdown_action: Literal["block", "close_and_block"] = "block"
    max_daily_loss: float = Field(0.05, gt=0, le=1)
    daily_loss_action: Literal["block", "close_and_block"] = "block"
    max_consecutive_losses: int = Field(3, ge=1)
    pause_bars_after_losses: int = Field(24, ge=1)
    max_open_positions: int = Field(1, ge=1, le=1)
    max_symbol_exposure: float = Field(3.0, gt=0, description="Nocional máximo / equity")
    max_leverage: float = Field(5.0, ge=1)
    margin_reserve: float = Field(0.2, ge=0, lt=1, description="Fracción de equity no usable")
```
<!-- fmt: on -->

- Los `Field(..., gt=0, le=0.1)` impiden, por ejemplo, un riesgo por operación del 50 %.
- `max_open_positions` solo admite 1 (`ge=1, le=1`): el motor no gestiona carteras.
- La validación cruzada de `AppConfig` (líneas 121–128) exige
  `execution.leverage ≤ risk.max_leverage` (`test_leverage_must_not_exceed_limit`).

**[Limitación]** Recuerda la sección 2.15: `model_copy(update=...)` no revalida. Las pruebas lo
usan para construir configuraciones extremas; desde YAML y la CLI siempre se valida.

---

## 11.8 Resumen

| Elemento | Valor por defecto | Etiqueta |
|---|---|---|
| Riesgo por operación | 1 % de la equity, incluidos costes estimados | [Diseño] |
| Tope efectivo de nocional | 2,4 × equity (margen con reserva del 20 %) | [Hecho] |
| Pérdida diaria | 5 % sobre equity de inicio del día UTC, mark-to-market | [Diseño] |
| Drawdown máximo | 15 %, kill-switch sin reactivación | [Diseño] |
| Racha de pérdidas | 3 → pausa de 24 velas | [Diseño] |
| Liquidación | Margen de mantenimiento fijo 0,5 % | [Limitación] |
| Especificaciones | Referencias no verificadas | [Pendiente] de contrastar con la API |
| Límites evaluados al cierre | Sin control intravela | [Limitación] |

### Comprobación final del módulo

Equity 20 000 USDT, riesgo 1 %, precio 2 000 USDT (ETHUSDT), stop a 10 USDT, comisión 0,055 %,
deslizamiento 2 bps, configuración por defecto. ¿Qué cantidad se abre y qué tope actúa?

<details><summary>Ver respuesta</summary>

Precio de ejecución ≈ 2 000,4. Coste por unidad = 10 + 2 000,4 × 2 × 0,00075 ≈ 13,0006.
`q_bruta = 200 / 13,0006 ≈ 15,38`. Tope de margen = 20 000 × 0,8 × 3 / 2 000,4 ≈ 23,99: no
actúa. Redondeo al paso 0,01 de ETHUSDT → **15,38 ETH**, sin tope (nocional ≈ 30 766, es decir,
1,54 × equity).
</details>
