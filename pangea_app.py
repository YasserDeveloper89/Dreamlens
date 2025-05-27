import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PANGEA – Simulador de Políticas Públicas", layout="wide")

st.title("PANGEA – Simulador de Políticas Públicas")
st.markdown("Explora cómo ciertas decisiones afectan la economía, salud, seguridad y más en Perú.")

# Entrada
decision = st.text_input("Describe tu decisión:", "Aumentar el salario mínimo")
categoria = st.selectbox("Selecciona la categoría", ["Economica", "Transporte", "Salud", "Educacion", "Seguridad"])

# Simulador
def simular(categoria):
    np.random.seed(42)
    meses = np.arange(1, 13)

    if categoria == "Economica":
        return pd.DataFrame({
            "Mes": meses,
            "PIB (%)": 0.1 * meses + np.random.normal(0, 0.5, 12),
            "Empleo (x1000)": 50 + 2 * meses + np.random.normal(0, 5, 12),
            "Inflacion (%)": 0.05 * meses + np.random.normal(0, 0.2, 12)
        })

    elif categoria == "Transporte":
        return pd.DataFrame({
            "Mes": meses,
            "Trafico (%)": 100 - 3 * meses + np.random.normal(0, 4, 12),
            "Emisiones CO2": 50 - 2 * meses + np.random.normal(0, 3, 12)
        })

    elif categoria == "Salud":
        return pd.DataFrame({
            "Mes": meses,
            "Cobertura (%)": 60 + 2 * meses + np.random.normal(0, 3, 12),
            "Mortalidad (%)": 10 - 0.3 * meses + np.random.normal(0, 0.2, 12)
        })

    elif categoria == "Educacion":
        return pd.DataFrame({
            "Mes": meses,
            "Rendimiento (%)": 70 + 1.5 * meses + np.random.normal(0, 2, 12),
            "Abandono Escolar (%)": 10 - 0.5 * meses + np.random.normal(0, 0.5, 12)
        })

    else:
        return pd.DataFrame({
            "Mes": meses,
            "Crimen (%)": 80 - 2 * meses + np.random.normal(0, 3, 12),
            "Percepción Seguridad (%)": 30 + 2 * meses + np.random.normal(0, 4, 12)
        })

# Simular
data = simular(categoria)

# Mostrar tabla
st.subheader("Resultados simulados")
st.dataframe(data.set_index("Mes"))

# Mostrar gráfico
st.subheader("Gráfico del impacto")
st.line_chart(data.set_index("Mes"))
