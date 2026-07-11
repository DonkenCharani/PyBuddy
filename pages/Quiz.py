import streamlit as st
from utils.constants import PYTHON_TOPICS, DIFFICULTY_LEVELS
from utils.helpers import generate_pdf
from services.quiz_engine import generate_quiz
from services.database import log_quiz, add_bookmark, is_bookmarked, remove_bookmark

# Headers
st.markdown("<h1 class='gradient-header'>📝 Knowledge Quiz</h1>", unsafe_allow_html=True)
st.markdown("<p class='gradient-subheader'>Test your knowledge and get personalized study feedback</p>", unsafe_allow_html=True)

username = st.session_state["username"]

# Initialize Quiz states in Session State
if "quiz_questions" not in st.session_state:
    st.session_state["quiz_questions"] = []
if "quiz_answers" not in st.session_state:
    st.session_state["quiz_answers"] = {}
if "quiz_submitted" not in st.session_state:
    st.session_state["quiz_submitted"] = False
if "quiz_topic" not in st.session_state:
    st.session_state["quiz_topic"] = ""
if "quiz_difficulty" not in st.session_state:
    st.session_state["quiz_difficulty"] = ""

# Quiz Configuration Layout
col1, col2, col3 = st.columns([1.5, 1, 1])
with col1:
    topic_select = st.selectbox("Select Quiz Topic:", PYTHON_TOPICS)
with col2:
    difficulty_select = st.selectbox("Difficulty:", DIFFICULTY_LEVELS)
with col3:
    st.markdown("<br>", unsafe_allow_html=True) # spacing
    btn_start = st.button("🏁 Start Quiz", use_container_width=True)

if btn_start:
    with st.spinner("🧠 PyBuddy is compiling your quiz..."):
        # Reset and generate
        st.session_state["quiz_questions"] = generate_quiz(topic_select, difficulty_select)
        st.session_state["quiz_answers"] = {}
        st.session_state["quiz_submitted"] = False
        st.session_state["quiz_topic"] = topic_select
        st.session_state["quiz_difficulty"] = difficulty_select
        st.rerun()

# Render active quiz
if st.session_state["quiz_questions"]:
    active_questions = st.session_state["quiz_questions"]
    q_topic = st.session_state["quiz_topic"]
    q_diff = st.session_state["quiz_difficulty"]
    
    st.markdown(f"### {q_topic} ({q_diff} Quiz)")
    
    # Form container to group questions
    with st.form("quiz_form"):
        for index, q in enumerate(active_questions):
            q_num = index + 1
            st.markdown(f"**Q{q_num}. {q['question']}**")
            
            # Find default selection index to avoid resetting radio buttons
            default_val = st.session_state["quiz_answers"].get(q["id"], None)
            
            # Map key ID string for radios
            ans = st.radio(
                f"Choose option for Q{q_num}:",
                q["options"],
                index=None if default_val is None else q["options"].index(default_val),
                key=f"q_radio_{q['id']}",
                label_visibility="collapsed"
            )
            if ans is not None:
                st.session_state["quiz_answers"][q["id"]] = ans
            st.markdown("<br>", unsafe_allow_html=True)
            
        form_submit = st.form_submit_button("Submit Answers")
        
        if form_submit:
            # Check if all questions answered
            if len(st.session_state["quiz_answers"]) < 5:
                st.warning("Please answer all 5 questions before submitting!")
            else:
                st.session_state["quiz_submitted"] = True
                st.rerun()

