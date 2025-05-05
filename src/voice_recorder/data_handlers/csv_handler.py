import pandas as pd
import logging
import os

from voice_recorder.audio_handlers.audio_processor import delete_audio_file

logger = logging.getLogger(__name__)

def load_data(csv_file):
    """
    Load existing data from CSV or create a new one
    
    Args:
        csv_file: Path to the CSV file
        
    Returns:
        pd.DataFrame: DataFrame with the loaded data
    """
    try:
        df = pd.read_csv(csv_file)
        logger.info(f"Successfully loaded {len(df)} records from {csv_file}")
        return df
    except FileNotFoundError:
        logger.warning(f"CSV file {csv_file} not found. Creating a new DataFrame.")
        # Create a new DataFrame with required columns
        return pd.DataFrame(columns=["text", "audio", "recorded"])
    except Exception as e:
        logger.error(f"Error loading data from {csv_file}: {e}")
        return pd.DataFrame(columns=["text", "audio", "recorded"])

def save_data(df, csv_path):
    """
    Save DataFrame to CSV
    
    Args:
        df: DataFrame to save
        csv_path: Path to save the CSV file
        
    Returns:
        bool: True if save was successful, False otherwise
    """
    try:
        df.to_csv(csv_path, index=False)
        logger.info(f"Successfully saved DataFrame to {csv_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving DataFrame to {csv_path}: {e}")
        return False

def add_text(df, text, csv_path):
    """
    Add a new text to the dataset
    
    Args:
        df: DataFrame to add text to
        text: Text to add
        csv_path: Path to save the updated DataFrame
        
    Returns:
        tuple: (success, updated_df)
    """
    if len(text) < 32 or len(text) > 140:
        logger.warning(f"Add Text failed: Text length ({len(text)}) not within 32-140 characters.")
        return False, df
    
    # Add to DataFrame
    new_row = pd.DataFrame({
        "text": [text],
        "audio": [None],
        "recorded": [False]
    })
    
    updated_df = pd.concat([df, new_row], ignore_index=True)
    
    # Save updated DataFrame
    success = save_data(updated_df, csv_path)
    if success:
        logger.info(f"New text added: '{text[:50]}...'" if len(text) > 50 else f"New text added: '{text}'")
    
    return success, updated_df

def save_recording(df, text_index, audio_path, csv_path):
    """
    Save a recording to the dataset
    
    Args:
        df: DataFrame to update
        text_index: Index of the text in the DataFrame
        audio_path: Path to the audio file
        csv_path: Path to save the updated DataFrame
        
    Returns:
        tuple: (success, updated_df)
    """
    try:
        # Update the DataFrame
        df_copy = df.copy()
        df_copy.loc[text_index, "audio"] = os.path.basename(audio_path)
        df_copy.loc[text_index, "recorded"] = True
        
        # Save the updated DataFrame
        success = save_data(df_copy, csv_path)
        if success:
            logger.info(f"Recording saved for text index {text_index}: {os.path.basename(audio_path)}")
            return True, df_copy
        return False, df
    except Exception as e:
        logger.error(f"Error saving recording data: {e}")
        return False, df

def delete_recording(df, index, csv_path):
    """
    Delete an audio recording and update the dataset
    
    Args:
        df: DataFrame to update
        index: Index of the text in the DataFrame
        csv_path: Path to save the updated DataFrame
        
    Returns:
        tuple: (success, updated_df)
    """
    try:
        # Get audio file path
        audio_filename = df.loc[index, "audio"]
        if audio_filename and not pd.isna(audio_filename):
            audio_path = os.path.join("audio_files", audio_filename)
            
            # Delete the audio file
            if delete_audio_file(audio_path):
                # Update the DataFrame
                df_copy = df.copy()
                df_copy.loc[index, "audio"] = None
                df_copy.loc[index, "recorded"] = False
                
                # Save the updated DataFrame
                if save_data(df_copy, csv_path):
                    logger.info(f"Recording deleted for text index {index}")
                    return True, df_copy
            
            return False, df
        else:
            logger.warning(f"No audio file to delete for index {index}")
            return False, df
    except Exception as e:
        logger.error(f"Error deleting recording: {e}")
        return False, df 