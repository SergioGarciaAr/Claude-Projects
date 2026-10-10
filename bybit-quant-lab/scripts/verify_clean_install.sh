#!/usr/bin/env bash
# Verifica la instalación desde un entorno virtual limpio y ejecuta las comprobaciones de
# calidad y un flujo mínimo con datos sintéticos. Uso: bash scripts/verify_clean_install.sh
set -euo pipefail
cd "$(dirname "$0")/.."
TMP="$(mktemp -d)"
python3 -m venv "$TMP/venv"
# shellcheck disable=SC1091
source "$TMP/venv/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest -q
bql --data-dir "$TMP/data" --output-dir "$TMP/out" synth --symbol BTCUSDT --timeframe 1h --bars 3000
bql --data-dir "$TMP/data" --output-dir "$TMP/out" backtest --symbol BTCUSDT --timeframe 1h \
    --strategy ema_crossover --segment validation
echo "OK: instalación limpia verificada en $TMP"
