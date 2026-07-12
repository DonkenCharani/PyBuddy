import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts.session import SYSTEM_INSTRUCTION

load_dotenv()

_client = None


def get_api_key():
    if st.session_state.get("api_key"):
        return st.session_state["api_key"]
    return os.getenv("GEMINI_API_KEY")


def is_api_configured():
    key = get_api_key()
    return bool(key)


def get_client():
    global _client

    if _client is None:
        key = get_api_key()

        if not key:
            raise ValueError(
                "Gemini API Key is missing. Add it to your .env file or sidebar."
            )

        _client = genai.Client(api_key=key)

    return _client


def generate_response(
    prompt: str,
    custom_system_instruction: str = None,
    json_mode: bool = False,
):

    system_instruction = (
        custom_system_instruction
        if custom_system_instruction
        else SYSTEM_INSTRUCTION
    )

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
    )

    if json_mode:
        config.response_mime_type = "application/json"

    try:
        response = get_client().models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=config,
        )

        if not response.text:
            return "Gemini returned an empty response."

        return response.text

    except Exception as e:
        raise RuntimeError(str(e))