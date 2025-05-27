
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="HydroAlert Perú", layout="wide", initial_sidebar_state="expanded")
st.markdown("<h1 style='color:#4db8ff'>HydroAlert Perú – Monitoreo Inteligente de Ríos y Clima</h1>", unsafe_allow_html=True)

# Función para obtener datos reales del SENAMHI (simulado)
def obtener_datos_hidrologicos():
    try:
        response = requests.get("https://api.senamhi.gob.pe/v1/hidrologia")  # Esta URL es simulada
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            return pd.read_csv("data/rios_peru_sample.csv")  # fallback local
    except:
        return pd.read_csv("data/rios_peru_sample.csv")

# Cargar datos
df = obtener_datos_hidrologicos()
df["nivel_m"] = pd.to_numeric(df["nivel_m"], errors="coerce")
df = df.dropna(subset=["nivel_m"])

# Filtros
departamento = st.sidebar.selectbox("Selecciona un departamento", df["departamento"].unique())
df_dep = df[df["departamento"] == departamento]

# Gráfico
fig = px.line(df_dep, x="fecha", y="nivel_m", color="estacion", title=f"Niveles de Ríos en {departamento}")
st.plotly_chart(fig, use_container_width=True)

# Mapa
st.subheader("Ubicación de Estaciones Hidrológicas")
mapa = px.scatter_mapbox(df_dep, lat="lat", lon="lon", color="nivel_m", size="nivel_m",
                         hover_name="estacion", zoom=5, height=500,
                         color_continuous_scale="Jet")
mapa.update_layout(mapbox_style="open-street-map")
st.plotly_chart(mapa, use_container_width=True)

# Noticias RSS
st.subheader("Noticias Relevantes")
try:
    import feedparser
    feed = feedparser.parse("https://news.google.com/rss/search?q=lluvias+peru+desbordes&hl=es-419&gl=PE&ceid=PE:es-419")
    for entry in feed.entries[:5]:
        st.markdown(f"**[{entry.title}]({entry.link})**")
except:
    st.write("No se pudieron cargar noticias.")

# Video embebido
st.subheader("Contenido Visual Relevante")
st.video("https://www.youtube.com/watch?v=7DgW49NnL9c")
