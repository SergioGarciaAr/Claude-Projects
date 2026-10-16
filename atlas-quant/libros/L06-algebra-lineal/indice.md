# L6. Álgebra lineal

Índice detallado · Versión 1.0 · Entrega 1b · 2026-10-16

## Ficha editorial

- **Serie:** II. Matemática para las finanzas.
- **Requisitos:** L2, L3 (y L1 a través de L2).
- **Uso como aplicación:** L5 (capítulos 11 y 13).
- **Capítulos:** 13, más un apéndice.
- **Extensión estimada:** 370–450 páginas.

**Propósito.** Este libro desarrolla el álgebra lineal necesaria para la estadística multivariante, la optimización, la teoría de carteras, las ecuaciones diferenciales y el análisis numérico. Combina la teoría abstracta (espacios vectoriales, transformaciones lineales, teorema espectral) con el cálculo matricial efectivo (eliminación, factorizaciones LU, QR, Cholesky y en valores singulares) y su comportamiento numérico. Las aplicaciones financieras se limitan a lo que no requiere probabilidad: replicación de pagos, precios de estado como funcional lineal, carteras como vectores y la matriz de covarianza muestral como objeto descriptivo.

**Exponencial de matrices.** Por el ajuste A-10, la exponencial de matrices se estudia en L15 c. 2, donde se usa; este libro desarrolla la forma de Jordan y las potencias de matrices que la preparan.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro (cambio a negritas para vectores y matrices, NOTACION §5).

## Capítulos

### Capítulo 1. Sistemas lineales y eliminación gaussiana

**Prerrequisitos:** L1 c. 12, L2 c. 11, L3 §5.3.

**Objetivos:** escribir sistemas lineales en forma matricial; aplicar operaciones elementales y justificar que preservan el conjunto solución; llevar una matriz a forma escalonada y escalonada reducida; decidir existencia y unicidad de soluciones; describir el conjunto solución con variables libres; estimar el costo de la eliminación.

**Secciones:**

- **1.1** Sistemas lineales en n incógnitas y su notación matricial.
- **1.2** Operaciones elementales y sistemas equivalentes.
- **1.3** Forma escalonada y forma escalonada reducida.
- **1.4\*** Unicidad de la forma escalonada reducida.
- **1.5** Eliminación gaussiana y variables libres.
- **1.6** Existencia y unicidad de soluciones; sistemas homogéneos.
- **1.7** Costo computacional de la eliminación.

**Resultados principales:** las operaciones elementales preservan el conjunto solución; criterio de existencia y unicidad.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** replicación de pagos en varios escenarios (anticipo de L6 c. 13).

**Computación:** eliminación gaussiana en Python.

**Extensión estimada:** 28–34 páginas; 35–45 ejercicios.

### Capítulo 2. Matrices, inversas y factorización LU

**Prerrequisitos:** L6 c. 1.

**Objetivos:** operar con matrices e interpretar el producto como composición; reconocer matrices elementales; calcular inversas y demostrar sus propiedades; enunciar y demostrar equivalencias de la invertibilidad; obtener y usar la factorización LU.

**Secciones:**

- **2.1** Matrices y operaciones; el producto como composición.
- **2.2** Propiedades algebraicas; falta de conmutatividad.
- **2.3** Matrices elementales.
- **2.4** Matriz inversa: existencia, cálculo y propiedades; equivalencias de la invertibilidad.
- **2.5** Transpuesta y matrices simétricas.
- **2.6** Factorización LU y su uso para resolver sistemas.

**Resultados principales:** teorema de la matriz invertible (equivalencias); existencia de la factorización LU sin pivoteo bajo condiciones explícitas.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** factorización LU.

**Extensión estimada:** 28–34 páginas; 40–50 ejercicios.

### Capítulo 3. Espacios vectoriales y subespacios

**Prerrequisitos:** L6 c. 2, L1 c. 3.

**Objetivos:** verificar los axiomas de espacio vectorial en ejemplos (ℝⁿ, polinomios, funciones, matrices); decidir si un subconjunto es un subespacio; describir el espacio generado por un conjunto; calcular el espacio columna y el espacio nulo de una matriz.

