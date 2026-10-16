# Fuentes de datos y licencias

Entrega 1e · Versión 1.0 · 2026-10-16

Este documento registra las fuentes de datos previstas para los capítulos con datos reales, en particular L20 y los casos de L23. Para cada fuente indica sus condiciones de uso, el nivel de verificación y sus consecuencias para la obra. No es asesoramiento jurídico. La redistribución de datos y la reproducción de cifras en una obra publicada deberían confirmarse con asesoría legal antes de la publicación (decisión D-05 en `ESTADO.md`).

**Método.** Búsqueda web el 2026-10-16. El entorno de trabajo no puede abrir directamente los sitios de las fuentes, de modo que las condiciones se tomaron de los fragmentos que devuelve la búsqueda. Cuando la búsqueda solo devolvió fuentes secundarias, se indica.

## 1. Resumen

| Fuente | Datos | Condiciones verificadas | Nivel | Uso previsto en la obra |
|---|---|---|---|---|
| Kenneth R. French Data Library (Tuck School, Dartmouth) | Factores de Fama-French, carteras ordenadas por tamaño, valor, *momentum*, industria; diarios y mensuales desde 1926 | Las páginas llevan aviso de copyright de Fama y French. Muchas series derivan de CRSP y Compustat. No se encontraron términos explícitos de redistribución | Parcial | L14, L17, L20, L23 c. 2, c. 3, c. 4 |
| FRED (Banco de la Reserva Federal de San Luis) | Series macroeconómicas y de tasas | Algunas series tienen copyright de terceros: sin permiso de su titular, solo se permite el uso personal o educativo no comercial. Desde junio de 2024 los términos prohíben usar el contenido o la API de FRED para desarrollar o entrenar sistemas de aprendizaje automático | Verificada (anuncio oficial y páginas legales) | L14, L20; **excluida** de L21 y L23 c. 6 |
| Departamento del Tesoro de EE. UU. | Curvas diarias de rendimientos a la par (CMT), tasas de letras | Las obras del Gobierno federal no tienen protección de copyright en EE. UU. (17 U.S.C. § 105). No se encontró el texto de uso propio del Tesoro | Parcial | L5, L12 c. 8, L22, L23 c. 4 |
| Cboe DataShop / LiveVol | Opciones: cotizaciones de fin de día, datos *open-close* | Producto de pago, con descuento académico (50 % del precio estándar, mínimo de 500 USD). Hay una muestra gratuita de fin de día (julio–diciembre de 2022). La distribución externa de datos derivados tiene tarifa propia. Los datos de profundidad son solo de uso interno | Verificada en presentaciones regulatorias de tarifas de Cboe ante la SEC | L23 c. 5 (pendiente de decisión) |
| CRSP / Compustat | Rendimientos y contables de acciones individuales | No verificado en esta entrega. Son la base de casi todas las series de French y de los artículos replicados | — | Solo como referencia del método original |

## 2. Detalle por fuente

### 2.1 Kenneth R. French Data Library

- Las páginas de detalle llevan avisos de copyright: «Copyright Eugene F. Fama and Kenneth R. French» en la de puntos de corte por tamaño y «Copyright Kenneth R. French» en la de capital contable histórico.
- La biblioteca indica que muchas series derivan de CRSP. Desde la publicación de enero de 2025 usa el formato CIZ (Flat File Format 2.0) de CRSP.
- Publica «10 Portfolios Formed on Momentum», construidas mensualmente con puntos de corte del NYSE sobre el rendimiento previo (2-12), además del factor *momentum* (Mom). Hay versiones mensual y diaria.
- No se encontró una política explícita de redistribución ni de cita. Las bibliotecas de R y Julia que descargan estos datos tienen licencias MIT, pero esas licencias cubren su código, no los datos.

**Consecuencia.** El libro no incluirá copias de los archivos. El código descargará los datos desde la fuente, y el texto citará la biblioteca y la fecha de descarga. Como los datos se revisan, las cifras impresas se fecharán y se acompañarán del código que las regenera.

### 2.2 FRED

- Las series con copyright de terceros requieren permiso de su titular para todo uso distinto del personal o educativo no comercial. El Banco de la Reserva Federal de San Luis no puede conceder ese permiso, y la nota de copyright figura bajo cada gráfico.
- La actualización de términos de junio de 2024 prohíbe usar los servicios, el contenido o la API de FRED para desarrollar o entrenar programas o sistemas de aprendizaje automático, incluidos modelos de lenguaje e IA generativa. La redacción de la página de términos es ambigua en el fragmento obtenido, pero el anuncio oficial la presenta como prohibición.

**Consecuencias.**

