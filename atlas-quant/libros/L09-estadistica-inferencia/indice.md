# L9. Estadística e inferencia

Índice detallado · Versión 1.0 · Entrega 1c · 2026-10-16

## Ficha editorial

- **Serie:** II. Matemática para las finanzas.
- **Requisitos:** L3, L6, L7, L8.
- **Uso como aplicación:** L5.
- **Capítulos:** 14, más un apéndice.
- **Extensión estimada:** 400–480 páginas.

**Propósito.** Este libro desarrolla la inferencia estadística clásica y una introducción a la bayesiana, con la atención puesta en los problemas que aparecen con datos financieros: muestras cortas respecto de la señal, colas pesadas, búsqueda de muchas hipótesis y sobreajuste. Demuestra los resultados centrales (Cramér-Rao, Neyman-Pearson, Gauss-Markov, método delta, Bonferroni, Holm, Benjamini-Hochberg, normalidad asintótica de la máxima verosimilitud bajo condiciones simplificadas) y declara con precisión los que se admiten. El libro termina con un capítulo dedicado a la dificultad de estimar rendimientos esperados, que motiva gran parte de los libros posteriores.

**Datos dependientes.** El libro supone muestras independientes salvo advertencia. La inferencia con dependencia temporal se desarrolla en L14.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro (NOTACION §7).

## Capítulos

### Capítulo 1. Datos, muestras y estadística descriptiva de rendimientos

**Prerrequisitos:** L8 c. 6, L8 c. 7, L3 c. 9, L3 c. 10, L2 §8.7.

**Objetivos:** distinguir población, muestra y proceso generador de datos; calcular e interpretar medidas de posición, dispersión, asimetría y curtosis; construir la función de distribución empírica y cuantiles empíricos; calcular covarianzas y correlaciones muestrales; anualizar medias y volatilidades explicitando los supuestos; producir histogramas y gráficos cuantil-cuantil.

**Secciones:**

- **1.1** Población, muestra y proceso generador de datos.
- **1.2** Medidas de posición y de dispersión.
- **1.3** Función de distribución empírica y cuantiles empíricos.
- **1.4** Asimetría y curtosis muestrales.
- **1.5** Covarianza y correlación muestrales.
- **1.6** Rendimientos financieros: frecuencia, agregación y anualización con sus supuestos.
- **1.7** Histogramas y gráficos cuantil-cuantil.

**Resultados principales:** propiedades algebraicas de las medidas muestrales.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** descripción de series de rendimientos.

**Usa como aplicación:** L5 §2.1.

**Computación:** estadística descriptiva con pandas.

**Extensión estimada:** 26–32 páginas; 30–40 ejercicios.

### Capítulo 2. Estimadores

**Prerrequisitos:** L9 c. 1, L8 c. 10.

**Objetivos:** formular modelos estadísticos paramétricos; definir estimadores y estadísticos; descomponer el error cuadrático medio en sesgo y varianza; demostrar la consistencia mediante la ley de los grandes números; demostrar el insesgamiento de la media y de la varianza muestral con divisor n − 1; aplicar el criterio de factorización para la suficiencia.

**Secciones:**

- **2.1** Modelos estadísticos paramétricos.
- **2.2** Estimadores y estadísticos.
- **2.3** Sesgo, varianza y error cuadrático medio.
- **2.4** Consistencia.
- **2.5** Insesgamiento de la media y de la varianza muestrales.
- **2.6\*** Suficiencia y criterio de factorización.
- **2.7** Precisión de los estimadores de media y volatilidad según la frecuencia de los datos (anticipo de L9 c. 14).

**Resultados principales:** descomposición sesgo-varianza; insesgamiento de S²; criterio de factorización.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** estimación de media y volatilidad de rendimientos.

**Computación:** distribución simulada de estimadores.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 3. Distribuciones muestrales

**Prerrequisitos:** L9 c. 2, L8 §7.6, L8 §8.7, L6 §7.3, L6 c. 10.

