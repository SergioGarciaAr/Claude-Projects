# L5. Matemática financiera

Índice detallado · Versión 1.0 · Entrega 1b · 2026-10-16

## Ficha editorial

- **Serie:** II. Matemática para las finanzas.
- **Requisitos:** L3, L4.
- **Capítulos:** 11, más un apéndice.
- **Extensión estimada:** 290–360 páginas.

**Propósito.** Este libro desarrolla la teoría del interés y la valoración de flujos de caja ciertos: tasas, descuento, anualidades, amortización, valor presente neto y tasa interna de retorno, inflación, bonos, duración, convexidad y estructura temporal de tasas. Cada fórmula se deriva a partir de definiciones explícitas y se distinguen con cuidado los resultados matemáticos de las convenciones de mercado, que se presentan con su fuente y fecha de verificación. El libro no trata todavía el riesgo ni la incertidumbre: los flujos son ciertos, salvo menciones explícitas que anticipan libros posteriores.

**Rutas de lectura.** Ruta temprana opcional: los capítulos 1 a 3, 5 y 7 pueden leerse después de L2, omitiendo las secciones que usan continuidad, integrales o derivadas (L5 §1.7, L5 §2.4, L5 §2.5) y las secciones computacionales. El capítulo 8 requiere el capítulo 6, que usa L4.

**Convenciones de mercado.** Las convenciones de conteo de días, de cotización de bonos y de cálculo del interés corrido varían entre mercados y cambian con el tiempo. El libro las presenta como convenciones, con referencia a la fuente y fecha de verificación (se verificarán en la entrega 1e).

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro (notación actuarial de NOTACION §8.1).

## Capítulos

### Capítulo 1. Valor temporal del dinero; interés simple y compuesto

**Prerrequisitos:** L1 §6.8, L1 §8.7, L1 §8.10, L2 c. 6, L2 c. 8, L4 §3.1.

**Objetivos:** explicar las razones económicas del valor temporal del dinero; definir funciones de acumulación y de monto; calcular con interés simple y compuesto; demostrar cuándo el interés compuesto supera al simple; demostrar que la consistencia temporal caracteriza al interés compuesto entre las funciones de acumulación continuas.

**Secciones:**

- **1.1** Por qué el dinero tiene valor temporal: preferencia temporal, costo de oportunidad, inflación y riesgo.
- **1.2** Funciones de acumulación y de monto; propiedades exigidas.
- **1.3** Interés simple.
- **1.4** Interés compuesto.
- **1.5** Comparación entre interés simple y compuesto mediante la desigualdad de Bernoulli.
- **1.6** Tasa efectiva de un período.
- **1.7** Consistencia temporal: a(s + t) = a(s)·a(t) y la ecuación funcional de Cauchy para funciones continuas.

**Resultados principales:** caracterización del interés compuesto por la consistencia temporal.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** funciones de acumulación en Python.

**Extensión estimada:** 26–32 páginas; 40–50 ejercicios.

### Capítulo 2. Tasas nominales, efectivas, equivalentes y continuas

**Prerrequisitos:** L5 c. 1, L4 §9.2, L4 §10.6, L4 §10.9.

**Objetivos:** convertir entre tasas efectivas de distintos períodos, tasas nominales y tasas de descuento; derivar las relaciones entre i, d, v y δ; trabajar con fuerza de interés variable; aplicar convenciones de conteo de días; leer críticamente las tasas informadas en la práctica.

**Secciones:**

- **2.1** Tasas efectivas y equivalentes para distintos períodos.
- **2.2** Tasas nominales convertibles m veces por período.
- **2.3** Tasa de descuento efectiva y nominal; relaciones entre i, d y v.
- **2.4** Fuerza de interés constante y variable: a(t) = exp(∫₀ᵗ δ(s) ds).
- **2.5** El límite de las tasas nominales cuando m → ∞.
- **2.6** Convenciones de conteo de días: Actual/360, Actual/365, 30/360 y variantes (convenciones de mercado).
- **2.7** Tasas en la práctica: tasas anuales informadas y costo financiero total; diferencias regulatorias entre países.

**Resultados principales:** relaciones de equivalencia entre i, i⁽ᵐ⁾, d, d⁽ᵐ⁾ y δ; fórmula de acumulación con fuerza de interés variable.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** conversión de tasas y cálculo de fracciones de año.

**Extensión estimada:** 28–34 páginas; 45–55 ejercicios.

### Capítulo 3. Ecuación de valor y descuento

**Prerrequisitos:** L5 c. 2, L4 §3.4.

**Objetivos:** plantear y resolver ecuaciones de valor con distintas fechas focales; calcular valores presentes y futuros de flujos discretos; distinguir descuento racional y comercial; despejar plazos y tasas, incluidos los casos que requieren métodos numéricos; decidir la equivalencia de dos conjuntos de flujos.

**Secciones:**

