# L1. Lenguaje matemático, números y álgebra

Índice detallado · Versión 1.0 · Entrega 1b · 2026-10-16

## Ficha editorial

- **Serie:** I. Fundamentos.
- **Requisitos:** ninguno.
- **Conocimientos de entrada:** lectura comprensiva en español y operaciones aritméticas elementales con números naturales (sumar, restar, multiplicar y dividir números pequeños). Todo lo demás se desarrolla en el libro.
- **Capítulos:** 14, más dos apéndices.
- **Extensión estimada:** 390–470 páginas.

**Propósito.** Este libro enseña a leer, escribir y verificar matemática. Parte de la idea de afirmación matemática, construye la lógica y el lenguaje de conjuntos, enseña los métodos de demostración y los aplica a la construcción ordenada de los sistemas numéricos hasta los números reales. Sobre esa base desarrolla las potencias, los logaritmos y el álgebra elemental, y termina con los primeros algoritmos programados en Python. Las finanzas aparecen como aplicación elemental: porcentajes, interés simple y compuesto, préstamos sencillos.

**Rutas de lectura.** Lectura completa en orden. Las secciones marcadas con asterisco (\*) contienen demostraciones o temas que pueden omitirse en una primera lectura sin perder el hilo; los resultados que establecen sí se usan después.

## Preliminares

Portada; créditos; prefacio (incluye la nota sobre la elaboración de la obra); guía del lector (cómo estudiar matemáticas, cómo leer una demostración, cómo usar los ejercicios y el solucionario, cómo usar el código); notación del libro.

## Capítulos

### Capítulo 1. Qué es una afirmación matemática

**Prerrequisitos:** ninguno.

**Objetivos:** distinguir definición, enunciado, conjetura y demostración; identificar hipótesis y conclusión en un enunciado; reconocer cuándo un ejemplo refuta un enunciado y cuándo no prueba nada; reescribir con precisión un enunciado ambiguo del lenguaje común.

**Secciones:**

- **1.1** Por qué la matemática exige precisión. Ambigüedades del lenguaje común; el ejemplo de «un rendimiento del 10 %» y las preguntas que deja abiertas.
- **1.2** Objetos, definiciones y nombres. Qué significa definir; definiciones circulares; las variables como nombres de objetos.
- **1.3** Enunciados: hipótesis y conclusión. La forma «si…, entonces…»; enunciados generales y de existencia, en lenguaje natural.
- **1.4** La demostración como argumento verificable. Primer ejemplo completo: la suma de dos números pares es par.
- **1.5** Contraejemplos y conjeturas. El polinomio n² + n + 41 y los límites de comprobar casos.
- **1.6** Ejemplos, intuición y demostración: qué establece cada uno. Por qué un cálculo numérico, por extenso que sea, no demuestra un enunciado general.
- **1.7** Cómo leer y estudiar un texto matemático. Lectura activa, reconstrucción de pasos, verificación de ejemplos.

**Resultados principales:** ninguno formal; el capítulo establece el vocabulario de la obra.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** precisión en la formulación de tasas y rendimientos.

**Computación:** no corresponde.

**Extensión estimada:** 22–28 páginas; 25–35 ejercicios.

### Capítulo 2. Lógica proposicional y cuantificadores

**Prerrequisitos:** L1 §1.3, L1 §1.4.

**Objetivos:** construir tablas de verdad; decidir si dos proposiciones son lógicamente equivalentes; formular el recíproco y el contrarrecíproco de una implicación; negar correctamente enunciados con cuantificadores; explicar por qué el orden de los cuantificadores cambia el significado.

**Secciones:**

- **2.1** Proposiciones y conectivos lógicos.
- **2.2** Tablas de verdad y equivalencias lógicas. Leyes de De Morgan y distributivas.
- **2.3** La implicación. Condición necesaria y condición suficiente; recíproco y contrarrecíproco.
- **2.4** Tautologías, contradicciones y reglas de inferencia. *Modus ponens* y *modus tollens*.
- **2.5** Predicados y cuantificadores universal y existencial.
- **2.6** Negación de enunciados cuantificados y orden de los cuantificadores. Preparación para las definiciones con ε y N.
- **2.7** Del lenguaje natural al lenguaje formal. Errores frecuentes; cláusulas de un contrato como ejemplo de lógica aplicada.

