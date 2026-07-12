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
You are an extremely strict Python coding evaluator.

Topic:
{topic}

Exercise:
{exercise_title}

Problem:
{exercise_description}

Student Code:
```python
{user_code}
```

Your task is to determine whether the student's solution is COMPLETELY correct.

Evaluation Rules:

1. Read the problem carefully.
2. Mentally execute the code.
3. Compare the returned output with what the problem asks.
4. Consider normal inputs and edge cases.
5. If the code would fail even ONE reasonable test case, set passed=false.
6. Wrong slicing, wrong return values, off-by-one errors, missing cases, incorrect algorithms or logic errors must result in passed=false.
7. Only use passed=true when you are completely confident the solution is correct.

Return ONLY a valid JSON object.

Do NOT explain anything.
Do NOT use markdown.
Do NOT wrap the JSON inside ```json.
Return exactly this structure:

{{
  "passed": false,
  "correctness_feedback": "",
  "logic_feedback": "",
  "efficiency_feedback": "",
  "style_feedback": "",
  "improvement_suggestions": "",
  "hint_to_fix": ""
}}
"""