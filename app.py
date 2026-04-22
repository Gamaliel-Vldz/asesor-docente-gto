import streamlit as st
from groq import Groq

# Configuración de la página
st.set_page_config(page_title="Asesor Docente GTO", page_icon="🏫", layout="centered")

# Estilo visual mejorado para parecerse a Claude
st.markdown("""
    <style>
    .stChatMessage { background-color: #f0f2f6; border-radius: 15px; padding: 15px; margin-bottom: 10px; }
    .stMarkdown h3 { color: #1E3A8A; border-bottom: 2px solid #1E3A8A; padding-bottom: 5px; }
    .stMarkdown p { font-size: 16px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# Validación de llaves secretas
if "GROQ_API_KEY" not in st.secrets:
    st.error("Error: Configura la GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Encabezado de la App
st.title("🏫 Asesor Docente GTO")
st.markdown("#### Consultoría Legal • Sostenimiento Federal • Sección 13")
st.info("Este asesor utiliza inteligencia artificial avanzada (70B) para analizar protocolos de la SEG y la SEP.")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu duda legal aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Llamada al modelo inteligente 70B
            chat_completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": st.secrets["SYSTEM_PROMPT"]},
                    * [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                temperature=0.3 # Baja temperatura para que sea más preciso y menos creativo
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Hubo un error al procesar la respuesta: {e}")
