-- Entornos propios de la obra sin equivalente nativo en Quarto (LIBRO_DE_ESTILO.md, sección 7):
-- .hipotesis, .empirico, .admitido, .convencion. Un encabezado inicial del div, si existe,
-- se usa como título. En LaTeX se emiten los entornos definidos en latex/preambulo.tex;
-- en Typst, un bloque con filete lateral; en otros formatos, un párrafo con el nombre en negrita.
local nombres = {
  hipotesis = "Hipótesis de modelización",
  empirico = "Resultado empírico",
  admitido = "Resultado admitido",
  convencion = "Convención de mercado",
}

function Div(el)
  local clase
  for c, _ in pairs(nombres) do
    if el.classes:includes(c) then clase = c end
  end
  if not clase then return nil end
  local titulo = nil
  local cuerpo = pandoc.List(el.content)
  if #cuerpo > 0 and cuerpo[1].t == "Header" then
    titulo = pandoc.utils.stringify(cuerpo[1].content)
    cuerpo:remove(1)
  end
  if quarto.doc.is_format("latex") then
    local cab = nombres[clase] .. (titulo and (" (\\mdseries " .. titulo .. ")") or "")
    local marca = pandoc.RawInline("latex", "\\atlasnotatitulo{" .. cab .. "}")
    if cuerpo[1] and cuerpo[1].t == "Para" then
      cuerpo[1].content:insert(1, marca)
    else
      cuerpo:insert(1, pandoc.Para({marca}))
    end
    local salida = pandoc.List({pandoc.RawBlock("latex", "\\begin{atlasnota}")})
    salida:extend(cuerpo)
    salida:insert(pandoc.RawBlock("latex", "\\end{atlasnota}"))
    return salida
  elseif quarto.doc.is_format("typst") then
    local cab = "*" .. nombres[clase] .. (titulo and (" (" .. titulo .. ")") or "") .. ".* "
    local salida = pandoc.List({pandoc.RawBlock("typst", "#block(stroke: (left: 1.5pt + luma(140)), inset: (left: 8pt, y: 4pt))[" .. cab)})
    salida:extend(cuerpo)
    salida:insert(pandoc.RawBlock("typst", "]"))
    return salida
  end
  local cab = pandoc.Strong({pandoc.Str(nombres[clase] .. (titulo and (" (" .. titulo .. ")") or "") .. ".")})
  if cuerpo[1] and cuerpo[1].t == "Para" then
    cuerpo[1].content:insert(1, pandoc.Space())
    cuerpo[1].content:insert(1, cab)
  else
    cuerpo:insert(1, pandoc.Para({cab}))
  end
  return cuerpo
end
