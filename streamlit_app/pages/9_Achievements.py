import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils import inject_custom_css, XP_REWARDS, BADGES

st.set_page_config(page_title="Achievements", page_icon="🏆", layout="wide")
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

# ------------------------ HERO SECTION ------------------------
st.markdown("""
<div class="hero-section" style="padding: 2rem;">
    <h1 class="hero-title"><span class="gradient-text">🏆 Achievements</span></h1>
    <p class="hero-subtitle">Track your progress, XP, levels, and earned badges.</p>
</div>
""", unsafe_allow_html=True)

# ------------------------ SESSION STATE ------------------------
xp = st.session_state.get("xp", 0)
badges = st.session_state.get("badges", [])
level = (xp // 100) + 1
progress = (xp % 100) / 100

# ------------------------ LEVEL + XP CARD ------------------------
st.markdown("""
<style>
.xp-card-premium {
    background: var(--bg-secondary);
    padding: 2rem;
    border-radius: 25px;
    border: 2px solid var(--border-color);
    box-shadow: var(--shadow-lg);
}
.level-circle {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: var(--bg-primary);
    display:flex;
    justify-content:center;
    align-items:center;
    font-size:2.5rem;
    font-weight:900;
    margin:auto;
    border: 6px solid #667eea;
    box-shadow: 0 0 25px var(--glow-purple);
}
.badge-box {
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 18px;
    padding: 1rem;
    text-align:center;
    transition: 0.3s ease;
}
.badge-box:hover {
    transform: translateY(-5px);
    border-color:#667eea;
    box-shadow: 0 10px 25px var(--glow-purple);
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2,1])

# -------- LEFT COLUMN (XP & LEVEL) --------
with col1:
    st.markdown("<div class='xp-card-premium'>", unsafe_allow_html=True)

    st.markdown(f"### ⭐ Total XP: **{xp}**")

    # Custom XP Progress Bar
    st.markdown(f"""
    <div style="margin-top:1rem;">
        <span style="font-weight:700;">Level Progress ({int(progress*100)}%)</span>
        <div style="height:16px; background:var(--bg-tertiary); border-radius:12px; margin-top:0.5rem; overflow:hidden;">
            <div style="height:100%; width:{progress*100}%; background:var(--primary-gradient); border-radius:12px; transition:0.4s;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 🎯 Current Level")
    st.markdown(f"""<div class='level-circle'>{level}</div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------- RIGHT COLUMN (BADGES) --------
with col2:
    st.markdown("### 🏅 Earned Badges")

    if badges:
        for b in badges:
            st.markdown(f"""
            <div class='badge-box' style="margin-top:0.5rem;">
                <span style="font-size:1.2rem; font-weight:700;">{b}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No badges earned yet. Use the app to unlock badges!")

# ------------------------ XP REWARD LIST ------------------------
st.markdown("---")
st.markdown("## ⚡ XP Rewards Guide")
for action, reward in XP_REWARDS.items():
    st.markdown(f"- **{action.replace('_',' ').title()}** → {reward} XP")

# ------------------------ BADGE CRITERIA ------------------------
st.markdown("---")
st.markdown("## 🏆 Available Badges")
for badge, desc in BADGES.items():
    st.markdown(f"- **{badge}** — {desc}")
