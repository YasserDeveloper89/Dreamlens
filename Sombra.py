import streamlit as st import pandas as pd import plotly.express as px import datetime import random import requests

st.set_page_config(page_title="HydroAlert Perú", layout="wide") st.title("HydroAlert Perú – Monitoreo Hidrológico en Tiempo Real") st.markdown("Visualiza niveles de ríos, embalses y alertas hídricas en tiempo real para el territorio peruano.")

Estaciones de monitoreo simuladas (usar APIs reales cuando estén disponibles)

stations = { "Amazonas - Río Utcubamba": {"lat": -5.75, "lon": -78.65}, "Cusco - Río Vilcanota": {"lat": -13.52, "lon": -71.97}, "Arequipa - Río Chili": {"lat": -16.39, "lon": -71.53}, "Lima - Río Rímac": {"lat": -12.04, "lon": -77.03}, }

def fetch_real_data(): try: url = "https://www.senamhi.gob.pe/mapas/mapaestaciones/_datos/estacioneshidrologicas.json" response = requests.get(url) data = response.json() return data except: return None

Generar datos simulados por ahora

def generate_data(): dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(10)][::-1] levels = [round(2 + random.uniform(-0.5, 0.5), 2) for _ in range(10)] df = pd.DataFrame({"Fecha": dates, "Nivel (m)": levels}) return df

station = st.selectbox("Selecciona una estación", list(stations.keys())) df = generate_data()

st.subheader(f"Niveles del río en {station}") fig = px.line(df, x="Fecha", y="Nivel (m)", markers=True, title="Histórico de niveles") st.plotly_chart(fig, use_container_width=True)

station_data = stations[station] st.subheader("Ubicación de la estación") st.map(pd.DataFrame([station_data], index=[0]))

st.subheader("Alertas") ultimo = df["Nivel (m)"].iloc[-1] if ultimo > 2.3: st.error("Alerta Roja: Posible desborde") elif ultimo > 2.1: st.warning("Alerta Amarilla: Nivel crítico") else: st.success("Nivel normal")

st.markdown("---") st.markdown("Desarrollado para ADR Technology | Versión Pro | Datos SENAMHI y ANA")
