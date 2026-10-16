# L16. Probabilidad con teoría de la medida y martingalas

Índice detallado · Versión 1.0 · Entrega 1c · 2026-10-16

## Ficha editorial

- **Serie:** IV. Matemática avanzada y tiempo continuo.
- **Requisitos:** L8, L11.
- **Uso como aplicación:** L10, L13.
- **Capítulos:** 12, más un apéndice.
- **Extensión estimada:** 354–436 páginas.

**Propósito.** Este libro reconstruye la probabilidad sobre la teoría de la medida y cierra los resultados que L8 y L15 admitieron: existencia de espacios de probabilidad y de sucesiones independientes, esperanza de funciones generales, unicidad por la función característica, completitud de L² y cambio de variables en ℝⁿ. Desarrolla la integral de Lebesgue, los espacios L^p, el teorema de Fubini, los modos de convergencia, la ley fuerte de los grandes números, la convergencia en distribución con funciones características, la esperanza condicional respecto de σ-álgebras y la teoría de martingalas en tiempo discreto. Termina con el teorema fundamental de valoración en tiempo discreto, que conecta con L10 y L13 y prepara L18.

**Resultados que se cierran.** RA-08 (§5.5\*), RA-09 (§8.4), RA-10 (§4.3), RA-24 (§1.7, §5.6 y §6.2), RA-26 (§3.6).

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro (NOTACION §6).

## Capítulos

### Capítulo 1. σ-álgebras, medidas y teorema de extensión de Carathéodory

**Prerrequisitos:** L11 c. 2, L8 c. 1, L4 c. 12.

**Objetivos:** explicar por qué no toda parte de ℝ puede medirse de forma consistente; definir σ-álgebras, σ-álgebras generadas y borelianos; deducir propiedades de las medidas; demostrar el teorema π-λ de Dynkin y la unicidad de extensiones; demostrar el teorema de extensión de Carathéodory; construir la medida de Lebesgue y las medidas de Lebesgue-Stieltjes; demostrar que toda función de distribución define una probabilidad en ℝ.

**Secciones:**

- **1.1** Por qué se necesita la teoría de la medida: el conjunto de Vitali.
- **1.2** σ-álgebras, σ-álgebras generadas y borelianos.
- **1.3** Medidas: propiedades y continuidad.
- **1.4** Clases π y λ; teorema de Dynkin y unicidad de extensiones.
- **1.5** Medidas exteriores y teorema de extensión de Carathéodory.
- **1.6** Medida de Lebesgue en ℝ.
- **1.7** Medidas de Lebesgue-Stieltjes: toda función de distribución define una probabilidad en ℝ.

**Resultados principales:** teorema π-λ; teorema de Carathéodory; existencia y unicidad de la medida de Lebesgue y de las medidas de Lebesgue-Stieltjes.

**Resultados admitidos:** ninguno. El capítulo cierra parte de RA-24.

**Aplicaciones financieras:** no corresponde.

**Computación:** no corresponde.

**Extensión estimada:** 34–40 páginas; 30–40 ejercicios.

### Capítulo 2. Funciones medibles y variables aleatorias

**Prerrequisitos:** L16 c. 1, L8 §5.7.

**Objetivos:** reconocer funciones medibles y demostrar que la medibilidad se preserva por operaciones y límites; definir variables aleatorias y su ley; aproximar funciones medibles por funciones simples; demostrar el lema de Doob-Dynkin; construir variables con distribución dada sobre el intervalo unidad mediante la función cuantil.

**Secciones:**

- **2.1** Funciones medibles y criterios.
- **2.2** Operaciones y límites de funciones medibles.
- **2.3** Variables aleatorias y su ley.
- **2.4** Aproximación por funciones simples.
- **2.5** σ-álgebra generada por una variable; lema de Doob-Dynkin.
- **2.6** Variables con distribución dada mediante la función cuantil.

**Resultados principales:** estabilidad de la medibilidad; aproximación por funciones simples; lema de Doob-Dynkin.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** la información disponible como σ-álgebra.