# Handle Quiz Grading and Results display
if st.session_state["quiz_submitted"] and st.session_state["quiz_questions"]:
    active_questions = st.session_state["quiz_questions"]
    answers = st.session_state["quiz_answers"]
    q_topic = st.session_state["quiz_topic"]
    q_diff = st.session_state["quiz_difficulty"]
    
    score = 0
    weak_categories = set()
    quiz_summary = []
    
    st.markdown("---")
    st.markdown("## 📊 Quiz Results Summary")
    
    # Render grading detail cards
    for idx, q in enumerate(active_questions):
        user_ans = answers.get(q["id"])
        correct_idx = q["correct_option_index"]
        correct_ans = q["options"][correct_idx]
        
        is_correct = (user_ans == correct_ans)
        if is_correct:
            score += 1
        else:
            weak_categories.add(q_topic)
            
        quiz_summary.append({
            "num": idx + 1,
            "question": q["question"],
            "user_ans": user_ans,
            "correct_ans": correct_ans,
            "explanation": q["explanation"],
            "status": "Passed" if is_correct else "Failed"
        })
        
    percent = (score / 5) * 100
    
    # Display Score metrics
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.metric(label="Score", value=f"{score} / 5")
    with s_col2:
        st.metric(label="Percentage", value=f"{percent:.1f}%")
        
    if percent == 100:
        st.balloons()
        st.success("🏆 Perfect Score! You've mastered this topic!")
    elif percent >= 60:
        st.success("🎉 Good job! You have a solid grasp of this topic.")
    else:
        st.warning("💪 Don't worry! Review the explanations below and try again to improve.")
        
    # Weak topics and study recommendations
    st.markdown("### 💡 Recommended Focus")
    if weak_categories:
        st.markdown(f"You should spend a bit more time reviewing **{', '.join(weak_categories)}**.")
        st.write("We recommend checking the **Learn Concepts** page for detailed explanations or visual analogies on this topic.")
    else:
        st.write("Excellent performance! You seem to understand all concepts in this set.")

    # Log results to SQLite DB
    weak_str = ", ".join(weak_categories) if weak_categories else "None"
    feedback_str = f"Scored {score}/5 on {q_topic} ({q_diff}). Percentage: {percent:.1f}%"
    log_quiz(username, q_topic, q_diff, score, 5, weak_str, feedback_str)
    
    # Export and Bookmark options
    st.markdown("### 🛠️ Actions")
    act_col1, act_col2 = st.columns(2)
    
    # Create text report
    quiz_report_text = f"Quiz Topic: {q_topic}\nDifficulty: {q_diff}\nScore: {score}/5 ({percent:.1f}%)\n\n"
    for s in quiz_summary:
        quiz_report_text += f"Q{s['num']}: {s['question']}\nYour Answer: {s['user_ans']} [{s['status']}]\nCorrect Answer: {s['correct_ans']}\nExplanation: {s['explanation']}\n\n"

    with act_col1:
        # Check bookmark
        booked = is_bookmarked(username, "quiz", f"{q_topic} ({q_diff}) Quiz")
        if booked:
            if st.button("❤️ Remove Saved Quiz"):
                remove_bookmark(username, "quiz", f"{q_topic} ({q_diff}) Quiz")
                st.toast("Removed from bookmarks!")
                st.rerun()
        else:
            if st.button("➕ Save Quiz Review"):
                add_bookmark(username, "quiz", f"{q_topic} ({q_diff}) Quiz", quiz_report_text)
                st.toast("Quiz results bookmarked!")
                st.rerun()
                
    with act_col2:
        try:
            pdf_bytes = generate_pdf(f"{q_topic} - Quiz Review Report", quiz_report_text)
            st.download_button(
                label="📥 Download Quiz Report PDF",
                data=pdf_bytes,
                file_name=f"Quiz_{q_topic.replace(' ', '_')}_{q_diff}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception:
            st.warning("Could not generate PDF.")

    st.markdown("---")
    st.markdown("### 🔍 Line-by-Line Review")
    
    for s in quiz_summary:
        box_color = "rgba(74, 222, 128, 0.15)" if s["status"] == "Passed" else "rgba(248, 113, 113, 0.15)"
        border_color = "#4ade80" if s["status"] == "Passed" else "#f87171"
        icon = "✅" if s["status"] == "Passed" else "❌"
        
        st.markdown(f"""
        <div style='background: {box_color}; border-left: 5px solid {border_color}; border-radius: 8px; padding: 15px; margin-bottom: 15px;'>
            <h4>{icon} Question {s['num']}</h4>
            <p><b>Question:</b> {s['question']}</p>
            <p><b>Your Answer:</b> <code>{s['user_ans']}</code></p>
            <p><b>Correct Answer:</b> <code>{s['correct_ans']}</code></p>
            <hr style='margin: 8px 0; border-color: rgba(255,255,255,0.05);'>
            <p style='margin: 0; font-size: 0.95rem; font-style: italic;'><b>Explanation:</b> {s['explanation']}</p>
        </div>
        """, unsafe_allow_html=True)
