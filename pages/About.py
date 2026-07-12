import streamlit as st
from utils.constants import FLASHCARDS, INTERVIEW_QUESTIONS, CODING_ROADMAP, PYTHON_DICTIONARY
from services.database import get_bookmarks, remove_bookmark

# Headers
st.markdown("<h1 class='gradient-header'>ℹ️ About & Extras</h1>", unsafe_allow_html=True)
st.markdown("<p class='gradient-subheader'>Explore additional resources, practice tools, and bookmarks</p>", unsafe_allow_html=True)

username = st.session_state["username"]

# Main tabs layout
tab_about, tab_bookmarks, tab_flashcards, tab_roadmap, tab_interview, tab_dict = st.tabs([
    "💡 Project Info", 
    "❤️ Saved Bookmarks",
    "📇 Flashcards", 
    "🗺️ Career Roadmap", 
    "🤝 Interview Prep", 
    "📖 Mini Dictionary"
])

# 1. Project Info Tab
with tab_about:
    st.markdown("### 🤖 About PyBuddy")
    st.write(
        "**PyBuddy** is an interactive, AI-powered Python mentoring web application designed to help beginners "
        "learn programming. By using Google's Gemini API, PyBuddy acts as a patient companion that "
        "provides clear tutorials, generates personalized coding exercises, analyzes code style, helps debug errors, "
        "and designs study roadmaps."
    )
    
    st.markdown("#### 🛠️ Technology Stack")
    col_tech1, col_tech2 = st.columns(2)
    with col_tech1:
        st.markdown(
            """
            - **Backend Framework**: Streamlit (Python Web Framework)
            - **AI Engine**: Google Gemini API (`gemini-3.5-flash`)
            - **Data Storage**: SQLite 3 Database
            """
        )
    with col_tech2:
        st.markdown(
            """
            - **Visualization**: Plotly Charts & Pandas DataFrames
            - **Formatting & Highlighting**: Pygments & Black
            - **Interactive Components**: Streamlit-Ace Code Editor
            """
        )
        
    st.markdown("#### 🔒 Responsible AI Declaration")
    st.warning(
        "**Disclaimer**: PyBuddy uses generative AI to provide learning instructions and code checks. "
        "Large Language Models (LLMs) can occasionally generate inaccurate outputs or logic errors. "
        "Always test important scripts locally and verify instructions. "
        "PyBuddy has built-in filters to block harmful topics, malicious operations, and cyberattack commands."
    )



