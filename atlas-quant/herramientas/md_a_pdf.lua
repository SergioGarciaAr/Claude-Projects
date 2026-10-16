-- Filtro de pandoc para los PDF de trabajo de Atlas Quant:
-- los enlaces relativos a archivos .md pasan a apuntar al .pdf equivalente.
function Link(el)
  if not el.target:match("^%a+://") then
    el.target = el.target:gsub("%.md$", ".pdf"):gsub("%.md#", ".pdf#")
  end
  return el
end
