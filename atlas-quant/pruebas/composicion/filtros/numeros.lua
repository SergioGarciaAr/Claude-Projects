-- Coma decimal en matemáticas: el libro de estilo escribe 0{,}5 en LaTeX.
-- En Typst la coma es puntuación y recibe espacio; los números con coma decimal
-- se convierten en un único literal vertical.
function Math(el)
  if quarto.doc.is_format("typst") and el.text:find("{,}", 1, true) then
    el.text = el.text:gsub("(%d+){,}(%d+)", "\\text{%1,%2}")
    return el
  end
end
