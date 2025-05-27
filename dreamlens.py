import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar la clave de API desde .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="DreamLens", layout="centered", page_icon="💤")
st.title("🌙 DreamLens")
st.subheader("Cuenta tu sueño. Visualiza lo que tu mente imaginó mientras dormías.")

with st.expander("¿Cómo funciona?"):
    st.markdown("""
    1. Escribe tu sueño con tantos detalles como puedas.
    2. DreamLens lo interpreta simbólicamente.
    3. Se genera una mini historia.
    4. Se crean imágenes realistas según tu descripción.
    """)

dream_input = st.text_area("¿Qué soñaste anoche?", height=250, placeholder="Ej: Estaba en un bosque donde los árboles hablaban...")

if st.button("Interpretar y Visualizar"):
    if not dream_input.strip():
        st.warning("Por favor, escribe tu sueño.")
    else:
        with st.spinner("Analizando tu mundo onírico..."):

            # Interpretación simbólica
            interp_prompt = f"""
Actúa como un analista de sueños profesional con enfoque junguiano.
Interpreta este sueño simbólicamente y explica qué podría significar:

Sueño: {dream_input}
"""
            interp_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": interp_prompt}],
                temperature=0.7
            )
            interpretation = interp_response.choices[0].message.content

            # Historia literaria
            story_prompt = f"""
Convierte este sueño en una breve historia literaria onírica y poética (máximo 3 párrafos):

{dream_input}
"""
            story_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": story_prompt}],
                temperature=0.9
            )
            story = story_response.choices[0].message.content

            # Imagen realista del sueño
            image_prompt = f"Una escena realista y onírica basada en este sueño: {dream_input}"
            image_response = client.images.generate(
                prompt=image_prompt,
                n=1,
                size="512x512"
            )
            image_url = image_response.data[0].url

        # Mostrar resultados
        st.success("¡Sueño interpretado!")
        st.markdown("### Interpretación simbólica:")
        st.markdown(interpretation)

        st.markdown("### Historia onírica:")
        st.markdown(story)

        st.markdown("### Visualización del sueño:")
        st.image(image_url, caption="Representación visual de tu sueño", use_column_width=True)

        st.markdown("---")
        st.markdown("¿Quieres volver a soñar?")
