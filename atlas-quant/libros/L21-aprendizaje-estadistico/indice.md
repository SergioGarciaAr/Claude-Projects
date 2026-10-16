# L21. Aprendizaje estadístico en finanzas

Índice detallado · Versión 1.0 · Entrega 1d · 2026-10-16

## Ficha editorial

- **Serie:** V. Investigación.
- **Requisitos:** L6, L7, L9, L12, L14, L20.
- **Capítulos:** 13, más un apéndice.
- **Extensión estimada:** 346–434 páginas.

**Propósito.** Este libro presenta el aprendizaje estadístico como continuación de la inferencia de L9 y de la metodología de L20, no como un conjunto de herramientas autónomas. Desarrolla la teoría de la generalización, la regularización, la validación con datos dependientes, la clasificación y su calibración, los árboles y ensambles, los métodos de núcleo, el aprendizaje no supervisado, los fundamentos de las redes neuronales, la interpretabilidad y los métodos bayesianos con MCMC. Las aplicaciones financieras se evalúan con escepticismo: relación señal-ruido baja, no estacionariedad, costos de transacción y riesgo de sobreajuste.

**Fuera del alcance.** El aprendizaje profundo y el aprendizaje por refuerzo se tratan solo como especializaciones (PLAN_EDITORIAL §4.1); este libro desarrolla los fundamentos que requieren.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro.

## Capítulos

### Capítulo 1. Riesgo, sesgo-varianza y generalización

**Prerrequisitos:** L9 c. 12, L8 §10.4.

**Objetivos:** formular el aprendizaje supervisado como minimización de riesgo; distinguir riesgo empírico y poblacional; demostrar la descomposición sesgo-varianza con pérdida cuadrática; demostrar cotas de generalización para clases finitas mediante la desigualdad de Hoeffding; enunciar las cotas basadas en la dimensión de Vapnik-Chervonenkis; explicar por qué la teoría para datos independientes no basta en finanzas.

**Secciones:**

- **1.1** Aprendizaje supervisado: riesgo y función de pérdida.
- **1.2** Minimización del riesgo empírico.
- **1.3** Descomposición sesgo-varianza.
- **1.4** Cotas de generalización para clases finitas.
- **1.5** Complejidad de la clase y dimensión de Vapnik-Chervonenkis.
- **1.6** Datos dependientes y no estacionarios.

**Resultados principales:** descomposición sesgo-varianza; cota de generalización para clases finitas.

**Resultados admitidos:** RA-58 (en §1.5).

**Aplicaciones financieras:** por qué un error de entrenamiento bajo no garantiza un pronóstico útil de rendimientos.

**Computación:** curvas de aprendizaje simuladas.

**Extensión estimada:** 26–32 páginas; 20–30 ejercicios.

### Capítulo 2. Regularización: ridge, lasso y red elástica

**Prerrequisitos:** L21 c. 1, L6 c. 11, L12 c. 7, L9 c. 11.

**Objetivos:** derivar la solución de ridge e interpretarla mediante la descomposición en valores singulares; caracterizar la solución del lasso con subgradientes y demostrar el umbral suave en el caso ortonormal; aplicar la red elástica; implementar descenso coordenado y gradiente proximal; recorrer el camino de regularización; demostrar la interpretación como estimadores de máxima posterior.

**Secciones:**

- **2.1** Ridge: solución cerrada y contracción en las direcciones singulares.
- **2.2** Lasso: condiciones de optimalidad, umbral suave y esparcidad.
- **2.3** Red elástica.
- **2.4** Algoritmos: descenso coordenado y gradiente proximal.
- **2.5** Camino de regularización.
- **2.6** Interpretación bayesiana: distribuciones previas gaussiana y de Laplace.
- **2.7** Predicción con muchas variables.

**Resultados principales:** fórmula de ridge; condiciones de optimalidad del lasso; equivalencia con estimadores de máxima posterior.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** predicción de rendimientos con muchas características.