**Computación:** no corresponde.

**Extensión estimada:** 22–28 páginas; 25–35 ejercicios.

### Capítulo 3. Integral de Lebesgue

**Prerrequisitos:** L16 c. 2, L4 c. 8.

**Objetivos:** construir la integral de Lebesgue; demostrar los teoremas de convergencia monótona y dominada y el lema de Fatou; demostrar que la integral de Lebesgue extiende la de Riemann; definir la esperanza como integral y demostrar la fórmula de cambio de variable para la esperanza de funciones; derivar bajo el signo integral.

**Secciones:**

- **3.1** Integral de funciones simples no negativas.
- **3.2** Funciones no negativas; teorema de convergencia monótona.
- **3.3** Funciones integrables y linealidad.
- **3.4** Lema de Fatou y teorema de convergencia dominada.
- **3.5** Relación con la integral de Riemann.
- **3.6** La esperanza como integral; fórmula de cambio de variable. Cierra RA-26.
- **3.7** Derivación bajo el signo integral.

**Resultados principales:** convergencia monótona; lema de Fatou; convergencia dominada; coincidencia con la integral de Riemann.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** intercambio de límite y esperanza en valoraciones.

**Computación:** no corresponde.

**Extensión estimada:** 32–38 páginas; 30–40 ejercicios.

### Capítulo 4. Espacios L^p

**Prerrequisitos:** L16 c. 3, L11 c. 8, L11 c. 9.

**Objetivos:** construir los espacios L^p como cocientes; demostrar las desigualdades de Hölder y Minkowski para integrales; demostrar la completitud de L^p; trabajar con L² como espacio de Hilbert; demostrar la densidad de funciones continuas y escalonadas; relacionar los modos de convergencia en L^p.

**Secciones:**

- **4.1** Seminorma y cociente por igualdad en casi todo punto.
- **4.2** Desigualdades de Hölder y Minkowski.
- **4.3** Completitud de L^p: teorema de Riesz-Fischer. Cierra RA-10.
- **4.4** L² como espacio de Hilbert.
- **4.5** Densidad de funciones continuas y escalonadas.
- **4.6** Convergencia en L^p y sus relaciones.

**Resultados principales:** teorema de Riesz-Fischer; densidad de funciones continuas.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** pagos de cuadrado integrable como espacio de Hilbert.

**Computación:** no corresponde.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

### Capítulo 5. Medida producto y teorema de Fubini-Tonelli

**Prerrequisitos:** L16 c. 3, L16 c. 1, L7 c. 10.

**Objetivos:** construir la σ-álgebra y la medida producto; demostrar los teoremas de Tonelli y Fubini; construir la medida de Lebesgue en ℝⁿ; demostrar el teorema de cambio de variables (sección opcional); construir vectores con marginales independientes dadas.

**Secciones:**

- **5.1** σ-álgebra producto.
- **5.2** Construcción de la medida producto.
- **5.3** Teoremas de Tonelli y de Fubini.
- **5.4** Medida de Lebesgue en ℝⁿ.
- **5.5\*** Teorema de cambio de variables para difeomorfismos. Cierra RA-08.
- **5.6** Vectores con componentes independientes de leyes dadas.

**Resultados principales:** existencia y unicidad de la medida producto; teoremas de Tonelli y Fubini; cambio de variables.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** no corresponde.

**Extensión estimada:** 26–32 páginas; 20–30 ejercicios.

### Capítulo 6. Independencia, lemas de Borel-Cantelli y ley 0-1

**Prerrequisitos:** L16 c. 5, L16 c. 2.

**Objetivos:** definir la independencia de σ-álgebras y de variables y demostrar el criterio por clases π; construir sucesiones de variables independientes con leyes dadas; demostrar los lemas de Borel-Cantelli y la ley 0-1 de Kolmogorov; aplicar estos resultados a eventos de cola y a la recurrencia del paseo aleatorio simple.

**Secciones:**

