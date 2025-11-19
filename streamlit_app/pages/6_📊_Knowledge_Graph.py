import streamlit as st
import sys
from pathlib import Path
import networkx as nx
from pyvis.network import Network
import tempfile
import re

sys.path.append(str(Path(__file__).parent.parent))

from utils import add_xp

st.set_page_config(page_title="Knowledge Graph", page_icon="📊", layout="wide")

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="hero-section" style="padding: 2rem;">
    <h1 class="hero-title" style="font-size: 3rem;">
        <span class="gradient-text">📊 Knowledge Graph</span>
    </h1>
    <p class="hero-subtitle" style="font-size: 1.2rem;">
        Visualize concepts and their relationships
    </p>
</div>
""", unsafe_allow_html=True)

def extract_concepts(text, max_concepts=20):
    """Extract key concepts from text"""
    # Simple keyword extraction (in production, use NLP)
    words = re.findall(r'\b[A-Z][a-z]+\b|\b[a-z]{5,}\b', text)
    # Count frequency
    from collections import Counter
    word_freq = Counter(words)
    # Get top concepts
    concepts = [word for word, _ in word_freq.most_common(max_concepts)]
    return concepts

def create_knowledge_graph(content):
    """Create a knowledge graph from content"""
    # Extract concepts
    concepts = extract_concepts(content)
    
    if len(concepts) < 2:
        return None
    
    # Create network
    net = Network(height="600px", width="100%", bgcolor="#1a1a2e", font_color="white")
    net.barnes_hut()
    
    # Add central node
    net.add_node(0, label="Main Topic", color="#667eea", size=40, title="Central concept")
    
    # Add concept nodes with connections
    for i, concept in enumerate(concepts[:15], start=1):
        # Determine node color based on position
        if i <= 5:
            color = "#f5576c"
        elif i <= 10:
            color = "#4facfe"
        else:
            color = "#fa709a"
        
        net.add_node(i, label=concept, color=color, size=25, title=concept)
        net.add_edge(0, i, color="#667eea", width=2)
        
        # Add some inter-concept connections
        if i > 1 and i % 2 == 0:
            net.add_edge(i-1, i, color="#9ca3af", width=1)
    
    # Configure physics
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -30000,
          "centralGravity": 0.3,
          "springLength": 200,
          "springConstant": 0.04,
          "damping": 0.09
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "zoomView": true,
        "dragView": true
      }
    }
    """)
    
    return net

# Check if content is available
content = st.session_state.get('extracted_content', '')

if content:
    # Options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        layout = st.selectbox(
            "Layout Algorithm",
            ["Barnes-Hut", "Force Atlas", "Hierarchical"]
        )
    
    with col2:
        show_labels = st.checkbox("Show Labels", value=True)
    
    with col3:
        node_size = st.slider("Node Size", 10, 50, 25)
    
    # Generate button
    if st.button("🎨 Generate Knowledge Graph", use_container_width=True, type="primary"):
        with st.spinner("🔮 Creating knowledge graph..."):
            net = create_knowledge_graph(content)
            
            if net:
                # Save to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w') as f:
                    net.save_graph(f.name)
                    html_content = open(f.name, 'r').read()
                
                # Display
                st.components.v1.html(html_content, height=650, scrolling=False)
                
                add_xp(30, "🕸️ Knowledge Mapper")
                
                # Download option
                st.download_button(
                    "📥 Download Graph",
                    data=html_content,
                    file_name="knowledge_graph.html",
                    mime="text/html"
                )
            else:
                st.error("Not enough concepts to create a graph. Upload more content!")
    
    # Stats
    st.markdown("---")
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-icon">📈</span>
            <h3 class="card-title">Graph Statistics</h3>
        </div>
        <div class="card-content">
    """, unsafe_allow_html=True)
    
    concepts = extract_concepts(content)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Concepts Identified", len(concepts))
    with col2:
        st.metric("Words Analyzed", len(content.split()))
    with col3:
        st.metric("Connections", len(concepts) if len(concepts) > 1 else 0)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Concept list
    if concepts:
        st.markdown("---")
        st.markdown("""
        <div class="custom-card">
            <div class="card-header">
                <span class="card-icon">🔑</span>
                <h3 class="card-title">Key Concepts</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display concepts in a grid
        cols = st.columns(4)
        for i, concept in enumerate(concepts[:20]):
            with cols[i % 4]:
                st.markdown(f"""
                <div style="
                    background: var(--primary-gradient);
                    color: white;
                    padding: 0.75rem;
                    border-radius: 10px;
                    text-align: center;
                    margin: 0.5rem 0;
                    font-weight: 600;
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
                ">
                    {concept}
                </div>
                """, unsafe_allow_html=True)

else:
    # No content uploaded
    st.markdown("""
    <div class="custom-card" style="text-align: center; padding: 4rem;">
        <div style="font-size: 5rem; margin-bottom: 2rem;">📊</div>
        <h2 style="color: var(--text-primary); margin-bottom: 1rem;">No Content Available</h2>
        <p style="color: var(--text-secondary); font-size: 1.2rem; margin-bottom: 2rem;">
            Upload a document first to generate a knowledge graph
        </p>
        <a href="/1_📄_Upload_PDF" style="
            display: inline-block;
            background: var(--primary-gradient);
            color: white;
            padding: 1rem 2rem;
            border-radius: 15px;
            text-decoration: none;
            font-weight: 600;
            box-shadow: 0 5px 20px var(--glow-purple);
        ">
            📄 Upload PDF
        </a>
    </div>
    """, unsafe_allow_html=True)

# Info section
st.markdown("---")
st.markdown("""
<div class="custom-card">
    <div class="card-header">
        <span class="card-icon">💡</span>
        <h3 class="card-title">About Knowledge Graphs</h3>
    </div>
    <div class="card-content">
        <p style="line-height: 1.8; margin-bottom: 1rem;">
            Knowledge graphs visualize relationships between concepts in your document.
            They help you:
        </p>
        <ul style="line-height: 2;">
            <li>🎯 Identify key concepts at a glance</li>
            <li>🔗 Understand how ideas connect</li>
            <li>📚 Navigate complex information</li>
            <li>🧠 Enhance learning and retention</li>
            <li>🔍 Discover hidden patterns</li>
        </ul>
        <p style="line-height: 1.8; margin-top: 1rem;">
            <strong>Tip:</strong> Zoom, drag, and click nodes to explore the graph interactively!
        </p>
    </div>
</div>
""", unsafe_allow_html=True)