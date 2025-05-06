import pandas as pd
from datasets import Dataset, Audio
import os
import logging

logger = logging.getLogger(__name__)

def export_dataset(input_csv, audio_dir, output_dir):
    """
    Export dataset to Hugging Face format
    
    Args:
        input_csv: Path to the input CSV file
        audio_dir: Directory containing audio files
        output_dir: Directory to save the exported dataset
    
    Returns:
        success: Boolean indicating if export was successful
    """
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Ensured output directory exists: {output_dir}")
        
        # Load CSV
        logger.info(f"Loading input CSV: {input_csv}")
        df = pd.read_csv(input_csv)
        logger.info(f"Loaded {len(df)} records from CSV.")
        
        # Filter to only include recorded data
        original_count = len(df)
        df = df[df["recorded"] == True]
        filtered_count = len(df)
        logger.info(f"Filtered records: {original_count} -> {filtered_count} (keeping only recorded=True)")
        
        if filtered_count == 0:
            logger.warning("No recorded data found in the input CSV. Export aborted.")
            return False
        
        # Ensure audio paths are absolute
        logger.info(f"Making audio paths absolute relative to: {audio_dir}")
        df["audio"] = df["audio"].apply(lambda x: os.path.join(audio_dir, x))
        
        # Select only the required columns for the final dataset
        logger.info("Selecting only 'text' and 'audio' columns for the final dataset.")
        if "text" not in df.columns:
            logger.error("'text' column not found in the input CSV. Cannot proceed with column selection.")
            return False
        df_final = df[["text", "audio"]]
        
        # Save to CSV in the output directory (optional: save df_final instead?)
        # For now, keeping the original df for the CSV dump for potential debugging
        output_csv_path = os.path.join(output_dir, "dataset.csv")
        logger.info(f"Saving full filtered data (for reference) to CSV: {output_csv_path}")
        df.to_csv(output_csv_path, index=False) # Save original df with all columns here
        
        # Create Hugging Face dataset from the selected columns
        logger.info("Creating Hugging Face Dataset object from selected columns ('text', 'audio').")
        dataset = Dataset.from_pandas(df_final) # Use df_final here
        
        # Cast audio column to Audio feature
        logger.info("Casting 'audio' column to Hugging Face Audio feature (sampling_rate=24000).")
        dataset = dataset.cast_column("audio", Audio(sampling_rate=24000))
        
        # Save dataset to Parquet format
        output_parquet_path = os.path.join(output_dir, "dataset.parquet")
        logger.info(f"Saving dataset to Parquet format: {output_parquet_path}")
        dataset.to_parquet(output_parquet_path)
        
        logger.info("Dataset export completed successfully.")
        return True
    except Exception as e:
        logger.error(f"Error during dataset export: {e}", exc_info=True)
        return False 