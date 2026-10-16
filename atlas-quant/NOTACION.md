# Convenciones de notación de Atlas Quant

Versión 1.3 · Entrega 1d · 2026-10-16

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
| o(·), O(·) | Notaciones de Landau | O(·) se define en L3 §5.3 para algoritmos; o(·) en L4 §4.7 |
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
| $\mathrm{VaR}_\alpha$, $\mathrm{ES}_\alpha$ | Valor en riesgo y Expected Shortfall al nivel α | Definidos sobre la pérdida L, con α nivel de confianza (por ejemplo, α = 0,99); L17 §6.2 |

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

## 11. Primera aparición de los símbolos en L1–L8

Lugar donde cada símbolo se define por primera vez en la colección. Cada libro lo vuelve a definir en su primera aparición propia (principio 2 de la sección 1).

| Símbolo | Primera aparición |
|---|---|
| := | L1 §1.2 |
| ¬, ∧, ∨ | L1 §2.1 |
| ⇒, ⇔ | L1 §2.3 |
| ∀, ∃ | L1 §2.5 |
| ∃! | L1 §4.5 |
| ∈, ⊆, ⊊ | L1 §3.1 |
| ∪, ∩, ∖, Aᶜ, ∅ | L1 §3.2 |
| A × B | L1 §3.3 |
| f: A → B, f ∘ g | L1 §3.6 |
| f⁻¹ | L1 §3.7 |
| \|A\| | L1 §3.8\* y L8 §2.1 |
| ℕ, ℕ₀ | L1 §5.1 |
| ℤ | L1 §5.2 |
| ℚ | L1 §6.1 |
| ℝ | L1 §7.2 |
| \|x\| | L1 §7.3 |
| Intervalos | L1 §7.4 |
| sup A, inf A | L1 §7.5 |
| $\log_b x$ | L1 §8.9 |
| ⌊x⌋ | L2 §1.6 |
| lim (sucesiones) | L2 §7.2 |
| e, eˣ | L2 §7.8 y L2 §8.2 |
| ln x | L2 §8.3 |
| ‖·‖ | L2 §11.3 |
| ℂ, unidad imaginaria i | L2 §12.1 |
| O(·) | L3 §5.3 |
| lim sup, lim inf | L4 §1.5 |
| f′, f″ | L4 §4.2 |
| df/dx, o(·) | L4 §4.7 |
| ∫ₐᵇ f(x) dx | L4 §8.2 |
| exp(x) | L4 §10.3 |
| $C^k(A)$ | L4 §13.1 |
| Negritas para vectores y matrices | L6, preliminares |
| **A**⁻¹ | L6 §2.4 |
| **A**ᵀ | L6 §2.5 |
| rg **A** | L6 §4.4 |
| ker **A**, im **A** | L6 §5.3 |
| det **A** | L6 §6.2 |
| ⟨·, ·⟩ (general) | L6 §7.1 |
| λ, tr **A** | L6 §9.1 |
| **A** ≻ 0, **A** ⪰ 0 | L6 §10.4 |
| ∂f/∂xᵢ | L7 §3.1 |
| ∇f | L7 §3.4 |
| D f | L7 §3.5 |
| ∇²f | L7 §5.2 |
| (Ω, ℱ, ℙ), ℙ(A) | L8 §1.2 |
| $p_X$, $F_X$ | L8 §4.1 y L8 §4.2 |
| 𝔼[X] | L8 §4.3 |
| $\mathbb{1}_A$ | L8 §4.4 |
| $f_X$ | L8 §5.1 |
| N(μ, σ²), Φ, φ | L8 §5.5 |
| Var(X) | L8 §6.3 |
| Cov(X, Y), Corr(X, Y) | L8 §7.4 |
| N(**μ**, **Σ**) | L8 §7.6 |
| 𝔼[X \| Y] | L8 §9.2 |
| i.i.d. | L8 §10.1 |
| →ᴾ, →ᵈ | L8 §10.2 |
| i (tasa de interés) | L1 §6.8 |
| C₀, Cₙ | L1 §8.10 |
| VP, VF | L2 §6.6 |
| d | L2 §4.5 |
| v | L2 §3.5 |
| K, función de pago | L2 §1.7 |
| $S_t$, $R_t$, $r_t$ | L2 §8.7 |
| δ | L4 §10.9 |
| i⁽ᵐ⁾ | L5 §2.2 |
| VPN, TIR | L5 §6.1 |
| y | L5 §8.3 |
| D, C (duración, convexidad) | L5 §9.2 y L5 §9.3 |
| P(t, T) | L5 §10.1 |
| **w** (pesos de cartera) | L6 §13.4 |
| **μ**, **Σ** | L7 §11.2 (forma algebraica) y L8 §7.5 (probabilística) |

## 12. Primera aparición de los símbolos en L9–L16

| Símbolo | Primera aparición |
|---|---|
| X̄, S² (estadísticos muestrales) | L9 §1.2 |
| θ, θ̂ | L9 §2.1 y L9 §2.2 |
| L(θ), ℓ(θ) | L9 §4.2 |
| I(θ) | L9 §4.4 |
| H₀, H₁, α | L9 §6.1 |
| **β** (coeficientes de regresión), ε | L9 §8.1 |
| $r_f$ | L10 §4.3 |
| β (beta de un activo) | L10 §7.2 |
| ℚ (medida neutral al riesgo) | L10 §8.5 |
| m (factor de descuento estocástico) | L10 §9.1 |
| ℓ^p | L11 §8.1 |
| τ (tiempo de parada) | L12 §11.5 |
| K, T, q | L13 §1.2 y L13 §3.1 |
| $V_t$, $C_t$, $P_t$ | L13 §3.1 |
| Δ | L13 §4.2 |
| $B_t$ | L13 §5.2 |
| σ (volatilidad) | L13 §8.1 |
| Γ | L13 §7.3 |
| $L^p$ | L16 §4.1 |
| →ᶜ·ˢ· | L16 §7.1 |
| 𝔼[X \| 𝒢] | L16 §9.1 |
| (ℱₜ) | L16 §10.1 |

## 13. Primera aparición de los símbolos en L17–L23

| Símbolo | Primera aparición |
|---|---|
| L (pérdida), $\mathrm{VaR}_\alpha$ | L17 §6.2 |
| $\mathrm{ES}_\alpha$ | L17 §6.4 |
| $N_t$ (proceso de Poisson) | L18 §2.1 |
| $W_t$ | L18 §3.1 |
| ∫ H dW (integral de Itô) | L18 §5.2 |
| ⟨X⟩ₜ, ⟨X, Y⟩ₜ (variación y covariación cuadráticas) | L18 §5.4 y L18 §6.4 |
| r (tasa corta en tiempo continuo) | L19 §1.1 |
| ν, Θ, ρ (griegas) | L19 §5.1 |

