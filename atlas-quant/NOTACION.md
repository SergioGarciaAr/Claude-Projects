# Convenciones de notación de Atlas Quant

Versión 1.0 · Fase 1a · 2026-10-15

Este documento fija la notación común a toda la colección. Cada libro introduce los símbolos gradualmente, en el capítulo donde se necesitan, y su índice de símbolos remite a ese lugar. Las entregas 1b a 1d completarán, para cada símbolo, la columna «primera aparición». Un símbolo fijado aquí no se redefine en otro sentido sin advertencia explícita y sin registrar la excepción.

## 1. Principios

1. Se introduce la notación más simple que permita expresar el contenido con precisión; nunca se usa notación sofisticada para aparentar profundidad.
2. Cada símbolo se define en el texto en su primera aparición en cada libro, aunque ya se haya definido en un libro anterior.
3. Cuando la literatura usa notaciones distintas para un mismo objeto, se adopta una y se mencionan las alternativas en una observación.
4. Las colisiones inevitables entre áreas se resuelven por contexto declarado: cada libro indica en su sección de notación qué convención usa.

## 2. Lógica y conjuntos

| Símbolo | Significado | Observaciones |
|---|---|---|
| ¬p, p ∧ q, p ∨ q | Negación, conjunción, disyunción | |
| p ⇒ q, p ⇔ q | Implicación, equivalencia | |
| ∀, ∃, ∃! | Para todo, existe, existe un único | |
| := | Igual por definición | El lado definido va a la izquierda |
| ∈, ∉ | Pertenencia | |
| A ⊆ B, A ⊊ B | Inclusión, inclusión estricta | No se usa ⊂ para evitar ambigüedad |
| A ∪ B, A ∩ B, A ∖ B, Aᶜ | Unión, intersección, diferencia, complemento | |
| A × B | Producto cartesiano | |
| ∅ | Conjunto vacío | |
| \|A\| | Cardinal de un conjunto finito | |
| $\mathbb{1}_A$ | Función indicadora de A | |

## 3. Conjuntos numéricos

| Símbolo | Significado | Observaciones |
|---|---|---|
| ℕ | {1, 2, 3, …} | El cero **no** pertenece a ℕ |
| ℕ₀ | {0, 1, 2, …} | |
| ℤ, ℚ, ℝ, ℂ | Enteros, racionales, reales, complejos | |
| ℝ₊, ℝ₊₊ | [0, ∞) y (0, ∞) | |
| [a, b], (a, b), [a, b), (a, b] | Intervalos | Con valores numéricos: [0; 1], (0,5; 1,2) |
| \|x\| | Valor absoluto | |
| ⌊x⌋, ⌈x⌉ | Parte entera inferior y superior | |
| sup A, inf A | Supremo e ínfimo | |
| i | Unidad imaginaria | En L5 y libros financieros *i* es la tasa efectiva; en esos libros la unidad imaginaria se escribe con letra recta **i** y se advierte (véase la sección 9) |

## 4. Funciones y análisis

| Símbolo | Significado | Observaciones |
|---|---|---|
| f: A → B | Función de A en B | |
| f ∘ g | Composición | |
| f⁻¹ | Función inversa | Nunca significa 1/f |
| ln x | Logaritmo natural | Se usa siempre ln; no se escribe log sin base |
| $\log_b x$ | Logaritmo en base b | log₁₀ se escribe con la base explícita |
| exp(x), eˣ | Función exponencial | exp se prefiere con argumentos largos |
| lim, lim sup, lim inf | Límites | |
| f′, f″, f⁽ⁿ⁾ | Derivadas de una variable | |
| df/dx | Notación de Leibniz | |
| ∂f/∂xᵢ | Derivada parcial | |
| ∇f | Gradiente (vector columna) | |
| ∇²f | Matriz hessiana | |
| D f | Matriz jacobiana | |
| ∫ₐᵇ f(x) dx | Integral | |
| $C^k(A)$ | Funciones k veces continuamente diferenciables en A | |
| o(·), O(·) | Notaciones de Landau | Se definen en L4 |
| ‖·‖ | Norma | Se indica cuál cuando hay ambigüedad |
| ⟨·, ·⟩ | Producto interno | |

