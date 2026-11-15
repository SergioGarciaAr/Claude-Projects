#!/usr/bin/env python3
"""Instala paquetes de conda-forge sin gestor de conda (el entorno no puede descargar micromamba).

Uso:  python conda_extraer.py PREFIJO CACHE paquete==versión [paquete==versión ...]
      python conda_extraer.py PREFIJO --lista versiones_composicion.txt

El segundo modo reinstala exactamente los archivos registrados (nombre, versión, archivo, sha256)
en la sección «conda-forge» del archivo de versiones; es el modo reproducible, porque el índice
reducido de conda-forge solo conserva las versiones más recientes.

- Lee los índices de conda-forge (linux-64 y noarch) guardados en CACHE
  (current_repodata.json y noarch_current_repodata.json).
- Resuelve las dependencias de forma simple: para cada nombre toma la versión más
  reciente que cumple todas las restricciones vistas hasta ese momento. Los paquetes
  virtuales (__glibc, etc.) se ignoran. Si una restricción no puede cumplirse, se detiene.
- Descarga cada archivo, verifica su SHA-256 contra el índice y lo extrae en PREFIJO,
  reemplazando el marcador de prefijo de conda en archivos de texto y binarios.
- Escribe PREFIJO/conda-meta/instalados.txt con la lista exacta (nombre, versión, archivo, sha256).
Requiere el módulo zstandard (para el formato .conda).
"""
import hashlib
import io
import json
import re
import sys
import tarfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import zstandard

CANAL = "https://conda.anaconda.org/conda-forge"


def clave_version(v):
    """Clave de orden aproximada para versiones de conda (suficiente para los paquetes usados)."""
    partes = []
    for p in re.split(r"[._-]", v):
        partes.append((0, int(p), "") if p.isdigit() else (1, 0, p))
    return partes


def cumple(version, spec):
    """Evalúa una especificación de conda simple: '1.2', '1.2.*', '>=1,<2', '>=1'."""
    if not spec:
        return True
    for parte in spec.split(","):
        parte = parte.strip()
        m = re.match(r"(>=|<=|>|<|==|!=)?(.+)", parte)
        op, ref = m.group(1) or "==", m.group(2)
        if ref.endswith(".*"):
            base = ref[:-2]
            ok = version == base or version.startswith(base + ".")
            if op == "!=":
                ok = not ok
        else:
            ref = re.sub(r"\.0a0$", "", ref)
            a, b = clave_version(version), clave_version(ref)
            ok = {"==": a == b or version.startswith(ref + "."), "!=": a != b, ">=": a >= b,
                  "<=": a <= b, ">": a > b, "<": a < b}[op]
        if not ok:
            return False
    return True


def cargar_indice(cache):
    paquetes = {}
    for nombre, sub in (("current_repodata.json", "linux-64"), ("noarch_current_repodata.json", "noarch")):
        d = json.loads((Path(cache) / nombre).read_text())
        for fn, m in {**d.get("packages", {}), **d.get("packages.conda", {})}.items():
            paquetes.setdefault(m["name"], []).append({**m, "fn": fn, "subdir": sub})
    return paquetes


def resolver(indice, pedidos):
    restricciones, elegidos, pendientes = {}, {}, list(pedidos)
    while pendientes:
        dep = pendientes.pop()
        nombre, _, spec = dep.partition(" ")
        if "==" in nombre:
            nombre, spec = nombre.split("==")
        if nombre.startswith("__"):
            continue
        spec = spec.split(" ")[0]
        restricciones.setdefault(nombre, set()).add(spec)
        candidatos = [p for p in indice.get(nombre, []) if all(cumple(p["version"], s) for s in restricciones[nombre])]
        if not candidatos:
            sys.exit(f"Sin candidato para {nombre} con {sorted(restricciones[nombre])}")
        mejor = max(candidatos, key=lambda p: (clave_version(p["version"]), p.get("build_number", 0), p["fn"].endswith(".conda")))
        if elegidos.get(nombre, {}).get("fn") != mejor["fn"]:
            elegidos[nombre] = mejor
            pendientes.extend(mejor.get("depends", []))
    return elegidos


