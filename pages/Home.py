import streamlit as st
import random
from utils.constants import TIPS_OF_THE_DAY, PYTHON_FACTS, DAILY_CHALLENGES
from services.database import get_or_create_user
from utils.syntax import validate_syntax
# Display Gradient Page Headers
st.markdown("<h1 class='gradient-header'>Welcome to PyBuddy!</h1>", unsafe_allow_html=True)
st.markdown("<p class='gradient-subheader'>Your Personal AI Python Learning Companion</p>", unsafe_allow_html=True)

# Fetch user details
username = st.session_state["username"]
user_data = get_or_create_user(username)

# Welcome message
st.markdown(f"### 👋 Hello, @{user_data['username']}! Ready to level up your Python skills today?")

# Layout: Features Grid (2 columns)
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="pybuddy-card">
            <h3 style="color: #FFE082; margin-top: 0;">📚 Interactive Tutor</h3>
            <p>Select any Python concept from <b>Variables</b> to <b>Asynchronous Coding</b>. Get real-world explanations, visual analogies, cheat sheets, or interview pitches.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div class="pybuddy-card">
            <h3 style="color: #FFE082; margin-top: 0;">📝 Knowledge Quizzes</h3>
            <p>Test your understanding with 5-question multiple-choice quizzes at three difficulty levels. Get details on weak topics and study tips instantly.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="pybuddy-card">
            <h3 style="color: #FFE082; margin-top: 0;">💻 Coding Practice</h3>
            <p>Solve custom exercises in an embedded text editor. The AI compiles and evaluates your correctness, logic, and style—giving hints before answers.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div class="pybuddy-card">
            <h3 style="color: #FFE082; margin-top: 0;">🐛 Error Debugger</h3>
            <p>Paste broken code and crash logs. Receive a detailed diagnosis of the error, a corrected file, and explanations for every line modified.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# CTA button
if st.button("🚀 Start Learning Now!", use_container_width=True):
    st.switch_page("pages/Learn.py")

st.markdown("---")

# Layout: Dynamic Widgets (Tip of the Day, Random Fact, Daily Challenge)
col_left, col_right = st.columns([1, 1.2])

with col_left:
    # Tip of the Day Card
    st.markdown("### 💡 Python Tip of the Day")
    # Fetch tip deterministically by calendar date or randomly
    random.seed(datetime_seed := len(TIPS_OF_THE_DAY))
    tip_idx = random.randint(0, len(TIPS_OF_THE_DAY) - 1)
    
    st.markdown(f"""
    <div style='background: rgba(55, 118, 171, 0.15); border-left: 5px solid #3776AB; border-radius: 8px; padding: 15px; margin-bottom: 20px;'>
        <p style='font-style: italic; margin: 0; font-size: 1.05rem;'>{TIPS_OF_THE_DAY[tip_idx]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Random Fact Card
    st.markdown("### 🐍 Random Python Fact")
    fact_idx = random.randint(0, len(PYTHON_FACTS) - 1)
    st.markdown(f"""
    <div style='background: rgba(255, 224, 130, 0.1); border-left: 5px solid #FFE082; border-radius: 8px; padding: 15px;'>
        <p style='margin: 0; font-size: 1.05rem;'>{PYTHON_FACTS[fact_idx]}</p>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    # Daily Challenge Widget
    st.markdown("### 🏆 Daily Python Challenge")
    
    # Load default challenge (id = 1)
    challenge = DAILY_CHALLENGES[0]
    
    st.markdown(f"**Challenge Title**: `{challenge['title']}`")
    st.write(challenge["description"])
    
    # Simple interactive solution dropdown
    with st.expander("💡 View Challenge Hint"):
        st.info(challenge["hint"])
        
    challenge_code = st.text_area("Write your code solution here:", value=challenge["starter_code"], height=120)
    
    if st.button("Check Solution"):

        valid, error = validate_syntax(challenge_code)

        if not valid:
            st.error(error)

        elif "pass" in challenge_code:
            st.warning("⚠️ Your solution is incomplete. Replace 'pass' with your code.")

        elif "return" not in challenge_code:
            st.warning("⚠️ Your function must return a value.")

        else:
            st.success("🎉 Good job! Your logic structures look correct.")

            with st.expander("🔍 Show Reference Solution"):
                st.code(challenge["solution"], language="python")