- **3.1** Fecha focal y ecuación de valor; independencia del resultado respecto de la fecha focal bajo interés compuesto.
- **3.2** Valor presente y futuro de flujos discretos.
- **3.3** Descuento racional y descuento comercial.
- **3.4** Despeje de plazos y tasas; cuándo se necesita un método numérico.
- **3.5** Equivalencia de conjuntos de flujos.

**Resultados principales:** independencia de la ecuación de valor respecto de la fecha focal bajo interés compuesto, y su falla bajo interés simple.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** refinanciación de deudas; descuento de documentos.

**Computación:** resolución numérica de la tasa por bisección.

**Extensión estimada:** 22–28 páginas; 35–45 ejercicios.

### Capítulo 4. Anualidades y perpetuidades

**Prerrequisitos:** L5 c. 3, L2 §6.6, L4 §11.3, L4 §12.2, L4 §3.3.

**Objetivos:** derivar el valor presente y futuro de anualidades vencidas, anticipadas, diferidas, con período de pago distinto del de capitalización, crecientes y continuas; valorar perpetuidades constantes y crecientes y explicar su condición de convergencia; demostrar la existencia y unicidad de la tasa de una anualidad y calcularla numéricamente.

**Secciones:**

- **4.1** Anualidades vencidas y anticipadas.
- **4.2** Anualidades diferidas.
- **4.3** Anualidades con período de pago distinto del de capitalización.
- **4.4** Anualidades crecientes aritméticas y geométricas.
- **4.5** Perpetuidades constantes y crecientes.
- **4.6** Anualidades continuas.
- **4.7** La tasa de una anualidad: existencia, unicidad y cálculo numérico.

**Resultados principales:** fórmulas de valor de anualidades y perpetuidades; existencia y unicidad de la tasa de una anualidad.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** verificación cruzada de fórmulas cerradas contra sumas directas.

**Extensión estimada:** 30–36 páginas; 50–60 ejercicios.

### Capítulo 5. Sistemas de amortización

**Prerrequisitos:** L5 c. 4, L3 c. 4.

**Objetivos:** calcular el saldo de una deuda por los métodos retrospectivo y prospectivo y demostrar su equivalencia; construir tablas de amortización de los sistemas francés, alemán y americano; analizar la precancelación y la refinanciación; describir préstamos con tasa variable e indexados.

**Secciones:**

- **5.1** Saldo de la deuda: métodos retrospectivo y prospectivo y su equivalencia.
- **5.2** Sistema francés (cuota constante).
- **5.3** Sistema alemán (amortización constante).
- **5.4** Sistema americano y fondo de amortización.
- **5.5** Tablas de amortización en Python.
- **5.6** Precancelación y refinanciación.
- **5.7** Tasas variables e indexación.

**Resultados principales:** equivalencia de los métodos retrospectivo y prospectivo.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** generación y verificación de tablas de amortización.

**Extensión estimada:** 24–30 páginas; 35–45 ejercicios.

### Capítulo 6. Valor presente neto y tasa interna de retorno

**Prerrequisitos:** L5 c. 3, L5 c. 4, L4 §3.3, L4 §3.4, L4 §6.3, L4 §7.5, L1 §10.6.

**Objetivos:** estudiar el VPN como función de la tasa; demostrar la existencia y unicidad de la TIR para flujos convencionales; construir ejemplos de TIR múltiples o inexistentes; calcular la TIR por bisección y por el método de Newton; comparar los criterios del VPN y de la TIR e identificar sus conflictos; calcular la TIR modificada.

**Secciones:**

- **6.1** El VPN como función de la tasa.
- **6.2** Flujos convencionales: existencia y unicidad de la TIR.
- **6.3** Flujos no convencionales: TIR múltiples o inexistentes; regla de los signos de Descartes.
- **6.4** Cálculo numérico de la TIR por bisección y por el método de Newton.
- **6.5** Criterios de decisión: conflictos entre VPN y TIR; crítica del supuesto de reinversión.
- **6.6** TIR modificada.

**Resultados principales:** existencia y unicidad de la TIR para flujos con un solo cambio de signo.

**Resultados admitidos:** RA-23 (en §6.3).

**Aplicaciones financieras:** evaluación de proyectos.

**Computación:** cálculo de la TIR con control del error.

**Extensión estimada:** 28–34 páginas; 40–50 ejercicios.

### Capítulo 7. Inflación y tasas reales

**Prerrequisitos:** L5 c. 2.

**Objetivos:** calcular tasas de inflación a partir de índices de precios; derivar la ecuación de Fisher exacta y acotar el error de su versión aproximada; valorar flujos nominales y reales de forma consistente; describir instrumentos indexados; explicar por qué las aproximaciones habituales fallan con inflación alta.

**Secciones:**

- **7.1** Índices de precios y tasa de inflación (definiciones de los organismos estadísticos como convención).
- **7.2** Ecuación de Fisher exacta y aproximada; error de la aproximación.
- **7.3** Flujos nominales y reales: regla de consistencia.
- **7.4** Instrumentos indexados a la inflación.
- **7.5** Inflación alta: efectos sobre el cálculo y sobre las aproximaciones.

