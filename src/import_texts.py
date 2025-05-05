import pandas as pd
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def import_texts(sample_file, output_file):
    """
    Import texts from a sample file to the app's data structure
    
    Args:
        sample_file: Path to the sample texts file (CSV)
        output_file: Path to save the app data (CSV)
    """
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    try:
        # Read the sample texts
        logger.info(f"Reading sample texts from {sample_file}")
        sample_df = pd.read_csv(sample_file)
        
        # Create the app data structure
        app_df = pd.DataFrame(columns=["text", "audio", "recorded"])
        
        # Add sample texts to the app data
        for _, row in sample_df.iterrows():
            # Handle potential quotes in text
            text = row["text"]
            if isinstance(text, str) and text.startswith('"') and text.endswith('"'):
                text = text.strip('"')
                
            app_df = pd.concat([
                app_df, 
                pd.DataFrame({
                    "text": [text],
                    "audio": [None],
                    "recorded": [False]
                })
            ], ignore_index=True)
        
        # Save to the app's data file
        logger.info(f"Saving {len(app_df)} texts to {output_file}")
        app_df.to_csv(output_file, index=False)
        
        logger.info(f"Successfully imported {len(app_df)} texts into the app data.")
        return True
    except Exception as e:
        logger.error(f"Error importing texts: {e}")
        return False

if __name__ == "__main__":
    # Use command line arguments if provided, otherwise use defaults
    sample_file = sys.argv[1] if len(sys.argv) > 1 else "sample_texts.csv"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "data/data.csv"
    
    success = import_texts(sample_file, output_file)
    
    if success:
        print(f"Imported texts successfully. You can now run the app with: streamlit run src/app.py")
    else:
        print("Failed to import texts. Check the logs for details.") 