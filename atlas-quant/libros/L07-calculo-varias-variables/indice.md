# L7. Cálculo en varias variables y optimización

Índice detallado · Versión 1.0 · Entrega 1b · 2026-10-16

## Ficha editorial

- **Serie:** II. Matemática para las finanzas.
- **Requisitos:** L4, L6.
- **Capítulos:** 11, más un apéndice.
- **Extensión estimada:** 320–400 páginas.

**Propósito.** Este libro extiende el cálculo a funciones de varias variables y desarrolla la teoría de la optimización que usa toda la colección: condiciones de primer y segundo orden, convexidad, teorema de separación y lema de Farkas, multiplicadores de Lagrange, condiciones de Karush-Kuhn-Tucker y dualidad. Demuestra los teoremas de la función inversa y de la función implícita mediante contracciones en ℝⁿ, y desarrolla la integración múltiple necesaria para la probabilidad con densidades. La interpretación probabilística del problema de Markowitz se deja para L10; aquí se estudia su forma algebraica.

**Resultados con demostración parcial.** El teorema de cambio de variables en integrales múltiples se demuestra para transformaciones lineales y se admite en general (RA-08). La integral gaussiana se demuestra sin usar ese resultado.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro.

## Capítulos

### Capítulo 1. Topología de ℝⁿ

**Prerrequisitos:** L4 c. 1, L6 c. 7, L6 §12.1.

**Objetivos:** trabajar con distintas normas en ℝⁿ y demostrar desigualdades entre las normas usuales; estudiar la convergencia de sucesiones en ℝⁿ; demostrar la completitud de ℝⁿ; reconocer conjuntos abiertos, cerrados y compactos; demostrar Bolzano-Weierstrass en ℝⁿ y la caracterización de los compactos como cerrados y acotados.

**Secciones:**

- **1.1** Normas en ℝⁿ; desigualdades entre las normas 1, 2 e ∞.
- **1.2** Sucesiones en ℝⁿ; convergencia por coordenadas; completitud.
- **1.3** Abiertos, cerrados, interior, clausura y frontera.
- **1.4** Teorema de Bolzano-Weierstrass en ℝⁿ.
- **1.5** Conjuntos compactos: caracterización como cerrados y acotados (versión secuencial).
- **1.6** Conjuntos conexos por caminos.

**Resultados principales:** completitud de ℝⁿ; Bolzano-Weierstrass en ℝⁿ; caracterización de los compactos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** el conjunto de carteras factibles como conjunto compacto.

**Computación:** no corresponde.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 2. Límites y continuidad

**Prerrequisitos:** L7 c. 1, L4 c. 2, L4 c. 3.

**Objetivos:** estudiar límites de funciones de varias variables y demostrar su inexistencia mediante trayectorias; demostrar la continuidad de funciones construidas por operaciones; demostrar el teorema de Weierstrass y la continuidad uniforme en compactos; demostrar la continuidad de las funciones lineales y definir la norma de operador.

**Secciones:**

- **2.1** Funciones de ℝⁿ en ℝᵐ; conjuntos de nivel.
- **2.2** Límites; inexistencia mediante trayectorias.
- **2.3** Continuidad y operaciones.
- **2.4** Teorema de Weierstrass en compactos.
- **2.5** Continuidad uniforme en compactos.
- **2.6** Continuidad de las funciones lineales; norma de operador.

**Resultados principales:** teorema de Weierstrass en ℝⁿ; continuidad uniforme en compactos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** existencia de una cartera óptima en un conjunto compacto.

**Computación:** no corresponde.

**Extensión estimada:** 24–30 páginas; 30–40 ejercicios.

### Capítulo 3. Diferenciabilidad

**Prerrequisitos:** L7 c. 2, L6 c. 5, L4 c. 4.

**Objetivos:** calcular derivadas parciales y direccionales; definir la diferencial como aproximación lineal; demostrar que las derivadas parciales continuas implican diferenciabilidad; interpretar el gradiente; calcular matrices jacobianas; calcular sensibilidades de un valor respecto de varios factores.

**Secciones:**

- **3.1** Derivadas parciales y direccionales.
- **3.2** La diferencial como aproximación lineal.
- **3.3** Diferenciabilidad implica continuidad; derivadas parciales continuas implican diferenciabilidad.
- **3.4** El gradiente como dirección de máximo crecimiento.
- **3.5** Matriz jacobiana.
- **3.6** Sensibilidades de un bono respecto de varias tasas cero.

**Resultados principales:** criterio de diferenciabilidad por derivadas parciales continuas; propiedad extremal del gradiente.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** sensibilidades a tasas clave.

**Usa como aplicación:** L5 §10.1.

**Computación:** gradientes numéricos por diferencias finitas.

**Extensión estimada:** 28–34 páginas; 35–45 ejercicios.

### Capítulo 4. Regla de la cadena

**Prerrequisitos:** L7 c. 3, L4 §6.2.

**Objetivos:** demostrar la regla de la cadena general; aplicarla a curvas y cambios de coordenadas; demostrar el teorema del valor medio en varias variables y su forma de desigualdad; demostrar el teorema de Euler para funciones homogéneas.

