# L4. Cálculo en una variable

Índice detallado · Versión 1.0 · Entrega 1b · 2026-10-16

## Ficha editorial

- **Serie:** I. Fundamentos.
- **Requisitos:** L2, L3 (y L1 a través de L2).
- **Capítulos:** 14, más un apéndice.
- **Extensión estimada:** 420–500 páginas.

**Propósito.** Este libro desarrolla el cálculo diferencial e integral de una variable con demostraciones completas, desde la completitud de los reales hasta las series de Taylor. Cierra los resultados admitidos de L1 y L2 sobre exponenciales, logaritmos y funciones trigonométricas, construyendo el logaritmo como integral y el seno y el coseno como series. Las aplicaciones financieras incluyen la optimización, la capitalización continua, el valor presente de flujos continuos, las perpetuidades y las aproximaciones de primer y segundo orden que preparan la duración y la convexidad de L5.

**Orden lógico de la exponencial.** Los capítulos 4 a 9 usan la exponencial y el logaritmo solo en ejemplos, como resultados admitidos (RA-02, RA-03, RA-06). Ninguna demostración de esos capítulos depende de ellos. El capítulo 10 los construye usando únicamente resultados de los capítulos 1 a 9.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro.

## Capítulos

### Capítulo 1. Completitud y sucesiones

**Prerrequisitos:** L1 §7.5, L1 §7.6, L1 §7.7, L2 c. 7.

**Objetivos:** extraer subsucesiones y demostrar el teorema de Bolzano-Weierstrass; demostrar que una sucesión real converge si y solo si es de Cauchy; calcular límites superiores e inferiores; aplicar el principio de intervalos encajados.

**Secciones:**

- **1.1** Repaso: supremo, convergencia y convergencia monótona (L2 §7.6).
- **1.2** Subsucesiones.
- **1.3** Teorema de Bolzano-Weierstrass.
- **1.4** Sucesiones de Cauchy y completitud.
- **1.5** Límite superior y límite inferior.
- **1.6** Intervalos encajados.

**Resultados principales:** teorema de Bolzano-Weierstrass; criterio de Cauchy; principio de intervalos encajados.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** no corresponde.

**Extensión estimada:** 28–34 páginas; 40–50 ejercicios.

### Capítulo 2. Límites de funciones

**Prerrequisitos:** L4 c. 1, L1 §2.6, L2 c. 1, L2 c. 4, L2 c. 10.

**Objetivos:** aplicar la definición ε-δ; caracterizar límites mediante sucesiones; demostrar el álgebra de límites de funciones; calcular límites laterales, infinitos y en el infinito; demostrar que sen x / x → 1.

**Secciones:**

- **2.1** Definición ε-δ.
- **2.2** Caracterización mediante sucesiones.
- **2.3** Álgebra de límites.
- **2.4** Límites laterales.
- **2.5** Límites infinitos y en el infinito; revisión rigurosa de las asíntotas de L2 c. 4.
- **2.6** Límites fundamentales; sen x / x → 1 mediante el argumento geométrico de áreas.

**Resultados principales:** equivalencia entre la definición ε-δ y la caracterización por sucesiones; límite de sen x / x.

**Resultados admitidos:** RA-22 (en §2.6).

**Aplicaciones financieras:** no corresponde.

**Computación:** no corresponde.

**Extensión estimada:** 28–34 páginas; 40–55 ejercicios.

### Capítulo 3. Continuidad

**Prerrequisitos:** L4 c. 2, L4 §1.3.

**Objetivos:** demostrar la continuidad de funciones construidas por operaciones; demostrar los teoremas de Bolzano y de Weierstrass; implementar el método de bisección con cota del error; demostrar el teorema de Heine sobre continuidad uniforme; demostrar la continuidad de la inversa de una función continua estrictamente monótona.

**Secciones:**

- **3.1** Definición de continuidad y ejemplos.
- **3.2** Operaciones con funciones continuas; continuidad de polinomios, funciones racionales y raíces.
- **3.3** Teorema de Bolzano (valores intermedios).
- **3.4** Método de bisección: convergencia y cota del error.
- **3.5** Teorema de Weierstrass sobre extremos.
- **3.6** Continuidad uniforme; teorema de Heine.
- **3.7** Continuidad de la función inversa; nueva demostración de la existencia de raíces n-ésimas.
- **3.8** Discontinuidades y funciones monótonas.

**Resultados principales:** teoremas de Bolzano, Weierstrass y Heine; continuidad de la inversa.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** existencia de una tasa que iguala dos valores (anticipo de la TIR).

**Computación:** bisección en Python (L3 c. 3).

**Extensión estimada:** 30–36 páginas; 40–55 ejercicios.

### Capítulo 4. La derivada

**Prerrequisitos:** L4 c. 2, L4 c. 3.

