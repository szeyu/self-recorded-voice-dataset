import streamlit as st

def init_session_state():
    """Initialize session state variables"""
    if 'recording' not in st.session_state:
        st.session_state.recording = False
    if 'audio_data' not in st.session_state:
        st.session_state.audio_data = []
    if 'current_text' not in st.session_state:
        st.session_state.current_text = ""
    if 'rerun_key' not in st.session_state:
        st.session_state['rerun_key'] = 0 