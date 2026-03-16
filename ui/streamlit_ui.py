"""
AI Prompt Optimizer - Streamlit UI
A sleek, dark-themed interface for prompt engineering.
"""

import streamlit as st
import sys
import os
import time
import plotly.graph_objects as go
import plotly.express as px

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import run_optimization_pipeline
from core.llm_engine import AVAILABLE_MODELS
from memory.prompt_memory import get_all_prompts, get_best_prompts, get_stats, clear_memory
from utils.helpers import calculate_improvement_percentage

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Prompt Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background: #0a0a0f;
    color: #e2e8f0;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f1a;
    border-right: 1px solid #1e1e3a;
}

[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}

/* ── Custom Header ── */
.hero-header {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}

.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(139, 92, 246, 0.06) 0%, transparent 50%);
    pointer-events: none;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #c084fc, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    color: #64748b;
    font-size: 1rem;
    margin-top: 8px;
    font-weight: 400;
}

.hero-badges {
    display: flex;
    gap: 8px;
    margin-top: 20px;
    flex-wrap: wrap;
}

.badge {
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
}

/* ── Cards ── */
.card {
    background: #0f0f1a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
}

.card-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #475569;
    margin-bottom: 12px;
}

/* ── Score Display ── */
.score-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-top: 16px;
}

.score-item {
    background: #13131f;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}

.score-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #475569;
    margin-bottom: 8px;
}

