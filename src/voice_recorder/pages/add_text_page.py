import streamlit as st
import time
import logging
import os

from voice_recorder.data_handlers.csv_handler import load_data, add_text
from voice_recorder.data_handlers.ai_text_generator import generate_text_suggestions, estimate_character_count

logger = logging.getLogger(__name__)

def show_add_text_page():
    """Display the add new text page"""
    st.header("Add New Text")
    
    # Load existing data
    csv_path = "data/data.csv"
    df = load_data(csv_path)
    
    # Add tabs for manual entry and AI suggestions
    tab1, tab2 = st.tabs(["Manual Entry", "AI Text Suggestions"])
    
    # Tab 1: Manual Entry
    with tab1:
        new_text = st.text_area(
            "Enter new text (32-140 characters):", 
            height=100, 
            max_chars=140,
            help="Enter a short sentence or phrase (32-140 characters)"
        )
        
        if st.button("Add Text", key="add_manual_text"):
            process_add_text(new_text, df, csv_path)
    
    # Tab 2: AI Text Suggestions
    with tab2:
        st.subheader("Generate Text Suggestions with Gemini")
        
        # API Settings section
        st.markdown("### API Settings")
        # API key input
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Your Google Gemini API key. Get one at https://makersuite.google.com/app/apikey",
            placeholder="Enter your Gemini API key here"
        )
        
        # Save API key to session state for convenience
        if api_key and 'gemini_api_key' not in st.session_state:
            st.session_state.gemini_api_key = api_key
        elif api_key:
            st.session_state.gemini_api_key = api_key
        
        # Allow using saved API key
        if 'gemini_api_key' in st.session_state and not api_key:
            use_saved_key = st.checkbox("Use saved API key", value=True)
            if use_saved_key:
                api_key = st.session_state.gemini_api_key
        
        # Basic settings
        st.markdown("### Text Settings")
        col1, col2 = st.columns(2)
        with col1:
            language = st.text_input("Language", value="English", help="Specify the language for generated texts")
        with col2:
            suggestion_count = st.number_input("Number of suggestions", min_value=1, max_value=10, value=3)
        
        # Domain and Context
        st.markdown("### Content Guidance")
        domain = st.text_input(
            "Domain/Topic", 
            placeholder="e.g., technology, healthcare, cooking, travel",
            help="Specify a domain or topic to focus the generated text"
        )
        
        context = st.text_area(
            "Specific Context or Requirements", 
            placeholder="Provide more details about what you want the text to contain or sound like...",
            help="Add specific context, partial sentences, or requirements to guide the AI",
            height=80
        )
        
        # Speech duration settings
        st.markdown("### Speech Duration")
        use_duration = st.checkbox("Generate text for specific speech duration", value=True,
                                help="Generate texts suitable for a specific recording duration")
        
        # Only show slider if using duration-based generation
        speech_duration = None
        min_length = 32
        max_length = 140
        
        if use_duration:
            speech_duration = st.slider(
                "Target speech duration (seconds)",
                min_value=3,
                max_value=15,
                value=8,
                step=1,
                help="The AI will generate text appropriate for this speech duration"
            )
            
            # Show estimated character count
            if speech_duration:
                min_chars, max_chars = estimate_character_count(speech_duration, language)
                st.caption(f"Estimated {min_chars}-{max_chars} characters for {speech_duration}s speech in {language}")
        else:
            # Advanced text length options (shown only when not using duration)
            st.markdown("### Character Length Settings")
            min_length = st.number_input("Minimum character length", min_value=32, max_value=120, value=32)
            max_length = st.number_input("Maximum character length", min_value=min_length, max_value=140, value=140)
            st.caption("Note: Values must be between 32-140 characters to be valid for the app")
        
        # Button to generate suggestions
        st.markdown("### Generate")
        generate_button = st.button("Generate Text Suggestions", key="generate_suggestions")
        
        if generate_button:
            if not api_key:
                st.error("Please enter a Gemini API key in the API Settings section.")
            else:
                with st.spinner("Generating text suggestions..."):
                    # Set parameters based on user selections
                    params = {
                        "api_key": api_key,
                        "language": language,
                        "count": suggestion_count,
                        "domain": domain if domain else None,
                        "context": context if context else None
                    }
                    
                    # Add speech duration or min/max length
                    if use_duration and speech_duration:
                        params["speech_duration"] = speech_duration
                    else:
                        params["min_length"] = min_length
                        params["max_length"] = max_length
                    
                    # Get text suggestions from Gemini API
                    suggestions = generate_text_suggestions(**params)
                    
                    if suggestions:
                        st.success(f"Generated {len(suggestions)} text suggestions.")
                        
                        # Store in session state for later use
                        st.session_state.text_suggestions = suggestions
                        
                        # Store the generation parameters for reference
                        st.session_state.generation_params = {
                            "language": language,
                            "domain": domain if domain else None,
                            "context": context if context else None,
                            "speech_duration": speech_duration if use_duration else None
                        }
                    else:
                        st.error("Failed to generate text suggestions. Please check your API key and try again.")
        
        # Display suggestions if available
        if 'text_suggestions' in st.session_state and st.session_state.text_suggestions:
            st.markdown("### Text Suggestions")
            
            # Show what parameters were used to generate these suggestions
            if 'generation_params' in st.session_state:
                params = st.session_state.generation_params
                param_details = []
                if params.get("language"):
                    param_details.append(f"Language: {params['language']}")
                if params.get("domain"):
                    param_details.append(f"Domain: {params['domain']}")
                if params.get("speech_duration"):
                    param_details.append(f"Speech Duration: {params['speech_duration']}s")
                
                if param_details:
                    st.caption("Generated with: " + ", ".join(param_details))
            
            for i, suggestion in enumerate(st.session_state.text_suggestions):
                col1, col2, col3 = st.columns([4, 1, 1])
                with col1:
                    st.text_area(f"Suggestion {i+1}", value=suggestion, height=80, key=f"suggestion_{i}", disabled=True)
                with col2:
                    # Show character count for reference
                    st.caption(f"{len(suggestion)} chars")
                with col3:
                    if st.button("Use This", key=f"use_suggestion_{i}"):
                        process_add_text(suggestion, df, csv_path)
                        
            # Option to clear suggestions
            if st.button("Clear Suggestions", key="clear_suggestions"):
                st.session_state.text_suggestions = []
                if 'generation_params' in st.session_state:
                    del st.session_state.generation_params
                st.rerun()
            

def process_add_text(text, df, csv_path):
    """Common function to process adding text to the dataset"""
    if not text or len(text.strip()) == 0:
        st.error("Please enter some text.")
    else:
        logger.info(f"Attempting to add new text: '{text[:50]}...'" if len(text) > 50 else f"Attempting to add new text: '{text}'")
        
        success, df = add_text(df, text, csv_path)
        
        if success:
            st.success("Text added successfully!")
            # Clear any suggestions to avoid duplicates
            if 'text_suggestions' in st.session_state:
                st.session_state.text_suggestions = []
            time.sleep(1)
            st.rerun()
        else:
            st.error("Text must be between 32 and 140 characters.")