import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

st.set_page_config(page_title="HydroAlert Perú", layout="wide")

# Estilos personalizados
st.markdown('''
    <style>
    .main {
        background-color: #f4f4f4;
        color: #333;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #0a3d62;
    }
    .stButton>button {
        background-color: #079992;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    </style>
''', unsafe_allow_html=True)

st.title("HydroAlert Perú – Monitoreo Inteligente")

# Cargar datos simulados de ríos
df = pd.read_csv("rios_peru_sample.csv")

# Mostrar alerta basada en nivel
nivel_actual = df['nivel'].iloc[-1]
alerta = "verde" if nivel_actual < 3 else "amarillo" if nivel_actual < 5 else "rojo"
color_alerta = {"verde": "green", "amarillo": "orange", "rojo": "red"}[alerta]

st.markdown(f"<h2>Estado del río: <span style='color:{color_alerta}'>{alerta.upper()}</span></h2>", unsafe_allow_html=True)

# Gráfico del nivel del río
fig = px.line(df, x='fecha', y='nivel', title='Nivel del río en los últimos días')
st.plotly_chart(fig, use_container_width=True)

# Clima en tiempo real
st.subheader("Clima actual en Lima, Perú")
weather = requests.get("https://wttr.in/Lima?format=3").text
st.info(weather)

# Noticias
st.subheader("Noticias recientes sobre clima e infraestructura hídrica")
st.markdown('''
- [Senamhi advierte lluvias intensas](https://www.senamhi.gob.pe)
- [Proyecto de represas en la selva](https://andina.pe)
- [Medidas ante crecidas del río](https://gestion.pe)
''')

# Video informativo
st.subheader("Video informativo")
st.video("https://youtu.be/zqsIIcbqomQ?si=4vzl7p9Mt8YAuJcZ")
