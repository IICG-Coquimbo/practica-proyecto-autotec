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
    st.header("Nivel Táctico: Análisis comercial de precios y segmentos")
    st.caption(
        "Frecuencia: semanal/mensual | Objetivo: apoyar decisiones comerciales "
        "comparando marcas, precios, kilometraje, combustible y ciudad."
    )

    df_tactico = df.copy()

    # Si la columna ciudad viene como ciudad_o_comuna, se adapta para el análisis
    if "ciudad" not in df_tactico.columns and "ciudad_o_comuna" in df_tactico.columns:
        df_tactico["ciudad"] = df_tactico["ciudad_o_comuna"]

    # -----------------------------------
    # Crear variables tácticas
    # -----------------------------------
    df_tactico["rango_kilometraje"] = pd.cut(
        df_tactico["km_num"],
        bins=[
            0,
            50000,
            100000,
            150000,
            200000,
            df_tactico["km_num"].max()
        ],
        labels=[
            "0 - 50.000 km",
            "50.001 - 100.000 km",
            "100.001 - 150.000 km",
            "150.001 - 200.000 km",
            "Más de 200.000 km"
        ],
        include_lowest=True
    )

    df_tactico["categoria_precio"] = pd.cut(
        df_tactico["precio_num"],
        bins=[
            0,
            df_tactico["precio_num"].quantile(0.33),
            df_tactico["precio_num"].quantile(0.66),
            df_tactico["precio_num"].max()
        ],
        labels=[
            "Precio bajo",
            "Precio medio",
            "Precio alto"
        ],
        include_lowest=True
    )

    # -----------------------------------
    # Filtros tácticos
    # -----------------------------------
    st.subheader("Filtros del análisis táctico")

    marcas_disponibles = sorted(df_tactico["marca"].dropna().unique())

    marcas_seleccionadas = st.multiselect(
        "Selecciona marcas para analizar",
        options=marcas_disponibles,
        default=marcas_disponibles[:8]
    )

    df_tactico = df_tactico[df_tactico["marca"].isin(marcas_seleccionadas)]

    if df_tactico.empty:
        st.warning("No hay datos disponibles para las marcas seleccionadas.")
    else:
        precio_promedio_general = df_tactico["precio_num"].mean()
        kilometraje_promedio = df_tactico["km_num"].mean()
        total_autos_tactico = len(df_tactico)

        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

        with col_kpi1:
            st.metric("Vehículos filtrados", total_autos_tactico)

        with col_kpi2:
            st.metric("Precio promedio", f"${precio_promedio_general:,.0f}")

        with col_kpi3:
            st.metric("Kilometraje promedio", f"{kilometraje_promedio:,.0f} km")

        st.markdown("---")

        # =====================================================
        # ANÁLISIS 1: Desviación de precios por marca
        # =====================================================
        st.subheader("1. Desviación del precio promedio por marca")
        st.write(
            "Este análisis compara el precio promedio de cada marca seleccionada "
            "con el precio promedio general del conjunto filtrado."
        )

        df_marca_precio = df_tactico.groupby("marca")["precio_num"].agg(
            precio_promedio="mean",
            cantidad_autos="count"
        ).reset_index()

        df_marca_precio["desviacion_pct"] = (
            (df_marca_precio["precio_promedio"] - precio_promedio_general)
            / precio_promedio_general
        ) * 100

        df_marca_precio = df_marca_precio.sort_values("desviacion_pct", ascending=True)

        col1, col2 = st.columns([1, 2])

        with col1:
            st.dataframe(
                df_marca_precio.sort_values("desviacion_pct", ascending=False),
                hide_index=True
            )

        with col2:
            fig1, ax1 = plt.subplots(figsize=(9, 5))
            ax1.barh(df_marca_precio["marca"], df_marca_precio["desviacion_pct"])
            ax1.axvline(0, linestyle="--")
            ax1.set_title("Desviación porcentual del precio promedio por marca")
            ax1.set_xlabel("Desviación respecto al promedio general (%)")
            ax1.set_ylabel("Marca")
            st.pyplot(fig1)

        st.markdown("---")

        # =====================================================
        # ANÁLISIS 2: Autos bajo promedio por rango de kilometraje
        # =====================================================
        st.subheader("2. Autos bajo el precio promedio según rango de kilometraje")
        st.write(
            "Este análisis identifica en qué rangos de kilometraje existe mayor proporción "
            "de vehículos con precio inferior al promedio de su propio rango."
        )

        precio_promedio_rango = df_tactico.groupby(
            "rango_kilometraje",
            observed=True
        )["precio_num"].transform("mean")

        df_tactico["precio_promedio_rango"] = precio_promedio_rango

        df_tactico["bajo_promedio_rango"] = (
            df_tactico["precio_num"] < df_tactico["precio_promedio_rango"]
        )

        df_km = df_tactico.groupby("rango_kilometraje", observed=True).agg(
            cantidad_autos=("precio_num", "count"),
            precio_promedio=("precio_num", "mean"),
            porcentaje_bajo_promedio=("bajo_promedio_rango", "mean")
        ).reset_index()

        df_km["porcentaje_bajo_promedio"] = df_km["porcentaje_bajo_promedio"] * 100

        col3, col4 = st.columns([1, 2])

        with col3:
            st.dataframe(df_km, hide_index=True)

        with col4:
            fig2, ax2 = plt.subplots(figsize=(9, 5))
            ax2.bar(
                df_km["rango_kilometraje"].astype(str),
                df_km["porcentaje_bajo_promedio"]
            )
            ax2.set_title("Porcentaje de autos bajo promedio por rango de kilometraje")
            ax2.set_xlabel("Rango de kilometraje")
            ax2.set_ylabel("Autos bajo promedio (%)")
            ax2.tick_params(axis="x", rotation=45)
            st.pyplot(fig2)

        st.markdown("---")

        # =====================================================
        # ANÁLISIS 3: Precio promedio por combustible y ciudad
        # =====================================================
        st.subheader("3. Precio promedio por tipo de combustible y ciudad")
        st.write(
            "Este análisis compara el precio promedio de los vehículos según ciudad "
            "y tipo de combustible."
        )

        if "combustible" in df_tactico.columns and "ciudad" in df_tactico.columns:
            top_ciudades = df_tactico["ciudad"].value_counts().head(6).index
            top_combustibles = df_tactico["combustible"].value_counts().head(4).index

            df_ciudad_comb = df_tactico[
                (df_tactico["ciudad"].isin(top_ciudades)) &
                (df_tactico["combustible"].isin(top_combustibles))
            ]

            df_precio_ciudad = df_ciudad_comb.groupby(
                ["ciudad", "combustible"]
            )["precio_num"].mean().reset_index()

            tabla_pivot = df_precio_ciudad.pivot(
                index="ciudad",
                columns="combustible",
                values="precio_num"
            )

            col5, col6 = st.columns([1, 2])

            with col5:
                st.dataframe(df_precio_ciudad, hide_index=True)

            with col6:
                fig3, ax3 = plt.subplots(figsize=(10, 5))
                tabla_pivot.plot(kind="bar", ax=ax3)
                ax3.set_title("Precio promedio por ciudad y combustible")
                ax3.set_xlabel("Ciudad")
                ax3.set_ylabel("Precio promedio")
                ax3.tick_params(axis="x", rotation=45)
                ax3.legend(title="Combustible")
                st.pyplot(fig3)

        else:
            st.info("No se encuentran disponibles las columnas combustible y ciudad para este análisis.")

        st.markdown("---")

        # =====================================================
        # Conclusión táctica
        # =====================================================
        st.subheader("Conclusión táctica")
        st.write(
            "Los análisis tácticos permiten comparar marcas, rangos de kilometraje, "
            "precios promedio, ciudades y tipos de combustible. Esta información apoya "
            "la gestión comercial de AutoTec, ya que permite identificar diferencias de precio, "
            "segmentos de mercado y posibles oportunidades de publicación o ajuste comercial."
        )
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