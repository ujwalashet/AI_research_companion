import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    research_topic,
    add_xp,
    inject_custom_css,
    create_progress_bar
)

st.set_page_config(page_title="Study Plan", page_icon="📅", layout="wide")
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
        <span class="gradient-text">📅 Study Plan Generator</span>
    </h1>
    <p class="hero-subtitle">
        Create structured, AI-assisted study plans based on topics or uploaded content.
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------ USER INPUT ------------------
st.markdown("""
<div class="custom-card">
    <div class="card-header">
        <span class="card-icon">📝</span>
        <h3 class="card-title">Create Your Study Plan</h3>
    </div>
    <div class="card-content">
""", unsafe_allow_html=True)

topic = st.text_input(
    "Enter a topic, chapter or concept",
    placeholder="e.g. Agentic AI, Neural Networks, Chapter 4, etc."
)

col1, col2 = st.columns([3, 1])
with col1:
    days = st.slider("Plan Duration (days)", min_value=1, max_value=30, value=7)
with col2:
    intensity = st.selectbox("Intensity", ["Light", "Moderate", "Intense"])

st.markdown("</div></div>", unsafe_allow_html=True)

# ------------------ GENERATE STUDY PLAN ------------------
if st.button("Generate Study Plan", use_container_width=True):
    if not topic:
        st.warning("Please enter a topic before generating a plan.")
    else:
        with st.spinner("🧠 AI is preparing your personalized study plan..."):
            backend_response = research_topic(topic)

            if backend_response and isinstance(backend_response, dict):
                summary = backend_response.get("summary", "")
                plan = []

                for d in range(1, days + 1):
                    plan.append({
                        "day": d,
                        "focus": f"Study section {(d % 5) + 1}",
                        "tasks": [
                            "Read core section",
                            "Write a brief summary",
                            "Review key concepts",
                            "Practice 3–5 questions"
                        ]
                    })
            else:
                plan = [
                    {
                        "day": d,
                        "focus": f"{topic} — Part {d}",
                        "tasks": [
                            "Read topic notes",
                            "Create bullet-point notes",
                            "Review with flashcards",
                            "Do quick practice questions"
                        ]
                    }
                    for d in range(1, days + 1)
                ]

        # Save plan to session
        st.session_state.study_plans[topic] = plan

        # Award XP
        add_xp(40, "📅 Study Planner")

        st.success("✅ Study plan generated successfully!")

# ------------------ DISPLAY EXISTING PLANS ------------------
if st.session_state.study_plans:
    st.markdown("<h2 class='section-title'>📚 Your Study Plans</h2>", unsafe_allow_html=True)

    for t, plan in st.session_state.study_plans.items():
        st.markdown(f"""
        <div class="custom-card">
            <div class="card-header">
                <span class="card-icon">📘</span>
                <h3 class="card-title">Study Plan: {t}</h3>
            </div>
            <div class="card-content">
        """, unsafe_allow_html=True)

        # Progress
        progress = int((len(plan) / max(1, len(plan))) * 100)
        create_progress_bar(progress, label="Plan Prepared", color="primary")

        # Day-wise breakdown
        for p in plan:
            st.markdown(f"""
            <div style="
                background: var(--bg-tertiary);
                border-radius: 12px;
                padding: 1rem 1.3rem;
                margin-bottom: 1rem;
                border: 1px solid var(--border-color);
            ">
                <h4 style="margin: 0;">📆 Day {p['day']} — {p['focus']}</h4>
                <ul style="margin-top: 0.7rem;">
            """, unsafe_allow_html=True)

            for task in p["tasks"]:
                st.markdown(f"<li>{task}</li>", unsafe_allow_html=True)

            st.markdown("</ul></div>", unsafe_allow_html=True)

        st.markdown("</div></div><br>", unsafe_allow_html=True)
