"""
AI Research Companion - Utility Functions
Helper functions and API integration for the Streamlit frontend
"""

import streamlit as st
import requests
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

# ==================== CONFIGURATION ====================
API_BASE_URL = "http://127.0.0.1:8000"

# ==================== API INTEGRATION FUNCTIONS ====================

def upload_pdf(file) -> Optional[Dict]:
    """
    Upload PDF to backend for processing
    
    Args:
        file: Streamlit UploadedFile object
        
    Returns:
        Dict with extracted_content, summary, quiz, or None on error
    """
    try:
        files = {"file": (file.name, file.getvalue(), "application/pdf")}
        response = requests.post(f"{API_BASE_URL}/upload_pdf", files=files, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The file may be too large.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to backend. Please ensure it's running on " + API_BASE_URL)
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ HTTP Error: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        st.error(f"❌ Error uploading PDF: {str(e)}")
        return None

def upload_image(file) -> Optional[Dict]:
    """
    Upload image to backend for OCR processing
    
    Args:
        file: Streamlit UploadedFile object
        
    Returns:
        Dict with extracted_text, summary, or None on error
    """
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{API_BASE_URL}/upload_image", files=files, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Try a smaller image.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to backend. Please ensure it's running on " + API_BASE_URL)
        return None
    except Exception as e:
        st.error(f"❌ Error uploading image: {str(e)}")
        return None

def upload_text(text: str) -> Optional[Dict]:
    """
    Upload text to backend for processing
    
    Args:
        text: Plain text string
        
    Returns:
        Dict with summary, quiz, or None on error
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/upload_text",
            json={"text": text},
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to backend. Please ensure it's running on " + API_BASE_URL)
        return None
    except Exception as e:
        st.error(f"❌ Error uploading text: {str(e)}")
        return None

def research_topic(topic: str) -> Optional[Dict]:
    """
    Research a topic using backend
    
    Args:
        topic: Topic to research
        
    Returns:
        Dict with research results or None on error
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/research",
            json={"topic": topic},
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"❌ Error researching topic: {str(e)}")
        return None

def generate_mindmap(content: str) -> str:
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate_mindmap",
            data={"text": content},   # <-- FORM data, not JSON
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("mindmap", "")
    except Exception as e:
        st.error(f"❌ Error generating mindmap: {str(e)}")
        return ""


def upload_to_rag(content: str, metadata: Optional[Dict] = None) -> bool:
    """
    Upload content to RAG system via temp file
    """

    try:
        # create a temporary file because backend expects UploadFile
        temp_file = "temp_rag.txt"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(content)

        files = {
            "file": ("rag.txt", open(temp_file, "rb"), "text/plain")
        }

        response = requests.post(
            f"{API_BASE_URL}/upload_to_rag",
            files=files,
            timeout=60
        )
        response.raise_for_status()
        return True

    except Exception as e:
        st.error(f"❌ Error uploading to RAG: {str(e)}")
        return False


