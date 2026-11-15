#!/usr/bin/env bash
# Compila el libro y su solucionario. Uso: bash compilar.sh   (requiere herramientas/instalar_composicion.sh)
set -euo pipefail
cd "$(dirname "$0")"
. "$HOME/atlas-herramientas/activar.sh"
python3 verificacion/cap08.py
quarto render --to pdf
mkdir -p ../../pdf/libros
cp _salida/*.pdf ../../pdf/libros/L01-libro-piloto.pdf
cp index.aux libro.aux
rm -f _salida/*.pdf
quarto render --to pdf --profile solucionario
cp _salida/*.pdf ../../pdf/libros/L01-solucionario-piloto.pdf
rm -f _salida/*.pdf
