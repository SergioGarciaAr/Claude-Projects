# L3. Programación en Python para la matemática aplicada

Índice detallado · Versión 1.0 · Entrega 1b · 2026-10-16

## Ficha editorial

- **Serie:** I. Fundamentos.
- **Requisitos:** L1, L2.
- **Capítulos:** 12, más un apéndice.
- **Extensión estimada:** 326–408 páginas.

**Propósito.** Este libro convierte la programación en una herramienta de trabajo matemático. Enseña Python con ejemplos tomados de la matemática y las finanzas, y presta atención especial a lo que suele omitirse en los cursos introductorios: la aritmética de punto flotante y sus consecuencias, la corrección y complejidad de los algoritmos, las pruebas, el manejo de datos temporales y la reproducibilidad. No es un manual de referencia del lenguaje: cubre lo que la colección necesita y explica por qué.

**Rutas de lectura.** Puede leerse en paralelo con L4. Los capítulos 1 a 4 y 8 son los requeridos por las secciones computacionales de L4; el resto se necesita a partir de L5.

**Versiones.** La versión de Python y de las bibliotecas se fijará en la Fase 2 y se declarará en el prefacio.

## Preliminares

Portada; créditos; prefacio; guía de lectura y prerrequisitos; convenciones tipográficas del código.

## Capítulos

### Capítulo 1. Programas, intérpretes y entornos

**Prerrequisitos:** L1 c. 14.

**Objetivos:** explicar qué ocurre cuando se ejecuta un programa; crear y usar un entorno virtual con versiones fijadas; ejecutar código como script, en el intérprete y en un cuaderno; leer un mensaje de error e identificar su origen.

**Secciones:**

- **1.1** Qué hace una computadora al ejecutar un programa.
- **1.2** Lenguajes interpretados y compilados.
- **1.3** Instalación, entornos virtuales y versiones de bibliotecas.
- **1.4** Scripts, módulos e intérprete interactivo.
- **1.5** Cuadernos: ventajas y riesgos para la reproducibilidad.
- **1.6** Cómo leer un mensaje de error.

**Resultados principales:** no corresponde.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** no corresponde.

**Computación:** todo el capítulo.

**Extensión estimada:** 20–26 páginas; 15–25 ejercicios.

### Capítulo 2. Tipos, expresiones y aritmética de punto flotante

**Prerrequisitos:** L3 c. 1, L1 §9.4, L1 §9.5, L1 §9.6.

**Objetivos:** usar los tipos básicos de Python; describir la representación IEEE 754 de un número de punto flotante; calcular el épsilon de máquina; explicar y prever errores de redondeo, cancelación catastrófica y acumulación; comparar flotantes correctamente; decidir cuándo usar aritmética decimal exacta para montos.

**Secciones:**

- **2.1** Tipos básicos: enteros, flotantes, booleanos y cadenas.
- **2.2** Enteros de precisión arbitraria.
- **2.3** El estándar IEEE 754: representación binaria de punto flotante.
- **2.4** Redondeo y épsilon de máquina.
- **2.5** Consecuencias: por qué 0.1 + 0.2 no es 0.3; cancelación catastrófica; sumas largas.
- **2.6** Comparación de flotantes con tolerancias.
- **2.7** Aritmética decimal para montos monetarios.

**Resultados principales:** cota del error relativo de redondeo en función del épsilon de máquina.

**Resultados admitidos:** ninguno. El estándar IEEE 754 se presenta como convención técnica, con referencia.

**Aplicaciones financieras:** redondeo de montos; acumulación de intereses.

**Computación:** todo el capítulo.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 3. Control de flujo, funciones y recursión

**Prerrequisitos:** L3 c. 2, L1 c. 2, L1 §4.6.

**Objetivos:** escribir condicionales y bucles correctos; diseñar funciones con parámetros y valores de retorno; explicar el alcance de las variables; escribir funciones recursivas y relacionar su corrección con la inducción; documentar el contrato de una función.

**Secciones:**

- **3.1** Condicionales y expresiones lógicas.
- **3.2** Bucles while y for.
- **3.3** Funciones: parámetros, retorno y alcance.
- **3.4** Funciones como objetos.
- **3.5** Recursión y su relación con la inducción matemática.
- **3.6** Documentación y contratos de funciones.