**Objetivos:** definir la derivada como límite del cociente incremental; demostrar que la diferenciabilidad implica continuidad; demostrar las reglas de derivación de sumas, productos y cocientes; derivar polinomios, potencias enteras, raíces, seno y coseno; usar la aproximación lineal.

**Secciones:**

- **4.1** Tasa de cambio media e instantánea; recta tangente.
- **4.2** Definición de derivada; diferenciabilidad implica continuidad.
- **4.3** Reglas de la suma, el producto y el cociente.
- **4.4** Derivadas de polinomios, potencias enteras y raíces.
- **4.5** Derivadas del seno y del coseno.
- **4.6** Sensibilidad de un valor presente a la tasa de interés (anticipo de la duración).
- **4.7** Aproximación lineal y diferencial.

**Resultados principales:** reglas de derivación; derivadas de las funciones elementales algebraicas y trigonométricas.

**Resultados admitidos:** RA-06 (solo en ejemplos), RA-22.

**Aplicaciones financieras:** sensibilidad del valor de un flujo a la tasa.

**Computación:** no corresponde.

**Extensión estimada:** 28–34 páginas; 45–60 ejercicios.

### Capítulo 5. Regla de la cadena, derivación implícita y derivada de la inversa

**Prerrequisitos:** L4 c. 4, L4 §3.7.

**Objetivos:** demostrar la regla de la cadena; demostrar el teorema de la derivada de la función inversa; derivar funciones trigonométricas inversas y potencias racionales; aplicar derivación implícita y tasas relacionadas.

**Secciones:**

- **5.1** Regla de la cadena.
- **5.2** Derivada de la función inversa.
- **5.3** Derivadas de funciones trigonométricas inversas y de potencias racionales.
- **5.4** Derivación implícita.
- **5.5** Tasas relacionadas.

**Resultados principales:** regla de la cadena; teorema de la derivada de la inversa.

**Resultados admitidos:** RA-06 (solo en ejemplos).

**Aplicaciones financieras:** no corresponde.

**Computación:** no corresponde.

**Extensión estimada:** 24–30 páginas; 40–50 ejercicios.

### Capítulo 6. Teorema del valor medio y consecuencias

**Prerrequisitos:** L4 c. 5, L4 §3.5.

**Objetivos:** demostrar los teoremas de Fermat, Rolle, del valor medio y del valor medio de Cauchy; relacionar el signo de la derivada con la monotonía; caracterizar la convexidad mediante derivadas y usarla para demostrar desigualdades; demostrar y aplicar la regla de L'Hôpital.

**Secciones:**

- **6.1** Extremos locales y teorema de Fermat.
- **6.2** Teorema de Rolle y teorema del valor medio.
- **6.3** Monotonía y signo de la derivada.
- **6.4** Funciones convexas: definición mediante cuerdas y caracterizaciones mediante derivadas; desigualdades por convexidad.
- **6.5** Teorema del valor medio de Cauchy y regla de L'Hôpital.

**Resultados principales:** teoremas de Rolle, del valor medio y de Cauchy; criterio de monotonía; caracterización de la convexidad; regla de L'Hôpital.

**Resultados admitidos:** RA-06 (solo en ejemplos).

**Aplicaciones financieras:** convexidad de funciones de valor (anticipo de L5 c. 9).

**Computación:** no corresponde.

**Extensión estimada:** 28–34 páginas; 40–55 ejercicios.

### Capítulo 7. Optimización y método de Newton

**Prerrequisitos:** L4 c. 6, L3 c. 3.

**Objetivos:** hallar extremos absolutos en intervalos cerrados; aplicar el criterio de la segunda derivada; modelar y resolver problemas de optimización económicos y financieros; derivar el método de Newton, demostrar su convergencia cuadrática local bajo hipótesis explícitas e identificar sus fallos; implementarlo con un criterio de parada.

**Secciones:**

- **7.1** Extremos absolutos en intervalos cerrados.
- **7.2** Criterio de la segunda derivada.
- **7.3** Modelización de problemas de optimización.
- **7.4** Aplicaciones económicas y financieras.
- **7.5** Método de Newton: derivación, convergencia cuadrática local y fallos.
- **7.6** Implementación en Python y criterios de parada.

**Resultados principales:** criterio de la segunda derivada; teorema de convergencia local del método de Newton.

**Resultados admitidos:** RA-06 (solo en ejemplos).

**Aplicaciones financieras:** maximización de beneficios; tamaño óptimo de un pedido o de un lote.

**Computación:** método de Newton en Python.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 8. La integral de Riemann

**Prerrequisitos:** L4 c. 1, L4 §3.6.

**Objetivos:** definir la integral mediante sumas superiores e inferiores; demostrar la integrabilidad de funciones continuas y monótonas; demostrar las propiedades de la integral; aplicar el teorema del valor medio para integrales; exhibir una función acotada no integrable.

