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
header[data-testid="stHeader"] {
    display: none;
}
.stDeployButton {
    display: none;
}
[data-testid="stToolbar"] {
    display: none;
}
[data-testid="stDecoration"] {
    display: none;
}
#MainMenu {
    visibility: hidden;
}
footer {
    visibility: hidden;
}
/* Quita el espacio extra arriba */
.block-container {
    padding-top: 1.2rem !important;
}
</style>
""", unsafe_allow_html=True)
#Imagen
BASE_DIR = Path(__file__).resolve().parent
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64(BASE_DIR / "auto.jpeg")
st.markdown(f"""
<div class="hero-box">
    <div class="hero-text">
        <h1>Cuadro de Mando Integral</h1>
        <p class="sub">Analítica Automotriz Ejecutiva</p>
        <p class="mini">Nivel Estratégico, Táctico y Operativo</p>
    </div>
    <img class="car-corner" src="data:image/jpg;base64,{img}">
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

# SIDE BAR
st.sidebar.write("Filtros globales")

marcas = sorted(df["marca"].dropna().unique()) if "marca" in df.columns else []

top_10_marcas = (
    df["marca"]
    .dropna()
    .value_counts()
    .head(10)
    .index
    .tolist()
) if "marca" in df.columns else []

marcas_sel = st.sidebar.multiselect(
    "Selecciona marcas:",
    options=marcas,
    default=top_10_marcas
)
df = df[df["marca"].isin(marcas_sel)] if "marca" in df.columns else df

if df.empty:
    st.warning("No hay datos disponibles con los filtros seleccionados.")
    st.stop()

# 4. Tabs por nivel organizacional
tab_inicio, tab_est, tab_tac, tab_op = st.tabs([
    "Inicio",
    "Nivel Estratégico (CEO)",
    "Nivel Táctico (Gerencia)",
    "Nivel Operacional (Supervisor)"
])
with tab_inicio: 
    import streamlit as st
    st.title("AutoTec")
    st.header("Propuesta de Valor")
    st.subheader("Predecir el precio justo de un auto usado según sus características y el mercado.")
    
    st.markdown(
        """
        AutoTec analiza información como marca, modelo, año, kilometraje, combustible y 
        comportamiento del mercado para estimar un valor referencial que apoye decisiones 
        de compra, venta y tasación.
        """
    )
    
    st.markdown("### ¿Qué puedes hacer en la plataforma?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(
            "**Predicción de precios**\n\n"
            "Estima el valor de un auto usado a partir de sus atributos principales."
        )
    
    with col2:
        st.info(
            "**Análisis de mercado**\n\n"
            "Explora patrones de precios, dispersión, retención de valor y segmentación."
        )
    
    with col3:
        st.info(
            "**Apoyo a decisiones**\n\n"
            "Detecta alertas, oportunidades y comportamientos relevantes para el negocio."
        )
    
    st.markdown("### Propuesta de valor")
    
    st.success(
        "Entregar una estimación objetiva del precio de un auto usado, alineada con las "
        "condiciones del mercado, para mejorar la toma de decisiones de compra, venta y análisis."
    )
# ==========================================
# PESTAÑA 1: NIVEL ESTRATÉGICO
# ==========================================
with tab_est:
    st.header("Nivel Estratégico")
    st.write(
        "Este tablero presenta una visión general del mercado automotriz usado, "
        "enfocada en indicadores estratégicos para apoyar la toma de decisiones."
    )
    # =========================
    # MÉTRICAS PRINCIPALES
    # =========================
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
            <div class="kpi-label">Vehículos analizados</div>
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
    
    st.write(" ")
    st.write(" ")
    
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
    fig.update_traces(line=dict(color="#B91C1C", width=3), marker=dict(size=8))
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Precio promedio",
        hovermode="x unified",
        template="plotly_white"
    )
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)
    
    st.write(" ")
    st.write(" ")

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
    
