import streamlit as st
import time
import logging
import os

from voice_recorder.utils.session import init_session_state
from voice_recorder.data_handlers.csv_handler import load_data, save_recording
from voice_recorder.audio_handlers.audio_processor import save_audio, create_unique_filename
from voice_recorder.audio_handlers.recorder import record_audio

logger = logging.getLogger(__name__)

def show_record_page():
    """Display the record from CSV page"""
    st.header("Record Voice for Existing Text")
    
    # Initialize session state
    init_session_state()
    
    # Load existing data
    csv_path = "data/data.csv"
    df = load_data(csv_path)
    
    # Filter dataframe to show only unrecorded texts
    unrecorded_df = df[df["recorded"].fillna(False) == False]
    
    if len(unrecorded_df) > 0:
        # Select a text to record
        text_index = st.selectbox(
            "Select a text to record:",
            options=unrecorded_df.index.tolist(),
            format_func=lambda x: unrecorded_df.loc[x, "text"],
            key=f"selectbox_{st.session_state.get('rerun_key', 0)}"
        )
        
        if text_index is not None:
            selected_text = unrecorded_df.loc[text_index, "text"]
            st.session_state.current_text = selected_text
            
            st.markdown(f"### Text to record:")
            st.markdown(f"<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; font-size: 20px;'>{selected_text}</div>", unsafe_allow_html=True)
            st.markdown("--- ")
            
            # Audio recording interface
            sample_rate = 24000  # 24kHz as required

            # Add slider for recording duration
            duration = st.slider(
                "Select Recording Duration (seconds):", 
                min_value=3,
                max_value=15,
                value=10,
                step=1
            )
            st.caption(f"Recording will last for {duration} seconds.")
            
            # Start/stop recording buttons
            col1, col2 = st.columns([1, 3])
            with col1:
                if not st.session_state.recording:
                    if st.button("Start Recording", key=f"start_rec_{text_index}"):
                        logger.info(f"Starting recording for text index: {text_index}, duration: {duration}s")
                        st.session_state.recording = True
                        st.session_state.audio_data = []
                        st.rerun()
                else:
                    if st.button("Stop Recording", key=f"stop_rec_{text_index}"):
                        logger.info("Stopping recording manually.")
                        st.session_state.recording = False 
                        st.rerun()
            
            # Recording indicator and execution
            with col2:
                if st.session_state.recording:
                    st.markdown("🔴 **Recording in progress...**")
                    
                    # Record audio
                    audio_data = record_audio(duration, sample_rate)
                    
                    # Update session state
                    st.session_state.audio_data = audio_data
                    st.session_state.recording = False
                    st.rerun()
            
            # Display recorded audio and save button
            if len(st.session_state.audio_data) > 0 and not st.session_state.recording:
                st.audio(st.session_state.audio_data, sample_rate=sample_rate)
                
                if st.button("Save Recording", key=f"save_rec_{text_index}"):
                    logger.info(f"Attempting to save recording for text index: {text_index}")
                    
                    # Create a unique filename
                    audio_filename = create_unique_filename("audio_files")
                    
                    # Save audio file
                    if save_audio(st.session_state.audio_data, sample_rate, audio_filename):
                        # Update the dataset
                        success, df = save_recording(df, text_index, audio_filename, csv_path)
                        
                        if success:
                            st.success(f"Recording saved successfully as {os.path.basename(audio_filename)}!")
                            st.session_state.audio_data = []
                            st.session_state['rerun_key'] = st.session_state.get('rerun_key', 0) + 1
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Failed to update dataset. Audio file saved but not linked.")
                    else:
                        st.error("Failed to save audio file.")
    else:
        logger.info("No unrecorded texts found in Tab 1.")
        st.info("No unrecorded texts found. Add new texts in the 'Add New Text' tab or import more.") 