**Computación:** implementación de ridge y lasso, y comparación con bibliotecas.

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

### Capítulo 3. Validación con datos dependientes

**Prerrequisitos:** L21 c. 2, L20 c. 7, L14 c. 7.

**Objetivos:** elegir hiperparámetros con validación progresiva y purgada; separar selección y evaluación mediante validación anidada; medir la estabilidad de la selección; detectar fugas de información en el preprocesamiento.

**Secciones:**

- **3.1** Elección de hiperparámetros.
- **3.2** Validación progresiva y purgada en la práctica.
- **3.3** Validación anidada.
- **3.4** Estabilidad de la selección.
- **3.5** Fugas de información en el preprocesamiento.

**Resultados principales:** no corresponde; capítulo de métodos.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** canal de validación reproducible con pruebas contra fugas.

**Extensión estimada:** 20–26 páginas; 15–25 ejercicios.

### Capítulo 4. Clasificación y calibración

**Prerrequisitos:** L21 c. 1, L9 c. 4, L12 c. 6.

**Objetivos:** demostrar la optimalidad del clasificador de Bayes; estimar la regresión logística y demostrar la convexidad de su verosimilitud; derivar el análisis discriminante lineal y cuadrático; usar matrices de confusión, curvas ROC y AUC, y demostrar la interpretación probabilística de la AUC; calibrar probabilidades; tratar clases desbalanceadas; predecir incumplimientos.

**Secciones:**

- **4.1** Pérdida 0-1 y clasificador de Bayes.
- **4.2** Regresión logística.
- **4.3** Análisis discriminante lineal y cuadrático.
- **4.4** Matriz de confusión, curva ROC y AUC.
- **4.5** Calibración: Platt, regresión isotónica y diagramas de fiabilidad.
- **4.6** Clases desbalanceadas.
- **4.7** Predicción de incumplimiento.

**Resultados principales:** optimalidad del clasificador de Bayes; convexidad de la log-verosimilitud logística; interpretación de la AUC.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** calificación crediticia.

**Computación:** clasificación con datos de crédito (fuente por verificar en 1e).

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

### Capítulo 5. Árboles de decisión

**Prerrequisitos:** L21 c. 1, L21 c. 4.

**Objetivos:** construir árboles de regresión y clasificación por partición recursiva; elegir criterios de impureza; podar por costo-complejidad; reconocer la alta varianza de los árboles; capturar interacciones y no linealidades.

**Secciones:**

- **5.1** Partición recursiva.
- **5.2** Criterios de impureza.
- **5.3** Poda por costo-complejidad.
- **5.4** Ventajas y limitaciones.
- **5.5** Interacciones y no linealidades.

**Resultados principales:** existencia de un subárbol óptimo para cada parámetro de complejidad y anidamiento de la sucesión.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** reglas de clasificación interpretables.

**Computación:** árboles con bibliotecas y visualización.

**Extensión estimada:** 20–26 páginas; 15–25 ejercicios.

### Capítulo 6. Ensambles y *boosting*

**Prerrequisitos:** L21 c. 5, L12 c. 6.

**Objetivos:** demostrar la reducción de varianza del promedio de predictores correlacionados; construir bosques aleatorios y estimar el error fuera de la bolsa; demostrar que AdaBoost minimiza por etapas la pérdida exponencial; interpretar la potenciación del gradiente como descenso funcional; regularizar el *boosting*; reconocer los sesgos de las medidas de importancia.

**Secciones:**

- **6.1** *Bagging* y reducción de varianza.
- **6.2** Bosques aleatorios y error fuera de la bolsa.
- **6.3** AdaBoost como minimización por etapas de la pérdida exponencial.
- **6.4** Potenciación del gradiente como descenso funcional.
- **6.5** Regularización del *boosting*.
- **6.6** Importancia de variables en ensambles y sus sesgos.

