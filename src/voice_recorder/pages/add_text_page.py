import streamlit as st
import time
import logging

from voice_recorder.data_handlers.csv_handler import load_data, add_text

logger = logging.getLogger(__name__)

def show_add_text_page():
    """Display the add new text page"""
    st.header("Add New Text")
    
    # Load existing data
    csv_path = "data/data.csv"
    df = load_data(csv_path)
    
    new_text = st.text_area(
        "Enter new text (32-140 characters):", 
        height=100, 
        max_chars=140,
        help="Enter a short sentence or phrase (32-140 characters)"
    )
    
    if st.button("Add Text"):
        if not new_text or len(new_text.strip()) == 0:
            st.error("Please enter some text.")
        else:
            logger.info(f"Attempting to add new text: '{new_text[:50]}...'" if len(new_text) > 50 else f"Attempting to add new text: '{new_text}'")
            
            success, df = add_text(df, new_text, csv_path)
            
            if success:
                st.success("Text added successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Text must be between 32 and 140 characters.") 