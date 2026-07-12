import json
import re

def parse_json_response(text: str):
    if not text:
        raise ValueError("Empty response from Gemini.")

    text = text.strip()

    # Remove markdown
    text = text.replace("```json", "")
    text = text.replace("```", "")

    # Extract JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found.")

    return json.loads(match.group())