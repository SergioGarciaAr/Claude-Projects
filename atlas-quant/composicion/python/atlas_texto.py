"""Utilidades de composición para las celdas ocultas de los capítulos (no forman parte del código del lector).

Convierten números al formato de la prosa (LIBRO_DE_ESTILO.md, §12): coma decimal, espacio fino
no separable (U+202F) como separador de millares en números de más de cuatro cifras, signo menos
tipográfico (U+2212) y espacio antes de %.
"""

ESPACIO_FINO = " "
MENOS = "−"


def numero(x, decimales=2):
    """Número con coma decimal; separador de millares solo con más de cuatro cifras enteras."""
    texto = f"{abs(x):.{decimales}f}"
    entera, _, frac = texto.partition(".")
    if len(entera) > 4:
        grupos = []
        while entera:
            grupos.insert(0, entera[-3:])
            entera = entera[:-3]
        entera = ESPACIO_FINO.join(grupos)
    resultado = entera + ("," + frac if frac else "")
    return (MENOS if x < 0 and float(texto) != 0 else "") + resultado


def porcentaje(x, decimales=2):
    """Fracción decimal como porcentaje: 0.05 -> '5,00 %' (espacio no separable antes de %)."""
    return numero(100 * x, decimales) + " %"


def tabla(encabezados, filas, alineacion=None):
    """Tabla en Markdown de pandoc; alineación por columna con 'l', 'r' o 'c'."""
    alineacion = alineacion or ["r"] * len(encabezados)
    marcas = {"l": ":---", "r": "---:", "c": ":---:"}
    lineas = ["| " + " | ".join(encabezados) + " |",
              "|" + "|".join(marcas[a] for a in alineacion) + "|"]
    lineas += ["| " + " | ".join(fila) + " |" for fila in filas]
    return "\n".join(lineas)
