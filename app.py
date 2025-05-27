import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

st.set_page_config(page_title="HydroAlert Perú", layout="wide")

st.title("HydroAlert Perú – Monitoreo Inteligente de Ríos y Clima")

# Cargar datos CSV (debe estar en el mismo directorio)
try:
    df = pd.read_csv("rios_peru_sample.csv")
except FileNotFoundError:
    st.error("Archivo CSV no encontrado. Asegúrate de que 'rios_peru_sample.csv' esté en el mismo directorio que este archivo.")
    st.stop()

# Validar columnas requeridas
required_columns = {"rio", "region", "nivel", "riesgo"}
if not required_columns.issubset(df.columns):
    st.error("El archivo CSV debe contener las columnas: rio, region, nivel, riesgo.")
    st.stop()

# Selección de región y río
regiones = df["region"].unique()
region_seleccionada = st.selectbox("Selecciona una región:", regiones)

rios_filtrados = df[df["region"] == region_seleccionada]["rio"].unique()
rio_seleccionado = st.selectbox("Selecciona un río:", rios_filtrados)

df_rio = df[(df["region"] == region_seleccionada) & (df["rio"] == rio_seleccionado)]

# Mostrar información básica
nivel = df_rio["nivel"].values[0]
riesgo = df_rio["riesgo"].values[0]

st.markdown(f"### Estado del río **{rio_seleccionado}**: Nivel **{nivel}**")
st.markdown(f"### Nivel de riesgo actual: **{riesgo}**")

# Mapa (opcional si hay lat/lon en CSV)
# Gráfico de barras
fig = px.bar(df[df["region"] == region_seleccionada], x="rio", y="nivel", color="riesgo", 
             color_discrete_map={
                 "Bajo": "green",
                 "Medio": "orange",
                 "Alto": "red"
             }, title=f"Niveles de los ríos en {region_seleccionada}")
st.plotly_chart(fig, use_container_width=True)

# Pronóstico del tiempo (Open-Meteo API para Lima)
st.subheader("Pronóstico del tiempo en Lima")

try:
    weather = requests.get("https://api.open-meteo.com/v1/forecast?latitude=-12.05&longitude=-77.04&current_weather=true").json()
    temp = weather["current_weather"]["temperature"]
    wind = weather["current_weather"]["windspeed"]
    st.metric(label="Temperatura actual (°C)", value=temp)
    st.metric(label="Velocidad del viento (km/h)", value=wind)
except:
    st.warning("No se pudo obtener el clima actual.")

# Noticias (simplificadas, reales requerirían scraping o API externa)
st.subheader("Noticias recientes relacionadas")
st.markdown("- [Prevención de inundaciones en el Rímac](https://elcomercio.pe)")
st.markdown("- [Alertas hidrometeorológicas activadas por Senamhi](https://andina.pe)")
st.markdown("- [Consejos de seguridad ante crecida de ríos](https://gestion.pe)")

# Videos educativos funcionales
st.subheader("Videos informativos")
video_ids = [
    "zqsIIcbqomQ",  # Aportado por ti
    "Nk6FV4l0gFQ",  # Video oficial Senamhi (si funciona)
    "8s0U4CUv1bg"   # Otro relacionado con prevención de desastres
]

for vid in video_ids:
    st.video(f"https://www.youtube.com/watch?v={vid}")
