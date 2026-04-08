import streamlit as st
import time
from chatbot_engine import CollegeChatbot
st.set_page_config(
    page_title="CollegeBot – Your Campus Guide",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ---------- Global ---------- */
html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* ---------- Header card ---------- */
.header-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(168,85,247,0.2));
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 28px;
    backdrop-filter: blur(10px);
}
.header-card h1 {
    font-size: 2.1rem;
    font-weight: 700;
    color: #fff;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}
.header-card p { color: #a5b4fc; margin: 0; font-size: 1rem; }

/* ---------- Chat bubbles ---------- */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    gap: 18px;
    padding: 8px 0;
}

.bubble-user {
    display: flex;
    justify-content: flex-end;
}
.bubble-user .msg {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #fff;
    padding: 14px 20px;
    border-radius: 20px 20px 4px 20px;
    max-width: 70%;
    font-size: 0.95rem;
    line-height: 1.55;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4);
}

.bubble-bot {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 12px;
}
.bot-avatar {
    width: 38px; height: 38px; min-width: 38px;
    background: linear-gradient(135deg, #ec4899, #f97316);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    box-shadow: 0 4px 12px rgba(236,72,153,0.35);
}
.bubble-bot .msg {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: #e2e8f0;
    padding: 14px 20px;
    border-radius: 4px 20px 20px 20px;
    max-width: 72%;
    font-size: 0.95rem;
    line-height: 1.6;
    backdrop-filter: blur(8px);
}

/* ---------- Confidence badge ---------- */
.conf-badge {
    display: inline-block;
    margin-top: 8px;
    padding: 3px 10px;
    border-radius: 30px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
}
.conf-high  { background: rgba(34,197,94,0.2);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3);  }
.conf-med   { background: rgba(251,191,36,0.2); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.conf-low   { background: rgba(239,68,68,0.2);  color: #f87171; border: 1px solid rgba(239,68,68,0.3);  }

/* ---------- Category pill ---------- */
.cat-pill {
    display: inline-block;
    margin-top: 6px; margin-left: 6px;
    padding: 3px 10px;
    border-radius: 30px;
    font-size: 0.73rem;
    background: rgba(99,102,241,0.2);
    color: #a5b4fc;
    border: 1px solid rgba(99,102,241,0.3);
}

/* ---------- Input area ---------- */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    color: #fff !important;
    border-radius: 12px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 12px 16px !important;
}
.stTextInput > div > div > input::placeholder { color: #6b7280 !important; }
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}

/* ---------- Buttons ---------- */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    padding: 12px 28px !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.5) !important;
}

/* ---------- Divider ---------- */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* ---------- Sidebar FAQ buttons ---------- */
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #c7d2fe !important;
    font-weight: 400 !important;
    font-size: 0.82rem !important;
    padding: 8px 14px !important;
    box-shadow: none !important;
    text-align: left !important;
    margin-bottom: 4px !important;
}