**Objetivos:** derivar la distribución de la media y la varianza muestrales de una muestra normal; demostrar su independencia mediante una transformación ortogonal; demostrar que las formas cuadráticas idempotentes de normales estándar tienen distribución chi-cuadrado; derivar las distribuciones t y F; aproximar distribuciones muestrales mediante el teorema central del límite.

**Secciones:**

- **3.1** Muestras normales.
- **3.2** Independencia de la media y la varianza muestrales.
- **3.3** Formas cuadráticas idempotentes y distribución chi-cuadrado.
- **3.4** Distribución t de Student.
- **3.5** Distribución F de Snedecor.
- **3.6** Distribuciones muestrales aproximadas mediante el teorema central del límite.

**Resultados principales:** independencia de X̄ y S² bajo normalidad; distribución de formas cuadráticas idempotentes; distribuciones de los estadísticos t y F.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** comparación de distribuciones exactas y simuladas.

**Extensión estimada:** 24–30 páginas; 30–40 ejercicios.

### Capítulo 4. Método de los momentos y máxima verosimilitud

**Prerrequisitos:** L9 c. 3, L7 §5.3, L7 c. 6, L8 c. 11, L8 §10.6.

**Objetivos:** construir estimadores por el método de los momentos y por máxima verosimilitud; calcular la información de Fisher y demostrar la cota de Cramér-Rao; demostrar la consistencia y la normalidad asintótica de la máxima verosimilitud bajo condiciones simplificadas explícitas; demostrar y aplicar el método delta; reconocer cuándo la verosimilitud requiere optimización numérica.

**Secciones:**

- **4.1** Método de los momentos.
- **4.2** Verosimilitud y estimador de máxima verosimilitud.
- **4.3** Ejemplos: normal, exponencial, Poisson y lognormal.
- **4.4** Información de Fisher y cota de Cramér-Rao.
- **4.5** Consistencia y normalidad asintótica de la máxima verosimilitud bajo condiciones simplificadas.
- **4.6** Método delta.
- **4.7** Verosimilitudes sin solución cerrada (anticipo de L12).

**Resultados principales:** cota de Cramér-Rao; normalidad asintótica de la máxima verosimilitud (condiciones simplificadas); método delta.

**Resultados admitidos:** RA-14 (en §4.5, caso general).

**Aplicaciones financieras:** estimación de parámetros del modelo lognormal; error estándar del índice de Sharpe por el método delta.

**Computación:** maximización numérica de verosimilitudes sencillas.

**Extensión estimada:** 32–38 páginas; 35–45 ejercicios.

### Capítulo 5. Intervalos de confianza

**Prerrequisitos:** L9 c. 4.

**Objetivos:** definir e interpretar correctamente un intervalo de confianza; construir intervalos exactos mediante cantidades pivotales; construir intervalos asintóticos de Wald; construir intervalos para proporciones; identificar errores frecuentes de interpretación; calcular intervalos para el rendimiento esperado y la volatilidad.

**Secciones:**

- **5.1** Definición e interpretación correcta.
- **5.2** Cantidades pivotales; intervalos para la media y la varianza normales.
- **5.3** Intervalos asintóticos de Wald.
- **5.4** Intervalos para proporciones.
- **5.5** Errores frecuentes de interpretación.
- **5.6** Intervalos para el rendimiento esperado y la volatilidad.

**Resultados principales:** cobertura exacta de los intervalos pivotales; cobertura asintótica de los intervalos de Wald.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** incertidumbre del rendimiento esperado.

**Computación:** comprobación de la cobertura por simulación.

**Extensión estimada:** 22–28 páginas; 30–40 ejercicios.

### Capítulo 6. Contrastes de hipótesis

**Prerrequisitos:** L9 c. 5.

**Objetivos:** formular hipótesis y controlar los errores de tipo I y II; demostrar el lema de Neyman-Pearson; calcular la potencia y el tamaño muestral necesario; aplicar contrastes t, chi-cuadrado y F; construir contrastes de razón de verosimilitud; definir e interpretar correctamente el valor p; relacionar intervalos y contrastes; distinguir significación estadística y económica.