**Secciones:**

- **3.1** ℝⁿ como espacio vectorial.
- **3.2** Axiomas y ejemplos: polinomios, funciones y matrices.
- **3.3** Subespacios.
- **3.4** Combinaciones lineales y espacio generado.
- **3.5** Espacio columna y espacio nulo de una matriz.

**Resultados principales:** criterio de subespacio.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** el conjunto de pagos replicables como espacio columna.

**Computación:** no corresponde.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 4. Independencia lineal, bases y dimensión

**Prerrequisitos:** L6 c. 3.

**Objetivos:** decidir la independencia lineal de un conjunto; obtener bases y coordenadas; demostrar que todas las bases tienen el mismo número de elementos; calcular el rango y demostrar que el rango por filas iguala al rango por columnas; cambiar de base.

**Secciones:**

- **4.1** Independencia lineal.
- **4.2** Bases y coordenadas.
- **4.3** Dimensión: lema de intercambio de Steinitz.
- **4.4** Rango; igualdad entre rango por filas y por columnas.
- **4.5** Cambio de base.

**Resultados principales:** lema de intercambio; invariancia de la dimensión; teorema del rango.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** número de activos independientes en un mercado de escenarios.

**Computación:** cálculo del rango y sus dificultades numéricas (anticipo de L6 c. 12).

**Extensión estimada:** 28–34 páginas; 35–45 ejercicios.

### Capítulo 5. Transformaciones lineales

**Prerrequisitos:** L6 c. 4.

**Objetivos:** reconocer transformaciones lineales; obtener su matriz en bases dadas; calcular núcleo e imagen; demostrar el teorema de la dimensión; caracterizar isomorfismos; componer e invertir transformaciones.

**Secciones:**

- **5.1** Definición y ejemplos.
- **5.2** Matriz asociada a una transformación.
- **5.3** Núcleo e imagen.
- **5.4** Teorema de la dimensión.
- **5.5** Isomorfismos.
- **5.6** Composición e inversión.

**Resultados principales:** teorema de la dimensión; correspondencia entre transformaciones y matrices.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** la función de precios lineal como transformación.

**Computación:** no corresponde.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 6. Determinantes

**Prerrequisitos:** L6 c. 5, L1 §3.7.

**Objetivos:** definir el signo de una permutación y demostrar que está bien definido; definir el determinante y caracterizarlo como función multilineal alternada normalizada; demostrar la multiplicatividad del determinante; relacionarlo con la invertibilidad; calcular determinantes por cofactores y mediante LU; interpretarlo como volumen orientado.

**Secciones:**

- **6.1** Permutaciones y signo.
- **6.2** Definición mediante la fórmula de Leibniz; caracterización axiomática.
- **6.3** Multiplicatividad: det(**AB**) = det **A** · det **B**.
- **6.4** Determinante e invertibilidad.
- **6.5** Desarrollo por cofactores; regla de Cramer.
- **6.6** Interpretación como área y volumen orientados.
- **6.7** Cálculo eficiente mediante LU.

**Resultados principales:** buena definición del signo; unicidad de la función determinante; multiplicatividad; criterio de invertibilidad.

**Resultados admitidos:** RA-25 (en §6.6).

**Aplicaciones financieras:** no corresponde.

**Computación:** cálculo de determinantes y sus riesgos numéricos.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 7. Producto interno, Gram-Schmidt y factorización QR

**Prerrequisitos:** L6 c. 4, L2 §11.4.

**Objetivos:** definir productos internos y sus normas; demostrar la desigualdad de Cauchy-Schwarz en espacios con producto interno; construir bases ortonormales con Gram-Schmidt; reconocer matrices ortogonales; obtener la factorización QR; describir el complemento ortogonal.

**Secciones:**

- **7.1** Producto interno y norma inducida; desigualdad de Cauchy-Schwarz.
- **7.2** Ortogonalidad y conjuntos ortonormales.
- **7.3** Matrices ortogonales.
- **7.4** Proceso de Gram-Schmidt.
- **7.5** Factorización QR.
- **7.6** Complemento ortogonal.

