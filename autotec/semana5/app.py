# app.py - Semana 5 AutoTec
# Responsable: Jocy
# Nivel 3: Tablero Operacional para Supervisores
# Base: proyecto_bigdata
# Colección: Contenedor_Autos_Limpio1

import os
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from pymongo import MongoClient

# --------------------------------------------------
# Configuración general
# --------------------------------------------------
st.set_page_config(
    page_title="AutoTec - Tablero Operacional",
    layout="wide"
)

st.title("AutoTec | Tablero Operacional")
st.markdown(
    "Dashboard orientado a supervisores para controlar alertas diarias, "
    "priorizar vehículos críticos y revisar publicaciones antes de la venta."
)
st.markdown("---")

# --------------------------------------------------
# Conexión MongoDB
# --------------------------------------------------
load_dotenv("/home/jovyan/work/.env")
load_dotenv("/home/jovyan/work/autotec/.env")
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

DATABASE_NAME = "proyecto_bigdata"
COLLECTION_NAME = "Contenedor_Autos_Limpio1"


@st.cache_data(ttl=600)
def cargar_datos_mongo():
    if not MONGO_URI:
        raise ValueError(
            "No se encontró MONGO_URI. Revisa el archivo .env."
        )

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")

    db = client[DATABASE_NAME]

    if COLLECTION_NAME not in db.list_collection_names():
        raise ValueError(
            f"No se encontró la colección {COLLECTION_NAME}. "
            f"Colecciones disponibles: {db.list_collection_names()}"
        )

    docs = list(db[COLLECTION_NAME].find({}, {"_id": 0}))

    if len(docs) == 0:
        raise ValueError("La colección no tiene registros.")

    return pd.DataFrame(docs)


def buscar_columna(df, opciones):
    for col in opciones:
        if col in df.columns:
            return col
    return None


def convertir_numero(serie):
    if pd.api.types.is_numeric_dtype(serie):
        return pd.to_numeric(serie, errors="coerce")

    return pd.to_numeric(
        serie.astype(str).str.replace(r"[^0-9]", "", regex=True),
        errors="coerce"
    )


def preparar_datos(df_original):
    df = df_original.copy()
    df.columns = [str(c).strip() for c in df.columns]

    col_marca = buscar_columna(df, ["marca", "Marca", "brand"])
    col_modelo = buscar_columna(df, ["modelo", "Modelo", "model"])
    col_precio = buscar_columna(df, ["precio_num", "precio", "Precio", "price"])
    col_km = buscar_columna(df, ["km_num", "kilometraje", "Kilometraje", "kms", "km"])
    col_year = buscar_columna(df, ["year_limpio", "year", "Year", "anio", "año", "Año"])
    col_combustible = buscar_columna(df, ["combustible", "Combustible", "tipo_combustible", "fuel"])
    col_ciudad = buscar_columna(df, ["ciudad", "Ciudad", "ciudad_o_comuna", "comuna", "ubicacion"])
    col_url = buscar_columna(df, ["url", "URL", "link"])

    df["marca_op"] = df[col_marca].astype(str).str.strip().str.title() if col_marca else "Sin marca"
    df["modelo_op"] = df[col_modelo].astype(str).str.strip().str.title() if col_modelo else "Sin modelo"
    df["combustible_op"] = df[col_combustible].astype(str).str.strip().str.title() if col_combustible else "Sin combustible"
    df["ciudad_op"] = df[col_ciudad].astype(str).str.strip().str.title() if col_ciudad else "Sin ciudad"
    df["url_op"] = df[col_url].astype(str).str.strip() if col_url else ""

    df["precio_op"] = convertir_numero(df[col_precio]) if col_precio else np.nan
    df["km_op"] = convertir_numero(df[col_km]) if col_km else np.nan
    df["year_op"] = convertir_numero(df[col_year]) if col_year else np.nan

    df = df.dropna(subset=["precio_op", "km_op", "year_op"])

    df = df[
        (df["precio_op"] > 0) &
        (df["km_op"] >= 0) &
        (df["year_op"] >= 1990)
    ].copy()

    df["year_op"] = df["year_op"].astype(int)

    return df


# --------------------------------------------------
# Carga de datos
# --------------------------------------------------
try:
    df_raw = cargar_datos_mongo()
    df = preparar_datos(df_raw)

