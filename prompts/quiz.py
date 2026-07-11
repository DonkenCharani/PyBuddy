# PyBuddy Quiz Prompts

QUIZ_GENERATOR_PROMPT = """
Generate a {difficulty}-difficulty multiple-choice quiz about the Python topic: "{topic}".
The quiz must contain exactly 5 questions.

You must return a raw JSON array of objects. Do not include markdown wraps like ```json ... ```. Output ONLY the JSON array.

Each question object in the array must contain the following keys exactly:
- "id": (integer) A unique question ID (1 to 5)
- "question": (string) The question text
- "options": (array of 4 strings) A list of four distinct multiple-choice options
- "correct_option_index": (integer) The 0-based index of the correct option in the options list (0, 1, 2, or 3)
- "explanation": (string) A beginner-friendly explanation of why this answer is correct and why other answers are wrong

Example JSON output structure:
[
  {{
    "id": 1,
    "question": "What is the output of print(2 ** 3)?",
    "options": ["6", "8", "9", "Error"],
    "correct_option_index": 1,
    "explanation": "The double asterisk (**) is the exponentiation operator in Python. Thus, 2 ** 3 represents 2 raised to the power of 3, which equals 8."
  }}
]
"""
