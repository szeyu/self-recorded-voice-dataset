import streamlit as st
import sounddevice as sd
import time
import logging

logger = logging.getLogger(__name__)

def record_audio(duration, sample_rate=24000):
    """
    Record audio for a specified duration
    
    Args:
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
        
    Returns:
        audio_data: NumPy array of recorded audio
    """
    logger.info(f"Recording audio for {duration} seconds at {sample_rate}Hz")
    
    # Record audio using sounddevice
    audio_data = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='float32'
    )
    
    # Create a progress bar
    progress_bar = st.progress(0)
    start_time = time.time()
    
    # Update progress bar
    while (time.time() - start_time) < duration:
        # Calculate progress percentage
        elapsed_time = time.time() - start_time
        progress = min(int((elapsed_time / duration) * 100), 100)
        progress_bar.progress(progress)
        time.sleep(0.1)  # Small sleep to avoid busy-waiting
    
    # Complete progress bar
    progress_bar.progress(100)
    
    # Wait for recording to complete
    sd.wait()
    
    logger.info("Recording finished")
    return audio_data.flatten() 