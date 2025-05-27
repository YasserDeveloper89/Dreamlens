import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests

st.set_page_config(page_title="HydroAlert Perú – Versión PRO", layout="wide")

# Estilos
st.markdown("""
    <style>
    body { background-color: #f2f4f8; }
    .big-font { font-size:24px !important; }
    .video-container { display: flex; gap: 20px; flex-wrap: wrap; }
    iframe { border-radius: 10px; }
    .alert-box { border-radius: 10px; padding: 20px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("HydroAlert Perú – Monitoreo Inteligente de Ríos y Clima")

# Cargar datos de ríos
try:
    df = pd.read_csv("rios_peru_sample.csv")
    required_cols = {'rio', 'region', 'nivel', 'riesgo'}
    if not required_cols.issubset(set(df.columns)):
        st.error("El archivo CSV debe contener las columnas: rio, region, nivel, riesgo.")
    else:
        rios = df["rio"].unique().tolist()
        rio_seleccionado = st.selectbox("Selecciona un río", rios)

        datos_rio = df[df["rio"] == rio_seleccionado]
        nivel = datos_rio["nivel"].values[0]
        riesgo = datos_rio["riesgo"].values[0]
        region = datos_rio["region"].values[0]

        # Colores de riesgo
        color_dict = {
            "Alto": "red",
            "Medio": "orange",
            "Bajo": "green"
        }
        color_riesgo = color_dict.get(riesgo, "gray")

        st.markdown(f"""
            <div class="alert-box" style="background-color: {color_riesgo}; color: white;">
                <strong>{rio_seleccionado}</strong> ({region})<br>
                Nivel Actual: <strong>{nivel}</strong><br>
                Nivel de Riesgo: <strong>{riesgo}</strong>
            </div>
        """, unsafe_allow_html=True)

        # Gráfico
        fig = px.bar(df, x='rio', y='nivel', color='riesgo', title="Comparación de niveles de los ríos")
        st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("Archivo CSV no encontrado. Asegúrate de colocar 'rios_peru_sample.csv' en el mismo directorio.")

# Clima actual - Desactivado hasta ingresar API
st.subheader("Clima actual en Lima (modo demostración)")
st.info("Para activar el pronóstico real, agrega tu API key de OpenWeatherMap.")

# Noticias
st.subheader("Noticias recientes")
st.markdown("- [Lluvias intensas provocan desbordes en zonas del norte de Perú](https://elcomercio.pe)")
st.markdown("- [SENAMHI advierte incremento del caudal en ríos amazónicos](https://andina.pe)")
st.markdown("- [Plan de emergencia hídrica anunciado por el gobierno](https://gestion.pe)")

# Videos informativos
st.subheader("Videos informativos")
st.markdown('<div class="video-container">', unsafe_allow_html=True)
st.video("https://youtu.be/zqsIIcbqomQ?si=wXxAZxSaeGNNK8YZ")
st.video("https://youtu.be/BO-OepQkvEM?si=Roq8KAW5C-5G58AH")
st.video("https://youtu.be/5vm9PUMeJVo?si=dNrwoqcgVgFEtJmy")
st.markdown('</div>', unsafe_allow_html=True)

# Sugerencia de funciones futuras
st.markdown("### Próximas funciones Pro:")
st.markdown("""
- Alertas por WhatsApp cuando un río supere niveles críticos.
- Mapa en tiempo real de estaciones meteorológicas.
- Historial interactivo de caudales.
- Detector de anomalías climáticas con IA.
""")