**Resultados principales:** equivalencia entre una implicación y su contrarrecíproco; reglas de negación de cuantificadores.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** lectura lógica de condiciones contractuales.

**Computación:** no corresponde.

**Extensión estimada:** 26–32 páginas; 35–45 ejercicios.

### Capítulo 3. Conjuntos, relaciones y funciones

**Prerrequisitos:** L1 §2.2, L1 §2.5, L1 §2.6.

**Objetivos:** operar con conjuntos y demostrar identidades entre ellos; reconocer relaciones de equivalencia y de orden; determinar si una función es inyectiva, sobreyectiva o biyectiva; construir la inversa de una biyección.

**Secciones:**

- **3.1** Conjuntos, pertenencia, igualdad y subconjuntos.
- **3.2** Operaciones con conjuntos. Leyes de De Morgan demostradas a partir de la lógica.
- **3.3** Pares ordenados y producto cartesiano.
- **3.4** Relaciones; relaciones de equivalencia y particiones.
- **3.5** Relaciones de orden.
- **3.6** Funciones: dominio, codominio, imagen y composición.
- **3.7** Funciones inyectivas, sobreyectivas y biyectivas; función inversa.
- **3.8\*** Conjuntos finitos, infinitos y numerables.

**Resultados principales:** correspondencia entre relaciones de equivalencia y particiones; existencia de inversa si y solo si la función es biyectiva.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** clasificación de activos como relación de equivalencia; ordenamiento de inversiones como relación de orden.

**Computación:** no corresponde.

**Extensión estimada:** 28–34 páginas; 40–50 ejercicios.

### Capítulo 4. Métodos de demostración

**Prerrequisitos:** L1 c. 2, L1 §3.1, L1 §3.2, L1 §3.6.

**Objetivos:** elegir y aplicar el método de demostración adecuado (directo, contrarrecíproco, absurdo, casos); demostrar enunciados de existencia y de unicidad; construir contraejemplos; demostrar enunciados sobre números naturales por inducción simple y fuerte; redactar una demostración legible.

**Secciones:**

- **4.1** Demostración directa.
- **4.2** Demostración por contrarrecíproco.
- **4.3** Demostración por reducción al absurdo.
- **4.4** Demostración por casos.
- **4.5** Existencia, unicidad y contraejemplos.
- **4.6** El principio de inducción matemática; inducción fuerte. El principio se presenta como propiedad fundamental de los números naturales; el capítulo 5 lo relaciona con el buen orden.
- **4.7** Aplicaciones de la inducción: fórmulas de sumas finitas y desigualdades entre naturales.
- **4.8** Cómo escribir una demostración. Estructura, redacción y errores frecuentes: circularidad, demostrar el recíproco, generalizar desde ejemplos.

**Resultados principales:** fórmula de la suma 1 + 2 + ⋯ + n; desigualdad 2ⁿ > n.

**Resultados admitidos:** ninguno. El principio de inducción es un axioma de los números naturales, no un resultado admitido.

**Aplicaciones financieras:** no corresponde.

**Computación:** no corresponde.

**Extensión estimada:** 30–36 páginas; 45–60 ejercicios.

### Capítulo 5. Números naturales y enteros

**Prerrequisitos:** L1 §3.4, L1 §3.5, L1 §4.6, L1 §4.7.

**Objetivos:** demostrar las reglas de los signos a partir de las propiedades de las operaciones; demostrar la existencia y unicidad de la división euclídea; calcular el máximo común divisor con el algoritmo de Euclides y obtener la identidad de Bézout; demostrar la infinitud de los primos y el teorema fundamental de la aritmética; operar con congruencias.

