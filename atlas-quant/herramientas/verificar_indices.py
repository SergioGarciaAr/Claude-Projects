"""Verifica la coherencia de los índices detallados de Atlas Quant y genera el mapa de dependencias.

Uso (desde atlas-quant/):  python3 herramientas/verificar_indices.py
Sale con código 1 si encuentra errores; las advertencias no detienen la ejecución.
Escribe editorial/dependencias.md a partir de los índices (no debe editarse a mano).

Comprobaciones:
  1. Toda referencia (L<n> §c.s, L<n> c. c, L<n> ap. X) apunta a un elemento existente.
  2. Los prerrequisitos de un capítulo son anteriores a él: otro libro de número menor,
     o un capítulo anterior del mismo libro (o un apéndice del mismo libro).
  3. Todo libro citado como prerrequisito está en la clausura transitiva de los requisitos
     declarados en PLAN_EDITORIAL.md, sección 6; los usos como aplicación pueden citar además
     los libros de la columna «Aplicación».
  4. Los capítulos y secciones están numerados de forma consecutiva y el número de capítulos
     coincide con el declarado en PLAN_EDITORIAL.md, sección 5.
  5. Los identificadores RA-xx citados existen en editorial/resultados_admitidos.md.
  6. La extensión declarada en la ficha de cada libro es la suma de las extensiones de sus
     capítulos más los preliminares (PRELIMINARES páginas) y los apéndices (PAGINAS_APENDICE
     por apéndice). Se advierte si la suma de los capítulos cae fuera del intervalo de
     PLAN_EDITORIAL.md, sección 8, que cuenta solo capítulos.
Advertencias: prerrequisitos sobre secciones opcionales (*) y requisitos declarados que ningún
capítulo usa.
"""

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REF = re.compile(r"L(\d+) (?:§(\d+)\.(\d+)|c\. (\d+)|ap\. ([A-Z]))")
RA = re.compile(r"RA-(\d+)")
EXTENSION = re.compile(r"\*\*Extensión estimada:\*\* ([\d\u202f ]+)–([\d\u202f ]+) páginas")
PRELIMINARES = 20              # páginas por libro (PLAN_EDITORIAL.md, sección 8)
PAGINAS_APENDICE = (10, 20)    # intervalo por apéndice


def numero(texto):
    return int(re.sub(r"\D", "", texto))


def leer_plan():
    texto = (RAIZ / "PLAN_EDITORIAL.md").read_text(encoding="utf-8")
    capitulos = {int(n): int(c) for n, c in re.findall(r"^#### L(\d+)\. .*\((?:especialización; )?(\d+) capítulos\)", texto, re.M)}
    requisitos, aplicacion = {}, {}
    seccion6 = texto.split("## 6. Prerrequisitos justificados")[1].split("**Ruta crítica")[0]
    for fila in re.findall(r"^\| L(\d+) \|(.*)$", seccion6, re.M):
        libro, resto = int(fila[0]), fila[1].split("|")
        requisitos[libro] = {int(x) for x in re.findall(r"L(\d+)", resto[0])}
        aplicacion[libro] = {int(x) for x in re.findall(r"L(\d+)", resto[2])}
    paginas = {int(n): (numero(a), numero(b)) for n, a, b in re.findall(r"L(\d+) \| \d+ \| ([\d\u202f ]+)–([\d\u202f ]+) \|", texto)}
    return capitulos, requisitos, aplicacion, paginas


def clausura(libro, requisitos, vistos=None):
    vistos = set() if vistos is None else vistos
    for r in requisitos.get(libro, ()):
        if r not in vistos:
            vistos.add(r)
            clausura(r, requisitos, vistos)
    return vistos


