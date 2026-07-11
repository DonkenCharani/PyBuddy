import streamlit as st
import json
from streamlit_ace import st_ace
from utils.constants import PYTHON_TOPICS, DIFFICULTY_LEVELS
from utils.syntax import validate_syntax
from services.gemini_service import generate_response, is_api_configured
from services.database import log_practice
from prompts.evaluator import EXERCISE_GENERATOR_PROMPT, CODE_EVALUATOR_PROMPT

# Headers
st.markdown("<h1 class='gradient-header'>💻 Coding Practice</h1>", unsafe_allow_html=True)
st.markdown("<p class='gradient-subheader'>Write real Python code and receive instant structural reviews</p>", unsafe_allow_html=True)

username = st.session_state["username"]

# Initialize practice page session state keys
if "practice_exercise" not in st.session_state:
    st.session_state["practice_exercise"] = None
if "practice_topic" not in st.session_state:
    st.session_state["practice_topic"] = ""
if "practice_difficulty" not in st.session_state:
    st.session_state["practice_difficulty"] = ""
if "practice_evaluation" not in st.session_state:
    st.session_state["practice_evaluation"] = None
if "practice_syntax_error" not in st.session_state:
    st.session_state["practice_syntax_error"] = ""

# Challenge configuration menu
col1, col2, col3 = st.columns([1.5, 1, 1])
with col1:
    topic_select = st.selectbox("Select Practice Topic:", PYTHON_TOPICS, key="pr_topic_select")
with col2:
    difficulty_select = st.selectbox("Difficulty:", DIFFICULTY_LEVELS, key="pr_diff_select")
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    btn_gen = st.button("🚀 Generate Exercise", use_container_width=True)

if btn_gen:
    with st.spinner("🤖 PyBuddy is designing your challenge..."):
        try:
            if is_api_configured():
                prompt = EXERCISE_GENERATOR_PROMPT.format(topic=topic_select, difficulty=difficulty_select)
                response_text = generate_response(prompt, json_mode=True)
                
                clean_text = response_text.strip()
                if clean_text.startswith("```"):
                    clean_text = clean_text.split("```json")[-1].split("```")[0].strip()
                    
                exercise_data = json.loads(clean_text)
            else:
                # Mock backup practice exercise
                exercise_data = {
                    "title": f"Process {topic_select}",
                    "description": f"Write a function `process_data(data)` that demonstrates the usage of {topic_select}. Return the input data in a sorted list format if applicable.",
                    "starter_code": "def process_data(data):\n    # Write your code here\n    pass",
                    "test_cases_description": "Input: [3, 1, 2] -> Output: [1, 2, 3]",
                    "hints": [
                        "Review the basic concept tutorial on the Learn page.",
                        "Use built-in functions like sorted() or methods like .sort().",
                        "Ensure your function takes 'data' as parameter and has a return statement."
                    ]
                }
                
            st.session_state["practice_exercise"] = exercise_data
            st.session_state["practice_topic"] = topic_select
            st.session_state["practice_difficulty"] = difficulty_select
            st.session_state["practice_evaluation"] = None
            st.session_state["practice_syntax_error"] = ""
            st.rerun()
            
        except Exception as e:
            st.error(f"Could not generate exercise: {str(e)}")

