# PyBuddy – AI Python Learning Buddy

PyBuddy is a production-quality, interactive, AI-powered Python tutoring web application designed specifically for beginners. 
Built using **Streamlit**, **Google Gemini API**, **SQLite**, and **Plotly**, PyBuddy acts as a personalized learning companion that teaches concepts, runs quizzes, evaluates code scripts, explains mistakes, diagnoses code bugs, and tracks learning progress.

---

## Key Features

### 1. Welcome Dashboard (Home Page)
- Modern gradient-themed interface with feature overview cards.
- **Python Tip of the Day** and **Random Python Fact** panels that refresh on session reload.
- **Daily Python Challenge** widget presenting mini-tasks with reference solutions and interactive hints.

### 2. Interactive Tutor (Learn Page)
- Choose from standard Python topics (from basic variables to async programming) or input custom topics.
- Pick an activity mode: Concept Explanation, Visual Analogy, Best Practices, Common Mistakes, Code Walkthroughs, and Cheat Sheets.
- **Gamification**: Logs reading events in the SQLite history database and awards XP.
- **Downloads & Favorites**: Bookmark favorite guides or export lessons to beautifully structured PDFs instantly.

### 3. Knowledge Quiz (Quiz Page)
- Dynamically generates 5 multi-choice questions (MCQs) for any topic and difficulty (Easy, Medium, Hard).
- Fully stateful interface to prevent quiz reset on click.
- Provides immediate grading metrics (Scores and Percentages), notes weak topics, and supplies line-by-line review explanations.
- Export review reports to PDF.

### 4. Coding Practice (Code Practice Page)
- Custom coding exercises designed by AI based on selected topics.
- Embedded high-performance code editor powered by **Streamlit-Ace** (with line numbers, syntax highlighting, and VSCode keybindings).
- **AST-Based Validator**: Scans submitted code syntax locally to catch syntax errors immediately without consuming API quota.
- **AI Evaluator**: Grades code logic, efficiency, correctness, and style guidelines (PEP 8) while giving progressive clues instead of revealing the answer.

### 5. Code Debugger (Debugger Page)
- Paste broken code and console tracebacks.
- AI diagnoses bugs, lists line-by-line code corrections, displays working code, and provides coding tips for the future.

### 6. Progress Tracker (Progress Page)
- Gamified dashboard tracking XP points, active streaks, and accomplishments.
- Interactive **Plotly charts**: Score trends over time, exercise statuses by difficulty, and learning intensity by topic.
- **AI Study Planner**: Formulates custom weekly study plans based on personal goals. Plans are saved in the database as an interactive checklist.

### 7. About & Extras (About Page)
- Project stack information and Responsible AI Safety guidelines.
- **Saved Bookmarks Manager**: Review and remove saved study notes and quizzes.
- **Interactive Flashcards**: Study cards that flip on click to reveal definitions and syntax examples.
- **Career Roadmap**: Multi-step guide detailing the path from Python novice to expert.
- **Job Interview Prep**: Collapsible panels with common Junior, Mid, and Senior interview questions.
- **Mini Python Dictionary**: Index of core Python keywords with search bar filtering.

---

## Folder Structure

```
PyBuddy/
│
├── app.py                     # Entry point & navigation routing
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
├── .env.example               # Environment variables template
├── .gitignore                 # Excluded directories checklist
│
├── assets/                    # Graphic assets (automatically generated on start)
│   ├── logo.png
│   └── banner.png
│
├── data/                      # Persistent database storage
│   └── progress.db
│
├── prompts/                   # Structured AI prompt templates
│   ├── explain.py
│   ├── example.py
│   ├── quiz.py
│   ├── evaluator.py
│   ├── debugger.py
│   └── session.py
│
├── services/                  # Business & API logic layers
│   ├── gemini_service.py      # Google Gemini API client
│   ├── database.py            # SQLite database queries & schemas
│   ├── quiz_engine.py         # MCQ generator & local fallback quizzes
│   └── analytics.py           # Dataframe processing & Plotly plots
│
└── utils/                     # Utility and formatting layers
    ├── helpers.py             # PDF generation, dates, & asset creator
    ├── syntax.py              # AST compiler checker & black code formatter
    └── constants.py           # Flashcards, interview Qs, dictionary, facts
```

---

## Getting Started

### 1. Prerequisites
Ensure you have **Python 3.11** or higher installed.

### 2. Installation
Clone the repository and install the dependencies listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. API Setup
Get a free Gemini API key from the [Google AI Studio](https://aistudio.google.com/). 
Create a `.env` file in the project root directory and paste your key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*Note: If the key is not defined in `.env`, you can input it dynamically in the sidebar text field during runtime.*

### 4. Running the Application
Launch the Streamlit server from the project root directory:
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501` to start learning with PyBuddy!

---

## Responsible AI & Safety
- PyBuddy features explicit safety system prompts that prevent the model from generating malicious code (e.g. keyloggers, viruses) or assisting in cyberattacks.
- It displays a mandatory disclaimer outlining that AI can make mistakes and students should verify critical information.
- Utilizes Google's default moderation categories (Harassment, Hate Speech, Sexually Explicit, and Dangerous Content) set to block harmful topics at a medium-and-above threshold.

---

## Future Improvements
1. **Coding Playground**: Integration of a secure Python sandbox to run code outputs directly in the browser.
2. **Leaderboards**: Support for multi-user accounts and global competitive ranking leaderboards.
3. **Advanced Analytics**: Deeper metrics analyzing topic mastery speed, time spent per code problem, and customized quiz retakes.
4. **Voice Assistance**: Integration of text-to-speech for vocal concept tutoring.
