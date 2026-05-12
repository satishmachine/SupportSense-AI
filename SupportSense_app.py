"""
SupportSense-AI — Streamlit Application
=========================================

A polished Streamlit UI for the SupportSense-AI review analysis workflow.
Run with:  streamlit run SupportSense_app.py
"""

import streamlit as st
from workflow import analyze_review

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="SupportSense AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# Custom CSS — Premium Dark Theme
# ──────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Import Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root variables ── */
:root {
    --bg-primary: #0f0f1a;
    --bg-card: rgba(255, 255, 255, 0.04);
    --bg-card-hover: rgba(255, 255, 255, 0.07);
    --border-card: rgba(255, 255, 255, 0.08);
    --accent-violet: #8b5cf6;
    --accent-violet-dim: rgba(139, 92, 246, 0.15);
    --accent-green: #34d399;
    --accent-green-dim: rgba(52, 211, 153, 0.12);
    --accent-rose: #fb7185;
    --accent-rose-dim: rgba(251, 113, 133, 0.12);
    --accent-amber: #fbbf24;
    --accent-amber-dim: rgba(251, 191, 36, 0.12);
    --accent-sky: #38bdf8;
    --accent-sky-dim: rgba(56, 189, 248, 0.12);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --radius: 16px;
    --radius-sm: 10px;
    --shadow-glow: 0 0 40px rgba(139, 92, 246, 0.08);
}

/* ── Global resets ── */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Hide Streamlit default elements ── */
#MainMenu, footer, [data-testid="stDecoration"] { display: none !important; }

/* ── Hero section ── */
.hero-container {
    text-align: center;
    padding: 2rem 1rem 1.5rem;
}
.hero-icon {
    font-size: 3.5rem;
    margin-bottom: 0.4rem;
    filter: drop-shadow(0 0 24px rgba(139,92,246,0.5));
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #8b5cf6 0%, #38bdf8 50%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    color: var(--text-secondary);
    font-size: 1.05rem;
    font-weight: 400;
    margin-top: 0.4rem;
}

/* ── Glass card ── */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: var(--radius);
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow-glow);
    transition: background 0.3s, border 0.3s;
}
.glass-card:hover {
    background: var(--bg-card-hover);
    border-color: rgba(139,92,246,0.18);
}
.card-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-muted);
    margin-bottom: 0.6rem;
}

/* ── Sentiment badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.88rem;
    letter-spacing: 0.3px;
}
.badge-positive {
    background: var(--accent-green-dim);
    color: var(--accent-green);
    border: 1px solid rgba(52,211,153,0.25);
}
.badge-negative {
    background: var(--accent-rose-dim);
    color: var(--accent-rose);
    border: 1px solid rgba(251,113,133,0.25);
}

/* ── Diagnosis chips ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 0.5rem; }
.chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 500;
}
.chip-violet  { background: var(--accent-violet-dim); color: var(--accent-violet); border: 1px solid rgba(139,92,246,0.2); }
.chip-amber   { background: var(--accent-amber-dim);  color: var(--accent-amber);  border: 1px solid rgba(251,191,36,0.2); }
.chip-sky     { background: var(--accent-sky-dim);     color: var(--accent-sky);     border: 1px solid rgba(56,189,248,0.2); }

/* ── Response area ── */
.response-text {
    color: var(--text-primary);
    font-size: 0.95rem;
    line-height: 1.75;
    white-space: pre-wrap;
}

/* ── Workflow steps ── */
.step-bar {
    display: flex;
    justify-content: center;
    gap: 6px;
    margin: 1.5rem 0 0.6rem;
}
.step-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--border-card);
    transition: background 0.4s, box-shadow 0.4s;
}
.step-dot.active {
    background: var(--accent-violet);
    box-shadow: 0 0 10px rgba(139,92,246,0.6);
}
.step-label {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.5px;
}

/* ── Text area ── */
[data-testid="stTextArea"] textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 1rem !important;
    transition: border 0.3s !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent-violet) !important;
    box-shadow: 0 0 0 2px var(--accent-violet-dim) !important;
}

/* ── Primary button ── */
[data-testid="stButton"] button[kind="primary"],
.stButton > button {
    background: linear-gradient(135deg, #8b5cf6, #6d28d9) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 2rem !important;
    letter-spacing: 0.3px !important;
    transition: transform 0.2s, box-shadow 0.3s !important;
    width: 100% !important;
}
[data-testid="stButton"] button[kind="primary"]:hover,
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(139,92,246,0.35) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--accent-violet) !important; }

