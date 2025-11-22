import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    generate_mindmap,
    add_xp,
    inject_custom_css,
    show_loading,
    show_success_message
)

st.set_page_config(page_title="Mindmap", page_icon="🗺️", layout="wide")
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
    <h1 class="hero-title"><span class="gradient-text">🗺️ Mindmap Generator</span></h1>
    <p class="hero-subtitle">Instantly generate a structured mindmap from your uploaded document.</p>
</div>
""", unsafe_allow_html=True)

# Check if content exists
content = st.session_state.get("extracted_content", "")

if not content:
    st.warning("No document uploaded. Please upload a PDF/Text/Image first.")
else:
    if st.button("✨ Generate Mindmap", use_container_width=True):
        with show_loading("Creating mindmap..."):
            mindmap_text = generate_mindmap(content)

        st.session_state.mindmap = mindmap_text
        add_xp(20, "🗺️ Mindmap Creator")
        show_success_message("Mindmap generated successfully!")
        st.experimental_rerun()

# Display mindmap
if st.session_state.get("mindmap"):
    st.markdown("---")
    st.markdown("### 📌 Generated Mindmap")
    st.code(st.session_state.mindmap, language="markdown")

    st.download_button(
        label="📥 Download Mindmap",
        data=st.session_state.mindmap,
        file_name="mindmap.md",
        mime="text/markdown",
        use_container_width=True
    )