## 5. Álgebra lineal

| Símbolo | Significado | Observaciones |
|---|---|---|
| **x**, **y** | Vectores (negrita minúscula), columnas por defecto | En L1–L2 se introducen sin negrita y se advierte el cambio en L6 |
| **A**, **B** | Matrices (negrita mayúscula) | |
| **A**ᵀ | Transpuesta | |
| **A**⁻¹ | Inversa | |
| **I**ₙ, **I** | Matriz identidad | |
| **0**, **1** | Vector de ceros, vector de unos | |
| det **A**, tr **A**, rg **A** | Determinante, traza, rango | |
| ker **A**, im **A** | Núcleo e imagen | |
| **A** ≻ 0, **A** ⪰ 0 | Definida positiva, semidefinida positiva | |
| λ | Valor propio | |
| $\mathbb{R}^n$, $\mathbb{R}^{m\times n}$ | Vectores y matrices reales | |

## 6. Probabilidad

| Símbolo | Significado | Observaciones |
|---|---|---|
| (Ω, ℱ, ℙ) | Espacio de probabilidad | En L8 se presenta sin teoría de la medida |
| ℙ(A) | Probabilidad de A | |
| X, Y, Z | Variables aleatorias (mayúsculas) | |
| x, y, z | Valores observados (minúsculas) | |
| $F_X$, $f_X$, $p_X$ | Función de distribución, densidad, función de masa | |
| 𝔼[X], Var(X), Cov(X, Y), Corr(X, Y) | Esperanza, varianza, covarianza, correlación | |
| 𝔼[X \| Y], 𝔼[X \| 𝒢] | Esperanza condicional | La segunda forma desde L16 |
| X ~ N(μ, σ²) | Distribución normal con media μ y **varianza** σ² | Nunca con la desviación estándar como segundo parámetro |
| N(**μ**, **Σ**) | Normal multivariante | |
| Φ, φ | Función de distribución y densidad normal estándar | |
| →ᴾ, →ᵈ, →ᶜ·ˢ· | Convergencia en probabilidad, en distribución, casi segura | |
| i.i.d. | Independientes e idénticamente distribuidas | |
| (ℱₜ) | Filtración | |
| $W_t$ | Movimiento browniano | Se usa W, no B |
| $N_t$ | Proceso de Poisson | |
| ℚ | Medida neutral al riesgo | Colisión con el conjunto de racionales resuelta por contexto (véase la sección 9) |

## 7. Estadística

| Símbolo | Significado |
|---|---|
| θ, **θ** | Parámetro |
| θ̂ | Estimador de θ |
| n | Tamaño muestral |
| X̄ | Media muestral |
| S² | Varianza muestral con divisor n − 1 |
| L(θ), ℓ(θ) | Verosimilitud y log-verosimilitud |
| I(θ) | Información de Fisher |
| H₀, H₁ | Hipótesis nula y alternativa |
| α | Nivel de significación |
| **β** | Vector de coeficientes de regresión |
| ε | Perturbación aleatoria |

## 8. Finanzas

### 8.1 Matemática financiera (L5 y posteriores)

| Símbolo | Significado | Unidad |
|---|---|---|
| C₀, Cₙ | Capital inicial y capital en el período n | u. m. |
| i | Tasa efectiva por período | Fracción por período |
| i⁽ᵐ⁾ | Tasa nominal convertible m veces por período | Fracción por período |
| δ | Fuerza de interés (tasa continua) | Por unidad de tiempo |
| d | Tasa de descuento efectiva | Fracción por período |
| v | Factor de descuento, v = 1/(1 + i) | Adimensional |
| VP, VF | Valor presente y valor futuro | u. m. |
| VPN | Valor presente neto | u. m. |
| TIR | Tasa interna de retorno | Fracción por período |
| y | Rendimiento al vencimiento de un bono | Fracción por período |
| D, C | Duración y convexidad | Períodos; períodos al cuadrado |
| P(t, T) | Precio en t de un bono cupón cero que paga 1 en T | u. m. |

