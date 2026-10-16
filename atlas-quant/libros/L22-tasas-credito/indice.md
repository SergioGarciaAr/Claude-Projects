# L22. Tasas de interés y riesgo de crédito

Índice detallado · Versión 1.0 · Entrega 1d · 2026-10-16

## Ficha editorial

- **Serie:** V. Investigación (especialización).
- **Requisitos:** L5, L12, L13, L17, L18, L19.
- **Capítulos:** 10, más un apéndice.
- **Extensión estimada:** 280–350 páginas.

**Propósito.** Este libro de especialización desarrolla los modelos de tasas de interés y de riesgo de crédito: instrumentos, construcción de curvas con varias curvas, modelos de tasa corta y estructura afín, el marco de Heath-Jarrow-Morton, las medidas forward y el modelo de mercado, los modelos estructurales y de intensidad, los swaps de incumplimiento crediticio, el crédito de cartera y los ajustes de valoración por riesgo de contraparte. Las convenciones de mercado y la transición de tasas de referencia cambian con el tiempo; se presentan con fecha de verificación.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro.

## Capítulos

### Capítulo 1. Instrumentos de tasa de interés

**Prerrequisitos:** L13 c. 2, L5 c. 10.

**Objetivos:** describir las tasas de referencia y su transición; valorar acuerdos de tasa futura y futuros de tasas; describir swaps indexados a tasas nocturnas; describir *caps*, *floors* y *swaptions*; aplicar las convenciones correspondientes.

**Secciones:**

- **1.1** Tasas de referencia y su transición (con fecha de verificación).
- **1.2** Acuerdos de tasa futura y futuros de tasas.
- **1.3** Swaps y swaps indexados a tasas nocturnas.
- **1.4** *Caps* y *floors*.
- **1.5** *Swaptions*.
- **1.6** Convenciones.

**Resultados principales:** valoración de acuerdos de tasa futura por replicación.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** no corresponde.

**Extensión estimada:** 24–30 páginas; 20–30 ejercicios.

### Capítulo 2. Construcción de curvas en la práctica

**Prerrequisitos:** L22 c. 1, L12 c. 4, L12 c. 8.

**Objetivos:** distinguir curvas de descuento y de proyección en el marco de varias curvas; elegir instrumentos de calibración; construir curvas por *bootstrapping* con varias curvas; evaluar la suavidad de las tasas a plazo según la interpolación; calcular sensibilidades a los instrumentos de mercado; verificar la curva.

**Secciones:**

- **2.1** Curvas de descuento y de proyección.
- **2.2** Instrumentos de calibración.
- **2.3** *Bootstrapping* con varias curvas.
- **2.4** Interpolación y suavidad de las tasas a plazo.
- **2.5** Sensibilidades a los instrumentos de mercado.
- **2.6** Verificación.

**Resultados principales:** existencia y unicidad del *bootstrapping* bajo condiciones explícitas.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** construcción de un juego de curvas.

**Extensión estimada:** 26–32 páginas; 15–25 ejercicios.

### Capítulo 3. Modelos de tasa corta y estructura afín

**Prerrequisitos:** L18 c. 7, L18 c. 8, L15 §2.6, L19 c. 4.

**Objetivos:** valorar bonos como esperanzas bajo un modelo de tasa corta; resolver el modelo de Vasicek y obtener el precio del bono; estudiar el modelo CIR y su positividad; demostrar el teorema de estructura afín mediante Feynman-Kac y ecuaciones de Riccati; ajustar el modelo de Hull-White a la curva inicial; valorar opciones sobre bonos en Vasicek con la medida forward; calibrar y discutir limitaciones.

**Secciones:**

- **3.1** El precio del bono como esperanza.
- **3.2** Modelo de Vasicek.
- **3.3** Modelo CIR.
- **3.4** Estructura afín.
- **3.5** Modelo de Hull-White.
- **3.6** Opciones sobre bonos en Vasicek.
- **3.7** Calibración y limitaciones.

**Resultados principales:** precios de bonos en Vasicek y CIR; teorema de estructura afín; ajuste de Hull-White.

**Resultados admitidos:** RA-18 (en §3.3), RA-55 (en §3.3).

**Aplicaciones financieras:** todo el capítulo.

**Computación:** valoración y simulación de modelos de tasa corta.

**Extensión estimada:** 32–38 páginas; 20–30 ejercicios.

### Capítulo 4. Marco de Heath-Jarrow-Morton

**Prerrequisitos:** L22 c. 3, L18 c. 9.

**Objetivos:** modelar tasas a plazo instantáneas; demostrar la condición de deriva de Heath-Jarrow-Morton; expresar Ho-Lee y Hull-White en ese marco; reconocer cuándo un modelo es markoviano y su dimensión; discutir limitaciones prácticas.

**Secciones:**

- **4.1** Modelos de tasas a plazo instantáneas.
- **4.2** Condición de deriva.
- **4.3** Ho-Lee y Hull-White como modelos de Heath-Jarrow-Morton.
- **4.4** Markovianidad y dimensión.
- **4.5** Limitaciones prácticas.

**Resultados principales:** condición de deriva de Heath-Jarrow-Morton.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** simulación de un modelo de un factor.

**Extensión estimada:** 22–28 páginas; 15–25 ejercicios.

### Capítulo 5. Medidas forward, fórmula de Black y modelo de mercado

**Prerrequisitos:** L22 c. 4, L19 c. 4.

