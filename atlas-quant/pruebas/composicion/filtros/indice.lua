-- Índice analítico: [término]{.idx} muestra el término y crea una entrada;
-- []{.idx entrada="término"} crea solo la entrada. LaTeX usa \index (con clave de orden sin
-- acentos); Typst usa metadatos con la etiqueta <idx>, que typst/indice.typ recopila.
local function sin_acentos(s)
  local mapa = {["á"]="a",["é"]="e",["í"]="i",["ó"]="o",["ú"]="u",["ü"]="u",["ñ"]="n~",
                ["Á"]="a",["É"]="e",["Í"]="i",["Ó"]="o",["Ú"]="u",["Ñ"]="n~"}
  for k, v in pairs(mapa) do s = s:gsub(k, v) end
  return s:lower()
end

function Span(el)
  if not el.classes:includes("idx") then return nil end
  local termo = el.attributes["entrada"] or pandoc.utils.stringify(el.content)
  local marca
  if quarto.doc.is_format("latex") then
    marca = pandoc.RawInline("latex", "\\index{" .. sin_acentos(termo) .. "@" .. termo .. "}")
  elseif quarto.doc.is_format("typst") then
    marca = pandoc.RawInline("typst", '#metadata("' .. termo .. '")<idx>')
  else
    return el.content
  end
  local salida = pandoc.List(el.content)
  salida:insert(marca)
  return salida
end
