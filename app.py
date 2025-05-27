import streamlit as st import pandas as pd import plotly.express as px import requests from datetime import datetime

Título principal

st.set_page_config(page_title="HydroAlert Perú PRO", layout="wide") st.markdown(""" <style> body { background-color: #f2f2f2; color: #1c1c1c; } .main-title { font-size: 3em; font-weight: bold; color: #0a3d62; } .section { padding: 1em; background-color: white; border-radius: 10px; box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); margin-bottom: 1em; } </style> """, unsafe_allow_html=True)

st.markdown("<div class='main-title'>HydroAlert Perú – Monitoreo Inteligente</div>", unsafe_allow_html=True)

Leer CSV sin carpeta 'data/'

try: df = pd.read_csv("rios_peru_sample.csv") if 'region' not in df.columns: st.error("El archivo CSV no contiene la columna 'region'. Por favor revisa el archivo.") else: regiones = df['region'].unique().tolist() region_seleccionada = st.selectbox("Selecciona una región para ver los datos hidrológicos:", regiones)

df_region = df[df['region'] == region_seleccionada]

    st.subheader(f"Nivel actual de ríos en {region_seleccionada}")
    fig = px.bar(df_region, x='rio', y='nivel', color='riesgo',
                 color_discrete_map={
                     'Bajo': 'green',
                     'Medio': 'orange',
                     'Alto': 'red'
                 },
                 labels={'nivel': 'Nivel del río (m)'})
    st.plotly_chart(fig)

    riesgo_predominante = df_region['riesgo'].mode()[0] if not df_region['riesgo'].mode().empty else "Desconocido"
    st.info(f"Nivel de riesgo predominante: {riesgo_predominante}")

except FileNotFoundError: st.error("No se encontró el archivo rios_peru_sample.csv. Asegúrate de que esté en el mismo directorio que este script.")

Clima actual para Lima

st.subheader("Clima Actual en Lima") API_KEY = "TU_API_KEY_AQUI"  # Reemplaza por tu clave de OpenWeather url = f"https://api.openweathermap.org/data/2.5/weather?q=Lima,pe&units=metric&appid={API_KEY}" try: response = requests.get(url).json() temp = response['main']['temp'] desc = response['weather'][0]['description'] st.success(f"Temperatura: {temp}°C - Condición: {desc.capitalize()}") except: st.error("No se pudo obtener la información del clima.")

Videos informativos

st.subheader("Videos Educativos sobre Seguridad Hídrica") video_urls = [ "https://youtu.be/zqsIIcbqomQ", "https://youtu.be/1t0KsbZzO9Q", "https://youtu.be/WZhxZcgIt2U", "https://youtu.be/B0gXgLke1nk", "https://youtu.be/Kb1ZKCPzTe8" ] for url in video_urls: st.video(url)

Noticias

st.subheader("Últimas Noticias Hidrológicas en Perú") noticias = [ ("Prevención de desbordes en el río Rímac avanza con nuevas obras", "https://www.andina.pe/agencia/noticia-prevencion-desbordes-rio-rimac-avanza-nuevas-obras-894587.aspx"), ("Senamhi advierte posibles lluvias en zonas altas de la selva", "https://rpp.pe/peru/actualidad/senamhi-advierte-posibles-lluvias-en-la-selva-noticia-1322103") ] for titulo, enlace in noticias: st.markdown(f"- {titulo}")

Información histórica y pronóstico

st.subheader("Explora Datos Históricos") fecha_inicio = st.date_input("Desde:", datetime(2023, 1, 1)) fecha_fin = st.date_input("Hasta:", datetime(2023, 12, 31)) if fecha_inicio > fecha_fin: st.warning("La fecha de inicio no puede ser posterior a la fecha de fin.") else: st.success("Fechas seleccionadas correctamente. En el futuro puedes vincular esta selección a gráficos históricos si los tienes disponibles.")

