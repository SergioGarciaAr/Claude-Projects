# L14. Econometría y series temporales financieras

Índice detallado · Versión 1.0 · Entrega 1c · 2026-10-16

## Ficha editorial

- **Serie:** III. Teoría financiera y modelización.
- **Requisitos:** L3, L6, L9, L10, L12.
- **Capítulos:** 15, más un apéndice.
- **Extensión estimada:** 436–536 páginas.

**Propósito.** Este libro desarrolla la econometría necesaria para el trabajo empírico en finanzas: regresión con errores no esféricos, endogeneidad, procesos estacionarios y no estacionarios, modelos ARMA, volatilidad condicional, modelos multivariantes, cointegración, cambios de régimen, regresiones de corte transversal, método generalizado de momentos, contraste de modelos de valoración y filtro de Kalman. La teoría asintótica para datos dependientes se usa extensamente; sus resultados generales se admiten con referencia y se demuestran los casos que el lector puede seguir con sus prerrequisitos.

**Resultados asintóticos admitidos.** Este libro concentra varios resultados admitidos (RA-11 a RA-13 y RA-36 a RA-41). Cada uno se acompaña de una ilustración por simulación que muestra su contenido, sin presentarla como demostración.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; notación del libro.

## Capítulos

### Capítulo 1. Hechos estilizados de los rendimientos financieros

**Prerrequisitos:** L9 c. 1, L9 c. 13, L10 c. 4, L3 c. 9.

**Objetivos:** describir las fuentes y frecuencias de datos de precios; documentar colas pesadas, ausencia de autocorrelación lineal, agrupamiento de volatilidad, efecto apalancamiento y normalidad agregada; distinguir regularidades empíricas de leyes; reproducir los hechos con datos.

**Secciones:**

- **1.1** Datos de precios y rendimientos: fuentes y frecuencias.
- **1.2** Colas pesadas.
- **1.3** Ausencia de autocorrelación lineal en los rendimientos.
- **1.4** Agrupamiento de la volatilidad.
- **1.5** Efecto apalancamiento.
- **1.6** Normalidad agregada.
- **1.7** Los hechos estilizados como resultados empíricos, no como leyes.

**Resultados principales:** no corresponde; capítulo empírico.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** reproducción de los hechos con datos (fuente por verificar en 1e).

**Extensión estimada:** 22–28 páginas; 15–25 ejercicios.

### Capítulo 2. Regresión matricial, mínimos cuadrados generalizados y errores HAC

**Prerrequisitos:** L9 c. 8, L9 c. 9, L6 c. 10.

**Objetivos:** repasar la teoría asintótica del modelo lineal; demostrar el teorema de Aitken para mínimos cuadrados generalizados; aplicar mínimos cuadrados generalizados factibles; usar errores robustos a la heterocedasticidad y a la autocorrelación; elegir el ancho de banda; hacer inferencia con rendimientos de horizontes superpuestos.

**Secciones:**

- **2.1** El modelo lineal en forma matricial y su teoría asintótica.
- **2.2** Mínimos cuadrados generalizados: teorema de Aitken.
- **2.3** Mínimos cuadrados generalizados factibles.
- **2.4** Errores robustos a la heterocedasticidad.
- **2.5** Autocorrelación: consecuencias y errores de Newey-West.
- **2.6** Elección del ancho de banda.
- **2.7** Regresiones con horizontes superpuestos.

**Resultados principales:** teorema de Aitken; sesgo de los errores convencionales bajo autocorrelación.

**Resultados admitidos:** RA-12 (en §2.5).

**Aplicaciones financieras:** regresiones de predictibilidad de rendimientos a largo plazo.

**Computación:** comparación de errores estándar por simulación.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

### Capítulo 3. Endogeneidad, variables instrumentales y causalidad

**Prerrequisitos:** L14 c. 2.

**Objetivos:** identificar las fuentes de endogeneidad; demostrar el sesgo de atenuación por errores en las variables; construir estimadores de variables instrumentales y de mínimos cuadrados en dos etapas y demostrar su consistencia; ilustrar el problema de los instrumentos débiles; formular preguntas causales con resultados potenciales; reconocer la endogeneidad en aplicaciones financieras.

