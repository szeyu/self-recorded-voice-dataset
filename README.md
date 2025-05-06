# Voice Recording Dataset Creator

A Streamlit application for creating voice recording datasets for text-to-speech training.

## Features

- Record voice samples for predefined text snippets
- Add custom text to record
- Generate text suggestions using Google's Gemini AI
  - Target specific speech durations
  - Focus on particular domains or topics
  - Provide context for tailored suggestions
  - Support for multiple languages
- Manage your dataset (view, delete recordings)
- Export to Hugging Face dataset format
- Directly upload datasets to Hugging Face Hub

## Project Structure

```
voice-recorder/
├── src/                      # Source code
│   ├── app.py                # Main application entry point
│   ├── import_texts.py       # Script to import texts
│   ├── push_to_hf.py         # Script to push dataset to Hugging Face
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
git clone https://github.com/szeyu/self-recorded-voice-dataset.git
cd self-recorded-voice-dataset
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
   - Add new texts to record (manually or using AI suggestions)
   - View and manage your dataset
   - Export your dataset to Hugging Face format
   - Upload your dataset to Hugging Face Hub

## AI Text Suggestions

The application can generate text suggestions for recording using Google's Gemini AI:

1. Navigate to the "Add New Text" tab and select the "AI Text Suggestions" sub-tab
2. Expand the "API Settings" section and enter your Gemini API key
   - You can get a Gemini API key at https://makersuite.google.com/app/apikey
3. Configure your text generation:
   - Choose your preferred language and number of suggestions
   - Specify a domain/topic (e.g., technology, healthcare, cooking)
   - Add specific context or requirements to guide the AI
   - Set your target speech duration (in seconds)
4. Click "Generate Text Suggestions"
5. Review the generated suggestions and select one to add to your dataset

## Uploading to Hugging Face

There are two ways to upload your dataset to Hugging Face:

### 1. Using the Streamlit interface

In the "Export Dataset" tab, select the "Upload to Hugging Face" sub-tab. Enter your repository ID (in the format `username/dataset-name`) and your Hugging Face token, then click "Upload to Hugging Face".

### 2. Using the command line script

```
python src/push_to_hf.py --repo-id username/dataset-name --export-first
```

Options:
- `--repo-id` (required): Your Hugging Face repository ID (username/dataset-name)
- `--token`: Your Hugging Face API token (if not provided, will ask or use HUGGINGFACE_TOKEN env var)
- `--dataset`: Path to the exported dataset directory (default: my_voice_dataset)
- `--export-first`: Export the dataset before pushing
- `--public`: Make the repository public (default is private)
- `--input-csv`: Path to input CSV (if exporting, default: data/data.csv)
- `--audio-dir`: Path to audio directory (if exporting, default: audio_files)

## License

This project is licensed under the MIT License - see the LICENSE file for details.