**Secciones:**

- **5.1** Los números naturales. Propiedades de la suma y el producto; el principio del buen orden y su equivalencia con la inducción.
- **5.2** Los números enteros. Opuesto, resta y reglas de los signos demostradas.
- **5.3** Divisibilidad y sus propiedades.
- **5.4** División euclídea: existencia y unicidad.
- **5.5** Máximo común divisor, algoritmo de Euclides e identidad de Bézout.
- **5.6** Números primos. Infinitud de los primos; teorema fundamental de la aritmética.
- **5.7** Congruencias y aritmética modular elemental. Calendarios y períodos como ejemplo.

**Resultados principales:** teorema de la división euclídea; corrección del algoritmo de Euclides; identidad de Bézout; lema de Euclides; teorema fundamental de la aritmética.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** conteo de períodos y fechas mediante aritmética modular.

**Computación:** el algoritmo de Euclides se describe paso a paso; su programación se hace en L1 c. 14.

**Extensión estimada:** 28–34 páginas; 40–55 ejercicios.

### Capítulo 6. Números racionales

**Prerrequisitos:** L1 §3.4, L1 §5.2, L1 §5.4, L1 §5.5.

**Objetivos:** operar con fracciones justificando cada propiedad; demostrar que entre dos racionales hay otro racional; caracterizar las expresiones decimales de los racionales; resolver problemas de proporcionalidad; calcular e interpretar porcentajes, puntos porcentuales y variaciones porcentuales sucesivas; calcular interés simple.

**Secciones:**

- **6.1** Fracciones y su equivalencia, como relación de equivalencia entre pares de enteros.
- **6.2** Operaciones con fracciones y sus propiedades; inversos.
- **6.3** Orden de los racionales y densidad.
- **6.4** Expresión decimal de los racionales: finita o periódica.
- **6.5** Razones y proporciones; proporcionalidad directa e inversa.
- **6.6** Porcentajes. Porcentaje de un porcentaje; diferencia entre puntos porcentuales y variación porcentual.
- **6.7** Variaciones porcentuales sucesivas. Asimetría entre subas y bajas; rendimiento simple de una inversión.
- **6.8** Interés simple como aplicación de la proporcionalidad.

**Resultados principales:** buena definición de las operaciones con fracciones; densidad de ℚ; caracterización de las expresiones decimales periódicas.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** porcentajes, comisiones, rendimiento simple, interés simple.

**Computación:** cálculos con Python como calculadora (L1 ap. A).

**Extensión estimada:** 28–34 páginas; 45–60 ejercicios.

### Capítulo 7. Números reales

**Prerrequisitos:** L1 §3.5, L1 §4.3, L1 §6.3, L1 §6.4.

**Objetivos:** demostrar que ningún racional tiene cuadrado igual a 2; deducir propiedades algebraicas y de orden a partir de los axiomas de los reales; resolver desigualdades y usar la desigualdad triangular; calcular supremos e ínfimos; demostrar la propiedad arquimediana, la densidad de los racionales y la existencia de la raíz cuadrada de 2 a partir del axioma del supremo.

**Secciones:**

- **7.1** Insuficiencia de los racionales: no existe un racional cuyo cuadrado sea 2.
- **7.2** Los reales como cuerpo ordenado. Axiomas de cuerpo y de orden; consecuencias algebraicas.
- **7.3** Valor absoluto y desigualdad triangular.
- **7.4** Desigualdades: propiedades y resolución.
- **7.5** Cotas, máximo, mínimo, supremo e ínfimo.
- **7.6** El axioma del supremo.
- **7.7** Propiedad arquimediana y densidad de los racionales en los reales.
- **7.8** Existencia de la raíz cuadrada de 2.
- **7.9** Expresión decimal de un número real y aproximación por truncamiento, con cota del error.

**Resultados principales:** irracionalidad de √2; desigualdad triangular; propiedad arquimediana; densidad de ℚ en ℝ; existencia de √2.

