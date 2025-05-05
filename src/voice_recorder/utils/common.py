import os
import logging

logger = logging.getLogger(__name__)

def ensure_directories():
    """Create necessary directories if they don't exist"""
    os.makedirs("data", exist_ok=True)
    os.makedirs("audio_files", exist_ok=True)
    logger.info("Ensured data and audio_files directories exist") 