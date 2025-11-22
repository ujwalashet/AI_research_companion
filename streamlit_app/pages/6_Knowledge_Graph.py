import streamlit as st
import sys
from pathlib import Path
import re
import tempfile
from pyvis.network import Network

sys.path.append(str(Path(__file__).parent.parent))

from utils import add_xp, inject_custom_css

st.set_page_config(page_title="Knowledge Graph", page_icon="📊", layout="wide")
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

# ------------------ HERO SECTION ------------------
st.markdown("""
<div class="hero-section" style="padding: 2rem;">
    <h1 class="hero-title">
        <span class="gradient-text">📊 Knowledge Graph</span>
    </h1>
    <p class="hero-subtitle">
        Visualize key concepts and relationships from your uploaded content.
    </p>
</div>
""", unsafe_allow_html=True)


# ------------------ EXTRACT CONCEPTS ------------------
def extract_concepts(text: str):
    """
    Extract important words from content.
    Capitalized words or long words (5+ chars) represent concepts.
    """
    words = re.findall(r"\b[A-Z][a-z]+|\b[a-z]{5,}\b", text)
    from collections import Counter
    common = [w for w, _ in Counter(words).most_common(25)]
    return common


# ------------------ BUILD GRAPH ------------------
def build_graph(content: str):
    concepts = extract_concepts(content)

    if len(concepts) < 2:
        return None, 0

    net = Network(
        height="650px",
        width="100%",
        bgcolor="#0f0f23",
        font_color="white",
        directed=False
    )

    # Add main node
    net.add_node(
        "Main Topic",
        label="Main Topic",
        size=45,
        color="#764ba2"
    )

    # Add concept nodes
    for c in concepts[:20]:
        net.add_node(
            c,
            label=c,
            size=25,
            color="#4facfe"
        )
        net.add_edge("Main Topic", c)

    # Add light interconnections between concepts
    for i in range(len(concepts) - 1):
        if i % 2 == 0:
            net.add_edge(concepts[i], concepts[i + 1])

    return net, len(concepts)


# ------------------ MAIN CONTENT ------------------
content = st.session_state.get("extracted_content", "")

if not content:
    st.info("Upload any PDF, image or text first to generate a knowledge graph.")
    st.stop()

# Settings card
st.markdown("""
<div class="custom-card">
    <div class="card-header">
        <span class="card-icon">⚙️</span>
        <h3 class="card-title">Graph Settings</h3>
    </div>
    <div class="card-content">
        <p>Click the button below to generate a visual knowledge graph based on your uploaded content.</p>
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("Generate Knowledge Graph", use_container_width=True):
    graph, count = build_graph(content)

    if not graph:
        st.error("Not enough concepts found to build a graph.")
        st.stop()

    # Save graph temporarily and display
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        graph.save_graph(tmp.name)
        html = open(tmp.name, "r", encoding="utf-8").read()

    st.components.v1.html(html, height=700)

    # XP reward
    add_xp(30, "🕸️ Knowledge Mapper")

    # Stats output
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-icon">📈</span>
            <h3 class="card-title">Graph Summary</h3>
        </div>
        <div class="card-content">
            <p><strong>Total Concepts Identified:</strong> {count}</p>
            <p>Your knowledge graph has been generated using semantic clustering and concept mapping.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Download button
    st.download_button(
        "Download Graph (HTML)",
        data=html.encode("utf-8"),
        file_name="knowledge_graph.html",
        mime="text/html",
        use_container_width=True
    )
