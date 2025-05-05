# Voice Recording Dataset Creator

A Streamlit application for creating voice recording datasets for text-to-speech training.

## Features

- Record voice samples for predefined text snippets
- Add custom text to record
- Manage your dataset (view, delete recordings)
- Export to Hugging Face dataset format

## Project Structure

```
voice-recorder/
├── src/                      # Source code
│   ├── app.py                # Main application entry point
│   ├── import_texts.py       # Script to import texts
│   ├── voice_recorder/       # Main package
│   │   ├── audio_handlers/   # Audio recording and processing
│   │   ├── components/       # Reusable UI components
│   │   ├── data_handlers/    # Data management (CSV, export)
│   │   ├── models/           # Data models
│   │   ├── pages/            # Application pages
│   │   └── utils/            # Utility functions
├── assets/                   # Static assets
├── data/                     # Data storage
├── audio_files/              # Recorded audio files
└── my_voice_dataset/         # Exported dataset
```

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Import sample texts (optional):
```
python src/import_texts.py sample_texts.csv
```

## Usage

1. Run the application:
```
streamlit run src/app.py
```

2. Use the tabs to:
   - Record your voice for existing texts
   - Add new texts to record
   - View and manage your dataset
   - Export your dataset to Hugging Face format

## Export to Hugging Face

The application can export your recorded dataset to Hugging Face format, making it easy to use for training text-to-speech models.

## License

This project is licensed under the MIT License - see the LICENSE file for details.