**Resultados principales:** corrección de funciones recursivas por inducción.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** cálculo recursivo del saldo de un préstamo.

**Computación:** todo el capítulo.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 4. Estructuras de datos

**Prerrequisitos:** L3 c. 3, L1 c. 3.

**Objetivos:** elegir entre listas, tuplas, diccionarios y conjuntos según la tarea; prever el costo aproximado de sus operaciones; representar un flujo de caja con fechas y montos.

**Secciones:**

- **4.1** Listas.
- **4.2** Tuplas e inmutabilidad.
- **4.3** Diccionarios.
- **4.4** Conjuntos.
- **4.5** Costo de las operaciones (presentación informal; análisis formal en L3 c. 5).
- **4.6** Representación de un flujo de caja.

**Resultados principales:** no corresponde.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** flujos de caja.

**Computación:** todo el capítulo.

**Extensión estimada:** 26–32 páginas; 25–35 ejercicios.

### Capítulo 5. Corrección y complejidad de algoritmos

**Prerrequisitos:** L3 c. 4, L1 c. 4, L2 §8.5.

**Objetivos:** demostrar la corrección de un algoritmo mediante invariantes de ciclo; demostrar su terminación; usar la notación O; analizar la búsqueda binaria y el ordenamiento por mezcla; implementar la exponenciación rápida.

**Secciones:**

- **5.1** Corrección: precondiciones, poscondiciones e invariantes de ciclo.
- **5.2** Terminación.
- **5.3** Notación O y crecimiento comparado.
- **5.4** Búsqueda lineal y binaria.
- **5.5** Ordenamiento por inserción y por mezcla; recurrencias de costo.
- **5.6** Exponenciación rápida.

**Resultados principales:** corrección y costo logarítmico de la búsqueda binaria; costo n log n del ordenamiento por mezcla.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** búsqueda de fechas en calendarios ordenados.

**Computación:** todo el capítulo.

**Extensión estimada:** 28–34 páginas; 30–40 ejercicios.

### Capítulo 6. Errores, pruebas y depuración

**Prerrequisitos:** L3 c. 5.

**Objetivos:** manejar y lanzar excepciones; validar entradas; escribir pruebas unitarias y pruebas basadas en propiedades; depurar sistemáticamente; distinguir errores numéricos de errores conceptuales.

**Secciones:**

- **6.1** Excepciones.
- **6.2** Validación de entradas.
- **6.3** Pruebas unitarias.
- **6.4** Pruebas basadas en propiedades.
- **6.5** Depuración sistemática.
- **6.6** Errores numéricos y errores conceptuales.

**Resultados principales:** no corresponde.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** pruebas de una función de valor presente.

**Computación:** todo el capítulo.

**Extensión estimada:** 22–28 páginas; 20–30 ejercicios.

### Capítulo 7. Clases y objetos con fines científicos

**Prerrequisitos:** L3 c. 6, L1 §8.10.

**Objetivos:** definir clases con atributos y métodos; proteger invariantes de un objeto; modelar un flujo de caja como objeto; decidir entre composición y herencia; reconocer cuándo una clase es innecesaria.

**Secciones:**

- **7.1** Clases, atributos y métodos.
- **7.2** Encapsulamiento y validación de invariantes.
- **7.3** Ejemplo: una clase para flujos de caja con valor presente.
- **7.4** Composición y herencia.
- **7.5** Cuándo no usar clases.

**Resultados principales:** no corresponde.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** flujos de caja y su valor presente.

**Computación:** todo el capítulo.

**Extensión estimada:** 22–28 páginas; 20–30 ejercicios.

### Capítulo 8. Cálculo vectorial con NumPy

**Prerrequisitos:** L3 c. 5, L2 c. 11.

**Objetivos:** crear y manipular arreglos; escribir código vectorizado; aplicar las reglas de *broadcasting*; indexar con máscaras; calcular productos escalares y productos de matrices; distinguir vistas de copias.

**Secciones:**

- **8.1** Arreglos y tipos de datos.
- **8.2** Operaciones elemento a elemento y vectorización.
- **8.3** *Broadcasting*.
- **8.4** Indexación y máscaras.
- **8.5** Producto escalar y producto de matrices (definición computacional; la teoría está en L6).
- **8.6** Rendimiento: bucles frente a vectorización.
- **8.7** Errores frecuentes: vistas y copias.

