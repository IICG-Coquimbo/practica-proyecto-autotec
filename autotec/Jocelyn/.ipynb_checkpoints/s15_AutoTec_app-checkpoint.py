import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dashboard AutoTec",
    layout="wide"
)

st.title("Dashboard Ejecutivo AutoTec")
st.markdown("Análisis interactivo del mercado de vehículos usados")
st.markdown("---")

@st.cache_data
def cargar_datos():
    return pd.read_csv("datos_autotec_dashboard.csv")

df = cargar_datos()

df = df.dropna(subset=["marca", "precio_num", "km_num", "year_limpio"])

tab_est, tab_tac, tab_op = st.tabs([
    "Nivel Estratégico",
    "Nivel Táctico",
    "Nivel Operacional"
])

with tab_est:
    st.header("Concentración del mercado por marca")
    st.caption("Frecuencia: mensual | Objetivo: identificar marcas dominantes en el mercado")

    total_autos = len(df)

    df_est = df["marca"].value_counts().reset_index()
    df_est.columns = ["marca", "cantidad_autos"]
    df_est["participacion"] = (df_est["cantidad_autos"] / total_autos) * 100

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric("Total de vehículos", total_autos)
        st.metric("Marca líder", df_est["marca"].iloc[0])
        st.metric("Participación marca líder", f"{df_est['participacion'].iloc[0]:.2f}%")
        st.dataframe(df_est.head(15), hide_index=True)

    with col2:
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.barh(df_est["marca"].head(10), df_est["participacion"].head(10))
        ax.set_xlabel("Participación (%)")
        ax.set_ylabel("Marca")
        ax.set_title("Top 10 marcas por participación")
        ax.invert_yaxis()
        st.pyplot(fig)

with tab_tac:
    st.header("Análisis táctico de precios por marca")
    st.caption("Frecuencia: semanal | Objetivo: comparar precios y apoyar decisiones comerciales")

    marcas_disponibles = sorted(df["marca"].dropna().unique())

    marcas = st.multiselect(
        "Selecciona marcas para comparar",
        options=marcas_disponibles,
        default=marcas_disponibles[:5]
    )

    df_filtrado = df[df["marca"].isin(marcas)]

    df_tac = df_filtrado.groupby("marca")["precio_num"].agg(
        ["min", "mean", "max", "count"]
    ).reset_index()

    df_tac = df_tac.sort_values("mean", ascending=False)

    st.dataframe(df_tac, hide_index=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df_tac["marca"], df_tac["mean"])
    ax.set_title("Precio promedio por marca")
    ax.set_xlabel("Marca")
    ax.set_ylabel("Precio promedio")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab_op:
    st.header("Alertas operacionales por kilometraje")
    st.caption("Frecuencia: diaria | Objetivo: detectar vehículos con alto nivel de uso")

    max_km = int(df["km_num"].max())

    umbral_km = st.slider(
        "Selecciona kilometraje crítico",
        min_value=0,
        max_value=max_km,
        value=150000,
        step=10000
    )

    zona_alerta = df[df["km_num"] >= umbral_km]

    st.warning(f"Vehículos sobre el umbral seleccionado: {len(zona_alerta)}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(df["km_num"], df["precio_num"], alpha=0.4)
    ax.axvline(x=umbral_km, linestyle="--")
    ax.set_title("Relación entre kilometraje y precio")
    ax.set_xlabel("Kilometraje")
    ax.set_ylabel("Precio")
    st.pyplot(fig)

    st.subheader("Vehículos en zona de alerta")

    columnas_mostrar = [
        "marca",
        "modelo",
        "year_limpio",
        "km_num",
        "precio_num",
        "combustible",
        "ciudad"
    ]

    columnas_existentes = [c for c in columnas_mostrar if c in zona_alerta.columns]

    st.dataframe(
        zona_alerta[columnas_existentes].sort_values("km_num", ascending=False).head(50),
        hide_index=True
    )