**Objetivos:** demostrar que las tasas a plazo son martingalas bajo la medida forward correspondiente; derivar la fórmula de Black para *caplets* y *swaptions*; derivar las derivas del modelo de mercado bajo distintas medidas; describir su simulación y calibración; tratar tasas negativas con el modelo normal.

**Secciones:**

- **5.1** Medida forward y tasas a plazo como martingalas.
- **5.2** Fórmula de Black para *caplets*.
- **5.3** Medida swap y *swaptions*.
- **5.4** Modelo de mercado de tasas a plazo: derivas.
- **5.5** Simulación y calibración (presentación).
- **5.6** Modelo normal y tasas negativas.

**Resultados principales:** propiedad de martingala de las tasas a plazo; fórmulas de Black; derivas del modelo de mercado.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** valoración de *caps* y *swaptions*.

**Extensión estimada:** 28–34 páginas; 15–25 ejercicios.

### Capítulo 6. Modelo estructural de Merton

**Prerrequisitos:** L19 c. 3, L19 c. 8, L5 c. 8.

**Objetivos:** modelar la deuda como opción sobre el valor de la firma; derivar la fórmula de Merton; obtener probabilidades de incumplimiento y diferenciales de crédito; extender a modelos de primer pasaje; describir la evidencia y el rompecabezas del diferencial de crédito.

**Secciones:**

- **6.1** Valor de la firma y deuda como opción.
- **6.2** Fórmula de Merton.
- **6.3** Probabilidad de incumplimiento y diferencial de crédito.
- **6.4** Modelos de primer pasaje.
- **6.5** Evidencia y limitaciones (resultados empíricos).

**Resultados principales:** fórmula de Merton; fórmula de primer pasaje de Black-Cox.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** calibración de Merton con datos de una firma (fuente por verificar en 1e).

**Extensión estimada:** 24–30 páginas; 15–25 ejercicios.

### Capítulo 7. Modelos de intensidad

**Prerrequisitos:** L18 c. 2, L22 c. 3.

**Objetivos:** modelar el incumplimiento como primer salto; trabajar con intensidades deterministas y estocásticas; demostrar la fórmula de valoración de bonos con riesgo bajo procesos de Cox; describir convenciones de recuperación; usar modelos afines de intensidad; calibrar a diferenciales.

**Secciones:**

- **7.1** El incumplimiento como primer salto.
- **7.2** Intensidad determinista y estocástica: procesos de Cox.
- **7.3** Valoración de bonos con riesgo.
- **7.4** Convenciones de recuperación.
- **7.5** Modelos afines de intensidad.
- **7.6** Calibración a diferenciales.

**Resultados principales:** fórmula de valoración bajo procesos de Cox.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** construcción de curvas de supervivencia.

**Extensión estimada:** 26–32 páginas; 15–25 ejercicios.

### Capítulo 8. Swaps de incumplimiento crediticio

**Prerrequisitos:** L22 c. 7.

**Objetivos:** describir el contrato; valorar las piernas de prima y de protección; calcular el diferencial par; construir la curva de supervivencia por *bootstrapping*; aplicar las convenciones estandarizadas; analizar la relación entre swaps de incumplimiento y bonos.

**Secciones:**

- **8.1** El contrato.
- **8.2** Pierna de prima y pierna de protección.
- **8.3** Diferencial par.
- **8.4** *Bootstrapping* de la curva de supervivencia.
- **8.5** Convenciones estandarizadas (con fecha de verificación).
- **8.6** Relación con los bonos: la base.

**Resultados principales:** fórmulas de valoración de las dos piernas.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** valoración de swaps de incumplimiento.

**Extensión estimada:** 20–26 páginas; 15–25 ejercicios.

### Capítulo 9. Riesgo de crédito de cartera

**Prerrequisitos:** L22 c. 7, L17 c. 9, L8 c. 11.

**Objetivos:** describir la distribución de pérdidas de una cartera; demostrar la distribución límite del modelo de un factor de Vasicek; modelar tiempos de incumplimiento con cópula gaussiana; valorar tramos y explicar la correlación implícita; extraer lecciones de la crisis de 2007-2008; describir el uso regulatorio con fecha de verificación.

**Secciones:**

- **9.1** Distribución de pérdidas de una cartera.
- **9.2** Modelo de un factor de Vasicek y su distribución límite.
- **9.3** Cópula gaussiana para tiempos de incumplimiento.
- **9.4** Tramos y correlación implícita.
- **9.5** Lecciones de 2007-2008.
- **9.6** Uso regulatorio (descripción con fecha de verificación).

**Resultados principales:** distribución límite de Vasicek mediante la ley de los grandes números condicional.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** simulación de pérdidas de cartera.

**Extensión estimada:** 26–32 páginas; 15–25 ejercicios.

### Capítulo 10. Riesgo de contraparte y CVA

**Prerrequisitos:** L22 c. 8, L19 c. 9.

**Objetivos:** definir exposición esperada y exposición potencial futura; demostrar la fórmula del CVA unilateral bajo independencia; calcularlo por simulación; describir el riesgo de correlación adversa; incorporar colateral y compensación; presentar otros ajustes de valoración y sus controversias.

**Secciones:**

- **10.1** Exposición: esperada y potencial futura.
- **10.2** CVA unilateral bajo independencia.
- **10.3** Cálculo por simulación.
- **10.4** Riesgo de correlación adversa.
- **10.5** Colateral y compensación.
- **10.6** Otros ajustes de valoración: presentación y controversias.

**Resultados principales:** fórmula del CVA unilateral bajo independencia.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** CVA de un swap por simulación.

**Extensión estimada:** 24–30 páginas; 15–25 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