**Resultados principales:** no corresponde.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** valor de una cartera para muchos escenarios de precios.

**Computación:** todo el capítulo.

**Extensión estimada:** 28–34 páginas; 25–35 ejercicios.

### Capítulo 9. Series temporales y datos tabulares con pandas

**Prerrequisitos:** L3 c. 8, L2 §8.7.

**Objetivos:** manipular series y tablas indexadas por fechas; leer y limpiar datos; prever y evitar errores de alineación; calcular rendimientos simples y logarítmicos; agregar series a otra frecuencia; tratar datos faltantes.

**Secciones:**

- **9.1** Series y tablas (DataFrame).
- **9.2** Índices de fechas.
- **9.3** Lectura y limpieza de datos.
- **9.4** Alineación por índice y sus trampas.
- **9.5** Rendimientos simples y logarítmicos a partir de precios.
- **9.6** Remuestreo y agregación temporal.
- **9.7** Datos faltantes.
- **9.8** Copia y modificación de datos.

**Resultados principales:** no corresponde.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** series de precios y rendimientos.

**Computación:** todo el capítulo.

**Extensión estimada:** 30–36 páginas; 25–35 ejercicios.

### Capítulo 10. Visualización científica honesta

**Prerrequisitos:** L3 c. 9, L2 c. 13.

**Objetivos:** diseñar gráficos que representen fielmente los datos; elegir escalas, ejes y unidades; graficar series temporales e histogramas; detectar gráficos engañosos; producir figuras reproducibles.

**Secciones:**

- **10.1** Principios de la visualización científica.
- **10.2** Ejes, escalas y unidades.
- **10.3** Gráficos de series temporales.
- **10.4** Histogramas (presentación descriptiva).
- **10.5** Gráficos engañosos y cómo evitarlos.
- **10.6** Figuras reproducibles.

**Resultados principales:** no corresponde.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** gráficos de precios, rendimientos y comparaciones de desempeño.

**Computación:** todo el capítulo.

**Extensión estimada:** 20–26 páginas; 15–25 ejercicios.

### Capítulo 11. Números pseudoaleatorios y reproducibilidad

**Prerrequisitos:** L3 c. 8, L1 §5.7.

**Objetivos:** explicar por qué un generador determinista puede imitar el azar; analizar un generador congruencial lineal; usar correctamente los generadores de NumPy y sus semillas; generar uniformes y transformarlos de manera sencilla; evitar errores frecuentes con semillas.

**Secciones:**

- **11.1** Determinismo y aleatoriedad aparente.
- **11.2** Generadores congruenciales lineales y su período.
- **11.3** Generadores modernos y sus propiedades declaradas.
- **11.4** Semillas y reproducibilidad.
- **11.5** Uniformes en [0; 1) y transformaciones sencillas (la teoría de probabilidad está en L8).
- **11.6** Errores frecuentes: reutilizar semillas, flujos paralelos.

**Resultados principales:** condiciones de período máximo de un generador congruencial (enunciado; demostración de un caso particular).

**Resultados admitidos:** ninguno. Las propiedades de los generadores modernos se presentan como especificaciones documentadas, con referencia.

**Aplicaciones financieras:** no corresponde.

**Computación:** todo el capítulo.

**Extensión estimada:** 22–28 páginas; 20–30 ejercicios.

### Capítulo 12. Organización de un trabajo computacional reproducible

**Prerrequisitos:** L3 c. 6, L3 c. 9, L3 c. 11.

**Objetivos:** usar control de versiones; organizar un proyecto; fijar entornos y dependencias; documentar la procedencia y transformación de los datos; integrar pruebas; producir un informe reproducible.

**Secciones:**

- **12.1** Control de versiones con git.
- **12.2** Estructura de un proyecto.
- **12.3** Entornos y dependencias fijadas.
- **12.4** Datos: procedencia, licencia y transformaciones documentadas.
- **12.5** Pruebas y verificación como parte del trabajo.
- **12.6** Informe reproducible.

**Resultados principales:** no corresponde.

**Resultados admitidos:** ninguno.

**Aplicaciones financieras:** proyecto de ejemplo con datos de precios.

**Computación:** todo el capítulo.

**Extensión estimada:** 22–28 páginas; 10–20 ejercicios.

## Apéndices

- **A** Soluciones seleccionadas.

## Material final

Bibliografía; índice analítico.