**Secciones:**

- **6.1** Hipótesis y errores de tipo I y II.
- **6.2** Lema de Neyman-Pearson.
- **6.3** Potencia y tamaño muestral.
- **6.4** Contrastes t, chi-cuadrado y F.
- **6.5** Razón de verosimilitud: distribución asintótica en el caso de un parámetro, demostrada; caso multiparamétrico, enunciado.
- **6.6** El valor p: definición, interpretación correcta y errores frecuentes.
- **6.7** Dualidad entre intervalos y contrastes.
- **6.8** Significación estadística y significación económica.

**Resultados principales:** lema de Neyman-Pearson; distribución asintótica de la razón de verosimilitud en un parámetro.

**Resultados admitidos:** RA-29 (en §6.5).

**Aplicaciones financieras:** contrastar si un gestor tiene rendimiento anormal positivo; potencia de esa prueba.

**Computación:** curvas de potencia por simulación.

**Extensión estimada:** 32–38 páginas; 40–50 ejercicios.

### Capítulo 7. Pruebas múltiples

**Prerrequisitos:** L9 c. 6, L8 c. 3.

**Objetivos:** explicar por qué la búsqueda entre muchas hipótesis produce falsos descubrimientos; demostrar el control de la tasa de error familiar de los procedimientos de Bonferroni y Holm; demostrar el control de la tasa de falsos descubrimientos del procedimiento de Benjamini-Hochberg bajo independencia; reconocer el sesgo de selección y la regresión a la media; aplicar correcciones al evaluar muchas señales.

**Secciones:**

- **7.1** El problema: búsqueda de estrategias y falsos descubrimientos.
- **7.2** Tasa de error familiar; procedimientos de Bonferroni y Holm.
- **7.3** Tasa de falsos descubrimientos; procedimiento de Benjamini-Hochberg.
- **7.4** Dependencia entre pruebas: el procedimiento de Benjamini-Yekutieli.
- **7.5** Sesgo de selección y regresión a la media.
- **7.6** Evaluación de muchas señales.

**Resultados principales:** control de la tasa de error familiar por Bonferroni y Holm; control de la tasa de falsos descubrimientos por Benjamini-Hochberg bajo independencia; control bajo dependencia arbitraria por Benjamini-Yekutieli.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** selección de estrategias y factores.

**Computación:** simulación de búsquedas con señales nulas.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

### Capítulo 8. Regresión lineal y teorema de Gauss-Markov

**Prerrequisitos:** L9 c. 3, L6 c. 8, L8 c. 9.

**Objetivos:** formular el modelo de regresión lineal y sus supuestos; obtener el estimador de mínimos cuadrados como proyección; demostrar su insesgamiento y calcular su varianza; demostrar el teorema de Gauss-Markov; derivar las distribuciones de los estimadores bajo normalidad; interpretar el coeficiente de determinación y sus límites; estimar el modelo de mercado.

**Secciones:**

- **8.1** El modelo de regresión lineal y sus supuestos.
- **8.2** Mínimos cuadrados ordinarios como proyección.
- **8.3** Propiedades en muestras finitas: insesgamiento y varianza.
- **8.4** Teorema de Gauss-Markov.
- **8.5** Distribución de los estimadores bajo normalidad.
- **8.6** Coeficiente de determinación y sus límites.
- **8.7** El modelo de mercado como regresión (anticipo de L10 c. 7).

**Resultados principales:** teorema de Gauss-Markov; distribución exacta de los estimadores bajo normalidad.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** estimación de betas.

**Computación:** regresión con NumPy y comparación con bibliotecas.

**Extensión estimada:** 28–34 páginas; 35–45 ejercicios.

### Capítulo 9. Inferencia y diagnóstico en regresión

**Prerrequisitos:** L9 c. 8, L9 c. 6, L9 c. 4.