**Resultados principales:** varianza del promedio de predictores correlacionados; interpretación de AdaBoost.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** pronóstico de volatilidad y de incumplimiento.

**Computación:** comparación de ensambles con validación purgada.

**Extensión estimada:** 26–32 páginas; 15–25 ejercicios.

### Capítulo 7. Métodos de núcleo (\*)

**Prerrequisitos:** L21 c. 2, L6 c. 10, L7 c. 9.

**Objetivos:** construir núcleos a partir de espacios de características; reconocer núcleos definidos positivos mediante matrices de Gram; demostrar el teorema del representante en espacios de características de dimensión finita; formular las máquinas de soporte vectorial y su dual; elegir núcleos y reconocer los límites de escala.

**Secciones:**

- **7.1** Del espacio de características al núcleo.
- **7.2** Núcleos definidos positivos y matrices de Gram.
- **7.3** Regresión ridge con núcleos y teorema del representante.
- **7.4** Máquinas de soporte vectorial y su dual.
- **7.5** Elección del núcleo y escalabilidad.

**Resultados principales:** teorema del representante (dimensión finita); dual de las máquinas de soporte vectorial.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** clasificación no lineal.

**Computación:** regresión con núcleos.

**Extensión estimada:** 22–28 páginas; 15–25 ejercicios.

### Capítulo 8. Aprendizaje no supervisado

**Prerrequisitos:** L21 c. 1, L9 c. 13, L6 c. 11.

**Objetivos:** aplicar componentes principales; demostrar que el algoritmo de Lloyd para k-medias disminuye la función objetivo en cada paso; construir agrupamientos jerárquicos; ajustar modelos de mezcla con el algoritmo EM y demostrar su monotonía; aplicar agrupamientos a regímenes y activos; evaluar su inestabilidad.

**Secciones:**

- **8.1** Componentes principales revisitadas.
- **8.2** k-medias y algoritmo de Lloyd.
- **8.3** Agrupamiento jerárquico.
- **8.4** Modelos de mezcla y algoritmo EM.
- **8.5** Aplicaciones: regímenes y agrupamiento de activos.
- **8.6** Inestabilidad de los agrupamientos.

**Resultados principales:** monotonía del algoritmo de Lloyd; monotonía del algoritmo EM.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** regímenes de mercado; estructura jerárquica de correlaciones.

**Computación:** agrupamiento de rendimientos.

**Extensión estimada:** 24–30 páginas; 15–25 ejercicios.

### Capítulo 9. Fundamentos de redes neuronales

**Prerrequisitos:** L21 c. 1, L7 c. 4, L12 c. 6.

**Objetivos:** definir el perceptrón multicapa; enunciar el teorema de aproximación universal y explicar qué no garantiza; derivar la retropropagación como regla de la cadena; entrenar con descenso de gradiente estocástico; regularizar con decaimiento de pesos, parada temprana y *dropout*; explicar por qué las redes no son la opción por defecto con datos financieros.

**Secciones:**

- **9.1** Perceptrón multicapa.
- **9.2** Teorema de aproximación universal.
- **9.3** Retropropagación.
- **9.4** Descenso de gradiente estocástico.
- **9.5** Regularización.
- **9.6** Redes neuronales con datos financieros: evidencia y cautelas.

**Resultados principales:** derivación de la retropropagación.

**Resultados admitidos:** RA-21 (en §9.4), RA-59 (en §9.2).

**Aplicaciones financieras:** predicción con muchas características (con escepticismo).

**Computación:** red pequeña implementada con NumPy y comparada con una biblioteca.

**Extensión estimada:** 26–32 páginas; 15–25 ejercicios.

### Capítulo 10. Interpretabilidad y estabilidad

**Prerrequisitos:** L21 c. 6, L21 c. 9.

