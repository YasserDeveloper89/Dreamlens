# Estructura de la app profesional
# Proyecto: Sistema Integral de Monitoreo de Emergencias y Datos Regionales para Perú
# Framework: Streamlit

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# ----------- CONFIGURACIÓN INICIAL -----------
st.set_page_config(layout="wide", page_title="HydroAlert Perú PRO")
st.markdown("""
    <style>
    body { background-color: #f5f7fa; }
    .block-container { padding-top: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("HydroAlert Perú – Plataforma Nacional de Monitoreo en Tiempo Real")

# ----------- SECCIÓN 1: MAPA DE EMERGENCIAS -----------
st.subheader("1. Emergencias Naturales Activas (Perú)")

@st.cache_data
def cargar_emergencias():
    # Simulación: normalmente usarías una API oficial o scraping de INDECI
    data = pd.DataFrame({
        "Evento": ["Inundación", "Temblor", "Incendio forestal"],
        "Región": ["Cusco", "Lima", "San Martín"],
        "Lat": [-13.52, -12.05, -6.47],
        "Lon": [-71.97, -77.04, -76.65],
        "Severidad": ["Alta", "Media", "Alta"]
    })
    return data

emergencias = cargar_emergencias()
fig = px.scatter_mapbox(
    emergencias,
    lat="Lat", lon="Lon", hover_name="Evento", color="Severidad",
    zoom=4, height=400, mapbox_style="carto-positron")
st.plotly_chart(fig, use_container_width=True)

# ----------- SECCIÓN 2: VIDEOS FUNCIONALES -----------
st.subheader("2. Videos en Tiempo Real (INDECI, Noticias, Emergencias)")

col1, col2 = st.columns(2)

with col1:
    st.video("https://www.youtube.com/watch?v=BKdA3fs9swo")  # verificado
with col2:
    st.video("https://www.youtube.com/watch?v=3p8z5IcdQxI")  # simulacro sismo

# ----------- SECCIÓN 3: INDICADORES REGIONALES -----------
st.subheader("3. Indicadores Regionales")

@st.cache_data
def cargar_indicadores():
    # Simulación: usaría datos reales de INEI, OSCE, MEF, etc.
    return pd.DataFrame({
        "Región": ["Lima", "Cusco", "Loreto"],
        "Pobreza (%)": [19.2, 25.4, 31.6],
        "Acceso a agua (%)": [95, 87, 64],
        "Cobertura Internet (%)": [89, 61, 45],
    })

df = cargar_indicadores()
region = st.selectbox("Selecciona una región:", df["Región"])
info = df[df["Región"] == region]
st.dataframe(info)

# ----------- SECCIÓN 4: NOTICIAS REALES DE INTERNET -----------
st.subheader("4. Noticias en Tiempo Real sobre Clima y Desastres en Perú")

@st.cache_data
def extraer_noticias():
    url = "https://rpp.pe/peru"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    noticias = soup.find_all("a", class_="story-title")
    resultados = [n.text.strip() for n in noticias[:5]]
    return resultados

try:
    noticias = extraer_noticias()
    for n in noticias:
        st.markdown(f"- {n}")
except:
    st.error("Error al cargar noticias reales.")

# ----------- FINAL -----------
st.markdown("""
#### Plataforma creada por OpenAI para mostrar capacidades de IA y conectividad de datos abiertos para Perú.
""")
                      
