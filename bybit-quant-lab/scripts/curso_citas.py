"""Herramienta del curso (docs/curso): citas de código verificables y ejemplos ejecutables.

No forma parte del paquete ni del código de producción. Convenciones en los .md del curso:

1. Cita de código real (rutas relativas a ``bybit-quant-lab/``)::

       <!-- cita: src/bybit_quant_lab/backtesting/engine.py#L183-L184 -->
       `src/bybit_quant_lab/backtesting/engine.py` · líneas 183–184   (rótulo visible, generado)

       ```python
       ...contenido...
       ```

   ``--fill`` sustituye el contenido del bloque por las líneas exactas del archivo.
   ``--check`` falla si algún bloque ya no coincide con el código (el curso quedó desfasado).

2. Ejemplo ejecutable con salida real::

       <!-- ejecutar -->
       ```python
       print(1 + 1)
       ```
       <!-- salida -->
       ```text
       2
       ```

   ``--fill`` ejecuta el ejemplo con el intérprete actual (cwd = bybit-quant-lab/) y escribe su
   salida real en el bloque ``salida``. ``--check`` vuelve a ejecutarlo y compara.

Uso::

    python scripts/curso_citas.py --fill    # rellena citas y salidas
    python scripts/curso_citas.py --check   # verifica (código de salida 1 si hay desajustes)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "docs" / "curso"

CITA = re.compile(
    r"(?P<head><!-- cita: (?P<path>[^#\s]+)#L(?P<a>\d+)-L(?P<b>\d+) -->\n)"
    r"(?P<caption>`[^`\n]+` · líneas [^\n]*\n\n)?"
    r"(?P<fence>```(?P<lang>\w*)\n)"
    r"(?P<body>.*?)(\n?```)",
    re.S,
)
EJEC = re.compile(
    r"(<!-- ejecutar -->\n```python\n)(?P<code>.*?)(\n```\n)"
    r"(?:(<!-- salida -->\n```text\n)(?P<out>.*?)(\n?```))?",
    re.S,
)


def _lines(path: str, a: int, b: int) -> str:
    file = ROOT / path
    if not file.exists():
        raise SystemExit(f"Archivo citado inexistente: {path}")
    lines = file.read_text(encoding="utf-8").splitlines()
    if not 1 <= a <= b <= len(lines):
        raise SystemExit(f"Rango fuera del archivo: {path}#L{a}-L{b} (tiene {len(lines)} líneas)")
    return "\n".join(lines[a - 1 : b])


def _run(code: str) -> str:
    proc = subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if proc.returncode != 0:
        raise SystemExit(f"El ejemplo falla:\n{code}\n--- stderr ---\n{proc.stderr}")
    return proc.stdout.rstrip("\n")


def process(md: Path, fill: bool) -> list[str]:
    text = md.read_text(encoding="utf-8")
    problems: list[str] = []

    def cita(m: re.Match[str]) -> str:
        real = _lines(m["path"], int(m["a"]), int(m["b"]))
        caption = f"`{m['path']}` · líneas {m['a']}–{m['b']}\n\n"
        if m["body"] != real or m["caption"] != caption:
            problems.append(f"{md.name}: cita desfasada {m['path']}#L{m['a']}-L{m['b']}")
        return m["head"] + caption + m["fence"] + real + "\n```"

    def ejec(m: re.Match[str]) -> str:
        out = _run(m["code"])
        if m["out"] is None:
            problems.append(f"{md.name}: ejemplo sin bloque de salida")
            new = m.group(1) + m["code"] + m.group(3) + "<!-- salida -->\n```text\n" + out + "\n```"
            return new
        if m["out"] != out:
            problems.append(
                f"{md.name}: salida distinta en ejemplo que empieza por "
                f"{m['code'].splitlines()[0][:60]!r}"
            )
        return m.group(1) + m["code"] + m.group(3) + m.group(4) + out + "\n```"

    new = CITA.sub(cita, text)
    new = EJEC.sub(ejec, new)
    if fill and new != text:
        md.write_text(new, encoding="utf-8")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--fill", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("files", nargs="*", help="Archivos .md (por defecto, todo el curso)")
    args = parser.parse_args()
    files = [Path(f) for f in args.files] or sorted(COURSE.glob("*.md"))
    total = 0
    problems: list[str] = []
    for md in files:
        text = md.read_text(encoding="utf-8")
        total += len(CITA.findall(text)) + len(EJEC.findall(text))
        problems += process(md, fill=args.fill)
    if args.fill:
        print(
            f"Rellenados {total} bloques en {len(files)} archivos ({len(problems)} actualizados)."
        )
        return 0
    for p in problems:
        print(p)
    print(f"{total} bloques verificados en {len(files)} archivos; {len(problems)} desajustes.")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
