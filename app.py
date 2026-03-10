import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Digital Assets Models Interface",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for model tracking
if 'current_llm_model' not in st.session_state:
    st.session_state.current_llm_model = None

# Sidebar navigation
st.sidebar.title("🤖 AI Models Interface")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Page:",
    ["Voice Assistant", "STT", "LLM", "TTS"],
    
)

# Import and display selected page
if page == "Voice Assistant":
    from pages import end_to_end
    end_to_end.show()
elif page == "STT":
    from pages import stt
    stt.show()
elif page == "LLM":
    from pages import llm
    llm.show()
elif page == "TTS":
    from pages import tts
    tts.show()

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit")
