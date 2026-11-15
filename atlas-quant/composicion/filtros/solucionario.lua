-- Separa el solucionario. Se ejecuta después de la etapa de Quarto (at: post-quarto).
-- Modo normal: elimina los bloques .solucion.
-- Modo solucionario (metadato solucionario: true): conserva los encabezados de capítulo,
-- cada ejercicio (el bloque inmediatamente anterior a un .solucion) y su solución.
-- Las referencias a teoremas y ecuaciones del libro se resuelven en LaTeX con el paquete xr,
-- que lee el archivo .aux de la compilación del libro (latex/solucionario.tex).
local modo = false

local function es_solucion(b)
  return b and b.t == "Div" and b.classes:includes("solucion")
end

local function es_capitulo(b)
  if b.t == "Header" and b.level == 1 then return true end
  if b.t == "Div" then
    -- Quarto envuelve cada capítulo en un Div cuyo segundo o tercer hijo es el encabezado
    for j = 1, math.min(3, #b.content) do
      local p = b.content[j]
      if p.t == "Header" and p.level == 1 then return true end
    end
  end
  return false
end

function Pandoc(doc)
  modo = doc.meta.solucionario == true
  local salida = pandoc.List()
  local bloques = doc.blocks
  for i, b in ipairs(bloques) do
    if not modo then
      if not es_solucion(b) then salida:insert(b) end
    elseif es_capitulo(b) or b.t == "RawBlock" then
      salida:insert(b)
    elseif es_solucion(bloques[i + 1]) then
      salida:insert(b)
    elseif es_solucion(b) then
      salida:insert(pandoc.Para({pandoc.Emph({pandoc.Str("Solución.")})}))
      salida:extend(b.content)
    end
  end
  doc.blocks = salida
  return doc
end
