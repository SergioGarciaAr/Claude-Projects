#!/usr/bin/env python3
"""Genera bibliografia/bibliografia.md a partir de bibliografia/atlas.bib.

Uso (desde atlas-quant/): python3 herramientas/bib_a_md.py

Además de la versión legible, informa:
  - número de entradas por estado de verificación y por sección;
  - claves duplicadas;
  - resultados admitidos con referencia externa (según editorial/resultados_admitidos.md)
    sin ninguna entrada que los cite en el campo `uso`.
Devuelve código 1 si hay claves duplicadas o resultados admitidos sin referencia.
"""
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BIB = RAIZ / "bibliografia" / "atlas.bib"
SALIDA = RAIZ / "bibliografia" / "bibliografia.md"
REGISTRO_RA = RAIZ / "editorial" / "resultados_admitidos.md"

# Sustituciones mínimas de LaTeX a Unicode para la versión legible.
LATEX = [(r"{\\'e}", "é"), (r"{\\'a}", "á"), (r"{\\'o}", "ó"), (r"{\\'i}", "í"), (r"{\\'u}", "ú"),
         (r"{\\'E}", "É"), (r'{\\"o}', "ö"), (r'{\\"u}', "ü"), (r"{\\^o}", "ô"), (r"{\\o}", "ø"),
         (r"{\\v{c}}", "č"), (r"{\\O}", "Ø"), (r"\\O ", "Ø"), (r"\\&", "&"), (r"\\ldots{}", "…"), ("--", "–")]


def ra_con_referencia_externa():
    """Lee del registro de resultados admitidos la lista de los que requieren referencia externa.

    La fila de resumen tiene la forma «| Admitidos con referencia externa ... | RA-07, RA-11 a RA-21, ... |».
    """
    for linea in REGISTRO_RA.read_text(encoding="utf-8").splitlines():
        if linea.startswith("| Admitidos con referencia externa"):
            lista = linea.rstrip(" |").split("|")[-1]
            numeros = set()
            for a, b in re.findall(r"RA-(\d+)(?: a RA-(\d+))?", lista):
                numeros.update(range(int(a), int(b or a) + 1))
            return sorted(numeros)
    sys.exit("No se encontró la fila de resumen en editorial/resultados_admitidos.md")


def limpiar(texto):
    """Convierte acentos LaTeX y elimina llaves de protección."""
    for a, b in LATEX:
        texto = texto.replace(a.replace("\\\\", "\\"), b)
    return re.sub(r"[{}]", "", texto).strip()


def leer_campos(cuerpo):
    """Lee pares campo = {valor} respetando llaves anidadas."""
    campos, i = {}, 0
    while True:
        m = re.compile(r"\s*([a-z_]+)\s*=\s*\{").match(cuerpo, i)
        if not m:
            break
        nombre, j, nivel = m.group(1), m.end(), 1
        k = j
        while nivel:
            nivel += {"{": 1, "}": -1}.get(cuerpo[k], 0)
            k += 1
        campos[nombre] = cuerpo[j:k - 1]
        i = k
        coma = re.compile(r"\s*,").match(cuerpo, i)
        if coma:
            i = coma.end()
    return campos


def leer_bib(texto):
    """Devuelve una lista de (sección, tipo, clave, campos) en el orden del archivo."""
    entradas = []
    # Localizar cada entrada y la última cabecera de sección que la precede.
    posiciones = [(m.start(), m.group(1), m.group(2)) for m in re.finditer(r"@(\w+)\{([^,]+),", texto)]
    secciones = [(m.start(), m.group(1).strip()) for m in re.finditer(r"% -{10,}\n% ([^\n]+)\n% -{10,}", texto)]
    for inicio, tipo, clave in posiciones:
        previas = [s for p, s in secciones if p < inicio]
        seccion = previas[-1] if previas else "Sin sección"
        # cuerpo: desde la coma tras la clave hasta la llave de cierre de la entrada
        j, nivel = texto.index(",", inicio) + 1, 1
        k = j
        while nivel:
            nivel += {"{": 1, "}": -1}.get(texto[k], 0)
            k += 1
        entradas.append((seccion, tipo.lower(), clave.strip(), leer_campos(texto[j:k - 1])))
    return entradas


