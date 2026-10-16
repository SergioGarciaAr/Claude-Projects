# L11. Análisis real

Índice detallado · Versión 1.0 · Entrega 1c · 2026-10-16

## Ficha editorial

- **Serie:** III. Teoría financiera y modelización.
- **Requisitos:** L4, L6, L7.
- **Capítulos:** 10, más un apéndice.
- **Extensión estimada:** 290–360 páginas.

**Propósito.** Este libro proporciona el análisis riguroso que necesitan la probabilidad con teoría de la medida, las ecuaciones diferenciales y el cálculo estocástico. Construye los números reales, estudia espacios métricos, completitud y el teorema del punto fijo de Banach, la integral de Riemann-Stieltjes, la convergencia uniforme y los espacios normados y con producto interno. Termina con la variación cuadrática de funciones deterministas y la fórmula de cambio de variables de Föllmer, que anticipa la fórmula de Itô sin probabilidad.

**Rutas de lectura.** Puede leerse inmediatamente después de L7. Los capítulos 1 y 5 pueden omitirse en una primera lectura orientada al cálculo estocástico; los capítulos 3, 6, 7, 8 y 10 son los más usados después.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro.

## Capítulos

### Capítulo 1. Construcción de los números reales

**Prerrequisitos:** L1 §3.4, L1 c. 6, L1 c. 7, L4 c. 1.

**Objetivos:** explicar por qué los axiomas de L1 c. 7 necesitan un modelo; construir los reales mediante cortaduras de Dedekind; definir las operaciones y el orden y verificar los axiomas de cuerpo ordenado; demostrar el axioma del supremo como teorema; demostrar, en la sección opcional, la equivalencia con la construcción por sucesiones de Cauchy y la unicidad del cuerpo ordenado completo.

**Secciones:**

- **1.1** Por qué construir los números reales.
- **1.2** Cortaduras de Dedekind.
- **1.3** Operaciones y orden; axiomas de cuerpo ordenado.
- **1.4** La completitud como teorema.
- **1.5\*** Construcción mediante sucesiones de Cauchy; unicidad del cuerpo ordenado completo salvo isomorfismo.
- **1.6** Consecuencia: los axiomas de L1 c. 7 están justificados.

**Resultados principales:** existencia de un cuerpo ordenado completo; unicidad salvo isomorfismo.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** no corresponde.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 2. Espacios métricos, compacidad y conexión

**Prerrequisitos:** L7 c. 1, L1 c. 3.

**Objetivos:** reconocer métricas, incluidas las de espacios de funciones; trabajar con la topología métrica; caracterizar conjuntos cerrados por sucesiones; demostrar la equivalencia entre compacidad por sucesiones y por cubrimientos en espacios métricos; demostrar el teorema de Heine-Borel; caracterizar los conexos de ℝ.

**Secciones:**

- **2.1** Métricas y ejemplos, incluida la métrica del supremo en espacios de funciones.
- **2.2** Topología métrica: abiertos, cerrados y clausura.
- **2.3** Sucesiones, convergencia y subespacios.
- **2.4** Compacidad por sucesiones y por cubrimientos; equivalencia en espacios métricos.
- **2.5** Teorema de Heine-Borel.
- **2.6** Conexión; los conexos de ℝ son los intervalos.

**Resultados principales:** equivalencia de las nociones de compacidad; teorema de Heine-Borel; caracterización de los conexos de ℝ.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** no corresponde.

**Extensión estimada:** 30–36 páginas; 35–45 ejercicios.

### Capítulo 3. Espacios completos y teorema del punto fijo de Banach

**Prerrequisitos:** L11 c. 2, L4 c. 1.

**Objetivos:** reconocer espacios completos; demostrar la completitud de ℝⁿ y del espacio de funciones continuas con la norma del supremo; demostrar el teorema del punto fijo de Banach con su cota del error; aplicarlo a ecuaciones integrales; demostrar el teorema de Baire y construir la completación de un espacio métrico (secciones opcionales).

**Secciones:**

- **3.1** Sucesiones de Cauchy y espacios completos.
- **3.2** Completitud de ℝⁿ y de C([a, b]) con la norma del supremo.
- **3.3** Teorema del punto fijo de Banach y cota del error.
- **3.4** Aplicaciones: ecuaciones integrales de Volterra; el método de Newton como punto fijo.
- **3.5\*** Teorema de Baire.
- **3.6\*** Completación de un espacio métrico.

