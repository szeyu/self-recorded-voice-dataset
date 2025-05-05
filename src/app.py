import streamlit as st
import logging
import os

# Import utility functions
from voice_recorder.utils.config import setup_logging, setup_page
from voice_recorder.utils.common import ensure_directories

# Import pages
from voice_recorder.pages.record_page import show_record_page
from voice_recorder.pages.add_text_page import show_add_text_page
from voice_recorder.pages.dataset_page import show_dataset_page
from voice_recorder.pages.export_page import show_export_page

# Setup logging
logger = setup_logging()

def main():
    """Main application entry point"""
    logger.info("Starting Streamlit application")
    
    # Setup page configuration
    setup_page()
    
    # Ensure required directories exist
    ensure_directories()
    
    # Setup sidebar
    st.sidebar.title("Voice Recording App")
    st.sidebar.markdown("Record your voice for text-to-speech training")
    
    # App title
    st.title("Voice Recording Application")
    
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs([
        "Record from CSV", 
        "Add New Text", 
        "View Data",
        "Export Dataset"
    ])
    
    # Display different pages in each tab
    with tab1:
        show_record_page()
    
    with tab2:
        show_add_text_page()
    
    with tab3:
        show_dataset_page()
        
    with tab4:
        show_export_page()

if __name__ == "__main__":
    main() 