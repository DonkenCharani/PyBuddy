# PyBuddy Code Practice and Evaluator Prompts

EXERCISE_GENERATOR_PROMPT = """
Generate a coding exercise about the Python topic: "{topic}" with difficulty level: "{difficulty}".

You must return a raw JSON object. Do not include markdown wraps like ```json ... ```. Output ONLY the JSON object.

The object must contain the following keys exactly:
- "title": (string) Short descriptive title of the exercise
- "description": (string) Explaining what the student must build. Keep instructions beginner-friendly. Define inputs and outputs.
- "starter_code": (string) A skeleton/template code (e.g. def func():) for the user to start from.
- "test_cases_description": (string) A short summary of what inputs and outputs will verify the code works.
- "hints": (array of 3 strings) Progressive hints that provide advice without giving away the final answer.

Example JSON output structure:
{{
  "title": "Filter Even Numbers",
  "description": "Write a function `filter_evens(numbers: list) -> list` that takes a list of integers and returns a new list containing only the even numbers.",
  "starter_code": "def filter_evens(numbers: list) -> list:\n    # Write your code here\n    pass",
  "test_cases_description": "Input: [1, 2, 3, 4] -> Output: [2, 4]\nInput: [5, 7, 9] -> Output: []",
  "hints": [
    "You can use a loop or a list comprehension to check each number.",
    "The modulo operator (%) can check if a number is even. A number is even if num % 2 == 0.",
    "Append even numbers to a new list and return it at the end."
  ]
}}
"""

CODE_EVALUATOR_PROMPT = """
You are grading a coding exercise submitted by a beginner student.
Topic: "{topic}"
Exercise Title: "{exercise_title}"
Problem Statement: "{exercise_description}"

Student's Submitted Code:
```python
{user_code}
```

Evaluate the code on:
1. **Correctness**: Does it satisfy the problem requirements?
2. **Logic**: Are there edge cases missed, logical flaws, or variable scoping errors?
3. **Efficiency**: Is the code unnecessarily slow or memory-heavy for a beginner level?
4. **Style**: Does it follow Pythonic style guidelines (PEP 8)?

You must return a raw JSON object. Do not include markdown wraps like ```json ... ```. Output ONLY the JSON object.

The object must contain the following keys exactly:
- "passed": (boolean) true if the code is correct and fully solves the problem, false otherwise.
- "correctness_feedback": (string) Friendly feedback about code functionality.
- "logic_feedback": (string) Evaluation of logic, structures, and variables.
- "efficiency_feedback": (string) Evaluation of performance and suggestions (e.g. time complexity, unnecessary steps).
- "style_feedback": (string) Comments on naming, structure, docstrings, formatting.
- "improvement_suggestions": (string) Summary of how to write it better.
- "hint_to_fix": (string) If they failed, give a gentle clue without revealing the answer. If they passed, give a fun challenge modification suggestion.

Remember to keep the tone of a patient PyBuddy mentor!
"""
