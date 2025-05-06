import logging
import os
import requests
import json

logger = logging.getLogger(__name__)

def estimate_character_count(speech_duration, language="English"):
    """
    Estimate the appropriate character count for a given speech duration
    
    Args:
        speech_duration: Speech duration in seconds
        language: Target language
        
    Returns:
        tuple: (min_length, max_length) character counts
    """
    # Approximate characters per second for various languages
    # These are rough estimates and can be adjusted
    chars_per_second = {
        "English": 15,  # ~180 words per minute, ~5 chars per word
        "German": 13,
        "French": 14,
        "Spanish": 15,
        "Italian": 15,
        "Japanese": 10,
        "Chinese": 5,
        "Korean": 8,
        "Russian": 14,
        "Arabic": 12,
        "Hindi": 13,
        "Portuguese": 15,
        "Dutch": 14,
        "Swedish": 14,
    }
    
    # Use English as fallback for unknown languages
    cps = chars_per_second.get(language, chars_per_second["English"])
    
    # Calculate target character count
    target_chars = int(speech_duration * cps)
    
    # Allow 20% variance for natural speech patterns
    min_length = max(32, int(target_chars * 0.8))
    max_length = min(140, int(target_chars * 1.2))
    
    logger.info(f"Estimated {min_length}-{max_length} characters for {speech_duration}s of speech in {language}")
    return min_length, max_length

def generate_text_suggestions(api_key, language="English", count=3, min_length=32, max_length=140, 
                             speech_duration=None, domain=None, context=None):
    """
    Generate text suggestions using Google's Gemini API
    
    Args:
        api_key: Gemini API key
        language: Target language for the suggestions
        count: Number of suggestions to generate
        min_length: Minimum text length
        max_length: Maximum text length
        speech_duration: Target speech duration in seconds (overrides min/max length if provided)
        domain: Domain or topic for the suggestions (e.g., "technology", "cooking", "healthcare")
        context: Additional context or specific requirements for the suggestions
        
    Returns:
        list: List of suggested texts, empty list if error
    """
    try:
        # If speech duration is provided, estimate appropriate character count
        if speech_duration is not None:
            min_length, max_length = estimate_character_count(speech_duration, language)
        
        # Ensure min_length and max_length are within app constraints
        min_length = max(32, min(min_length, 140))
        max_length = max(32, min(max_length, 140))
        
        # Endpoint for Gemini Pro API
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        # Add API key as query parameter
        url = f"{url}?key={api_key}"
        
        # Create domain-specific text if provided
        domain_text = ""
        if domain:
            domain_text = f"The sentences should be related to the domain or topic of '{domain}'. "
            
        # Add context if provided
        context_text = ""
        if context:
            context_text = f"Consider this specific context or requirement: '{context}'. "
        
        # Create prompt
        prompt = f"""Generate {count} natural-sounding sentences in {language} that would be good for 
        voice recording samples. Each sentence should be between {min_length} and {max_length} characters, 
        be conversational, clear, and engaging.
        {domain_text}
        {context_text}
        These sentences should take approximately {speech_duration if speech_duration else 'unknown'} seconds to read aloud.
        Make them sound natural, as if spoken by a real person.
        
        Format the output as a JSON array of strings, with no additional text or explanation.
        Example format: ["First sentence here", "Second sentence here", "Third sentence here"]
        """
        
        # Prepare request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topP": 0.95,
                "topK": 40
            }
        }
        
        # Make API request
        headers = {
            "Content-Type": "application/json"
        }
        
        logger.info(f"Requesting text suggestions from Gemini API in {language}" + 
                  (f" for domain '{domain}'" if domain else ""))
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # Check for successful response
        if response.status_code == 200:
            response_data = response.json()
            
            # Extract text from response
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                text = response_data['candidates'][0]['content']['parts'][0]['text']
                
                # Try to parse JSON array from response
                try:
                    # Extract just the JSON array part if needed
                    if '[' in text and ']' in text:
                        start_idx = text.find('[')
                        end_idx = text.rfind(']') + 1
                        json_str = text[start_idx:end_idx]
                    else:
                        json_str = text
                        
                    suggestions = json.loads(json_str)
                    
                    # Ensure suggestions are within length constraints
                    valid_suggestions = [s for s in suggestions 
                                        if isinstance(s, str) and min_length <= len(s) <= max_length]
                    
                    logger.info(f"Generated {len(valid_suggestions)} valid text suggestions")
                    return valid_suggestions
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON from Gemini response: {e}")
                    # Try to extract sentences directly if JSON parsing fails
                    sentences = [s.strip() for s in text.split('.') 
                                if min_length <= len(s.strip()) <= max_length]
                    return sentences[:count]
            
        # Log error if request failed
        logger.error(f"Gemini API request failed: {response.status_code} - {response.text}")
        return []
        
    except Exception as e:
        logger.error(f"Error generating text suggestions: {e}", exc_info=True)
        return [] 