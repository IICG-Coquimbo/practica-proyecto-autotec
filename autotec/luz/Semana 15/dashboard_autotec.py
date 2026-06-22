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
# 7️⃣ Nivel estrategico
# ==============================

st.header("Concentración del mercado por marca")
st.caption("KPI: Participación de marcas | Objetivo: Identificar dominio y presencia de marcas en la muestra | Frecuencia: Trimestral")

# Contamos cuántos modelos tiene cada marca
marca_modelos = df_filtrado.groupby('marca')['modelo'].nunique().reset_index()
marcas_top_modelos = marca_modelos[marca_modelos['modelo'] > 10]['marca'].tolist()

# Filtramos df por esas marcas
df_marca_filtrada = df_filtrado[df_filtrado['marca'].isin(marcas_top_modelos)]

# Calculamos la participación de cada marca
df_marca = df_marca_filtrada['marca'].value_counts(normalize=True).reset_index()
df_marca.columns = ["Marca", "Participación (%)"]
df_marca["Participación (%)"] = df_marca["Participación (%)"] * 100

# Gráfico horizontal con porcentaje al lado de la barra
fig_marca = px.bar(
    df_marca,
    y="Marca",
    x="Participación (%)",
    text=df_marca["Participación (%)"].apply(lambda x: f"{x:.1f}%"),
    orientation="h",
    color="Participación (%)",
    color_continuous_scale=px.colors.sequential.Reds,
    title="Participación de marcas (solo con >10 modelos)"
)
fig_marca.update_traces(
    textposition='outside',             # Texto afuera de la barra
    texttemplate='%{x:.1f}%',           # Formato 1 decimal + %
)

fig_marca.update_layout(
    yaxis={'categoryorder':'total ascending'},
    bargap=0.3,                           # Reduce espacio entre barras, haciéndolas más gruesas
    height=700                             # Ajusta la altura total del gráfico
)
st.plotly_chart(fig_marca, use_container_width=True)

# Gráfico 2: Tendencia del precio promedio de vehículos (line chart)
st.header("Tendencia del precio promedio de vehículos")
st.caption("KPI: Precio promedio de vehículos en el tiempo | Objetivo: Mostrar la tendencia del valor promedio del mercado para detectar alzas, caídas o estabilidad | Frecuencia: Mensual")

df_year = df_filtrado.groupby("year")["precio"].mean().reset_index()

fig_precio = px.line(
    df_year,
    x="year",
    y="precio",
    markers=True,
    line_shape="linear",
    color_discrete_sequence=["#D62E00"],
    labels={"year":"Año", "precio":"Precio promedio ($)"},
    title="Precio promedio de vehículos en el tiempo"
)
fig_precio.update_yaxes(tickformat=",.0f")  # 10000000 -> 10.000.000
st.plotly_chart(fig_precio, use_container_width=True)


st.header("Pérdida de valor promedio por kilómetro")
st.caption("KPI: Costo de depreciación por kilómetro recorrido | Objetivo: Medir la pérdida de valor promedio asociada al uso del vehículo | Frecuencia: Trimestral")

# Suponiendo que df_filtrado ya existe con tus datos
# Creamos tramos de kilometraje
bins = [0, 50000, 100000, 150000, 200000, 300000, float('inf')]
labels = ["0-50 mil", "50-100 mil", "100-150 mil", "150-200 mil", "200-300 mil", "+300 mil"]
df_filtrado['tramo_km'] = pd.cut(df_filtrado['kilometraje'], bins=bins, labels=labels, include_lowest=True)

# Calculamos precio promedio por tramo
df_tramo = df_filtrado.groupby('tramo_km')['precio'].mean().reset_index()

# Creamos el gráfico
fig_km = px.line(
    df_tramo,
    x='tramo_km',
    y='precio',
    markers=True,
    title="Costo de depreciación por kilómetro recorrido",
    labels={
        "tramo_km":"Tramo de kilometraje",
        "precio":"Precio promedio ($)"
    },
    color_discrete_sequence=["#D62E00"] 
)
fig_km.update_yaxes(tickformat=",.0f")
# Mostramos en Streamlit
st.plotly_chart(fig_km, use_container_width=True)

