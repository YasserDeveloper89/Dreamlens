import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime

st.set_page_config(layout="wide", page_title="HydroAlert Perú")
st.title("HydroAlert Perú – Monitoreo Inteligente de Ríos y Clima")

# Cargar datos CSV
try:
    df = pd.read_csv("rios_peru_sample.csv")
except FileNotFoundError:
    st.error("No se encontró el archivo de datos CSV. Asegúrate de colocarlo en el mismo directorio.")

# Función para mostrar el estado por río
if 'region' in df.columns and 'caudal' in df.columns:
    regiones = df['region'].unique()
    region_seleccionada = st.selectbox("Selecciona una región para visualizar su caudal:", regiones)
    df_filtrado = df[df['region'] == region_seleccionada]
    fig = px.line(df_filtrado, x='fecha', y='caudal', title=f"Caudal del río en {region_seleccionada}")
    st.plotly_chart(fig, use_container_width=True)

# Pronóstico del tiempo actual desde Open-Meteo
st.subheader("Pronóstico del Tiempo (Lima)")
params = {
    "latitude": -12.0464,
    "longitude": -77.0428,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "auto"
}
response = requests.get("https://api.open-meteo.com/v1/forecast", params=params)
if response.status_code == 200:
    data = response.json()
    dias = data['daily']['time']
    temp_max = data['daily']['temperature_2m_max']
    temp_min = data['daily']['temperature_2m_min']
    lluvia = data['daily']['precipitation_sum']
    df_clima = pd.DataFrame({
        "Fecha": dias,
        "Temp Max (°C)": temp_max,
        "Temp Min (°C)": temp_min,
        "Lluvia (mm)": lluvia
    })
    st.dataframe(df_clima)
else:
    st.error("No se pudo obtener el pronóstico del clima.")

# Indicador de riesgo simplificado
st.subheader("Estado General de Riesgo")
riesgo_actual = df['estado'].value_counts().idxmax() if 'estado' in df.columns else "Desconocido"
st.markdown(f"**Nivel de riesgo predominante:** `{riesgo_actual}`")
if riesgo_actual == "Rojo":
    st.error("¡Alerta crítica! Evitar zonas cercanas a los ríos.")
elif riesgo_actual == "Amarillo":
    st.warning("Precaución, caudales en ascenso.")
else:
    st.success("Sin peligro inminente.")

# Noticias reales (placeholder con enlace a RPP)
st.subheader("Noticias Hidrometeorológicas del Perú")
noticias = {
    "Lluvias intensas afectan diversas regiones del Perú": "https://rpp.pe/peru/actualidad",
    "Advertencia del SENAMHI por desborde en río Marañón": "https://www.senamhi.gob.pe",
}
for titulo, enlace in noticias.items():
    st.markdown(f"- [{titulo}]({enlace})")

# Ranking de regiones
if 'caudal' in df.columns and 'region' in df.columns:
    st.subheader("Ranking de Regiones con Mayor Caudal")
    ranking = df.groupby("region")["caudal"].mean().sort_values(ascending=False).reset_index()
    ranking.columns = ["Región", "Caudal Promedio (m³/s)"]
    st.dataframe(ranking)

# Video informativo
st.subheader("Video Informativo")
st.video("https://youtu.be/zqsIIcbqomQ?si=wXxAZxSaeGNNK8YZ")
