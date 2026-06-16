import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard Automotriz Ejecutivo", layout="wide")

st.title("Cuadro de Mando Integral - Analítica Automotriz")
st.markdown("### Proyecto Big Data | Depreciación por marca y modelo")
st.markdown("---")

# 2. Carga de datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("datos_automotriz_dashboard.csv")

    # Estandarización mínima
    if "precio" in df.columns:
        df["precio"] = pd.to_numeric(df["precio"], errors="coerce")

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

    if "kilometraje" in df.columns:
        df["kilometraje"] = pd.to_numeric(df["kilometraje"], errors="coerce")

    # Variable derivada clave para el proyecto
    if "year" in df.columns and "antiguedad_auto" not in df.columns:
        df["antiguedad_auto"] = datetime.now().year - df["year"]

    return df

df = cargar_datos()

# 3. Validación básica
st.sidebar.header("Filtros globales")

marcas = sorted(df["marca"].dropna().unique()) if "marca" in df.columns else []
marcas_sel = st.sidebar.multiselect(
    "Selecciona marcas:",
    options=marcas,
    default=marcas
)

df = df[df["marca"].isin(marcas_sel)] if "marca" in df.columns else df

if df.empty:
    st.warning("No hay datos disponibles con los filtros seleccionados.")
    st.stop()

# 4. Tabs por nivel organizacional
tab_est, tab_tac, tab_op = st.tabs([
    "Nivel Estratégico (CEO)",
    "Nivel Táctico (Gerencia)",
    "Nivel Operacional (Supervisor)"
])

# ==========================================
# PESTAÑA 1: NIVEL ESTRATÉGICO
# ==========================================
with tab_est:
    st.header("Concentración del mercado por marca")
    st.caption("Frecuencia: Mensual | Objetivo: Identificar dominio y presencia de marcas en la muestra")

    total_autos = len(df)

    df_est = df["marca"].value_counts().reset_index()
    df_est.columns = ["marca", "cantidad_autos"]
    df_est["participacion"] = (df_est["cantidad_autos"] / total_autos) * 100

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric("Total vehículos analizados", total_autos)
        st.metric(
            "Marca líder",
            df_est["marca"].iloc[0],
            delta=f"{df_est['participacion'].iloc[0]:.1f}% del mercado analizado"
        )
        st.dataframe(df_est, hide_index=True, use_container_width=True)

    with col2:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        sns.barplot(
            data=df_est,
            x="participacion",
            y="marca",
            hue="marca",
            palette="Blues_r",
            legend=False,
            ax=ax
        )
        ax.set_xlabel("Participación (%)")
        ax.set_ylabel("Marca")
        ax.set_title("Participación de marcas en la base")
        sns.despine(left=True, bottom=False)
        st.pyplot(fig)
# ==============================
# 9️⃣ Evolución Precio Promedio por Año
# ==============================
with tab_est:
    st.subheader("Evolución de Precio Promedio por Año")
    df_year = df.groupby("year")["precio"].mean().reset_index()
    fig3 = px.line(df_year, x="year", y="precio")
    st.plotly_chart(fig3, use_container_width=True)

