import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    upload_text, add_xp, show_loading, 
    inject_custom_css, show_success_message, validate_file_size
)

st.set_page_config(page_title="Upload Text", page_icon="✍️", layout="wide")
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
    <h1 class="hero-title" style="font-size: 3rem;">
        <span class="gradient-text">Paste / Upload Text</span>
    </h1>
    <p class="hero-subtitle" style="font-size: 1.2rem;">
        Paste text or upload a .txt/.md file to summarize and generate quizzes.
    </p>
</div>
""", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([2,1])

with col1:
    mode = st.radio("Input method", ["Paste text", "Upload file"], index=0, horizontal=True)

    content = ""
    uploaded_file = None

    if mode == "Paste text":
        content = st.text_area(
            "Paste your text here",
            height=300,
            placeholder="Paste or type text..."
        )

    else:
        uploaded_file = st.file_uploader("Upload .txt or .md file", type=['txt','md'])
        
        if uploaded_file:
            if not validate_file_size(uploaded_file, max_size_mb=5):
                st.error("❌ File too big (max 5MB). Please upload a smaller file.")
            else:
                content = uploaded_file.getvalue().decode('utf-8', errors='ignore')

with col2:
    st.markdown("<div style='position: sticky; top: 2rem;'>", unsafe_allow_html=True)

    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-icon">💡</span>
            <h3 class="card-title">Tips</h3>
        </div>
        <div class="card-content">
            <ul>
                <li>Best for articles, notes, or lecture transcripts.</li>
                <li>Keep text under 50,000 characters for best results.</li>
                <li>Use semantic search later to find facts fast.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Process Text", use_container_width=True):
        if not content.strip():
            st.warning("⚠️ Please paste text or upload a file first.")
        else:
            with show_loading("Analyzing text..."):
                res = upload_text(content)

            if res:
                st.session_state.extracted_content = content
                st.session_state.summary = res.get("summary", "")
                st.session_state.quiz = res.get("quiz", [])

                add_xp(30, "Text Contributor")
                show_success_message("Text processed successfully!")

                st.rerun()

# Results
st.markdown("---")

if st.session_state.get("summary"):
    st.markdown("<h3>AI Summary</h3>", unsafe_allow_html=True)
    st.write(st.session_state.summary)

if st.session_state.get("quiz"):
    st.markdown("---")
    st.markdown("<h3>Generated Quiz</h3>", unsafe_allow_html=True)

    for idx, q in enumerate(st.session_state.quiz):
        st.markdown(f"**{idx+1}. {q.get('question','-')}**")
        opts = q.get("options", [])
        if opts:
            st.radio(
                f"q_{idx}",
                opts,
                key=f"quiz_{idx}",
                label_visibility="collapsed"
            )
        st.markdown("---")
