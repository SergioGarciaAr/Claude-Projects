// Genera los PDF de trabajo de Atlas Quant a partir de las fuentes Markdown.
// Uso (desde atlas-quant/):  NODE_PATH=/opt/node22/lib/node_modules node herramientas/generar_pdf.mjs [archivo.md ...]
// Sin argumentos convierte todos los .md del proyecto, salvo los de herramientas/ y pdf/.
// Salida: pdf/<misma ruta relativa>.pdf; los índices libros/<carpeta>/indice.md salen como pdf/libros/<carpeta>-indice.pdf
// Requisitos: pandoc (HTML con MathML) y Playwright con Chromium, ambos presentes en el entorno.

import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, readdirSync, statSync, rmSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const RAIZ = resolve(dirname(new URL(import.meta.url).pathname), "..");
const CSS = join(RAIZ, "herramientas", "estilo_pdf.css");
const FILTRO = join(RAIZ, "herramientas", "md_a_pdf.lua");
const SALIDA = join(RAIZ, "pdf");
const EXCLUIDOS = new Set(["herramientas", "pdf", ".git"]);
// Documentos largos que llevan índice de contenidos al comienzo.
const CON_INDICE = new Set(["PLAN_EDITORIAL.md", "LIBRO_DE_ESTILO.md", "NOTACION.md", "GLOSARIO.md"]);

function buscarMarkdown(dir) {
  const encontrados = [];
  for (const nombre of readdirSync(dir)) {
    if (EXCLUIDOS.has(nombre)) continue;
    const ruta = join(dir, nombre);
    if (statSync(ruta).isDirectory()) encontrados.push(...buscarMarkdown(ruta));
    else if (nombre.endsWith(".md")) encontrados.push(ruta);
  }
  return encontrados.sort();
}

// Título del documento: el primer encabezado de nivel 1 de la fuente.
function titulo(ruta) {
  const linea = readFileSync(ruta, "utf8").split("\n").find((l) => l.startsWith("# "));
  return linea ? linea.slice(2).trim() : relative(RAIZ, ruta);
}

function aHtml(ruta, destinoHtml) {
  const args = [
    ruta, "--from=markdown-implicit_figures",
    "--to=html5", "--standalone", "--mathml",
    "--shift-heading-level-by=-1",           // el primer encabezado de nivel 1 pasa a ser el título
    `--css=${CSS}`, "--embed-resources",
    `--lua-filter=${FILTRO}`,
    "--metadata=lang:es",
    "-o", destinoHtml,
  ];
  if (CON_INDICE.has(relative(RAIZ, ruta)) || ruta.endsWith("indice.md")) args.push("--toc", "--toc-depth=2", "--metadata=toc-title:Contenido");
  execFileSync("pandoc", args, { cwd: dirname(ruta) });
}

const pie = (texto) => `
  <div style="width:100%; font-family:'Bitstream Charter',serif; font-size:8pt; color:#666; padding:0 20mm; display:flex; justify-content:space-between;">
    <span>Atlas Quant · ${texto}</span>
    <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
  </div>`;

const fuentes = process.argv.length > 2 ? process.argv.slice(2).map((p) => resolve(p)) : buscarMarkdown(RAIZ);
const navegador = await chromium.launch();
try {
  for (const ruta of fuentes) {
    const rel = relative(RAIZ, ruta);
    const destinoPdf = join(SALIDA, rel.replace(/\/indice\.md$/, "-indice.md").replace(/\.md$/, ".pdf"));
    const html = destinoPdf.replace(/\.pdf$/, ".tmp.html");
    mkdirSync(dirname(destinoPdf), { recursive: true });
    aHtml(ruta, html);
    const pagina = await navegador.newPage();
    await pagina.goto("file://" + html, { waitUntil: "load" });
    await pagina.pdf({
      path: destinoPdf, format: "A4", printBackground: true, preferCSSPageSize: true,
      displayHeaderFooter: true, headerTemplate: "<span></span>",
      footerTemplate: pie(titulo(ruta).replace(/[<>&]/g, "")),
    });
    await pagina.close();
    rmSync(html);
    console.log(`${rel} -> ${relative(RAIZ, destinoPdf)}`);
  }
} finally {
  await navegador.close();
}