def referencia(tipo, c):
    """Formato legible de una referencia (estilo autor-año simple)."""
    autores = limpiar(c.get("author", "")).replace(" and ", "; ")
    partes = [f"{autores} ({c.get('year', 's. f.')}).", f"*{limpiar(c.get('title', ''))}*."]
    if tipo == "article":
        vol = c.get("volume", "")
        num = f"({c['number']})" if c.get("number") else ""
        pag = f", {limpiar(c['pages'])}" if c.get("pages") else ""
        partes.append(f"{limpiar(c.get('journal', ''))} {vol}{num}{pag}.")
    elif tipo in ("incollection", "inproceedings"):
        pag = f", pp. {limpiar(c['pages'])}" if c.get("pages") else ""
        partes.append(f"En {limpiar(c.get('booktitle', ''))}{pag}.")
    else:
        ed = f"{c['edition']}.ª ed. " if c.get("edition") else ""
        editorial = limpiar(c.get("publisher", c.get("howpublished", c.get("institution", ""))))
        partes.append(f"{ed}{editorial}.".strip())
    if c.get("isbn"):
        partes.append(f"ISBN {c['isbn']}.")
    if c.get("doi"):
        partes.append(f"DOI {c['doi']}.")
    return " ".join(p for p in partes if p.strip(". "))


def main():
    entradas = leer_bib(BIB.read_text(encoding="utf-8"))
    claves = Counter(e[2] for e in entradas)
    duplicadas = [k for k, v in claves.items() if v > 1]
    estados = Counter(e[3].get("verificacion", "sin estado") for e in entradas)
    usos = " ".join(e[3].get("uso", "") for e in entradas)
    citados = {int(n) for n in re.findall(r"RA-(\d+)", usos)}
    externos = ra_con_referencia_externa()
    sin_ref = [f"RA-{n:02d}" for n in externos if n not in citados]

    por_seccion = OrderedDict()
    for sec, tipo, clave, c in entradas:
        por_seccion.setdefault(sec, []).append((tipo, clave, c))

    out = ["# Bibliografía de la colección", "",
           "Versión legible generada por `herramientas/bib_a_md.py` a partir de `bibliografia/atlas.bib`, que es la fuente.",
           "No editar este archivo a mano.", "",
           "## Estado de la verificación", "",
           "| Estado | Entradas |", "|---|---|"]
    for est in ("verificada", "parcial", "pendiente"):
        out.append(f"| {est} | {estados.get(est, 0)} |")
    out += [f"| **Total** | **{len(entradas)}** |", "",
            "*Verificada*: autores, título, publicación, año y paginación (o ISBN) confirmados en una fuente identificable "
            "(editor, catálogo bibliográfico o índice especializado). *Parcial*: algún dato no pudo confirmarse o las fuentes "
            "discrepan; la nota de cada entrada indica cuál. Los DOI se registran solo cuando una fuente los muestra explícitamente.", ""]
    for sec, lista in por_seccion.items():
        out += [f"## {sec}", ""]
        for tipo, clave, c in sorted(lista, key=lambda t: (limpiar(t[2].get("author", "")).lower(), t[2].get("year", ""))):
            marca = "" if c.get("verificacion") == "verificada" else " **[parcial]**"
            out.append(f"- `{clave}` {referencia(tipo, c)}{marca}\\")
            detalle = f"  Uso: {c.get('uso', '—')}. Verificación: <{c.get('fuente_verificacion', '—')}>."
            if c.get("nota_verificacion"):
                detalle += f" Nota: {limpiar(c['nota_verificacion'])}"
            out.append(detalle)
        out.append("")
    SALIDA.write_text("\n".join(out), encoding="utf-8")

    print(f"Entradas: {len(entradas)} · " + " · ".join(f"{k}: {v}" for k, v in sorted(estados.items())))
    for sec, lista in por_seccion.items():
        print(f"  {sec}: {len(lista)}")
    print(f"Claves duplicadas: {duplicadas or 'ninguna'}")
    print(f"Resultados admitidos con referencia externa: {len(externos)}; sin entrada en la bibliografía: {sin_ref or 'ninguno'}")
    return 1 if duplicadas or sin_ref else 0


if __name__ == "__main__":
    sys.exit(main())