**Objetivos:** contrastar hipótesis individuales y conjuntas sobre los coeficientes; imponer restricciones lineales; diagnosticar el modelo mediante residuos; demostrar la consistencia de los errores estándar robustos a la heterocedasticidad bajo muestreo independiente; detectar multicolinealidad y observaciones influyentes; analizar el sesgo por variables omitidas; obtener la distribución asintótica de los estimadores sin normalidad.

**Secciones:**

- **9.1** Contrastes t y F sobre coeficientes.
- **9.2** Restricciones lineales.
- **9.3** Residuos y diagnóstico gráfico.
- **9.4** Heterocedasticidad: consecuencias y errores estándar robustos de White.
- **9.5** Multicolinealidad.
- **9.6** Apalancamiento y observaciones influyentes.
- **9.7** Variables omitidas y sesgo.
- **9.8** Teoría asintótica de los mínimos cuadrados sin normalidad.

**Resultados principales:** consistencia de los errores estándar de White bajo muestreo independiente; fórmula del sesgo por variables omitidas; normalidad asintótica de los mínimos cuadrados.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** inferencia sobre alfas y betas.

**Computación:** diagnóstico de regresiones con datos de rendimientos.

**Extensión estimada:** 30–36 páginas; 35–45 ejercicios.

### Capítulo 10. Bootstrap y remuestreo

**Prerrequisitos:** L9 c. 5, L8 c. 13, L3 c. 11.

**Objetivos:** usar la distribución empírica como estimador; construir errores estándar e intervalos bootstrap; explicar cuándo funciona y cuándo falla el bootstrap; aplicar el bootstrap paramétrico; demostrar la validez exacta de las pruebas de permutación; explicar por qué el bootstrap para datos independientes falla con dependencia temporal.

**Secciones:**

- **10.1** La distribución empírica como estimador.
- **10.2** Bootstrap no paramétrico: errores estándar e intervalos percentil y básico.
- **10.3** Por qué funciona y cuándo falla.
- **10.4** Bootstrap paramétrico.
- **10.5** Pruebas de permutación.
- **10.6** Datos dependientes: por qué falla el bootstrap independiente (anticipo de L14 c. 7).

**Resultados principales:** validez exacta de las pruebas de permutación bajo intercambiabilidad.

**Resultados admitidos:** RA-30 (en §10.3).

**Aplicaciones financieras:** intervalos para el índice de Sharpe; comparación de dos estrategias.

**Computación:** implementación del bootstrap y de las pruebas de permutación.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

### Capítulo 11. Inferencia bayesiana introductoria

**Prerrequisitos:** L9 c. 4, L8 c. 3, L8 c. 9, L8 §9.6.

**Objetivos:** obtener distribuciones posteriores a partir de la distribución previa y la verosimilitud; trabajar con familias conjugadas; derivar estimadores bayesianos para distintas funciones de pérdida; distinguir intervalos de credibilidad y de confianza; calcular distribuciones predictivas; interpretar la contracción hacia la distribución previa; analizar la sensibilidad a la elección de la distribución previa.

**Secciones:**

- **11.1** Distribución previa, verosimilitud y distribución posterior.
- **11.2** Familias conjugadas: beta-binomial y normal-normal.
- **11.3** Estimadores bayesianos y funciones de pérdida.
- **11.4** Intervalos de credibilidad e intervalos de confianza.
- **11.5** Distribución predictiva posterior.
- **11.6** Contracción hacia la distribución previa (anticipo de Black-Litterman, L17 c. 3).
- **11.7** Elección de la distribución previa y sensibilidad.

**Resultados principales:** posteriores conjugadas; la media posterior minimiza la pérdida cuadrática esperada.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** estimación bayesiana del rendimiento esperado; actualización de la creencia sobre la habilidad de un gestor.

**Computación:** posteriores conjugadas y su verificación por simulación.

**Extensión estimada:** 26–32 páginas; 30–40 ejercicios.

### Capítulo 12. Validación y sobreajuste

**Prerrequisitos:** L9 c. 8, L9 c. 7.

**Objetivos:** distinguir error de entrenamiento y error de generalización; reconocer el sobreajuste; usar conjuntos de validación y de prueba; aplicar validación cruzada; usar los criterios de información AIC y BIC conociendo su justificación aproximada; identificar el sesgo de selección de modelos; anticipar los problemas de los datos temporales.