- **6.1** Independencia de σ-álgebras y de variables; criterio por clases π.
- **6.2** Existencia de sucesiones independientes con leyes dadas mediante los dígitos binarios. Cierra RA-24.
- **6.3** Lemas de Borel-Cantelli.
- **6.4** Ley 0-1 de Kolmogorov.
- **6.5** Aplicaciones: eventos de cola y recurrencia del paseo aleatorio simple.

**Resultados principales:** existencia de sucesiones independientes; lemas de Borel-Cantelli; ley 0-1.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** no corresponde.

**Extensión estimada:** 22–28 páginas; 25–35 ejercicios.

### Capítulo 7. Modos de convergencia y ley fuerte de los grandes números

**Prerrequisitos:** L16 c. 6, L16 c. 4.

**Objetivos:** relacionar convergencia casi segura, en probabilidad y en L^p con demostraciones y contraejemplos; demostrar el teorema de Vitali mediante integrabilidad uniforme; demostrar la ley fuerte con cuarto momento y la versión de Etemadi con primer momento; demostrar el teorema de Glivenko-Cantelli; aplicar a la consistencia fuerte de estimadores y de Monte Carlo.

**Secciones:**

- **7.1** Convergencia casi segura, en probabilidad y en L^p: relaciones y contraejemplos.
- **7.2** Integrabilidad uniforme y teorema de Vitali.
- **7.3** Ley fuerte con cuarto momento finito.
- **7.4** Ley fuerte de Etemadi.
- **7.5** Teorema de Glivenko-Cantelli.
- **7.6** Consistencia fuerte de estimadores y de Monte Carlo.

**Resultados principales:** teorema de Vitali; ley fuerte de los grandes números; teorema de Glivenko-Cantelli.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** fundamento de la estimación por simulación.

**Computación:** no corresponde.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 8. Convergencia en distribución y funciones características

**Prerrequisitos:** L16 c. 7, L16 c. 5, L8 c. 8, L8 c. 11, L11 c. 7.

**Objetivos:** demostrar las equivalencias de la convergencia en distribución; demostrar el teorema de representación de Skorokhod; demostrar el teorema de Helly y caracterizar la tensión; demostrar la fórmula de inversión y la unicidad de la función característica; demostrar el teorema de continuidad de Lévy, el teorema central del límite de Lindeberg-Feller y el criterio de Cramér-Wold.

**Secciones:**

- **8.1** Convergencia en distribución: equivalencias.
- **8.2** Teorema de representación de Skorokhod.
- **8.3** Tensión y teorema de Helly.
- **8.4** Fórmula de inversión y unicidad de la función característica. Cierra RA-09.
- **8.5** Teorema de continuidad de Lévy.
- **8.6** Teorema central del límite de Lindeberg-Feller.
- **8.7** Criterio de Cramér-Wold y teorema central del límite multivariante.

**Resultados principales:** todos los enunciados del capítulo se demuestran.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** fundamento de la valoración por métodos de Fourier (L19 c. 9).

**Computación:** inversión numérica de funciones características.

**Extensión estimada:** 32–38 páginas; 25–35 ejercicios.

### Capítulo 9. Esperanza condicional y teorema de Radon-Nikodym

**Prerrequisitos:** L16 c. 4, L16 c. 5, L8 c. 9.

**Objetivos:** definir la esperanza condicional respecto de una σ-álgebra; demostrar su existencia mediante la proyección en L² y su extensión a L¹; demostrar sus propiedades, incluida la desigualdad de Jensen condicional; demostrar el teorema de Radon-Nikodym por el argumento de von Neumann; obtener la esperanza condicional como derivada de Radon-Nikodym.

**Secciones:**

- **9.1** Condicionar a la información: σ-álgebras.
- **9.2** Existencia mediante la proyección en L² y extensión a L¹.
- **9.3** Propiedades: torre, extracción de lo conocido, independencia y Jensen condicional.
- **9.4** Teorema de Radon-Nikodym.
- **9.5** La esperanza condicional como derivada de Radon-Nikodym.

**Resultados principales:** existencia y unicidad de la esperanza condicional; propiedades; teorema de Radon-Nikodym.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** valoración condicional a la información disponible.

