import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import requests
from bs4 import BeautifulSoup

# Estilo moderno tipo Tesla/corporativo
st.set_page_config(layout="wide", page_title="HydroAlert Perú", page_icon="🌊")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('''
<div class='header'>
    <h1>HydroAlert Perú</h1>
    <p>Monitoreo inteligente de ríos, clima extremo y noticias peruanas en tiempo real.</p>
</div>
''', unsafe_allow_html=True)

# Datos simulados
datos = {
    "Departamento": ["Lima", "Cusco", "Loreto", "Arequipa"],
    "Lat": [-12.0464, -13.5319, -3.7491, -16.4090],
    "Lon": [-77.0428, -71.9675, -73.2538, -71.5375],
    "Nivel Río": [1.5, 2.1, 3.8, 1.2],
    "Alerta": ["Verde", "Amarilla", "Roja", "Verde"]
}
df = pd.DataFrame(datos)

st.subheader("Mapa de Monitoreo de Ríos")
fig = px.scatter_mapbox(
    df, lat="Lat", lon="Lon", color="Alerta", size="Nivel Río",
    hover_name="Departamento", zoom=4, height=500, mapbox_style="carto-positron"
)
st.plotly_chart(fig, use_container_width=True)

# Video
st.subheader("Video informativo")
st.video("https://www.youtube.com/watch?v=dViE9bd-7Xc")

# Noticias reales
st.subheader("Últimas noticias desde RPP.pe")
try:
    url = 'https://rpp.pe/peru'
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.content, "html.parser")
    noticias = soup.find_all("h3")[:5]
    for n in noticias:
        st.markdown(f"<div class='news'>• {n.get_text(strip=True)}</div>", unsafe_allow_html=True)
except:
    st.warning("No se pudieron cargar noticias reales.")

# Tendencia de caudal
st.subheader("Tendencia de caudal (simulado)")
fecha = pd.date_range(end=datetime.datetime.today(), periods=30)
caudal = pd.Series([round(1.5 + 0.3*i + (i%5)*0.5, 2) for i in range(30)])
trend_df = pd.DataFrame({"Fecha": fecha, "Caudal (m³/s)": caudal})

fig_linea = px.line(trend_df, x="Fecha", y="Caudal (m³/s)", title="Tendencia de caudal diario")
st.plotly_chart(fig_linea, use_container_width=True)