/* ---------- Stats cards ---------- */
.stat-grid { display: flex; gap: 14px; margin-top: 20px; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 100px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 14px 18px;
    text-align: center;
}
.stat-card .num { font-size: 1.6rem; font-weight: 700; color: #a5b4fc; }
.stat-card .lbl { font-size: 0.75rem; color: #64748b; margin-top: 2px; }

/* ---------- Scrollable chat ---------- */
.chat-scroll {
    max-height: 520px;
    overflow-y: auto;
    padding-right: 8px;
    scrollbar-width: thin;
    scrollbar-color: rgba(99,102,241,0.4) transparent;
}

/* ---------- Metric overrides ---------- */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 12px !important;
}
[data-testid="metric-container"] label { color: #94a3b8 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #a5b4fc !important; }

/* ---------- Select box ---------- */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    border-radius: 10px !important;
    color: #fff !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ── Session state init ───────────────────────────────────────────────────────
def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "bot" not in st.session_state:
        st.session_state.bot = CollegeChatbot("college_data.csv")
    if "query_count" not in st.session_state:
        st.session_state.query_count = 0
    if "prefill" not in st.session_state:
        st.session_state.prefill = ""


init_state()
bot: CollegeChatbot = st.session_state.bot


# ── Helpers ──────────────────────────────────────────────────────────────────
def conf_class(score: float) -> str:
    if score >= 60:
        return "conf-high"
    elif score >= 30:
        return "conf-med"
    return "conf-low"


def render_bubble_user(text: str):
    st.markdown(
        f'<div class="bubble-user"><div class="msg">{text}</div></div>',
        unsafe_allow_html=True,
    )


def render_bubble_bot(text: str, score: float, category: str):
    cls = conf_class(score)
    badge = f'<span class="conf-badge {cls}">⚡ {score:.1f}% match</span>'
    cat_pill = f'<span class="cat-pill">🏷 {category}</span>' if category != "Unknown" else ""
    st.markdown(
        f"""
        <div class="bubble-bot">
            <div class="bot-avatar">🎓</div>
            <div class="msg">
                {text}
                <br>{badge}{cat_pill}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def add_message(role: str, content: str, score: float = 0.0, category: str = ""):
    st.session_state.messages.append(
        {"role": role, "content": content, "score": score, "category": category}
    )


def process_query(query: str):
    if not query.strip():
        return
    add_message("user", query)
    answer, score, category, _ = bot.get_response(query)
    add_message("bot", answer, score, category)
    st.session_state.query_count += 1
    st.session_state.prefill = ""


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 CollegeBot")
    st.markdown("*Your 24×7 campus information guide*")
    st.markdown("---")

    # Stats
    col1, col2 = st.columns(2)
    col1.metric("Queries", st.session_state.query_count)
    col2.metric("FAQs", len(bot.df))

    st.markdown("---")
    st.markdown("### 📂 Browse by Topic")
    categories = bot.get_all_categories()

    selected_cat = st.selectbox(
        "Choose a category", ["— select —"] + categories, label_visibility="collapsed"
    )

    if selected_cat and selected_cat != "— select —":
        questions = bot.get_questions_by_category(selected_cat)
        for q in questions:
            short = q[:52] + "…" if len(q) > 52 else q
            if st.button(f"❓ {short}", key=f"faq_{q}", use_container_width=True):
                st.session_state.prefill = q

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='color:#475569'>Built with Streamlit + scikit-learn<br>"
        "TF-IDF Vectorizer · Cosine Similarity</small>",
        unsafe_allow_html=True,
    )


# ── Main layout ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="header-card">
        <h1>🎓 College Query Chatbot</h1>
        <p>Ask me anything about admissions, fees, courses, placements, hostel, and more!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Chat history
if st.session_state.messages:
    st.markdown('<div class="chat-scroll">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            render_bubble_user(msg["content"])
        else:
            render_bubble_bot(msg["content"], msg["score"], msg["category"])
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Welcome state
    st.markdown(
        """
        <div style="text-align:center; padding: 60px 20px; color: #475569;">
            <div style="font-size:4rem; margin-bottom:16px;">💬</div>
            <div style="font-size:1.1rem; color:#94a3b8; margin-bottom:8px;">No messages yet</div>
            <div style="font-size:0.9rem;">Type a question below or pick a topic from the sidebar</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Input row ────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])

with col_input:
    user_input = st.text_input(
        "Your question",
        value=st.session_state.prefill,
        placeholder="e.g. What is the fee structure? What courses are available?",
        label_visibility="collapsed",
        key="main_input",
    )

with col_btn:
    send_clicked = st.button("Send 🚀", use_container_width=True)

# Trigger on Enter or button click
if send_clicked and user_input:
    process_query(user_input)
    st.rerun()

# Handle sidebar FAQ prefill
if st.session_state.prefill and st.session_state.prefill != user_input:
    process_query(st.session_state.prefill)
    st.rerun()

# ── Quick-suggest chips ──────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<small style='color:#475569; font-size:0.8rem;'>✨ Quick questions:</small>",
    unsafe_allow_html=True,
)

quick = [
    "What courses are offered?",
    "Fee structure",
    "Placement details",
    "Hostel facilities",
    "Scholarships",
    "College timings",
]

cols = st.columns(len(quick))
for i, q in enumerate(quick):
    with cols[i]:
        if st.button(q, key=f"quick_{i}", use_container_width=True):
            process_query(q)
            st.rerun()
# ── Second row of quick-suggest chips ───────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

quick2 = [
    "Labs",
    "Library",
    "Loan",
    "Location",
    "Placements",
    "Ranking",
    "Sports",
    "Timings",
    "WiFi",
]

cols2 = st.columns(len(quick2))

for i, q in enumerate(quick2):
    with cols2[i]:
        if st.button(q, key=f"quick2_{i}", use_container_width=True):
            process_query(q)
            st.rerun()