**Secciones:**

- **4.1** Regla de la cadena general.
- **4.2** Casos particulares: composición con curvas y cambios de coordenadas.
- **4.3** Teorema del valor medio en varias variables; desigualdad del valor medio.
- **4.4** Funciones homogéneas y teorema de Euler.
- **4.5** Derivación implícita (justificada en L7 c. 8).

**Resultados principales:** regla de la cadena; desigualdad del valor medio; teorema de Euler.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** descomposición del riesgo por contribuciones mediante el teorema de Euler (anticipo de L17 c. 4).

**Computación:** no corresponde.

**Extensión estimada:** 22–28 páginas; 30–40 ejercicios.

### Capítulo 5. Teorema de Taylor y matriz hessiana

**Prerrequisitos:** L7 c. 4, L4 §13.2, L6 c. 10.

**Objetivos:** demostrar el teorema de Schwarz sobre derivadas cruzadas; calcular matrices hessianas; demostrar el teorema de Taylor de segundo orden con resto; relacionar la aproximación cuadrática con formas cuadráticas.

**Secciones:**

- **5.1** Derivadas de orden superior; teorema de Schwarz.
- **5.2** Matriz hessiana.
- **5.3** Teorema de Taylor de segundo orden con resto.
- **5.4** Aproximación cuadrática y formas cuadráticas.
- **5.5** Aproximación de segundo orden del valor de una posición respecto de varios factores.

**Resultados principales:** teorema de Schwarz; teorema de Taylor en varias variables.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** aproximaciones de segundo orden con varios factores.

**Computación:** hessianas numéricas.

**Extensión estimada:** 24–30 páginas; 30–40 ejercicios.

### Capítulo 6. Optimización sin restricciones

**Prerrequisitos:** L7 c. 5, L7 §2.4, L6 c. 8.

**Objetivos:** aplicar las condiciones necesarias de primer orden; demostrar las condiciones de segundo orden; clasificar puntos críticos; demostrar la existencia de óptimos globales mediante compacidad o coercividad; reformular los mínimos cuadrados como problema de optimización.

**Secciones:**

- **6.1** Extremos locales y globales; condición de primer orden.
- **6.2** Condiciones de segundo orden.
- **6.3** Puntos de silla.
- **6.4** Existencia de óptimos globales: compacidad y coercividad.
- **6.5** Mínimos cuadrados como problema de optimización.

**Resultados principales:** condiciones necesarias y suficientes de segundo orden; existencia de mínimos de funciones coercivas.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** ajuste de una curva de tasas por mínimos cuadrados.

**Computación:** no corresponde.

**Extensión estimada:** 24–30 páginas; 30–40 ejercicios.

### Capítulo 7. Convexidad, separación y lema de Farkas

**Prerrequisitos:** L7 c. 6, L7 c. 1, L6 c. 7, L6 c. 10, L4 §6.4.

**Objetivos:** reconocer conjuntos y funciones convexas; demostrar sus caracterizaciones de primer y segundo orden; demostrar que en problemas convexos los mínimos locales son globales; demostrar la existencia, unicidad y caracterización de la proyección sobre un convexo cerrado; demostrar el teorema de separación y el lema de Farkas; interpretar el lema de Farkas como teorema de alternativa.

**Secciones:**

- **7.1** Conjuntos convexos, combinaciones convexas y envoltura convexa.
- **7.2** Funciones convexas: caracterizaciones de primer y segundo orden.
- **7.3** Mínimos de funciones convexas: todo mínimo local es global; unicidad con convexidad estricta.
- **7.4** Proyección sobre un convexo cerrado: existencia, unicidad y caracterización.
- **7.5** Teorema de separación entre un punto y un convexo cerrado.
- **7.6** Conos finitamente generados: son cerrados; lema de Farkas.
- **7.7** Teoremas de alternativa; anticipo de su lectura como ausencia de arbitraje (L10 c. 8).

**Resultados principales:** caracterizaciones de la convexidad; teorema de la proyección; teorema de separación; clausura de los conos finitamente generados; lema de Farkas.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** teoremas de alternativa como forma matemática de la ausencia de arbitraje (anticipo).

**Computación:** no corresponde.

**Extensión estimada:** 30–36 páginas; 35–45 ejercicios.

### Capítulo 8. Funciones inversa e implícita; multiplicadores de Lagrange

**Prerrequisitos:** L7 c. 4, L7 §1.2, L7 §2.6, L6 c. 5.

**Objetivos:** demostrar el teorema del punto fijo para contracciones en subconjuntos cerrados de ℝⁿ; demostrar los teoremas de la función inversa y de la función implícita; describir el espacio tangente a una superficie de nivel; demostrar la condición necesaria de Lagrange y las condiciones de segundo orden con restricciones; interpretar los multiplicadores mediante el teorema de la envolvente.

**Secciones:**