**Resultados principales:** desigualdad de Cauchy-Schwarz; existencia de bases ortonormales; existencia de la factorización QR.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** QR con NumPy y comparación con Gram-Schmidt clásico.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 8. Proyecciones ortogonales y mínimos cuadrados

**Prerrequisitos:** L6 c. 7.

**Objetivos:** demostrar el teorema de la mejor aproximación; derivar las ecuaciones normales; resolver problemas de mínimos cuadrados mediante QR; ajustar rectas y polinomios a datos; caracterizar las matrices de proyección.

**Secciones:**

- **8.1** Proyección ortogonal sobre un subespacio; teorema de la mejor aproximación.
- **8.2** Ecuaciones normales.
- **8.3** Mínimos cuadrados mediante QR.
- **8.4** Ajuste de rectas y polinomios a datos (sin modelo probabilístico; la inferencia está en L9 c. 8).
- **8.5** Matrices de proyección: idempotencia y simetría.

**Resultados principales:** teorema de la mejor aproximación; equivalencia entre mínimos cuadrados y ecuaciones normales.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** ajuste descriptivo de una curva de tasas.

**Computación:** mínimos cuadrados con NumPy.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 9. Valores propios, diagonalización y forma de Jordan

**Prerrequisitos:** L6 c. 6, L2 c. 12.

**Objetivos:** calcular valores y vectores propios; trabajar con valores propios complejos; decidir si una matriz es diagonalizable; distinguir multiplicidades algebraica y geométrica; usar la forma de Jordan; calcular potencias de matrices y resolver recurrencias lineales mediante la matriz compañera; demostrar el teorema de Cayley-Hamilton.

**Secciones:**

- **9.1** Valores y vectores propios; polinomio característico.
- **9.2** Valores propios complejos.
- **9.3** Diagonalización; matrices con valores propios distintos.
- **9.4** Multiplicidad algebraica y geométrica.
- **9.5** Forma de Jordan: enunciado y uso.
- **9.6\*** Demostración de la existencia de la forma de Jordan.
- **9.7** Potencias de matrices y recurrencias lineales; matriz compañera.
- **9.8** Teorema de Cayley-Hamilton.

**Resultados principales:** criterio de diagonalización; independencia de vectores propios asociados a valores propios distintos; existencia de la forma de Jordan; teorema de Cayley-Hamilton.

**Resultados admitidos:** RA-07 (en §9.2).

**Aplicaciones financieras:** recurrencias de saldos con varias cuentas.

**Computación:** valores propios con NumPy.

**Extensión estimada:** 32–38 páginas; 40–50 ejercicios.

### Capítulo 10. Teorema espectral y formas cuadráticas

**Prerrequisitos:** L6 §9.1, L6 §9.2, L6 §9.3, L6 c. 7.

**Objetivos:** demostrar que las matrices simétricas reales tienen valores propios reales y vectores propios ortogonales; demostrar el teorema espectral; clasificar formas cuadráticas; caracterizar las matrices definidas positivas por valores propios y por la existencia de la factorización de Cholesky; acotar formas cuadráticas mediante el cociente de Rayleigh; construir la raíz cuadrada de una matriz semidefinida.

**Secciones:**

- **10.1** Matrices simétricas: valores propios reales y vectores propios ortogonales.
- **10.2** Teorema espectral.
- **10.3** Formas cuadráticas y su clasificación.
- **10.4** Matrices definidas positivas: criterios y factorización de Cholesky.
- **10.5** Cociente de Rayleigh y valores propios extremos.
- **10.6** Raíz cuadrada de una matriz semidefinida positiva.

**Resultados principales:** teorema espectral; criterios de definición positiva; existencia y unicidad de la factorización de Cholesky.

**Resultados admitidos:** RA-07 (a través de §9.2).

**Aplicaciones financieras:** formas cuadráticas como anticipo de la varianza de una cartera (L8 c. 7).

**Computación:** verificación numérica de definición positiva.

