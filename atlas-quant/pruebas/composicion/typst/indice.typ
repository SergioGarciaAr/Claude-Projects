// Índice analítico para la salida Typst: recopila los metadatos <idx> que emite filtros/indice.lua.
#let clave-orden(t) = {
  let s = lower(t)
  for (a, b) in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ü", "u"), ("ñ", "n~")) {
    s = s.replace(a, b)
  }
  s
}
#pagebreak(weak: true)
#heading(numbering: none)[Índice analítico]
#context {
  let mapa = (:)
  for e in query(<idx>) {
    let t = e.value
    let p = counter(page).at(e.location()).first()
    let lista = mapa.at(t, default: ())
    if p not in lista { lista.push(p) }
    mapa.insert(t, lista)
  }
  let claves = mapa.keys().sorted(key: clave-orden)
  columns(2, for k in claves [#k, #mapa.at(k).map(str).join(", ") \ ])
}
