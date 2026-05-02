# Big Data Proyecto AutoTec
Este respositorio sirve para el trabajo práctico de la asignatura Big Data. 
## Hito 1
### 1. Situación Problema
Las organizaciones del sector automotriz incluyendo concesionarias y plataformas de compraventa enfrentan serias limitaciones al definir precios de compra, venta y tasación de vehículos usados. Con frecuencia, estas decisiones se toman con información insuficiente, recurriendo a métodos manuales, criterios subjetivos o datos desactualizados.
En muchos casos, el valor de un vehículo se determina de manera práctica, basándose en la experiencia del vendedor o en promedios generales de mercado. Este enfoque no incorpora de forma precisa variables críticas como el kilometraje, el estado de conservación o la ubicación, lo que afecta directamente la exactitud de la tasación.
Asimismo, el uso de tablas de depreciación estáticas o referencias genéricas no refleja la dinámica real del mercado ni el impacto de factores como marca, modelo, año y por sobre todo el kilometraje del vehículo en la pérdida de valor. Como consecuencia, las organizaciones se exponen a riesgos relevantes: la sobrevaloración, que disminuye la competitividad, y la subvaloración, que afecta la rentabilidad. En definitiva, la toma de decisiones se sustenta más en la intuición que en información confiable, limitando la capacidad de competir de manera eficiente.

### 2. Propuesta de Valor
La incorporación de técnicas de scraping en plataformas de venta de automóviles usados constituye una solución innovadora, al reemplazar enfoques intuitivos por modelos sustentados en Business Intelligence (BI).
El scraping aplicado en estas páginas permite recolectar de manera automatizada grandes volúmenes de datos actuales y relevantes del mercado, conformando una base  con etiquetas clave como marca, modelo, año, kilometraje, combustible y precio.
La disponibilidad de estas etiquetas posibilita realizar comparaciones entre vehículos que comparten características similares, midiendo la diferencia de kilometraje y, a partir de ello, estimando la variación de valor. Este análisis constituye la base para calcular la depreciación real de los vehículos, reemplazando estimaciones subjetivas por métricas verificables y mejorando la exactitud en los procesos de tasación.
Además, el acceso a datos históricos y actualizados abre la puerta al desarrollo de modelos predictivos capaces de estimar el valor de un vehículo según sus características y nivel de desgaste. Esto otorga a las organizaciones una ventaja competitiva significativa, al permitir ajustar precios de compra y venta en función de las condiciones actuales del mercado.
En conclusión, el scraping no solo eleva la calidad de la información disponible, sino que la transforma en conocimiento estratégico, habilitando una toma de decisiones más informada, precisa y orientada a maximizar la rentabilidad y competitividad en el negocio automotriz.
### 3. Análisis de las 4V Iniciales:
1. Volumen: Para que el análisis sea confiable y provechoso, se necesita recolectar una numerosa cantidad de datos, idealmente más 3000 registros, considerando aproximadamente 500 datos por persona, siendo una muestra representativa para el estudio del caso. Esto es importante porque el mercado automotriz usado tiene mucha variación: un mismo modelo puede cambiar bastante de precio según el año, kilometraje, ciudad, estado, combustible o página donde fue publicado.
Si se trabaja con pocos datos, el promedio puede quedar distorsionado por casos aislados, por ejemplo, un auto demasiado barato por estar en mal estado o detalles significativos, también uno muy caro por tener poco kilometraje. Sin embargo, si se tiene más de 3000 datos, se obtiene una muestra mucho más representativa, con menos sesgo, permite que los promedios se estabilicen y reflejen mejor la distribución real del mercado.
Este volumen permite comparar marcas, modelos, años y rangos de kilometraje con mayor precisión. Así, la decisión sobre depreciación no se basa en percepciones, sino en una cantidad suficiente de datos reales publicados en distintas plataformas como Yapo, Autocosmos, Piamonte, Callegari, Kovac, Clicar, Emol, Cariautos y Bruno Fritsch. 
 2. Variedad : La variedad es fundamental porque no basta con extraer solo el precio del vehículo para poder analizar correctamente la depreciación, se necesitan varias etiquetas o variables que entreguen un mejor contexto al dato.
