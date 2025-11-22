import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils import upload_image, add_xp, show_loading, inject_custom_css, show_success_message

st.set_page_config(page_title="Upload Image", page_icon="🖼️", layout="wide")
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
<div class="hero-section">
    <h1 class="hero-title"><span class="gradient-text">Upload Image</span></h1>
    <p class="hero-subtitle">Extract text from images using OCR.</p>
</div>
""", unsafe_allow_html=True)

# File upload
col1, col2, col3 = st.columns([1,2,1])

with col2:
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["png","jpg","jpeg","webp"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        # Preview the image
        st.markdown("""
        <div class="custom-card">
            <h3>Image Preview</h3>
        </div>
        """, unsafe_allow_html=True)

        st.image(uploaded_file, use_container_width=True)

        if st.button("Extract Text", use_container_width=True):
            with show_loading("Extracting text..."):
                result = upload_image(uploaded_file)

                if result:
                    st.session_state.extracted_content = result.get("extracted_text", "")
                    st.session_state.summary = result.get("summary", "")

                    add_xp(40, "Image Analyzer")
                    show_success_message("OCR completed successfully!")

                    st.rerun()

# Results
if st.session_state.get("extracted_content"):
    tab1, tab2 = st.tabs(["Extracted Text", "Summary"])

    with tab1:
        st.text_area("Extracted Text", st.session_state.extracted_content, height=300)

    with tab2:
        st.write(st.session_state.summary)

    with tab3:
        quiz = st.session_state.get("quiz", [])

        # If quiz is missing or not a list → show fallback
        if not isinstance(quiz, list) or len(quiz) == 0:
            st.warning("No quiz available for this image.")
        else:
            for i, q in enumerate(quiz):
                if not isinstance(q, dict):
                    continue  # Skip invalid items

                st.write(f"**{i+1}. {q.get('question', '')}**")
                options = q.get("options", [])

                if isinstance(options, list) and len(options) > 0:
                    st.radio(f"q_img_{i}", options, key=f"quiz_img_{i}")

                st.markdown("---")
