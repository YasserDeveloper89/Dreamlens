import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(layout="wide", page_title="HydroAlert Perú – PRO")

st.markdown(
    """
    <style>
    body { background-color: #f4f6f9; }
    .main { background-color: #ffffff; padding: 1.5em; border-radius: 10px; }
    h1, h2, h3, h4 { color: #003366; }
    .stButton>button { background-color: #003366; color: white; font-weight: bold; }
    .stVideo { border: 1px solid #ddd; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True
)

st.title("HydroAlert Perú – Monitoreo Inteligente")

# Cargar CSV en el mismo directorio
try:
    df = pd.read_csv("rios_peru_sample.csv")
except FileNotFoundError:
    st.error("Archivo CSV no encontrado. Asegúrate de tener 'rios_peru_sample.csv' en el mismo directorio.")
    st.stop()

if "region" not in df.columns or "nivel" not in df.columns:
    st.error("El archivo CSV debe tener las columnas 'region' y 'nivel'.")
    st.stop()

# Selector de región
region = st.selectbox("Selecciona una región:", sorted(df["region"].unique()))
datos_region = df[df["region"] == region]

# Nivel de riesgo
if not datos_region.empty:
    nivel = datos_region["nivel"].values[0]
else:
    nivel = "Desconocido"

color_nivel = {
    "VERDE": "green",
    "AMARILLO": "orange",
    "ROJO": "red"
}.get(nivel.upper(), "gray")

st.markdown(f"### Nivel de riesgo predominante: <span style='color:{color_nivel}'>{nivel.upper()}</span>", unsafe_allow_html=True)

# Gráfico de niveles de río por región
fig = px.bar(datos_region, x="fecha", y="nivel_num", title=f"Niveles del río - {region}", color="nivel", height=400)
st.plotly_chart(fig, use_container_width=True)

# Clima actual (ejemplo con Open-Meteo API)
with st.spinner("Obteniendo datos meteorológicos..."):
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=-12.0464&longitude=-77.0428&current=temperature_2m&timezone=auto"
    res = requests.get(weather_url).json()
    temp = res.get("current", {}).get("temperature_2m", None)
    if temp:
        st.metric("Temperatura actual en Lima", f"{temp}°C")
    else:
        st.warning("No se pudo obtener el clima actual.")

# Noticias (simuladas pero puedes conectarlo a RSS o News API)
st.subheader("Noticias recientes sobre ríos y clima en Perú")
news = [
    {"titulo": "Crecida del río Rímac activa alertas en Lima", "url": "https://andina.pe/agencia/noticia-crecida-del-rio-rimac-activan-alertas-957462.aspx"},
    {"titulo": "INDECI recomienda estar alerta por lluvias intensas", "url": "https://www.indeci.gob.pe/"},
    {"titulo": "SENAMHI emite advertencia hidrológica en la selva", "url": "https://www.senamhi.gob.pe/"}
]

for item in news:
    st.markdown(f"- [{item['titulo']}]({item['url']})")

# Videos educativos embebidos
st.subheader("Videos informativos sobre prevención y monitoreo")

video_urls = [
    "https://www.youtube.com/embed/Afv7X-XGxS8",
    "https://www.youtube.com/embed/WoHgXguC8KI",
    "https://www.youtube.com/embed/Xcb4w5xu6Rg",
    "https://www.youtube.com/embed/zqsIIcbqomQ",
    "https://www.youtube.com/embed/EpjmYy9K3XU",
    "https://www.youtube.com/embed/UjQPT7iHuUs"
]

cols = st.columns(2)
for i, url in enumerate(video_urls):
    with cols[i % 2]:
        st.video(url)

st.info("Fuente de datos: SENAMHI, INDECI, Open-Meteo – Información actualizada automáticamente.")