def leer_indice(ruta):
    """Devuelve (libro, capítulos) donde capítulos = {n: {titulo, secciones, opcionales, campos}}."""
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    libro = int(re.match(r"# L(\d+)\.", lineas[0]).group(1))
    capitulos, apendices, actual, extension = {}, set(), None, None
    for linea in lineas:
        m = EXTENSION.match(linea[2:]) if linea.startswith("- **Extensión") else None
        if m:
            extension = (numero(m.group(1)), numero(m.group(2)))
            continue
        m = re.match(r"### Capítulo (\d+)\. (.+)", linea)
        if m:
            actual = int(m.group(1))
            capitulos[actual] = {"titulo": m.group(2), "secciones": [], "opcionales": set(), "campos": {}}
            continue
        if linea.startswith("## ") and not linea.startswith("## Capítulos"):
            actual = None
        m = re.match(r"- \*\*([A-Z])\*\* ", linea)
        if m:
            apendices.add(m.group(1))
            continue
        if actual is None:
            continue
        m = re.match(r"- \*\*(\d+)\.(\d+)(\\\*)?\*\* ", linea)
        if m:
            capitulos[actual]["secciones"].append((int(m.group(1)), int(m.group(2))))
            if m.group(3):
                capitulos[actual]["opcionales"].add(int(m.group(2)))
            continue
        m = re.match(r"\*\*(Prerrequisitos|Usa como aplicación|Resultados admitidos):\*\* (.*)", linea)
        if m:
            capitulos[actual]["campos"][m.group(1)] = m.group(2)
            continue
        m = EXTENSION.match(linea)
        if m:
            capitulos[actual]["paginas"] = (numero(m.group(1)), numero(m.group(2)))
    return libro, capitulos, apendices, extension


