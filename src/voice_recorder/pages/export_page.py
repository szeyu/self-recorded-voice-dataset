import streamlit as st
import logging
import os

from voice_recorder.data_handlers.export_handler import export_dataset
from voice_recorder.data_handlers.huggingface_uploader import push_to_huggingface

logger = logging.getLogger(__name__)

def show_export_page():
    """Display the export dataset page"""
    st.header("Export Dataset to Hugging Face Format")
    
    # Input for export settings
    input_csv = st.text_input("Input CSV Path", value="data/data.csv")
    audio_dir = st.text_input("Audio Directory", value="audio_files")
    output_dir = st.text_input("Output Directory", value="my_voice_dataset")
    
    # Create tabs for local export and HF upload
    export_tab, upload_tab = st.tabs(["Export Locally", "Upload to Hugging Face"])
    
    with export_tab:
        # Button to trigger export
        if st.button("Export Dataset Locally"):
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
    
    with upload_tab:
        st.subheader("Upload to Hugging Face Hub")
        
        # Input for Hugging Face settings
        repo_id = st.text_input("Repository ID (username/dataset-name)")
        token = st.text_input("Hugging Face Token", type="password", 
                              help="Your Hugging Face API token. If not provided, will use HUGGINGFACE_TOKEN environment variable.")
        is_private = st.checkbox("Make repository private", value=True)
        
        # Offer to export before uploading
        export_before_upload = st.checkbox("Export before uploading", value=True, 
                                         help="Export the dataset before uploading to Hugging Face")
        
        # Button to trigger upload
        if st.button("Upload to Hugging Face"):
            if not repo_id or '/' not in repo_id:
                st.error("Please enter a valid repository ID in the format 'username/dataset-name'")
            else:
                # First export if requested
                if export_before_upload:
                    st.info("Exporting dataset before uploading...")
                    with st.spinner("Exporting dataset..."):
                        export_success = export_dataset(input_csv, audio_dir, output_dir)
                        
                        if not export_success:
                            st.error("Failed to export dataset. Upload aborted.")
                            st.stop()
                        else:
                            st.success("Dataset exported successfully.")
                
                # Now upload to Hugging Face
                st.info(f"Uploading to Hugging Face Hub: {repo_id}")
                with st.spinner("Uploading to Hugging Face Hub..."):
                    # If token is empty, pass None to use env variable
                    hf_token = token if token else None
                    success, repo_url = push_to_huggingface(
                        dataset_dir=output_dir,
                        repo_id=repo_id,
                        private=is_private,
                        token=hf_token
                    )
                    
                    if success:
                        st.success(f"Dataset successfully uploaded to Hugging Face!")
                        st.markdown(f"[View your dataset on Hugging Face]({repo_url})")
                    else:
                        st.error("Failed to upload dataset to Hugging Face. Check logs for details.") 