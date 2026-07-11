import sqlite3
import os
import json
from datetime import datetime, date
from utils.helpers import calculate_streak

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "progress.db")

# Ensure data directory exists
os.makedirs(DB_DIR, exist_ok=True)

def get_connection():
    """Returns a sqlite3 connection object with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if tables do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Users Table (gamification elements)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                joined_at TEXT NOT NULL,
                streak_days INTEGER DEFAULT 0,
                last_active_date TEXT,
                xp INTEGER DEFAULT 0
            )
        """)
        
        # 2. History Table (concept logs)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                topic TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                response_text TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
            )
        """)
        
        # 3. Quiz Results Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                quiz_topic TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                weak_topics TEXT,
                feedback TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
            )
        """)
        
        # 4. Practice Table (coding exercises)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS practice (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                exercise_title TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                user_code TEXT NOT NULL,
                evaluation_feedback TEXT NOT NULL,
                passed INTEGER NOT NULL, -- 0 for false, 1 for true
                created_at TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
            )
        """)
        
        # 5. Bookmarks Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                item_type TEXT NOT NULL, -- 'concept', 'code_practice', 'cheat_sheet'
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(username, item_type, title),
                FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
            )
        """)

        # 6. Study Plans Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                goal TEXT NOT NULL,
                duration INTEGER NOT NULL, -- in weeks
                plan_json TEXT NOT NULL,
                completed_tasks TEXT DEFAULT '[]', -- JSON list of strings (completed task titles)
                created_at TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
            )
        """)
        
        conn.commit()

# --- User Management & Streak ---

def get_or_create_user(username: str) -> dict:
    """Fetches user details, creates user if they don't exist."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        else:
            joined = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO users (username, joined_at, streak_days, last_active_date, xp) VALUES (?, ?, 0, NULL, 0)",
                (username, joined)
            )
            conn.commit()
            return {"username": username, "joined_at": joined, "streak_days": 0, "last_active_date": None, "xp": 0}

def update_user_activity(username: str, xp_gained: int = 0):
    """
    Updates user last active date, recalculates streak, and adds XP.
    """
    user = get_or_create_user(username)
    last_active = user["last_active_date"]
    current_streak = user["streak_days"]
    current_xp = user["xp"]
    
    new_streak = calculate_streak(last_active, current_streak)
    new_xp = current_xp + xp_gained
    today_str = date.today().isoformat()
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET last_active_date = ?, streak_days = ?, xp = ? WHERE username = ?",
            (today_str, new_streak, new_xp, username)
        )
        conn.commit()

# --- History & Learning Logs ---

def log_concept(username: str, topic: str, activity_type: str, response_text: str):
    """Logs the concept reading activity and awards 10 XP."""
    update_user_activity(username, xp_gained=10)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (username, topic, activity_type, response_text, created_at) VALUES (?, ?, ?, ?, ?)",
            (username, topic, activity_type, response_text, datetime.now().isoformat())
        )
        conn.commit()

def get_concept_history(username: str) -> list[dict]:
    """Retrieves all concept history for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history WHERE username = ? ORDER BY id DESC", (username,))
        return [dict(r) for r in cursor.fetchall()]

# --- Quiz Logs ---

def log_quiz(username: str, topic: str, difficulty: str, score: int, total: int, weak_topics: str, feedback: str):
    """Logs a completed quiz. Awards 10 XP base + 10 XP per correct answer."""
    xp_gained = 10 + (score * 10)
    update_user_activity(username, xp_gained=xp_gained)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO quiz_results 
               (username, quiz_topic, difficulty, score, total_questions, weak_topics, feedback, created_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (username, topic, difficulty, score, total, weak_topics, feedback, datetime.now().isoformat())
        )
        conn.commit()

def get_quiz_results(username: str) -> list[dict]:
    """Retrieves all quiz results for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quiz_results WHERE username = ? ORDER BY id DESC", (username,))
        return [dict(r) for r in cursor.fetchall()]

# --- Coding Practice Logs ---

def log_practice(username: str, exercise_title: str, difficulty: str, user_code: str, evaluation_feedback: str, passed: bool):
    """Logs a practice submission. Awards 30 XP if passed, 5 XP otherwise."""
    xp_gained = 30 if passed else 5
    update_user_activity(username, xp_gained=xp_gained)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO practice 
               (username, exercise_title, difficulty, user_code, evaluation_feedback, passed, created_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (username, exercise_title, difficulty, user_code, evaluation_feedback, 1 if passed else 0, datetime.now().isoformat())
        )
        conn.commit()

def get_practice_results(username: str) -> list[dict]:
    """Retrieves all practice results for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM practice WHERE username = ? ORDER BY id DESC", (username,))
        return [dict(r) for r in cursor.fetchall()]

# --- Bookmarks ---

def add_bookmark(username: str, item_type: str, title: str, content: str) -> bool:
    """Adds a bookmark. Returns True if added, False if duplicate."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bookmarks (username, item_type, title, content, created_at) VALUES (?, ?, ?, ?, ?)",
                (username, item_type, title, content, datetime.now().isoformat())
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def remove_bookmark(username: str, item_type: str, title: str):
    """Removes a bookmark."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM bookmarks WHERE username = ? AND item_type = ? AND title = ?",
            (username, item_type, title)
        )
        conn.commit()

def get_bookmarks(username: str) -> list[dict]:
    """Retrieves all bookmarks for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookmarks WHERE username = ? ORDER BY id DESC", (username,))
        return [dict(r) for r in cursor.fetchall()]

def is_bookmarked(username: str, item_type: str, title: str) -> bool:
    """Checks if a specific item is bookmarked."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM bookmarks WHERE username = ? AND item_type = ? AND title = ?",
            (username, item_type, title)
        )
        return cursor.fetchone() is not None

# --- Study Plans ---

def save_study_plan(username: str, goal: str, duration: int, plan_json: str):
    """Saves a study plan. Awards 20 XP."""
    update_user_activity(username, xp_gained=20)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO study_plans (username, goal, duration, plan_json, completed_tasks, created_at) VALUES (?, ?, ?, ?, '[]', ?)",
            (username, goal, duration, plan_json, datetime.now().isoformat())
        )
        conn.commit()

def get_study_plans(username: str) -> list[dict]:
    """Retrieves all study plans for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM study_plans WHERE username = ? ORDER BY id DESC", (username,))
        return [dict(r) for r in cursor.fetchall()]

def update_study_plan_tasks(plan_id: int, completed_tasks_list: list[str]):
    """Updates the completed tasks list for a study plan."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE study_plans SET completed_tasks = ? WHERE id = ?",
            (json.dumps(completed_tasks_list), plan_id)
        )
        conn.commit()

def delete_study_plan(plan_id: int):
    """Deletes a specific study plan."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM study_plans WHERE id = ?", (plan_id,))
        conn.commit()
