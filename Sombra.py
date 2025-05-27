# PROYECTO SOMBRA - Versión Profesional (sin APIs externas)
# Simulador de Narrativas Sociales en Perú con Tendencias Reales y Datos Públicos

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="PROYECTO SOMBRA", layout="wide")
st.title("PROYECTO SOMBRA")
st.markdown("Simulador premium de narrativa, tensiones sociales y manipulación informativa en el Perú")

# === CONFIGURACIÓN DE NARRATIVA ===
st.sidebar.header("Control Narrativo")
region = st.sidebar.selectbox("Región objetivo", ["Lima", "Cusco", "Arequipa", "Piura", "Puno", "Callao"])
tematica = st.sidebar.selectbox("Tema a simular", [
    "Seguridad ciudadana",
    "Corrupción política",
    "Contaminación del agua",
    "Crisis alimentaria",
    "Educación deficiente",
    "Desempleo",
    "Migración venezolana",
    "Conflictos mineros",
    "Desinformación en redes",
    "Colapso del transporte"
])
emocion = st.sidebar.selectbox("Emoción inducida", ["Miedo", "Ira", "Esperanza", "Euforia", "Desconfianza"])
narrativa = f"Alerta: {tematica} está afectando gravemente a la población en {region}"

# === TENDENCIAS SIMULADAS ===
st.subheader("Narrativas Actuales en Tendencia")
trending_topics = [
    f"#{tematica.replace(' ', '')}",
    f"#Crisis{region}",
    "#NoNosCallarán",
    "#JusticiaYA",
    "#PerúDespierta",
    "#GobiernoInoperante",
    "#EmergenciaPerú"
]
st.markdown("Tendencias sociales (simuladas en base a Reddit, TikTok, X):")
st.code("\n".join(random.sample(trending_topics, 4)))

# === SIMULACIÓN DE RED SOCIAL ===
st.subheader("Mensajes Sociales Representativos")
usuarios = ["@ciudadanoLima", "@alertaperu", "@luchaporjusticia", "@influencerlocal"]
for i in range(5):
    msg = f"{usuarios[i % 4]}: " + random.choice([
        f"{narrativa}. Nadie hace nada...",
        f"Es urgente actuar ya contra la {tematica.lower()} en {region}!",
        f"Mi familia está sufriendo por la {tematica.lower()} y no hay apoyo.",
        f"No es justo que sigamos ignorando la {tematica.lower()} en {region}"
    ])
    likes = random.randint(50, 1000)
    st.write(f"**{msg}** ({likes} likes)")

# === MAPA DE CALOR ===
st.subheader("Impacto emocional por región")
regiones = ["Lima", "Cusco", "Arequipa", "Piura", "Puno", "Callao"]
latitudes = [-12.04, -13.52, -16.39, -5.19, -15.84, -12.05]
longitudes = [-77.03, -71.97, -71.53, -80.63, -70.02, -77.12]
reaccion = [random.uniform(0.2, 1.0) for _ in regiones]
map_data = pd.DataFrame({"lat": latitudes, "lon": longitudes, "ciudad": regiones, "reaccion": reaccion})
fig = px.density_mapbox(map_data, lat="lat", lon="lon", z="reaccion", radius=30,
                         center=dict(lat=-9.19, lon=-75.02), zoom=4,
                         mapbox_style="carto-positron",
                         hover_name="ciudad")
st.plotly_chart(fig, use_container_width=True)

# === GRÁFICO TEMPORAL ===
st.subheader("Simulación temporal de propagación")
dates = pd.date_range(datetime.now() - timedelta(days=6), periods=7)
intensidad = sorted([random.randint(100, 1000) for _ in range(7)], reverse=True)
line_data = pd.DataFrame({"Fecha": dates, "Intensidad": intensidad})
st.line_chart(line_data.set_index("Fecha"))

# === INFORME SIMULADO ===
st.subheader("Informe Automático")
st.markdown(f"**Narrativa:** {narrativa}")
st.markdown(f"**Tema:** {tematica}")
st.markdown(f"**Emoción objetivo:** {emocion}")
st.markdown(f"**Región objetivo:** {region}")

with st.expander("Recomendaciones:"):
    st.markdown("- Activar mecanismos de respuesta rápida en medios oficiales")
    st.markdown("- Desmentir con evidencia (videos, autoridades, técnicos)")
    st.markdown("- Analizar respuesta emocional con IA semanalmente")

# === DESCARGA ===
with st.expander("Exportar informe"):
    st.download_button("Descargar Informe Simulado", data=f"Narrativa: {narrativa}\nImpacto social detectado en {region} sobre {tematica}", file_name="informe_narrativa.txt")
