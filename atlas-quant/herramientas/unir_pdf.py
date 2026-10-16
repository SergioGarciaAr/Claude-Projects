"""Une varios PDF en uno, en el orden dado. Uso: python3 herramientas/unir_pdf.py salida.pdf entrada1.pdf entrada2.pdf ..."""
import sys
from pypdf import PdfWriter

salida, entradas = sys.argv[1], sys.argv[2:]
escritor = PdfWriter()
for ruta in entradas:
    escritor.append(ruta)  # conserva los marcadores de cada documento
with open(salida, "wb") as f:
    escritor.write(f)
print(f"{len(entradas)} documentos unidos en {salida}")