# Render active coding workspace
if st.session_state["practice_exercise"]:
    ex = st.session_state["practice_exercise"]
    t_topic = st.session_state["practice_topic"]
    t_diff = st.session_state["practice_difficulty"]
    
    st.markdown(f"## 🏆 {ex['title']} ({t_diff})")
    st.markdown(f"**Topic**: `{t_topic}`")
    
    # Description column layout
    d_col, e_col = st.columns([1, 1])
    with d_col:
        st.markdown("### 📝 Instruction")
        st.markdown(
            f"""
            <div style='background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 15px;'>
                {ex['description']}
            </div>
            """, 
            unsafe_allow_html=True
        )

    with e_col:
        st.markdown("### 🔬 Expected Outputs")

        formatted_test_cases = ex["test_cases_description"].replace("\n", "<br>")

        st.markdown(
            f"""
            <div style='background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 15px;'>
                <code>{formatted_test_cases}</code>
            </div>
            """,
            unsafe_allow_html=True
        )
    # Progressive hints expander
    st.markdown("### 💡 Progressive Hints")
    h_col1, h_col2, h_col3 = st.columns(3)
    with h_col1:
        with st.expander("Hint 1"):
            st.info(ex["hints"][0])
    with h_col2:
        with st.expander("Hint 2 (More helpful)"):
            st.info(ex["hints"][1])
    with h_col3:
        with st.expander("Hint 3 (Direct approach)"):
            st.info(ex["hints"][2])
            
    # Ace Editor Container
    st.markdown("### 🐍 Code Editor")
    
    # Render streamlit-ace editor
    code_submission = st_ace(
        value=ex["starter_code"],
        language="python",
        theme="monokai",
        keybinding="vscode",
        font_size=14,
        tab_size=4,
        min_lines=15,
        max_lines=25,
        wrap=True,
        key="practice_ace"
    )
    
    btn_submit = st.button("Submit Code for Review", use_container_width=True)
    
    if btn_submit:
        # 1. AST Syntax validation checks
        is_syntactically_valid, error_msg = validate_syntax(code_submission)
        
        if not is_syntactically_valid:
            st.session_state["practice_syntax_error"] = error_msg
            st.session_state["practice_evaluation"] = None
        else:
            st.session_state["practice_syntax_error"] = ""
            with st.spinner("🤖 Evaluating your code..."):
                try:
                    # 2. AI Code evaluation checks
                    eval_prompt = CODE_EVALUATOR_PROMPT.format(
                        topic=t_topic,
                        exercise_title=ex["title"],
                        exercise_description=ex["description"],
                        user_code=code_submission
                    )
                    
                    if is_api_configured():
                        response_text = generate_response(eval_prompt, json_mode=True)
                        clean_text = response_text.strip()
                        if clean_text.startswith("```"):
                            clean_text = clean_text.split("```json")[-1].split("```")[0].strip()
                        eval_data = json.loads(clean_text)
                    else:
                        # Demo Mode Evaluator response
                        eval_data = {
                            "passed": True,
                            "correctness_feedback": "Demo mode: Code syntax is valid!",
                            "logic_feedback": "Looks like reasonable structure.",
                            "efficiency_feedback": "No performance bottlenecks detected.",
                            "style_feedback": "Indentation matches AST standards.",
                            "improvement_suggestions": "Configure API Key for live reviews.",
                            "hint_to_fix": "Add GEMINI_API_KEY in .env to get detailed comments."
                        }
                        
                    st.session_state["practice_evaluation"] = eval_data
                    
                    # Log practice submission in SQLite
                    log_practice(
                        username,
                        ex["title"],
                        t_diff,
                        code_submission,
                        json.dumps(eval_data),
                        eval_data["passed"]
                    )
                    
                except Exception as e:
                    st.error(f"Evaluation error: {str(e)}")
                    
    # Render errors or evaluation report
    if st.session_state["practice_syntax_error"]:
        st.markdown("### ⚠️ Compilation Issue")
        st.error(st.session_state["practice_syntax_error"])
        
    elif st.session_state["practice_evaluation"]:
        report = st.session_state["practice_evaluation"]
        
        st.markdown("---")
        st.markdown("## 📊 Evaluation Report")
        
        # Pass/Fail Banner
        if report["passed"]:
            st.success("🎉 Challenge Passed! Excellent work!")
        else:
            st.warning("💪 Needs work. Check the feedback below and fix the issues.")
            
        # Detail reviews grid columns
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.markdown(f"""
            <div style='background: rgba(30, 41, 59, 0.6); border-radius: 8px; padding: 15px; margin-bottom: 12px;'>
                <b style='color: #FFE082;'>✅ Correctness:</b><br>{report['correctness_feedback']}
            </div>
            <div style='background: rgba(30, 41, 59, 0.6); border-radius: 8px; padding: 15px;'>
                <b style='color: #FFE082;'>⚙️ Logic & Structure:</b><br>{report['logic_feedback']}
            </div>
            """, unsafe_allow_html=True)
            
        with f_col2:
            st.markdown(f"""
            <div style='background: rgba(30, 41, 59, 0.6); border-radius: 8px; padding: 15px; margin-bottom: 12px;'>
                <b style='color: #FFE082;'>⚡ Efficiency:</b><br>{report['efficiency_feedback']}
            </div>
            <div style='background: rgba(30, 41, 59, 0.6); border-radius: 8px; padding: 15px;'>
                <b style='color: #FFE082;'>🎨 Style & PEP 8:</b><br>{report['style_feedback']}
            </div>
            """, unsafe_allow_html=True)
            
        # Review summaries
        st.markdown("### 💡 Suggestions for Improvement")
        st.info(report["improvement_suggestions"])
        
        if not report["passed"]:
            st.markdown("### 🔍 Fix Clue")
            st.info(report["hint_to_fix"])
        else:
            st.markdown("### 🏆 Fun Modification Challenge")
            st.success(report["hint_to_fix"])
