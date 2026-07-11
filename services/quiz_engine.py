import json
import random
from services.gemini_service import generate_response, is_api_configured
from prompts.quiz import QUIZ_GENERATOR_PROMPT

def generate_quiz(topic: str, difficulty: str) -> list[dict]:
    """
    Generates a list of 5 multiple-choice questions for a specific topic and difficulty.
    Uses Gemini API if configured; otherwise, falls back to a high-quality local generator.
    """
    if is_api_configured():
        prompt = QUIZ_GENERATOR_PROMPT.format(topic=topic, difficulty=difficulty)
        try:
            response_text = generate_response(prompt, json_mode=True)
            # Remove any outer markdown formatting that some models return despite json_mode
            clean_text = response_text.strip()
            if clean_text.startswith("```"):
                # strip code block formatting
                clean_text = clean_text.split("```json")[-1].split("```")[0].strip()
                
            quiz_data = json.loads(clean_text)
            
            # Basic structural validation
            validated_questions = []
            for q in quiz_data:
                if all(k in q for k in ("id", "question", "options", "correct_option_index", "explanation")):
                    if len(q["options"]) == 4:
                        validated_questions.append(q)
            
            if len(validated_questions) == 5:
                return validated_questions
                
        except Exception as e:
            # If API fails or parsing fails, fall back to local mock quiz
            pass

    # Fallback / Mock quiz generator (keeps the app robust)
    return get_local_backup_quiz(topic, difficulty)

def get_local_backup_quiz(topic: str, difficulty: str) -> list[dict]:
    """Generates a high-quality local quiz when Gemini is unavailable."""
    # We will generate mock questions based on the topic.
    templates = [
        {
            "question": f"Which of the following statements about {topic} in Python is true?",
            "options": [
                f"It is a core feature used to structure Python programs efficiently.",
                f"It is deprecated in Python 3 and should be avoided.",
                f"It requires importing an external C library to function.",
                f"It can only be used inside the global namespace."
            ],
            "correct_option_index": 0,
            "explanation": f"{topic} is a fundamental concept in Python designed to make code clean, modular, and maintainable."
        },
        {
            "question": f"What is a common error or pitfall when working with {topic}?",
            "options": [
                "Raising a SyntaxError due to incorrect indentation or keyword spelling.",
                "Executing the code causes the computer's CPU to overheat.",
                "It automatically deletes all local text files.",
                "It requires wrapping all variables inside a tuple."
            ],
            "correct_option_index": 0,
            "explanation": "Indentations and typing correct keywords are crucial syntax rules in Python."
        },
        {
            "question": f"How does a beginner master {topic} according to best practices?",
            "options": [
                "By writing small test programs, running them, and analyzing the output.",
                "By memorizing the entire Python documentation word for word.",
                "By only writing code in notepad without syntax highlighting.",
                "By avoiding coding practice altogether."
            ],
            "correct_option_index": 0,
            "explanation": "Interactive practice, trial and error, and debugging are the best ways to learn programming concepts."
        },
        {
            "question": f"Which built-in Python function or keyword is closely associated with {topic}?",
            "options": [
                "It depends on the context, but Python's built-ins are always optimized.",
                "The 'goto' statement.",
                "The 'malloc' allocation function.",
                "The 'include' directive."
            ],
            "correct_option_index": 0,
            "explanation": "Python has a rich set of built-in functions, keywords, and standard library components."
        },
        {
            "question": f"Why is {topic} considered important in Python software design?",
            "options": [
                "It improves readability, supports code reusability, and fits Python's clean code philosophy.",
                "It speeds up execution to make Python run faster than C.",
                "It forces Python to use static compilation instead of dynamic typing.",
                "It is a requirement for running Python on mobile devices."
            ],
            "correct_option_index": 0,
            "explanation": "Proper use of programming structures increases project structure readability, scalability, and code reuse."
        }
    ]
    
    # Randomize the correct options and structure the response
    quiz = []
    for i, t in enumerate(templates):
        opts = list(t["options"])
        correct = opts[0]
        # Shuffle options
        random.shuffle(opts)
        correct_idx = opts.index(correct)
        
        quiz.append({
            "id": i + 1,
            "question": t["question"],
            "options": opts,
            "correct_option_index": correct_idx,
            "explanation": t["explanation"]
        })
    return quiz
