import streamlit as st
from utils.constants import PYTHON_TOPICS
from utils.helpers import generate_pdf
from prompts.explain import (
    EXPLAIN_CONCEPT_PROMPT,
    VISUAL_ANALOGY_PROMPT,
    BEST_PRACTICES_PROMPT,
    COMMON_MISTAKES_PROMPT,
    CHEAT_SHEET_PROMPT,
    INTERVIEW_PREP_PROMPT
)
from prompts.example import (
    REAL_WORLD_EXAMPLE_PROMPT,
    CODE_WALKTHROUGH_PROMPT
)
from services.gemini_service import generate_response, is_api_configured
from services.database import log_concept, add_bookmark, remove_bookmark, is_bookmarked, get_concept_history

# Heading
st.markdown("<h1 class='gradient-header'>📚 Interactive Tutor</h1>", unsafe_allow_html=True)
st.markdown("<p class='gradient-subheader'>Master Python concepts with personalized AI guidance</p>", unsafe_allow_html=True)

username = st.session_state["username"]

# Main layout controls
col1, col2 = st.columns([1.5, 1])

with col1:
    # Topic Selector
    options_list = PYTHON_TOPICS + ["Custom Topic..."]
    selected_topic = st.selectbox("Select a Python Topic:", options_list)
    
    topic = selected_topic
    if selected_topic == "Custom Topic...":
        topic = st.text_input("Enter your custom Python topic:", placeholder="e.g., Decorators with arguments, Threading")

with col2:
    # Activity Selector
    activity_type = st.selectbox(
        "Choose Learning Activity:",
        [
            "Explain Concept",
            "Real World Example",
            "Interview Explanation",
            "Visual Analogy",
            "Best Practices",
            "Common Mistakes",
            "Code Walkthrough",
            "Generate Cheat Sheet"
        ]
    )

# Prompt Map lookup
PROMPT_MAP = {
    "Explain Concept": EXPLAIN_CONCEPT_PROMPT,
    "Real World Example": REAL_WORLD_EXAMPLE_PROMPT,
    "Interview Explanation": INTERVIEW_PREP_PROMPT,
    "Visual Analogy": VISUAL_ANALOGY_PROMPT,
    "Best Practices": BEST_PRACTICES_PROMPT,
    "Common Mistakes": COMMON_MISTAKES_PROMPT,
    "Code Walkthrough": CODE_WALKTHROUGH_PROMPT,
    "Generate Cheat Sheet": CHEAT_SHEET_PROMPT
}

# Fetch or generate
generate_clicked = st.button("🌟 Generate Learning Guide", use_container_width=True)

# State variable to hold active note
if "active_note_text" not in st.session_state:
    st.session_state["active_note_text"] = ""
if "active_note_topic" not in st.session_state:
    st.session_state["active_note_topic"] = ""
if "active_note_activity" not in st.session_state:
    st.session_state["active_note_activity"] = ""

if generate_clicked:
    if not topic or not topic.strip():
        st.warning("Please specify a topic first.")
    else:
        with st.spinner("🤖 PyBuddy is preparing your lesson..."):
            try:
                # Compile target prompt template
                raw_template = PROMPT_MAP[activity_type]
                formatted_prompt = raw_template.format(topic=topic)
                
                # Fetch response
                if is_api_configured():
                    response_text = generate_response(formatted_prompt)
                else:
                    # Provide helpful warning & high-quality static content if Gemini key not set
                    response_text = f"""### ⚠️ PyBuddy Demo Mode
Gemini API Key is not configured. To enable full AI responses, enter your key in the sidebar.

Here is a quick look at **{topic}** ({activity_type}):
- **What it is**: {topic} is a fundamental concept in Python programming.
- **Why it matters**: Understanding it helps write clean, readable code.
- **Learn More**: Run this code locally:
```python
# Demo code for {topic}
print("Learning {topic} with PyBuddy!")
```
"""
                # Log reading history in SQLite
                log_concept(username, topic, activity_type, response_text)
                
                # Save to session state
                st.session_state["active_note_text"] = response_text
                st.session_state["active_note_topic"] = topic
                st.session_state["active_note_activity"] = activity_type
                
            except Exception as e:
                st.error(str(e))

# Display active note if exists
if st.session_state["active_note_text"]:
    note_topic = st.session_state["active_note_topic"]
    note_activity = st.session_state["active_note_activity"]
    note_text = st.session_state["active_note_text"]
    
    st.markdown(f"## {note_topic} - {note_activity}")
    
    # Render PDF download and Bookmark actions in columns
    act_col1 = st.container()
    
    with act_col1:
        # Check if already bookmarked
        booked = is_bookmarked(username, "concept", f"{note_topic} ({note_activity})")
        if booked:
            if st.button("❤️ Remove Bookmark"):
                remove_bookmark(username, "concept", f"{note_topic} ({note_activity})")
                st.toast("Removed from bookmarks!")
                st.rerun()
        else:
            if st.button("➕ Bookmark Concept"):
                add_bookmark(username, "concept", f"{note_topic} ({note_activity})", note_text)
                st.toast("Saved to bookmarks!")
                st.rerun()
                


    # Main output display container
    st.markdown(
        f"""
        <div style='background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 25px; margin-top: 15px;'>
            {note_text}
        </div>
        """,
        unsafe_allow_html=True
    )

# Sidebar Utility: History and Quick Reloading
st.sidebar.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.sidebar.markdown("### 📚 Your Learning History")
history = get_concept_history(username)

if history:
    # Filter uniques
    seen_topics = set()
    unique_history = []
    for h in history:
        key = (h["topic"], h["activity_type"])
        if key not in seen_topics:
            seen_topics.add(key)
            unique_history.append(h)
            
    # List top 5
    for h in unique_history[:5]:
        btn_label = f"{h['topic']} ({h['activity_type']})"
        if st.sidebar.button(f"📖 {btn_label}", key=f"hist_{h['id']}", use_container_width=True):
            st.session_state["active_note_text"] = h["response_text"]
            st.session_state["active_note_topic"] = h["topic"]
            st.session_state["active_note_activity"] = h["activity_type"]
            st.rerun()
else:
    st.sidebar.caption("No topics studied yet. Try generating one!")
