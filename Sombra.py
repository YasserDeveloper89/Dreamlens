# PROYECTO SOMBRA PRO - Plataforma de Inteligencia Social y Narrativas (Versión Ultra Premium)
# Requiere: streamlit, pandas, plotly, geopandas (opcional), folium

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# Configuración general
st.set_page_config(page_title="PROYECTO SOMBRA PRO", layout="wide", page_icon="🕵️")
st.title("PROYECTO SOMBRA PRO")
st.markdown("""
**Sistema avanzado de simulación de narrativas sociales, propagación emocional y mapeo de tensiones en el Perú.**
Desarrollado para defensa, inteligencia, gobiernos y analistas de riesgo sociopolítico.
""")

# Sidebar - Filtros de control
st.sidebar.header("Panel de Control")
region = st.sidebar.selectbox("Región objetivo", ["Lima", "Arequipa", "Cusco", "Piura", "Puno", "Tacna"])
tematica = st.sidebar.selectbox("Tema de narrativa", [
    "Corrupción estatal", "Crisis alimentaria", "Migración", "Contaminación minera", "Educación", "Salud pública"
])
emocion = st.sidebar.selectbox("Emoción propagada", ["Miedo", "Indignación", "Esperanza", "Desconfianza"])
periodo = st.sidebar.slider("Duración (días)", 1, 30, 7)

narrativa = f"Se reporta incremento de {tematica.lower()} en {region}, generando {emocion.lower()} en población."

# Tabs
tabs = st.tabs(["Mapa Interactivo", "Tendencias", "Mensajes Sociales", "Dashboard", "Informe"])

# Mapa Interactivo
with tabs[0]:
    st.subheader("Mapa de Tensiones Sociales")
    regiones = ["Lima", "Arequipa", "Cusco", "Piura", "Puno", "Tacna"]
    lat = [-12.05, -16.4, -13.5, -5.2, -15.8, -18.0]
    lon = [-77.04, -71.5, -72.0, -80.6, -70.0, -70.25]
    intensidad = [random.uniform(0.1, 1.0) for _ in regiones]
    mapa_df = pd.DataFrame({"Region": regiones, "Lat": lat, "Lon": lon, "Intensidad": intensidad})
    fig_map = px.density_mapbox(mapa_df, lat="Lat", lon="Lon", z="Intensidad", radius=30,
        center=dict(lat=-10, lon=-75), zoom=4, mapbox_style="carto-positron", hover_name="Region")
    st.plotly_chart(fig_map, use_container_width=True)

# Tendencias
with tabs[1]:
    st.subheader("Tendencias Digitales Simuladas")
    st.info("Basado en comportamientos reales de redes en Perú")
    hashtags = [f"#{tematica.replace(' ', '')}", f"#{region}Despierta", "#CrisisYa", "#JusticiaSocial"]
    st.code("\n".join(hashtags))
    dates = pd.date_range(datetime.now() - timedelta(days=periodo), periods=periodo)
    evol = [random.randint(100, 2000) for _ in dates]
    df_line = pd.DataFrame({"Fecha": dates, "Intensidad": evol})
    fig_line = px.line(df_line, x="Fecha", y="Intensidad", title="Evolución de la narrativa")
    st.plotly_chart(fig_line, use_container_width=True)

# Mensajes Sociales
with tabs[2]:
    st.subheader("Narrativas Simuladas en Red")
    usuarios = ["@alertaperu", "@indignado", "@periodista", "@ciudadanox"]
    for _ in range(6):
        msg = random.choice([
            f"{tematica} está destruyendo el futuro de {region}. {emocion.upper()}!",
            f"Ya no podemos ignorar la {tematica.lower()}...",
            f"Gobierno no responde ante {tematica.lower()} en {region}"
        ])
        st.write(f"**{random.choice(usuarios)}**: {msg}")

# Dashboard
with tabs[3]:
    st.subheader("Panel de Indicadores de Riesgo")
    metrics = {
        "Alcance Narrativo": random.randint(10000, 100000),
        "Población Afectada": random.randint(1000, 50000),
        "Nivel de Crisis": random.choice(["Bajo", "Medio", "Alto"]),
        "Tasa de Reacción": f"{random.uniform(0.3, 0.9):.2f}"
    }
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Alcance Narrativo", metrics["Alcance Narrativo"])
        st.metric("Nivel de Crisis", metrics["Nivel de Crisis"])
    with col2:
        st.metric("Población Afectada", metrics["Población Afectada"])
        st.metric("Tasa de Reacción", metrics["Tasa de Reacción"])

# Informe
with tabs[4]:
    st.subheader("Informe Ejecutable")
    resumen = f"Narrativa detectada en {region} sobre {tematica}. Propagación emocional: {emocion}."
    st.text_area("Resumen del Informe:", resumen, height=100)
    st.download_button("Descargar Informe PDF", data=resumen, file_name="informe_sombra.txt")
