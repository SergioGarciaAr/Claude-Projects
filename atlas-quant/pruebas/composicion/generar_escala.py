"""Genera una copia de la muestra de unas 400 páginas para medir tiempos (prueba R-15).

Uso: python3 generar_escala.py N   (N copias de cada capítulo; con N = 40 se obtienen ~80 capítulos)
Escribe escala/*.qmd y _quarto-escala.yml. Las etiquetas se renombran con un sufijo por copia.
"""
import re
import sys
from pathlib import Path

n = int(sys.argv[1])
destino = Path("escala")
destino.mkdir(exist_ok=True)
capitulos = []
for k in range(1, n + 1):
    for base in ("cap-a", "cap-b"):
        texto = Path(f"{base}.qmd").read_text(encoding="utf-8")
        # Sufijo en todas las etiquetas definidas y referidas (sec-, def-, thm-, cor-, exm-, exr-, eq-, tbl-, fig-)
        texto = re.sub(r"(#|@|-@)((?:sec|def|thm|cor|exm|exr|eq|tbl|fig)-[\w-]+)", rf"\1\2-c{k}", texto)
        texto = re.sub(r"(#\| label: )((?:tbl|fig)-[\w-]+)", rf"\1\2-c{k}", texto)
        texto = re.sub(r"(#\| label: )(duplicacion|simulacion-mbg)", rf"\1\2-c{k}", texto)
        nombre = f"escala/{base}-{k:02d}.qmd"
        Path(nombre).write_text(texto, encoding="utf-8")
        capitulos.append(nombre)
lista = "\n".join(f"    - {c}" for c in ["index.qmd", *capitulos, "referencias.qmd"])
Path("_quarto-escala.yml").write_text(f"book:\n  chapters:\n{lista}\n", encoding="utf-8")
print(f"{len(capitulos)} capítulos generados")
