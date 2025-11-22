import streamlit as st
import sys
from pathlib import Path
import random

sys.path.append(str(Path(__file__).parent.parent))

from utils import add_xp, inject_custom_css, show_success_message

st.set_page_config(page_title="Flashcards", page_icon="🧠", layout="wide")
# ---- Initialize session state if not set ----
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "badges" not in st.session_state:
    st.session_state.badges = []


css_path = Path(__file__).parents[1] / "styles.css"
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


inject_custom_css()

st.markdown("""
<div class="hero-section" style="padding: 2rem;">
    <h1 class="hero-title"><span class="gradient-text">🧠 Flashcards</span></h1>
    <p class="hero-subtitle">Practice with flashcards generated from your document summaries.</p>
</div>
""", unsafe_allow_html=True)

# Initialize flashcards
if 'flashcards' not in st.session_state:
    # If quiz exists, convert to simple Q/A flashcards
    fc = []
    if st.session_state.get("quiz"):
        for q in st.session_state.quiz:
            question = q.get("question")
            answer = q.get("correct_answer") or (q.get("options") and q.get("options")[0]) or "Answer"
            if question:
                fc.append({"q": question, "a": answer, "mastered": False})
    st.session_state.flashcards = fc
    st.session_state.current_card = 0
    st.session_state.is_flipped = False

def flip_card():
    st.session_state.is_flipped = not st.session_state.is_flipped

def next_card():
    st.session_state.current_card = (st.session_state.current_card + 1) % max(1, len(st.session_state.flashcards))
    st.session_state.is_flipped = False

def prev_card():
    st.session_state.current_card = (st.session_state.current_card - 1) % max(1, len(st.session_state.flashcards))
    st.session_state.is_flipped = False

if not st.session_state.flashcards:
    st.info("No flashcards available. Generate them by uploading a document or creating a quiz.")
else:
    card = st.session_state.flashcards[st.session_state.current_card]
    st.markdown(f"""
    <div style="background: var(--bg-secondary); padding: 2rem; border-radius: 20px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style="margin:0">Card {st.session_state.current_card+1} / {len(st.session_state.flashcards)}</h3>
            <div>
                <button id="prev">◀</button>
                <button id="next">▶</button>
            </div>
        </div>
        <div style="margin-top:1.5rem; text-align:center;">
    """, unsafe_allow_html=True)

    if not st.session_state.is_flipped:
        st.markdown(f"<div style='font-size:1.2rem; padding:2rem; border-radius:12px; background:var(--bg-primary);'>{card['q']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='font-size:1.1rem; padding:2rem; border-radius:12px; background:var(--bg-primary);'>**Answer:** {card['a']}</div>", unsafe_allow_html=True)

    # Controls
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        if st.button("◀ Prev"):
            prev_card()
            st.experimental_rerun()
    with col2:
        if st.button("Flip"):
            flip_card()
        if st.button("Mark Mastered"):
            st.session_state.flashcards[st.session_state.current_card]['mastered'] = True
            add_xp(10, None)
            show_success_message("Marked as mastered! +10 XP")
    with col3:
        if st.button("Next ▶"):
            next_card()
            st.experimental_rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Progress
    mastered = sum(1 for c in st.session_state.flashcards if c.get('mastered'))
    st.progress(0 if len(st.session_state.flashcards)==0 else mastered/len(st.session_state.flashcards))
    st.write(f"{mastered} / {len(st.session_state.flashcards)} mastered")
