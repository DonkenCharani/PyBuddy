# PyBuddy Explanation and Concept Prompts

EXPLAIN_CONCEPT_PROMPT = """
Explain the Python concept: "{topic}" to a beginner.

Your explanation must follow this clean structure:
1. **Introduction**: A clear, 2-3 sentence high-level overview.
2. **Key Analogy**: Translate the abstract idea into a physical or everyday action.
3. **Core Syntax**: Show a clean, basic Python code example. Document it thoroughly with comments.
4. **Line-by-Line Walkthrough**: Break down the code example, explaining what each keyword/symbol is doing.
5. **A Quick Quiz Question**: Provide a quick, simple 1-question check that they can think about.

Remember the PyBuddy persona: keep it encouraging and ask if they'd like another example!
"""

VISUAL_ANALOGY_PROMPT = """
Explain the Python concept: "{topic}" using a vivid visual analogy.

Create a relatable scenario (e.g., cooking in a kitchen, a post office, organizing a bookshelf, assembling a LEGO set).
Draw explicit comparisons between the components of the analogy and the parts of the Python code.

Include a code block that represents this analogy, complete with comments.
"""

BEST_PRACTICES_PROMPT = """
Explain the best practices when writing or using "{topic}" in Python.

Provide:
1. **Rule of Thumb**: General guidelines.
2. **DOs & DON'Ts**: Code examples of "How NOT to do it" vs. "The Pythonic Way (How to do it)".
3. **Why it matters**: Explain performance, memory, or readability impacts.
"""

COMMON_MISTAKES_PROMPT = """
Detail the most common mistakes beginners make when working with "{topic}" in Python.

Provide:
1. **Mistake Example**: Broken or buggy code snippet.
2. **Why it fails**: Explain the common misconception or syntax/logic error.
3. **The Fix**: Corrected code snippet with comments.
"""

CHEAT_SHEET_PROMPT = """
Generate a comprehensive, compact Cheat Sheet for the Python topic: "{topic}".

Include:
1. **Quick Syntax Cheat List**: Brief definitions and one-liner code examples.
2. **Essential Methods / Functions**: A small table or bullet list of common methods associated with this topic (if applicable).
3. **Common Tricks**: Simple short-cuts.
"""

INTERVIEW_PREP_PROMPT = """
Provide an Interview Explanation for the Python topic: "{topic}".

Imagine a junior candidate is asked about this topic in a software engineering interview.
Provide:
1. **The 30-Second Elevator Pitch**: A concise, professional response.
2. **Key Concepts to Mention**: Buzzwords/details they must include in their answer.
3. **Possible Follow-up Questions**: 2-3 advanced questions the interviewer might ask, along with brief answers.
"""

STUDY_PLANNER_PROMPT = """
Create a personalized, step-by-step Study Planner to master the following goal: "{goal}" in Python over a duration of {weeks} weeks.

You must return a raw JSON array of objects. Do not include markdown wraps like ```json ... ```. Output ONLY the JSON array.
Each object in the array represents a week and must contain the following keys exactly:
- "week": (integer) The week number (e.g., 1, 2, 3...)
- "title": (string) High-level topic title for the week
- "topics": (list of strings) Sub-topics to study
- "tasks": (list of strings) Hands-on tasks/mini-projects to build
- "challenge": (string) A weekly test/quiz goal

Example JSON structure:
[
  {{
    "week": 1,
    "title": "Basics of the topic",
    "topics": ["subtopic A", "subtopic B"],
    "tasks": ["Task 1", "Task 2"],
    "challenge": "Write a program that does X"
  }}
]
"""