### 8.2 Mercados, carteras y riesgo

| Símbolo | Significado | Observaciones |
|---|---|---|
| $S_t$ | Precio de un activo con riesgo | |
| $R_t$ | Rendimiento simple en (t − 1, t] | |
| $r_t$ | Rendimiento logarítmico, $r_t = \ln(S_t / S_{t-1})$ | Solo en contextos empíricos (véase la sección 9) |
| $r_f$ | Tasa libre de riesgo en contextos empíricos y de un período | |
| **w** | Vector de pesos de cartera | |
| **μ**, **Σ** | Vector de rendimientos esperados y matriz de covarianzas | |
| β | Beta de un activo | Colisión con **β** de regresión resuelta por contexto |
| $\mathrm{VaR}_\alpha$, $\mathrm{ES}_\alpha$ | Valor en riesgo y Expected Shortfall al nivel α | La convención de α (cola o confianza) se fija en L17 c. 6 |

### 8.3 Derivados y tiempo continuo

| Símbolo | Significado | Observaciones |
|---|---|---|
| K | Precio de ejercicio | |
| T | Vencimiento | En años |
| t | Tiempo actual | |
| τ | Tiempo hasta el vencimiento, τ = T − t; tiempo de parada | El sentido se declara en cada caso |
| r | Tasa corta libre de riesgo en modelos de valoración | Continua, anual |
| σ | Volatilidad | Anual |
| μ | Deriva | Anual |
| q | Tasa de dividendo continua | |
| $B_t$ | Cuenta bancaria (numerario) | |
| $V_t$, $C_t$, $P_t$ | Valor de un derivado, de una opción de compra, de una opción de venta | $P_t$ no se confunde con P(t, T), que siempre lleva dos argumentos |
| Δ, Γ, ν, Θ, ρ | Griegas | ν (vega) se escribe con nu |

## 9. Colisiones de notación y su resolución

| Colisión | Resolución |
|---|---|
| i como unidad imaginaria y como tasa de interés | La unidad imaginaria se escribe con letra recta (i, `\mathrm{i}` en LaTeX) y la tasa en cursiva (*i*). Se advierte en L2 c. 12, L5 y L12 c. 12. |
| r como rendimiento logarítmico y como tasa libre de riesgo | En contextos empíricos (L9, L14, L17, L20, L21, L23), $r_t$ es rendimiento logarítmico y la tasa libre de riesgo es $r_f$. En modelos de valoración (L13, L18, L19, L22), r es la tasa libre de riesgo y los rendimientos logarítmicos se escriben $\ln(S_t / S_s)$. |
| ℚ como racionales y como medida | El sentido es inequívoco por contexto; se advierte en la primera aparición de la medida neutral al riesgo. |
| β de regresión y beta de un activo | Coinciden conceptualmente en el modelo de mercado; se explicita la relación en L10. |
| P precio de opción de venta y P(t, T) precio de bono | P(t, T) siempre lleva dos argumentos; la opción de venta se escribe $P_t$ o $P(t, S)$. |
| C capital y C convexidad | La convexidad solo aparece en L5 c. 9, donde el capital se escribe con subíndice. |
| τ tiempo hasta el vencimiento y tiempo de parada | El sentido se declara en cada capítulo. |

## 10. Convenciones tipográficas de las fórmulas

- Variables en cursiva; funciones con nombre propio (ln, exp, sen, cos, det, Var) en letra recta.
- El seno se escribe **sen** (no sin).
- Coma decimal en fórmulas con `{,}`; separador de millares con `\,`.
- Diferencial en las integrales con letra recta o cursiva de manera uniforme dentro de cada libro (se fijará en la prueba de composición).
