import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==============================
# 1️⃣ Configuración de la página
# ==============================
st.set_page_config(
    page_title="🚗 DASHBOARD AUTOTEC - Vehículos Usados",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚗 DASHBOARD AUTOTEC - Vehículos Usados")
st.markdown("Explora los vehículos usados filtrando por marca, precio, año y analiza depreciación, kilometraje y tendencias.")
st.markdown("---")

# ==============================
# 2️⃣ Cargar los datos
# ==============================
ruta_csv = "datos_dashboard.csv"
df = pd.read_csv(ruta_csv)

# ==============================
# 3️⃣ Barra lateral con filtros
# ==============================
st.sidebar.header("Filtros")

marcas = df["marca"].unique()
marca_seleccionada = st.sidebar.multiselect("Marca", marcas, default=marcas)

categorias = df["categoria_precio"].unique()
categoria_seleccionada = st.sidebar.multiselect("Categoría de Precio", categorias, default=categorias)

anio_min = int(df["year"].min())
anio_max = int(df["year"].max())
anio_seleccionado = st.sidebar.slider("Año del Vehículo", anio_min, anio_max, (anio_min, anio_max))


# Filtro por rango de precio
precio_min = int(df["precio"].min())
precio_max = int(df["precio"].max())
precio_seleccionado = st.sidebar.slider(
    "Rango de Precio",
    precio_min,
    precio_max,
    (precio_min, precio_max),
    step=1000000
)

# Luego aplicas este filtro junto con los otros
df_filtrado = df[
    (df["marca"].isin(marca_seleccionada)) &
    (df["categoria_precio"].isin(categoria_seleccionada)) &
    (df["year"] >= anio_seleccionado[0]) &
    (df["year"] <= anio_seleccionado[1]) &
    (df["precio"] >= precio_seleccionado[0]) &
    (df["precio"] <= precio_seleccionado[1])
]
# ==============================
# 5️⃣ Depreciación como texto
# ==============================
map_depreciacion = {
    "baja depreciacion": "Baja Depreciación",
    "depreciacion media": "Depreciación Media",
    "alta depreciacion": "Alta Depreciación",
    "N/A": "N/A"
}
df_filtrado['depreciacion_texto'] = df_filtrado['segmento_depreciacion'].map(map_depreciacion)

# ==============================
# 6️⃣ Indicadores principales
# ==============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("🚙 Vehículos filtrados", len(df_filtrado))
col2.metric("💰 Precio promedio", f"${df_filtrado['precio'].mean():,.0f}")
col3.metric("🛣️ Kilometraje promedio", f"{df_filtrado['kilometraje'].mean():,.0f} km")

# Depreciación: mostrar el texto más frecuente
dep_prom = df_filtrado['depreciacion_texto'].mode()[0] if not df_filtrado['depreciacion_texto'].isna().all() else "N/A"
col4.metric("📉 Depreciación promedio", dep_prom)

tab_est, tab_tac, tab_op = st.tabs([
    "📊 Nivel Estratégico",
    "📈 Nivel Táctico",
    "⚙️ Nivel Operacional"
])

# ==============================
# 7️⃣ Gráfico: Precio vs Kilometraje
# ==============================
with tab_est:
    st.subheader("Relación Precio vs Kilometraje")
    fig1 = px.scatter(
        df_filtrado,
        x="kilometraje",
        y="precio",
        color="categoria_precio",
        size=df_filtrado['depreciacion_texto'].map({
            "Baja Depreciación": 5,
            "Depreciación Media": 10,
            "Alta Depreciación": 15,
        "N/A": 0
        }),
        hover_data=["marca", "modelo", "year", "segmento_depreciacion"],
    )
    st.plotly_chart(fig1, use_container_width=True)

# ==============================
# 8️⃣ Histograma de precios
# ==============================
with tab_tac:
    st.subheader("Distribución de Precios por Categoría")
    fig2 = px.histogram(
    df_filtrado,
    x="precio",
    nbins=30,
    color="categoria_precio",
    )
    st.plotly_chart(fig2, use_container_width=True)

# ==============================
# 9️⃣ Evolución Precio Promedio por Año
# ==============================
with tab_op:
    st.subheader("Evolución de Precio Promedio por Año")
    df_year = df_filtrado.groupby("year")["precio"].mean().reset_index()
    fig3 = px.line(df_year, x="year", y="precio")
    st.plotly_chart(fig3, use_container_width=True)

# ==============================
# 🔟 Tabla de datos filtrados
# ==============================
st.subheader("Datos filtrados")
st.dataframe(df_filtrado)

# ==============================
# 1️⃣1️⃣ Botón para descargar CSV
# ==============================
st.download_button(
    "Descargar datos filtrados",
    df_filtrado.to_csv(index=False).encode("utf-8"),
    file_name="datos_filtrados_autotec.csv",
    mime="text/csv"
)

# ==============================
# 1️⃣2️⃣ Interpretación inicial
# ==============================
st.subheader("Interpretación inicial")
st.markdown("""
- Los vehículos se concentran en categorías de precio alto y medio.
- El precio y kilometraje promedio reflejan el uso general de los autos.
- La depreciación promedio muestra la tendencia de pérdida de valor.
- Los gráficos permiten explorar relaciones entre precio, kilometraje y categoría.
""")