**Resultados admitidos:** ninguno. El axioma del supremo es un axioma de los reales; su construcción a partir de los racionales se hace en L11 c. 1.

**Aplicaciones financieras:** no corresponde.

**Computación:** aproximaciones decimales de √2 (L1 ap. A).

**Extensión estimada:** 32–38 páginas; 45–60 ejercicios.

### Capítulo 8. Potencias, raíces y logaritmos (capítulo piloto)

**Prerrequisitos:** L1 §4.6, L1 §6.2, L1 §6.7, L1 §6.8, L1 §7.2, L1 §7.4, L1 §7.6, L1 §7.8, L1 ap. A.

**Objetivos:** demostrar las leyes de los exponentes enteros y racionales; justificar por qué a⁰ = 1 y a⁻ⁿ = 1/aⁿ; usar la existencia de raíces n-ésimas y, en la sección opcional, demostrarla; comparar potencias según base y exponente; demostrar la desigualdad de Bernoulli y usarla para comparar interés simple y compuesto; definir el logaritmo y demostrar sus propiedades a partir de las de las potencias; resolver problemas de interés compuesto, tasas equivalentes y tiempo de duplicación; evaluar la regla del 72 como aproximación.

**Secciones:**

- **8.1** Potencias de exponente natural. Definición recursiva; leyes demostradas por inducción.
- **8.2** Exponente cero y exponentes enteros negativos. Por qué estas definiciones son las únicas compatibles con las leyes; leyes de los exponentes enteros.
- **8.3** Raíces n-ésimas. Definición, unicidad y uso de su existencia.
- **8.4\*** Demostración de la existencia de raíces n-ésimas a partir del axioma del supremo, generalizando L1 §7.8; identidad aⁿ − bⁿ = (a − b)(aⁿ⁻¹ + aⁿ⁻²b + ⋯ + bⁿ⁻¹).
- **8.5** Exponentes racionales. Buena definición e independencia de la fracción elegida; leyes de los exponentes racionales.
- **8.6** Monotonía de las potencias respecto de la base y del exponente.
- **8.7** Desigualdad de Bernoulli. Comparación entre interés simple y compuesto.
- **8.8** Exponentes reales: idea mediante aproximaciones racionales y uso como resultado admitido.
- **8.9** Logaritmos. Definición, propiedades demostradas a partir de las leyes de los exponentes, cambio de base.
- **8.10** Aplicaciones financieras. Interés compuesto, tasa equivalente entre períodos, tiempo de duplicación, regla del 72 como aproximación con exploración numérica de su error.
- **8.11** Cálculo con Python. Potencias y logaritmos en la calculadora; primeras observaciones sobre redondeo.

**Resultados principales:** leyes de los exponentes enteros y racionales; existencia y unicidad de raíces n-ésimas positivas; monotonía de las potencias; desigualdad de Bernoulli; propiedades de los logaritmos.

**Resultados admitidos:** RA-02, RA-03, RA-05.

**Aplicaciones financieras:** capitalización compuesta, tasas equivalentes, tiempo de duplicación, regla del 72.

**Computación:** Python como calculadora (L1 ap. A); comparación numérica entre la regla del 72 y el tiempo de duplicación exacto.

**Extensión estimada:** 34–40 páginas; 45–60 ejercicios.

### Capítulo 9. Magnitudes, unidades, órdenes de magnitud y error

**Prerrequisitos:** L1 §7.3, L1 §7.9, L1 §8.2, L1 §8.9.

**Objetivos:** verificar la coherencia dimensional de una fórmula; expresar cantidades en notación científica y estimar órdenes de magnitud; redondear correctamente y declarar cifras significativas; acotar el error absoluto y relativo de sumas y productos; convertir números entre bases; explicar por qué una computadora no representa exactamente la mayoría de los números reales.

**Secciones:**

