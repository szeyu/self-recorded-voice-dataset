import streamlit as st
import logging
import os

from voice_recorder.data_handlers.export_handler import export_dataset

logger = logging.getLogger(__name__)

def show_export_page():
    """Display the export dataset page"""
    st.header("Export Dataset to Hugging Face Format")
    
    # Input for export settings
    input_csv = st.text_input("Input CSV Path", value="data/data.csv")
    audio_dir = st.text_input("Audio Directory", value="audio_files")
    output_dir = st.text_input("Output Directory", value="my_voice_dataset")
    
    # Button to trigger export
    if st.button("Export Dataset"):
        logger.info(f"Exporting dataset: {input_csv} -> {output_dir}")
        
        # Check if CSV exists
        if not os.path.exists(input_csv):
            st.error(f"Input CSV file not found: {input_csv}")
        # Check if audio directory exists
        elif not os.path.exists(audio_dir):
            st.error(f"Audio directory not found: {audio_dir}")
        else:
            # Show spinner during export
            with st.spinner("Exporting dataset..."):
                success = export_dataset(input_csv, audio_dir, output_dir)
                
                if success:
                    st.success(f"Dataset successfully exported to {output_dir}")
                    
                    # Show info about the exported files
                    st.info(
                        f"Exported files:\n"
                        f"- {os.path.join(output_dir, 'dataset.csv')}\n"
                        f"- {os.path.join(output_dir, 'dataset.parquet')}"
                    )
                else:
                    st.error("Export failed. Check logs for details.") 