# 🚗 AutoTec — Análisis del Mercado Automotriz Chileno

**Curso:** Big Data para la Toma de Decisiones  
**Profesora:** Vanessa Duarte 
**Fecha:** 23-06-2026  
**Repositorio:** https://github.com/IICG-Coquimbo/proyecto-big-data-2026-autotec.git

---

## Integrantes y Roles Organizacionales

| Nombre | Rol Técnico | Nivel |
|---|---|---|
| **Neiel Cortés** | Coordinación General + Ingesta (Autocosmos) + Modelo de Predicción + Base app.py | *Operativo* |
| **Belén Andrades** | Ingesta (Callegari, Gildemeister, Valentini, Autoselect, Salazar Israel) + Tablero Táctico + Informe Final | *Táctico* |
| **Daniela Cofré** | Ingesta (Yapo) + Modelo de Regresión (precio) + Tablero Táctico | *Táctico* |
| **Jocelyn León** | Ingesta (Bruno Fritsch) + Tablero Operativo (Alertas) | *Operativo* |
| **Luz Azocar** | Ingesta (Emol) + Tablero Estratégico + Storytelling Estratégico | *Estratégico* |
| **Javiera Pizarro** | Ingesta (Clicar) + Modelo Random Forest + Tablero Estratégico | *Estratégico* |
| **Martin Rojas** | Ingesta (Aspillaga, Difor, Piamonte) + Tablero Operativo + Alertas Críticas | *Operativo* |

---

## Situación Problema

Las organizaciones del sector automotriz enfrentan dificultades para definir precios y tasaciones de vehículos usados debido al uso de métodos manuales y criterios subjetivos. La valoración suele basarse en experiencia o referencias generales, sin considerar adecuadamente variables clave como la marca, modelo, año y kilometraje del vehículo. Esto genera tasaciones imprecisas que provocan riesgos de sobrevaloración o subvaloración, afectando tanto la competitividad como la rentabilidad de las organizaciones.

---

## Arquitectura del Proyecto

El proyecto opera sobre un ecosistema reproducible compuesto por:

- **Docker + Jupyter Lab**: entorno de desarrollo aislado y reproducible donde se ejecutan todos los notebooks del proyecto.
- **MongoDB Atlas**: base de datos NoSQL en la nube donde se almacenan los datos crudos (colección de scraping) y los datos procesados (`ContenedorAutosLimpio`).
- **PySpark**: motor de procesamiento distribuido utilizado para la limpieza, transformación y análisis de los datos.

El flujo general es: **Scraping → MongoDB Atlas (crudo) → PySpark (limpieza) → MongoDB Atlas (limpio) → Análisis / Clustering / Modelamiento → Storytelling**.

```
[Scrapers Python] → [MongoDB Atlas: colección cruda]
                          ↓
                  [PySpark: limpieza y normalización]
                          ↓
               [MongoDB Atlas: ContenedorAutosLimpio]
                          ↓
        ┌─────────────────┬───────────────────┐
     [EDA]           [Clustering]        [Regresión]
        └─────────────────┴───────────────────┘
                          ↓
                   [Storytelling / BI]
```

---

## Resumen de Indicadores Clave (KPIs)

| Indicador | Valor |
|---|---|
| Total de registros válidos | 1.988 |
| Precio promedio del mercado | $16.450.599 CLP |
| Kilometraje promedio | 71.070 km |
| Año promedio de fabricación | 2021 |
| Antigüedad promedio | 5 años |
| Correlación Precio–Kilometraje | -0.233 |
| Correlación Precio–Año | +0.236 |
| Correlación Kilometraje–Antigüedad | +0.700 |
| Anomalías detectadas en precio | 126 (6,34%) |
| Anomalías detectadas en kilometraje | 49 (2,46%) |
| Silhouette Score K-Means (k=4) | 0.446 |
| Número de clústeres seleccionados | 4 |

---

## Hallazgos Principales

- **El kilometraje y la antigüedad son los principales factores de depreciación.** A mayor kilometraje y años de uso, menor valor de mercado.
- **La marca modera el impacto del kilometraje.** Un mismo nivel de uso deprecia más a una marca generalista que a una premium.
- **Tres segmentos de riesgo diferenciados.** Vehículos con más de 8 años o más de 120.000 km caen en zona de alta depreciación, donde las tasaciones manuales tienen mayor probabilidad de error.
- **La geografía es un factor secundario.** Las diferencias de precio entre ciudades reflejan el tipo de vehículos disponibles, no una depreciación diferencial real.

---

## Segmentación K-Means (k=4)

