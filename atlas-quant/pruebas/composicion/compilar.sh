#!/usr/bin/env bash
# Compila la muestra con las dos cadenas de Quarto (Typst y LuaLaTeX), libro y solucionario,
# y registra los tiempos en resultados/tiempos.txt. Uso: bash compilar.sh
set -euo pipefail
cd "$(dirname "$0")"
. "$HOME/atlas-herramientas/activar.sh"
export QUARTO_PYTHON="$HOME/atlas-herramientas/venv/bin/python"
export TYPST_FONT_PATHS=/usr/share/texlive/texmf-dist/fonts/opentype/public/libertinus-fonts
mkdir -p resultados
echo "--- $(date "+%F %T")" >> resultados/tiempos.txt
medir() {  # medir etiqueta comando...
  local inicio fin
  inicio=$(date +%s.%N)
  "${@:2}" > "resultados/$1.log" 2>&1
  fin=$(date +%s.%N)
  printf "%s\t%.1f s\n" "$1" "$(echo "$fin - $inicio" | bc)" | tee -a resultados/tiempos.txt
}
medir C2-libro quarto render --to pdf
cp _salida/*.pdf resultados/C2-quarto-lualatex-libro.pdf
cp index.aux libro.aux
rm -f _salida/*.pdf
medir C2-solucionario quarto render --to pdf --profile solucionario
cp _salida/*.pdf resultados/C2-quarto-lualatex-solucionario.pdf
rm -f _salida/*.pdf
medir C1-libro quarto render --to typst
cp _salida/*.pdf resultados/C1-quarto-typst-libro.pdf
rm -f _salida/*.pdf
# El solucionario en Typst no puede resolver referencias al libro (no hay equivalente de xr):
# se registra el resultado sin detener el guion.
if medir C1-solucionario quarto render --to typst --profile solucionario; then
  cp _salida/*.pdf resultados/C1-quarto-typst-solucionario.pdf
else
  echo "C1-solucionario: sin PDF (referencias al libro sin resolver en Typst)" | tee -a resultados/tiempos.txt
fi
rm -f _salida/*.pdf
