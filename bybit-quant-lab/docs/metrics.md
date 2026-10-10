# Métricas

Implementación: `analytics/metrics.py` (`compute_metrics`). Todas las cifras monetarias
están en la moneda cotizada (USDT).

## Convenciones

- **Retornos por vela:** `r_t = E_t / E_{t-1} - 1` sobre la equity mark-to-market al cierre.
  Para el primer retorno, `E_{-1}` es el capital inicial.
- **Períodos sin operaciones:** se incluyen con retorno 0. El Sharpe y el Sortino miden, por
  tanto, la estrategia completa, incluido el tiempo en efectivo.
- **Anualización:** el mercado cripto opera 24/7 y se toma un año de 365 días, así que
  `N = 525 600 / minutos_por_vela` (5m: 105 120; 15m: 35 040; 1h: 8 760; 4h: 2 190).
- **Tasa libre de riesgo:** 0.

## Definiciones

| Métrica | Fórmula / definición |
|---|---|
| `net_profit` | `E_final - capital_inicial` (incluye comisiones, slippage y funding aplicado) |
| `net_profit_pct`, `cumulative_return` | `E_final / capital_inicial - 1` |
| `gross_profit_before_costs` | `Σ gross_pnl` de las operaciones (precios sin slippage, sin comisiones ni funding) |
| `cagr` | `(E_final/E_0)^(365/días) - 1`, **solo** si `días ≥ min_days_for_cagr` (180); si no, `null` con advertencia |
| `sharpe` | `media(r) / desv(r, ddof=1) · sqrt(N)`; `null` si hay menos de 30 velas, si la desviación es 0 o si hay menos de 10 operaciones con una exposición inferior al 90 % (pocos episodios dominan la serie) |
| `sortino` | `media(r) / sqrt(media(min(r,0)²)) · sqrt(N)`, con las mismas condiciones de validez que el Sharpe |
| `max_drawdown` | `max(1 - E_t / max_{s≤t} E_s)` |
| `max_dd_duration_bars` | Racha más larga de velas por debajo del máximo previo |
| `max_dd_recovery_bars` | Velas desde el valle del máximo drawdown hasta recuperar el máximo previo (`null` si no se recupera) |
| `max_dd_start/trough/end` | Fechas del pico, el valle y la recuperación |
| `num_trades` | Operaciones cerradas |
| `win_rate` | Fracción de operaciones con PnL neto > 0 |
| `avg_win` / `avg_loss` | Media del PnL neto de las ganadoras y de las perdedoras |
| `profit_factor` | `Σ ganancias netas / |Σ pérdidas netas|`; `null` si no hay pérdidas |
| `expectancy` | Media del PnL neto por operación |
| `expectancy_pct_equity` | Media del PnL neto / equity al entrar |
| `exposure` | Fracción de velas con posición abierta al cierre |
| `turnover` | Nocional negociado (entradas + salidas) / equity media |
| `total_fees`, `total_slippage`, `total_costs` | Comisiones, slippage y su suma |
| `total_funding` | Funding neto pagado (positivo = coste) |
| `avg_bars_in_trade` | Velas medias por operación (incluye las de entrada y salida) |
| `long_trades`, `short_trades` | Operaciones por dirección |
| `rejected_signals`, `risk_events` | Señales rechazadas y eventos de riesgo |

Desgloses (`analytics/breakdowns.py`): por dirección (`side`), motivo de salida
(`exit_reason`) y régimen al entrar (`regime`: tendencia/lateral × volatilidad). Para
comparar por símbolo y temporalidad: `bql markets` (matriz de métricas por mercado y
resumen de consistencia, en `validation/research.py`: `market_matrix` y
`consistency_summary`).

## Validez y muestras pequeñas

- Con menos de `min_trades_for_stats` (30) operaciones, el informe advierte de que las
  métricas por operación tienen alta incertidumbre.
- El Sharpe por vela de series con muchas velas sin posición puede estar sesgado por la
  autocorrelación de los retornos de posiciones mantenidas varias velas. No se corrige.
- Un CAGR de períodos cortos extrapola de forma engañosa y por eso no se calcula.
- Las métricas de benchmarks sin operaciones (efectivo) devuelven `null` donde no están
  definidas.
- Ver `docs/methodology.md` (sección 6) para el DSR, Holm y el bootstrap.