**Resultados principales:** completitud de C([a, b]); teorema del punto fijo de Banach; teorema de Baire.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** existencia y unicidad de soluciones de ecuaciones de valor recursivas.

**Computación:** iteración de punto fijo y verificación de la cota del error.

**Extensión estimada:** 26–32 páginas; 30–40 ejercicios.

### Capítulo 4. Continuidad y continuidad uniforme

**Prerrequisitos:** L11 c. 2, L4 §3.6.

**Objetivos:** caracterizar la continuidad en espacios métricos; demostrar que la imagen continua de un compacto es compacta; demostrar el teorema de Heine en espacios métricos compactos; trabajar con funciones de Lipschitz y de Hölder; extender funciones uniformemente continuas a la clausura.

**Secciones:**

- **4.1** Continuidad en espacios métricos: caracterizaciones.
- **4.2** Imagen continua de compactos; existencia de extremos.
- **4.3** Continuidad uniforme; teorema de Heine en compactos métricos.
- **4.4** Funciones de Lipschitz y de Hölder.
- **4.5** Extensión de funciones uniformemente continuas.

**Resultados principales:** teorema de Heine; teorema de extensión.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** no corresponde.

**Extensión estimada:** 22–28 páginas; 25–35 ejercicios.

### Capítulo 5. Diferenciabilidad rigurosa

**Prerrequisitos:** L11 c. 3, L11 c. 4, L7 c. 3, L7 c. 8.

**Objetivos:** definir la derivada de Fréchet en espacios normados; demostrar la regla de la cadena y la desigualdad del valor medio en ese contexto; relacionar diferenciabilidad y convexidad mediante subgradientes; reformular el teorema de la función inversa como aplicación del punto fijo de Banach.

**Secciones:**

- **5.1** Derivada de Fréchet en espacios normados.
- **5.2** Regla de la cadena.
- **5.3** Desigualdad del valor medio en espacios normados.
- **5.4** Diferenciabilidad, convexidad y subgradientes.
- **5.5** Revisión del teorema de la función inversa mediante el punto fijo de Banach.

**Resultados principales:** regla de la cadena y desigualdad del valor medio en espacios normados; caracterización de la diferenciabilidad de funciones convexas mediante el subdiferencial.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** no corresponde.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

### Capítulo 6. Integral de Riemann-Stieltjes y variación acotada

**Prerrequisitos:** L11 c. 4, L4 c. 8, L4 c. 9.

**Objetivos:** definir funciones de variación acotada y demostrar su descomposición de Jordan; definir la integral de Riemann-Stieltjes; demostrar su existencia para integrandos continuos e integradores de variación acotada; aplicar la integración por partes; expresar esperanzas de variables discretas y ganancias de estrategias de negociación como integrales de Stieltjes.

**Secciones:**

- **6.1** Funciones de variación acotada; descomposición de Jordan.
- **6.2** Integral de Riemann-Stieltjes.
- **6.3** Existencia para integrandos continuos e integradores de variación acotada.
- **6.4** Integración por partes y cambio de variable.
- **6.5** Integradores escalonados: sumas como integrales.
- **6.6** Ganancias de una estrategia de negociación como integral de Stieltjes (preparación para la integral estocástica).

**Resultados principales:** descomposición de Jordan; teorema de existencia; fórmula de integración por partes.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** proceso de ganancias de una estrategia.

**Computación:** aproximación numérica de integrales de Stieltjes.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 7. Convergencia uniforme e intercambio de límites

**Prerrequisitos:** L11 c. 3, L11 c. 6, L4 §13.5.

**Objetivos:** distinguir convergencia puntual y uniforme; demostrar la continuidad del límite uniforme y los teoremas de intercambio de límite con integral y con derivada; aplicar el criterio M de Weierstrass; demostrar el teorema de aproximación de Weierstrass; construir una función continua no derivable en ningún punto y demostrar el teorema de Arzelà-Ascoli (secciones opcionales).

**Secciones:**

- **7.1** Convergencia puntual y convergencia uniforme.
- **7.2** Continuidad del límite uniforme.
- **7.3** Intercambio de límite e integral (de Riemann y de Stieltjes).
- **7.4** Intercambio de límite y derivada.
- **7.5** Criterio M de Weierstrass; series de funciones.
- **7.6** Teorema de aproximación de Weierstrass mediante núcleos de Landau.
- **7.7\*** Una función continua no derivable en ningún punto.
- **7.8\*** Teorema de Arzelà-Ascoli.

**Resultados principales:** teoremas de intercambio de límites; teorema de aproximación de Weierstrass; teorema de Arzelà-Ascoli.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** visualización de convergencia no uniforme.