df_modelo = df_filtrado.groupby(["modelo","year"])["precio"].mean().nlargest(30).reset_index()
fig_modelo = px.bar(
    df_modelo,
    x="modelo",
    y="precio",
    color="precio",
    color_continuous_scale=px.colors.sequential.Reds,
    title="Precio Promedio por Modelo (Top 30)",
    labels={"precio":"Precio Promedio ($)", "modelo":"Modelo"},
    color_discrete_sequence=["#D62E00"] 
)
fig_modelo.update_yaxes(tickformat=",.0f")
st.plotly_chart(fig_modelo, use_container_width=True)
    
fig_ant = px.scatter(
df_filtrado,
    x="kilometraje",
    y="precio",
    size="antiguedad_auto",
    color="categoria_precio",
    hover_data=["marca", "modelo", "year", "ciudad", "antiguedad_auto"],
    title="Precio vs Kilometraje (tamaño según Antigüedad)"
)
st.plotly_chart(fig_ant, use_container_width=True)


# ==============================
# 8️⃣ Nivel tactico
# ==============================
with tab_tac:
    st.subheader("Nivel Táctico: Análisis de Precios y Distribución por Marca")
    
    # Gráfico 1: Histograma de precios por categoría
    fig_hist = px.histogram(
        df_filtrado,
        x="precio",
        nbins=30,
        color="categoria_precio",
        title="Distribución de Precios por Categoría",
        labels={"precio":"Precio ($)", "categoria_precio":"Categoría"}
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Gráfico 2: Cantidad de vehículos por marca
    df_marca = df_filtrado.groupby("marca")["precio"].count().reset_index()
    df_marca.columns = ["marca", "cantidad"]
    fig_bar_marca = px.bar(
        df_marca,
        x="marca",
        y="cantidad",
        color="cantidad",
        title="Cantidad de Vehículos por Marca",
        labels={"marca":"Marca", "cantidad":"Cantidad de Vehículos"}
    )
    st.plotly_chart(fig_bar_marca, use_container_width=True)
    
    # Gráfico 3: Precio vs Kilometraje por tipo de marca (premium/general)
    fig_scatter = px.scatter(
        df_filtrado,
        x="kilometraje",
        y="precio",
        color="tipo_marca",
        size="precio",
        hover_data=["marca", "modelo", "year"],
        title="Precio vs Kilometraje por Tipo de Marca",
        labels={"kilometraje":"Kilometraje (km)", "precio":"Precio ($)", "tipo_marca":"Tipo de Marca"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    

# ==============================
# 9️⃣ Evolución Precio Promedio por Año
# ==============================
with tab_op:
    st.subheader("Nivel Operacional: Evolución y Alertas")
    
    # Gráfico 1: Evolución del precio promedio por año
    df_year = df_filtrado.groupby("year")["precio"].mean().reset_index()
    fig_line = px.line(
        df_year,
        x="year",
        y="precio",
        title="Evolución de Precio Promedio por Año",
        labels={"year":"Año", "precio":"Precio Promedio ($)"}
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Placeholder/indicador operativo: vehículos con alto kilometraje o riesgo de depreciación
    umbral_km = st.slider("Kilometraje crítico", min_value=50000, max_value=250000, value=120000, step=10000)
    umbral_anio = st.slider("Año crítico", min_value=2005, max_value=2024, value=2014, step=1)
    
    zona_riesgo = df_filtrado[
        (df_filtrado["kilometraje"] >= umbral_km) | 
        (df_filtrado["year"] <= umbral_anio)
    ]
    st.warning(f"⚠️ Vehículos en zona de riesgo: {len(zona_riesgo)}")
    
    st.dataframe(zona_riesgo[["marca", "modelo", "year", "kilometraje", "precio", "tipo_marca"]])


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