- **8.1** Contracciones en subconjuntos cerrados de ℝⁿ; teorema del punto fijo.
- **8.2** Teorema de la función inversa.
- **8.3** Teorema de la función implícita.
- **8.4** Superficies de nivel y espacio tangente.
- **8.5** Multiplicadores de Lagrange: condición necesaria.
- **8.6** Condiciones de segundo orden con restricciones de igualdad.
- **8.7** Los multiplicadores como precios sombra; teorema de la envolvente.

**Resultados principales:** teorema del punto fijo en ℝⁿ; teoremas de la función inversa e implícita; teorema de Lagrange; condiciones de segundo orden; teorema de la envolvente.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** precio sombra de una restricción presupuestaria.

**Computación:** no corresponde.

**Extensión estimada:** 32–38 páginas; 35–45 ejercicios.

### Capítulo 9. Condiciones de Karush-Kuhn-Tucker y dualidad

**Prerrequisitos:** L7 c. 8, L7 c. 7.

**Objetivos:** plantear problemas con restricciones de desigualdad; demostrar el teorema de Karush-Kuhn-Tucker bajo la condición de independencia lineal de los gradientes activos; demostrar la suficiencia de las condiciones KKT en problemas convexos; construir el lagrangiano y el problema dual; demostrar la dualidad débil y, bajo la condición de Slater, la dualidad fuerte; aplicar la dualidad a la programación lineal.

**Secciones:**

- **9.1** Problemas con restricciones de desigualdad.
- **9.2** Restricciones activas, cono tangente y condiciones de calificación.
- **9.3** Teorema de Karush-Kuhn-Tucker.
- **9.4** Problemas convexos: suficiencia de las condiciones KKT.
- **9.5** Lagrangiano, problema dual y dualidad débil.
- **9.6\*** Dualidad fuerte bajo la condición de Slater.
- **9.7** Programación lineal y su dual.

**Resultados principales:** teorema de Karush-Kuhn-Tucker; suficiencia en problemas convexos; dualidad débil; dualidad fuerte bajo Slater.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** carteras con prohibición de ventas en corto; problemas de cobertura de mínimo costo como programas lineales.

**Computación:** resolución de programas lineales pequeños.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 10. Integrales múltiples

**Prerrequisitos:** L7 c. 2, L4 c. 8, L4 c. 9, L4 c. 11, L6 c. 6.

**Objetivos:** definir la integral de Riemann en rectángulos de ℝⁿ; demostrar la integrabilidad de funciones continuas y el teorema de Fubini para ellas; integrar en regiones no rectangulares; aplicar el teorema de cambio de variables (demostrado para transformaciones lineales); usar coordenadas polares; demostrar el valor de la integral gaussiana; calcular integrales impropias múltiples.

**Secciones:**

- **10.1** Integral de Riemann en rectángulos.
- **10.2** Integrabilidad de las funciones continuas.
- **10.3** Teorema de Fubini para funciones continuas en rectángulos.
- **10.4** Integración en regiones no rectangulares.
- **10.5** Cambio de variables: demostración para transformaciones lineales; enunciado general.
- **10.6** Coordenadas polares; la integral gaussiana ∫ e^(−x²) dx = √π, demostrada mediante Fubini y una sustitución en una variable, sin usar el cambio de variables general.
- **10.7** Integrales impropias múltiples de funciones no negativas.
- **10.8** Volúmenes y promedios; preparación para densidades conjuntas.

**Resultados principales:** teorema de Fubini para funciones continuas; cambio de variables lineal; valor de la integral gaussiana.

**Resultados admitidos:** RA-08 (en §10.5, para transformaciones no lineales).

**Aplicaciones financieras:** no corresponde.

**Computación:** integración numérica en dos dimensiones.

**Extensión estimada:** 30–36 páginas; 35–45 ejercicios.

### Capítulo 11. Optimización cuadrática y utilidad determinista

**Prerrequisitos:** L7 c. 8, L7 c. 9, L6 c. 10.

**Objetivos:** resolver problemas cuadráticos con restricciones lineales de igualdad mediante el sistema KKT; resolver la forma algebraica del problema de Markowitz con matriz definida positiva dada y describir la geometría de su solución; caracterizar soluciones con restricciones de desigualdad; resolver problemas de maximización de utilidad con restricción presupuestaria; aplicar el teorema de la envolvente.

**Secciones:**

- **11.1** Problemas cuadráticos con restricciones lineales de igualdad: solución cerrada.
- **11.2** Forma algebraica del problema de Markowitz: minimizar **w**ᵀ**Σ****w** sujeto a **w**ᵀ**μ** = m y **w**ᵀ**1** = 1, con **Σ** y **μ** dados; la solución como hipérbola. La interpretación probabilística está en L10 c. 6.
- **11.3** Restricciones de desigualdad: caracterización mediante KKT.
- **11.4** Maximización de la utilidad con restricción presupuestaria.
- **11.5** Estática comparativa mediante el teorema de la envolvente.
- **11.6** Resolución numérica básica.

**Resultados principales:** solución cerrada del problema cuadrático con restricciones de igualdad.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** forma algebraica del problema de Markowitz; elección del consumidor.

**Computación:** resolución numérica de problemas cuadráticos.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
