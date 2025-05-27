import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import requests

st.set_page_config(page_title="HydroAlert Perú", layout="wide")

st.markdown("""
    <style>
        .main {
            background-color: #f4f6f9;
        }
        .title {
            color: #111;
            font-size: 32px;
            font-weight: bold;
        }
        .section {
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .alerta {
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">HydroAlert Perú – Monitoreo Inteligente</div>', unsafe_allow_html=True)

# Leer CSV directamente del directorio
@st.cache_data
def cargar_datos():
    return pd.read_csv("rios_peru_sample.csv")

df = cargar_datos()

# Validar columnas y limpieza básica
if 'region' not in df.columns:
    st.error("El archivo CSV no contiene la columna 'region'. Por favor revisa el archivo.")
    st.stop()

# Selección de región
region = st.selectbox("Selecciona una región para ver los datos hidrológicos:", df['region'].unique())

datos_region = df[df['region'] == region]

if not datos_region.empty:
    st.markdown(f"### Datos para la región: {region}")
    fig = px.line(datos_region, x='fecha', y='caudal', title=f'Caudal del río en {region}')
    st.plotly_chart(fig, use_container_width=True)

    caudal_actual = datos_region.iloc[-1]['caudal']
    estado = "VERDE" if caudal_actual < 20 else "AMARILLO" if caudal_actual < 40 else "ROJO"
    color_estado = {"VERDE": "#4CAF50", "AMARILLO": "#FFC107", "ROJO": "#F44336"}

    st.markdown(f"<div class='alerta' style='background-color: {color_estado[estado]};'>Estado actual del río: {estado}</div>", unsafe_allow_html=True)
else:
    st.warning("No hay datos para esta región.")

# Pronóstico del clima en Lima (Open-Meteo)
st.markdown("### Pronóstico del clima (Lima, Perú)")
try:
    clima = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude=-12.05&longitude=-77.05&hourly=temperature_2m,precipitation_probability&timezone=auto"
    ).json()
    temp = clima["hourly"]["temperature_2m"][0]
    lluvia = clima["hourly"]["precipitation_probability"][0]

    st.metric("Temperatura actual", f"{temp} °C")
    st.metric("Probabilidad de lluvia", f"{lluvia}%")
except Exception as e:
    st.error("Error al obtener el pronóstico del clima.")

# Embed de video funcional
st.markdown("### Video informativo")
st.video("https://youtu.be/zqsIIcbqomQ")

# Noticias desde Google News RSS
st.markdown("### Noticias recientes sobre agua y clima en Perú")

def obtener_noticias():
    try:
        import feedparser
        feed = feedparser.parse("https://news.google.com/rss/search?q=agua+clima+Perú")
        noticias = []
        for entry in feed.entries[:5]:
            noticias.append((entry.title, entry.link))
        return noticias
    except:
        return []

noticias = obtener_noticias()
if noticias:
    for titulo, enlace in noticias:
        st.markdown(f"- [{titulo}]({enlace})")
else:
    st.write("No se pudieron obtener noticias.")
