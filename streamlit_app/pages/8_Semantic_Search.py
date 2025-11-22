import streamlit as st
import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))

from utils import add_xp, inject_custom_css

st.set_page_config(page_title="Semantic Search", page_icon="🔍", layout="wide")
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

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title"><span class="gradient-text">🔍 Semantic Search</span></h1>
    <p class="hero-subtitle">Find relevant information inside your uploaded documents using intelligent keyword matching.</p>
</div>
""", unsafe_allow_html=True)

# Get extracted content
content = st.session_state.get("extracted_content", "")

# ---------------- SEARCH INPUT ----------------
st.markdown("""
<style>
.search-box {
    padding: 1rem;
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 18px;
    transition: 0.3s ease;
}

.search-box:hover {
    border-color: #667eea;
    box-shadow: 0 5px 25px var(--glow-purple);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='search-box'>", unsafe_allow_html=True)
query = st.text_input("Search inside your document", placeholder="Enter keywords or phrases...")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SEARCH ACTION ----------------
if st.button("🔍 Run Search", use_container_width=True):
    if not content:
        st.warning("⚠️ No content available. Please upload a PDF or image first.")
    else:
        # Split into meaningful sentences
        sentences = re.split(r"[.!?]", content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        query_words = set(query.lower().split())
        results = []

        for s in sentences:
            sentence_words = set(s.lower().split())
            overlap = len(query_words & sentence_words)
            if overlap > 0:
                results.append({"text": s, "matches": overlap})

        # Sort by relevance
        results.sort(key=lambda x: x["matches"], reverse=True)

        st.session_state.search_results = results
        add_xp(10, "🔍 Search Expert")

# ---------------- DISPLAY RESULTS ----------------
results = st.session_state.get("search_results", [])

if results:
    st.markdown("<h2 class='section-title'>🔎 Top Results</h2>", unsafe_allow_html=True)

    for item in results[:10]:
        text = item["text"]
        score = item["matches"]

        # highlight matched keywords
        for word in query.split():
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            text = pattern.sub(
                f"<span style='background: var(--primary-gradient); color:white; padding:2px 6px; border-radius:5px;'>{word}</span>",
                text
            )

        st.markdown(f"""
        <div class="custom-card" style="margin-top: 1rem;">
            <div class="card-header">
                <span class="card-icon">📌</span>
                <h3 class="card-title">{score} keyword matches</h3>
            </div>
            <div class="card-content">{text}</div>
        </div>
        """, unsafe_allow_html=True)

elif query:
    st.info("No matching sentences found. Try different keywords.")
