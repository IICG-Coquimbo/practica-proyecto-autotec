import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

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