# ==========================================
# PESTAÑA 2: NIVEL TÁCTICO
# ==========================================
with tab_tac:
    # =========================
    # KPI 1
    # ========================
    st.header("Valor de mercado por combustible y nivel de uso")
    st.caption(
        "KPI: Valor promedio de mercado por combustible y nivel de uso | Objetivo: Identificar qué combinaciones de combustible y nivel de uso "
        "presentan mayor y menor valor comercial | Frecuencia: Mensual"
    )
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
        "bencina": "#2F6F68",      # Azul eléctrico brillante
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
    st.write(" ")
    # =========================
    # KPI 2
    # ========================
    st.header("Posicionamiento de precios por marca")
    st.caption(
        "KPI: Banda de precios por marca | Objetivo: comparar el rango de precios y el precio promedio por marca "
        "para identificar posicionamiento y dispersión competitiva | Frecuencia: Mensual"
    )  
    df_marca = df.dropna(subset=["marca", "precio"]).copy()
    resumen_marca = (
        df_marca.groupby("marca", as_index=False)["precio"]
        .agg(minimo="min", promedio="mean", maximo="max")
        .sort_values("promedio", ascending=True)
    )
    
    paleta = {
        "texto": "#1F2937",
        "texto_suave": "#6B7280",
        "grid": "rgba(148, 163, 184, 0.18)",
        "fondo": "#FFFFFF",
        "rango": "#C9C3B8",      # Arena fría
        "promedio": "#5E4B8B",   # Índigo oscuro
        "minimo": "#800020",     # Verde oceánico
        "maximo": "#2F6F68"      # Óxido moderno
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
    
    fig.add_trace(
        go.Scatter(
            x=resumen_marca["promedio"],
            y=resumen_marca["marca"],
            mode="markers",
            name="Promedio",
            marker=dict(
                size=12,
                color=paleta["promedio"],
                line=dict(color="white", width=1.5)
            ),
            customdata=resumen_marca[["minimo", "maximo"]],
            hovertemplate=(
                "<b>Marca:</b> %{y}<br>"
                "<b>Promedio:</b> $%{x:,.0f}<br>"
                "<b>Mínimo:</b> $%{customdata[0]:,.0f}<br>"
                "<b>Máximo:</b> $%{customdata[1]:,.0f}<extra></extra>"
            )
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=resumen_marca["minimo"],
            y=resumen_marca["marca"],
            mode="markers",
            name="Mínimo",
            marker=dict(size=9, color=paleta["minimo"], symbol="diamond")
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=resumen_marca["maximo"],
            y=resumen_marca["marca"],
            mode="markers",
            name="Máximo",
            marker=dict(size=9, color=paleta["maximo"], symbol="diamond")
        )
    )
   
    fig.update_layout(
        template="plotly_white",
        height=550,
        title="Banda de precios por marca",
        font=dict(family="Inter, sans-serif", color=paleta["texto"]),
        plot_bgcolor=paleta["fondo"],
        paper_bgcolor=paleta["fondo"],
        xaxis_title="Precio",
        yaxis_title="Marca",
        legend_title="Referencia",
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
    
    st.info(
        "Interpretación táctica: una banda de precios más amplia indica mayor dispersión "
        "comercial dentro de la marca, mientras que un promedio alto con menor dispersión "
        "sugiere un posicionamiento más consistente en el mercado."
    )
    st.info(
        "ESTO NO VA A IR Decision: Mantener o reforzar el posicionamiento premium en marcas con promedio alto y rango controlado"
        "Revisar el pricing en marcas con banda muy amplia para reducir dispersión y evitar subvaloración o sobreprecio en ciertos modelos"
        "Ajustar el mix de inventario favoreciendo marcas con mejor relación entre valor promedio y consistencia de precio"
    )   
    
    st.write(" ")
    st.write(" ")
    # =========================
    # KPI 3
    # ========================
    st.header("Retención de valor por marca")
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
        "sobre": "#2F6F68",
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
        legend_title="Desempeño relativo",
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
    
    st.info(
        "Interpretación táctica: las marcas con índice superior a 100 conservan un valor "
        "relativo por encima de la mediana del mercado, lo que sugiere mayor fortaleza de "
        "posicionamiento y mejor capacidad de sostener precios."
    )
# ==========================================
# PESTAÑA 3: NIVEL OPERACIONAL
# ==========================================
with tab_op:
    # ============================
    # KPI 1
    # ============================
    st.header("Alertas de Precios Fuera de Rango")
    st.caption(
        "agregar"
    ) 
    # --- BLOQUE DE REGRESIÓN (para generar y_pred y mae) ---
    X = df[['kilometraje','year','marca','combustible']]
    X = pd.get_dummies(X, columns=['marca','combustible'], drop_first=True)
    X = X.astype(float)
    y = df['precio'].astype(float)
    X_b = np.c_[np.ones((len(X),1)), X.values]
    theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
    y_pred = X_b.dot(theta_best)
    mae = np.mean(np.abs(y - y_pred))
    rmse = np.sqrt(np.mean((y - y_pred)**2))

    # 🔎 Bloque de métricas del modelo
    st.markdown("### Métricas del Modelo de Predicción")
    colm1, colm2 = st.columns(2)
    with colm1:
        st.metric("Error MAE", f"${mae:,.0f}")
    with colm2:
        st.metric("Error RMSE", f"${rmse:,.0f}")

    st.info(f"""
    📊 El modelo de regresión lineal se construyó con variables:
    - Kilometraje
    - Año
    - Marca
    - Combustible

    Los umbrales de alerta se definieron como:
    - **Aceptable**: diferencia ≤ MAE (${mae:,.0f})
    - **Moderado**: diferencia ≤ 2 × MAE (${2*mae:,.0f})
    - **Crítico**: diferencia > 2 × MAE
    """)

    # BLOQUE DE REGRESIÓN (para generar y_pred y mae)
    X = df[['kilometraje','year','marca','combustible']]
    X = pd.get_dummies(X, columns=['marca','combustible'], drop_first=True)
    X = X.astype(float)
    y = df['precio'].astype(float)
    X_b = np.c_[np.ones((len(X),1)), X.values]
    theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
    y_pred = X_b.dot(theta_best)
    mae = np.mean(np.abs(y - y_pred))

    df_alertas = pd.DataFrame({
        "Real": y,
        "Predicho": y_pred,
        "Diferencia": y - y_pred
    })

    # Umbrales dinámicos (como tu antiguo app.py)
    umbral_leve = mae
    umbral_moderado = 2 * mae

    def clasificar_riesgo(diff):
        if abs(diff) <= umbral_leve:
            return "Aceptable"
        elif abs(diff) <= umbral_moderado:
            return "Moderado"
        else:
            return "Crítico"

    df_alertas["Riesgo"] = df_alertas["Diferencia"].apply(clasificar_riesgo)

    fuera_rango = (df_alertas["Riesgo"] != "Aceptable").mean() * 100
    st.metric("% Autos Fuera de Rango", f"{fuera_rango:.1f}%")

    df_riesgo = df_alertas["Riesgo"].value_counts().reset_index()
    df_riesgo.columns = ["Nivel de Riesgo", "Cantidad"]
    df_riesgo["Porcentaje"] = (df_riesgo["Cantidad"] / df_alertas.shape[0] * 100).round(1)

    color_map = {"Aceptable":"green","Moderado":"orange","Crítico":"red"}
    fig_riesgo = px.bar(df_riesgo,
                        x="Nivel de Riesgo", y="Cantidad",
                        title="Distribución de Autos por Nivel de Riesgo",
                        color="Nivel de Riesgo",
                        color_discrete_map=color_map,
                        text="Porcentaje")
    fig_riesgo.update_traces(textposition="outside")
    st.plotly_chart(fig_riesgo, use_container_width=True)

    opcion = st.selectbox("🔎 Selecciona el rango de autos a visualizar:",
                          ["Ninguna", "Aceptable", "Moderado", "Crítico"])

    if opcion != "Ninguna":
        df_rango = df_alertas[df_alertas["Riesgo"]==opcion].copy()

        if "marca" in df.columns: 
            df_rango["Marca"] = df.loc[df_rango.index, "marca"]
        if "year" in df.columns: 
            df_rango["Año"] = df.loc[df_rango.index, "year"]
        if "combustible" in df.columns: 
            df_rango["Combustible"] = df.loc[df_rango.index, "combustible"]

        cantidad = len(df_rango)
        promedio = df_rango["Diferencia"].mean()
        maximo = df_rango["Diferencia"].abs().max()

        df_rango = df_rango.sort_index().reset_index(drop=True)
        df_rango.index = df_rango.index + 1
        df_rango.rename_axis("ID_BD", inplace=True)

        columnas_utiles = ["Real","Predicho","Diferencia","Riesgo","Marca","Año","Combustible"]
        df_rango = df_rango[columnas_utiles]

        st.write(f"📊 Autos {opcion} ({cantidad}) | Diferencia promedio: ${promedio:,.0f} | Máxima diferencia: ${maximo:,.0f}")
        st.dataframe(df_rango, use_container_width=True)

    st.warning("⚠️ Supervisores deben revisar autos fuera de rango para evitar sobrevaloración/subvaloración.")
    st.markdown("---")
    
      # ============================
    # KPI 2
    # ============================

    st.header("Alertas de sobrevaloración")
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
            return "Revisar"
        elif row["antiguedad"] < umbral_antiguedad and row["precio"] >= umbral_precio:
            return "Premium"
        elif row["antiguedad"] >= umbral_antiguedad and row["precio"] < umbral_precio:
            return "Monitorear"
        else:
            return "Normal"
    
    df_alerta["cuadrante"] = df_alerta.apply(clasificar_alerta, axis=1)
    df_alerta["label"] = df_alerta["marca"].str.title() + " " + df_alerta["modelo"].astype(str)
    
    paleta = {
        "Revisar": "#A06A6A",
        "Premium": "#B08968",
        "Monitorear": "#A3B18A",
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
        type="rect", x0=0, x1=umbral_antiguedad, y0=0, y1=umbral_precio,
        fillcolor="#F5F5F4", line_width=0, layer="below"
    )
    fig.add_shape(
        type="rect", x0=umbral_antiguedad, x1=x_max, y0=0, y1=umbral_precio,
        fillcolor="#EEF4EA", line_width=0, layer="below"
    )
    fig.add_shape(
        type="rect", x0=0, x1=umbral_antiguedad, y0=umbral_precio, y1=y_max,
        fillcolor="#F7EFE8", line_width=0, layer="below"
    )
    fig.add_shape(
        type="rect", x0=umbral_antiguedad, x1=x_max, y0=umbral_precio, y1=y_max,
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
        text="Monitorear",
        showarrow=False,
        font=dict(size=12, color="#6B7280")
    )
    
    fig.add_annotation(
        x=umbral_antiguedad / 2,
        y=(umbral_precio + y_max) / 2,
        text="Premium",
        showarrow=False,
        font=dict(size=12, color="#6B7280")
    )
    
    fig.add_annotation(
        x=(umbral_antiguedad + x_max) / 2,
        y=(umbral_precio + y_max) / 2,
        text="Revisar",
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
        legend_title="Estado",
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
        df_alerta[df_alerta["cuadrante"] == "Revisar"][
            ["marca", "modelo", "year", "antiguedad", "precio", "ciudad"]
        ]
        .sort_values(["precio", "antiguedad"], ascending=[False, False])
    )
    
    with st.expander("Ver publicaciones en revisión"):
        st.dataframe(df_revision, use_container_width=True)
    
    st.info(
        "Interpretación operativa: el cuadrante 'Revisar' concentra vehículos antiguos "
        "con precio alto, que deben validarse como posibles casos de sobrevaloración, "
        "error de carga o premium justificado por versión, estado o equipamiento."
    )
        


with tab_op:


    # ============================
    # KPI 1: Depreciación por Segmento
    # ============================
    st.subheader("Depreciación por Segmento de Mercado")
    q1, q2 = df["precio"].quantile(0.33), df["precio"].quantile(0.66)
    df["segmento_precio"] = pd.cut(df["precio"], bins=[0, q1, q2, df["precio"].max()],
                                   labels=["Bajo", "Medio", "Alto"])
    segmento = st.selectbox("Segmento de Precio", ["Todos", "Bajo", "Medio", "Alto"])
    marca = st.selectbox("Marca", ["Todas"] + sorted(df["marca"].dropna().unique()))
    df_filtrado = df.copy()
    if segmento != "Todos": df_filtrado = df_filtrado[df_filtrado["segmento_precio"] == segmento]
    if marca != "Todas": df_filtrado = df_filtrado[df_filtrado["marca"] == marca]
    criticos = df_filtrado[(df_filtrado["kilometraje"] > 150000) & (df_filtrado["precio"] < 3000000)]
    porcentaje_criticos = len(criticos) / len(df_filtrado) * 100 if len(df_filtrado) > 0 else 0
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Vehículos", f"{len(df_filtrado):,}")
    with c2: st.metric("Precio Promedio", f"${df_filtrado['precio'].mean():,.0f}")
    with c3: st.metric("KM Promedio", f"{df_filtrado['kilometraje'].mean():,.0f}")
    with c4: st.metric("% Zona Crítica", f"{porcentaje_criticos:.1f}%")
    fig = px.scatter(df_filtrado, x="kilometraje", y="precio", color="segmento_precio",
                     hover_data=["marca","modelo","year"], opacity=0.65,
                     title="Relación entre Kilometraje y Precio")
    st.plotly_chart(fig, use_container_width=True)
    top_marcas = df_filtrado.groupby("marca").size().reset_index(name="Cantidad").sort_values("Cantidad", ascending=False).head(10)
    fig_marcas = px.bar(top_marcas, x="marca", y="Cantidad", text="Cantidad", title="Top 10 Marcas")
    st.plotly_chart(fig_marcas, use_container_width=True)
    st.success(f"✅ Solo el {porcentaje_criticos:.1f}% de los vehículos se encuentra en zona crítica." if porcentaje_criticos <= 20 else f"⚠️ El {porcentaje_criticos:.1f}% presenta depreciación elevada.")
    st.markdown("---")

    # ============================
    # KPI 2: Impacto del Kilometraje
    # ============================
    st.subheader("Impacto del Kilometraje en el Precio")
    bins = [0, 50000, 100000, 150000, 200000, 300000]
    labels = ["0-50 mil","50-100 mil","100-150 mil","150-200 mil","+200 mil"]
    df["rango_km"] = pd.cut(df["kilometraje"], bins=bins, labels=labels)
    precio_km = df.groupby("rango_km")["precio"].mean().reset_index()
    fig2 = px.line(precio_km, x="rango_km", y="precio", markers=True, text="precio",
                   title="Precio Promedio según Rango de Kilometraje")
    fig2.update_traces(texttemplate="$%{text:,.0f}", textposition="top center")
    st.plotly_chart(fig2, use_container_width=True)
    precio_km["caida"] = precio_km["precio"].pct_change() * 100
    mayor_caida = precio_km.loc[precio_km["caida"].idxmin()]
    depreciacion_total = (precio_km["precio"].max() - precio_km["precio"].min()) / precio_km["precio"].max() * 100
    col1, col2 = st.columns(2)
    with col1: st.metric("Depreciación Total Observada", f"{depreciacion_total:.1f}%")
    with col2: st.metric("Mayor Caída de Valor", f"{abs(mayor_caida['caida']):.1f}%")
    st.info(f" **Hallazgo Principal**\n\nLa mayor pérdida ocurre en el tramo **{mayor_caida['rango_km']}**, con una caída de **{abs(mayor_caida['caida']):.1f}%**.")
    st.markdown("---")

    # ============================
    # KPI 3: Precio por Año
    # ============================
    st.subheader("Precio Promedio por Año de Fabricación")
    precios_por_año = df.groupby("year")["precio"].mean().reset_index().sort_values("year")
    fig3 = px.line(precios_por_año, x="year", y="precio", markers=True, title="Precio Promedio por Año de Fabricación")
    st.plotly_chart(fig3, use_container_width=True)
    recientes, antiguos = df[df["year"] >= 2018]["precio"].mean(), df[df["year"] <= 2010]["precio"].mean()
    ratio = recientes / antiguos
    st.metric("Relación Recientes vs Antiguos", f"{ratio:.2f}x")
    st.success("✅ Los vehículos recientes mantienen mejor su valor." if ratio > 2 else "⚠️ La diferencia entre recientes y antiguos es menor a lo esperado.")
    st.markdown("---")