except Exception as e:
    st.error("No se pudo cargar la base operacional desde MongoDB.")
    st.warning(
        "Revisa que el archivo .env tenga MONGO_URI y que la colección se llame "
        "Contenedor_Autos_Limpio1 dentro de proyecto_bigdata."
    )
    st.exception(e)
    st.stop()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.header("Configuración operacional")
st.sidebar.success("Conexión MongoDB activa")
st.sidebar.info(f"Base: {DATABASE_NAME}")
st.sidebar.info(f"Colección: {COLLECTION_NAME}")

st.sidebar.markdown("### Umbrales principales")

umbral_km = st.sidebar.slider(
    "Kilometraje crítico",
    min_value=0,
    max_value=int(df["km_op"].max()),
    value=150000,
    step=10000
)

umbral_year = st.sidebar.slider(
    "Año mínimo para revisión",
    min_value=int(df["year_op"].min()),
    max_value=int(df["year_op"].max()),
    value=max(int(df["year_op"].min()), 2014),
    step=1
)

percentil_precio = st.sidebar.slider(
    "Percentil para precio fuera de rango",
    min_value=80,
    max_value=99,
    value=95,
    step=1
)

st.sidebar.markdown("### Umbrales complementarios")

umbral_uso_anual_alto = st.sidebar.number_input(
    "Uso anual crítico km/año",
    min_value=10000,
    max_value=80000,
    value=30000,
    step=5000
)

umbral_uso_anual_bajo = st.sidebar.number_input(
    "Uso anual bajo km/año",
    min_value=500,
    max_value=10000,
    value=3000,
    step=500
)


# --------------------------------------------------
# Filtros
# --------------------------------------------------
st.header("Filtros de supervisión diaria")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    marcas = sorted(df["marca_op"].dropna().unique())
    marcas_sel = st.multiselect(
        "Marca",
        options=marcas,
        default=marcas[:10]
    )

with col_f2:
    ciudades = sorted(df["ciudad_op"].dropna().unique())
    ciudades_sel = st.multiselect(
        "Ciudad",
        options=ciudades,
        default=ciudades[:10]
    )

with col_f3:
    combustibles = sorted(df["combustible_op"].dropna().unique())
    combustibles_sel = st.multiselect(
        "Combustible",
        options=combustibles,
        default=combustibles[:6]
    )

df_op = df[
    df["marca_op"].isin(marcas_sel) &
    df["ciudad_op"].isin(ciudades_sel) &
    df["combustible_op"].isin(combustibles_sel)
].copy()

if df_op.empty:
    st.warning("No hay vehículos disponibles con los filtros seleccionados.")
    st.stop()


# --------------------------------------------------
# Alertas operacionales principales
# --------------------------------------------------
limite_precio_alto = df_op["precio_op"].quantile(percentil_precio / 100)
limite_precio_bajo = df_op["precio_op"].quantile((100 - percentil_precio) / 100)
precio_mediano = df_op["precio_op"].median()

df_op["alerta_km_critico"] = df_op["km_op"] >= umbral_km
df_op["alerta_year_revision"] = df_op["year_op"] <= umbral_year

df_op["alerta_precio_fuera_rango"] = (
    (df_op["precio_op"] >= limite_precio_alto) |
    (df_op["precio_op"] <= limite_precio_bajo)
)

df_op["alerta_datos_incompletos"] = False

for col in ["marca_op", "modelo_op", "combustible_op", "ciudad_op"]:
    df_op["alerta_datos_incompletos"] = (
        df_op["alerta_datos_incompletos"] |
        df_op[col].isna() |
        df_op[col].astype(str).str.strip().isin([
            "",
            "Nan",
            "None",
            "Sin Marca",
            "Sin Modelo",
            "Sin Combustible",
            "Sin Ciudad"
        ])
    )

df_op["alerta_revision_publicacion"] = (
    (df_op["km_op"] >= umbral_km) &
    (df_op["precio_op"] >= precio_mediano)
)

columnas_alertas = [
    "alerta_km_critico",
    "alerta_year_revision",
    "alerta_precio_fuera_rango",
    "alerta_datos_incompletos",
    "alerta_revision_publicacion"
]

df_op["total_alertas"] = df_op[columnas_alertas].sum(axis=1)

df_op["prioridad_operacional"] = np.select(
    [
        df_op["total_alertas"] >= 3,
        df_op["total_alertas"] == 2,
        df_op["total_alertas"] == 1
    ],
    [
        "Alta",
        "Media",
        "Baja"
    ],
    default="Sin alerta"
)