# ==========================================
# PESTAÑA 2: NIVEL TÁCTICO
# ==========================================
with tab_tac:
    st.header("Bandas de precios por marca")
    st.caption("Frecuencia: Semanal | Objetivo: Comparar dispersión de precios y posicionamiento competitivo")

    if "precio" not in df.columns:
        st.error("La columna 'precio' no existe en el dataset.")
    else:
        marcas_tac = st.multiselect(
            "Filtrar marcas para comparación:",
            options=sorted(df["marca"].dropna().unique()),
            default=sorted(df["marca"].dropna().unique())
        )

        df_filtrado = df[df["marca"].isin(marcas_tac)].copy()

        df_tac = (
            df_filtrado.groupby("marca")["precio"]
            .agg(["min", "mean", "max"])
            .reset_index()
            .sort_values(by="mean")
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            fig, ax = plt.subplots(figsize=(10, 4.8))
            ax.vlines(
                x=df_tac["marca"],
                ymin=df_tac["min"],
                ymax=df_tac["max"],
                colors="#B0BEC5",
                alpha=0.8,
                linewidth=3
            )
            ax.scatter(df_tac["marca"], df_tac["mean"], color="#0D47A1", s=120, zorder=3, label="Promedio")
            ax.scatter(df_tac["marca"], df_tac["min"], color="#2E7D32", marker="^", s=80, zorder=3, label="Mínimo")
            ax.scatter(df_tac["marca"], df_tac["max"], color="#C62828", marker="v", s=80, zorder=3, label="Máximo")
            ax.set_ylabel("Precio")
            ax.set_xlabel("Marca")
            ax.set_title("Rango de precios por marca")
            plt.xticks(rotation=25, ha="right")
            ax.legend()
            sns.despine(left=True)
            st.pyplot(fig)

        with col2:
            st.dataframe(df_tac, hide_index=True, use_container_width=True)
            
#  scatter de kilometraje vs precio
with tab_tac:
    st.subheader("Relación entre Kilometraje y Precio")

    fig = px.scatter(
        df,
        x="kilometraje",
        y="precio",
        color="categoria_precio",
        hover_data=["marca", "modelo", "year"],
        opacity=0.7,
    )

    st.plotly_chart(fig, use_container_width=True)
# ==========================================
# PESTAÑA 3: NIVEL OPERACIONAL
# ==========================================
with tab_op:
    st.header("Matriz de alertas: autos muy antiguos con precio alto")
    st.caption("Frecuencia: Diario | Objetivo: Detectar publicaciones potencialmente sobrevaloradas")

    if "antiguedad_auto" not in df.columns or "precio" not in df.columns:
        st.error("Se requieren las columnas 'antiguedad_auto' y 'precio' para este análisis.")
    else:
        colf1, colf2 = st.columns(2)

        with colf1:
            umbral_antiguedad = st.slider(
                "Ajustar umbral de antigüedad (años):",
                min_value=0,
                max_value=30,
                value=10,
                step=1
            )

        with colf2:
            precio_max = int(df["precio"].dropna().max()) if df["precio"].dropna().shape[0] > 0 else 20000000
            umbral_precio = st.slider(
                "Ajustar umbral de precio:",
                min_value=0,
                max_value=precio_max,
                value=min(15000000, precio_max),
                step=max(100000, precio_max // 100 if precio_max > 0 else 100000)
            )

        df_op = df.copy()

        zona_peligro = df_op[
            (df_op["antiguedad_auto"] > umbral_antiguedad) &
            (df_op["precio"] > umbral_precio)
        ].copy()

        st.warning(f"Se han detectado {len(zona_peligro)} vehículos con alerta operacional.")

        fig, ax = plt.subplots(figsize=(10, 5.5))
        ax.scatter(
            df_op["antiguedad_auto"],
            df_op["precio"],
            alpha=0.45,
            s=60,
            color="#78909C",
            label="Vehículos"
        )

        if not zona_peligro.empty:
            ax.scatter(
                zona_peligro["antiguedad_auto"],
                zona_peligro["precio"],
                color="#D32F2F",
                s=110,
                edgecolor="black",
                zorder=4,
                label="Alertas críticas"
            )

        ax.axvline(x=umbral_antiguedad, color="#C62828", linestyle="--", alpha=0.7)
        ax.axhline(y=umbral_precio, color="#C62828", linestyle="--", alpha=0.7)

        ax.set_xlabel("Antigüedad del auto (años)")
        ax.set_ylabel("Precio")
        ax.set_title("Alertas operacionales por antigüedad y precio")
        ax.legend()
        sns.despine(left=True)
        st.pyplot(fig)

        if len(zona_peligro) > 0:
            st.subheader("Lista de vehículos para revisión")
            columnas_mostrar = [c for c in ["marca", "modelo", "year", "precio", "kilometraje", "ciudad", "antiguedad_auto"] if c in zona_peligro.columns]
            st.dataframe(zona_peligro[columnas_mostrar], hide_index=True, use_container_width=True)



with tab_op:

    st.markdown("## Resumen Ejecutivo")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Autos Analizados", f"{len(df):,}")
    with col2: st.metric("Precio Promedio", f"${df['precio'].mean():,.0f}")
    with col3: st.metric("Kilometraje Promedio", f"{df['kilometraje'].mean():,.0f}")
    with col4: st.metric("Año Promedio", f"{int(df['year'].mean())}")
    st.markdown("---")

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

    # ============================
    # KPI 4: Precio por Combustible
    # ============================
    st.subheader(" Precio Promedio por Tipo de Combustible")
    fig4 = px.box(df, x="combustible", y="precio", color="combustible", title="Distribución de Precios por Tipo de Combustible")
    st.plotly_chart(fig4, use_container_width=True)
    eco = df[df["es_ecologico"] == 1]["precio"].mean()
    tradicional = df[df["combustible"].isin(["bencina","diesel"])]["precio"].mean()
    gap = eco - tradicional
    st.metric("Diferencia Ecológicos vs Tradicionales", f"${gap:,.0f}")
    st.success("✅ Los vehículos ecológicos presentan mayor valor promedio." if gap > 0 else "⚠️ Los vehículos ecológicos presentan menor valor promedio.")