**Extensión estimada:** 30–36 páginas; 35–45 ejercicios.

### Capítulo 8. Espacios normados y con producto interno

**Prerrequisitos:** L11 c. 3, L11 c. 7, L6 c. 7.

**Objetivos:** trabajar con espacios normados y de Banach, incluidos ℓ¹, ℓ² y ℓ^∞; definir operadores acotados y su norma; caracterizar los espacios con producto interno por la ley del paralelogramo; demostrar el teorema de la proyección en espacios de Hilbert; trabajar con bases ortonormales y la desigualdad de Bessel; explicar por qué el espacio de funciones integrables según Riemann no es completo.

**Secciones:**

- **8.1** Espacios normados; ejemplos ℓ¹, ℓ², ℓ^∞ y C([a, b]).
- **8.2** Espacios de Banach; completitud de ℓ¹, ℓ² y ℓ^∞ (el caso ℓ^p general está en L11 §9.4).
- **8.3** Operadores lineales acotados y norma de operador.
- **8.4** Espacios con producto interno; ley del paralelogramo.
- **8.5** Espacios de Hilbert: teorema de la proyección.
- **8.6** Bases ortonormales, desigualdad de Bessel y series de Fourier abstractas.
- **8.7** El espacio de funciones integrables según Riemann con la norma cuadrática no es completo: motivación de la integral de Lebesgue (L16).

**Resultados principales:** teorema de la proyección en espacios de Hilbert; desigualdad de Bessel; falta de completitud del espacio de Riemann.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** la valoración como proyección en espacios de pagos (generaliza L10 §9.4).

**Computación:** no corresponde.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 9. Funciones convexas y desigualdades

**Prerrequisitos:** L11 c. 8, L7 c. 7, L4 §6.4.

**Objetivos:** demostrar la continuidad de las funciones convexas en el interior de su dominio; demostrar la desigualdad de Jensen en versiones discreta e integral; demostrar las desigualdades de Young, Hölder y Minkowski; demostrar la completitud de ℓ^p para todo p ≥ 1; definir el conjugado convexo; aplicar estas desigualdades a problemas financieros.

**Secciones:**

- **9.1** Funciones convexas: continuidad en el interior del dominio.
- **9.2** Desigualdad de Jensen discreta e integral.
- **9.3** Desigualdades de Young, Hölder y Minkowski.
- **9.4** Espacios ℓ^p para p ≥ 1 y su completitud.
- **9.5** Conjugado convexo de Legendre-Fenchel.
- **9.6** Aplicaciones: media geométrica y aritmética; convexidad de los pagos de opciones.

**Resultados principales:** continuidad de las funciones convexas; desigualdades de Jensen, Hölder y Minkowski; completitud de ℓ^p.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** desigualdades entre medias de rendimientos; convexidad de pagos.

**Computación:** no corresponde.

**Extensión estimada:** 24–30 páginas; 30–40 ejercicios.

### Capítulo 10. Variación cuadrática de funciones deterministas

**Prerrequisitos:** L11 c. 6, L11 c. 7, L4 c. 6, L7 §5.3.

**Objetivos:** definir la variación cuadrática a lo largo de una sucesión de particiones; demostrar que las funciones continuas de variación acotada tienen variación cuadrática nula; demostrar, en la sección opcional, que la existencia de la integral de Stieltjes para todo integrando continuo exige variación acotada; construir funciones con variación cuadrática no nula; demostrar la fórmula de cambio de variables de Föllmer para funciones con variación cuadrática.

**Secciones:**

- **10.1** Variación cuadrática a lo largo de una sucesión de particiones.
- **10.2** Las funciones continuas de variación acotada tienen variación cuadrática nula.
- **10.3\*** La integral de Stieltjes para todo integrando continuo exige variación acotada (mediante el teorema de Baire, L11 §3.5).
- **10.4** Funciones continuas con variación cuadrática no nula.
- **10.5** Fórmula de cambio de variables de Föllmer: el término de segundo orden.
- **10.6** Anticipo: las trayectorias del movimiento browniano (L18).

**Resultados principales:** variación cuadrática nula de las funciones de variación acotada; fórmula de Föllmer.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** por qué las ganancias de una estrategia sobre precios con variación cuadrática no nula requieren un cálculo nuevo.

**Computación:** cálculo numérico de variaciones cuadráticas sobre trayectorias simuladas.

**Extensión estimada:** 24–30 páginas; 20–30 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