**Secciones:**

- **3.1** Fuentes de endogeneidad: variables omitidas, errores en las variables y simultaneidad.
- **3.2** Variables instrumentales y mínimos cuadrados en dos etapas.
- **3.3** Instrumentos débiles: ilustración por simulación.
- **3.4** Resultados potenciales; correlación y causalidad.
- **3.5** Ejemplo: errores en las variables en la estimación de betas.

**Resultados principales:** sesgo de atenuación; consistencia de variables instrumentales.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** estimación de betas y de efectos de políticas corporativas.

**Computación:** simulación de sesgos e instrumentos débiles.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 4. Procesos estocásticos en tiempo discreto

**Prerrequisitos:** L9 c. 2, L8 c. 10, L6 §9.7, L2 c. 12.

**Objetivos:** definir procesos estacionarios en sentido estricto y débil; demostrar las propiedades de la función de autocovarianza; distinguir ruido blanco, diferencia de martingala e independencia; enunciar las leyes de los grandes números para procesos dependientes; resolver ecuaciones en diferencias lineales y caracterizar su estabilidad por las raíces del polinomio característico; operar con el operador de rezagos.

**Secciones:**

- **4.1** Procesos estocásticos en tiempo discreto.
- **4.2** Estacionariedad estricta y débil.
- **4.3** Autocovarianza y autocorrelación.
- **4.4** Ruido blanco, diferencia de martingala e independencia.
- **4.5** Ergodicidad y leyes de los grandes números para procesos dependientes.
- **4.6** Ecuaciones en diferencias lineales y estabilidad.
- **4.7** Operador de rezagos y su inversión.

**Resultados principales:** la autocovarianza es semidefinida positiva; solución general y criterio de estabilidad de las ecuaciones en diferencias.

**Resultados admitidos:** RA-13 (en §4.5).

**Aplicaciones financieras:** rendimientos como diferencia de martingala.

**Computación:** autocorrelaciones muestrales.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 5. Modelos ARMA

**Prerrequisitos:** L14 c. 4, L9 c. 4, L9 §12.5.

**Objetivos:** estudiar procesos MA(q) y AR(p); demostrar la condición de estacionariedad de los AR y su representación MA(∞); definir causalidad e invertibilidad de los ARMA; identificar modelos mediante autocorrelaciones simples y parciales; estimar por Yule-Walker y por máxima verosimilitud; diagnosticar residuos; seleccionar modelos por criterios de información.

**Secciones:**

- **5.1** Procesos de medias móviles.
- **5.2** Procesos autorregresivos: estacionariedad y representación MA(∞).
- **5.3** Procesos ARMA: causalidad e invertibilidad.
- **5.4** Autocorrelación simple y parcial; identificación.
- **5.5** Estimación: Yule-Walker y máxima verosimilitud.
- **5.6** Diagnóstico de residuos; prueba de Ljung-Box.
- **5.7** Selección de modelos.

**Resultados principales:** condición de estacionariedad de los AR; ecuaciones de Yule-Walker.

**Resultados admitidos:** RA-41 (en §5.6).

**Aplicaciones financieras:** modelos de tasas de interés y de spreads en tiempo discreto.

**Computación:** estimación y diagnóstico de modelos ARMA.

**Extensión estimada:** 32–38 páginas; 30–40 ejercicios.

### Capítulo 6. Raíces unitarias y regresiones espurias

**Prerrequisitos:** L14 c. 5, L12 c. 9.

**Objetivos:** distinguir procesos integrados y estacionarios; distinguir tendencias deterministas y estocásticas; demostrar por simulación y explicar la regresión espuria; aplicar las pruebas de Dickey-Fuller y KPSS obteniendo valores críticos por simulación; reconocer la baja potencia de estas pruebas; elegir transformaciones.

**Secciones:**

