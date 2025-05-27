app.py

import streamlit as st import pandas as pd import plotly.express as px import requests from datetime import datetime import folium from streamlit_folium import folium_static

st.set_page_config(page_title="HydroAlert Perú Premium PRO", layout="wide") st.title("HydroAlert Perú – Monitoreo Inteligente")

Cargar datos de ríos

def cargar_datos(): try: df = pd.read_csv("rios_peru.csv") columnas_necesarias = {"rio", "region", "nivel", "riesgo", "lat", "lon"} if not columnas_necesarias.issubset(set(df.columns)): st.error("El archivo CSV debe contener las columnas: rio, region, nivel, riesgo, lat, lon") return None return df except FileNotFoundError: st.error("Archivo rios_peru.csv no encontrado") return None

df = cargar_datos()

if df is not None: regiones = df['region'].unique().tolist() region_seleccionada = st.selectbox("Selecciona la región:", regiones) df_region = df[df['region'] == region_seleccionada]

rio_seleccionado = st.selectbox("Selecciona el río:", df_region['rio'].unique())
datos_rio = df_region[df_region['rio'] == rio_seleccionado].iloc[0]

st.subheader(f"Estado actual del Río {rio_seleccionado} - {region_seleccionada}")
nivel = datos_rio['nivel']
riesgo = datos_rio['riesgo']

color = "green" if riesgo == "Bajo" else "orange" if riesgo == "Medio" else "red"
st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:8px'>"
            f"<h4 style='color:white;'>Nivel: {nivel} m / Riesgo: {riesgo}</h4></div>", unsafe_allow_html=True)

# Gráfico comparativo de niveles
fig = px.bar(df_region, x='rio', y='nivel', color='riesgo',
             color_discrete_map={'Bajo': 'green', 'Medio': 'orange', 'Alto': 'red'},
             title="Comparación de niveles de ríos en la región")
st.plotly_chart(fig, use_container_width=True)

# Mapa interactivo con predicción simple
st.subheader("Mapa de estaciones y predicción")
mapa = folium.Map(location=[-9.19, -75.02], zoom_start=6)

for i, row in df.iterrows():
    riesgo_color = 'green' if row['riesgo'] == 'Bajo' else 'orange' if row['riesgo'] == 'Medio' else 'red'
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        color=riesgo_color,
        fill=True,
        popup=f"{row['rio']} - Riesgo: {row['riesgo']}"
    ).add_to(mapa)

folium_static(mapa)

# Videos de YouTube funcionales
st.subheader("Videos informativos")
videos = [
    "https://www.youtube.com/embed/zqsIIcbqomQ",
    "https://www.youtube.com/embed/xoUhNu0Jn94",
    "https://www.youtube.com/embed/BO-OepQkvEM",
    "https://www.youtube.com/embed/5vm9PUMeJVo",
    "https://www.youtube.com/embed/QfTx3jUtaVQ"
]
for v in videos:
    st.video(v)

# Noticias diarias (placeholder real)
st.subheader("Noticias relevantes")
noticias = [
    ("SENAMHI alerta lluvias en la sierra sur", "https://www.senamhi.gob.pe/"),
    ("Previsión hidrológica actualizada para la costa", "https://www.senamhi.gob.pe/?p=boletin-hidrologico")
]
for titulo, enlace in noticias:
    st.markdown(f"- [{titulo}]({enlace})")

# Pronóstico del clima actual en Lima
st.subheader("Clima actual en Lima")
clima = requests.get("https://api.open-meteo.com/v1/forecast?latitude=-12.04&longitude=-77.03&current_weather=true")
if clima.ok:
    data_clima = clima.json()["current_weather"]
    st.write(f"Temperatura: {data_clima['temperature']} °C")
    st.write(f"Viento: {data_clima['windspeed']} km/h")
    st.write(f"Estado: {data_clima['weathercode']}")
else:
    st.warning("No se pudo obtener el clima actual.")

# Historial (simulado, se puede conectar a base de datos futura)
st.subheader("Historial del Río (simulado)")
historial = pd.DataFrame({
    "fecha": pd.date_range(end=datetime.today(), periods=7),
    "nivel": [nivel - 0.2, nivel - 0.1, nivel, nivel + 0.1, nivel - 0.3, nivel, nivel + 0.2]
})
st.line_chart(historial.set_index("fecha"))

