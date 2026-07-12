import streamlit as st
import os
from dotenv import load_dotenv
from services.database import init_db, get_or_create_user, update_user_activity
from utils.helpers import generate_default_assets

# 1. Page Configuration (MUST be the first Streamlit command)
st.set_page_config(
    page_title="PyBuddy - AI Python Tutor",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Initialize DB tables & Pillow graphics
init_db()
generate_default_assets()

# 2. Session State Initialization
if "username" not in st.session_state:
    st.session_state["username"] = "PythonLearner"  # Default user profile
if "api_key" not in st.session_state:
    st.session_state["api_key"] = os.getenv("GEMINI_API_KEY", "")
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Home"

# 3. Global CSS Injections for Premium Aesthetics
# Glassmorphism, animations, responsive scrollbars, custom fonts
st.markdown(
    """
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Global Background Adjustments */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Header Gradient Text styling */
    .gradient-header {
        background: linear-gradient(135deg, #FFE082 0%, #3776AB 50%, #4B8BBE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 20px rgba(55, 118, 171, 0.15);
    }
    
    .gradient-subheader {
        font-size: 1.25rem;
        color: #94A3B8;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Glassmorphic card styling */
    .pybuddy-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .pybuddy-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 224, 130, 0.3);
    }
    
    /* Button Hover Enhancements */
    div.stButton > button {
        background: linear-gradient(135deg, #3776AB 0%, #1E415F 100%) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #FFE082 0%, #FFD43B 100%) !important;
        color: #0F172A !important;
        border-color: #FFE082 !important;
        transform: scale(1.03);
        box-shadow: 0 4px 15px rgba(255, 224, 130, 0.4);
    }
    
    /* Code editor styling override */
    .ace_editor {
        border-radius: 8px;
        border: 1px solid #334155;
    }
    /* Text Area Text Color */
    .stTextArea textarea {
        color: white !important;
        -webkit-text-fill-color: white !important;
        caret-color: white !important;
    }
    .stTextArea textarea::placeholder {
        color: #b0b0b0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Render Unified Gamified Sidebar Header
st.sidebar.image("assets/logo.png", width=120)
st.sidebar.markdown("<h2 style='margin-top:0px;'>PyBuddy</h2>", unsafe_allow_html=True)
st.sidebar.caption("Your Personal AI Python Mentor")

# Fetch and update user stats in SQLite database
username = st.session_state["username"]
user_data = get_or_create_user(username)

# Award active streak calculation trigger
update_user_activity(username, xp_gained=0)
user_data = get_or_create_user(username)  # Refresh after streak update

# Sidebar profile cards
st.sidebar.markdown(f"""
<div style='background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255, 224, 130, 0.2); border-radius: 12px; padding: 12px; margin-bottom: 15px;'>
    <div style='font-size: 0.85rem; color: #94A3B8;'>Logged in as:</div>
    <div style='font-size: 1.1rem; font-weight: bold; color: #FFE082;'>@{user_data["username"]}</div>
    <hr style='margin: 8px 0; border-color: rgba(255,255,255,0.05);'>
    <div style='display: flex; justify-content: space-between; font-size: 0.9rem;'>
        <span>🔥 Streak: <b>{user_data["streak_days"]} Days</b></span>
        <span>🏆 XP: <b>{user_data["xp"]}</b></span>
    </div>
</div>
""", unsafe_allow_html=True)

# Username customization expander
with st.sidebar.expander("👤 Customize Profile"):
    new_username = st.text_input("Change Username:", value=username, max_chars=15)
    if new_username and new_username.strip() != username:
        st.session_state["username"] = new_username.strip()
        st.rerun()

# 5. Gemini API Key Configuration Section
with st.sidebar.expander("🔑 Gemini API Settings"):
    api_input = st.text_input(
        "Enter Gemini API Key:",
        value=st.session_state["api_key"],
        type="password",
        help="Input your Google Gemini API key. Keys are not logged or stored outside your local session."
    )
    if api_input != st.session_state["api_key"]:
        st.session_state["api_key"] = api_input
        st.rerun()
        
    if st.session_state["api_key"]:
        st.success("API Key is locally configured!")
    else:
        st.info("No Key? Enter one here or define GEMINI_API_KEY in your local .env file.")

# Responsible AI disclaimer
st.sidebar.markdown("<br><br><hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.sidebar.info("💡 **Responsible AI Disclaimer:** PyBuddy is powered by AI. LLMs can make errors. Always verify critical code logic. PyBuddy will never generate malicious software.")

# 6. Set up program pages routing
pages = [
    st.Page("pages/Home.py", title="Home", icon="🏠"),
    st.Page("pages/Learn.py", title="Learn Concepts", icon="📚"),
    st.Page("pages/Quiz.py", title="Knowledge Quiz", icon="📝"),
    st.Page("pages/Code_Practice.py", title="Coding Practice", icon="💻"),
    st.Page("pages/Debugger.py", title="Code Debugger", icon="🐛"),
    st.Page("pages/Progress.py", title="Progress Tracker", icon="📊"),
    st.Page("pages/About.py", title="About & Extras", icon="ℹ️")
]

pg = st.navigation(pages)
pg.run()
