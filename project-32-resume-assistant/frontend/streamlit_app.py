import streamlit as st
import httpx
import json
import uuid
import os
from pathlib import Path
import plotly.graph_objects as go

# Enforce clean, high-density IDE page configurations matching your naming scheme
st.set_page_config(
    page_title="Resume — Workspace Console",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Deep custom theme injection for a premium low-contrast IDE interface
st.markdown(
    """
    <style>
        /* Global Background & Core Typography */
        .stApp { background-color: #0b0f19; color: #e2e8f0; }
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        
        /* Sidebar Styling Overhaul */
        [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 1px solid #1f2937; }
        
        /* Container Cards */
        div[data-testid="stVerticalBlock"] > div {
            background-color: transparent;
        }
        .metric-card {
            background-color: #111827;
            border: 1px solid #1f2937;
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }
        
        /* Custom Button Styling */
        div.stButton > button:first-child {
            background-color: #2563eb;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            width: 100%;
            transition: all 0.2s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #1d4ed8;
            border: none;
        }
        
        /* Hide native Streamlit branding indicators */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize state contracts safely across reruns
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "ats_trend" not in st.session_state:
    # Real scores only: filled from the backend's "ats_score" field, never invented
    st.session_state.ats_trend = []

BACKEND_API_URL = os.getenv("RESUME_BACKEND_URL", "http://127.0.0.1:8000/api/v1")

# Your application board lives in a local, git-ignored file so real company
# names never reach the public repo. Without it, clearly labeled sample data shows.
APPLICATIONS_FILE = Path(__file__).resolve().parent.parent / "data" / "applications.json"
SAMPLE_APPLICATIONS = {
    "saved": ["Sample: ML Intern, fintech", "Sample: Data Analyst, airline"],
    "active": ["Sample: AI Engineer co-op"],
    "offers": [],
}


def load_applications():
    try:
        return json.loads(APPLICATIONS_FILE.read_text(encoding="utf-8")), False
    except (OSError, ValueError):
        return SAMPLE_APPLICATIONS, True

# --- SIDEBAR: COMPACT DOCUMENT INGESTION ---
with st.sidebar:
    st.markdown("### 🛠️ Core Engine Context")
    st.caption(f"Thread Frame ID: `{st.session_state.thread_id}`")
    st.markdown("---")

    st.markdown("#### 📤 Knowledge Base")
    uploaded_file = st.file_uploader(
        "Ingest Word Resume (.docx)", type=["docx"], label_visibility="collapsed"
    )

    if uploaded_file is not None:
        if st.button("Vectorize & Cache Resume"):
            with st.spinner("Processing embeddings into ChromaDB..."):
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                }
                try:
                    response = httpx.post(
                        f"{BACKEND_API_URL}/process-document", files=files, timeout=30.0
                    )
                    if response.status_code == 200:
                        st.success("Context indexed in memory.")
                    else:
                        st.error("Vector database handshake failed.")
                except Exception as e:
                    st.error(f"Backend offline or connection refused: {e}")

# --- MAIN WORKSPACE INTERFACE ---
st.markdown("## 💻 Resume — Workspace Console")
st.markdown(
    "<p style='color: #9ca3af; margin-top:-15px;'>Asynchronous Multi-Agent Application Optimization Platform</p>",
    unsafe_allow_html=True,
)

# Layout: Split Analytics & Kanban Controls
col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("#### 📊 ATS Alignment Progress Index")
    if not st.session_state.ats_trend:
        st.caption("No scores yet. A point appears each time the backend scores your resume against a job.")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            y=st.session_state.ats_trend,
            mode="lines+markers",
            name="ATS Index",
            line=dict(color="#2563eb", width=3),
            marker=dict(size=8, color="#60a5fa"),
        )
    )
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=10, r=10, t=10, b=10),
        height=180,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#1f2937"),
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("#### 📋 Targeted Application Pipeline")
    applications, is_sample = load_applications()
    if is_sample:
        st.caption("Sample data. Add data/applications.json (git-ignored) to track your own.")
    columns = [
        ("saved", "📌 SAVED", "#1e1b4b", "#c084fc"),
        ("active", "⏳ ACTIVE", "#1c1917", "#fb923c"),
        ("offers", "🎉 OFFERS", "#064e3b", "#4ade80"),
    ]
    for col, (key, label, bg, fg) in zip(st.columns(3), columns):
        items = "<br>".join(f"• {item}" for item in applications.get(key, [])) or "—"
        with col:
            st.markdown(
                f"<div style='background:{bg}; padding:10px; border-radius:6px; min-height:115px;'>"
                f"<b style='color:{fg};'>{label}</b><br>"
                f"<span style='font-size:11px; color:#cbd5e1;'>{items}</span></div>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 💬 Active Multi-Agent Optimization Console")

# Render historical conversation elements cleanly from memory session blocks
for agent, message in st.session_state.chat_history:
    with st.chat_message(name="user" if agent == "user" else "assistant"):
        st.markdown(f"**{agent.upper()}**: {message}")

# Central execution input frame
if user_input := st.chat_input(
    "Paste a new job URL or requirements text matrix to trigger the orchestration engine..."
):
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response_content = ""
        last_displayed_agent = None

        payload = {"message": user_input, "thread_id": st.session_state.thread_id}
        try:
            with httpx.stream(
                "POST", f"{BACKEND_API_URL}/chat/stream", data=payload, timeout=60.0
            ) as r:
                for line in r.iter_lines():
                    if line.startswith("data: "):
                        data_chunk = json.loads(line[6:])

                        # Guard rails against processing error messages from stream
                        if "error" in data_chunk:
                            st.error(data_chunk["error"])
                            break

                        # Record a real score only when the backend sends one
                        if isinstance(data_chunk.get("ats_score"), (int, float)):
                            st.session_state.ats_trend.append(data_chunk["ats_score"])

                        chunk_agent = data_chunk.get("agent", "system").upper()
                        chunk_content = data_chunk.get("content", "")

                        # Prepend the appropriate agent tag only when the active node changes
                        if chunk_agent != last_displayed_agent:
                            if full_response_content:
                                full_response_content += "\n\n"
                            full_response_content += f"### 🤖 [{chunk_agent}]\n"
                            last_displayed_agent = chunk_agent

                        full_response_content += chunk_content
                        placeholder.markdown(full_response_content)

            # Log the complete, finalized clean stream chunk directly into local memory state arrays
            st.session_state.chat_history.append(
                ("AI System Operator", full_response_content)
            )

            st.rerun()

        except Exception as e:
            st.error(f"Data stream infrastructure disconnected unexpectedly: {e}")
