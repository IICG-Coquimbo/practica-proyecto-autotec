import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial
st.set_page_config(page_title="Dashboard AutoTec", layout="wide")
st.title("🚗 Cuadro de Mando Integral - AutoTec")
st.markdown("### Analítica de depreciación y tasación de vehículos usados")
st.markdown("---")

# Carga de datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("datos_autotec_dashboard.csv")

df = cargar_datos()

# Pestañas
tab_est, tab_tac, tab_op = st.tabs([
    "📊 Nivel Estratégico",
    "📈 Nivel Táctico",
    "⚙️ Nivel Operacional"
])

# ==============================
# NIVEL 1: ESTRATÉGICO
# ==============================
with tab_est:
    st.header("Participación del Mercado por Marca")
    total_autos = len(df)
    df_est = df["marca"].value_counts().reset_index()
    df_est.columns = ["marca", "Cantidad_Vehiculos"]
    df_est["Participacion"] = (df_est["Cantidad_Vehiculos"] / total_autos) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total vehículos", total_autos)
    col2.metric("Marca líder", df_est["marca"].iloc[0])
    col3.metric("Participación líder", f"{df_est['Participacion'].iloc[0]:.1f}%")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=df_est.head(10),
        x="Participacion",
        y="marca",
        palette="Blues_r",
        ax=ax
    )
    ax.set_xlabel("Participación (%)")
    ax.set_ylabel("Marca")
    ax.set_title("Top 10 marcas con mayor presencia")
    sns.despine()
    st.pyplot(fig)

# ==============================
# NIVEL 2: TÁCTICO
# ==============================
with tab_tac:
    st.header("Competitividad y Volatilidad de Precios")
    marcas = st.multiselect(
        "Filtrar marcas:",
        options=sorted(df["marca"].dropna().unique()),
        default=sorted(df["marca"].dropna().unique())[:8]
    )

    df_filtrado = df[df["marca"].isin(marcas)]
    df_tac = (
        df_filtrado.groupby("marca")["precio_num"]
        .agg(["min", "mean", "max"])
        .reset_index()
        .sort_values(by="mean", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.vlines(x=df_tac["marca"], ymin=df_tac["min"], ymax=df_tac["max"], colors="#B0BEC5", alpha=0.7, linewidth=3)
    ax.scatter(df_tac["marca"], df_tac["mean"], color="#1A237E", s=120, label="Promedio")
    ax.scatter(df_tac["marca"], df_tac["min"], color="#2E7D32", marker="^", s=80, label="Mínimo")
    ax.scatter(df_tac["marca"], df_tac["max"], color="#C62828", marker="v", s=80, label="Máximo")
    ax.set_ylabel("Precio ($)")
    ax.set_xlabel("Marca")
    ax.set_title("Bandas de precio por marca")
    plt.xticks(rotation=35, ha="right")
    ax.legend()
    sns.despine()
    st.pyplot(fig)

# ==============================
# NIVEL 3: OPERACIONAL
# ==============================
with tab_op:
    st.header("Alertas de Depreciación y Tasación")
    col1, col2 = st.columns(2)
    with col1:
        umbral_km = st.slider("Kilometraje crítico:", min_value=50000, max_value=250000, value=120000, step=10000)
    with col2:
        umbral_anio = st.slider("Año crítico:", min_value=2005, max_value=2024, value=2014, step=1)

    zona_riesgo = df[(df["kilometraje_num"] >= umbral_km) | (df["year"] <= umbral_anio)]
    st.warning(f"⚠️ Se detectaron {len(zona_riesgo)} vehículos con posible alta depreciación.")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(df["kilometraje_num"], df["precio_num"], alpha=0.35, s=60, color="#78909C", label="Vehículos generales")
    ax.scatter(zona_riesgo["kilometraje_num"], zona_riesgo["precio_num"], color="#D32F2F", s=90, edgecolor="black", label="Zona de riesgo")
    ax.axvline(x=umbral_km, color="#C62828", linestyle="--")
    ax.set_xlabel("Kilometraje")
    ax.set_ylabel("Precio")
    ax.set_title("Matriz de riesgo por kilometraje y precio")
    ax.legend()
    sns.despine()
    st.pyplot(fig)

    st.subheader("📋 Vehículos con alerta")
    columnas = ["marca", "modelo", "year", "kilometraje_num", "precio_num", "combustible", "ciudad"]
    st.dataframe(zona_riesgo[columnas], hide_index=True)