**Resultados principales:** ecuación de Fisher exacta; cota del error de la aproximación.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** no corresponde.

**Extensión estimada:** 18–24 páginas; 25–35 ejercicios.

### Capítulo 8. Bonos

**Prerrequisitos:** L5 c. 4, L5 c. 6, L5 §2.6.

**Objetivos:** valorar un bono con cupones como suma de valores presentes; demostrar la existencia y unicidad del rendimiento al vencimiento; demostrar la relación entre tasa de cupón, rendimiento y precio respecto de la par; calcular el precio entre fechas de cupón, el interés corrido y los precios limpio y sucio; valorar bonos cupón cero.

**Secciones:**

- **8.1** Descripción de un bono: valor nominal, cupón, vencimiento.
- **8.2** Precio como valor presente; fórmula cerrada.
- **8.3** Rendimiento al vencimiento: existencia y unicidad.
- **8.4** Bonos a la par, con prima y con descuento.
- **8.5** Precio entre fechas de cupón: interés corrido, precio limpio y precio sucio (convenciones).
- **8.6** Bonos cupón cero.
- **8.7** Riesgo de crédito: presentación conceptual (se trata en L22).
- **8.8** Precio y rendimiento de bonos en Python.

**Resultados principales:** existencia y unicidad del rendimiento al vencimiento; relación entre cupón, rendimiento y precio.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** precio y rendimiento de bonos.

**Extensión estimada:** 28–34 páginas; 40–50 ejercicios.

### Capítulo 9. Duración y convexidad

**Prerrequisitos:** L5 c. 8, L4 c. 4, L4 §13.2, L4 §13.3, L4 §14.1.

**Objetivos:** derivar las duraciones de Macaulay y modificada y la convexidad; acotar el error de la aproximación de segundo orden del precio; calcular la duración de una cartera; demostrar el teorema de inmunización de Redington y explicar sus limitaciones; calcular duraciones efectivas por diferencias finitas.

**Secciones:**

- **9.1** Sensibilidad del precio al rendimiento.
- **9.2** Duración de Macaulay y duración modificada.
- **9.3** Convexidad y aproximación de segundo orden con cota del error.
- **9.4** Duración y convexidad de una cartera.
- **9.5** Inmunización: teorema de Redington y sus limitaciones (desplazamientos paralelos de la curva).
- **9.6** Duración efectiva por diferencias finitas.

**Resultados principales:** fórmulas de duración y convexidad; cota del error de la aproximación de segundo orden; teorema de Redington.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** sensibilidades analíticas y numéricas.

**Extensión estimada:** 28–34 páginas; 40–50 ejercicios.

### Capítulo 10. Estructura temporal de tasas

**Prerrequisitos:** L5 c. 8, L5 c. 9, L2 §2.5, L4 c. 10.

**Objetivos:** relacionar factores de descuento, tasas cero y tasas a plazo; construir una curva cero por *bootstrapping* a partir de bonos con cupón; analizar el efecto del método de interpolación sobre las tasas a plazo; explicar por qué el rendimiento al vencimiento difiere de las tasas cero; distinguir hipótesis económicas sobre la curva de resultados; ajustar una curva paramétrica.

**Secciones:**

- **10.1** Factores de descuento y tasas cero.
- **10.2** Tasas a plazo implícitas y su consistencia.
- **10.3** *Bootstrapping* de la curva cero: algoritmo y condiciones de existencia.
- **10.4** Interpolación lineal en tasas y lineal en el logaritmo de los factores de descuento; consecuencias sobre las tasas a plazo.
- **10.5** Rendimiento al vencimiento frente a tasas cero.
- **10.6** Hipótesis sobre la forma de la curva: expectativas y preferencia por liquidez (hipótesis, no resultados).
- **10.7** La curva de Nelson-Siegel (anticipo de la calibración de L12 c. 8).

**Resultados principales:** relaciones entre factores de descuento, tasas cero y tasas a plazo; existencia y unicidad del *bootstrapping* bajo condiciones de no degeneración.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** *bootstrapping* e interpolación en Python.

**Extensión estimada:** 30–36 páginas; 40–50 ejercicios.

### Capítulo 11. Implementación y verificación computacional

**Prerrequisitos:** L5 c. 10, L3 c. 6, L3 c. 7, L3 c. 9.

**Objetivos:** diseñar funciones financieras con pruebas; verificar fórmulas cerradas contra cálculos directos; manejar fechas y calendarios; decidir entre flotantes y aritmética decimal; organizar una pequeña biblioteca de matemática financiera.

**Secciones:**

- **11.1** Diseño de funciones financieras con pruebas.
- **11.2** Verificación cruzada: fórmula cerrada frente a suma directa.
- **11.3** Fechas, calendarios y convenciones de conteo en Python.
- **11.4** Precisión: flotantes y aritmética decimal en montos.
- **11.5** Una pequeña biblioteca de matemática financiera.

**Resultados principales:** no corresponde.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** todo el capítulo.

**Extensión estimada:** 22–28 páginas; 20–30 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