# --------------------------------------------------
# KPIs complementarios
# --------------------------------------------------
anio_actual = pd.Timestamp.today().year

df_op["antiguedad_op"] = (anio_actual - df_op["year_op"]).clip(lower=1)
df_op["uso_anual_estimado"] = df_op["km_op"] / df_op["antiguedad_op"]

df_op["precio_por_km"] = np.where(
    df_op["km_op"] > 0,
    df_op["precio_op"] / df_op["km_op"],
    np.nan
)

df_op["alerta_uso_anual_critico"] = df_op["uso_anual_estimado"] > umbral_uso_anual_alto

df_op["alerta_uso_anual_bajo"] = (
    (df_op["antiguedad_op"] >= 5) &
    (df_op["uso_anual_estimado"] < umbral_uso_anual_bajo)
)

df_op["alerta_sin_url"] = (
    df_op["url_op"].isna() |
    df_op["url_op"].astype(str).str.strip().isin(["", "nan", "None", "Sin url"]) |
    (df_op["url_op"].astype(str).str.len() < 8)
)

df_op["alerta_posible_duplicado"] = df_op.duplicated(
    subset=["marca_op", "modelo_op", "year_op", "km_op", "precio_op"],
    keep=False
)

serie_ppkm = df_op["precio_por_km"].replace([np.inf, -np.inf], np.nan).dropna()

if len(serie_ppkm) >= 10:
    limite_ppkm_bajo = serie_ppkm.quantile(0.05)
    limite_ppkm_alto = serie_ppkm.quantile(0.95)

    df_op["alerta_precio_km_extremo"] = (
        (df_op["precio_por_km"] <= limite_ppkm_bajo) |
        (df_op["precio_por_km"] >= limite_ppkm_alto)
    )
else:
    df_op["alerta_precio_km_extremo"] = False

conteo_marcas = df_op["marca_op"].value_counts()
marcas_baja_muestra = conteo_marcas[conteo_marcas <= 3].index
df_op["alerta_marca_baja_muestra"] = df_op["marca_op"].isin(marcas_baja_muestra)

columnas_alertas_complementarias = [
    "alerta_uso_anual_critico",
    "alerta_uso_anual_bajo",
    "alerta_sin_url",
    "alerta_posible_duplicado",
    "alerta_precio_km_extremo",
    "alerta_marca_baja_muestra"
]

df_op["total_alertas_complementarias"] = df_op[columnas_alertas_complementarias].sum(axis=1)


# --------------------------------------------------
# Función KPI
# --------------------------------------------------
total_vehiculos = len(df_op)

def porcentaje(condicion):
    return round((condicion.sum() / total_vehiculos) * 100, 2)


# --------------------------------------------------
# KPIs principales
# --------------------------------------------------
st.markdown("---")
st.header("KPIs operacionales principales")

col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)

with col_k1:
    st.metric("Vehículos supervisados", total_vehiculos)

with col_k2:
    st.metric("% prioridad alta", f"{porcentaje(df_op['prioridad_operacional'] == 'Alta')}%")

with col_k3:
    st.metric("% km crítico", f"{porcentaje(df_op['alerta_km_critico'])}%")

with col_k4:
    st.metric("% precio fuera de rango", f"{porcentaje(df_op['alerta_precio_fuera_rango'])}%")

with col_k5:
    st.metric("% datos incompletos", f"{porcentaje(df_op['alerta_datos_incompletos'])}%")

tabla_kpis = pd.DataFrame({
    "KPI operacional": [
        "% vehículos con prioridad alta",
        "% vehículos con kilometraje crítico",
        "% vehículos con precio fuera de rango",
        "% publicaciones con datos incompletos",
        "% vehículos que requieren revisión de publicación"
    ],
    "Objetivo operacional": [
        "Priorizar revisión diaria de unidades críticas",
        "Detectar vehículos con alto nivel de uso",
        "Revisar precios extremos antes de publicar o vender",
        "Corregir información faltante en publicaciones",
        "Detectar autos con alto kilometraje y precio sobre la mediana"
    ],
    "Frecuencia": [
        "Diaria",
        "Diaria",
        "Diaria",
        "Diaria",
        "Diaria"
    ],
    "Valor KPI (%)": [
        porcentaje(df_op["prioridad_operacional"] == "Alta"),
        porcentaje(df_op["alerta_km_critico"]),
        porcentaje(df_op["alerta_precio_fuera_rango"]),
        porcentaje(df_op["alerta_datos_incompletos"]),
        porcentaje(df_op["alerta_revision_publicacion"])
    ]
})

