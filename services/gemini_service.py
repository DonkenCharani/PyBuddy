import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from prompts.session import SYSTEM_INSTRUCTION

# Load environment variables
load_dotenv()

def get_api_key() -> str | None:
    """
    Retrieves the Gemini API key. 
    Checks streamlit session state first, then checks environment variables.
    """
    if "api_key" in st.session_state and st.session_state["api_key"]:
        return st.session_state["api_key"]
    return os.getenv("GEMINI_API_KEY")

def is_api_configured() -> bool:
    """Returns True if a Gemini API key is available."""
    key = get_api_key()
    return bool(key and key.strip())

def generate_response(prompt: str, custom_system_instruction: str = None, json_mode: bool = False) -> str:
    """
    Generates content using Google's gemini-1.5-flash model.
    Supports system instructions and JSON structured output formatting.
    """
    key = get_api_key()
    if not key or not key.strip():
        raise ValueError(
            "Gemini API Key is missing. Please supply your API key in the sidebar "
            "or set it as GEMINI_API_KEY in a .env file."
        )
    
    # Configure genai with the retrieved key
    genai.configure(api_key=key.strip())
    
    # Setup generation configuration
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "max_output_tokens": 8192,
    }
    
    if json_mode:
        generation_config["response_mime_type"] = "application/json"
        
    system_instr = custom_system_instruction if custom_system_instruction else SYSTEM_INSTRUCTION
    
    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=system_instr,
            generation_config=generation_config
        )
        
        # Responsible AI: Moderate output content implicitly using safety settings
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        response = model.generate_content(prompt, safety_settings=safety_settings)
        
        # Verify if prompt was blocked
        if not response.text:
            if hasattr(response, "prompt_feedback") and response.prompt_feedback.block_reason:
                return f"Error: Request blocked by Gemini Safety Filters due to: {response.prompt_feedback.block_reason}"
            return "Error: Gemini returned an empty response. The prompt may have violated safety policies."
            
        return response.text
        
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg:
            raise ValueError("The provided Gemini API Key is invalid. Please double-check your key.")
        elif "ResourceExhausted" in error_msg or "quota" in error_msg.lower():
            raise RuntimeError("API quota limits reached. Please try again in a few moments.")
        else:
            raise RuntimeError(f"Error calling Gemini API: {error_msg}")
