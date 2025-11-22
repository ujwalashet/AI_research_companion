import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    upload_pdf, generate_mindmap, upload_to_rag, add_xp,
    show_loading, inject_custom_css, show_success_message, create_progress_bar
)

st.set_page_config(page_title="Upload PDF", page_icon="📄", layout="wide")
# ---- Initialize session state if not set ----
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "badges" not in st.session_state:
    st.session_state.badges = []


css_path = Path(__file__).parents[1] / "styles.css"
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

inject_custom_css()

# Page header
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title"><span class="gradient-text">Upload PDF</span></h1>
    <p class="hero-subtitle">Extract, summarize, and analyze PDFs using AI.</p>
</div>
""", unsafe_allow_html=True)

# File upload
col1, col2, col3 = st.columns([1,2,1])

with col2:
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        help="Upload a PDF document to analyze",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.markdown(f"""
        <div class="custom-card">
            <h3>{uploaded_file.name}</h3>
            <p>Size: {uploaded_file.size/1024:.2f} KB</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Analyze PDF", use_container_width=True):
            with show_loading("Processing PDF..."):
                result = upload_pdf(uploaded_file)

                if result:
                    st.session_state.extracted_content = result.get("extracted_content","")
                    st.session_state.summary = result.get("summary","")
                    st.session_state.quiz = result.get("quiz",[])

                    st.session_state.mindmap = generate_mindmap(
                        st.session_state.extracted_content
                    )

                    upload_to_rag(
                        st.session_state.extracted_content,
                        {"filename": uploaded_file.name}
                    )

                    add_xp(50, "PDF Master")
                    show_success_message("PDF analyzed successfully!")
                    st.rerun()

# Results
if st.session_state.get("summary"):
    st.markdown("---")
    create_progress_bar(100, "Analysis Complete")

    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Full Text", "Quiz", "Mindmap"])

    with tab1:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.write(st.session_state.summary)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.text_area("Extracted Text", st.session_state.extracted_content, height=400)

    with tab3:
        quiz = st.session_state.get("quiz", [])

    # If quiz is missing or not a list → show fallback
        if not isinstance(quiz, list) or len(quiz) == 0:
            st.warning("No quiz available for this PDF.")
        else:
            for i, q in enumerate(quiz):
                if not isinstance(q, dict):
                    continue  # Skip anything invalid

                st.write(f"**{i+1}. {q.get('question', '')}**")
                options = q.get("options", [])

                if isinstance(options, list) and len(options) > 0:
                    st.radio(f"q_{i}", options, key=f"quiz_{i}")

                st.markdown("---")



    with tab4:
        if st.session_state.mindmap:
            st.code(st.session_state.mindmap, language="text")
        else:
            st.info("Mindmap is being generated...")