st.dataframe(tabla_kpis, hide_index=True, use_container_width=True)


# --------------------------------------------------
# KPIs complementarios
# --------------------------------------------------
st.markdown("---")
st.header("KPIs operacionales complementarios")

tabla_kpis_complementarios = pd.DataFrame({
    "KPI operacional complementario": [
        "% vehículos con uso anual crítico",
        "% vehículos con uso anual sospechosamente bajo",
        "% publicaciones sin URL válida",
        "% vehículos posiblemente duplicados",
        "% vehículos con precio por km fuera de rango",
        "% vehículos de marcas con baja muestra"
    ],
    "Objetivo operacional": [
        "Detectar vehículos con uso intensivo para revisión prioritaria",
        "Revisar kilometrajes poco coherentes con la antigüedad del vehículo",
        "Corregir publicaciones sin enlace o con enlace inválido",
        "Detectar registros repetidos antes de reportar o publicar",
        "Identificar valores extremos considerando precio y kilometraje",
        "Evitar decisiones basadas en marcas con poca representación"
    ],
    "Frecuencia": [
        "Diaria",
        "Diaria",
        "Diaria",
        "Diaria",
        "Semanal",
        "Semanal"
    ],
    "Valor KPI (%)": [
        porcentaje(df_op["alerta_uso_anual_critico"]),
        porcentaje(df_op["alerta_uso_anual_bajo"]),
        porcentaje(df_op["alerta_sin_url"]),
        porcentaje(df_op["alerta_posible_duplicado"]),
        porcentaje(df_op["alerta_precio_km_extremo"]),
        porcentaje(df_op["alerta_marca_baja_muestra"])
    ]
})

st.dataframe(tabla_kpis_complementarios, hide_index=True, use_container_width=True)


# --------------------------------------------------
# Visualizaciones
# --------------------------------------------------
st.markdown("---")
st.header("Visualizaciones operacionales")

# Gráfico 1: prioridad operacional
st.subheader("1. Semáforo de prioridad operacional")

df_prioridad = df_op["prioridad_operacional"].value_counts().reset_index()
df_prioridad.columns = ["prioridad_operacional", "cantidad"]

orden_prioridad = ["Alta", "Media", "Baja", "Sin alerta"]

df_prioridad["prioridad_operacional"] = pd.Categorical(
    df_prioridad["prioridad_operacional"],
    categories=orden_prioridad,
    ordered=True
)

df_prioridad = df_prioridad.sort_values("prioridad_operacional")

fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.bar(df_prioridad["prioridad_operacional"].astype(str), df_prioridad["cantidad"])
ax1.set_title("Cantidad de vehículos por prioridad operacional")
ax1.set_xlabel("Prioridad operacional")
ax1.set_ylabel("Cantidad de vehículos")

for i, valor in enumerate(df_prioridad["cantidad"]):
    ax1.text(i, valor, str(valor), ha="center", va="bottom")

st.pyplot(fig1)

st.write(
    "Este gráfico permite ordenar la revisión diaria. Los vehículos con prioridad alta "
    "deben revisarse primero porque acumulan más alertas operacionales."
)

st.markdown("---")

# Gráfico 2: alertas principales
st.subheader("2. Distribución de alertas operacionales principales")

df_alertas = pd.DataFrame({
    "tipo_alerta": [
        "Kilometraje crítico",
        "Año para revisión",
        "Precio fuera de rango",
        "Datos incompletos",
        "Revisión de publicación"
    ],
    "cantidad": [
        int(df_op["alerta_km_critico"].sum()),
        int(df_op["alerta_year_revision"].sum()),
        int(df_op["alerta_precio_fuera_rango"].sum()),
        int(df_op["alerta_datos_incompletos"].sum()),
        int(df_op["alerta_revision_publicacion"].sum())
    ]
}).sort_values("cantidad", ascending=True)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.barh(df_alertas["tipo_alerta"], df_alertas["cantidad"])
ax2.set_title("Cantidad de vehículos por tipo de alerta operacional")
ax2.set_xlabel("Cantidad de vehículos")
ax2.set_ylabel("Tipo de alerta")