- FRED no se usará en L21 ni en L23 c. 6 (aprendizaje automático).
- En L14 y L20 solo se usarán series de dominio público, como las producidas por organismos federales, y el texto indicará el estado de copyright de cada serie usada.
- Si la obra se publica con licencia comercial (D-02), toda serie con copyright de terceros queda excluida o requiere permiso.

### 2.3 Departamento del Tesoro de EE. UU.

- Publica diariamente las curvas de rendimientos a la par, las reales, las tasas de letras y las tasas de largo plazo.
- Según 17 U.S.C. § 105, la protección de copyright no se aplica a las obras del Gobierno de EE. UU. No se encontró el texto de condiciones de uso del sitio del Tesoro.

**Consecuencia.** Es la fuente preferida para los casos de tasas de interés y curvas. Antes de la composición final debe confirmarse su política de reutilización.

### 2.4 Datos de opciones

- No se encontró una fuente gratuita, con licencia verificable y con historial suficiente para un caso de estudio reproducible.
- Cboe DataShop ofrece datos de fin de día de pago, con descuento académico, y una muestra gratuita de seis meses (julio–diciembre de 2022) de datos *open-close*.
- Las condiciones de la muestra no se pudieron leer, y la distribución externa de datos derivados tiene tarifa propia. OptionMetrics, la fuente habitual en la investigación académica, no pudo verificarse.

**Opciones para L23 c. 5** (decisión D-05):

1. **Datos sintéticos** generados con un modelo de volatilidad estocástica calibrado a parámetros publicados, con el código que los genera. Es reproducible y sin restricciones, pero no son datos reales. Esta es la opción recomendada.
2. **Muestra gratuita de Cboe**, si sus condiciones permiten el uso descrito. Hay que verificarlas directamente con Cboe.
3. **Licencia académica** adquirida por el lector. El libro daría el código y el procedimiento, pero no los datos.

El título del capítulo («con datos reales») debería ajustarse si se elige la opción 1.

### 2.5 Acciones individuales (CRSP, Compustat)

Los artículos que replica L23 (Fama-French 1993, Jegadeesh-Titman 1993) usan acciones individuales de CRSP y datos contables de Compustat. Esta entrega no verificó sus condiciones de licencia; se trata de bases comerciales, habitualmente accesibles mediante suscripción institucional.

**Consecuencias para L23.**

- **L23 c. 2 (factores).** La réplica se hará sobre las carteras y factores publicados por French: pruebas de series de tiempo, regresiones de Fama-MacBeth sobre carteras y prueba GRS. La construcción de factores a partir de acciones individuales se explicará y se ilustrará con datos sintéticos o con un universo pequeño de fuente libre.
- **L23 c. 3 (*momentum*).** La réplica usará las diez carteras de *momentum* y el factor Mom de French, que siguen la definición 2-12, distinta de las estrategias superpuestas J/K de Jegadeesh y Titman. El capítulo explicará la diferencia y construirá las carteras superpuestas con datos sintéticos.
- **Sección 2.2 de L23** («Datos: fuente, licencia y validación») y **sección 2.1 de L20** («Fuentes de datos y licencias»). Usarán este documento como caso de estudio.

## 3. Política propuesta para la obra

1. La obra no redistribuye datos de terceros. El código descarga los datos de la fuente original y el texto indica la fuente, la serie, la fecha de consulta y el estado de licencia.
2. Toda cifra empírica impresa lleva fecha y el código que la regenera. Si la fuente revisa los datos, la diferencia se documenta en la siguiente edición.
3. Los datos sintéticos se generan con semilla fija y parámetros publicados en el texto.
4. Ninguna fuente cuyos términos prohíban un uso se emplea para ese uso; es el caso de FRED en el aprendizaje automático.
5. Antes de la publicación, una revisión legal confirma los puntos 1 y 2 según la licencia elegida (D-02).

## 4. Fuentes consultadas

- Kenneth R. French, Data Library: <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>; detalle de 10 carteras por *momentum*: <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_10_port_form_pr_12_2.html>; detalle de puntos de corte: <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library/det_me_breakpoints.html>.
- FRED, avisos legales: <https://fred.stlouisfed.org/legal/terms/>; anuncio de junio de 2024: <https://news.research.stlouisfed.org/2024/06/weve-updated-our-terms-of-use-action-requested/>.
- 17 U.S.C. § 105: <https://www.law.cornell.edu/uscode/text/17/105>.
- Cboe, descuento académico: <https://datashopcert.livevol.com/academic-discount>; tarifas presentadas ante la SEC: <https://www.sec.gov/files/rules/sro/c2/2026/34-106149-ex5.pdf>.
