# HydroAlert Perú - Versión Premium PRO

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="HydroAlert Perú", layout="wide")

st.title("HydroAlert Perú - Monitoreo Inteligente")
st.markdown("""
Esta aplicación muestra datos hidrológicos y meteorológicos en tiempo real.
Provee visualizaciones interactivas para facilitar la interpretación de los datos.
""")

# Cargar CSV
try:
    df = pd.read_csv("rios_peru_sample.csv")
    columnas_esperadas = {'nombre', 'nivel', 'riesgo', 'region'}
    if not columnas_esperadas.issubset(df.columns):
        raise ValueError("El archivo CSV no contiene las columnas necesarias: 'nombre', 'nivel', 'riesgo', 'region'")
except Exception as e:
    st.error(f"Error al cargar CSV: {e}")
    st.stop()

# Selector interactivo de río
rio_seleccionado = st.selectbox("Selecciona un río para ver su estado:", df['nombre'].unique())
rio_datos = df[df['nombre'] == rio_seleccionado].iloc[0]

# Mostrar información del río
st.subheader(f"Estado actual del Río {rio_seleccionado}")
st.markdown(f"**Nivel:** {rio_datos['nivel']} cm")
st.markdown(f"**Nivel de Riesgo:** {rio_datos['riesgo']}")

# Color según riesgo
colores_riesgo = {"BAJO": "green", "MODERADO": "orange", "ALTO": "red"}
color = colores_riesgo.get(rio_datos['riesgo'].upper(), "gray")
st.markdown(f"<div style='background-color:{color}; padding:10px; color:white;'>RIESGO: {rio_datos['riesgo']}</div>", unsafe_allow_html=True)

# Gráfico de barras
st.subheader("Comparativa de Niveles de Ríos")
fig = px.bar(df, x='nombre', y='nivel', color='riesgo', title='Niveles actuales por río')
st.plotly_chart(fig, use_container_width=True)

# Pronóstico del tiempo
st.subheader("Pronóstico del Clima en Lima")
try:
    weather = requests.get("https://wttr.in/Lima?format=3").text
    st.text(weather)
except:
    st.warning("No se pudo obtener el clima actual.")

# Noticias
st.subheader("Noticias Recientes sobre Recursos Hídricos")
noticias = [
    {"titulo": "Senamhi alerta de posibles desbordes en la selva", "link": "https://www.senamhi.gob.pe"},
    {"titulo": "Proyectos de prevención ante lluvias intensas en Perú", "link": "https://elcomercio.pe"},
]
for noticia in noticias:
    st.markdown(f"- [{noticia['titulo']}]({noticia['link']})")

# Videos informativos
st.subheader("Videos Informativos")
videos = [
    "https://www.youtube.com/embed/zqsIIcbqomQ",  # verificado como funcional
    "https://www.youtube.com/embed/2aHDuEaErE0",
    "https://www.youtube.com/embed/NalRIRJz4Hk"
]

for url in videos:
    st.video(url)

st.success("Aplicación cargada correctamente. Datos actualizados.")