**Extensión estimada:** 28–34 páginas; 35–45 ejercicios.

### Capítulo 11. Descomposición en valores singulares y componentes principales

**Prerrequisitos:** L6 c. 8, L6 c. 10.

**Objetivos:** demostrar la existencia de la descomposición en valores singulares; interpretarla geométricamente; demostrar el teorema de Eckart-Young; calcular la pseudoinversa y su relación con los mínimos cuadrados; plantear las componentes principales de una matriz de datos como problema algebraico; describir los movimientos de una curva de tasas mediante componentes principales.

**Secciones:**

- **11.1** Existencia de la descomposición en valores singulares.
- **11.2** Interpretación geométrica.
- **11.3** Aproximación de rango bajo: teorema de Eckart-Young.
- **11.4** Pseudoinversa y mínimos cuadrados.
- **11.5** Componentes principales como problema algebraico sobre una matriz de datos centrada.
- **11.6** Aplicación: nivel, pendiente y curvatura en los cambios de una curva de tasas.

**Resultados principales:** existencia de la descomposición en valores singulares; teorema de Eckart-Young.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** componentes principales de curvas de tasas (datos por verificar en la entrega 1e).

**Usa como aplicación:** L5 §10.1.

**Computación:** descomposición en valores singulares y componentes principales con NumPy.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 12. Álgebra lineal numérica

**Prerrequisitos:** L6 §2.6, L6 §7.5, L6 §10.4, L6 c. 11, L3 c. 2, L3 c. 8, L1 c. 9.

**Objetivos:** definir normas vectoriales y matriciales; demostrar la cota de sensibilidad de un sistema lineal mediante el número de condición; explicar el pivoteo parcial; analizar la factorización de Cholesky; comparar ecuaciones normales, QR y descomposición en valores singulares para mínimos cuadrados; usar correctamente las funciones de biblioteca.

**Secciones:**

- **12.1** Normas vectoriales y matriciales.
- **12.2** Número de condición y sensibilidad de los sistemas lineales.
- **12.3** Estabilidad de la eliminación y pivoteo parcial.
- **12.4** Factorización de Cholesky: algoritmo y estabilidad.
- **12.5** Mínimos cuadrados: ecuaciones normales, QR y descomposición en valores singulares desde el punto de vista numérico.
- **12.6** Qué hacen las funciones de NumPy y SciPy; por qué no se invierte explícitamente una matriz.

**Resultados principales:** cota de perturbación de sistemas lineales; número de condición de las ecuaciones normales.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** sensibilidad de una cartera de replicación a errores en los datos.

**Computación:** todo el capítulo.

**Extensión estimada:** 26–32 páginas; 30–40 ejercicios.

### Capítulo 13. Aplicaciones a mercados de escenarios y carteras

**Prerrequisitos:** L6 c. 5, L6 c. 8, L6 c. 10, L6 c. 12.

**Objetivos:** representar un mercado de escenarios mediante su matriz de pagos; replicar un pago resolviendo un sistema lineal; caracterizar la completitud del mercado por el rango; describir los precios de estado como funcional lineal (la positividad por ausencia de arbitraje se estudia en L10 c. 8); representar restricciones de cartera; demostrar que la matriz de covarianza muestral es semidefinida positiva; plantear la inmunización con varios bonos como sistema lineal.

**Secciones:**

- **13.1** Mercados de escenarios: matriz de pagos y replicación.
- **13.2** Completitud del mercado como condición de rango.
- **13.3** Precios de estado como funcional lineal de precios.
- **13.4** Carteras como vectores: restricciones presupuestarias y exposiciones.
- **13.5** Matriz de covarianza muestral como objeto descriptivo; semidefinición positiva.
- **13.6** Inmunización con varios bonos como sistema lineal.

**Resultados principales:** caracterización de la completitud por el rango; semidefinición positiva de la covarianza muestral.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Usa como aplicación:** L5 §9.5, L5 §10.1.

**Computación:** replicación y covarianzas muestrales con NumPy.

**Extensión estimada:** 24–30 páginas; 30–40 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
