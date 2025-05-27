import streamlit as st
from openai import OpenAI

# Obtener clave desde Streamlit Secrets
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Configuración de la página (sin emojis para evitar errores Unicode)
st.set_page_config(page_title="DreamLens", layout="centered")
st.title("DreamLens")
st.subheader("Cuenta tu sueño y visualiza lo que tu mente imaginó mientras dormías")

# Explicación
with st.expander("¿Cómo funciona?"):
    st.markdown("""
    1. Escribe tu sueño con muchos detalles.
    2. DreamLens lo interpreta simbólicamente.
    3. Se genera una pequeña historia inspirada en tu sueño.
    4. Se crea una imagen visual basada en lo que soñaste.
    """)

# Entrada del sueño
dream_input = st.text_area(
    "¿Qué soñaste anoche?",
    height=250,
    placeholder="Ejemplo: Soñé con un cielo oscuro y un perro verde que hablaba..."
)

# Botón de acción
if st.button("Interpretar y Visualizar"):
    if not dream_input.strip():
        st.warning("Por favor, escribe tu sueño.")
    else:
        with st.spinner("Analizando tu sueño..."):

            # Interpretación del sueño
            interp_prompt = f"""
Actúa como un analista de sueños profesional. Interpreta simbólicamente el siguiente sueño:

{dream_input}
""".encode('utf-8').decode('utf-8')

            interp_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": interp_prompt}],
                temperature=0.7
            )
            interpretation = interp_response.choices[0].message.content

            # Historia inspirada en el sueño
            story_prompt = f"""
Convierte este sueño en una breve historia literaria (máximo 3 párrafos):

{dream_input}
""".encode('utf-8').decode('utf-8')

            story_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": story_prompt}],
                temperature=0.9
            )
            story = story_response.choices[0].message.content

            # Generación de imagen
            image_prompt = f"Una escena realista basada en este sueño: {dream_input}"
            image_response = client.images.generate(
                prompt=image_prompt,
                n=1,
                size="512x512"
            )
            image_url = image_response.data[0].url

        # Resultados
        st.success("¡Sueño procesado con éxito!")
        st.markdown("### Interpretación simbólica:")
        st.markdown(interpretation)

        st.markdown("### Historia basada en tu sueño:")
        st.markdown(story)

        st.markdown("### Imagen generada:")
        st.image(image_url, caption="Visualización del sueño", use_column_width=True)

        st.markdown("---")
        st.markdown("¿Quieres analizar otro sueño?")
