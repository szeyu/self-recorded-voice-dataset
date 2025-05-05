import wave
import numpy as np
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def save_audio(audio_data, sample_rate, file_path):
    """
    Save audio data as a WAV file
    
    Args:
        audio_data: NumPy array of audio data
        sample_rate: Sample rate of audio (Hz)
        file_path: Path to save the WAV file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure the audio is in float32 format and normalize if needed
        audio_data = np.array(audio_data, dtype=np.float32)
        
        # Convert from float32 to int16 for WAV file
        audio_data_int = (audio_data * 32767).astype(np.int16)
        
        # Create WAV file
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data_int.tobytes())
        logger.info(f"Successfully saved audio to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving audio to {file_path}: {e}")
        return False

def create_unique_filename(directory, prefix="audio_", extension=".wav"):
    """
    Create a unique filename based on timestamp
    
    Args:
        directory: Directory to save the file
        prefix: Prefix for the filename
        extension: File extension
        
    Returns:
        str: Full path to the new file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(directory, f"{prefix}{timestamp}{extension}")

def delete_audio_file(audio_path):
    """
    Delete an audio file from the filesystem
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"Deleted audio file: {audio_path}")
            return True
        else:
            logger.warning(f"Audio file not found: {audio_path}")
            return False
    except Exception as e:
        logger.error(f"Error deleting audio file {audio_path}: {e}")
        return False 