**Secciones:**

- **12.1** Error de entrenamiento y error de generalización.
- **12.2** Sobreajuste en la regresión polinómica.
- **12.3** Conjuntos de validación y de prueba.
- **12.4** Validación cruzada.
- **12.5** Criterios de información AIC y BIC: derivación aproximada bajo supuestos de regularidad.
- **12.6** Selección de modelos y sesgo de selección.
- **12.7** Advertencia sobre datos temporales (anticipo de L14 c. 7 y L20 c. 7).

**Resultados principales:** descomposición del error esperado de predicción; optimismo del error de entrenamiento en regresión lineal.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** selección de variables predictivas de rendimientos.

**Computación:** validación cruzada con simulación.

**Extensión estimada:** 24–30 páginas; 25–35 ejercicios.

### Capítulo 13. Estadística multivariante, no paramétrica y robusta

**Prerrequisitos:** L9 c. 4, L9 c. 6, L6 c. 11, L8 §7.6.

**Objetivos:** estimar medias y covarianzas multivariantes; interpretar las componentes principales estadísticas y elegir su número; describir el error de estimación de matrices de covarianza cuando el número de variables es comparable al de observaciones; estimar densidades por núcleos y elegir el ancho de banda; usar estimadores robustos y su punto de ruptura; aplicar pruebas no paramétricas de signos, rangos y Kolmogorov-Smirnov.

**Secciones:**

- **13.1** Estimación de medias y covarianzas multivariantes; distribución de Wishart.
- **13.2** Componentes principales estadísticas y elección del número de componentes.
- **13.3** Error de estimación de covarianzas en alta dimensión (anticipo de L17 c. 2).
- **13.4** Estimación de densidades por núcleos: sesgo, varianza y ancho de banda.
- **13.5** Estimación robusta: mediana, desviación absoluta mediana, M-estimadores y punto de ruptura.
- **13.6** Pruebas no paramétricas: signos, rangos de Wilcoxon y Kolmogorov-Smirnov.

**Resultados principales:** sesgo y varianza asintóticos del estimador de densidad por núcleos; punto de ruptura de la mediana; distribución libre de los estadísticos de rangos y de Kolmogorov-Smirnov bajo la hipótesis nula.

**Resultados admitidos:** RA-31 (en §13.6), RA-32 (en §13.1).

**Aplicaciones financieras:** componentes principales de rendimientos; densidad empírica de pérdidas.

**Computación:** estimación de densidades y componentes principales con datos.

**Extensión estimada:** 32–38 páginas; 30–40 ejercicios.

### Capítulo 14. El problema de estimar rendimientos esperados

**Prerrequisitos:** L9 c. 5, L9 c. 10, L9 c. 11, L9 c. 13.

**Objetivos:** demostrar que el error estándar de la media de rendimientos depende de la longitud del período observado y no de la frecuencia de muestreo, mientras que la precisión de la volatilidad mejora con la frecuencia; cuantificar los años de datos necesarios para detectar primas de riesgo realistas; demostrar el resultado de James-Stein (sección opcional); explicar por qué la teoría económica y la información previa son necesarias.

**Secciones:**

- **14.1** Error estándar de la media de rendimientos.
- **14.2** Frecuencia de muestreo: la volatilidad mejora, la media no.
- **14.3** Consecuencias para la construcción de carteras (anticipo de L17 c. 1).
- **14.4\*** Estimadores de contracción para medias: teorema de James-Stein.
- **14.5** Información previa y teoría económica.
- **14.6** Estudio integrador con datos.

**Resultados principales:** independencia de la precisión de la media respecto de la frecuencia de muestreo bajo rendimientos independientes; teorema de James-Stein.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** simulación de la precisión de estimadores; estudio con datos.

**Extensión estimada:** 22–28 páginas; 20–30 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; tablas de las distribuciones t, chi-cuadrado y F; índice de símbolos; índice analítico.