- **9.1** Magnitudes y unidades; análisis dimensional. Unidades en finanzas: unidades monetarias, tasas por período, tiempo en años.
- **9.2** Notación científica y órdenes de magnitud.
- **9.3** Aproximación, redondeo y cifras significativas.
- **9.4** Error absoluto y relativo; propagación del error en sumas y productos, con cotas demostradas.
- **9.5** Sistemas de numeración posicional; base binaria.
- **9.6** Cómo representa números una computadora: enteros y punto flotante (introducción; el estudio completo está en L3 c. 2).
- **9.7** Errores de cálculo en finanzas: redondeo de montos y acumulación de errores.

**Resultados principales:** cotas de propagación del error relativo en productos y cocientes.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** coherencia de unidades en fórmulas de interés; redondeo de montos.

**Computación:** ejemplos de representación inexacta con Python (L1 ap. A).

**Extensión estimada:** 24–30 páginas; 35–45 ejercicios.

### Capítulo 10. Polinomios

**Prerrequisitos:** L1 §5.4, L1 §7.2, L1 §8.1, L1 §8.2.

**Objetivos:** operar con polinomios y fracciones algebraicas; factorizar mediante productos notables; dividir polinomios y demostrar el algoritmo de la división; usar los teoremas del resto y del factor; demostrar que un polinomio no nulo de grado n tiene a lo sumo n raíces; demostrar el teorema del binomio.

**Secciones:**

- **10.1** Expresiones algebraicas y su evaluación.
- **10.2** Polinomios: grado, igualdad y operaciones.
- **10.3** Productos notables y factorización.
- **10.4** División de polinomios: existencia y unicidad del cociente y el resto.
- **10.5** Teorema del resto y teorema del factor.
- **10.6** Número de raíces de un polinomio.
- **10.7** Coeficientes binomiales, triángulo de Pascal y teorema del binomio.
- **10.8** Fracciones algebraicas: simplificación y operaciones.

**Resultados principales:** algoritmo de la división; teorema del factor; cota del número de raíces; identidad de Pascal; teorema del binomio.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** el valor futuro de una serie de depósitos como polinomio en el factor de acumulación.

**Computación:** no corresponde.

**Extensión estimada:** 28–34 páginas; 45–60 ejercicios.

### Capítulo 11. Ecuaciones e inecuaciones

**Prerrequisitos:** L1 §7.3, L1 §7.4, L1 §8.3, L1 §8.9, L1 §10.3, L1 §10.5, L1 §10.8.

**Objetivos:** resolver ecuaciones lineales, cuadráticas, racionales, con radicales, con valor absoluto, exponenciales y logarítmicas; derivar la fórmula cuadrática; detectar soluciones extrañas y explicar su origen; resolver inecuaciones mediante análisis de signos; comprobar soluciones.

**Secciones:**

- **11.1** Qué significa resolver una ecuación. Conjunto solución y ecuaciones equivalentes.
- **11.2** Ecuaciones lineales.
- **11.3** Ecuaciones cuadráticas. Completar el cuadrado; derivación de la fórmula; discriminante.
- **11.4** Ecuaciones polinómicas reducibles y ecuaciones racionales; soluciones extrañas.
- **11.5** Ecuaciones con radicales y con valor absoluto.
- **11.6** Inecuaciones lineales, cuadráticas y racionales; análisis de signos.
- **11.7** Ecuaciones exponenciales y logarítmicas. Despejar el plazo en un problema de interés compuesto.
- **11.8** Comprobación de soluciones y sensibilidad elemental de la solución a los datos.

**Resultados principales:** fórmula cuadrática y clasificación por el discriminante.

**Resultados admitidos:** RA-02, RA-03 (en §11.7).

**Aplicaciones financieras:** plazo necesario para alcanzar un monto; tasa implícita en una operación de dos flujos.

**Computación:** comprobación numérica de soluciones (L1 ap. A).

**Extensión estimada:** 30–36 páginas; 50–65 ejercicios.

### Capítulo 12. Sistemas de ecuaciones

**Prerrequisitos:** L1 §3.3, L1 §11.2, L1 §11.3.