- **6.1** Paseo aleatorio y procesos integrados.
- **6.2** Tendencia determinista y tendencia estocástica.
- **6.3** Regresión espuria.
- **6.4** Pruebas de Dickey-Fuller y Dickey-Fuller aumentada.
- **6.5** Prueba KPSS.
- **6.6** Potencia de las pruebas y consecuencias prácticas.
- **6.7** Diferenciación y transformaciones.

**Resultados principales:** varianza creciente de los procesos integrados; inconsistencia del estimador en la regresión espuria (ilustrada).

**Resultados admitidos:** RA-11 (en §6.4), RA-41 (en §6.5).

**Aplicaciones financieras:** precios, tasas y spreads: ¿estacionarios o integrados?

**Computación:** valores críticos de Dickey-Fuller por simulación.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 7. Pronóstico, validación temporal y bootstrap para datos dependientes

**Prerrequisitos:** L14 c. 5, L9 c. 10, L9 c. 12, L8 §9.5.

**Objetivos:** derivar el pronóstico óptimo bajo pérdida cuadrática y los pronósticos de modelos ARMA; construir intervalos de pronóstico; evaluar fuera de muestra con ventanas fija, móvil y expansiva; comparar pronósticos con la prueba de Diebold-Mariano; aplicar el bootstrap por bloques; identificar fugas de información temporal.

**Secciones:**

- **7.1** Pronóstico óptimo y pronósticos ARMA.
- **7.2** Intervalos de pronóstico.
- **7.3** Evaluación fuera de muestra: ventanas fija, móvil y expansiva.
- **7.4** Comparación de pronósticos: prueba de Diebold-Mariano.
- **7.5** Bootstrap por bloques móviles y bootstrap estacionario.
- **7.6** Fuga de información temporal: errores frecuentes.

**Resultados principales:** optimalidad de la esperanza condicional; fórmulas de pronóstico ARMA.

**Resultados admitidos:** RA-36 (en §7.5), RA-41 (en §7.4).

**Aplicaciones financieras:** evaluación de modelos de predicción de rendimientos y volatilidad.

**Computación:** evaluación fuera de muestra y bootstrap por bloques.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

### Capítulo 8. Volatilidad condicional: ARCH y GARCH

**Prerrequisitos:** L14 c. 5, L9 c. 4, L12 c. 6.

**Objetivos:** definir la volatilidad condicional; estudiar los modelos ARCH y GARCH; demostrar la condición de estacionariedad en covarianza del GARCH(1,1) y calcular su curtosis; estimar por máxima verosimilitud y cuasi máxima verosimilitud; usar extensiones asimétricas y con distribución t; pronosticar volatilidad y evaluar pronósticos; introducir la volatilidad realizada.

**Secciones:**

- **8.1** Volatilidad condicional.
- **8.2** Modelos ARCH.
- **8.3** GARCH(1,1): estacionariedad en covarianza y curtosis.
- **8.4** Estimación por máxima verosimilitud y cuasi máxima verosimilitud.
- **8.5** Extensiones: EGARCH, GJR y distribuciones t.
- **8.6** Pronóstico de volatilidad y su evaluación.
- **8.7** Volatilidad realizada (introducción; teoría en L18 y especialización).

**Resultados principales:** condición de estacionariedad en covarianza del GARCH(1,1); fórmula de la curtosis; pronósticos de varianza a varios pasos.

**Resultados admitidos:** RA-37 (en §8.4).

**Aplicaciones financieras:** pronóstico de volatilidad; VaR condicional (anticipo de L17 c. 7).

**Computación:** estimación de modelos GARCH con datos.

**Extensión estimada:** 30–36 páginas; 25–35 ejercicios.

### Capítulo 9. Vectores autorregresivos y causalidad de Granger

**Prerrequisitos:** L14 c. 5, L6 c. 9.

**Objetivos:** caracterizar la estacionariedad de un VAR mediante la matriz compañera; demostrar que la estimación ecuación por ecuación es eficiente cuando todas las ecuaciones comparten regresores; calcular funciones de impulso-respuesta y reconocer la arbitrariedad de la identificación recursiva; descomponer la varianza del error de pronóstico; aplicar e interpretar correctamente la prueba de causalidad de Granger.