def main():
    errores, avisos = [], []
    capitulos_plan, requisitos, aplicacion, paginas_plan = leer_plan()
    ras = {int(x) for x in RA.findall((RAIZ / "editorial" / "resultados_admitidos.md").read_text(encoding="utf-8"))}

    libros = {}
    for ruta in sorted((RAIZ / "libros").glob("L*/indice.md")):
        libro, caps, apend, extension = leer_indice(ruta)
        libros[libro] = (caps, apend)
        sin_extension = [c for c, d in caps.items() if "paginas" not in d]
        if sin_extension or extension is None:
            errores.append(f"L{libro}: falta la extensión estimada del libro o de los capítulos {sin_extension}")
        else:
            bajo = sum(d["paginas"][0] for d in caps.values()) + PRELIMINARES + PAGINAS_APENDICE[0] * len(apend)
            alto = sum(d["paginas"][1] for d in caps.values()) + PRELIMINARES + PAGINAS_APENDICE[1] * len(apend)
            if extension != (bajo, alto):
                errores.append(f"L{libro}: la ficha declara {extension[0]}–{extension[1]} páginas; la regla da {bajo}–{alto}")
            plan = paginas_plan.get(libro)
            cap_bajo = sum(d["paginas"][0] for d in caps.values())
            cap_alto = sum(d["paginas"][1] for d in caps.values())
            if plan and not (plan[0] <= cap_bajo and cap_alto <= plan[1]):
                avisos.append(f"L{libro}: capítulos {cap_bajo}–{cap_alto} páginas, fuera del intervalo del plan {plan[0]}–{plan[1]}")

    for libro, (caps, apend) in sorted(libros.items()):
        nombre = f"L{libro}"
        if sorted(caps) != list(range(1, len(caps) + 1)):
            errores.append(f"{nombre}: numeración de capítulos no consecutiva")
        if capitulos_plan.get(libro) != len(caps):
            errores.append(f"{nombre}: {len(caps)} capítulos en el índice; el plan declara {capitulos_plan.get(libro)}")
        for c, datos in caps.items():
            numeros = [s for (cc, s) in datos["secciones"]]
            if any(cc != c for (cc, _) in datos["secciones"]) or numeros != list(range(1, len(numeros) + 1)):
                errores.append(f"{nombre} c. {c}: numeración de secciones incorrecta")
            if "Prerrequisitos" not in datos["campos"]:
                errores.append(f"{nombre} c. {c}: falta la línea de prerrequisitos")

    usados = {libro: set() for libro in libros}
    dependencias = {}
    for libro, (caps, _) in sorted(libros.items()):
        permitidos = clausura(libro, requisitos)
        for c, datos in caps.items():
            lugar = f"L{libro} c. {c}"
            deps = set()
            for campo, extra in (("Prerrequisitos", set()), ("Usa como aplicación", aplicacion.get(libro, set()))):
                for m in REF.finditer(datos["campos"].get(campo, "")):
                    rl = int(m.group(1))
                    ref = m.group(0)
                    if rl not in libros:
                        if rl >= libro:
                            errores.append(f"{lugar}: referencia {ref} a un libro posterior o sin índice")
                        else:
                            avisos.append(f"{lugar}: {ref} no puede verificarse (libro sin índice)")
                        continue
                    rcaps, rapend = libros[rl]
                    if m.group(5):
                        if m.group(5) not in rapend:
                            errores.append(f"{lugar}: {ref} no existe")
                        rc = None
                    else:
                        rc = int(m.group(2) or m.group(4))
                        if rc not in rcaps:
                            errores.append(f"{lugar}: {ref} no existe")
                            continue
                        if m.group(2):
                            rs = int(m.group(3))
                            if (rc, rs) not in rcaps[rc]["secciones"]:
                                errores.append(f"{lugar}: {ref} no existe")
                            elif rs in rcaps[rc]["opcionales"]:
                                avisos.append(f"{lugar}: prerrequisito sobre sección opcional {ref}")
                    if rl == libro:
                        if rc is not None and rc >= c:
                            errores.append(f"{lugar}: {ref} no es anterior al capítulo")
                    elif rl > libro:
                        errores.append(f"{lugar}: {ref} es de un libro posterior")
                    elif campo == "Prerrequisitos" and rl not in permitidos:
                        errores.append(f"{lugar}: L{rl} no está entre los requisitos declarados de L{libro} (ni transitivamente)")
                    elif campo != "Prerrequisitos" and rl not in permitidos | extra:
                        errores.append(f"{lugar}: L{rl} no está declarado como requisito ni como aplicación de L{libro}")
                    if campo == "Prerrequisitos" and rl != libro:
                        usados[libro].add(rl)
                    if rc is not None:
                        deps.add((rl, rc, campo != "Prerrequisitos"))
            for n in RA.findall(datos["campos"].get("Resultados admitidos", "")):
                if int(n) not in ras:
                    errores.append(f"{lugar}: RA-{n} no está en el registro de resultados admitidos")
            dependencias[(libro, c)] = deps

    for libro in libros:
        for r in requisitos.get(libro, set()) - usados[libro]:
            avisos.append(f"L{libro}: el requisito declarado L{r} no es usado directamente por ningún capítulo")

    escribir_dependencias(libros, dependencias, requisitos)
    for a in avisos:
        print("AVISO:", a)
    for e in errores:
        print("ERROR:", e)
    total = sum(len(c) for c, _ in libros.values())
    print(f"Libros verificados: {len(libros)}; capítulos: {total}; errores: {len(errores)}; avisos: {len(avisos)}")
    return 1 if errores else 0


def escribir_dependencias(libros, dependencias, requisitos):
    salida = ["# Mapa de dependencias por capítulo", "",
              "Generado automáticamente por `herramientas/verificar_indices.py` a partir de los índices detallados. No editar a mano.", "",
              "Cada fila indica los capítulos de los que depende un capítulo (a nivel de capítulo, aunque el índice cite secciones). "
              "Las dependencias marcadas «(aplic.)» solo aportan ejemplos o aplicaciones.", ""]
    for libro, (caps, _) in sorted(libros.items()):
        salida += [f"## L{libro}", "", f"Requisitos declarados en el plan: {', '.join(f'L{r}' for r in sorted(requisitos.get(libro, ()))) or 'ninguno'}.", "",
                   "| Capítulo | Depende de |", "|---|---|"]
        for c, datos in sorted(caps.items()):
            deps = sorted(dependencias[(libro, c)])
            texto = ", ".join(f"L{rl} c. {rc}" + (" (aplic.)" if ap else "") for rl, rc, ap in deps) or "—"
            salida.append(f"| {c}. {datos['titulo']} | {texto} |")
        salida.append("")
    (RAIZ / "editorial" / "dependencias.md").write_text("\n".join(salida), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
