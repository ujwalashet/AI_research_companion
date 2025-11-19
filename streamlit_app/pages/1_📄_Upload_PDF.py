import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    upload_pdf, generate_mindmap, upload_to_rag, add_xp,
    show_loading, inject_card_css, show_success_message, create_progress_bar
)

st.set_page_config(page_title="Upload PDF", page_icon="📄", layout="wide")

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

inject_card_css()

# Page header
st.markdown("""
<div class="hero-section" style="padding: 2rem;">
    <h1 class="hero-title" style="font-size: 3rem;">
        <span class="gradient-text">📄 Upload PDF</span>
    </h1>
    <p class="hero-subtitle" style="font-size: 1.2rem;">
        Upload your PDF and let AI extract, summarize, and analyze it
    </p>
</div>
""", unsafe_allow_html=True)

# File uploader
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF document to analyze",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        st.markdown(f"""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📄</div>
            <h3 style="color: var(--text-primary);">{uploaded_file.name}</h3>
            <p style="color: var(--text-secondary);">Size: {uploaded_file.size / 1024:.2f} KB</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Analyze PDF", use_container_width=True):
            with show_loading():
                # Upload PDF
                result = upload_pdf(uploaded_file)
                
                if result:
                    st.session_state.extracted_content = result.get('extracted_content', '')
                    st.session_state.summary = result.get('summary', '')
                    st.session_state.quiz = result.get('quiz', [])
                    
                    # Generate mindmap
                    mindmap = generate_mindmap(st.session_state.extracted_content)
                    st.session_state.mindmap = mindmap
                    
                    # Upload to RAG
                    upload_to_rag(st.session_state.extracted_content, {"filename": uploaded_file.name})
                    
                    # Add XP and badge
                    add_xp(50, "📚 PDF Master")
                    
                    show_success_message("PDF analyzed successfully! 🎉")
                    st.rerun()

# Display results if available
if st.session_state.get('extracted_content'):
    st.markdown("---")
    
    # Progress indicator
    create_progress_bar(100, "Analysis Complete")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Summary", "📄 Full Text", "❓ Quiz", "🗺️ Mindmap"])
    
    with tab1:
        st.markdown("""
        <div class="custom-card">
            <div class="card-header">
                <span class="card-icon">📝</span>
                <h3 class="card-title">AI-Generated Summary</h3>
            </div>
            <div class="card-content">
        """, unsafe_allow_html=True)
        
        st.write(st.session_state.summary)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy Summary", use_container_width=True):
                st.write("✅ Copied to clipboard!")
        with col2:
            if st.button("🔄 Regenerate", use_container_width=True):
                st.rerun()
    
    with tab2:
        st.markdown("""
        <div class="custom-card">
            <div class="card-header">
                <span class="card-icon">📄</span>
                <h3 class="card-title">Extracted Text</h3>
            </div>
            <div class="card-content">
        """, unsafe_allow_html=True)
        
        st.text_area(
            "Full Content",
            st.session_state.extracted_content,
            height=400,
            label_visibility="collapsed"
        )
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="custom-card">
            <div class="card-header">
                <span class="card-icon">❓</span>
                <h3 class="card-title">Knowledge Quiz</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.quiz:
            for i, q in enumerate(st.session_state.quiz):
                st.markdown(f"""
                <div class="quiz-card">
                    <div class="quiz-question">
                        {i+1}. {q.get('question', 'Question not available')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                options = q.get('options', [])
                if options:
                    selected = st.radio(
                        f"question_{i}",
                        options,
                        key=f"quiz_{i}",
                        label_visibility="collapsed"
                    )
                    
                    if st.button(f"Check Answer", key=f"check_{i}"):
                        correct = q.get('correct_answer', '')
                        if selected == correct:
                            show_success_message("Correct! 🎉")
                            add_xp(10, None)
                        else:
                            st.error(f"❌ Incorrect. The correct answer is: {correct}")
                
                st.markdown("---")
        else:
            st.info("No quiz questions available. Try uploading a different document.")
    
    with tab4:
        st.markdown("""
        <div class="custom-card">
            <div class="card-header">
                <span class="card-icon">🗺️</span>
                <h3 class="card-title">Concept Mindmap</h3>
            </div>
            <div class="card-content">
        """, unsafe_allow_html=True)
        
        if st.session_state.mindmap:
            st.code(st.session_state.mindmap, language="markdown")
        else:
            st.info("Mindmap generation in progress...")
        
        st.markdown("</div></div>", unsafe_allow_html=True)

# Tips section
st.markdown("---")
st.markdown("""
<div class="custom-card">
    <div class="card-header">
        <span class="card-icon">💡</span>
        <h3 class="card-title">Tips for Best Results</h3>
    </div>
    <div class="card-content">
        <ul style="line-height: 2;">
            <li>📄 Use clear, text-based PDFs (not scanned images)</li>
            <li>📏 Files under 10MB work best</li>
            <li>🎯 Academic papers and articles produce great summaries</li>
            <li>🔍 Use the semantic search feature to find specific information</li>
            <li>💬 Chat with your document using the RAG Chat feature</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)