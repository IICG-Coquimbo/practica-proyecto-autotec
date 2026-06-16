# s15_AutoTec_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------
# Configuración de la página
# -----------------------------------
st.set_page_config(
    page_title="Dashboard AutoTec",
    layout="wide"
)

st.title("Dashboard Ejecutivo AutoTec")
st.markdown("Análisis interactivo del mercado de vehículos usados")
st.markdown("---")

# -----------------------------------
# Carga de datos desde CSV
# -----------------------------------
@st.cache_data
def cargar_datos():
    return pd.read_csv("datos_autotec_dashboard.csv")

df = cargar_datos()

# Limpiar columnas obligatorias
df = df.dropna(subset=["marca", "precio_num", "km_num", "year_limpio"])

# -----------------------------------
# Crear pestañas por nivel organizacional
# -----------------------------------
tab_est, tab_tac, tab_op = st.tabs([
    "Nivel Estratégico",
    "Nivel Táctico",
    "Nivel Operacional"
])

# -----------------------------------
# Pestaña Nivel Estratégico
# -----------------------------------
with tab_est:
    st.header("Nivel Estratégico: Análisis general del mercado")
    st.caption("Frecuencia: mensual | Objetivo: apoyar decisiones gerenciales sobre marcas, precios y composición del mercado")

    total_autos = len(df)

    # ===============================
    # KPI generales
    # ===============================
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

    with col_kpi1:
        st.metric("Total de vehículos analizados", total_autos)

    with col_kpi2:
        marca_lider = df["marca"].value_counts().idxmax()
        st.metric("Marca con mayor presencia", marca_lider)

    with col_kpi3:
        precio_promedio = df["precio_num"].mean()
        st.metric("Precio promedio general", f"${precio_promedio:,.0f}")

    st.markdown("---")

    # ===============================
    # Análisis 1: Participación por marca
    # ===============================
    st.subheader("1. Participación de mercado por marca")
    st.write(
        "Este análisis permite identificar qué marcas tienen mayor presencia dentro de la base de vehículos usados."
    )

    df_marcas = df["marca"].value_counts().reset_index()
    df_marcas.columns = ["marca", "cantidad_autos"]
    df_marcas["participacion"] = (df_marcas["cantidad_autos"] / total_autos) * 100

    col1, col2 = st.columns([1, 2])

    with col1:
        st.dataframe(df_marcas.head(10), hide_index=True)

    with col2:
        fig1, ax1 = plt.subplots(figsize=(9, 5))
        ax1.barh(df_marcas["marca"].head(10), df_marcas["participacion"].head(10))
        ax1.set_xlabel("Participación (%)")
        ax1.set_ylabel("Marca")
        ax1.set_title("Top 10 marcas por participación de mercado")
        ax1.invert_yaxis()
        st.pyplot(fig1)

    st.markdown("---")

    # ===============================
    # Análisis 2: Precio promedio por año
    # ===============================
    st.subheader("2. Evolución del precio promedio según año del vehículo")
    st.write(
        "Este análisis permite observar cómo varía el precio promedio de los vehículos según su año de fabricación."
    )

    df_year = df.groupby("year_limpio")["precio_num"].mean().reset_index()
    df_year = df_year.sort_values("year_limpio")

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(df_year["year_limpio"], df_year["precio_num"], marker="o")
    ax2.set_title("Precio promedio por año del vehículo")
    ax2.set_xlabel("Año del vehículo")
    ax2.set_ylabel("Precio promedio")
    ax2.tick_params(axis="x", rotation=45)
    st.pyplot(fig2)

    st.markdown("---")

    # ===============================
    # Análisis 3: Distribución por combustible
    # ===============================
    st.subheader("3. Distribución de vehículos por tipo de combustible")
    st.write(
        "Este análisis permite conocer qué tipo de combustible predomina en la oferta de vehículos usados."
    )

    if "combustible" in df.columns:
        df_combustible = df["combustible"].value_counts().reset_index()
        df_combustible.columns = ["combustible", "cantidad_autos"]

        col3, col4 = st.columns([1, 2])

        with col3:
            st.dataframe(df_combustible, hide_index=True)

        with col4:
            fig3, ax3 = plt.subplots(figsize=(8, 5))
            ax3.bar(df_combustible["combustible"], df_combustible["cantidad_autos"])
            ax3.set_title("Cantidad de vehículos por combustible")
            ax3.set_xlabel("Tipo de combustible")
            ax3.set_ylabel("Cantidad de vehículos")
            ax3.tick_params(axis="x", rotation=45)
            st.pyplot(fig3)
    else:
        st.info("La columna combustible no está disponible en la base de datos.")

    st.markdown("---")

    # ===============================
    # Conclusión estratégica
    # ===============================
    st.subheader("Conclusión estratégica")
    st.write(
        "A partir de estos análisis, AutoTec puede identificar las marcas con mayor presencia, "
        "evaluar el comportamiento de los precios según el año del vehículo y reconocer la composición "
        "del mercado según tipo de combustible. Esta información sirve como apoyo para decisiones de compra, "
        "publicación de vehículos, segmentación comercial y planificación de inventario."
    )
# -----------------------------------
# Pestaña Nivel Táctico
# -----------------------------------
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

# -----------------------------------
# Pestaña Nivel Operacional
# -----------------------------------
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