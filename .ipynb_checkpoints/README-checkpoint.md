# 🚗 AutoTec — Análisis del Mercado Automotriz Chileno

**Proyecto final · Big Data para la Toma de Decisiones · IICG 2026**

AutoTec es un proyecto de análisis de datos centrado en el mercado de vehículos usados en Chile. El objetivo es comprender el comportamiento de los precios, detectar patrones relevantes en la oferta disponible y construir modelos que ayuden a estimar el valor de un automóvil según sus características, con énfasis en la depreciación asociada al kilometraje y la antigüedad.[file:2]

A partir del repositorio se desarrolla un flujo completo que incluye extracción de datos, limpieza distribuida, análisis exploratorio, generación de variables derivadas y preparación de insumos para etapas posteriores de segmentación y modelamiento predictivo.[file:2]

## Integrantes

| Nombre | Rol |
|---|---|
| Neiel Cortes | Coordinación |
| Belen Andrades | Integrante |
| Luz Azocar | Integrante |
| Daniela Cofre | Integrante |
| Jocelyn León | Integrante |
| Javiera Pizarro | Integrante |
| Martin Rojas | Integrante |

## Descripción del proyecto

El proyecto reúne publicaciones de autos usados obtenidas desde portales web del mercado chileno para analizarlas en un entorno reproducible basado en Python, Docker, Jupyter, MongoDB Atlas y PySpark.[file:2]

En el notebook de EDA multivariado se indica que el análisis considera variables originales como marca, modelo, precio, kilometraje, año, combustible y ciudad, además de variables derivadas como antigüedad del vehículo, uso anual estimado, categoría de precio, rango de kilometraje, tipo de marca, condición ecológica y un segmento de depreciación creado para profundizar el análisis.[file:2]

## Fuentes de datos

Los datos fueron recolectados mediante web scraping desde portales de compra y venta de vehículos usados en Chile, entre ellos:

- Callegari Automotriz
- Valentini
- Autocosmos
- Clicar
- Emol Automóviles
- Cariautos
- Brunofritsch
- Aspillaga Hornauer
- Difor
- Gildemeister Usados
- Autoselect
- Salazar Israel

> Nota: esta lista proviene de la descripción del proyecto entregada para el README. El notebook verificado utilizado en este repositorio trabaja sobre la colección consolidada ya limpia en MongoDB Atlas.[file:2]

## Base de datos

El notebook verificado carga datos desde **MongoDB Atlas** usando la colección **`ContenedorAutosLimpio`**, que corresponde al contenedor consolidado para el análisis multivariado.[file:2]

Según la descripción del flujo del proyecto, el proceso contempla tres etapas:

1. **Extracción**: almacenamiento inicial de datos crudos en una colección de trabajo.
2. **Limpieza**: normalización y depuración de variables con PySpark.
3. **Integración**: consolidación en `ContenedorAutosLimpio` y creación de nuevas variables analíticas.[file:2]

## Variables principales

| Variable | Descripción |
|---|---|
| `marca` | Marca del vehículo |
| `modelo` | Modelo del vehículo |
| `precio` | Precio de venta en pesos chilenos |
| `kilometraje` | Kilometraje informado en la publicación |
| `year` | Año de fabricación |
| `combustible` | Tipo de combustible |
| `ciudad` | Ciudad o comuna de publicación |

### Variables derivadas usadas en el análisis

- `antiguedadauto`
- `usoanualestimado`
- `categoriaprecio`
- `rangokilometraje`
- `tipomarca`
- `esecologico`
- `catcombustible`
- `segmentodepreciacion`[file:2]

## Tecnologías utilizadas

- **Python** para scraping, limpieza, análisis y modelamiento.
- **Selenium** y **undetected-chromedriver** para sitios dinámicos.
- **BeautifulSoup** y **Requests** para scraping estático.
- **MongoDB Atlas** como almacenamiento NoSQL en la nube.[file:2]
- **PySpark** para procesamiento distribuido y limpieza.[file:2]
- **Pandas** y **NumPy** para análisis de datos.[file:2]
- **Matplotlib** y **Seaborn** para visualización.[file:2]
- **Scikit-learn** para modelos de machine learning.
- **Docker** y **Jupyter Lab** para entorno reproducible.
- **Git** y **GitHub** para versionado y trabajo colaborativo.

