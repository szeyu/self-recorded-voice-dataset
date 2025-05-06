#!/usr/bin/env python3
"""
Script to push a dataset to the Hugging Face Hub.
This can be run after exporting a dataset using the Streamlit app.
"""
import os
import sys
import argparse
import logging
from getpass import getpass

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add src to path if needed
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Hugging Face uploader
from voice_recorder.data_handlers.huggingface_uploader import push_to_huggingface
from voice_recorder.data_handlers.export_handler import export_dataset

def main():
    """Push a dataset to the Hugging Face Hub"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Push a voice dataset to Hugging Face Hub")
    parser.add_argument("--dataset", default="my_voice_dataset", help="Path to the dataset directory")
    parser.add_argument("--repo-id", required=True, help="Hugging Face repository ID (username/repo-name)")
    parser.add_argument("--token", help="Hugging Face API token (if not provided, will ask or use HUGGINGFACE_TOKEN env var)")
    parser.add_argument("--public", action="store_true", help="Make the repository public (default is private)")
    parser.add_argument("--export-first", action="store_true", help="Export the dataset before pushing")
    parser.add_argument("--input-csv", default="data/data.csv", help="Path to input CSV (if exporting)")
    parser.add_argument("--audio-dir", default="audio_files", help="Path to audio directory (if exporting)")
    
    args = parser.parse_args()
    
    # Export the dataset if requested
    if args.export_first:
        logger.info(f"Exporting dataset first: {args.input_csv} -> {args.dataset}")
        if not os.path.exists(args.input_csv):
            logger.error(f"Input CSV file not found: {args.input_csv}")
            return 1
        
        if not os.path.exists(args.audio_dir):
            logger.error(f"Audio directory not found: {args.audio_dir}")
            return 1
        
        success = export_dataset(args.input_csv, args.audio_dir, args.dataset)
        if not success:
            logger.error("Export failed. Aborting push to Hugging Face.")
            return 1
        
        logger.info("Dataset exported successfully.")
    
    # Check if dataset exists
    if not os.path.exists(args.dataset):
        logger.error(f"Dataset directory not found: {args.dataset}")
        return 1
    
    # Get token if not provided
    token = args.token
    if token is None:
        # Check environment variable
        token = os.environ.get("HUGGINGFACE_TOKEN")
        if token is None:
            # Prompt user for token
            token = getpass("Enter your Hugging Face token: ")
    
    # Push to Hugging Face
    logger.info(f"Pushing dataset to Hugging Face: {args.repo_id}")
    success, repo_url = push_to_huggingface(
        dataset_dir=args.dataset,
        repo_id=args.repo_id,
        private=not args.public,
        token=token
    )
    
    if success:
        logger.info(f"Dataset successfully pushed to: {repo_url}")
        return 0
    else:
        logger.error("Failed to push dataset to Hugging Face.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 