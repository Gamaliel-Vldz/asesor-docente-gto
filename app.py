import streamlit as st

# Configuración de la App
st.set_page_config(page_title="Asesor Docente GTO", page_icon="🏫")

# Personalidad del Asesor
SYSTEM_PROMPT = """Actúa como un asesor experto en derechos laborales de docentes de sostenimiento federal en Guanajuato..."""

st.title("🏫 Asesor Docente GTO")
st.info("Hola, compañero. Soy tu asesor legal. ¿En qué área necesitas orientación hoy?")

# Menú de temas
tema = st.selectbox("Selecciona un área temática:", [
    "Permisos y licencias",
    "Protocolos de emergencia/accidentes",
    "Conflictos laborales/Acoso",
    "Incapacidades (ISSSTE)",
    "Derechos y Promoción (USICAMM)",
    "Responsabilidad legal"
])

# Chat simple
if prompt := st.chat_input("Escribe tu duda específica aquí..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        st.markdown(f"Has seleccionado: **{tema}**. Estoy analizando tu duda: '{prompt}' conforme a la normativa vigente de Guanajuato.")
        st.warning("Nota: Para que yo responda con IA real, necesitamos conectar una 'API Key' en el siguiente paso.")