**Secciones:**

- **9.1** VAR(p): estacionariedad mediante la matriz compañera.
- **9.2** Estimación ecuación por ecuación.
- **9.3** Funciones de impulso-respuesta e identificación recursiva.
- **9.4** Descomposición de la varianza del error de pronóstico.
- **9.5** Causalidad de Granger: definición, prueba y lo que no significa.

**Resultados principales:** criterio de estacionariedad del VAR; equivalencia de la estimación ecuación por ecuación.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** interacción entre rendimientos, volumen y variables macroeconómicas.

**Computación:** estimación de VAR y funciones de impulso-respuesta.

**Extensión estimada:** 26–32 páginas; 20–30 ejercicios.

### Capítulo 10. Cointegración

**Prerrequisitos:** L14 c. 6, L14 c. 9.

**Objetivos:** definir cointegración y vectores de cointegración; enunciar el teorema de representación de Granger y demostrar el caso bivariado; aplicar el método de Engle-Granger y el de Johansen; formular modelos de corrección de errores; evaluar críticamente estrategias de pares.

**Secciones:**

- **10.1** Cointegración y vector de cointegración.
- **10.2** Teorema de representación de Granger: caso bivariado demostrado.
- **10.3** Método de Engle-Granger.
- **10.4** Método de Johansen.
- **10.5** Modelos de corrección de errores.
- **10.6** Estrategias de pares y sus riesgos: inestabilidad de los parámetros.

**Resultados principales:** representación de corrección de errores en el caso bivariado.

**Resultados admitidos:** RA-38 (en §10.2).

**Aplicaciones financieras:** estrategias de pares; relaciones entre tasas.

**Computación:** pruebas de cointegración con datos simulados y reales.

**Extensión estimada:** 26–32 páginas; 20–30 ejercicios.

### Capítulo 11. Rupturas estructurales y cambios de régimen

**Prerrequisitos:** L14 c. 5, L8 c. 3, L8 c. 14, L12 c. 6.

**Objetivos:** reconocer la inestabilidad de parámetros en finanzas; aplicar la prueba de Chow con fecha conocida; usar estadísticos de supremo con fecha desconocida; derivar el filtro de Hamilton para modelos de cambio de régimen markoviano y estimarlos por máxima verosimilitud; extraer consecuencias para la evaluación de estrategias.

**Secciones:**

- **11.1** Inestabilidad de parámetros en finanzas.
- **11.2** Prueba de Chow con fecha conocida.
- **11.3** Fecha desconocida: estadísticos de supremo.
- **11.4** Modelos de cambio de régimen markoviano: filtro de Hamilton y estimación.
- **11.5** Consecuencias para la evaluación de estrategias (anticipo de L20).

**Resultados principales:** derivación del filtro de Hamilton.

**Resultados admitidos:** RA-39 (en §11.3).

**Aplicaciones financieras:** regímenes de volatilidad y de mercado.

**Computación:** estimación de un modelo de cambio de régimen.

**Extensión estimada:** 24–30 páginas; 20–30 ejercicios.

### Capítulo 12. Regresiones de corte transversal y procedimiento de Fama-MacBeth

**Prerrequisitos:** L14 c. 2, L10 c. 7, L10 c. 10.

**Objetivos:** estimar regresiones de corte transversal de rendimientos sobre betas y características; derivar los estimadores y errores estándar de Fama-MacBeth; derivar la corrección de Shanken por errores en las variables; comparar carteras ordenadas y regresiones; usar efectos fijos y errores agrupados en datos de panel.

**Secciones:**

- **12.1** Regresiones de corte transversal de rendimientos.
- **12.2** Procedimiento de Fama-MacBeth: estimadores y errores estándar.
- **12.3** Errores en las variables y corrección de Shanken.
- **12.4** Carteras ordenadas frente a regresiones.
- **12.5** Datos de panel: efectos fijos y errores agrupados.

