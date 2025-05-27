import streamlit as st import pandas as pd import plotly.express as px import requests from datetime import datetime

st.set_page_config(layout="wide") st.title("HydroAlert Perú – Monitoreo Inteligente de Ríos y Clima")

Leer datos actualizados desde archivo CSV local (debe estar en el mismo directorio que este archivo)

try: df = pd.read_csv("rios_peru_sample.csv") if 'rio' not in df.columns or 'region' not in df.columns or 'nivel' not in df.columns or 'riesgo' not in df.columns: st.error("El archivo CSV debe tener las columnas: rio, region, nivel, riesgo") st.stop() except FileNotFoundError: st.error("Archivo CSV no encontrado. Asegúrate de que 'rios_peru_sample.csv' esté en el mismo directorio.") st.stop()

Lista de ríos únicos disponibles

df["rio"] = df["rio"].str.strip() rios_disponibles = df["rio"].unique().tolist()

Selección del río

rio_seleccionado = st.selectbox("Selecciona un río para ver su estado actual:", rios_disponibles) datos_rio = df[df["rio"] == rio_seleccionado]

Mostrar gráfica de nivel del río

fig = px.bar( datos_rio, x="region", y="nivel", color="riesgo", color_discrete_map={ "Alto": "red", "Medio": "orange", "Bajo": "green", "Desconocido": "gray" }, labels={"nivel": "Nivel del río (m)", "region": "Región"}, title=f"Niveles del río {rio_seleccionado} por región" ) st.plotly_chart(fig, use_container_width=True)

Mostrar nivel de riesgo predominante

riesgo_predominante = datos_rio["riesgo"].mode()[0] if not datos_rio.empty else "Desconocido" st.markdown(f"## Nivel de riesgo predominante: {riesgo_predominante}")

Obtener pronóstico del clima actual (ejemplo: Lima)

st.subheader("Pronóstico del tiempo actual") API_KEY = "TU_API_KEY_OPENWEATHERMAP" ciudad = "Lima,PE" url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"

try: clima_data = requests.get(url).json() temp = clima_data['main']['temp'] descripcion = clima_data['weather'][0]['description'] humedad = clima_data['main']['humidity'] viento = clima_data['wind']['speed']

st.metric("Temperatura (°C)", temp)
st.metric("Humedad (%)", humedad)
st.metric("Viento (m/s)", viento)
st.markdown(f"**Descripción**: {descripcion.capitalize()}")

except: st.warning("No se pudo obtener información climática en tiempo real.")

Sección de vídeos informativos funcionales

st.subheader("Videos educativos y de prevención") videos = [ "https://www.youtube.com/embed/zqsIIcbqomQ", "https://www.youtube.com/embed/xoUhNu0Jn94", "https://www.youtube.com/embed/HEN8Uh4IC3M", "https://www.youtube.com/embed/duBeDcLBtCA", "https://www.youtube.com/embed/5_zQhKoxWQA" ]

cols = st.columns(3) for i, url in enumerate(videos): with cols[i % 3]: st.components.v1.iframe(url, height=200)

Noticias relacionadas (simulación con enlaces)

st.subheader("Noticias recientes sobre hidrología y clima") noticias = [ ("SENAMHI alerta sobre crecida de ríos en la costa peruana", "https://www.senamhi.gob.pe/?p=aviso&id=123"), ("Precipitaciones inusuales activan planes de emergencia en Lima", "https://andina.pe/Agencia/noticia-precipitaciones-lima-alerta"), ("Recomendaciones para prevención ante desbordes de ríos", "https://www.gob.pe/institucion/indeci/noticias/"), ("Río Chillón alcanza su nivel más alto en una década", "https://elcomercio.pe/lima/rio-chillon-alto-nivel") ]

for titulo, enlace in noticias: st.markdown(f"- {titulo}")

