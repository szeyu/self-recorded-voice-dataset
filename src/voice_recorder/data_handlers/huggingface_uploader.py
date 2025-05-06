import os
import logging
from huggingface_hub import HfApi, create_repo
from datasets import load_dataset

logger = logging.getLogger(__name__)

def push_to_huggingface(dataset_dir, 
                        repo_id=None, 
                        private=True, 
                        token=None, 
                        repo_type="dataset",
                        commit_message="Upload voice dataset"):
    """
    Push a dataset to the Hugging Face Hub
    
    Args:
        dataset_dir: Local directory containing the dataset (with dataset.parquet)
        repo_id: ID for the repository (username/dataset-name format)
        private: Whether the repository should be private
        token: HuggingFace API token (if not provided, will use HUGGINGFACE_TOKEN env var)
        repo_type: Type of repository ("dataset" or "model")
        commit_message: Commit message for the upload
        
    Returns:
        success: Boolean indicating if push was successful
        repo_url: URL of the created repository if successful
    """
    try:
        # Check if token is provided or in environment variables
        if token is None:
            token = os.environ.get("HUGGINGFACE_TOKEN")
            if token is None:
                logger.error("No Hugging Face token provided and HUGGINGFACE_TOKEN not set in environment")
                return False, None
        
        # Verify repo_id format
        if repo_id is None or '/' not in repo_id:
            logger.error(f"Invalid repo_id format: {repo_id}. Should be 'username/dataset-name'")
            return False, None
        
        # Initialize Hugging Face API
        api = HfApi(token=token)
        logger.info(f"Initialized Hugging Face API")
        
        # Check if dataset files exist
        parquet_path = os.path.join(dataset_dir, "dataset.parquet")
        if not os.path.exists(parquet_path):
            logger.error(f"Dataset file not found: {parquet_path}")
            return False, None
        
        # Create the repository if it doesn't exist
        try:
            logger.info(f"Creating repository: {repo_id}")
            create_repo(
                repo_id=repo_id,
                repo_type=repo_type,
                private=private,
                token=token,
                exist_ok=True
            )
        except Exception as e:
            logger.error(f"Failed to create repository {repo_id}: {e}")
            return False, None
        
        # Upload the dataset
        logger.info(f"Uploading dataset from {dataset_dir} to {repo_id}")
        
        # Load and push the dataset
        dataset = load_dataset("parquet", data_files={"train": parquet_path})
        dataset.push_to_hub(
            repo_id=repo_id,
            private=private,
            token=token,
            commit_message=commit_message
        )
        
        # Upload the CSV file as well for reference
        csv_path = os.path.join(dataset_dir, "dataset.csv")
        if os.path.exists(csv_path):
            logger.info(f"Uploading CSV file: {csv_path}")
            api.upload_file(
                path_or_fileobj=csv_path,
                path_in_repo="dataset.csv",
                repo_id=repo_id,
                repo_type=repo_type,
                commit_message="Upload CSV version of dataset"
            )
        
        # Generate repo URL
        repo_url = f"https://huggingface.co/datasets/{repo_id}"
        logger.info(f"Dataset successfully uploaded to {repo_url}")
        
        return True, repo_url
    
    except Exception as e:
        logger.error(f"Error pushing to Hugging Face: {e}", exc_info=True)
        return False, None 