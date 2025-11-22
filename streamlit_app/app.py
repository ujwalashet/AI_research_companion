"""
AI Research Companion - Main Application
A premium Streamlit frontend for AI-powered document analysis
"""

import streamlit as st
from pathlib import Path

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="AI Research Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== LOAD CSS ====================
def load_css():
    css_file = Path(__file__).parent / "styles.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ==================== SESSION STATE INITIALIZATION ====================
def init_session_state():
    defaults = {
        'theme': 'dark',
        'xp': 0,
        'level': 1,
        'badges': [],
        'extracted_content': '',
        'summary': '',
        'quiz': [],
        'mindmap': '',
        'chat_history': [],
        'message_count': 0,
        'flashcards': [],
        'current_card': 0,
        'is_flipped': False,
        'cards_studied': 0,
        'cards_mastered': 0,
        'study_mode': 'sequential',
        'study_plans': {},
        'completed_tasks': set(),
        'search_results': [],
        'search_history': [],
        'documents_processed': 0,
        'total_searches': 0,
        'flashcards_created': 0
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

# ==================== HELPER FUNCTIONS ====================
def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme=='dark' else 'dark'
    st.rerun()

def calculate_level():
    return (st.session_state.xp // 100) + 1

def level_title(level):
    if level < 5: return "🌱 Beginner"
    if level < 10: return "📚 Student"
    if level < 15: return "🎓 Scholar"
    if level < 20: return "🔬 Researcher"
    if level < 30: return "🏆 Expert"
    return "👑 Master"

st.session_state.level = calculate_level()

# ==================== SIDEBAR ====================
with st.sidebar:

    st.markdown("""
    <div class="sidebar-header">
        <span class="logo-icon">🧠</span>
        <h1 class="sidebar-title">AI Research Companion</h1>
    </div>
    """, unsafe_allow_html=True)

    # Theme toggle
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col1:
        mode_label = "🌙 Dark Mode" if st.session_state.theme=="dark" else "☀️ Light Mode"
        st.markdown(f"<p class='theme-label'>{mode_label}</p>", unsafe_allow_html=True)
    with col2:
        if st.button("🔄"):
            toggle_theme()

    # XP card
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    level = st.session_state.level
    xp_current = st.session_state.xp % 100
    xp_next = 100 - xp_current

    st.markdown(f"""
    <div class="xp-card">
        <div class="xp-header">
            <span class="xp-icon">⭐</span>
            <div>
                <span class="xp-text">Level {level}</span>
                <p class="xp-subtitle">{level_title(level)}</p>
            </div>
        </div>
        <div class="xp-bar-container">
            <div class="xp-bar" style="width:{xp_current}%"></div>
        </div>
        <p class="xp-label">{st.session_state.xp} XP • {xp_next} to Level {level+1}</p>
    </div>
    """, unsafe_allow_html=True)

    # Badges
    if st.session_state.badges:
        st.markdown("<p class='badges-title'>🏆 Recent Achievements</p>", unsafe_allow_html=True)
        for b in st.session_state.badges[-3:]:
            st.markdown(f"<div class='badge-item'>{b}</div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Quick stats
    st.metric("Documents", st.session_state.documents_processed)
    st.metric("Searches", st.session_state.total_searches)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <p class="nav-title">🎯 Features</p>
    <p>📄 Upload & Analyze Documents</p>
    <p>🖼️ Image OCR</p>
    <p>💬 RAG Chat</p>
    <p>🧠 Flashcards</p>
    <p>📊 Knowledge Graph</p>
    <p>📅 Study Plan</p>
    <p>🔍 Semantic Search</p>
    <p>🏆 Achievements</p>
    """, unsafe_allow_html=True)

# ==================== MAIN HOME UI ====================
theme_class = "dark-mode" if st.session_state.theme=="dark" else "light-mode"

st.markdown(f"""
<div class="hero-section {theme_class}">
    <h1 class="hero-title"><span class="gradient-text">AI Research Companion</span></h1>
    <p class="hero-subtitle">Transform your learning with AI-powered document analysis</p>
    <div class="hero-badges">
        <span class="hero-badge">🚀 AI-Powered</span>
        <span class="hero-badge">📚 Smart Learning</span>
        <span class="hero-badge">🎯 Personalized</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== FEATURE CARD BUTTONS ====================
st.markdown("<h2 class='section-title'>✨ Core Features</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Upload PDF", use_container_width=True):
        st.switch_page("pages/1_upload_pdf.py")

with col2:
    if st.button("🖼️ Upload Image", use_container_width=True):
        st.switch_page("pages/2_upload_image.py")

with col3:
    if st.button("✍️ Paste Text", use_container_width=True):
        st.switch_page("pages/3_upload_text.py")

# ==================== LEARNING TOOLS ====================
col4, col5, col6 = st.columns(3)

with col4:
    if st.button("💬 RAG Chat", use_container_width=True):
        st.switch_page("pages/4_rag_chat.py")

with col5:
    if st.button("🧠 Flashcards", use_container_width=True):
        st.switch_page("pages/5_flashcards.py")

with col6:
    if st.button("📊 Knowledge Graph", use_container_width=True):
        st.switch_page("pages/6_knowledge_graph.py")

col7, col8 = st.columns(2)

with col7:
    if st.button("📅 Study Plan", use_container_width=True):
        st.switch_page("pages/7_study_plan.py")

with col8:
    if st.button("🔍 Semantic Search", use_container_width=True):
        st.switch_page("pages/8_semantic_search.py")

st.markdown("---")

if st.button("🏆 View Achievements", use_container_width=True):
    st.switch_page("pages/9_achievements.py")