**Secciones:**

- **8.1** Área y sumas de Riemann.
- **8.2** Sumas superiores e inferiores; definición de integrabilidad.
- **8.3** Integrabilidad de funciones continuas y de funciones monótonas.
- **8.4** Linealidad, monotonía y aditividad de la integral.
- **8.5** Teorema del valor medio para integrales.
- **8.6** Una función acotada no integrable.

**Resultados principales:** criterio de integrabilidad de Riemann; integrabilidad de funciones continuas y monótonas; propiedades de la integral.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** acumulación de un flujo de pagos continuo (anticipo).

**Computación:** no corresponde.

**Extensión estimada:** 30–36 páginas; 35–45 ejercicios.

### Capítulo 9. Teorema fundamental del cálculo y técnicas de integración

**Prerrequisitos:** L4 c. 8, L4 c. 5, L4 c. 6, L1 §10.4.

**Objetivos:** demostrar los dos teoremas fundamentales del cálculo; calcular primitivas; aplicar sustitución, integración por partes y fracciones parciales; calcular integrales trigonométricas básicas; demostrar la fórmula de la longitud de arco (sección opcional).

**Secciones:**

- **9.1** Primer teorema fundamental: derivada de la integral con límite variable.
- **9.2** Segundo teorema fundamental: cálculo de integrales mediante primitivas.
- **9.3** Primitivas.
- **9.4** Integración por sustitución.
- **9.5** Integración por partes.
- **9.6** Fracciones parciales.
- **9.7** Integrales trigonométricas básicas.
- **9.8\*** Longitud de arco de una gráfica: definición como supremo de longitudes poligonales y fórmula integral.

**Resultados principales:** teoremas fundamentales del cálculo; fórmulas de sustitución y de integración por partes; fórmula de la longitud de arco.

**Resultados admitidos:** RA-06 (solo en ejemplos).

**Aplicaciones financieras:** valor acumulado de un flujo continuo con tasa constante.

**Computación:** no corresponde.

**Extensión estimada:** 30–36 páginas; 50–65 ejercicios.

### Capítulo 10. Construcción rigurosa del logaritmo y la exponencial

**Prerrequisitos:** L4 c. 1, L4 §3.3, L4 §3.7, L4 §5.2, L4 §6.3, L4 §6.4, L4 §9.1, L4 §9.4, L1 §8.5, L1 §8.9, L2 §7.8.

**Objetivos:** definir el logaritmo natural como integral y demostrar sus propiedades; construir la exponencial como su inversa; definir las potencias de exponente real y demostrar que extienden las de exponente racional; demostrar que exp(1) coincide con el *e* de L2 y que (1 + x/n)ⁿ → eˣ; derivar exponenciales, logaritmos y potencias reales; demostrar desigualdades exponenciales y logarítmicas; formular la capitalización continua.

**Secciones:**

- **10.1** El logaritmo natural: ln x = ∫₁ˣ dt/t; propiedad ln(xy) = ln x + ln y.
- **10.2** El logaritmo es una biyección de (0, ∞) en ℝ.
- **10.3** La exponencial como inversa del logaritmo: exp′ = exp y exp(x + y) = exp x · exp y.
- **10.4** Potencias reales aˣ = exp(x ln a) y coherencia con las potencias racionales de L1 c. 8. Cierra RA-02 y RA-03.
- **10.5** exp(1) coincide con el límite de (1 + 1/n)ⁿ de L2 §7.8.
- **10.6** Límite (1 + x/n)ⁿ → eˣ para todo x real. Cierra RA-04.
- **10.7** Derivadas de aˣ, logₐ x y xʳ con r real. Cierra RA-06.
- **10.8** Desigualdades ln(1 + x) ≤ x y eˣ ≥ 1 + x. Cierra la primera parte de RA-05.
- **10.9** Capitalización continua y fuerza de interés constante.
- **10.10** Crecimiento comparado riguroso: xᵏ/eˣ → 0 y ln x / xᵏ → 0.

**Resultados principales:** propiedades del logaritmo y la exponencial; extensión coherente de las potencias; caracterización de *e*; límite de la capitalización.

**Resultados admitidos:** ninguno. El capítulo cierra RA-02, RA-03, RA-04, RA-06 y parte de RA-05.

**Aplicaciones financieras:** capitalización continua; equivalencia entre tasa efectiva y fuerza de interés.

**Computación:** comparación numérica entre capitalización discreta y continua.

**Extensión estimada:** 28–34 páginas; 40–55 ejercicios.

### Capítulo 11. Integrales impropias y función Gamma

**Prerrequisitos:** L4 c. 9, L4 c. 10.