.score-value {
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

.score-good { color: #34d399; }
.score-medium { color: #fbbf24; }
.score-poor { color: #f87171; }

/* ── Pipeline steps ── */
.pipeline-step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: #13131f;
    border: 1px solid #1e293b;
    border-radius: 8px;
    margin-bottom: 8px;
    transition: all 0.3s ease;
}

.step-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    background: rgba(99, 102, 241, 0.15);
    flex-shrink: 0;
}

.step-active { border-color: #6366f1; background: #1a1a2e; }
.step-done { border-color: #34d399; opacity: 0.7; }

/* ── Prompt Display ── */
.prompt-box {
    background: #080812;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    line-height: 1.7;
    color: #cbd5e1;
    white-space: pre-wrap;
    word-break: break-word;
}

.prompt-box-original { border-left: 3px solid #f87171; }
.prompt-box-optimized { border-left: 3px solid #34d399; }

/* ── Response Box ── */
.response-box {
    background: #080812;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 20px;
    font-size: 0.9rem;
    line-height: 1.7;
    color: #e2e8f0;
    max-height: 400px;
    overflow-y: auto;
}

/* ── Improvement Badge ── */
.improvement-banner {
    background: linear-gradient(135deg, rgba(52, 211, 153, 0.1), rgba(99, 102, 241, 0.1));
    border: 1px solid rgba(52, 211, 153, 0.3);
    border-radius: 12px;
    padding: 20px 28px;
    text-align: center;
    margin: 24px 0;
}

.improvement-number {
    font-size: 3rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    color: #34d399;
}

.improvement-label {
    font-size: 0.8rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}

/* ── Problem Tags ── */
.problem-tag {
    display: inline-block;
    background: rgba(248, 113, 113, 0.1);
    border: 1px solid rgba(248, 113, 113, 0.25);
    color: #fca5a5;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    margin: 3px;
}

.suggestion-tag {
    display: inline-block;
    background: rgba(52, 211, 153, 0.1);
    border: 1px solid rgba(52, 211, 153, 0.25);
    color: #6ee7b7;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    margin: 3px;
}

.type-tag {
    display: inline-block;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.35);
    color: #a5b4fc;
    padding: 5px 14px;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
}

/* ── Text Areas & Inputs ── */
.stTextArea textarea {
    background: #0f0f1a !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
}

.stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
}

.stSelectbox select, [data-baseweb="select"] {
    background: #0f0f1a !important;
    border: 1px solid #1e293b !important;
    color: #e2e8f0 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0f0f1a;
    border-bottom: 1px solid #1e293b;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #64748b;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    border-radius: 6px 6px 0 0;
}

.stTabs [aria-selected="true"] {
    background: rgba(99, 102, 241, 0.1) !important;
    color: #a5b4fc !important;
    border-bottom: 2px solid #6366f1 !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #0f0f1a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 16px;
}

[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-family: 'JetBrains Mono', monospace !important; }

/* ── Dividers ── */
hr { border-color: #1e293b !important; }

/* ── Expander ── */
details {
    background: #0f0f1a !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2d3748; }

/* ── Status messages ── */
.stSuccess { background: rgba(52, 211, 153, 0.08) !important; border: 1px solid rgba(52, 211, 153, 0.2) !important; }
.stInfo { background: rgba(99, 102, 241, 0.08) !important; border: 1px solid rgba(99, 102, 241, 0.2) !important; }
.stWarning { background: rgba(251, 191, 36, 0.08) !important; border: 1px solid rgba(251, 191, 36, 0.2) !important; }
.stError { background: rgba(248, 113, 113, 0.08) !important; border: 1px solid rgba(248, 113, 113, 0.2) !important; }

/* ── Section Dividers ── */
.section-header {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #334155;
    padding: 8px 0 4px;
    border-bottom: 1px solid #1e293b;
    margin-bottom: 16px;
}

/* ── Feedback tiles ── */
.feedback-tile {
    background: #13131f;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 8px;
}

.feedback-tile-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #475569;
    margin-bottom: 5px;
}

.feedback-tile-text {
    font-size: 0.85rem;
    color: #cbd5e1;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)


# ─── Helper Functions ──────────────────────────────────────────────────────────

def make_score_color(score: float) -> str:
    if score >= 7.5:
        return "score-good"
    elif score >= 5:
        return "score-medium"
    return "score-poor"


def render_score_card(label: str, value: float):
    css_class = make_score_color(value)
    return f"""
    <div class="score-item">
        <div class="score-label">{label}</div>
        <div class="score-value {css_class}">{value}</div>
    </div>
    """


def make_radar_chart(original_score, optimized_score):
    categories = ["Clarity", "Specificity", "Context", "Structure"]
    orig_vals = [
        original_score.clarity,
        original_score.specificity,
        original_score.context,
        original_score.structure,
    ]
    opt_vals = [
        optimized_score.clarity,
        optimized_score.specificity,
        optimized_score.context,
        optimized_score.structure,
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=orig_vals + [orig_vals[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Original",
        line_color="#f87171",
        fillcolor="rgba(248, 113, 113, 0.1)",
    ))
    fig.add_trace(go.Scatterpolar(
        r=opt_vals + [opt_vals[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Optimized",
        line_color="#34d399",
        fillcolor="rgba(52, 211, 153, 0.1)",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="#0a0a0f",
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                color="#334155",
                gridcolor="#1e293b",
            ),
            angularaxis=dict(color="#64748b", gridcolor="#1e293b"),
        ),
        showlegend=True,
        paper_bgcolor="#0a0a0f",
        plot_bgcolor="#0a0a0f",
        font_color="#94a3b8",
        margin=dict(l=30, r=30, t=30, b=30),
        legend=dict(
            bgcolor="rgba(15,15,26,0.8)",
            bordercolor="#1e293b",
            borderwidth=1,
        ),
    )
    return fig


def make_bar_comparison(original_score, optimized_score):
    categories = ["Clarity", "Specificity", "Context", "Structure", "Overall"]
    orig_vals = [
        original_score.clarity,
        original_score.specificity,
        original_score.context,
        original_score.structure,
        original_score.total,
    ]
    opt_vals = [
        optimized_score.clarity,
        optimized_score.specificity,
        optimized_score.context,
        optimized_score.structure,
        optimized_score.total,
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Original",
        x=categories,
        y=orig_vals,
        marker_color="#f87171",
        marker_line_color="#0a0a0f",
        marker_line_width=1,
    ))
    fig.add_trace(go.Bar(
        name="Optimized",
        x=categories,
        y=opt_vals,
        marker_color="#34d399",
        marker_line_color="#0a0a0f",
        marker_line_width=1,
    ))
    fig.update_layout(
        barmode="group",
        paper_bgcolor="#0a0a0f",
        plot_bgcolor="#0a0a0f",
        font_color="#94a3b8",
        yaxis=dict(range=[0, 10], gridcolor="#1e293b", color="#475569"),
        xaxis=dict(color="#475569", gridcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(bgcolor="rgba(15,15,26,0.8)", bordercolor="#1e293b", borderwidth=1),
    )
    return fig


# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 10px; text-align: center;'>
        <div style='font-size: 2rem;'>⚡</div>
        <div style='font-size: 1rem; font-weight: 700; color: #a5b4fc; margin-top: 4px;'>Prompt Optimizer</div>
        <div style='font-size: 0.7rem; color: #334155; margin-top: 2px;'>AI Prompt Engineering System</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Configuration</div>', unsafe_allow_html=True)

    selected_model = st.selectbox(
        "🤖 LLM Model",
        options=list(AVAILABLE_MODELS.keys()),
        index=0,  # Ollama is first
        help="Select the model to generate responses",
    )

    temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative, Lower = more focused",
    )

    use_self_refine = st.toggle(
        "🔄 Self-Refine Loop",
        value=False,
        help="Run the prompt through multiple refinement iterations",
    )

    save_to_memory = st.toggle(
        "💾 Save to Memory",
        value=True,
        help="Store optimized prompts for future reference",
    )

    st.markdown('<div class="section-header" style="margin-top:20px;">API Keys</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.2);
    border-radius:8px;padding:10px 14px;margin-bottom:12px;">
        <div style="color:#34d399;font-size:0.75rem;font-weight:600;">🦙 Ollama Active</div>
        <div style="color:#64748b;font-size:0.7rem;margin-top:2px;">Running locally — no API key needed. Unlimited & free!</div>
    </div>
    """, unsafe_allow_html=True)

    gemini_key = st.text_input(
        "Gemini API Key (optional)",
        type="password",
        placeholder="AIza...",
        help="Get free key at aistudio.google.com",
    )
    if gemini_key:
        os.environ["GOOGLE_API_KEY"] = gemini_key
        st.success("✓ Gemini key set")

    groq_key = st.text_input(
        "Groq API Key (optional)",
        type="password",
        placeholder="gsk_...",
        help="Get free key at console.groq.com",
    )
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key

    st.markdown('<div class="section-header" style="margin-top:20px;">Pipeline</div>', unsafe_allow_html=True)
    pipeline_steps = [
        ("🔍", "Prompt Analyzer"),
        ("🏷️", "Type Detector"),
        ("✍️", "Rewriter Agent"),
        ("🔬", "Critic Agent"),
        ("📊", "Quality Scorer"),
        ("🚀", "LLM Generator"),
        ("📈", "Response Compare"),
    ]
    for icon, step in pipeline_steps:
        st.markdown(f"""
        <div class="pipeline-step">
            <div class="step-icon">{icon}</div>
            <span style="font-size: 0.8rem; color: #94a3b8;">{step}</span>
        </div>
        """, unsafe_allow_html=True)

    # Memory Stats
    stats = get_stats()
    if stats["total"] > 0:
        st.markdown('<div class="section-header" style="margin-top:20px;">Memory Stats</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        col1.metric("Total", stats["total"])
        col2.metric("Avg +", f"+{stats['avg_improvement']}")

        if st.button("🗑️ Clear Memory", width='stretch'):
            clear_memory()
            st.success("Memory cleared!")


# ─── Main Content ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">⚡ AI Prompt Optimizer</h1>
    <p class="hero-subtitle">Transform weak prompts into precision-engineered instructions using multi-agent AI</p>
    <div class="hero-badges">
        <span class="badge">🤖 Multi-Agent</span>
        <span class="badge">🔄 Self-Refine</span>
        <span class="badge">📊 Quality Scoring</span>
        <span class="badge">🧠 Prompt Memory</span>
        <span class="badge">📈 Analytics</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3 = st.tabs(["⚡ Optimize", "📊 Analytics", "🗄️ History"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: OPTIMIZE
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
    col_input, col_meta = st.columns([2, 1])

    with col_input:
        st.markdown('<div class="section-header">Your Prompt</div>', unsafe_allow_html=True)
        user_prompt = st.text_area(
            label="Enter your prompt",
            placeholder="Enter your prompt here...\n\nExample: 'Explain AI'\nor 'Write Python code for sorting'\nor 'Summarize this article'",
            height=160,
            key="user_prompt",
            label_visibility="collapsed",
        )

    with col_meta:
        st.markdown('<div class="section-header">Quick Examples</div>', unsafe_allow_html=True)
        examples = {
            "💻 Coding": "Write Python code for binary search",
            "✍️ Writing": "Write a blog about AI",
            "🔬 Research": "Explain machine learning",
            "📝 Summary": "Summarize climate change",
        }
        for label, example in examples.items():
            if st.button(label, key=f"ex_{label}", width='stretch'):
                st.session_state["user_prompt"] = example
                st.rerun()

    # Optimize Button
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
    with col_btn1:
        optimize_clicked = st.button("⚡ Optimize Prompt", width='stretch', type="primary")

    # Check API key
    has_api_key = bool(os.getenv("OPENAI_API_KEY"))

    if optimize_clicked:
        if not user_prompt.strip():
            st.warning("⚠️ Please enter a prompt first.")
        elif not has_api_key:
            st.error("🔑 Please enter your OpenAI API Key in the sidebar.")
        else:
            # ── Progress UI ──
            progress_container = st.container()
            with progress_container:
                prog_bar = st.progress(0)
                status_text = st.empty()

                steps = [
                    (10, "🔍 Analyzing prompt quality..."),
                    (25, "🏷️ Detecting prompt type..."),
                    (40, "✍️ Rewriting with AI agent..."),
                    (60, "🔬 Running critic review..."),
                    (75, "📊 Scoring both prompts..."),
                    (88, "🚀 Generating LLM responses..."),
                    (95, "💾 Saving to memory..."),
                ]

                for pct, msg in steps:
                    prog_bar.progress(pct)
                    status_text.markdown(f"<p style='color:#64748b; font-size:0.85rem;'>{msg}</p>", unsafe_allow_html=True)
                    time.sleep(0.1)

                try:
                    result = run_optimization_pipeline(
                        user_prompt=user_prompt,
                        model_name=selected_model,
                        temperature=temperature,
                        use_self_refine=use_self_refine,
                        save_to_memory=save_to_memory,
                    )

                    prog_bar.progress(100)
                    status_text.markdown("<p style='color:#34d399; font-size:0.85rem;'>✅ Optimization complete!</p>", unsafe_allow_html=True)
                    st.session_state["result"] = result
                    time.sleep(0.5)
                    progress_container.empty()

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    progress_container.empty()

    # ── Display Results ──────────────────────────────────────────────────────
    if "result" in st.session_state:
        result = st.session_state["result"]

        # Improvement Banner
        imp_pct = result.improvement_pct
        imp_sign = "+" if imp_pct >= 0 else ""
        st.markdown(f"""
        <div class="improvement-banner">
            <div class="improvement-number">{imp_sign}{imp_pct}%</div>
            <div class="improvement-label">Prompt Quality Improvement</div>
            <div style="color:#475569; font-size:0.8rem; margin-top:8px;">
                {result.original_score.total}/10 → {result.optimized_score.total}/10
                &nbsp;|&nbsp; {result.type_icon} {result.prompt_type}
                &nbsp;|&nbsp; Model: {selected_model}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Row 1: Analysis + Prompts ──
        col_analysis, col_prompts = st.columns([1, 2])

        with col_analysis:
            st.markdown('<div class="section-header">Analysis</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card">
                <div class="card-title">Detected Type</div>
                <span class="type-tag">{result.type_icon} {result.prompt_type}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""<div class="card">
                <div class="card-title">Problems Found</div>""", unsafe_allow_html=True)
            problems_html = " ".join([f'<span class="problem-tag">✗ {p}</span>' for p in result.analysis.problems])
            st.markdown(problems_html + "</div>", unsafe_allow_html=True)

            st.markdown("""<div class="card">
                <div class="card-title">Missing Elements</div>""", unsafe_allow_html=True)
            missing_html = " ".join([f'<span class="problem-tag">⚠ {m}</span>' for m in result.analysis.missing_elements])
            st.markdown(missing_html + "</div>", unsafe_allow_html=True)

            st.markdown("""<div class="card">
                <div class="card-title">Improvements Applied</div>""", unsafe_allow_html=True)
            suggest_html = " ".join([f'<span class="suggestion-tag">✓ {s}</span>' for s in result.analysis.suggestions])
            st.markdown(suggest_html + "</div>", unsafe_allow_html=True)

        with col_prompts:
            st.markdown('<div class="section-header">Prompt Comparison</div>', unsafe_allow_html=True)

            st.markdown("""
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="background:rgba(248,113,113,0.15); border:1px solid rgba(248,113,113,0.3); 
                color:#fca5a5; padding:3px 10px; border-radius:6px; font-size:0.72rem; font-weight:600;">
                ORIGINAL</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="prompt-box prompt-box-original">{result.original_prompt}</div>', unsafe_allow_html=True)

            st.markdown("""
            <div style="display:flex; align-items:center; gap:8px; margin:12px 0 8px;">
                <span style="background:rgba(52,211,153,0.15); border:1px solid rgba(52,211,153,0.3); 
                color:#6ee7b7; padding:3px 10px; border-radius:6px; font-size:0.72rem; font-weight:600;">
                OPTIMIZED</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="prompt-box prompt-box-optimized">{result.optimized_prompt}</div>', unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

        # ── Row 2: Scores ──
        st.markdown('<div class="section-header">Quality Scores</div>', unsafe_allow_html=True)

        col_orig_score, col_opt_score = st.columns(2)

        with col_orig_score:
            st.markdown("<p style='color:#f87171;font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;text-align:center;'>Original Prompt</p>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            for col, label, val in [
                (c1, "Clarity", result.original_score.clarity),
                (c2, "Specificity", result.original_score.specificity),
                (c3, "Context", result.original_score.context),
                (c4, "Structure", result.original_score.structure),
            ]:
                color = "#34d399" if val >= 7.5 else "#fbbf24" if val >= 5 else "#f87171"
                html = f'<div style="text-align:center;background:#13131f;border:1px solid #1e293b;border-radius:8px;padding:10px 4px;"><div style="font-size:0.6rem;color:#475569;text-transform:uppercase;">{label}</div><div style="font-size:1.5rem;font-weight:700;color:{color};">{val}</div></div>'
                col.markdown(html, unsafe_allow_html=True)
            total_html = f'<div style="text-align:center;margin-top:12px;padding:12px;background:#13131f;border-radius:8px;border:1px solid #1e293b;"><div style="color:#64748b;font-size:0.7rem;text-transform:uppercase;">Total Score</div><div style="font-size:2.2rem;font-weight:700;color:#f87171;">{result.original_score.total}/10</div><div style="color:#64748b;font-size:0.75rem;">{result.original_score.quality_label}</div></div>'
            st.markdown(total_html, unsafe_allow_html=True)

        with col_opt_score:
            st.markdown("<p style='color:#34d399;font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;text-align:center;'>Optimized Prompt</p>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            for col, label, val in [
                (c1, "Clarity", result.optimized_score.clarity),
                (c2, "Specificity", result.optimized_score.specificity),
                (c3, "Context", result.optimized_score.context),
                (c4, "Structure", result.optimized_score.structure),
            ]:
                color = "#34d399" if val >= 7.5 else "#fbbf24" if val >= 5 else "#f87171"
                html = f'<div style="text-align:center;background:#13131f;border:1px solid #1e293b;border-radius:8px;padding:10px 4px;"><div style="font-size:0.6rem;color:#475569;text-transform:uppercase;">{label}</div><div style="font-size:1.5rem;font-weight:700;color:{color};">{val}</div></div>'
                col.markdown(html, unsafe_allow_html=True)
            total_html = f'<div style="text-align:center;margin-top:12px;padding:12px;background:#13131f;border-radius:8px;border:1px solid rgba(52,211,153,0.2);"><div style="color:#64748b;font-size:0.7rem;text-transform:uppercase;">Total Score</div><div style="font-size:2.2rem;font-weight:700;color:#34d399;">{result.optimized_score.total}/10</div><div style="color:#64748b;font-size:0.75rem;">{result.optimized_score.quality_label}</div></div>'
            st.markdown(total_html, unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

        # ── Row 3: Charts ──
        st.markdown('<div class="section-header">Visual Analysis</div>', unsafe_allow_html=True)
        col_radar, col_bar = st.columns(2)

        with col_radar:
            st.markdown("<p style='color:#475569; font-size:0.75rem; text-align:center; text-transform:uppercase; letter-spacing:0.1em;'>Radar Chart</p>", unsafe_allow_html=True)
            st.plotly_chart(
                make_radar_chart(result.original_score, result.optimized_score),
                width='stretch',
            )

        with col_bar:
            st.markdown("<p style='color:#475569; font-size:0.75rem; text-align:center; text-transform:uppercase; letter-spacing:0.1em;'>Score Breakdown</p>", unsafe_allow_html=True)
            st.plotly_chart(
                make_bar_comparison(result.original_score, result.optimized_score),
                width='stretch',
            )

        st.markdown("<hr/>", unsafe_allow_html=True)

        # ── Row 4: Critic Feedback ──
        st.markdown('<div class="section-header">Critic Agent Feedback</div>', unsafe_allow_html=True)
        critique = result.critique

        approval_color = "#34d399" if critique.approved else "#f87171"
        approval_text = "✓ APPROVED" if critique.approved else "✗ NEEDS REVISION"
        st.markdown(f"""
        <div style="background:rgba(52,211,153,0.05); border:1px solid {approval_color}33; border-radius:10px; 
        padding:12px 20px; margin-bottom:16px; display:flex; align-items:center; gap:12px;">
            <span style="color:{approval_color}; font-weight:700; font-size:0.85rem;">{approval_text}</span>
            <span style="color:#64748b; font-size:0.8rem;">— {critique.overall_assessment}</span>
        </div>
        """, unsafe_allow_html=True)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            for label, text in [
                ("Clarity", critique.clarity_feedback),
                ("Specificity", critique.specificity_feedback),
                ("Context", critique.context_feedback),
            ]:
                st.markdown(f"""
                <div class="feedback-tile">
                    <div class="feedback-tile-label">{label}</div>
                    <div class="feedback-tile-text">{text}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_c2:
            for label, text in [
                ("Structure", critique.structure_feedback),
                ("Output Format", critique.output_format_feedback),
                ("Top Suggestion", critique.top_suggestion),
            ]:
                st.markdown(f"""
                <div class="feedback-tile">
                    <div class="feedback-tile-label">{label}</div>
                    <div class="feedback-tile-text">{text}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

        # ── Row 5: LLM Responses ──
        st.markdown('<div class="section-header">LLM Response Comparison</div>', unsafe_allow_html=True)

        col_orig_resp, col_opt_resp = st.columns(2)

        with col_orig_resp:
            st.markdown("""
            <span style="background:rgba(248,113,113,0.15); border:1px solid rgba(248,113,113,0.3); 
            color:#fca5a5; padding:3px 10px; border-radius:6px; font-size:0.72rem; font-weight:600;">
            ORIGINAL PROMPT RESPONSE</span>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="response-box" style="margin-top:12px;">{result.original_response}</div>', unsafe_allow_html=True)
            tok = result.original_tokens
            st.markdown(f"<p style='color:#334155; font-size:0.72rem; margin-top:6px;'>~{tok} tokens</p>", unsafe_allow_html=True)

        with col_opt_resp:
            st.markdown("""
            <span style="background:rgba(52,211,153,0.15); border:1px solid rgba(52,211,153,0.3); 
            color:#6ee7b7; padding:3px 10px; border-radius:6px; font-size:0.72rem; font-weight:600;">
            OPTIMIZED PROMPT RESPONSE</span>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="response-box" style="margin-top:12px;">{result.optimized_response}</div>', unsafe_allow_html=True)
            tok = result.optimized_tokens
            st.markdown(f"<p style='color:#334155; font-size:0.72rem; margin-top:6px;'>~{tok} tokens</p>", unsafe_allow_html=True)

        # ── Refinement History ──
        if use_self_refine and len(result.refinement_history) > 2:
            with st.expander("🔄 View Self-Refinement History"):
                for i, version in enumerate(result.refinement_history):
                    label = "Original" if i == 0 else f"Iteration {i}"
                    color = "#f87171" if i == 0 else "#6366f1" if i < len(result.refinement_history) - 1 else "#34d399"
                    st.markdown(f"""
                    <div style="margin-bottom:12px;">
                        <span style="color:{color}; font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.1em;">
                        {label}</span>
                        <div class="prompt-box" style="margin-top:6px;">{version}</div>
                    </div>
                    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════

with tab2:
    all_prompts = get_all_prompts()
    stats = get_stats()

    st.markdown('<div class="section-header">Overall Statistics</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Optimized", stats.get("total", 0))
    c2.metric("Avg Improvement", f"+{stats.get('avg_improvement', 0)}")
    c3.metric("Best Score", f"{stats.get('best_score', 0)}/10")
    c4.metric("Avg Score", f"{stats.get('avg_score', 0)}/10")

    if all_prompts:
        st.markdown('<div class="section-header" style="margin-top:24px;">Score Trends</div>', unsafe_allow_html=True)

        ids = [p["id"] for p in all_prompts]
        orig = [p["original_score"] for p in all_prompts]
        opt = [p["optimized_score"] for p in all_prompts]

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=ids, y=orig, mode="lines+markers",
            name="Original", line_color="#f87171", marker_size=6,
        ))
        fig_trend.add_trace(go.Scatter(
            x=ids, y=opt, mode="lines+markers",
            name="Optimized", line_color="#34d399", marker_size=6,
        ))
        fig_trend.update_layout(
            paper_bgcolor="#0a0a0f", plot_bgcolor="#0a0a0f",
            font_color="#94a3b8",
            yaxis=dict(range=[0, 10], gridcolor="#1e293b"),
            xaxis=dict(title="Optimization #", gridcolor="#1e293b"),
            legend=dict(bgcolor="rgba(15,15,26,0.8)", bordercolor="#1e293b", borderwidth=1),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_trend, width='stretch')

        st.markdown('<div class="section-header">Prompt Type Distribution</div>', unsafe_allow_html=True)
        type_counts = {}
        for p in all_prompts:
            t = p.get("prompt_type", "General")
            type_counts[t] = type_counts.get(t, 0) + 1

        fig_pie = go.Figure(go.Pie(
            labels=list(type_counts.keys()),
            values=list(type_counts.values()),
            hole=0.5,
            marker_colors=["#6366f1", "#8b5cf6", "#38bdf8", "#34d399", "#fbbf24", "#f87171", "#c084fc"],
        ))
        fig_pie.update_layout(
            paper_bgcolor="#0a0a0f",
            font_color="#94a3b8",
            legend=dict(bgcolor="rgba(15,15,26,0.8)", bordercolor="#1e293b", borderwidth=1),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_pie, width='stretch')
    else:
        st.info("📊 Run some optimizations to see analytics here.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: HISTORY
# ══════════════════════════════════════════════════════════════════════════════

with tab3:
    all_prompts = get_all_prompts()
    st.markdown('<div class="section-header">Optimization History</div>', unsafe_allow_html=True)

    if not all_prompts:
        st.info("📝 No prompts saved yet. Run optimizations to build your history.")
    else:
        for p in reversed(all_prompts[-20:]):
            imp_color = "#34d399" if p.get("improvement", 0) >= 0 else "#f87171"
            with st.expander(
                f"#{p['id']} — {p.get('prompt_type', 'General')} — Score: {p['original_score']} → {p['optimized_score']} — {p['timestamp'][:10]}"
            ):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Original Prompt**")
                    st.markdown(f'<div class="prompt-box prompt-box-original">{p["original_prompt"]}</div>', unsafe_allow_html=True)
                with col_b:
                    st.markdown("**Optimized Prompt**")
                    st.markdown(f'<div class="prompt-box prompt-box-optimized">{p["optimized_prompt"]}</div>', unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-top:10px; display:flex; gap:12px; flex-wrap:wrap;">
                    <span style="color:#64748b; font-size:0.75rem;">Type: <b style="color:#a5b4fc;">{p.get('prompt_type','?')}</b></span>
                    <span style="color:#64748b; font-size:0.75rem;">Original: <b style="color:#f87171;">{p['original_score']}/10</b></span>
                    <span style="color:#64748b; font-size:0.75rem;">Optimized: <b style="color:#34d399;">{p['optimized_score']}/10</b></span>
                    <span style="color:#64748b; font-size:0.75rem;">Improvement: <b style="color:{imp_color};">+{p.get('improvement',0)}</b></span>
                </div>
                """, unsafe_allow_html=True)
