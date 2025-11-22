import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils import rag_chat, add_xp, inject_custom_css, show_loading

st.set_page_config(page_title="RAG Chat", page_icon="💬", layout="wide")
# ---- Initialize session state if not set ----
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "badges" not in st.session_state:
    st.session_state.badges = []

# Load CSS


css_path = Path(__file__).parents[1] / "styles.css"
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


inject_custom_css()

# Header
st.markdown("""
<div class="hero-section" style="padding: 2rem;">
    <h1 class="hero-title"><span class="gradient-text">RAG Chat</span></h1>
    <p class="hero-subtitle">Ask questions about the documents you've uploaded.</p>
</div>
""", unsafe_allow_html=True)

# Chat history state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
query = st.text_input(
    "Ask a question about your documents",
    placeholder="e.g., Give me a short summary of chapter 2",
    key="rag_input"
)

col1, col2, col3 = st.columns([6, 2, 2])

with col2:
    if st.button("Ask AI", use_container_width=True) and query:
        if not st.session_state.get("extracted_content"):
            st.warning("No documents uploaded. Please upload a document first.")
        else:
            with show_loading("Querying RAG..."):
                answer = rag_chat(query)

            st.session_state.chat_history.append({"q": query, "a": answer})
            add_xp(5)
            st.rerun()

# Display conversation
if st.session_state.chat_history:
    st.markdown("---")
    for msg in reversed(st.session_state.chat_history):
        st.markdown(f"""
        <div style="margin: 0.5rem 0;">
            
            <!-- User message -->
            <div style="
                background: var(--bg-secondary); 
                border: 1px solid var(--border-color);
                padding: 0.75rem 1rem; 
                border-radius: 12px;
                ">
                <strong style="color: var(--text-secondary);">You:</strong> {msg['q']}
            </div>
            
            <!-- AI message -->
            <div style="
                margin-top: 0.5rem; 
                background: linear-gradient(90deg, #667eea, #764ba2);
                padding: 0.9rem 1rem; 
                border-radius: 12px;
                color: white;
                ">
                <strong>AI:</strong> {msg['a']}
            </div>

        </div>
        """, unsafe_allow_html=True)
