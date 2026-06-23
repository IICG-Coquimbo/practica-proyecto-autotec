import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import base64
from pathlib import Path
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# 1. Configuración de la página
st.set_page_config(page_title="Dashboard Automotriz Ejecutivo", layout="wide")
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<style>
:root {
    --bg-main: #F5F5F4;
    --bg-card: #FFFFFF;
    --bg-sidebar: linear-gradient(180deg, #1F2937 0%, #111827 100%);
    --text-main: #1F2937;
    --text-soft: #6B7280;
    --text-light: #F9FAFB;
    --accent: #B91C1C;
    --accent-soft: #FEE2E2;
    --border: #E5E7EB;
    --shadow: 0 6px 18px rgba(17, 24, 39, 0.08);
}
/* App general */
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FAFAF9 0%, #F3F4F6 100%);
    color: var(--text-main);
}
[data-testid="stHeader"] {
    background: rgba(250, 250, 249, 0.85);
}
/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bg-sidebar);
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * {
    color: var(--text-light) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Playfair Display', serif !important;
    color: #FFFFFF !important;
    letter-spacing: 0.3px;
}
/* Labels sidebar */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] p {
    color: #E5E7EB !important;
    font-weight: 500;
}
/* Selects y multiselect */
[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 14px !important;
    min-height: 44px !important;
}
/* Texto interno inputs */
[data-baseweb="select"] input,
[data-baseweb="select"] span {
    color: #F9FAFB !important;
}
/* Chips multiselect */
[data-baseweb="tag"] {
    background-color: rgba(185, 28, 28, 0.22) !important;
    border: 1px solid rgba(248, 113, 113, 0.22) !important;
    color: #FEE2E2 !important;
    border-radius: 999px !important;
    padding-inline: 6px !important;
}
/* Tabs */
button[data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    color: #4B5563 !important;
    padding-bottom: 10px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 3px solid var(--accent) !important;
}
/* Títulos */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #111827;
    letter-spacing: 0.2px;
}
h1 {
    font-size: 3rem !important;
    margin-bottom: 0.2rem;
}
h2 {
    font-size: 2rem !important;
}
/* Texto secundario */
p, .stCaption {
    color: var(--text-soft);
}
/* KPI cards */
[data-testid="metric-container"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #FCFCFC 100%);
    border: 1px solid #E5E7EB;
    padding: 18px 16px;
    border-radius: 18px;
    box-shadow: var(--shadow);
}
[data-testid="metric-container"] label {
    color: #6B7280 !important;
    font-weight: 600;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #111827;
    font-weight: 700;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    background: #FEE2E2;
    color: #991B1B !important;
    padding: 4px 8px;
    border-radius: 999px;
    width: fit-content;
}
/* Botones */
.stButton > button {
    background: linear-gradient(180deg, #B91C1C 0%, #991B1B 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1rem;
    font-weight: 600;
    box-shadow: 0 6px 14px rgba(185, 28, 28, 0.22);
}
.stButton > button:hover {
    background: linear-gradient(180deg, #991B1B 0%, #7F1D1D 100%);
    color: white;
}
/* Dataframe y contenedores */
[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
}
/* Expanders */
details {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 0.35rem 0.75rem;
}
/* Separadores */
hr {
    border: none;
    border-top: 1px solid #E5E7EB;
}
/* Plotly chart card effect */
[data-testid="stPlotlyChart"],
[data-testid="stPyplotChart"] {
    background: #FFFFFF;
    border: 1px solid #ECECEC;
    border-radius: 18px;
    padding: 10px;
    box-shadow: var(--shadow);
}
/* Bloques principales */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.hero-box {
    position: relative;
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e5e7eb;
    border-radius: 22px;
    padding: 2rem 2rem 1.5rem 2rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
    overflow: hidden;
    min-height: 180px;
}
.hero-text h1 {
    margin: 0;
    font-size: 2.8rem;
    color: #111827;
}
.hero-text .sub {
    margin-top: 0.4rem;
    font-size: 1.15rem;
    color: #991b1b;
    font-weight: 600;
}
.hero-text .mini {
    margin-top: 0.25rem;
    color: #6b7280;
}
.car-corner {
    position: absolute;
    right: 18px;
    top: 12px;
    width: 180px;
    max-width: 22%;
    opacity: 0.95;
    object-fit: contain;
    pointer-events: none;
}
@media (max-width: 900px) {
    .car-corner {
        width: 110px;
        top: 14px;
        right: 12px;
        opacity: 0.85;
    }
    .hero-box {
        min-height: 160px;
        padding-right: 7rem;
    }

    .hero-text h1 {
        font-size: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.kpi-card {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 18px 18px 16px 18px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
    min-height: 145px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.10);
}

.kpi-label {
    font-size: 0.92rem;
    font-weight: 600;
    color: #6b7280;
    margin-bottom: 0.6rem;
    font-family: 'Inter', sans-serif;
}

.kpi-value {
    font-size: 2.25rem;
    line-height: 1.05;
    font-weight: 700;
    color: #111827;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.02em;
}
.kpi-badge {
    display: inline-block;
    width: fit-content;
    margin-top: 0.9rem;
    background: #fee2e2;
    color: #991b1b;
    font-size: 0.86rem;
    font-weight: 600;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    border: 1px solid #fecaca;
}
@media (max-width: 900px) {
    .kpi-card {
        min-height: 125px;
        padding: 16px;
    }

    .kpi-value {
        font-size: 1.7rem;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Ocultar botón de Deploy y menús por defecto */
    .stDeployButton {
        display: none;
    }
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }    
    /* Hacer completamente transparente la barra superior al hacer scroll */
    header[data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0) !important;
        background: transparent !important;
    }
    header[data-testid="stHeader"] > div {
        background-color: rgba(0, 0, 0, 0) !important;
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    .hero-box {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2f7 100%);
        padding: 28px 32px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        margin-bottom: 22px;
    }
    .hero-b {
        background: linear-gradient(180deg, #1F2937 0%, #111827 100%);
        padding: 28px 32px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        margin-bottom: 22px;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 8px;
    }    
    .hero-subtitle {
        font-size: 1.05rem;
        color: #4b5563;
        line-height: 1.6;
    }    
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #111827;
        margin-top: 8px;
        margin-bottom: 18px;
    }    
    .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 22px 24px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
        height: 100%;
    }    
    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 14px;
    }    
    .card-item {
        font-size: 0.96rem;
        color: #4b5563;
        margin-bottom: 10px;
        line-height: 1.5;
    }   
    .card-item b {
        color: #111827;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown("""
<style>
.hero-b{
    position: relative;
    background: linear-gradient(135deg, #0f172a 0%, #102a43 45%, #0b132b 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 2rem 2rem 1.5rem 2rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
    overflow: hidden;
    min-height: 180px;
}
.hero-b .hero-text h1{
    margin: 0;
    font-size: 2.8rem;
    color: #F8FAFC !important;
    text-shadow: 0 2px 10px rgba(0,0,0,0.25);
}
.hero-b .hero-text .sub{
    margin-top: 0.45rem;
    font-size: 1.15rem;
    color: #FCA5A5 !important;
    font-weight: 700;
}
.hero-b .hero-text .mini{
    margin-top: 0.3rem;
    color: #E2E8F0 !important;
    font-size: 1rem;
}
.hero-b .car-corner{
    position: absolute;
    right: 18px;
    top: 12px;
    width: 180px;
    max-width: 22%;
    object-fit: contain;
    pointer-events: none;
}
@media (max-width: 900px){
    .hero-b{
        min-height: 160px;
        padding-right: 7rem;
    }

    .hero-b .hero-text h1{
        font-size: 2rem;
    }

    .hero-b .car-corner{
        width: 110px;
        top: 14px;
        right: 12px;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
div[data-baseweb="select"] > div {
    background: #F4F8FC !important;
    border: 1px solid #002855 !important;
    border-radius: 12px !important;
    min-height: 46px !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] input {
    color: #002855 !important;
    font-weight: 600 !important;
}

div[data-baseweb="select"] svg {
    fill: #002855 !important;
}
</style>
""", unsafe_allow_html=True)
#Imagen
BASE_DIR = Path(__file__).resolve().parent
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64(BASE_DIR / "logo.png")
st.markdown(f"""
<div class="hero-b">
    <div class="hero-text">
        <h1>Cuadro de Mando Integral</h1>
        <p class="sub">Analítica Automotriz Ejecutiva</p>
        <p class="mini">Nivel Estratégico, Táctico y Operativo</p>
    </div>
    <img class="car-corner" src="data:image/png;base64,{img}">
</div>
""", unsafe_allow_html=True)

# 2. Carga de datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("datos_autotec.csv")

    # Estandarización mínima
    if "precio" in df.columns:
        df["precio"] = pd.to_numeric(df["precio"], errors="coerce")

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

    if "kilometraje" in df.columns:
        df["kilometraje"] = pd.to_numeric(df["kilometraje"], errors="coerce")

    return df

df = cargar_datos()
# =========================
# Cluster de marcas
# =========================
df_cluster_base = df.dropna(subset=["marca", "precio", "kilometraje"]).copy()

resumen_cluster = (
    df_cluster_base.groupby("marca", as_index=False)
    .agg(
        precio_promedio=("precio", "mean"),
        kilometraje_promedio=("kilometraje", "mean"),
        cantidad=("marca", "count")
    )
)
scaler = StandardScaler()
X = resumen_cluster[["precio_promedio", "kilometraje_promedio"]]
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
resumen_cluster["cluster"] = kmeans.fit_predict(X_scaled)

centros = pd.DataFrame(
    scaler.inverse_transform(kmeans.cluster_centers_),
    columns=["precio_promedio", "kilometraje_promedio"]
)
orden_clusters = centros.sort_values("precio_promedio").index.tolist()

mapa_cluster = {
    orden_clusters[0]: "Económico",
    orden_clusters[1]: "Intermedio",
    orden_clusters[2]: "Costoso"
}
resumen_cluster["cluster_nombre"] = resumen_cluster["cluster"].map(mapa_cluster)

# SIDE BAR
st.sidebar.header("Filtros globales")
df_base = cargar_datos().copy()
marcas = sorted(df_base["marca"].dropna().unique()) if "marca" in df_base.columns else []
top_10_marcas = (
    df_base["marca"]
    .dropna()
    .value_counts()
    .head(10)
    .index
    .tolist()
) if "marca" in df_base.columns else []
# Valores por defecto
if "filtro_marcas" not in st.session_state:
    st.session_state["filtro_marcas"] = top_10_marcas

if "filtro_modelos" not in st.session_state:
    st.session_state["filtro_modelos"] = []

if "filtro_combustible" not in st.session_state:
    st.session_state["filtro_combustible"] = "Todos"

if "filtro_categoria_precio" not in st.session_state:
    st.session_state["filtro_categoria_precio"] = "Todas"

if "filtro_ciudades" not in st.session_state:
    st.session_state["filtro_ciudades"] = []

if "filtro_tipo_marca" not in st.session_state:
    st.session_state["filtro_tipo_marca"] = []

if "year" in df_base.columns and "filtro_year" not in st.session_state:
    st.session_state["filtro_year"] = (
        2000,
        int(df_base["year"].dropna().max())
    )
if "kilometraje" in df_base.columns and df_base["kilometraje"].notna().any() and "filtro_km" not in st.session_state:
    st.session_state["filtro_km"] = (
        int(df_base["kilometraje"].dropna().min()),
        int(df_base["kilometraje"].dropna().max())
    )
# Botón limpiar filtros
def limpiar_filtros():
    st.session_state["filtro_marcas"] = top_10_marcas
    st.session_state["filtro_modelos"] = []
    st.session_state["filtro_combustible"] = "Todos"
    st.session_state["filtro_categoria_precio"] = "Todas"
    st.session_state["filtro_ciudades"] = []
    st.session_state["filtro_tipo_marca"] = []
    if "year" in df_base.columns:
        st.session_state["filtro_year"] = (
            2000,
            int(df_base["year"].dropna().max())
        )
    if "kilometraje" in df_base.columns and df_base["kilometraje"].notna().any():
        st.session_state["filtro_km"] = (
            int(df_base["kilometraje"].dropna().min()),
            int(df_base["kilometraje"].dropna().max())
        )
st.sidebar.button("Limpiar filtros", on_click=limpiar_filtros)
# Marca
marcas_sel = st.sidebar.multiselect(
    "Selecciona marcas:",
    options=marcas,
    key="filtro_marcas"
)

df_filtrado = df_base.copy()
if "marca" in df_filtrado.columns and marcas_sel:
    df_filtrado = df_filtrado[df_filtrado["marca"].isin(marcas_sel)]
# Año
if "year" in df_filtrado.columns and df_filtrado["year"].notna().any():
    year_min = 2000
    year_max = int(df_base["year"].dropna().max())
    st.sidebar.slider(
        "Rango de año:",
        min_value=year_min,
        max_value=year_max,
        key="filtro_year"
    )
    df_filtrado = df_filtrado[
        (df_filtrado["year"] >= st.session_state["filtro_year"][0]) &
        (df_filtrado["year"] <= st.session_state["filtro_year"][1])
    ]
# Combustible como radio (círculos)
if "combustible" in df_filtrado.columns:
    combustibles = sorted(df_base["combustible"].dropna().astype(str).unique())
    opciones_comb = ["Todos"] + combustibles
    st.sidebar.radio(
        "Tipo de combustible:",
        options=opciones_comb,
        key="filtro_combustible"
    )
    if st.session_state["filtro_combustible"] != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["combustible"].astype(str) == st.session_state["filtro_combustible"]
        ]

# Categoría de precio como radio (círculos)
if "categoria_precio" in df_filtrado.columns:
    categorias = sorted(df_base["categoria_precio"].dropna().astype(str).unique())
    opciones_cat = ["Todas"] + categorias
    st.sidebar.radio(
        "Tipo de precio:",
        options=opciones_cat,
        key="filtro_categoria_precio"
    )
    if st.session_state["filtro_categoria_precio"] != "Todas":
        df_filtrado = df_filtrado[
            df_filtrado["categoria_precio"].astype(str) == st.session_state["filtro_categoria_precio"]
        ]

# Ciudad
if "ciudad" in df_filtrado.columns:
    ciudades = sorted(df_filtrado["ciudad"].dropna().astype(str).unique())
    st.sidebar.multiselect(
        "Ciudad:",
        options=ciudades,
        key="filtro_ciudades"
    )
    if st.session_state["filtro_ciudades"]:
        df_filtrado = df_filtrado[
            df_filtrado["ciudad"].astype(str).isin(st.session_state["filtro_ciudades"])
        ]
# Kilometraje
if "kilometraje" in df_filtrado.columns and df_filtrado["kilometraje"].notna().any():
    km_min = int(df_base["kilometraje"].dropna().min())
    km_max = int(df_base["kilometraje"].dropna().max())
    st.sidebar.slider(
        "Rango de kilometraje:",
        min_value=km_min,
        max_value=km_max,
        step=5000,
        key="filtro_km"
    )
    df_filtrado = df_filtrado[
        (df_filtrado["kilometraje"] >= st.session_state["filtro_km"][0]) &
        (df_filtrado["kilometraje"] <= st.session_state["filtro_km"][1])
    ]
st.sidebar.metric("Registros filtrados:", len(df_filtrado))
df = df_filtrado.copy()
if df.empty:
    st.warning("No hay datos disponibles con los filtros seleccionados.")
    st.stop()


# 4. Tabs por nivel organizacional
tab_inicio, tab_est, tab_tac, tab_op = st.tabs([
    "Inicio",
    "Nivel Estratégico",
    "Nivel Táctico",
    "Nivel Operacional"
])
with tab_inicio: 
    import streamlit as st
    st.title("AutoTec")
    st.header("Propuesta de Valor:")
    st.subheader("Definir el precio justo de un auto usado según sus características y el mercado.")
    st.markdown(
        """
        AutoTec analiza información como marca, modelo, año, kilometraje, combustible y 
        comportamiento del mercado para estimar un valor referencial que apoye decisiones 
        de compra, venta y tasación.
        """
    )
  #  img2 = get_base64(BASE_DIR / "auto.jpeg")
   # st.markdown(f"""
    #<div class="card">
    #    <img  src="data:image/jpg;base64,{img2}">
    #</div>
   # """, unsafe_allow_html=True)
    
    st.header("Estructura de Datos")
    col1, col2 = st.columns(2, gap="large") 
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">Identificación del vehículo</div>
            <div class="card-item"><b>marca:</b> Marca del vehículo.</div>
            <div class="card-item"><b>modelo:</b> Modelo del vehículo.</div>
            <div class="card-item"><b>year:</b> Año de fabricación.</div>
        </div>
        """, unsafe_allow_html=True)
    
        st.markdown("<br>", unsafe_allow_html=True)
    
        st.markdown("""
        <div class="card">
            <div class="card-title">Variables de precio</div>
            <div class="card-item"><b>precio:</b> Precio publicado del vehículo.</div>
            <div class="card-item"><b>categoria_precio:</b> Segmento o rango de precio.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Uso y estado del vehículo</div>
            <div class="card-item"><b>kilometraje:</b> Kilómetros recorridos.</div>
            <div class="card-item"><b>uso_anual_estimado:</b> Estimación de uso anual.</div>
            <div class="card-item"><b>rango_kilometraje:</b> Nivel de kilometraje del vehículo.</div>
        </div>
        """, unsafe_allow_html=True)
    
        st.markdown("<br>", unsafe_allow_html=True)
    
        st.markdown("""
        <div class="card">
            <div class="card-title">Contexto de mercado</div>
            <div class="card-item"><b>combustible:</b> Tipo de combustible.</div>
            <div class="card-item"><b>ciudad:</b> Ciudad de publicación.</div>
            <div class="card-item"><b>fecha_captura:</b> Fecha de captura del registro.</div>
        </div>
        """, unsafe_allow_html=True)
# ==========================================
# PESTAÑA 1: NIVEL ESTRATÉGICO
# ==========================================
with tab_est:
    st.title("Tablero Estratégico")
    st.write(
        "Este tablero presenta una visión general del mercado automotriz usado, "
        "enfocada en indicadores estratégicos para apoyar la toma de decisiones."
    )
    # =========================
    # MÉTRICAS PRINCIPALES
    # =========================
    st.header("Métricas principales")
    df_full = cargar_datos()
    total_autos = len(df_full)
    precio_promedio = df_full["precio"].mean()
    kilometraje_promedio = df_full["kilometraje"].mean()
    uso_anual_promedio = df_full["uso_anual_estimado"].mean()
    
    df_est = df["marca"].value_counts().reset_index()
    df_est.columns = ["marca", "cantidad_autos"]
    df_est["participacion"] = (df_est["cantidad_autos"] / total_autos) * 100    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Vehículos totales</div>
            <div class="kpi-value">{f"{total_autos:,}".replace(",", ".")}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Precio promedio</div>
            <div class="kpi-value">${precio_promedio/1_000_000:.1f} MM</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Kilometraje promedio</div>
            <div class="kpi-value">{f"{kilometraje_promedio:,.0f} km".replace(",", ".")}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Marca líder</div>
            <div class="kpi-value">{df_est["marca"].iloc[0]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write(" ")
    st.write(" ")
    st.divider()
    # =========================
    # KPI 1
    # =========================
    st.header("1. Concentración del mercado por marca")
    st.caption("KPI: Participación de marcas | Objetivo: Identificar dominio y presencia de marcas en la muestra | Frecuencia: Semestral")    
    df_est = df_est.sort_values("participacion", ascending=False).copy()
    colors = [
        "#991B1B", "#A61E1E", "#B91C1C", "#C53030", "#D14B43",
        "#DD6B5F", "#E59283", "#EDB8AD", "#F3D6CF", "#F8ECE8"
    ]   
    fig = px.bar(
        df_est,
        x="participacion",
        y="marca",
        orientation="h",
        text="participacion",
        color="marca",
        color_discrete_sequence=colors,
    )
    
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Participación: %{x:.1f}%<extra></extra>"
    )   
    fig.update_layout(
        title=dict(
            text="Participación de marcas",
            x=0,
            xanchor="left",
            font=dict(size=20, color="#111827")
        ),
        xaxis=dict(
            title="Participación (%)",
            showgrid=True,
            gridcolor="rgba(156, 163, 175, 0.18)",
            zeroline=False,
            tickfont=dict(color="#6B7280"),
            title_font=dict(color="#6B7280")
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color="#374151"),
            categoryorder="total ascending"
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        margin=dict(l=20, r=40, t=60, b=20),
        height=500,
        font=dict(family="Inter, sans-serif", color="#111827")
    )
    fig.update_yaxes(automargin=True) 
    st.plotly_chart(fig, use_container_width=True)  
    st.markdown("""
    <div style="
        background: #FAFAF9;
        border: 1px solid #D6E2F0;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 16px;
        color: #002855;
        font-size: 0.96rem;
        line-height: 1.6;
    ">
    <b style="color:#002855;">Interpretación: </b><br>
    <span>La oferta del mercado no se distribuye de manera uniforme entre las marcas, sino por un grupo de marcas con presencia relativamente repartida, aunque con dos líderes claros: Ford y Chevrolet.</span><br>
    </div>
    """, unsafe_allow_html=True)
    st.write(" ")
    st.divider()

    # =========================
    # KPI 2
    # =========================
    st.header("2. Tendencia del precio promedio de vehículos")
    st.caption("KPI: Precio promedio de vehículos en el tiempo | Objetivo: Mostrar la tendencia del valor promedio del mercado para detectar alzas, caídas o estabilidad | Frecuencia: Anual")    
    df_time = (
        df.dropna(subset=["year", "precio"])
          .query("year >= 2000")
          .groupby("year", as_index=False)["precio"]
          .mean()
          .sort_values("year")
    )
    fig = px.line(
        df_time,
        x="year",
        y="precio",
        markers=True,
        title="Precio promedio de vehículos en el tiempo",
    )
    fig.update_traces(line=dict(color="#002855", width=3), marker=dict(size=8))
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Precio promedio",
        hovermode="x unified",
        template="plotly_white"
    )
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <div style="
        background: #FAFAF9;
        border: 1px solid #D6E2F0;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 16px;
        color: #002855;
        font-size: 0.96rem;
        line-height: 1.6;
    ">
    <b style="color:#002855;">Interpretación: </b><br>
    <span>Existe una tendencia claramente ascendente del precio promedio de los vehículos a lo largo del tiempo, con algunas correcciones puntuales, pero con un salto más fuerte en los últimos años.</span><br>
    </div>
    """, unsafe_allow_html=True)
    st.write(" ")
    st.divider()
    # =========================
    # KPI 3
    # =========================
    st.header("3. Pérdida de valor por kilómetro")
    st.caption("KPI: Costo de depreciación por kilómetro recorrido | Objetivo: Medir la pérdida de valor promedio asociada al uso del vehículo | Frecuencia: Trimestral")
    df_km = df.dropna(subset=["kilometraje", "precio"]).copy()
    bins = [0, 50000, 100000, 150000, 200000, 300000, float("inf")]
    labels = ["0-50 mil", "50-100 mil", "100-150 mil", "150-200 mil", "200-300 mil", "+300 mil"]  
    df_km["tramo_km"] = pd.cut(
        df_km["kilometraje"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )
    df_dep_km = (
        df_km.groupby("tramo_km", as_index=False)["precio"]
        .mean()
    )
    fig = px.line(
        df_dep_km,
        x="tramo_km",
        y="precio",
        markers=True,
        title="Costo de depreciación por kilómetro recorrido"
    ) 
    fig.update_traces(
        line=dict(color="#B91C1C", width=3),
        marker=dict(size=8, color="#7F1D1D"),
        hovertemplate="<b>Tramo:</b> %{x}<br><b>Precio promedio:</b> $%{y:,.0f}<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="Tramo de kilometraje",
        yaxis_title="Precio promedio",
        hovermode="x unified",
        template="plotly_white",
        height=440,
        title=dict(x=0, xanchor="left", font=dict(size=20, color="#111827")),
        font=dict(family="Inter, sans-serif", color="#111827"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20)
    )
    fig.update_yaxes(
        tickprefix="$",
        tickformat=",.0f",
        gridcolor="rgba(156, 163, 175, 0.18)"
    )
    fig.update_xaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <div style="
        background: #FAFAF9;
        border: 1px solid #D6E2F0;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 16px;
        color: #002855;
        font-size: 0.96rem;
        line-height: 1.6;
    ">
    <b style="color:#002855;">Interpretación: </b><br>
    <span>A medida que aumenta el kilometraje, el precio promedio del vehículo disminuye de forma sostenida, evidenciando una relación inversa entre uso acumulado y valor de mercado.</span><br>
    </div>
    """, unsafe_allow_html=True)
# ==========================================
# PESTAÑA 2: NIVEL TÁCTICO
# ==========================================
with tab_tac:
    st.title("Tablero Táctico")
    st.write(
        "Este tablero presenta una visión táctica del mercado automotriz usado, "
        "enfocada en apoyar decisiones de gestión, segmentación y posicionamiento comercial."
    )
    st.write(" ")
    st.divider()
    # =========================
    # KPI 1
    # ========================
    st.header("1. Valor de mercado por combustible y nivel de uso")
    st.caption(
        "KPI: Valor promedio de mercado por combustible y nivel de uso | Objetivo: Identificar qué combinaciones de combustible y nivel de uso "
        "presentan mayor y menor valor comercial | Frecuencia: Mensual"
    )
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #002855 0%, #0A3D73 100%);
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 16px;
        color: #FFFFFF;
        font-size: 0.96rem;
        line-height: 1.6;
        box-shadow: 0 6px 16px rgba(0, 40, 85, 0.18);
    ">
    <b>Para este KPI, la variable rango kilometraje fue segmentada en tres niveles de uso: </b><br>
    • <b>Bajo:</b> menos de 50.000 km<br>
    • <b>Medio:</b> entre 50.000 y 119.999 km<br>
    • <b>Alto:</b> 120.000 km o más
    </div>
    """, unsafe_allow_html=True)
    df_tac = df.dropna(subset=["precio", "combustible", "rango_kilometraje"]).copy()
    df_plot = (
        df_tac.groupby(["rango_kilometraje", "combustible"], as_index=False)["precio"]
        .mean()
    )
    paleta_tablero = {
        "superficie": "#FFFFFF",
        "texto": "#1F2937",
        "texto_suave": "#6B7280",
        "grid": "rgba(148, 163, 184, 0.20)",
        "bencina": "#002855",      # Azul eléctrico brillante
        "diesel": "#800020",       # Burgundy / rojo vino clásico
        "hibrido": "#3D3D3D",      # Gris antracita
        "híbrido": "#3D3D3D",
        "electrico": "#0066CC",    # Azul eléctrico profundo
        "eléctrico": "#0066CC"
    }
    fig = px.bar(
        df_plot,
        x="rango_kilometraje",
        y="precio",
        color="combustible",
        barmode="group",
        text="precio",
        category_orders={"rango_kilometraje": ["Bajo", "Medio", "Alto"]},
        color_discrete_map={
        "bencina": paleta_tablero["bencina"],
        "diesel": paleta_tablero["diesel"],
        "hibrido": paleta_tablero["hibrido"],
        "híbrido": paleta_tablero["híbrido"],
        "electrico": paleta_tablero["electrico"],
        "eléctrico": paleta_tablero["eléctrico"]
        },
        title="Valor promedio de mercado por combustible y nivel de uso",
        hover_data={
            "rango_kilometraje": True,
            "combustible": True,
            "precio": ":,.0f"
        }
    )
    
    fig.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )
    
    fig.update_layout(
        template="plotly_white",
        height=500,
        title=dict(
            text="Valor promedio de mercado por combustible y nivel de uso",
            x=0,
            xanchor="left",
            font=dict(size=20, color="#111827")
        ),
        font=dict(family="Inter, sans-serif", color="#111827"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Rango de kilometraje",
        yaxis_title="Precio promedio",
        legend_title="Combustible",
        margin=dict(l=20, r=20, t=70, b=20)
    )
    
    fig.update_yaxes(
        tickprefix="$",
        tickformat=",.0f",
        gridcolor="rgba(156, 163, 175, 0.18)"
    )
    
    fig.update_xaxes(showgrid=False)
    
    st.plotly_chart(fig, use_container_width=True)

    st.write(" ")
    st.divider()
    # =========================
    # KPI 2
    # ========================
    st.header("2. Posicionamiento de precios por marca")
    st.caption(
        "KPI: Banda de precios por marca | Objetivo: comparar el rango de precios y el precio promedio por marca "
        "para identificar posicionamiento, dispersión competitiva y cluster comercial | Frecuencia: Mensual"
    )
    
    df_marca = df.dropna(subset=["marca", "precio"]).copy()
    
    resumen_marca = (
        df_marca.groupby("marca", as_index=False)["precio"]
        .agg(minimo="min", promedio="mean", maximo="max")
        .sort_values("promedio", ascending=True)
    )
    
    resumen_marca = resumen_marca.merge(
        resumen_cluster[["marca", "cluster_nombre", "cantidad"]],
        on="marca",
        how="left"
    )
    
    paleta = {
        "texto": "#1F2937",
        "texto_suave": "#6B7280",
        "grid": "rgba(148, 163, 184, 0.18)",
        "fondo": "#FFFFFF",
        "rango": "#C9C3B8",
        "minimo": "#800020",
        "maximo": "#2F6F68"
    }
    
    paleta_cluster = {
        "Económico": "#C8C2B8",
        "Intermedio": "#D9A441",
        "Costoso": "#002855"
    }
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=resumen_marca["minimo"],
            y=resumen_marca["marca"],
            mode="markers",
            marker=dict(size=1, color="rgba(0,0,0,0)"),
            showlegend=False,
            hoverinfo="skip"
        )
    )
    
    for _, row in resumen_marca.iterrows():
        fig.add_shape(
            type="line",
            x0=row["minimo"],
            x1=row["maximo"],
            y0=row["marca"],
            y1=row["marca"],
            xref="x",
            yref="y",
            line=dict(color=paleta["rango"], width=6)
        )
    
    for cluster in ["Económico", "Intermedio", "Costoso"]:
        df_cluster_plot = resumen_marca[resumen_marca["cluster_nombre"] == cluster]
    
        fig.add_trace(
            go.Scatter(
                x=df_cluster_plot["promedio"],
                y=df_cluster_plot["marca"],
                mode="markers",
                name=cluster,
                marker=dict(
                    size=13,
                    color=paleta_cluster[cluster],
                    line=dict(color="white", width=1.4)
                ),
                customdata=df_cluster_plot[["minimo", "maximo", "cluster_nombre", "cantidad"]],
                hovertemplate=(
                    "<b>Marca:</b> %{y}<br>"
                    "<b>Promedio:</b> $%{x:,.0f}<br>"
                    "<b>Mínimo:</b> $%{customdata[0]:,.0f}<br>"
                    "<b>Máximo:</b> $%{customdata[1]:,.0f}<br>"
                    "<b>Cluster:</b> %{customdata[2]}<br>"
                    "<b>N° publicaciones:</b> %{customdata[3]}<extra></extra>"
                )
            )
        )
    
    fig.add_trace(
        go.Scatter(
            x=resumen_marca["minimo"],
            y=resumen_marca["marca"],
            mode="markers",
            name="Mínimo",
            marker=dict(size=11, color=paleta["minimo"], symbol="diamond")
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=resumen_marca["maximo"],
            y=resumen_marca["marca"],
            mode="markers",
            name="Máximo",
            marker=dict(size=11, color=paleta["maximo"], symbol="diamond")
        )
    )
    
    fig.update_layout(
        template="plotly_white",
        height=560,
        font=dict(family="Inter, sans-serif", color=paleta["texto"]),
        plot_bgcolor=paleta["fondo"],
        paper_bgcolor=paleta["fondo"],
        xaxis_title="Precio",
        yaxis_title="Marca",
        legend_title="Clasificación",
        margin=dict(l=20, r=20, t=70, b=20)
    )
    
    fig.update_xaxes(
        tickprefix="$",
        tickformat=",.0f",
        showgrid=True,
        gridcolor=paleta["grid"],
        tickfont=dict(color=paleta["texto_suave"]),
        title_font=dict(color=paleta["texto_suave"])
    )
    
    fig.update_yaxes(
        showgrid=False,
        tickfont=dict(color=paleta["texto_suave"]),
        title_font=dict(color=paleta["texto_suave"])
    )
    
    st.plotly_chart(fig, use_container_width=True, theme=None)
    
    st.markdown("""
    <div style="
        background: #FAFAF9;
        border: 1px solid #D6E2F0;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 16px;
        color: #002855;
        font-size: 0.96rem;
        line-height: 1.6;
    ">
    <b style="color:#002855;">Interpretación: </b><br>
    <span>La banda horizontal muestra el rango de precios por marca, mientras que el punto central representa el precio promedio. El color del punto identifica el cluster comercial de cada marca, facilitando distinguir entre marcas económicas, intermedias y costosas dentro del mercado.</span><br>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Cluster comercial por marca")

    tabla_cluster = resumen_marca[["marca", "promedio", "cluster_nombre", "cantidad"]].copy()
    tabla_cluster = tabla_cluster.rename(columns={
        "marca": "Marca",
        "promedio": "Precio promedio",
        "cluster_nombre": "Cluster",
        "cantidad": "N° publicaciones"
    })
    tabla_cluster["Precio promedio"] = tabla_cluster["Precio promedio"].round(0).astype(int)
    st.dataframe(tabla_cluster, use_container_width=True, hide_index=True)
    
    st.write(" ")
    st.divider()
    # =========================
    # KPI 3
    # ========================
    st.header("3. Retención de valor por marca")
    st.caption(
        "KPI: Índice de retención de valor por marca | Objetivo: identificar qué marcas conservan mejor su valor relativo "
        "en el mercado | Frecuencia: Mensual"
    )
    
    df_ret = df.dropna(subset=["marca", "precio"]).copy()
    
    resumen_ret = (
        df_ret.groupby("marca", as_index=False)["precio"]
        .median()
        .rename(columns={"precio": "precio_mediano"})
    )
    
    mediana_mercado = resumen_ret["precio_mediano"].median()
    
    resumen_ret["indice_retencion"] = (
        resumen_ret["precio_mediano"] / mediana_mercado * 100
    )
    
    resumen_ret["categoria"] = resumen_ret["indice_retencion"].apply(
        lambda x: "Sobre mercado" if x >= 100 else "Bajo mercado"
    )
    
    resumen_ret = resumen_ret.sort_values("indice_retencion", ascending=True)
    
    orden_marcas = resumen_ret["marca"].tolist()
    
    paleta = {
        "sobre": "#002855",
        "bajo": "#C8C2B8",
        "texto": "#1F2937",
        "texto_suave": "#6B7280",
        "grid": "rgba(148, 163, 184, 0.18)",
        "fondo": "#FFFFFF",
        "linea_base": "#A8A29E"
    }
    
    fig = px.bar(
        resumen_ret,
        x="indice_retencion",
        y="marca",
        orientation="h",
        text="indice_retencion",
        color="categoria",
        category_orders={"marca": orden_marcas},
        color_discrete_map={
            "Sobre mercado": paleta["sobre"],
            "Bajo mercado": paleta["bajo"]
        },
        title="Índice de retención de valor por marca",
        hover_data={
            "marca": True,
            "precio_mediano": ":,.0f",
            "indice_retencion": ":.1f",
            "categoria": True
        }
    )
    
    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        cliponaxis=False
    )
    
    fig.add_vline(
        x=100,
        line_width=1.5,
        line_dash="dash",
        line_color=paleta["linea_base"]
    )
    
    fig.update_layout(
        template="plotly_white",
        height=520,
        title=dict(
            text="Índice de retención de valor por marca (base mercado = 100)",
            x=0,
            xanchor="left",
            font=dict(size=20, color=paleta["texto"])
        ),
        font=dict(
            family="Inter, sans-serif",
            color=paleta["texto"]
        ),
        plot_bgcolor=paleta["fondo"],
        paper_bgcolor=paleta["fondo"],
        xaxis_title="Índice de retención",
        yaxis_title="Marca",
        legend_title="Desempeño",
        margin=dict(l=20, r=40, t=70, b=20)
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridcolor=paleta["grid"],
        tickfont=dict(color=paleta["texto_suave"]),
        title_font=dict(color=paleta["texto_suave"])
    )
    
    fig.update_yaxes(
        showgrid=False,
        tickfont=dict(color=paleta["texto_suave"]),
        title_font=dict(color=paleta["texto_suave"])
    )
    
    st.plotly_chart(fig, use_container_width=True, theme=None)
    st.markdown("""
    <div style="
        background: #FAFAF9;
        border: 1px solid #D6E2F0;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 16px;
        color: #002855;
        font-size: 0.96rem;
        line-height: 1.6;
    ">
    <b style="color:#002855;">Interpretación: </b><br>
    <span>Las marcas con índice superior a 100 conservan un valor relativo por encima de la mediana del mercado, lo que sugiere mayor fortaleza de posicionamiento y mejor capacidad de sostener precios.</span><br>
    </div>
    """, unsafe_allow_html=True)
# ==========================================
# PESTAÑA 3: NIVEL OPERACIONAL
# ==========================================
with tab_op:
    st.title("Tablero Operativo")
    st.write(
        "Este tablero presenta una visión operativa del mercado automotriz usado, "
        "enfocada en el control diario, la detección de alertas y el seguimiento de casos específicos."
    )
    st.write("")
    st.divider()
    # ============================
    # KPI 1
    # ============================    
    st.header("1. Alertas de publicaciones fuera de rango estimado")
    st.caption(
        "KPI: Desviación entre precio real y precio estimado | Objetivo: Detectar vehículos cuyo precio publicado se desvía significativamente "
        "del valor esperado según un modelo de predicción | Frecuencia: diaria."
    )
    columnas_modelo = ["kilometraje", "year", "marca", "combustible", "precio"]
    df_modelo = df[columnas_modelo].dropna().copy()
    
    X = df_modelo[["kilometraje", "year", "marca", "combustible"]]
    X = pd.get_dummies(X, columns=["marca", "combustible"], drop_first=True)
    X = X.astype(float)   
    y = df_modelo["precio"].astype(float).values
    X_b = np.c_[np.ones((len(X), 1)), X.values]
    theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
    y_pred = X_b.dot(theta_best)

    errores = y - y_pred
    errores_abs = np.abs(errores)
    
    mae = np.mean(errores_abs)
    rmse = np.sqrt(np.mean(errores ** 2))

    st.write("Este KPI utiliza modelo de regresión para estimar el precio esperado de cada vehículo a partir de sus características principales: kilometraje, año, marca y tipo de combustible.")
    st.write("Luego compara el precio real publicado con el precio estimado por el modelo. La diferencia entre ambos permite detectar publicaciones potencialmente fuera de rango, ya sea por sobrevaloración o subvaloración.")

    df_alertas = df_modelo.copy()
    df_alertas["Precio real"] = y
    df_alertas["Precio estimado"] = y_pred
    df_alertas["Diferencia"] = df_alertas["Precio real"] - df_alertas["Precio estimado"]
    df_alertas["Diferencia absoluta"] = np.abs(df_alertas["Diferencia"])
    
    umbral_aceptable = mae
    umbral_moderado = 2 * mae
    
    def clasificar_riesgo(diff_abs):
        if diff_abs <= umbral_aceptable:
            return "Aceptable"
        elif diff_abs <= umbral_moderado:
            return "Moderado"
        else:
            return "Crítico"
    
    df_alertas["Nivel de riesgo"] = df_alertas["Diferencia absoluta"].apply(clasificar_riesgo)
    
    df_alertas["Tipo de desvío"] = df_alertas["Diferencia"].apply(
        lambda x: "Sobrevalorado" if x > 0 else "Subvalorado"
    )

    fuera_rango = (df_alertas["Nivel de riesgo"] != "Aceptable").mean() * 100
    df_riesgo = (
        df_alertas["Nivel de riesgo"]
        .value_counts()
        .reindex(["Aceptable", "Moderado", "Crítico"], fill_value=0)
        .reset_index()
    )
    
    df_riesgo.columns = ["Nivel de riesgo", "Cantidad"]
    df_riesgo["Porcentaje"] = (df_riesgo["Cantidad"] / len(df_alertas) * 100).round(1).astype(str) + "%"

    st.header("Métricas del modelo de predicción")   
    total_criticos = (df_alertas["Nivel de riesgo"] == "Crítico").sum()
    total_moderados = (df_alertas["Nivel de riesgo"] == "Moderado").sum()
    porc_fuera_rango = (df_alertas["Nivel de riesgo"] != "Aceptable").mean() * 100
    porc_sobrevalorados = (df_alertas["Diferencia"] > 0).mean() * 100    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">% Fuera de rango</div>
            <div class="kpi-value">{porc_fuera_rango:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Alertas críticas</div>
            <div class="kpi-value">{f"{total_criticos:,}".replace(",", ".")}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Alertas moderadas</div>
            <div class="kpi-value">{f"{total_moderados:,}".replace(",", ".")}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("    ")
    st.write("- MAE(Error Absoluto Promedio): La magnitud promedio de los errores en el conjunto de predicciones, en pesos.")
        
    st.write("   ")     
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #002855 0%, #0A3D73 100%);
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 16px;
        color: #FFFFFF;
        font-size: 0.96rem;
        line-height: 1.6;
        box-shadow: 0 6px 16px rgba(0, 40, 85, 0.18);
    ">
    <b>Criterios de clasificación de alertas:</b><br>
    • <b>Aceptable:</b> diferencia absoluta menor o igual al MAE ($4.956.184)<br>
    • <b>Moderado:</b> diferencia absoluta mayor al MAE y menor o igual a 2 × MAE ($7.188.811)"<br>
    • <b>Crítico:</b> diferencia absoluta superior a 2 × MAE 
    </div>
    """, unsafe_allow_html=True)
    
    
    color_map = {
        "Aceptable": "#2F6F68",
        "Moderado": "#D9A441",
        "Crítico": "#800020"
    }
    
    fig_riesgo = px.bar(
        df_riesgo,
        x="Nivel de riesgo",
        y="Cantidad",
        color="Nivel de riesgo",
        color_discrete_map=color_map,
        text="Porcentaje",
        title="Distribución de vehículos por nivel de alerta"
    )
    
    fig_riesgo.update_traces(textposition="outside")
    fig_riesgo.update_layout(
        template="plotly_white",
        height=430,
        showlegend=False,
        title=dict(x=0, xanchor="left"),
        xaxis_title="Nivel de alerta",
        yaxis_title="Cantidad de vehículos",
        margin=dict(l=20, r=20, t=60, b=20)
    )
    st.plotly_chart(fig_riesgo, use_container_width=True)
    
    opcion = st.selectbox(
        "🔎 Selecciona el nivel de alerta a visualizar:",
        ["Todos", "Aceptable", "Moderado", "Crítico"]
    )
    
    if opcion == "Todos":
        df_filtrado = df_alertas.copy()
    else:
        df_filtrado = df_alertas[df_alertas["Nivel de riesgo"] == opcion].copy()
    
    cantidad = len(df_filtrado)
    promedio = df_filtrado["Diferencia"].mean() if cantidad > 0 else 0
    maximo = df_filtrado["Diferencia absoluta"].max() if cantidad > 0 else 0
    
    st.markdown("### Detalle de publicaciones evaluadas")
    st.markdown(f"""
    <div style="
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 12px;
    ">
        Vehículos mostrados: <b>{cantidad}</b> |
        Diferencia promedio: <b>${promedio:,.0f}</b> |
        Máxima diferencia detectada: <b>${maximo:,.0f}</b>
    </div>
    """, unsafe_allow_html=True)
    
    columnas_mostrar = [
        "marca",
        "year",
        "Precio real",
        "Precio estimado",
        "Diferencia",
        "Tipo de desvío",
        "Nivel de riesgo"
    ]
    
    df_filtrado = df_filtrado[columnas_mostrar].rename(columns={
        "marca": "Marca",
        "year": "Año",
        "combustible": "Combustible",
        "kilometraje": "Kilometraje"
    })
    
    with st.expander("Ver datos"):
        st.dataframe(df_filtrado, use_container_width=True)
        
    st.markdown("""
    <div style="
        background: #FAFAF9;
        border: 1px solid #D6E2F0;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 16px;
        color: #002855;
        font-size: 0.96rem;
        line-height: 1.6;
    ">
    <b style="color:#002855;">Interpretación: </b><br>
    <span>El modelo en su mayoría captura adecuadamente las tendencias generales de depreciación y tasación. Las publicaciones clasificadas como moderadas o críticas presentan una desviación relevante respecto del precio esperado por el modelo. Estas alertas deben revisarse para validar si corresponden a sobrevaloración, subvaloración, error de carga o condiciones especiales del vehículo.</span><br>
    </div>
    """, unsafe_allow_html=True)

    st.write(" ")
    st.divider()
    # ============================
    # KPI 2
    # ============================

    st.header("2. Matriz de alertas por antigüedad y precio")
    st.caption(
        "KPI: Matriz de alertas de sobrevaloración | Objetivo: detectar publicaciones potencialmente "
        "sobrevaloradas, especialmente autos muy antiguos con precio alto | Frecuencia: Diario"
    )
    
        
    df_alerta = df.dropna(subset=["year", "precio", "marca", "modelo"]).copy()
    
    anio_actual = pd.Timestamp.today().year
    df_alerta["antiguedad"] = anio_actual - df_alerta["year"]
    
    # Umbrales operativos
    umbral_antiguedad = 8
    umbral_precio = df_alerta["precio"].quantile(0.75)
    
    # Clasificación por cuadrante
    def clasificar_alerta(row):
        if row["antiguedad"] >= umbral_antiguedad and row["precio"] >= umbral_precio:
            return "Alerta de revisión"
        elif row["antiguedad"] < umbral_antiguedad and row["precio"] >= umbral_precio:
            return "Gama alta"
        elif row["antiguedad"] >= umbral_antiguedad and row["precio"] < umbral_precio:
            return "Observar"
        else:
            return "Normal"
    
    df_alerta["cuadrante"] = df_alerta.apply(clasificar_alerta, axis=1)
    df_alerta["label"] = df_alerta["marca"].str.title() + " " + df_alerta["modelo"].astype(str)
    
    paleta = {
        "Alerta de revisión": "#800020",
        "Gama alta": "#002855",
        "Observar": "#D9A441",
        "Normal": "#D6D3D1"
    }
    
    x_max = max(df_alerta["antiguedad"].max() + 1, umbral_antiguedad + 2)
    y_max = df_alerta["precio"].max() * 1.08
    
    fig = px.scatter(
        df_alerta,
        x="antiguedad",
        y="precio",
        color="cuadrante",
        color_discrete_map=paleta,
        hover_data={
            "marca": True,
            "modelo": True,
            "year": True,
            "antiguedad": True,
            "precio": ":,.0f",
            "ciudad": True,
            "cuadrante": True
        },
        title="Matriz de alertas: autos antiguos con precio alto"
    )
    
    # Fondos por cuadrante
    fig.add_shape(
        type="rect", x0=0, x1=umbral_antiguedad, y0=0, y1=umbral_precio, #normal
        fillcolor="#F5F5F4", line_width=0, layer="below"
    )
    fig.add_shape(
        type="rect", x0=umbral_antiguedad, x1=x_max, y0=0, y1=umbral_precio, #monitorear
        fillcolor="#F7EFE8", line_width=0, layer="below"
    )
    fig.add_shape(
        type="rect", x0=0, x1=umbral_antiguedad, y0=umbral_precio, y1=y_max, #gama alta
        fillcolor="#F4F8FC", line_width=0, layer="below"
    )
    fig.add_shape(
        type="rect", x0=umbral_antiguedad, x1=x_max, y0=umbral_precio, y1=y_max, #revisar
        fillcolor="#F8EAEA", line_width=0, layer="below"
    )
    
    # Líneas de corte
    fig.add_vline(
        x=umbral_antiguedad,
        line_dash="dash",
        line_color="#9CA3AF",
        line_width=1.5
    )
    
    fig.add_hline(
        y=umbral_precio,
        line_dash="dash",
        line_color="#9CA3AF",
        line_width=1.5
    )
    
    # Etiquetas de cuadrantes
    fig.add_annotation(
        x=umbral_antiguedad / 2,
        y=umbral_precio * 0.5,
        text="Normal",
        showarrow=False,
        font=dict(size=12, color="#6B7280")
    )
    
    fig.add_annotation(
        x=(umbral_antiguedad + x_max) / 2,
        y=umbral_precio * 0.5,
        text="Observar",
        showarrow=False,
        font=dict(size=12, color="#6B7280")
    )
    
    fig.add_annotation(
        x=umbral_antiguedad / 2,
        y=(umbral_precio + y_max) / 2,
        text="Gama alta",
        showarrow=False,
        font=dict(size=12, color="#6B7280")
    )
    
    fig.add_annotation(
        x=(umbral_antiguedad + x_max) / 2,
        y=(umbral_precio + y_max) / 2,
        text="Alerta de revisión",
        showarrow=False,
        font=dict(size=12, color="#7F1D1D")
    )
    
    fig.update_traces(
        marker=dict(size=10, opacity=0.8, line=dict(width=0.6, color="white"))
    )
    
    fig.update_layout(
        template="plotly_white",
        height=580,
        title=dict(
            text="Matriz de alertas: autos antiguos con precio alto",
            x=0,
            xanchor="left",
            font=dict(size=20, color="#1F2937")
        ),
        font=dict(family="Inter, sans-serif", color="#1F2937"),
        xaxis_title="Antigüedad del vehículo (años)",
        yaxis_title="Precio",
        legend_title="Clasificación",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=20, r=20, t=70, b=20)
    )
    
    fig.update_xaxes(
        range=[0, x_max],
        gridcolor="rgba(148, 163, 184, 0.18)",
        tickfont=dict(color="#6B7280"),
        title_font=dict(color="#6B7280")
    )
    
    fig.update_yaxes(
        range=[0, y_max],
        tickprefix="$",
        tickformat=",.0f",
        gridcolor="rgba(148, 163, 184, 0.18)",
        tickfont=dict(color="#6B7280"),
        title_font=dict(color="#6B7280")
    )
    
    st.plotly_chart(fig, use_container_width=True, theme=None)
    
    df_revision = (
        df_alerta[df_alerta["cuadrante"] == "Alerta de revisión"][
            ["marca", "modelo", "year", "antiguedad", "precio", "ciudad"]
        ]
        .sort_values(["precio", "antiguedad"], ascending=[False, False])
    )
    
    with st.expander("Ver autos en Alerta de revisión"):
        st.dataframe(df_revision, use_container_width=True)
        
    st.markdown("""
    <div style="
        background: #FAFAF9;
        border: 1px solid #D6E2F0;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 16px;
        color: #002855;
        font-size: 0.96rem;
        line-height: 1.6;
    ">
    <b style="color:#002855;">Interpretación: </b><br>
    <span>La matriz permite identificar rápidamente publicaciones fuera de comportamiento, priorizando la revisión de autos antiguos con precios altos y dejando para monitoreo aquellos casos que solo requieren observación.</span><br>
    </div>
    """, unsafe_allow_html=True)
        