**Objetivos:** calcular importancias por permutación; construir gráficos de dependencia parcial y efectos acumulados locales; definir los valores de Shapley y demostrar su unicidad bajo sus axiomas; detectar la inestabilidad de las explicaciones y de los modelos; documentar modelos.

**Secciones:**

- **10.1** Importancia por permutación.
- **10.2** Dependencia parcial y efectos acumulados locales.
- **10.3** Valores de Shapley.
- **10.4** Inestabilidad de las explicaciones.
- **10.5** Estabilidad de los modelos ante cambios de datos.
- **10.6** Documentación de modelos.

**Resultados principales:** unicidad de los valores de Shapley.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** explicación de modelos de crédito y de señales.

**Computación:** comparación de métodos de explicación.

**Extensión estimada:** 22–28 páginas; 15–25 ejercicios.

### Capítulo 11. Métodos bayesianos y MCMC

**Prerrequisitos:** L21 c. 2, L9 c. 11, L8 c. 14, L12 c. 9.

**Objetivos:** estimar regresiones bayesianas conjugadas; explicar por qué hace falta simular la posterior; demostrar que el equilibrio detallado implica estacionariedad y que Metropolis-Hastings lo satisface; demostrar la convergencia en espacios finitos y enunciarla en general; aplicar el muestreo de Gibbs; diagnosticar la convergencia; construir modelos jerárquicos sencillos.

**Secciones:**

- **11.1** Regresión bayesiana conjugada.
- **11.2** Por qué simular la posterior.
- **11.3** Metropolis-Hastings: equilibrio detallado y convergencia.
- **11.4** Muestreo de Gibbs.
- **11.5** Diagnóstico de convergencia.
- **11.6** Modelos jerárquicos y contracción.

**Resultados principales:** equilibrio detallado implica estacionariedad; Metropolis-Hastings satisface el equilibrio detallado; convergencia en espacios finitos.

**Resultados admitidos:** RA-60 (en §11.3).

**Aplicaciones financieras:** estimación jerárquica de alfas y de betas.

**Computación:** implementación de Metropolis-Hastings y de Gibbs.

**Extensión estimada:** 26–32 páginas; 15–25 ejercicios.

### Capítulo 12. Aplicaciones con escepticismo metodológico

**Prerrequisitos:** L21 c. 3, L21 c. 6, L20 c. 8.

**Objetivos:** evaluar la evidencia sobre el aprendizaje automático en la predicción del corte transversal de rendimientos; comparar pronósticos de volatilidad con GARCH; construir modelos de puntaje crediticio; describir señales de texto; traducir pronósticos a carteras con costos y capacidad; fijar expectativas realistas.

**Secciones:**

- **12.1** Corte transversal de rendimientos (resultados empíricos).
- **12.2** Volatilidad: aprendizaje automático frente a GARCH.
- **12.3** Puntaje crediticio.
- **12.4** Señales a partir de texto (presentación).
- **12.5** Del pronóstico a la cartera: costos y capacidad.
- **12.6** Magnitudes realistas.

**Resultados principales:** no corresponde; capítulo de aplicaciones.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** estudio aplicado con evaluación económica.

**Extensión estimada:** 28–34 páginas; 10–20 ejercicios.

### Capítulo 13. Replicación crítica de un artículo

**Prerrequisitos:** L21 c. 12, L20 c. 12.

**Objetivos:** elegir un artículo replicable con criterios explícitos; reconstruir datos y variables; replicar los resultados principales; probar su robustez; escribir un informe de replicación.

**Secciones:**

- **13.1** Elección del artículo y criterios.
- **13.2** Reconstrucción de datos y variables.
- **13.3** Replicación de los resultados principales.
- **13.4** Pruebas de robustez.
- **13.5** Informe de replicación.

**Resultados principales:** no corresponde; capítulo de práctica.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** todo el capítulo.

**Extensión estimada:** 20–26 páginas; proyecto guiado.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice analítico.
