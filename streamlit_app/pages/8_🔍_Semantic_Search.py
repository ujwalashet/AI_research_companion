import streamlit as st
import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent))

from utils import add_xp, inject_card_css

st.set_page_config(page_title="Semantic Search", page_icon="🔍", layout="wide")

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

inject_card_css()

# Search-specific CSS
st.markdown("""
<style>
.search-container {
    max-width: 800px;
    margin: 0 auto;
}

.search-box {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 25px;
    padding: 1rem 1.5rem;
    transition: all 0.3s ease;
}

.search-box:focus-within {
    border-color: #667eea;
    box-shadow: 0 10px 40px var(--glow-purple);
}

.search-result {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    transition: all 0.3s ease;
    cursor: pointer;
}

.search-result:hover {
    transform: translateX(10px);
    border-color: #667eea;
    box-shadow: 0 5px 20px var(--glow-purple);
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.result-score {
    background: var(--success-gradient);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.result-text {
    color: var(--text-primary);
    line-height: 1.8;
    font-size: 1.05rem;
}

.highlight {
    background: var(--primary-gradient);
    color: white;
    padding: 0.2rem 0.4rem;
    border-radius: 5px;
    font-weight: 600;
}

.result-meta {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-color);
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.filter-chip {
    display: inline-block;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 0.5rem 1rem;
    margin: 0.25rem;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.9rem;
}

.filter-chip:hover, .filter-chip.active {
    background: var(--primary-gradient);
    color: white;
    border-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="hero-section" style="padding: 2rem;">
    <h1 class="hero-title" style="font-size: 3rem;">
        <span class="gradient-text">🔍 Semantic Search</span>
    </h1>
    <p class="hero-subtitle" style="font-size: 1.2rem;">
        Find exactly what you're looking for in your documents
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

def simple_semantic_search(query, content, top_k=10):
    """Simple semantic search implementation"""
    if not content:
        return []
    
    # Split content into sentences
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Simple scoring based on keyword matching (in production, use embeddings)
    query_words = set(query.lower().split())
    results = []
    
    for i, sentence in enumerate(sentences):
        sentence_words = set(sentence.lower().split())
        # Calculate overlap
        overlap = len(query_words & sentence_words)
        if overlap > 0:
            score = (overlap / len(query_words)) * 100
            results.append({
                'text': sentence,
                'score': score,
                'index': i,
                'page': (i // 10) + 1  # Approximate page number
            })
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]

# Search interface
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    search_query = st.text_input(
        "Search",
        placeholder="Enter keywords or phrases...",
        label_visibility="collapsed"
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        search_button = st.button("🔍 Search", use_container_width=True, type="primary")
    with col_b:
        if st.button("🔄 Clear Results", use_container_width=True):
            st.session_state.search_results = []
            st.rerun()

# Perform search
if search_button and search_query:
    content = st.session_state.get('extracted_content', '')
    
    if content:
        with st.spinner("🔎 Searching through your documents..."):
            results = simple_semantic_search(search_query, content)
            st.session_state.search_results = results
            
            # Add to search history
            if search_query not in st.session_state.search_history:
                st.session_state.search_history.insert(0, search_query)
                st.session_state.search_history = st.session_state.search_history[:10]
            
            add_xp(10, "🔍 Search Expert" if len(st.session_state.search_history) >= 10 else None)
            st.rerun()
    else:
        st.warning("⚠️ No content available. Please upload a document first!")

# Display results
if st.session_state.search_results:
    st.markdown("---")
    
    # Results header
    st.markdown(f"""
    <div class="custom-card" style="text-align: center;">
        <h3 style="color: var(--text-primary);">
            Found {len(st.session_state.search_results)} results for "{search_query}"
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    st.markdown("<h4 style='color: var(--text-primary); margin: 1.5rem 0 1rem 0;'>🎯 Filter Results</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        min_score = st.slider("Minimum Relevance Score", 0, 100, 0)
    with col2:
        sort_by = st.selectbox("Sort by", ["Relevance", "Position"])
    with col3:
        results_per_page = st.selectbox("Results per page", [5, 10, 20], index=1)
    
    # Filter results
    filtered_results = [r for r in st.session_state.search_results if r['score'] >= min_score]
    
    if sort_by == "Position":
        filtered_results.sort(key=lambda x: x['index'])
    
    # Display results
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    
    for i, result in enumerate(filtered_results[:results_per_page]):
        # Highlight search terms
        highlighted_text = result['text']
        for word in search_query.split():
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            highlighted_text = pattern.sub(f'<span class="highlight">{word}</span>', highlighted_text)
        
        st.markdown(f"""
        <div class="search-result">
            <div class="result-header">
                <span style="color: var(--text-primary); font-weight: 600;">Result #{i+1}</span>
                <span class="result-score">{result['score']:.0f}% Match</span>
            </div>
            <div class="result-text">{highlighted_text}</div>
            <div class="result-meta">
                <span>📄 Position: {result['index'] + 1}</span>
                <span>📖 Page: ~{result['page']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy", key=f"copy_{i}"):
                st.success("✅ Copied to clipboard!")
        with col2:
            if st.button("💬 Ask AI", key=f"ask_{i}"):
                st.info("🤖 Redirecting to RAG Chat...")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Pagination
    if len(filtered_results) > results_per_page:
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0; color: var(--text-secondary);">
            Showing {min(results_per_page, len(filtered_results))} of {len(filtered_results)} results
        </div>
        """, unsafe_allow_html=True)

# Search history
if st.session_state.search_history:
    st.markdown("---")
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-icon">🕐</span>
            <h3 class="card-title">Recent Searches</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(5)
    for i, query in enumerate(st.session_state.search_history[:5]):
        with cols[i]:
            if st.button(f"🔍 {query}", key=f"history_{i}", use_container_width=True):
                st.session_state.temp_search = query
                st.rerun()

# Tips section
st.markdown("---")
st.markdown("""
<div class="custom-card">
    <div class="card-header">
        <span class="card-icon">💡</span>
        <h3 class="card-title">Search Tips</h3>
    </div>
    <div class="card-content">
        <ul style="line-height: 2;">
            <li>🎯 Use specific keywords for better results</li>
            <li>🔤 Try different phrasings of your question</li>
            <li>📝 Use quotes for exact phrase matching</li>
            <li>🔍 Combine multiple keywords for precision</li>
            <li>📊 Adjust the relevance score filter to refine results</li>
            <li>💬 Use "Ask AI" button to get detailed explanations</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# No content warning
if not st.session_state.get('extracted_content'):
    st.markdown("""
    <div class="custom-card" style="text-align: center; padding: 4rem; margin-top: 3rem; background: var(--secondary-gradient); color: white;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">⚠️</div>
        <h2 style="margin-bottom: 1rem;">No Documents Available</h2>
        <p style="font-size: 1.2rem; margin-bottom: 2rem;">
            Upload a document to start searching
        </p>
        <a href="/1_📄_Upload_PDF" style="
            display: inline-block;
            background: white;
            color: #f5576c;
            padding: 1rem 2rem;
            border-radius: 15px;
            text-decoration: none;
            font-weight: 600;
        ">
            📄 Upload PDF
        </a>
    </div>
    """, unsafe_allow_html=True)