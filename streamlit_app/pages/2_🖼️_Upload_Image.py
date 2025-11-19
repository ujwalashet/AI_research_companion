import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils import upload_image, add_xp, show_loading, inject_card_css, show_success_message

st.set_page_config(page_title="Upload Image", page_icon="🖼️", layout="wide")

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

inject_card_css()

# Page header
st.markdown("""
<div class="hero-section" style="padding: 2rem;">
    <h1 class="hero-title" style="font-size: 3rem;">
        <span class="gradient-text">🖼️ Upload Image</span>
    </h1>
    <p class="hero-subtitle" style="font-size: 1.2rem;">
        Extract text from images using OCR technology
    </p>
</div>
""", unsafe_allow_html=True)

# File uploader
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'webp'],
        help="Upload an image with text to extract",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        # Display image preview
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)
        
        st.markdown(f"""
        <div class="custom-card" style="text-align: center;">
            <h3 style="color: var(--text-primary);">{uploaded_file.name}</h3>
            <p style="color: var(--text-secondary);">Size: {uploaded_file.size / 1024:.2f} KB</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Extract Text", use_container_width=True, type="primary"):
            with show_loading():
                result = upload_image(uploaded_file)
                
                if result:
                    st.session_state.extracted_content = result.get('extracted_text', '')
                    st.session_state.summary = result.get('summary', '')
                    
                    add_xp(40, "🖼️ Image Analyzer")
                    show_success_message("Text extracted successfully! 🎉")
                    st.rerun()

# Display results if available
if st.session_state.get('extracted_content'):
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📝 Extracted Text", "📄 Summary"])
    
    with tab1:
        st.markdown("""
        <div class="custom-card">
            <div class="card-header">
                <span class="card-icon">📝</span>
                <h3 class="card-title">Extracted Text</h3>
            </div>
            <div class="card-content">
        """, unsafe_allow_html=True)
        
        st.text_area(
            "Extracted Content",
            st.session_state.extracted_content,
            height=300,
            label_visibility="collapsed"
        )
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        if st.button("📋 Copy Text", use_container_width=True):
            st.write("✅ Copied to clipboard!")
    
    with tab2:
        st.markdown("""
        <div class="custom-card">
            <div class="card-header">
                <span class="card-icon">📄</span>
                <h3 class="card-title">AI Summary</h3>
            </div>
            <div class="card-content">
        """, unsafe_allow_html=True)
        
        st.write(st.session_state.summary)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

else:
    st.markdown("---")
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-icon">💡</span>
            <h3 class="card-title">Supported Image Types</h3>
        </div>
        <div class="card-content">
            <ul style="line-height: 2;">
                <li>📷 Photos of documents, notes, or books</li>
                <li>📱 Screenshots with text content</li>
                <li>🖼️ Scanned pages or receipts</li>
                <li>📊 Charts and diagrams with labels</li>
                <li>✍️ Handwritten notes (may vary in accuracy)</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tips
st.markdown("---")
st.markdown("""
<div class="custom-card">
    <div class="card-header">
        <span class="card-icon">💡</span>
        <h3 class="card-title">Tips for Best OCR Results</h3>
    </div>
    <div class="card-content">
        <ul style="line-height: 2;">
            <li>📸 Use high-resolution, clear images</li>
            <li>💡 Ensure good lighting and contrast</li>
            <li>📏 Keep text straight and aligned</li>
            <li>🎯 Crop to focus on the text area</li>
            <li>🖼️ Avoid blurry or distorted images</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)