En el caso de Autotec, se recopilan datos como: Marca, modelo, año, kilometraje, combustible, ciudad, precio y fecha de captura. Estas variables permiten entender por qué un auto vale más o menos que otro. Por ejemplo, dos vehículos de la misma marca, modelo y año pueden tener precios distintos si uno tiene menos kilometraje, es de un año más reciente, está en otra ciudad o usa un tipo de combustible diferente.
También es importante extraer información desde distintas páginas, porque cada plataforma puede tener públicos, precios y tipos de publicaciones diferentes. Comparar datos de Yapo, Autocosmos, Clicar, Emol, concesionarias y automotoras permite tener una visión más amplia del mercado.
El atributo Fecha de Captura, permite ordenar los datos en el tiempo y asegurar una correcta comparación en intervalos de tiempo, ya que los precios en el mercado automotriz son tan volátiles, tener un registro estructurado con un atributo de fecha, se garantiza que el análisis de depreciación sea coherente y periodico. 
Gracias a esta variedad, se puede analizar no solo el precio promedio, sino también cómo influye cada característica en la depreciación del valor del auto y en específico en como el kilometraje influye de manera importante en el valor del vehículo. 
3. Veracidad : La veracidad se refiere a asegurar que los datos scrapeados sean reales, útiles y confiables. Como los datos vienen desde distintas páginas web, pueden existir errores, publicaciones incompletas, precios mal escritos, vehículos repetidos, valores fuera de lo normal o bien campos vacíos. 
Para mejorar la veracidad, es importante realizar una limpieza de datos. Por ejemplo, no todas las páginas tendrán el mismo formato de precio para ello se debe transformar todos los precios al mismo formato, eliminar símbolos como “$” o puntos, validar que el año sea lógico, revisar que el kilometraje sea numérico y descartar registros sin precio, sin modelo o con datos incompletos, asegurando un estándar de calidad y formato para la manipulación y estudio del caso. 
También se deben eliminar valores extremos que pueden alterar el promedio. Por ejemplo, si un auto aparece publicado a $1.000 o a $999.999.999, es un error o una publicación que no sirve para el análisis y puede perjudicar completamente el propósito de scraping. 
La fecha de captura es importante, porque permite ordenar los datos en el tiempo y hacer comparaciones correctas. Por ejemplo, no sería bueno comparar un precio tomado en enero con otro muchos meses después sin considerar los cambios del mercado. Tener la fecha ayuda a hacer un análisis más real y ordenado.
Además, se debe revisar si existen vehículos duplicados entre páginas o dentro de la misma plataforma. Esto permite evitar contar el mismo auto varias veces y que los resultados se vean alterados. Con estos procesos, el análisis no se basa simplemente en datos recolectados, sino en datos depurados, ordenados y confiables.
4. Velocidad : La velocidad es la relación con que la frecuencia debe ejecutarse al scraper para que la información no quede obsoleta. El objetivo principal no es ver cambios diarios de precio, sino analizar la depreciación del valor de los autos según su kilometraje. Por eso, no se necesita correr el scraper todos los días, porque el kilometraje y la baja de valor se ven mejor en un tiempo más largo. 
Para este caso, lo mejor sería ejecutar el scraper una vez al mes, ya que así se puede comparar cómo cambian los precios de autos parecidos según kilometraje, marca, modelo, año, combustible y ciudad. Al guardar datos cada mes, se puede formar una base histórica para ver si un auto con más kilometraje vale menos y cuánto baja su precio promedio frente a otros del mismo tipo. 
En conclusión, para estudiar la depreciación por kilometraje, una frecuencia mensual es suficiente, porque permite ver tendencias reales sin juntar datos repetidos. Así, el análisis se enfoca en cuánto influye el kilometraje en el precio de un auto usado.


### a) Comando para ejecutar
```bash
docker-compose up -d
```

### b) Evidencia 1: Consumo de contenedores
![Docker stats](img/docker-stats.png)

### c) Evidencia 2: Conteo de documentos en MongoDB
![MongoDB countDocuments](img/mongo-count.png)

### d) Tabla de Atributos
En este hito, todos los integrantes trabajaron con una estructura de datos común.  
Cada registro almacenado en MongoDB fue construido con los mismos atributos, con el objetivo de mantener consistencia en la base de datos y facilitar el análisis posterior.

Los campos utilizados en cada documento fueron los siguientes:

- `marca`
- `modelo`
- `year`
- `kilometraje`
- `combustible`
- `ciudad`
- `url`
- `precio`
- `fecha_captura`
- `grupo`
- `usuario`

Si bien la instrucción solicita una tabla de atributos por integrante, en este proyecto no se dividieron los campos por persona.  
En cambio, cada integrante capturó aproximadamente 500 registros utilizando la misma estructura de atributos, diferenciándose principalmente por la fuente de datos utilizada.

### Tabla de integrantes y fuentes extraídas

| Integrante | Sitio(s) fuente | Observación |
|------------|-----------------|-------------|
| Daniela Cofre | [Yapo Autos Usados](https://www.yapo.cl/autos-usados/coquimbo-la-serena) | Extracción de registros desde portal de autos usados. |
| Jocelyn Leon | [Bruno Fritsch](https://www.brunofritsch.cl/autos-usados) | Extracción de autos usados con la estructura común del proyecto. |
| Luz Azocar | [Emol Autos Usados](https://automoviles.emol.com/venta/autos-usados) | Captura de vehículos usados bajo el mismo esquema JSON. |
| Javiera Pizarro | [Clicar](https://www.clicar.cl/vehiculos/usado) | Registros obtenidos manteniendo los mismos atributos. |
| Neiel Cortes | [Autocosmos](https://www.autocosmos.cl/auto/usado) | Extracción de publicaciones de autos usados. |
| Martin Rojas | [Aspillaga Hornauer](https://seminuevos.aspillagahornauer.cl/stock-seminuevos/), [Difor](https://www.difor.cl/autos-usados-chile?page=), [Piamonte Usados](https://www.piamonteusados.cl/autos/seminuevos?annio_desde=&annio_hasta=&precios=&unidades=30) | Se utilizaron varias fuentes porque una sola página no tenía suficientes vehículos para alcanzar la cantidad requerida. |
| Belen Andrades | [Callegari](https://callegari.cl/seminuevos/), [Gildemeister Usados](https://gildemeisterusados.cl/compra-tu-auto/), [Valentini Seminuevos](https://seminuevosvalentini.cl/), [Autoselect](https://www.autoselect.cl/web/autos-usados?page=%7B%7D), [Salazar Israel](https://www.salazarisrael.cl/vehiculos/usado) | Se recurrió a múltiples sitios para completar el volumen mínimo de registros exigido. |

### Estructura de cada documento almacenado

Ejemplo de documento JSON:

```json
{
  "marca": "Toyota",
  "modelo": "Hilux",
  "year": "2018",
  "kilometraje": "180 km",
  "combustible": "diesel",
  "ciudad": "Buin",
  "url": "https://...",
  "precio": 12600000,
  "fecha_captura": "2026-04-30 23:39:11",
  "grupo": "autotec",
  "usuario": "dani"
}
```