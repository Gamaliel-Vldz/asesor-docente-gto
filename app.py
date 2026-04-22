import streamlit as st
from groq import Groq

st.set_page_config(page_title="Asesor Docente GTO", page_icon="🏫")

# 1. DIAGNÓSTICO DE SECRETOS
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ ERROR: No encuentro la palabra 'GROQ_API_KEY' en tus Secrets.")
    st.info("Ve a Manage App -> Settings -> Secrets y asegúrate de que la primera línea diga exactamente: GROQ_API_KEY = 'tu_llave'")
    st.stop()

# 2. INICIALIZAR CLIENTE
try:
    # Usamos la llave que pusiste en Secrets
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"❌ ERROR AL INICIAR MOTOR: {e}")
    st.stop()

st.title("🏫 Asesor Docente GTO")
st.caption("Asesoría Legal - Guanajuato")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu duda aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Usamos un modelo muy rápido y estable
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": st.secrets.get("SYSTEM_PROMPT", "Eres un asesor legal.")},
                    * [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"❌ ERROR DE RESPUESTA: {e}")
            st.warning("Verifica que tu llave de Groq sea válida y no tenga espacios.")
