"""
AI Research Companion - Main Application
A premium Streamlit frontend for AI-powered document analysis
"""

import streamlit as st
from pathlib import Path
import base64

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="AI Research Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/ai-research-companion',
        'Report a bug': "https://github.com/yourusername/ai-research-companion/issues",
        'About': "# AI Research Companion\nPowered by AI & Built with ❤️"
    }
)

# ==================== LOAD CSS ====================
def load_css():
    """Load custom CSS styling"""
    css_file = Path(__file__).parent / "styles.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ styles.css not found. UI may not display correctly.")

load_css()

# ==================== SESSION STATE INITIALIZATION ====================
def init_session_state():
    """Initialize all session state variables"""
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
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ==================== HELPER FUNCTIONS ====================
def toggle_theme():
    """Toggle between dark and light theme"""
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
    st.rerun()

def calculate_level():
    """Calculate user level based on XP"""
    return (st.session_state.xp // 100) + 1

def get_level_title(level):
    """Get title based on level"""
    if level < 5:
        return "🌱 Beginner"
    elif level < 10:
        return "📚 Student"
    elif level < 15:
        return "🎓 Scholar"
    elif level < 20:
        return "🔬 Researcher"
    elif level < 30:
        return "🏆 Expert"
    else:
        return "👑 Master"

# Update level
st.session_state.level = calculate_level()

# ==================== SIDEBAR ====================
with st.sidebar:
    # Logo and Title
    st.markdown("""
    <div class="sidebar-header">
        <div class="logo-container">
            <span class="logo-icon">🧠</span>
        </div>
        <h1 class="sidebar-title">AI Research<br/>Companion</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Theme Toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        theme_label = "🌙 Dark Mode" if st.session_state.theme == 'dark' else "☀️ Light Mode"
        st.markdown(f"<p class='theme-label'>{theme_label}</p>", unsafe_allow_html=True)
    with col2:
        if st.button("🔄", key="theme_toggle", help="Toggle theme"):
            toggle_theme()
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # XP and Level Display
    level = st.session_state.level
    xp_in_level = st.session_state.xp % 100
    xp_for_next = 100 - xp_in_level
    progress_percent = xp_in_level
    
    st.markdown(f"""
    <div class="xp-card">
        <div class="xp-header">
            <span class="xp-icon">⭐</span>
            <div>
                <span class="xp-text">Level {level}</span>
                <p class="xp-subtitle">{get_level_title(level)}</p>
            </div>
        </div>
        <div class="xp-bar-container">
            <div class="xp-bar" style="width: {progress_percent}%"></div>
        </div>
        <p class="xp-label">{st.session_state.xp} XP • {xp_for_next} to Level {level + 1}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recent Badges
    if st.session_state.badges:
        st.markdown("<div class='badges-section'>", unsafe_allow_html=True)
        st.markdown("<p class='badges-title'>🏆 Recent Achievements</p>", unsafe_allow_html=True)
        for badge in st.session_state.badges[-3:]:
            st.markdown(f"<div class='badge-item'>{badge}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("""
    <div class="sidebar-stats">
        <p class="stat-title">📊 Quick Stats</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents", st.session_state.documents_processed, delta=None)
    with col2:
        st.metric("Searches", st.session_state.total_searches, delta=None)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Navigation Tips
    st.markdown("""
    <div class="nav-info">
        <p class="nav-title">🎯 Features</p>
        <p>📄 Upload & Analyze Documents</p>
        <p>💬 Chat with AI Assistant</p>
        <p>🧠 Generate Flashcards</p>
        <p>📊 Visualize Knowledge</p>
        <p>📅 Create Study Plans</p>
        <p>🔍 Semantic Search</p>
        <p>🏆 Track Achievements</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="sidebar-footer">
        <p>Made with ❤️ using Streamlit</p>
        <p style="font-size: 0.75rem; opacity: 0.7;">v1.0.0 | © 2024</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================

# Apply theme class
theme_class = 'dark-mode' if st.session_state.theme == 'dark' else 'light-mode'

# Hero Section
st.markdown(f"""
<div class="hero-section {theme_class}">
    <div class="hero-content">
        <h1 class="hero-title">
            <span class="gradient-text">AI Research Companion</span>
        </h1>
        <p class="hero-subtitle">
            Transform your learning with AI-powered document analysis, smart flashcards, and intelligent study tools
        </p>
        <div class="hero-badges">
            <span class="hero-badge">🚀 AI-Powered</span>
            <span class="hero-badge">📚 Smart Learning</span>
            <span class="hero-badge">🎯 Personalized</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Feature Cards
st.markdown("<h2 class='section-title'>✨ Core Features</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-wrapper">
            <div class="feature-icon">📚</div>
        </div>
        <h3 class="feature-title">Upload & Analyze</h3>
        <p class="feature-desc">Upload PDFs, images, or text. Get instant AI-powered summaries, quizzes, and mindmaps.</p>
        <div class="feature-stats">
            <span>📄 Multi-format support</span>
        </div>
        <div class="feature-glow"></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-wrapper">
            <div class="feature-icon">🤖</div>
        </div>
        <h3 class="feature-title">AI Chat Assistant</h3>
        <p class="feature-desc">Have natural conversations with your documents using advanced RAG technology.</p>
        <div class="feature-stats">
            <span>💬 Context-aware responses</span>
        </div>
        <div class="feature-glow"></div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-wrapper">
            <div class="feature-icon">🧠</div>
        </div>
        <h3 class="feature-title">Smart Learning</h3>
        <p class="feature-desc">Generate flashcards, study plans, and visualize knowledge graphs automatically.</p>
        <div class="feature-stats">
            <span>🎯 Spaced repetition</span>
        </div>
        <div class="feature-glow"></div>
    </div>
    """, unsafe_allow_html=True)

# Stats Section
st.markdown("<div style='margin: 4rem 0;'></div>", unsafe_allow_html=True)
st.markdown("<h2 class='section-title'>📊 Your Progress</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card pulse">
        <div class="stat-icon">📄</div>
        <div class="stat-value">{st.session_state.documents_processed}</div>
        <div class="stat-label">Documents Processed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card pulse">
        <div class="stat-icon">💬</div>
        <div class="stat-value">{st.session_state.message_count}</div>
        <div class="stat-label">Chat Messages</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card pulse">
        <div class="stat-icon">🧠</div>
        <div class="stat-value">{st.session_state.cards_studied}</div>
        <div class="stat-label">Cards Studied</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card pulse">
        <div class="stat-icon">🏆</div>
        <div class="stat-value">{len(st.session_state.badges)}</div>
        <div class="stat-label">Badges Earned</div>
    </div>
    """, unsafe_allow_html=True)

# Getting Started Guide
st.markdown("<div style='margin: 4rem 0;'></div>", unsafe_allow_html=True)
st.markdown("<h2 class='section-title'>🚀 Getting Started</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="getting-started-container">
    <div class="steps-wrapper">
        <div class="step-item">
            <div class="step-number">1</div>
            <div class="step-content">
                <h3 class="step-title">📤 Upload Content</h3>
                <p class="step-desc">Upload a PDF, image, or paste text to begin your learning journey.</p>
            </div>
        </div>
        
        <div class="step-arrow">→</div>
        
        <div class="step-item">
            <div class="step-number">2</div>
            <div class="step-content">
                <h3 class="step-title">🤖 AI Analysis</h3>
                <p class="step-desc">Get instant summaries, quizzes, and mindmaps generated by AI.</p>
            </div>
        </div>
        
        <div class="step-arrow">→</div>
        
        <div class="step-item">
            <div class="step-number">3</div>
            <div class="step-content">
                <h3 class="step-title">📚 Learn & Master</h3>
                <p class="step-desc">Use flashcards, chat, and study plans to master the content.</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Call to Action
st.markdown("<div style='margin: 4rem 0;'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="cta-card">
        <h2 class="cta-title">Ready to Start Learning?</h2>
        <p class="cta-desc">Choose an upload method from the sidebar to begin</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("📄 Upload PDF", use_container_width=True, type="primary"):
            st.switch_page("pages/1_📄_Upload_PDF.py")
    with col_b:
        if st.button("🖼️ Upload Image", use_container_width=True):
            st.switch_page("pages/2_🖼️_Upload_Image.py")
    with col_c:
        if st.button("✍️ Paste Text", use_container_width=True):
            st.switch_page("pages/3_✍️_Upload_Text.py")

# Tips Section
st.markdown("<div style='margin: 4rem 0;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tip-card">
        <div class="tip-icon">💡</div>
        <h3 class="tip-title">Pro Tips</h3>
        <ul class="tip-list">
            <li>Upload clear, high-quality documents for best results</li>
            <li>Use the chat feature to ask specific questions</li>
            <li>Generate flashcards for effective memorization</li>
            <li>Create study plans to stay organized</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="tip-card">
        <div class="tip-icon">🎯</div>
        <h3 class="tip-title">Earn More XP</h3>
        <ul class="tip-list">
            <li>Upload documents: +50 XP</li>
            <li>Chat with AI: +5 XP per message</li>
            <li>Study flashcards: +10 XP per card</li>
            <li>Complete quizzes: +20 XP</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <p class="footer-text">🧠 AI Research Companion</p>
        <p class="footer-subtext">Powered by FastAPI Backend • Built with Streamlit • Designed for Excellence</p>
    </div>
</div>
""", unsafe_allow_html=True)