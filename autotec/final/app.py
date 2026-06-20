import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AutoTec | Tablero Táctico",
    page_icon="🚗",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    ruta = "/home/jovyan/work/autotec/final/autos1.csv"
    df = pd.read_csv(ruta)

    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
    df["kilometraje"] = pd.to_numeric(df["kilometraje"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["uso_anual_estimado"] = pd.to_numeric(df["uso_anual_estimado"], errors="coerce")

    df["uso_anual_estimado"] = df["uso_anual_estimado"].fillna(
        df["uso_anual_estimado"].median()
    )

    df = df.dropna(subset=["precio", "kilometraje", "year"])
    return df

df = cargar_datos()

st.markdown(
    """
    <div style="background:linear-gradient(90deg,#003356,#0A6FAE);
    padding:28px;border-radius:18px;margin-bottom:25px;">
        <h1 style="color:white;margin:0;">🚗 AutoTec | Tablero Táctico</h1>
        <p style="color:#DCEEFF;font-size:18px;margin:5px 0 0 0;">
        Valorización de vehículos usados basada en datos de mercado
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("🔎 Filtros")

marca = st.sidebar.multiselect(
    "Marca",
    sorted(df["marca"].dropna().unique())
)

combustible = st.sidebar.multiselect(
    "Combustible",
    sorted(df["combustible"].dropna().unique())
)

rango = st.sidebar.multiselect(
    "Rango kilometraje",
    sorted(df["rango_kilometraje"].dropna().unique())
)

df_f = df.copy()

if marca:
    df_f = df_f[df_f["marca"].isin(marca)]

if combustible:
    df_f = df_f[df_f["combustible"].isin(combustible)]

if rango:
    df_f = df_f[df_f["rango_kilometraje"].isin(rango)]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Vehículos", f"{len(df_f):,}".replace(",", "."))
col2.metric("Precio promedio", f"${df_f['precio'].mean():,.0f}".replace(",", "."))
col3.metric("Km promedio", f"{df_f['kilometraje'].mean():,.0f}".replace(",", "."))
col4.metric("Uso anual mediano", f"{df_f['uso_anual_estimado'].median():,.0f} km/año".replace(",", "."))

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📉 Precio promedio por kilometraje")

    kpi1 = (
        df_f.groupby("rango_kilometraje")["precio"]
        .mean()
        .reset_index()
    )

    fig1 = px.bar(
        kpi1,
        x="rango_kilometraje",
        y="precio",
        color="rango_kilometraje",
        color_discrete_sequence=["#7EC8E3", "#0A6FAE", "#003356"],
        text_auto=".2s"
    )

    fig1.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        xaxis_title="Rango de kilometraje",
        yaxis_title="Precio promedio ($)"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("🏷️ Top marcas por precio promedio")

    kpi2 = (
        df_f.groupby("marca")["precio"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        kpi2,
        x="precio",
        y="marca",
        orientation="h",
        color="precio",
        color_continuous_scale="Blues",
        text_auto=".2s"
    )

    fig2.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(autorange="reversed"),
        xaxis_title="Precio promedio ($)",
        yaxis_title="Marca"
    )

    st.plotly_chart(fig2, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("⛽ Precio por combustible y kilometraje")

    kpi3 = (
        df_f.groupby(["combustible", "rango_kilometraje"])["precio"]
        .mean()
        .reset_index()
    )

    fig3 = px.bar(
        kpi3,
        x="rango_kilometraje",
        y="precio",
        color="combustible",
        barmode="group",
        color_discrete_sequence=["#003356", "#0A6FAE", "#7EC8E3"],
        text_auto=".2s"
    )

    fig3.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Rango de kilometraje",
        yaxis_title="Precio promedio ($)"
    )

    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.subheader("📊 Uso anual estimado")

    kpi4 = (
        df_f.groupby("rango_kilometraje")["uso_anual_estimado"]
        .mean()
        .reset_index()
    )

    fig4 = px.bar(
        kpi4,
        x="rango_kilometraje",
        y="uso_anual_estimado",
        color="rango_kilometraje",
        color_discrete_sequence=["#7EC8E3", "#0A6FAE", "#003356"],
        text_auto=".2s"
    )

    fig4.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        xaxis_title="Rango de kilometraje",
        yaxis_title="Km/año"
    )

    st.plotly_chart(fig4, use_container_width=True)

st.divider()

st.subheader("📌 Tabla formal de KPI tácticos")

tabla_kpi = pd.DataFrame({
    "Nivel": ["Táctico", "Táctico", "Táctico", "Táctico"],
    "Objetivo": [
        "Evaluar cómo cambia el valor de mercado según el nivel de uso",
        "Analizar el impacto de la marca en la valorización",
        "Evaluar diferencias según combustible y nivel de uso",
        "Validar coherencia entre antigüedad y uso acumulado"
    ],
    "Frecuencia": ["Mensual", "Mensual", "Trimestral", "Trimestral"],
    "Datos": [
        "precio, kilometraje, rango_kilometraje",
        "precio, marca",
        "precio, combustible, kilometraje",
        "year, uso_anual_estimado"
    ],
    "KPI": [
        "Variación porcentual del precio promedio entre rangos de kilometraje",
        "Precio promedio por marca",
        "Variación del valor de mercado según combustible y nivel de uso",
        "Uso anual promedio como indicador de coherencia del valor comercial"
    ]
})

st.dataframe(tabla_kpi, use_container_width=True)

st.success("Dashboard táctico enfocado en estimación del valor de mercado de vehículos usados.")