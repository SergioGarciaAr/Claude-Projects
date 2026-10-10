# Gestión de riesgo

El módulo `risk/` es independiente de las estrategias. Los valores por defecto son **límites
de referencia para investigación**: no son garantías de seguridad ni recomendaciones para
operar con dinero real.

## Tres mecanismos distintos

| Mecanismo | Dónde | Qué hace |
|---|---|---|
| **Stop de estrategia** | `stop_distance` de cada estrategia (ATR) | Cierra una operación concreta. Motivos `stop_loss` o `stop_loss_gap`. |
| **Límites del sistema** | `risk/limits.py` (`RiskManager`) | Bloquean nuevas entradas o fuerzan cierres. Motivo `risk_limit_close`; se registran como eventos de riesgo. |
| **Liquidación del exchange** | `backtesting/engine.py` (aproximación) | Pérdida del margen aislado. Motivos `liquidation` o `liquidation_gap`. |

## Parámetros (`configs/default.yaml`, sección `risk`)

| Parámetro | Defecto | Definición |
|---|---|---|
| `risk_per_trade` | 0,01 | Fracción de la equity que se arriesga hasta el stop, incluidos los costes estimados |
| `max_drawdown` | 0,15 | Drawdown sobre el máximo de equity que detiene las nuevas entradas |
| `drawdown_action` | block | `block` o `close_and_block` |
| `max_daily_loss` | 0,05 | Pérdida diaria máxima (definición abajo) |
| `daily_loss_action` | block | `block` o `close_and_block` |
| `max_consecutive_losses` | 3 | Pérdidas seguidas que activan la pausa |
| `pause_bars_after_losses` | 24 | Duración de la pausa, en velas |
| `max_open_positions` | 1 | Única configuración soportada |
| `max_symbol_exposure` | 3,0 | Nocional máximo / equity |
| `max_leverage` | 5,0 | Límite superior; `execution.leverage` no puede superarlo (se valida al cargar) |
| `margin_reserve` | 0,2 | Fracción de la equity que nunca se usa como margen |

## Dimensionamiento (`risk/sizing.py`)

```
riesgo_por_unidad = stop_distance + precio · 2 · (taker_fee + slippage)
cantidad          = equity · risk_per_trade / riesgo_por_unidad
```

Límites, aplicados en orden (se registra cuál actúa):

1. Exposición por símbolo: `cantidad ≤ equity · max_symbol_exposure / precio`.
2. Apalancamiento máximo: `cantidad ≤ equity · max_leverage / precio`.
3. Margen disponible: `cantidad ≤ (equity · (1 - margin_reserve) - margen_usado) · apalancamiento / precio`.
4. Cantidad máxima del instrumento.

Después se **redondea hacia abajo** al `qty_step`. La entrada se rechaza si la cantidad queda
por debajo de `min_qty`, si el nocional no llega a `min_notional` o si el stop está más allá de
la liquidación aproximada.

El apalancamiento **no** cambia el PnL de una cantidad dada: solo modifica el margen
bloqueado y el precio de liquidación (está verificado por una prueba). El riesgo lo fija la
distancia al stop, no el apalancamiento.

## Pérdida diaria (definición inequívoca)

- **Día:** el día natural UTC (00:00–24:00).
- **Referencia:** la equity al cierre de la última vela del día UTC anterior. El primer día se
  usa el capital inicial.
- **Medida:** al **cierre de cada vela**, `pnl_día = equity_mark_to_market - referencia`.
  Incluye el PnL **realizado** (con comisiones y funding) y el **no realizado**, valorado al
  cierre.
- **Activación:** `pnl_día ≤ -max_daily_loss · referencia`.
- **Política:**
  - `block`: no se abren posiciones hasta el siguiente día UTC; la posición abierta sigue
    gestionada por sus stops.
  - `close_and_block`: además, se cierra en la siguiente apertura.
- **Limitación:** los mínimos intravela no realizados no se consideran; solo se miden los
  cierres.

## Pérdidas consecutivas

- Una operación con PnL neto `< 0` incrementa la racha, una con PnL neto `> 0` la reinicia y
  una con exactamente 0 no la cambia.
- Al llegar a `max_consecutive_losses`, las entradas se pausan `pause_bars_after_losses`
  velas y la racha vuelve a 0.
- La pausa **no** anula los demás límites. Al terminar, siguen vigentes el bloqueo diario, el
  kill-switch de drawdown y el resto de controles.

## Drawdown máximo

`drawdown = 1 - equity / máximo_histórico`, medido al cierre. Al alcanzar `max_drawdown`, las
nuevas entradas quedan bloqueadas **durante el resto de la simulación** (kill-switch). Con
`close_and_block`, además, se cierra la posición en la siguiente apertura.

## Especificaciones de instrumentos

`risk/instruments.py` contiene valores de referencia (marcados `verified=False`):

| Símbolo | tick | qty_step | min_qty | max_qty | min_notional |
|---|---|---|---|---|---|
| BTCUSDT | 0,1 | 0,001 | 0,001 | 100 | 5 |
| ETHUSDT | 0,01 | 0,01 | 0,01 | 1000 | 5 |

Estos valores **deben contrastarse** con `GET /v5/market/instruments-info`
(`BybitPublicClient.fetch_instrument_info` + `spec_from_bybit`), porque Bybit puede
modificarlos. Mientras se usen los valores de referencia, los informes muestran una advertencia.

## Pruebas

`tests/unit/test_risk.py` y `tests/unit/test_engine.py` cubren:

- dimensionamiento por distancia al stop y costes;
- límites de exposición y redondeo;
- rechazo por tamaño mínimo;
- pausa tras tres pérdidas, tanto en el gestor como en el motor;
- la pausa no anula otros límites;
- bloqueo diario y reinicio en el siguiente día UTC;
- `close_and_block`;
- validación del apalancamiento;
- apalancamiento neutral para el PnL;
- liquidación y stop más allá de la liquidación;
- reinicio diario independiente de la resolución temporal del índice (prueba de regresión).
