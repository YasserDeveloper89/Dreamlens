HydroAlert Perú - Versión Premium PRO

import streamlit as st import pandas as pd import requests import plotly.express as px from datetime import datetime

--- Estilo Profesional ---

st.set_page_config(page_title="HydroAlert Perú", layout="wide")

--- Estilo visual con CSS personalizado ---

st.markdown(""" <style> body { background-color: #111; color: white; } .stApp { background-color: #1e1e1e; } .big-font { font-size:24px !important; font-weight:bold; color: #00f5d4; } .video-title { font-size:18px !important; margin-top: 10px; } </style> """, unsafe_allow_html=True)

--- Carga de datos CSV (en mismo directorio) ---

try: df = pd.read_csv("rios_peru_sample.csv") except Exception as e: st.error("Error al cargar el CSV: " + str(e)) st.stop()

--- Barra lateral de selección ---

st.sidebar.title("Opciones") rio_seleccionado = st.sidebar.selectbox("Selecciona un río:", df["rio"].unique())

--- Filtrado de datos ---

df_rio = df[df["rio"] == rio_seleccionado]

--- Título Principal ---

st.title("HydroAlert Perú - Monitoreo Inteligente") st.markdown(f"### Río seleccionado: {rio_seleccionado}")

--- Nivel actual del río ---

ultimo_valor = df_rio.iloc[-1] nivel = ultimo_valor["nivel"]

if nivel < 2: alerta = "Verde" color_alerta = "#00ff00" elif nivel < 3.5: alerta = "Amarillo" color_alerta = "#ffff00" else: alerta = "Rojo" color_alerta = "#ff0000"

st.markdown(f"Nivel actual: {nivel} m") st.markdown(f"<div style='padding:10px;background-color:{color_alerta};border-radius:10px;'> <span class='big-font'>Alerta: {alerta}</span></div>", unsafe_allow_html=True)

--- Gráfico de nivel del río ---

fig = px.line(df_rio, x="fecha", y="nivel", title=f"Historial del Río {rio_seleccionado}", labels={"fecha": "Fecha", "nivel": "Nivel (m)"}) st.plotly_chart(fig, use_container_width=True)

--- Pronóstico del tiempo actual ---

st.subheader("Clima Actual en Lima") try: clima = requests.get("https://api.open-meteo.com/v1/forecast?latitude=-12.04&longitude=-77.03&current=temperature_2m,precipitation,weathercode&timezone=auto").json() temp = clima['current']['temperature_2m'] lluvias = clima['current']['precipitation'] st.markdown(f"Temperatura actual: {temp} °C") st.markdown(f"Precipitación: {lluvias} mm/h") except: st.warning("No se pudo cargar el pronóstico del clima en tiempo real.")

--- Noticias Actualizadas ---

st.subheader("Noticias Recientes sobre Ríos y Clima") try: noticias = requests.get("https://www.peru21.pe/arcio/rss/peru21.xml") if noticias.status_code == 200: from xml.etree import ElementTree root = ElementTree.fromstring(noticias.text) for item in root.findall(".//item")[:5]: title = item.find("title").text link = item.find("link").text st.markdown(f"- {title}") except: st.warning("No se pudieron cargar las noticias.")

--- Videos Educativos (YouTube verificados) ---

st.subheader("Videos Informativos") video_urls = [ "https://www.youtube.com/watch?v=zqsIIcbqomQ", "https://www.youtube.com/watch?v=UY2Dvlq1xQk", "https://www.youtube.com/watch?v=v5LZqIjhDEY", "https://www.youtube.com/watch?v=lOlUAPfJXrQ", "https://www.youtube.com/watch?v=mtqQ3XwDH-Q", "https://www.youtube.com/watch?v=dUUlSgoaI8o" ]

for url in video_urls: st.video(url)

--- Pie de página ---

st.markdown("---") st.markdown("Aplicación desarrollada para monitoreo y prevención hidrometeorológica en Perú. Datos actualizados y visuales en tiempo real.")

