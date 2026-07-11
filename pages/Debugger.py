import streamlit as st
from streamlit_ace import st_ace
from services.gemini_service import generate_response, is_api_configured
from prompts.debugger import DEBUGGER_PROMPT

# Headers
st.markdown("<h1 class='gradient-header'>🐛 Code Debugger</h1>", unsafe_allow_html=True)
st.markdown("<p class='gradient-subheader'>Paste buggy code and error logs for an instant diagnostics & fix review</p>", unsafe_allow_html=True)

# Main container
st.write("Is your code acting up? Let's check it together! Paste your code below and add any error messages you got.")

# Layout
col_code, col_err = st.columns([1.5, 1])

with col_code:
    st.markdown("### 📝 Buggy Code")
    buggy_code = st_ace(
        value="",
        language="python",
        theme="monokai",
        keybinding="vscode",
        font_size=14,
        tab_size=4,
        min_lines=15,
        max_lines=25,
        wrap=True,
        key="debugger_ace"
    )

with col_err:
    st.markdown("### ⚠️ Error Log (Optional)")
    error_log = st.text_area(
        "Paste any console traceback or compilation error message here:",
        value="",
        height=320,
        placeholder="e.g., IndexError: list index out of range\nor NameError: name 'x' is not defined"
    )

btn_debug = st.button("🔧 Debug My Code", use_container_width=True)

if btn_debug:
    if not buggy_code.strip():
        st.warning("Please paste some code to debug first!")
    else:
        with st.spinner("🤖 PyBuddy is diagnosing the issues..."):
            try:
                # Compile debugger prompt
                prompt = DEBUGGER_PROMPT.format(
                    user_code=buggy_code,
                    error_log=error_log if error_log.strip() else "None provided"
                )
                
                # Fetch debugging review from Gemini
                if is_api_configured():
                    debug_response = generate_response(prompt)
                else:
                    # Fallback / demo mode
                    debug_response = f"""### ⚠️ PyBuddy Demo Mode
Gemini API Key is not configured. Here is a generic debug trace:

1. **Bug Diagnosis**:
   - Ensure you are checking variable scopes and proper indentation.
   - Standard syntax issues: missing colons or parenthesis.

2. **Corrected Code**:
```python
# Double-check code formatting
{buggy_code}
```

3. **Tips**:
   - Enable the API key in the sidebar to get detailed analysis of this code.
"""
                
                # Display output
                st.markdown("---")
                st.markdown("## 🔍 Debugger Report")
                
                st.markdown(
                    f"""
                    <div style='background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 25px;'>
                        {debug_response}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            except Exception as e:
                st.error(str(e))