| Clúster | Perfil | Precio Promedio | Kilometraje Promedio | Año Promedio |
|---|---|---|---|---|
| Clúster 1 | Alta depreciación | $11,6 M | 140.042 km | 2016 |
| Clúster 3 | Valor intermedio | $14,6 M | 52.455 km | 2022 |
| Clúster 0 | Recientes / diversidad | $15,8 M | 64.660 km | 2021 |
| Clúster 2 | Premium / alto valor | $41,8 M | 42.266 km | 2023 |

---

## Estructura del Repositorio

```
AutoTec/
├── README.md
├── autotec/
│   ├── algoritmo_supervisado/     # Modelos supervisados: regresión y clasificación
│   ├── analisis_descriptivo/      # EDA univariado y multivariado
│   ├── app/                       # Tableros y aplicación Streamlit
│   ├── clustering/                # K-Means, DBSCAN y PCA
│   ├── definicion_predictiva/     # Definición de variable objetivo y metadatos
│   ├── pipeline_contenedores/     # Limpieza y normalización con PySpark
│   ├── refinamiento_datos/        # Tratamiento de veracidad e ingeniería de atributos
│   └── scrapers/                  # Scripts de extracción por fuente
└── .env                           # Variables de entorno (MONGO_URI) — no subir al repo
```

---

## Fuentes de Datos

Los datos fueron recolectados mediante web scraping desde portales de compra y venta de vehículos usados en Chile:

| Integrante | Fuente(s) |
|---|---|
| Neiel Cortés | Autocosmos |
| Belén Andrades | Callegari, Gildemeister Usados, Valentini Seminuevos, Autoselect, Salazar Israel |
| Daniela Cofré | Yapo Autos Usados |
| Jocelyn León | Bruno Fritsch |
| Luz Azocar | Emol Automóviles |
| Javiera Pizarro | Clicar |
| Martin Rojas | Aspillaga Hornauer, Difor, Piamonte Usados |

---

## Variables del Dataset

### Variables originales

| Variable | Descripción |
|---|---|
| `marca` | Marca del vehículo |
| `modelo` | Modelo del vehículo |
| `year` | Año de fabricación |
| `kilometraje` | Kilometraje informado en la publicación |
| `combustible` | Tipo de combustible (Bencina, Diésel, Híbrido, Eléctrico) |
| `ciudad` | Ciudad o comuna de publicación |
| `precio` | Precio de venta en pesos chilenos |
| `fecha_captura` | Fecha en que se realizó el scraping |

### Variables derivadas (Ingeniería de Atributos)

| Variable | Descripción |
|---|---|
| `antiguedad_auto` | Años transcurridos desde la fabricación |
| `uso_anual_estimado` | Kilometraje promedio por año de uso |
| `rango_kilometraje` | Categoría: Bajo / Medio / Alto |
| `categoria_precio` | Categoría: Bajo / Medio / Alto |
| `tipo_marca` | Clasificación: Premium / Generalista |
| `es_ecologico` | Indica si el vehículo es híbrido o eléctrico |
| `segmento_depreciacion` | Segmento construido para análisis de depreciación |

---

## Tecnologías Utilizadas

- **Python** — scraping, limpieza, análisis y modelamiento
- **Selenium** + **undetected-chromedriver** — scraping de sitios dinámicos
- **BeautifulSoup** + **Requests** — scraping de sitios estáticos
- **MongoDB Atlas** — almacenamiento NoSQL en la nube
- **PySpark** — procesamiento distribuido y limpieza de datos
- **Pandas** + **NumPy** — análisis y manipulación de datos
- **Matplotlib** + **Seaborn** — visualización
- **Scikit-learn** — clustering (K-Means, DBSCAN) y modelos supervisados
- **Docker** + **Jupyter Lab** — entorno reproducible
- **Git** + **GitHub** — control de versiones y trabajo colaborativo

---

## Cómo Ejecutar el Proyecto

1. Clona el repositorio:
```bash
git clone https://github.com/IICG-Coquimbo/proyecto-big-data-2026-autotec.git
```

2. Configura el archivo `.env` con tu URI de MongoDB Atlas:
```
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
```

3. Levanta el entorno Docker:
```bash
docker-compose up -d
```

4. Accede a Jupyter Lab en `http://localhost:8888`

5. Ejecuta los notebooks en orden:
   - `scrapers/` → extracción de datos
   - `limpieza/` → normalización con PySpark
   - `eda/` → análisis exploratorio
   - `clustering/` → segmentación K-Means
   - `modelos/` → predicción supervisada
   - `storytelling/` → visualizaciones y KPIs por nivel
