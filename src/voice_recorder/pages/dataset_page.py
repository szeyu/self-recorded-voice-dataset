import streamlit as st
import logging
import os

from voice_recorder.data_handlers.csv_handler import load_data, delete_recording
from voice_recorder.audio_handlers.audio_processor import delete_audio_file

logger = logging.getLogger(__name__)

def show_dataset_page():
    """Display the dataset overview page"""
    st.header("Dataset Overview")
    
    # Load existing data
    csv_path = "data/data.csv"
    df = load_data(csv_path)
    
    # Display statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Texts", len(df))
    with col2:
        st.metric("Recorded", len(df[df["recorded"] == True]))
    with col3:
        st.metric("Remaining", len(df[df["recorded"] != True]))
    
    # Add a data management section
    st.subheader("Data Management")
    
    # Display the data with interactive components
    # Filter options
    view_option = st.radio(
        "View options:", 
        ["All Entries", "Recorded Only", "Unrecorded Only"], 
        horizontal=True
    )
    
    # Filter the dataframe based on selection
    if view_option == "Recorded Only":
        filtered_df = df[df["recorded"] == True]
    elif view_option == "Unrecorded Only":
        filtered_df = df[df["recorded"] != True]
    else:
        filtered_df = df.copy()
    
    # Display dataframe with actions
    if not filtered_df.empty:
        # Create columns for display and actions
        for idx, row in filtered_df.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                text = row["text"]
                # Truncate long text for display
                display_text = text if len(text) < 60 else f"{text[:57]}..."
                st.text(display_text)
            
            with col2:
                if row["recorded"] == True:
                    audio_file = os.path.join("audio_files", row["audio"])
                    if os.path.exists(audio_file):
                        st.audio(audio_file, format="audio/wav")
                    else:
                        st.warning("Audio file missing")
                else:
                    st.info("Not recorded")
            
            with col3:
                if row["recorded"] == True:
                    if st.button("Delete", key=f"delete_{idx}"):
                        logger.info(f"Deleting recording for text index: {idx}")
                        
                        # Delete audio file
                        audio_path = os.path.join("audio_files", row["audio"])
                        delete_audio_file(audio_path)
                        
                        # Update database
                        success, df = delete_recording(df, idx, csv_path)
                        
                        if success:
                            st.success("Recording deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete recording.")
    else:
        st.info("No records match the selected filter.") 