/* ── Divider ── */
hr { border-color: var(--border-card) !important; }

/* ── Example pills ── */
.example-pill {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.25s;
    margin: 3px;
}
.example-pill:hover {
    background: var(--accent-violet-dim);
    border-color: rgba(139,92,246,0.3);
    color: var(--accent-violet);
}
</style>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# Hero Header
# ──────────────────────────────────────────────
st.markdown(
    """
<div class="hero-container">
    <div class="hero-icon">🧠</div>
    <h1 class="hero-title">SupportSense AI</h1>
    <p class="hero-subtitle">Intelligent Review Analysis &amp; Response Engine</p>
</div>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# Example Reviews
# ──────────────────────────────────────────────
EXAMPLES = {
    "😠 Login Bug": "I have been trying to log in for over an hour now, & app keeps getting stuck, really frustrating!",
    "😞 Slow App": "The app is incredibly slow, pages take forever to load. Very disappointed with the performance.",
    "😊 Great Support": "Your customer support team was amazing! They resolved my issue within minutes. Truly impressed!",
    "🤬 Broken Feature": "The payment feature is completely broken! I lost money because of this bug. Absolutely unacceptable!",
    "💚 Love It": "This product has completely transformed my workflow. The UI is beautiful and everything just works perfectly.",
}

st.markdown('<p class="card-label" style="text-align:center;">Try an example</p>', unsafe_allow_html=True)
cols = st.columns(len(EXAMPLES))
for i, (label, text) in enumerate(EXAMPLES.items()):
    with cols[i]:
        if st.button(label, key=f"ex_{i}", use_container_width=True):
            st.session_state["review_input"] = text

# ──────────────────────────────────────────────
# Input Area
# ──────────────────────────────────────────────
st.markdown("---")

review_text = st.text_area(
    "📝  Paste a customer review",
    value=st.session_state.get("review_input", ""),
    height=130,
    placeholder="e.g. The app crashes every time I try to upload a file…",
)

analyze_clicked = st.button("⚡  Analyze Review", type="primary", use_container_width=True)

# ──────────────────────────────────────────────
# Analysis Pipeline
# ──────────────────────────────────────────────
if analyze_clicked and review_text.strip():
    with st.spinner("🔍  Analyzing sentiment & generating response…"):
        result = analyze_review(review_text.strip())

    sentiment = result.get("sentiment", "unknown")
    diagnosis = result.get("diagnosis")
    response = result.get("response", "")

    # ── Workflow Steps ──
    is_negative = sentiment == "negative"
    total_steps = 4 if is_negative else 2
    st.markdown(
        f"""
    <div class="step-bar">
        <div class="step-dot active"></div>
        <div class="step-dot active"></div>
        {"<div class='step-dot active'></div><div class='step-dot active'></div>" if is_negative else ""}
    </div>
    <p class="step-label">{total_steps}/{total_steps} workflow nodes completed</p>
    """,
        unsafe_allow_html=True,
    )

    # ── Sentiment Card ──
    badge_cls = "badge-positive" if sentiment == "positive" else "badge-negative"
    badge_icon = "✅" if sentiment == "positive" else "⚠️"
    st.markdown(
        f"""
    <div class="glass-card">
        <p class="card-label">Detected Sentiment</p>
        <span class="badge {badge_cls}">{badge_icon} {sentiment.upper()}</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Diagnosis Card (negative only) ──
    if diagnosis:
        issue = diagnosis.get("issue_type", "—")
        tone = diagnosis.get("tone", "—")
        urgency = diagnosis.get("urgency", "—")
        st.markdown(
            f"""
        <div class="glass-card">
            <p class="card-label">Issue Diagnosis</p>
            <div class="chip-row">
                <span class="chip chip-violet">🏷️ {issue}</span>
                <span class="chip chip-amber">🎭 {tone}</span>
                <span class="chip chip-sky">🔥 Urgency: {urgency}</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ── Response Card ──
    st.markdown(
        f"""
    <div class="glass-card">
        <p class="card-label">Generated Response</p>
        <div class="response-text">{response}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

elif analyze_clicked:
    st.warning("Please enter a review before analyzing.")

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
<div style="text-align:center; padding: 0.5rem 0 1.5rem;">
    <span style="color: var(--text-muted); font-size: 0.78rem;">
        Built with ❤️ using <strong>LangGraph</strong> · <strong>Groq</strong> · <strong>Streamlit</strong>
    </span>
</div>
""",
    unsafe_allow_html=True,
)
