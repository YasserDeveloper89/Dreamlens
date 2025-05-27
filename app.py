import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

st.set_page_config(page_title="HydroAlert Perú", layout="wide")

st.markdown("<h1 style='color:#0A5D5E'>HydroAlert Perú – Monitoreo Inteligente</h1>", unsafe_allow_html=True)

# Cargar datos hidrológicos desde el mismo directorio
@st.cache_data
def obtener_datos_hidrologicos():
    return pd.read_csv("rios_peru_sample.csv")

df = obtener_datos_hidrologicos()

# Selección por río y región
region = st.selectbox("Selecciona una región:", sorted(df["region"].unique()))
ríos = df[df["region"] == region]["rio"].unique()
río = st.selectbox("Selecciona un río:", sorted(ríos))

datos_río = df[(df["region"] == region) & (df["rio"] == río)]

st.subheader(f"Estado actual del río {río}")
estado = datos_río["estado"].values[0]
color_estado = {"VERDE": "green", "AMARILLO": "orange", "ROJO": "red"}
st.markdown(f"<h3 style='color:{color_estado.get(estado, 'gray')}'>Estado: {estado}</h3>", unsafe_allow_html=True)

# Gráfico interactivo de caudal
fig = px.line(datos_río, x="fecha", y="nivel_caudal", title=f"Nivel de caudal del río {río} (histórico)")
st.plotly_chart(fig, use_container_width=True)

# Clima actual por ciudad
st.subheader("Clima actual en Perú")
ciudades = ["Lima", "Cusco", "Arequipa", "Piura"]
ciudad = st.selectbox("Selecciona una ciudad:", ciudades)

def obtener_clima(ciudad):
    api_key = "6cbcbfddda724bcdbd114711241305"  # demo key de WeatherAPI
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={ciudad}&lang=es"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        data = respuesta.json()
        return {
            "temp_c": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "icon": "https:" + data["current"]["condition"]["icon"]
        }
    return None

clima = obtener_clima(ciudad)
if clima:
    st.markdown(f"**{ciudad}**: {clima['temp_c']}°C – {clima['condition']}")
    st.image(clima["icon"], width=50)

# Noticias reales (con enlaces)
st.subheader("Noticias recientes sobre hidrología y clima en Perú")
noticias = [
    {
        "titulo": "SENAMHI alerta aumento de caudales en la región Loreto",
        "url": "https://www.senamhi.gob.pe/?p=avisos"
    },
    {
        "titulo": "Estudio revela cambios drásticos en el caudal del río Rímac",
        "url": "https://andina.pe/agencia/noticia-senamhi-rio-rimac"
    }
]
for noticia in noticias:
    st.markdown(f"- [{noticia['titulo']}]({noticia['url']})")

# Video informativo funcional
st.subheader("Video informativo sobre riesgo hídrico")
st.video("https://youtu.be/zqsIIcbqomQ?si=wXxAZxSaeGNNK8YZ")