for i, valor in enumerate(df_alertas["cantidad"]):
    ax2.text(valor, i, str(valor), va="center")

st.pyplot(fig2)

st.write(
    "Este gráfico permite decidir si la revisión diaria debe enfocarse en kilometraje, "
    "año, precio fuera de rango, datos incompletos o revisión de publicación."
)

st.markdown("---")

# Gráfico 3: mapa km precio
st.subheader("3. Mapa operacional: kilometraje versus precio")

fig3, ax3 = plt.subplots(figsize=(10, 6))

for prioridad in orden_prioridad:
    subset = df_op[df_op["prioridad_operacional"] == prioridad]
    ax3.scatter(
        subset["km_op"],
        subset["precio_op"],
        alpha=0.6,
        label=prioridad
    )

ax3.axvline(umbral_km, linestyle="--")
ax3.axhline(precio_mediano, linestyle="--")
ax3.set_title("Vehículos según kilometraje, precio y prioridad operacional")
ax3.set_xlabel("Kilometraje")
ax3.set_ylabel("Precio")
ax3.legend(title="Prioridad")

st.pyplot(fig3)

st.write(
    "Este gráfico permite detectar autos con alto kilometraje, precio elevado "
    "o acumulación de alertas antes de publicarlos o destacarlos."
)

st.markdown("---")

# Gráfico 4: alertas complementarias
st.subheader("4. Alertas operacionales complementarias")

df_alertas_complementarias = pd.DataFrame({
    "alerta_complementaria": [
        "Uso anual crítico",
        "Uso anual bajo",
        "Sin URL válida",
        "Posible duplicado",
        "Precio por km extremo",
        "Marca con baja muestra"
    ],
    "cantidad": [
        int(df_op["alerta_uso_anual_critico"].sum()),
        int(df_op["alerta_uso_anual_bajo"].sum()),
        int(df_op["alerta_sin_url"].sum()),
        int(df_op["alerta_posible_duplicado"].sum()),
        int(df_op["alerta_precio_km_extremo"].sum()),
        int(df_op["alerta_marca_baja_muestra"].sum())
    ]
}).sort_values("cantidad", ascending=True)

fig4, ax4 = plt.subplots(figsize=(10, 5))
ax4.barh(
    df_alertas_complementarias["alerta_complementaria"],
    df_alertas_complementarias["cantidad"]
)
ax4.set_title("Cantidad de vehículos por alerta operacional complementaria")
ax4.set_xlabel("Cantidad de vehículos")
ax4.set_ylabel("Tipo de alerta complementaria")

for i, valor in enumerate(df_alertas_complementarias["cantidad"]):
    ax4.text(valor, i, str(valor), va="center")

st.pyplot(fig4)

st.write(
    "Este gráfico entrega una segunda capa de control operacional, permitiendo revisar "
    "duplicados, enlaces inválidos, uso anual incoherente y valores extremos."
)


# --------------------------------------------------
# Listado operacional final
# --------------------------------------------------
st.markdown("---")
st.header("Listado operacional de vehículos a revisar")

columnas_mostrar = [
    "prioridad_operacional",
    "total_alertas",
    "total_alertas_complementarias",
    "marca_op",
    "modelo_op",
    "year_op",
    "km_op",
    "precio_op",
    "ciudad_op",
    "combustible_op",
    "antiguedad_op",
    "uso_anual_estimado",
    "precio_por_km",
    "alerta_km_critico",
    "alerta_year_revision",
    "alerta_precio_fuera_rango",
    "alerta_datos_incompletos",
    "alerta_revision_publicacion",
    "alerta_uso_anual_critico",
    "alerta_uso_anual_bajo",
    "alerta_sin_url",
    "alerta_posible_duplicado",
    "alerta_precio_km_extremo",
    "alerta_marca_baja_muestra",
    "url_op"
]

columnas_existentes = [col for col in columnas_mostrar if col in df_op.columns]

df_lista = df_op[columnas_existentes].sort_values(
    ["total_alertas_complementarias", "total_alertas", "km_op"],
    ascending=[False, False, False]
)

st.dataframe(df_lista.head(100), hide_index=True, use_container_width=True)

st.success(
    "Conclusión operacional: este dashboard permite priorizar revisiones diarias, "
    "detectar vehículos críticos, corregir publicaciones incompletas, revisar posibles duplicados "
    "y controlar valores extremos antes de publicar o vender."
)
