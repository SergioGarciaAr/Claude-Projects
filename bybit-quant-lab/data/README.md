# Datos

- `raw/`: reservado para datos sin procesar.
- `processed/`: datasets limpios en Parquet (`<SÍMBOLO>_<tf>.parquet`) con metadatos de
  procedencia (`.meta.json`) y funding (`<SÍMBOLO>_funding.parquet`).

El contenido de ambos directorios está excluido de Git (`.gitignore`). Para obtener datos:

```bash
bql download --symbol BTCUSDT --timeframe 1h --start 2024-01-01 --end 2024-06-30 --funding
bql import --symbol BTCUSDT --timeframe 1h --file mis_velas.csv
bql synth --symbol BTCUSDT --timeframe 1h --bars 6000   # solo para pruebas de lógica
```

Detalles en [`../docs/data_sources.md`](../docs/data_sources.md).