def rag_chat(question: str) -> str:
    """
    Chat with RAG system
    
    Args:
        question: User question
        
    Returns:
        AI response string
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}/rag_chat",
            params={"question": question},
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result.get("answer", "No response received")
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to backend. Please ensure it's running."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ==================== GAMIFICATION FUNCTIONS ====================

def add_xp(points: int, badge: Optional[str] = None):
    """
    Add XP points and optionally a badge to session state
    
    Args:
        points: XP points to add
        badge: Optional badge name to award
    """
    st.session_state.xp += points
    
    if badge and badge not in st.session_state.badges:
        st.session_state.badges.append(badge)
        st.balloons()
        st.toast(f"🎉 Achievement Unlocked: {badge}", icon="🏆")

def check_level_up():
    """Check if user leveled up and show notification"""
    old_level = st.session_state.get('prev_level', 1)
    new_level = (st.session_state.xp // 100) + 1
    
    if new_level > old_level:
        st.session_state.prev_level = new_level
        st.balloons()
        st.success(f"🎊 Level Up! You reached Level {new_level}!")

# ==================== UI HELPER FUNCTIONS ====================

def show_loading(message: str = "🔮 AI is working its magic..."):
    """Display a loading spinner"""
    return st.spinner(message)

def show_success_message(message: str):
    """Show a custom success message"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.25rem 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.4);
        animation: slideIn 0.5s ease;
    ">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">✅</span>
            <span style="font-size: 1.15rem; font-weight: 700;">{message}</span>
        </div>
    </div>
    <style>
    @keyframes slideIn {{
        from {{ transform: translateX(-100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def show_error_message(message: str):
    """Show a custom error message"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.25rem 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.4);
    ">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">⚠️</span>
            <span style="font-size: 1.15rem; font-weight: 700;">{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_info_message(message: str):
    """Show a custom info message"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.25rem 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    ">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">ℹ️</span>
            <span style="font-size: 1.15rem; font-weight: 700;">{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_progress_bar(progress: int, label: str = "Progress", color: str = "primary"):
    """
    Create a custom animated progress bar
    
    Args:
        progress: Progress percentage (0-100)
        label: Label text
        color: Color theme (primary, success, warning, danger)
    """
    gradient_map = {
        "primary": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "success": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "warning": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "danger": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
    }
    
    gradient = gradient_map.get(color, gradient_map["primary"])
    
    st.markdown(f"""
    <div style="margin: 2rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
            <span style="color: var(--text-primary); font-weight: 700; font-size: 1.1rem;">{label}</span>
            <span style="color: var(--text-secondary); font-weight: 700; font-size: 1.1rem;">{progress}%</span>
        </div>
        <div style="
            width: 100%;
            height: 16px;
            background: var(--bg-tertiary);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2);
        ">
            <div style="
                width: {progress}%;
                height: 100%;
                background: {gradient};
                border-radius: 12px;
                transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 0 20px rgba(102, 126, 234, 0.6);
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 50%;
                    background: linear-gradient(180deg, rgba(255,255,255,0.3), transparent);
                    border-radius: 12px 12px 0 0;
                "></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_custom_card(title: str, content: str, icon: str = "📄", card_type: str = "default"):
    """
    Create a custom styled card
    
    Args:
        title: Card title
        content: Card content (HTML supported)
        icon: Icon emoji
        card_type: Type of card (default, success, warning, info)
    """
    gradient_map = {
        "default": "var(--border-color)",
        "success": "#4facfe",
        "warning": "#fee140",
        "info": "#667eea"
    }
    
    border_color = gradient_map.get(card_type, gradient_map["default"])
    
    st.markdown(f"""
    <div class="custom-card" style="border-color: {border_color};">
        <div class="card-header">
            <span class="card-icon">{icon}</span>
            <h3 class="card-title">{title}</h3>
        </div>
        <div class="card-content">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def inject_custom_css():
    """Inject additional custom CSS for cards and components"""
    st.markdown("""
    <style>
    .custom-card {
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        border-radius: 25px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-md);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--border-color);
    }
    
    .card-icon {
        font-size: 2.5rem;
    }
    
    .card-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0;
    }
    
    .card-content {
        color: var(--text-secondary);
        font-size: 1.05rem;
        line-height: 1.8;
    }
    
    .upload-box {
        border: 3px dashed var(--border-color);
        border-radius: 25px;
        padding: 3rem;
        text-align: center;
        background: var(--bg-tertiary);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .upload-box:hover {
        border-color: #667eea;
        background: var(--bg-secondary);
        transform: scale(1.02);
    }
    
    .upload-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== DATA FORMATTING FUNCTIONS ====================

def format_timestamp(timestamp: datetime = None) -> str:
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%I:%M %p")

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

# ==================== VALIDATION FUNCTIONS ====================

def validate_file_type(file, allowed_types: List[str]) -> bool:
    """
    Validate if file type is allowed
    
    Args:
        file: Uploaded file
        allowed_types: List of allowed file extensions
        
    Returns:
        True if valid, False otherwise
    """
    if file is None:
        return False
    
    file_ext = file.name.split('.')[-1].lower()
    return file_ext in allowed_types

def validate_file_size(file, max_size_mb: int = 10) -> bool:
    """
    Validate if file size is within limit
    
    Args:
        file: Uploaded file
        max_size_mb: Maximum size in MB
        
    Returns:
        True if valid, False otherwise
    """
    if file is None:
        return False
    
    max_size_bytes = max_size_mb * 1024 * 1024
    return file.size <= max_size_bytes

# ==================== SESSION STATE HELPERS ====================

def init_page_state(page_name: str, defaults: Dict):
    """Initialize session state for a specific page"""
    if f'{page_name}_initialized' not in st.session_state:
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
        st.session_state[f'{page_name}_initialized'] = True

def clear_page_state(page_name: str, keys: List[str]):
    """Clear specific session state keys for a page"""
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]

# ==================== EXPORT FUNCTIONS ====================

def export_to_json(data: Any, filename: str = "export.json") -> bytes:
    """Export data to JSON format"""
    return json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')

def export_to_text(data: str, filename: str = "export.txt") -> bytes:
    """Export data to text format"""
    return data.encode('utf-8')

# ==================== ANALYTICS HELPERS ====================

def track_event(event_name: str, properties: Dict = None):
    """Track user events for analytics"""
    # Placeholder for analytics integration
    if 'events' not in st.session_state:
        st.session_state.events = []
    
    event = {
        'name': event_name,
        'timestamp': datetime.now().isoformat(),
        'properties': properties or {}
    }
    
    st.session_state.events.append(event)

# ==================== CONSTANTS ====================

ALLOWED_PDF_EXTENSIONS = ['pdf']
ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'webp', 'bmp']
ALLOWED_TEXT_EXTENSIONS = ['txt', 'md']

MAX_FILE_SIZE_MB = 10
MAX_TEXT_LENGTH = 50000

# XP Rewards
XP_REWARDS = {
    'upload_pdf': 50,
    'upload_image': 40,
    'upload_text': 30,
    'chat_message': 5,
    'study_flashcard': 10,
    'complete_quiz': 20,
    'create_study_plan': 40,
    'semantic_search': 10,
    'generate_knowledge_graph': 30,
}

# Badge Requirements
BADGES = {
    '📚 PDF Master': 'Upload your first PDF',
    '🖼️ Image Analyzer': 'Extract text from an image',
    '💬 Conversation Master': 'Send 10 chat messages',
    '🧠 Flashcard Pro': 'Study 50 flashcards',
    '🔍 Search Expert': 'Perform 10 searches',
    '📅 Study Planner': 'Create a study plan',
    '🕸️ Knowledge Mapper': 'Generate a knowledge graph',
    '🎓 Quiz Champion': 'Complete 10 quizzes',
    '🌟 AI Explorer': 'Use all features',
    '🚀 Speed Learner': 'Earn 500 XP',
    '💎 Knowledge Hunter': 'Reach Level 10',
    '👑 Master Scholar': 'Reach Level 20',
}