## Hallazgos del EDA

En el notebook validado se trabajan **1.988 registros** provenientes de la colección consolidada para EDA multivariado.[file:2]

Las estadísticas descriptivas muestran un **precio promedio** de **16.450.599 CLP**, un **kilometraje promedio** de **71.070 km**, un **año promedio** de **2021** y una **antigüedad promedio** de **5 años**.[file:2]

La matriz de correlación del notebook muestra que `precio` tiene relación negativa con `kilometraje` 
\(-0.23\) y con `antiguedadauto` \(-0.24\), mientras que `kilometraje` y `antiguedadauto` presentan una relación positiva más marcada \(0.70\).[file:2]

El propio análisis del notebook concluye que la antigüedad aparece como una variable relevante para explicar el comportamiento del precio, aunque debe interpretarse en conjunto con otras características como marca, modelo, kilometraje y combustible.[file:2]

## Resultados destacados

El resumen por año incluido en el notebook muestra que los vehículos más recientes concentran menores kilometrajes promedio y, en general, precios medios más altos; por ejemplo, 2024 registra un precio promedio de **20.123.299 CLP** y 2025 de **20.202.467 CLP**, mientras años más antiguos presentan precios promedio menores y mayores kilometrajes.[file:2]

En el ranking por marca mostrado en el notebook, **Lexus**, **BMW**, **Mercedes** y **Audi** figuran entre las marcas con mayores precios promedio dentro del subconjunto filtrado presentado en el análisis.[file:2]

## Etapas del análisis

### 1. Extracción de datos
Cada integrante participó en la recopilación de información desde al menos una fuente web, extrayendo variables base del vehículo para integrarlas al flujo analítico del proyecto.

### 2. Limpieza y normalización
Con PySpark se estandarizaron formatos, se trataron nulos, se corrigieron inconsistencias y se preparó una colección consolidada para el análisis.[file:2]

### 3. Análisis exploratorio
Se desarrolló estadística descriptiva, visualizaciones y análisis de relaciones entre variables originales y derivadas para estudiar precio y depreciación.[file:2]

### 4. Clustering no supervisado
Según la descripción del proyecto, se aplicaron K-Means, PCA y DBSCAN como parte de la etapa de segmentación. Estos resultados aparecen en tu borrador, pero no están respaldados por el notebook verificado que se usó para construir este README, por lo que conviene dejarlos como parte general del proyecto y no como métricas validadas en este archivo.[file:2]

### 5. Modelos supervisados
El borrador menciona regresión lineal y modelos de clasificación con distintas métricas. Como esas cifras no aparecen en el notebook validado disponible aquí, se recomienda mantenerlas solo si existen notebooks o reportes adicionales en el repositorio que las documenten explícitamente.[file:2]

## Estructura sugerida del repositorio

```bash
AutoTec/
├── README.md
├── docker-compose.yml
├── notebooks/
│   ├── scrapers/
│   ├── limpieza/
│   ├── analisis/
│   ├── graficos/
│   ├── semana10_clustering/
│   └── semana12_modelos/
├── src/
│   ├── scraping/
│   ├── preprocessing/
│   └── modeling/
├── data/
│   └── muestras_o_diccionarios/
└── docs/
```

## Cómo ejecutar el proyecto

1. Clona el repositorio.
2. Levanta el entorno con `docker-compose up`.
3. Accede a Jupyter Lab en `http://localhost:8888`.
4. Ejecuta los notebooks en orden, desde scraping y limpieza hasta análisis, visualizaciones y modelamiento.

## Próximos ajustes recomendados

- Reemplazar la sección de estructura del repositorio por la estructura real una vez que el proyecto esté cerrado.
- Verificar en notebooks de clustering y clasificación las métricas finales antes de dejarlas fijas en el README.
- Agregar capturas de gráficos del EDA para que la portada del repositorio sea más visual.
- Incluir un bloque de instalación de dependencias si el repositorio también puede correrse sin Docker.

