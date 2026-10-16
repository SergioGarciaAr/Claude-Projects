#!/usr/bin/env bash
# Instala las herramientas de composición de Atlas Quant en ~/atlas-herramientas (fuera del repositorio).
# Reproduce la instalación de la prueba de la Fase 2; las versiones exactas están en
# herramientas/versiones_composicion.txt. Uso (desde atlas-quant/): bash herramientas/instalar_composicion.sh
#
# Orígenes (accesibles con la política de red actual del entorno):
#   - conda-forge: Quarto 1.9.38 y sus dependencias (pandoc, typst, deno, dart-sass, esbuild),
#     extraídas sin gestor de conda por herramientas/conda_extraer.py, con verificación SHA-256.
#   - Ubuntu 24.04: TeX Live 2023 (LuaLaTeX, español, paquetes científicos, fuentes, biber).
#   - PyPI: pila de Python para ejecutar el código del libro.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/atlas-herramientas"
VERS="$RAIZ/herramientas/versiones_composicion.txt"
mkdir -p "$DEST/cache"

# 1. Entorno virtual de Python con las versiones registradas
python3 -m venv "$DEST/venv"
grep -E '^[A-Za-z0-9_.-]+==' "$VERS" > "$DEST/requisitos.txt"
"$DEST/venv/bin/pip" install -q -r "$DEST/requisitos.txt"

# 2. Quarto y dependencias desde conda-forge
for sub in linux-64 noarch; do
  archivo="$DEST/cache/$( [ "$sub" = noarch ] && echo noarch_ )current_repodata.json"
  [ -s "$archivo" ] || curl -sS -m 600 -o "$archivo" "https://conda.anaconda.org/conda-forge/$sub/current_repodata.json"
done
"$DEST/venv/bin/python" "$RAIZ/herramientas/conda_extraer.py" "$DEST/conda" "$DEST/cache" "quarto==1.9.38"

# 3. TeX Live y fuentes desde Ubuntu
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
  texlive-luatex texlive-latex-extra texlive-lang-spanish texlive-science texlive-bibtex-extra \
  biber texlive-fonts-extra fonts-stix texlive-latex-recommended texlive-fonts-recommended

# 4. Guion de activación y núcleo de Jupyter
cat > "$DEST/activar.sh" <<'EOF'
# Activa las herramientas de composición de Atlas Quant (generado por instalar_composicion.sh).
export CONDA_PREFIX="$HOME/atlas-herramientas/conda"
for f in "$CONDA_PREFIX"/etc/conda/activate.d/*.sh; do . "$f"; done
export QUARTO_DENO_DOM="$CONDA_PREFIX/lib/deno_dom.so"
export PATH="$CONDA_PREFIX/bin:$HOME/atlas-herramientas/venv/bin:$PATH"
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export QUARTO_PYTHON="$HOME/atlas-herramientas/venv/bin/python"
export TYPST_FONT_PATHS=/usr/share/texlive/texmf-dist/fonts/opentype/public/libertinus-fonts
EOF
"$DEST/venv/bin/python" -m ipykernel install --user --name atlas --display-name "Atlas Quant" > /dev/null
. "$DEST/activar.sh"
echo "Quarto $(quarto --version); $(pandoc --version | head -1); $(lualatex --version | head -1)"