# 2. Bookmarks Manager Tab
with tab_bookmarks:
    st.markdown("### ❤️ Your Saved Bookmarks")
    bookmarks = get_bookmarks(username)

    if not bookmarks:
        st.info(
            "You haven't bookmarked any concepts, cheat sheets, or quizzes yet. "
            "Use the 'Bookmark' options in Learn or Quiz pages to save files here."
        )
    else:
        for idx, book in enumerate(bookmarks):
            card_title = f"{book['title']} ({book['item_type'].title()})"

            with st.expander(f"📌 {card_title}"):

                if st.button(
                    "🗑️ Remove Bookmark",
                    key=f"del_book_{book['id']}",
                    use_container_width=True,
                ):
                    remove_bookmark(username, book["item_type"], book["title"])
                    st.toast("Bookmark removed!")
                    st.rerun()

                formatted_content = book["content"].replace("\n", "<br>")

                st.markdown(
                    f"""
                    <div style='background: rgba(30, 41, 59, 0.4); border-radius: 8px; padding: 15px; font-family: monospace;'>
                        {formatted_content}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# 3. Flashcards Tab
with tab_flashcards:
    st.markdown("### 📇 Interactive Study Cards")
    st.write("Click the card title to flip between the term and its Python definition.")
    
    # Store flipped state in session
    if "flash_flipped" not in st.session_state:
        st.session_state["flash_flipped"] = {}
        
    f_col1, f_col2 = st.columns(2)
    
    for idx, card in enumerate(FLASHCARDS):
        target_col = f_col1 if idx % 2 == 0 else f_col2
        
        # Check flipped state
        is_flipped = st.session_state["flash_flipped"].get(card["id"], False)
        
        with target_col:
            card_color = "rgba(55, 118, 171, 0.15)" if not is_flipped else "rgba(255, 224, 130, 0.15)"
            border_color = "#3776AB" if not is_flipped else "#FFE082"
            
            # Interactive container using expander or buttons
            title = f"🏷️ {card['term']} [{card['category']}]" if not is_flipped else "💡 Definition / Code"
            content = f"**{card['term']}**\n\n*(Click 'Flip Card' below to view definition)*" if not is_flipped else card["definition"]
            
            st.markdown(f"""
            <div style='background: {card_color}; border: 1px solid {border_color}; border-radius: 12px; padding: 20px; min-height: 140px; margin-bottom: 10px;'>
                <b>{title}</b>
                <p style='margin-top: 10px; font-size: 0.95rem;'>{content}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Flip Card", key=f"flip_{card['id']}", use_container_width=True):
                st.session_state["flash_flipped"][card["id"]] = not is_flipped
                st.rerun()

# 4. Career Roadmap Tab
with tab_roadmap:
    st.markdown("### 🗺️ Developer Career Roadmap")
    st.write("Follow this comprehensive step-by-step curriculum to transition from a beginner to a Python expert.")
    
    for idx, step in enumerate(CODING_ROADMAP):
        num = idx + 1
        st.markdown(f"""
        <div style='background: rgba(30, 41, 59, 0.5); border-left: 5px solid #3776AB; border-radius: 8px; padding: 15px; margin-bottom: 15px;'>
            <h4 style='margin-top:0px; color: #FFE082;'>Step {num}: {step['phase']}</h4>
            <p style='font-size: 0.95rem; margin-bottom: 8px;'>{step['description']}</p>
            <b>Key Skillsets to Master:</b>
            <ul style='font-size: 0.9rem; margin-top: 4px;'>
                {"".join(f"<li>{m}</li>" for m in step['milestones'])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

# 5. Interview Prep Tab
with tab_interview:
    st.markdown("### 🤝 Python Job Interview Guide")
    st.write("Browse common interview questions categorized by target professional level.")
    
    level_choice = st.radio("Choose Level:", ["Junior", "Mid", "Senior"], horizontal=True)
    questions = INTERVIEW_QUESTIONS[level_choice]
    
    for idx, q in enumerate(questions):
        with st.expander(f"❓ Q{idx+1}: {q['question']}"):
            st.markdown(
                f"""
                <div style='background: rgba(30, 41, 59, 0.4); border-radius: 8px; padding: 15px;'>
                    <b>Answer:</b><br>{q['answer']}
                </div>
                """,
                unsafe_allow_html=True
            )

# 6. Mini Dictionary Tab
with tab_dict:
    st.markdown("### 📖 Mini Python Dictionary")
    st.write("Search for Python keywords, methods, and syntax guidelines quickly.")
    
    # Search input
    search_query = st.text_input("🔍 Search keyword:", placeholder="e.g., yield, decorator, lambda")
    
    if search_query:
        matches = {k: v for k, v in PYTHON_DICTIONARY.items() if search_query.lower() in k.lower()}
        if matches:
            for k, v in matches.items():
                st.markdown(f"**`{k}`**: {v}")
        else:
            st.warning("No matching keywords found. Try searching for 'lambda', 'venv', or 'yield'.")
            
    st.markdown("#### Complete Keyword Registry")
    # Clean two-column table view of glossary
    d_col1, d_col2 = st.columns(2)
    keys = sorted(list(PYTHON_DICTIONARY.keys()))
    
    for idx, k in enumerate(keys):
        target_col = d_col1 if idx % 2 == 0 else d_col2
        with target_col:
            with st.expander(f"🔑 {k}"):
                st.write(PYTHON_DICTIONARY[k])
