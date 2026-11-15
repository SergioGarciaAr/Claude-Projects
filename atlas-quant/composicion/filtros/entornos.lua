-- Entornos propios de la obra (LIBRO_DE_ESTILO.md, §6.1 y §6.2):
--   .hipotesis   Hipótesis de modelización   numerada por capítulo
--   .empirico    Resultado empírico          numerada por capítulo
--   .admitido    Resultado admitido          numerada por capítulo
--   .convencion  Convención de mercado       sin numerar
--   .presentacion  página de presentación del capítulo (prerrequisitos y objetivos)
-- Un encabezado inicial del div, si existe, es su título. Un identificador con prefijo
-- hip-, emp- o adm- permite citarlo con @hip-…, @emp-…, @adm-… (se resuelve con \ref).
local tipos = {
  hipotesis = {nombre = "Hipótesis de modelización", numerado = true},
  empirico = {nombre = "Resultado empírico", numerado = true},
  admitido = {nombre = "Resultado admitido", numerado = true},
  convencion = {nombre = "Convención de mercado", numerado = false},
}
local prefijos = {["hip"] = "Hipótesis de modelización", ["emp"] = "Resultado empírico", ["adm"] = "Resultado admitido"}

local function Div(el)
  if el.classes:includes("presentacion") then
    if quarto.doc.is_format("latex") then
      local salida = pandoc.List({pandoc.RawBlock("latex", "\\begin{atlaspresentacion}")})
      salida:extend(el.content)
      salida:insert(pandoc.RawBlock("latex", "\\end{atlaspresentacion}"))
      return salida
    end
    return el.content
  end
  local clase
  for c, _ in pairs(tipos) do
    if el.classes:includes(c) then clase = c end
  end
  if not clase then return nil end
  local t = tipos[clase]
  local titulo
  local cuerpo = pandoc.List(el.content)
  if #cuerpo > 0 and cuerpo[1].t == "Header" then
    titulo = pandoc.utils.stringify(cuerpo[1].content)
    cuerpo:remove(1)
  end
  if quarto.doc.is_format("latex") then
    local cab
    if t.numerado then
      cab = "\\refstepcounter{" .. clase .. "}" .. t.nombre .. "~\\the" .. clase
      if el.identifier ~= "" then cab = cab .. "\\label{" .. el.identifier .. "}" end
    else
      cab = t.nombre
    end
    if titulo then cab = cab .. " (\\mdseries " .. titulo .. ")" end
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
  end
  local cab = pandoc.Strong({pandoc.Str(t.nombre .. (titulo and (" (" .. titulo .. ")") or "") .. ".")})
  if cuerpo[1] and cuerpo[1].t == "Para" then
    cuerpo[1].content:insert(1, pandoc.Space())
    cuerpo[1].content:insert(1, cab)
  else
    cuerpo:insert(1, pandoc.Para({cab}))
  end
  return cuerpo
end

local function Cite(el)
  if #el.citations ~= 1 then return nil end
  local id = el.citations[1].id
  local pref = id:match("^(%a+)%-")
  if not (pref and prefijos[pref]) then return nil end
  if quarto.doc.is_format("latex") then
    return pandoc.RawInline("latex", prefijos[pref] .. "~\\ref{" .. id .. "}")
  end
  return pandoc.Str(prefijos[pref])
end

return {{Div = Div}, {Cite = Cite}}