**Objetivos:** definir y calcular integrales impropias de primera y segunda especie; aplicar criterios de comparación; calcular el valor presente de flujos continuos con horizonte infinito; definir la función Gamma y demostrar Γ(n + 1) = n!.

**Secciones:**

- **11.1** Integrales impropias de primera y segunda especie.
- **11.2** Criterios de comparación.
- **11.3** Valor presente de flujos continuos: ∫ c(t) e^(−δt) dt.
- **11.4** La función Gamma: definición, convergencia y relación con el factorial.
- **11.5\*** Integrales impropias condicionalmente convergentes: ∫ sen x / x dx.

**Resultados principales:** criterios de comparación; Γ(n + 1) = n!.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** valor presente de rentas continuas perpetuas y crecientes.

**Computación:** no corresponde.

**Extensión estimada:** 24–30 páginas; 30–40 ejercicios.

### Capítulo 12. Series numéricas

**Prerrequisitos:** L4 c. 1, L4 §11.2, L2 §7.7.

**Objetivos:** estudiar la convergencia de series mediante los criterios de comparación, del cociente, de la raíz y de la integral; distinguir convergencia absoluta y condicional; aplicar el criterio de Leibniz; valorar perpetuidades constantes y crecientes como series.

**Secciones:**

- **12.1** Series y sumas parciales.
- **12.2** Serie geométrica y perpetuidades: constante y con crecimiento geométrico.
- **12.3** Criterios para series de términos positivos: comparación, cociente, raíz e integral.
- **12.4** Convergencia absoluta y condicional; series alternadas.
- **12.5** Reordenamiento de series absolutamente convergentes.
- **12.6\*** Producto de Cauchy de series.

**Resultados principales:** criterios de convergencia; criterio de Leibniz; invariancia de la suma por reordenamiento bajo convergencia absoluta.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** perpetuidades constantes y crecientes; condición de convergencia del modelo de dividendos con crecimiento constante.

**Computación:** no corresponde.

**Extensión estimada:** 28–34 páginas; 40–55 ejercicios.

### Capítulo 13. Series de potencias y teorema de Taylor

**Prerrequisitos:** L4 c. 12, L4 c. 10, L4 c. 6, L4 §9.8, L2 c. 12.

**Objetivos:** demostrar el teorema de Taylor con resto de Lagrange e integral; acotar el error de aproximaciones de primer y segundo orden; calcular radios de convergencia; demostrar la derivación e integración término a término de series de potencias; definir seno y coseno mediante series y demostrar su coherencia con la definición geométrica; definir la exponencial compleja y demostrar la fórmula de Euler.

**Secciones:**

- **13.1** Polinomio de Taylor.
- **13.2** Teorema de Taylor con resto de Lagrange y resto integral.
- **13.3** Aproximaciones de primer y segundo orden y su error. Cota del error de la regla del 72; cierra RA-05.
- **13.4** Series de potencias y radio de convergencia.
- **13.5** Convergencia uniforme de series de potencias en intervalos cerrados interiores; derivación e integración término a término.
- **13.6** Series de la exponencial, seno, coseno y ln(1 + x).
- **13.7** Definición analítica de seno y coseno y coherencia con la definición geométrica (con L4 §9.8). Cierra RA-22.
- **13.8** Exponencial compleja y fórmula de Euler.

**Resultados principales:** teorema de Taylor; teorema de derivación término a término; fórmula de Euler.

**Resultados admitidos:** ninguno. El capítulo cierra RA-05 y RA-22.

**Aplicaciones financieras:** aproximaciones de primer y segundo orden del valor de un bono (anticipo de L5 c. 9); error de la regla del 72.

**Computación:** comparación numérica de aproximaciones de Taylor.

**Extensión estimada:** 30–36 páginas; 45–60 ejercicios.

### Capítulo 14. Derivación e integración numéricas

**Prerrequisitos:** L4 §8.4, L4 §13.2, L3 c. 2, L3 c. 8.

**Objetivos:** derivar fórmulas de diferencias finitas y su error de truncamiento; explicar el compromiso entre error de truncamiento y de redondeo y elegir el paso; demostrar las cotas de error de las reglas del trapecio y de Simpson; aplicar la extrapolación de Richardson; verificar numéricamente resultados analíticos.

**Secciones:**

- **14.1** Diferencias finitas hacia adelante y centradas; error de truncamiento mediante Taylor.
- **14.2** Error de redondeo y elección del paso.
- **14.3** Reglas del trapecio y de Simpson con cotas del error.
- **14.4** Extrapolación de Richardson.
- **14.5** Verificación numérica de resultados analíticos.

**Resultados principales:** cotas del error de truncamiento de las diferencias finitas y de las reglas de cuadratura.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** sensibilidades numéricas de un valor presente; integración numérica de flujos continuos.

**Computación:** todo el capítulo.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