def extraer(pkg, prefijo):
    url = f"{CANAL}/{pkg['subdir']}/{pkg['fn']}"
    datos = urllib.request.urlopen(url, timeout=600).read()
    if hashlib.sha256(datos).hexdigest() != pkg["sha256"]:
        sys.exit(f"SHA-256 incorrecto: {pkg['fn']}")
    miembros = []
    if pkg["fn"].endswith(".conda"):
        z = zipfile.ZipFile(io.BytesIO(datos))
        for n in z.namelist():
            if n.endswith(".tar.zst"):
                bruto = zstandard.ZstdDecompressor().stream_reader(io.BytesIO(z.read(n))).read()
                miembros.append(tarfile.open(fileobj=io.BytesIO(bruto)))
    else:
        miembros.append(tarfile.open(fileobj=io.BytesIO(datos), mode="r:bz2"))
    info_paths = None
    for t in miembros:
        for m in t.getmembers():
            if m.name == "info/paths.json":
                info_paths = json.load(t.extractfile(m))
            if m.name.startswith("info/"):
                continue
            t.extract(m, prefijo, filter="tar")
    # Reemplazo del marcador de prefijo
    for p in (info_paths or {}).get("paths", []):
        marcador = p.get("prefix_placeholder")
        if not marcador:
            continue
        ruta = Path(prefijo) / p["_path"]
        contenido = ruta.read_bytes()
        nuevo_prefijo = str(prefijo).encode()
        if p.get("file_mode") == "binary":
            def sustituir(mo):
                cadena = mo.group(0)
                reemplazo = cadena.replace(marcador.encode(), nuevo_prefijo)
                return reemplazo + b"\0" * (len(cadena) - len(reemplazo))
            contenido = re.sub(re.escape(marcador.encode()) + rb"[^\0]*\0", sustituir, contenido)
        else:
            contenido = contenido.replace(marcador.encode(), nuevo_prefijo)
        ruta.write_bytes(contenido)


def instalar_lista(prefijo, archivo):
    """Instala los paquetes registrados en el archivo de versiones, verificando su SHA-256."""
    registro, en_seccion = [], False
    for linea in Path(archivo).read_text(encoding="utf-8").splitlines():
        if linea.startswith("## "):
            en_seccion = linea.startswith("## conda-forge")
            continue
        partes = linea.split("\t")
        if en_seccion and len(partes) == 4:
            nombre, version, fn, sha = partes
            for sub in ("linux-64", "noarch"):
                pkg = {"fn": fn, "subdir": sub, "sha256": sha}
                try:
                    print(f"instalando {fn} ({sub})", flush=True)
                    extraer(pkg, prefijo)
                    registro.append(linea)
                    break
                except urllib.error.HTTPError:
                    continue
            else:
                sys.exit(f"No se encontró {fn} en conda-forge")
    (prefijo / "conda-meta").mkdir(parents=True, exist_ok=True)
    (prefijo / "conda-meta" / "instalados.txt").write_text("\n".join(registro) + "\n")


def main():
    if len(sys.argv) == 4 and sys.argv[2] == "--lista":
        instalar_lista(Path(sys.argv[1]).resolve(), sys.argv[3])
        return
    prefijo, cache, pedidos = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3:]
    elegidos = resolver(cargar_indice(cache), pedidos)
    (prefijo / "conda-meta").mkdir(parents=True, exist_ok=True)
    registro = []
    for nombre, pkg in sorted(elegidos.items()):
        print(f"instalando {pkg['fn']}", flush=True)
        extraer(pkg, prefijo)
        registro.append(f"{nombre}\t{pkg['version']}\t{pkg['fn']}\t{pkg['sha256']}")
    (prefijo / "conda-meta" / "instalados.txt").write_text("\n".join(registro) + "\n")


if __name__ == "__main__":
    main()
