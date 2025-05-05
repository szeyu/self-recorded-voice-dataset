import streamlit as st
import logging

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def setup_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Voice Recording App", 
        layout="wide",
        initial_sidebar_state="expanded"
    ) 