**Resultados principales:** propiedades del estimador de Fama-MacBeth bajo sus supuestos; corrección de Shanken.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** contraste de premios por factores y características.

**Computación:** Fama-MacBeth con datos de carteras (fuente por verificar en 1e).

**Extensión estimada:** 26–32 páginas; 20–30 ejercicios.

### Capítulo 13. Método generalizado de momentos

**Prerrequisitos:** L14 c. 2, L9 c. 4, L12 c. 6.

**Objetivos:** formular condiciones de momentos; definir el estimador MGM; demostrar su consistencia y normalidad asintótica bajo condiciones simplificadas; demostrar la eficiencia de la matriz de ponderación óptima; aplicar el estimador en dos etapas; usar la prueba J de sobreidentificación; reconocer mínimos cuadrados, variables instrumentales y máxima verosimilitud como casos particulares.

**Secciones:**

- **13.1** Condiciones de momentos.
- **13.2** El estimador MGM.
- **13.3** Consistencia y normalidad asintótica.
- **13.4** Matriz de ponderación óptima; estimación en dos etapas.
- **13.5** Prueba J de sobreidentificación.
- **13.6** Mínimos cuadrados, variables instrumentales y máxima verosimilitud como casos particulares.

**Resultados principales:** normalidad asintótica bajo condiciones simplificadas; optimalidad de la matriz de ponderación.

**Resultados admitidos:** RA-40 (en §13.3), RA-41 (en §13.5).

**Aplicaciones financieras:** estimación de modelos de factor de descuento.

**Computación:** implementación del MGM en dos etapas.

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

### Capítulo 14. Contraste de modelos de valoración de activos

**Prerrequisitos:** L14 c. 12, L14 c. 13, L10 c. 9, L9 c. 3.

**Objetivos:** derivar la prueba GRS bajo normalidad; aplicar pruebas de corte transversal; estimar modelos de factor de descuento por MGM mediante ecuaciones de Euler; calcular la distancia de Hansen-Jagannathan; resumir la evidencia sobre el CAPM y los modelos multifactoriales; identificar los problemas de carteras de prueba, potencia y minería de datos.

**Secciones:**

- **14.1** Pruebas de series temporales: prueba GRS.
- **14.2** Pruebas de corte transversal.
- **14.3** Modelos de factor de descuento por MGM: ecuaciones de Euler.
- **14.4** Distancia de Hansen-Jagannathan.
- **14.5** Evidencia sobre el CAPM y los modelos multifactoriales (resultados empíricos).
- **14.6** Carteras de prueba, potencia y minería de datos.

**Resultados principales:** distribución F exacta de la prueba GRS bajo normalidad.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** contraste de modelos de factores con datos.

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

### Capítulo 15. Modelos de espacio de estados y filtro de Kalman

**Prerrequisitos:** L14 c. 4, L8 §9.6, L9 c. 4, L12 c. 6.

**Objetivos:** formular modelos de espacio de estados lineales y gaussianos; derivar el filtro de Kalman a partir de la distribución condicional de la normal multivariante; derivar y aplicar el suavizador; calcular la verosimilitud mediante los errores de predicción y estimar por máxima verosimilitud; aplicar el filtro a betas variables en el tiempo y a modelos dinámicos de curvas de tasas.

**Secciones:**

- **15.1** Modelos de espacio de estados lineales y gaussianos.
- **15.2** Filtro de Kalman.
- **15.3** Suavizado de Rauch-Tung-Striebel.
- **15.4** Verosimilitud mediante errores de predicción y estimación.
- **15.5** Aplicaciones: betas variables y Nelson-Siegel dinámico.
- **15.6** Extensiones no lineales (presentación).

**Resultados principales:** derivación del filtro de Kalman; descomposición de la verosimilitud por errores de predicción; derivación del suavizador.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** betas variables; dinámica de curvas de tasas.

**Computación:** implementación del filtro y del suavizador.

**Extensión estimada:** 28–34 páginas; 20–30 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
