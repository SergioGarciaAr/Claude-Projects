"""Une el curso (docs/curso/*.md) en un único Markdown pensado para convertir a PDF.

Uso (desde bybit-quant-lab/):

    python scripts/curso_unificar.py                 # escribe docs/curso_completo.md
    python scripts/curso_unificar.py --out otro.md

Transformaciones (solo fuera de los bloques de código):

* Orden: README (portada e índice), módulos I-XVII y glosario.
* Los enlaces entre archivos del curso pasan a texto (en un solo documento no hay archivos).
* Se eliminan los comentarios HTML de control (citas, marcas de ejecución) y se sustituyen
  las marcas de ejemplo ejecutable y de salida por rótulos visibles. Se conservan
  ``fmt: off/on``, invisibles al renderizar, para que ``ruff format`` no altere las citas.
* Los bloques plegables <details> se convierten en "Respuesta:" / "Solución:" visibles,
  porque un PDF no puede desplegarlos.
* Salto de página antes de cada módulo (<div style="page-break-before: always">).
"""

from __future__ import annotations

import argparse
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURSO = ROOT / "docs" / "curso"
SALTO = '<div style="page-break-before: always;"></div>'

ENLACE = re.compile(r"\[([^\]]+)\]\((?:modulo-\d\d-[\w-]+|glosario|README)\.md(?:#[^)]*)?\)")
SUMMARY = re.compile(r"^<details><summary>(.*?)</summary>\s*$")


def archivos() -> list[Path]:
    modulos = sorted(CURSO.glob("modulo-*.md"))
    return [CURSO / "README.md", *modulos, CURSO / "glosario.md"]


def transformar(texto: str) -> str:
    salida: list[str] = []
    en_codigo = False
    for linea in texto.splitlines():
        if linea.startswith("```"):
            en_codigo = not en_codigo
            salida.append(linea)
            continue
        if en_codigo:
            salida.append(linea)
            continue
        s = linea.strip()
        if s == "<!-- ejecutar -->":
            salida.append("*Ejemplo ejecutable:*")
            salida.append("")
            continue
        if s == "<!-- salida -->":
            salida.append("*Salida real:*")
            salida.append("")
            continue
        if s in ("<!-- fmt: off -->", "<!-- fmt: on -->"):
            salida.append(linea)  # invisibles; impiden que ruff format altere las citas
            continue
        if re.fullmatch(r"<!--.*-->", s):  # marcadores de cita y otros comentarios de control
            continue
        m = SUMMARY.match(s)
        if m:
            rotulo = "Respuesta" if "respuesta" in m.group(1).lower() else m.group(1)
            salida.append(f"**{rotulo}:**")
            continue
        if s == "</details>":
            continue
        salida.append(ENLACE.sub(r"\1", linea))
    return "\n".join(salida).rstrip() + "\n"


def commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "desconocido"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "docs" / "curso_completo.md"))
    args = ap.parse_args()
    partes = []
    for i, f in enumerate(archivos()):
        cuerpo = transformar(f.read_text(encoding="utf-8"))
        partes.append(cuerpo if i == 0 else f"{SALTO}\n\n{cuerpo}")
    cabecera = (
        f"> Documento generado con `scripts/curso_unificar.py` a partir de `docs/curso/` "
        f"(commit `{commit()}`, {datetime.now(UTC):%Y-%m-%d}). Para corregirlo, edita los "
        f"archivos de `docs/curso/` y vuelve a generarlo. Los comentarios de control de las "
        f"citas se han eliminado: cada cita conserva la línea con su archivo y sus números "
        f"de línea, y las respuestas de las comprobaciones aparecen desplegadas.\n\n"
    )
    texto = partes[0].replace("\n\n", "\n\n" + cabecera, 1) + "\n" + "\n".join(partes[1:])
    Path(args.out).write_text(texto, encoding="utf-8")
    print(f"{args.out}: {len(texto.splitlines())} líneas, {len(archivos())} archivos unidos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