**Objetivos:** resolver sistemas lineales de dos y tres incógnitas por sustitución y eliminación; interpretar geométricamente un sistema de dos ecuaciones; clasificar un sistema según su número de soluciones; resolver sistemas no lineales sencillos; plantear sistemas en problemas aplicados.

**Secciones:**

- **12.1** Sistemas lineales de dos ecuaciones: sustitución, igualación y eliminación.
- **12.2** Interpretación geométrica en el plano ℝ × ℝ: rectas como conjuntos solución.
- **12.3** Clasificación: solución única, infinitas soluciones o ninguna.
- **12.4** Sistemas de tres ecuaciones; eliminación sistemática (anticipo de L6 c. 1).
- **12.5** Sistemas no lineales sencillos.
- **12.6** Aplicaciones: cartera de dos activos con restricción presupuestaria; mezclas; replicación de un pago futuro con dos instrumentos.

**Resultados principales:** criterio de unicidad para sistemas 2 × 2.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** composición de carteras; replicación elemental de pagos.

**Computación:** no corresponde.

**Extensión estimada:** 24–30 páginas; 35–45 ejercicios.

### Capítulo 13. Modelización algebraica

**Prerrequisitos:** L1 §9.1, L1 c. 11, L1 c. 12.

**Objetivos:** traducir un problema verbal a un modelo con variables, parámetros y unidades; explicitar los supuestos de un modelo; resolver y verificar el modelo con casos límite, unidades y órdenes de magnitud; identificar cuándo un supuesto invalida la conclusión.

**Secciones:**

- **13.1** Del enunciado al modelo: variables, parámetros y unidades.
- **13.2** Supuestos de un modelo y su validez.
- **13.3** Problemas de tasas, mezclas y presupuestos.
- **13.4** Problemas financieros: interés simple y compuesto, descuentos, comisiones, punto de equilibrio.
- **13.5** Verificación: casos límite, unidades y orden de magnitud.
- **13.6** Cuando el modelo falla: sensibilidad a los supuestos.

**Resultados principales:** no corresponde; el capítulo desarrolla método.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** todo el capítulo.

**Computación:** no corresponde.

**Extensión estimada:** 22–28 páginas; 30–40 ejercicios.

### Capítulo 14. Algoritmos y primeros programas en Python

**Prerrequisitos:** L1 §5.5, L1 §8.3, L1 §8.10, L1 §9.6, L1 §11.3, L1 ap. A.

**Objetivos:** describir un algoritmo con entrada, salida y pasos finitos; escribir programas con variables, condicionales, bucles y funciones; implementar el algoritmo de Euclides y justificar su corrección; aproximar raíces n-ésimas por bisección con una cota del error; construir una tabla de capitalización compuesta; probar un programa con casos de resultado conocido.

**Secciones:**

- **14.1** Qué es un algoritmo: entrada, salida, finitud y corrección.
- **14.2** Variables, tipos numéricos y expresiones en Python.
- **14.3** Condicionales.
- **14.4** Bucles.
- **14.5** Funciones.
- **14.6** El algoritmo de Euclides programado y la prueba de su corrección.
- **14.7** Bisección para aproximar raíces n-ésimas. La raíz existe por L1 §8.3; el intervalo se reduce a la mitad en cada paso, lo que da una cota explícita del error.
- **14.8** Capitalización compuesta y tablas de saldos en Python.
- **14.9** Verificación de programas mediante casos con resultado conocido.

**Resultados principales:** corrección del algoritmo de Euclides; cota del error de la bisección.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** tabla de capitalización; saldo de un ahorro periódico.

**Computación:** todo el capítulo.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

## Apéndices

- **A** Python como calculadora científica. Instalación mínima, expresiones, operador de potencia, funciones del módulo `math`; explicado línea por línea para quien nunca programó. Puede leerse desde el capítulo 6.
- **B** Soluciones seleccionadas.

## Material final

Bibliografía; índice de símbolos; índice analítico.