**Computación:** no corresponde.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 10. Martingalas en tiempo discreto y tiempos de parada

**Prerrequisitos:** L16 c. 9, L8 §9.7, L8 c. 14.

**Objetivos:** definir filtraciones, procesos adaptados, martingalas, submartingalas y supermartingalas; demostrar que las transformadas de martingala son martingalas y leerlas como ganancias de estrategias; definir tiempos de parada y procesos detenidos; demostrar el teorema de muestreo opcional; demostrar la descomposición de Doob; demostrar que no existen estrategias de apuesta ganadoras en juegos equitativos.

**Secciones:**

- **10.1** Filtraciones y procesos adaptados.
- **10.2** Martingalas, submartingalas y supermartingalas.
- **10.3** Transformadas de martingala: la integral estocástica discreta y las ganancias de una estrategia.
- **10.4** Tiempos de parada y procesos detenidos.
- **10.5** Teorema de muestreo opcional.
- **10.6** Descomposición de Doob.
- **10.7** Aplicaciones: ruina del jugador y estrategias de apuesta.

**Resultados principales:** propiedad de martingala de las transformadas; teorema de muestreo opcional; descomposición de Doob.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** ganancias de estrategias de negociación; imposibilidad de ganar sistemáticamente en un juego equitativo.

**Computación:** simulación de estrategias de apuesta.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 11. Convergencia de martingalas y desigualdades de Doob

**Prerrequisitos:** L16 c. 10, L16 c. 7.

**Objetivos:** demostrar la desigualdad de cruces y el teorema de convergencia casi segura de martingalas; caracterizar las martingalas uniformemente integrables y su cierre; demostrar las desigualdades maximales de Doob; aplicar martingalas hacia atrás a la ley fuerte y estudiar la martingala de verosimilitud (secciones opcionales).

**Secciones:**

- **11.1** Desigualdad de cruces.
- **11.2** Teorema de convergencia casi segura.
- **11.3** Martingalas uniformemente integrables, convergencia en L¹ y cierre.
- **11.4** Desigualdades maximales de Doob y convergencia en L^p.
- **11.5\*** Martingalas hacia atrás y la ley fuerte revisitada.
- **11.6\*** La razón de verosimilitudes como martingala.

**Resultados principales:** desigualdad de cruces; teoremas de convergencia; desigualdades de Doob.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** procesos de precios descontados en horizonte largo.

**Computación:** no corresponde.

**Extensión estimada:** 24–30 páginas; 20–30 ejercicios.

### Capítulo 12. Cambio de medida y teorema fundamental de valoración en tiempo discreto

**Prerrequisitos:** L16 c. 9, L16 c. 10, L7 c. 7.

**Objetivos:** trabajar con medidas equivalentes y sus densidades; demostrar la fórmula de Bayes para esperanzas condicionales bajo cambio de medida; formular un mercado en tiempo discreto con espacio muestral finito; demostrar el teorema de Harrison-Pliska; demostrar la caracterización de la completitud por la unicidad de la medida martingala equivalente; enunciar el caso general de Dalang-Morton-Willinger; reinterpretar el modelo binomial.

**Secciones:**

- **12.1** Medidas equivalentes y densidades.
- **12.2** El proceso densidad como martingala; fórmula de Bayes condicional.
- **12.3** Mercados en tiempo discreto: estrategias autofinanciadas y arbitraje.
- **12.4** Teorema de Harrison-Pliska.
- **12.5** Completitud y unicidad de la medida martingala equivalente.
- **12.6** El caso general: teorema de Dalang-Morton-Willinger.
- **12.7** El modelo binomial a la luz del teorema fundamental.

**Resultados principales:** fórmula de Bayes condicional; teorema de Harrison-Pliska; segundo teorema fundamental en mercados finitos.

**Resultados admitidos:** RA-19 (en §12.6).

**Aplicaciones financieras:** todo el capítulo.

**Usa como aplicación:** L10 c. 8, L13 c. 5.

**Computación:** no corresponde.

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
