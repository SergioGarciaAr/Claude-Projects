# Guía de uso

Flujo recomendado de investigación, de principio a fin. Todas las órdenes se ejecutan desde
`bybit-quant-lab/`, con el entorno virtual activado.

## 1. Preparar los datos

```bash
bql download --symbol BTCUSDT --timeframe 1h 4h --start 2022-01-01 --end 2024-12-31 --funding
bql validate-data --symbol BTCUSDT --timeframe 1h
```

Revisa el informe de calidad: los huecos se reportan, pero no se rellenan. Si no tienes acceso
a la API, importa un CSV (`bql import`) o, solo para probar el sistema, genera datos
sintéticos (`bql synth`).

## 2. Revisar la configuración

- Costes: confirma la tarifa de tu cuenta (`costs.taker_fee`) y un slippage realista para la
  temporalidad elegida.
- Riesgo: ajusta `risk.*` a la hipótesis que investigas.
- Segmentos: `validation.train_frac` y `validation.validation_frac`. Para un test con
  suficientes operaciones, usa varios años de datos.

## 3. Explorar en entrenamiento

```bash
bql backtest --symbol BTCUSDT --timeframe 1h --strategy ema_crossover --segment train
bql sensitivity --symbol BTCUSDT --timeframe 1h --strategy ema_crossover --segment train
```

Busca zonas estables de parámetros, no el máximo aislado. El resumen `stability.json` indica
la fracción de configuraciones positivas y la distancia entre la mejor y la mediana.

## 4. Comparar en validación

```bash
bql compare --symbol BTCUSDT --timeframe 1h
```

En el informe, compara:

- **bruto frente a neto:** cuánto se lo llevan los costes;
- **frente a los benchmarks:** buy-and-hold, efectivo y entradas aleatorias con igual
  exposición;
- **DSR:** un Sharpe alto en validación con un DSR bajo sugiere una selección por azar;
- **dependencia de las mejores operaciones:** si el signo cambia al quitar 3 operaciones, el
  resultado no es robusto;
- **correlación de señales:** las combinaciones con miembros muy correlacionados cuentan la
  misma información varias veces.

## 5. Walk-forward

```bash
bql walkforward --symbol BTCUSDT --timeframe 1h --strategy donchian_breakout
```

Comprueba si la configuración elegida en cada ventana mantiene un rendimiento fuera de
muestra y si los parámetros elegidos cambian mucho entre ventanas.

## 6. Test final (una vez)

Cuando la selección esté decidida **sin mirar el test**:

```bash
bql final-test --selection outputs/compare_BTCUSDT_1h_<fecha>/selection.json
```

No ajustes nada a partir de este resultado y vuelvas a evaluar el mismo período: la
herramienta lo impide salvo con `--allow-repeat`, y entonces lo marca como no independiente.

## 7. Repetir en otros mercados

```bash
bql compare --symbol ETHUSDT --timeframe 4h
```

Un resultado que solo aparece en un símbolo y una temporalidad es una señal de alarma.

## Lectura de los informes

| Sección | Qué mirar |
|---|---|
| Limitaciones y advertencias | Datos sintéticos, funding ausente, muestras pequeñas, especificaciones no verificadas |
| Métricas | Neto frente a bruto, drawdown, número de operaciones y profit factor junto con la expectativa |
| Curva de equity | Comparación con buy-and-hold y efectivo |
| Desgloses | Si el resultado depende de una sola dirección o de un régimen |
| Eventos de riesgo | Si los límites del sistema intervienen a menudo |
| Metadatos | Commit, hash de datos, configuración y semilla, para reproducir el resultado |
