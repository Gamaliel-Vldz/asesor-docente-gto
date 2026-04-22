import streamlit as st
from groq import Groq

# 1. Configuración de la App
st.set_page_config(page_title="Asesor Docente GTO", page_icon="🏫")

# 2. Conexión segura con tus "Secrets" (la llave y el prompt)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    system_message = st.secrets["SYSTEM_PROMPT"]
except Exception as e:
    st.error("Falta configurar la API Key o el Prompt en los Secrets de Streamlit.")
    st.stop()

# 3. Estilo visual de la App
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInput { position: fixed; bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏫 Asesor Docente GTO")
st.caption("Asesor Legal para Docentes Federalizados - Guanajuato")

# 4. Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Lógica del Chat
if prompt := st.chat_input("¿En qué puedo ayudarte, compañero?"):
    # Guardar y mostrar lo que escribe el docente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la Inteligencia Artificial
    with st.chat_message("assistant"):
        with st.spinner("Consultando normativa vigente..."):
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "system", "content": system_message}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("Hubo un error al conectar con el cerebro de la IA. Revisa tu llave de Groq.")
