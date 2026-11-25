import os
import streamlit as st
from summarizer import summarize, DEFAULT_MODEL

# 1. Page Configuration
st.set_page_config(
    page_title="MeetLens | Executive Meeting Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Precision-Aligned Editorial CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

/* Base App Styling */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0F172A;
}

.stApp {
    background: linear-gradient(180deg, #EEF2F9 0%, #F8FAFC 40%, #F3F5FA 100%);
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
}

.block-container {
    padding-top: 1.4rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1360px;
}

/* Hero Navigation Bar */
.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.6rem;
    background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 60%, #1E293B 100%);
    border-radius: 14px;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.16);
}

.brand-wrap {
    display: flex;
    align-items: center;
    gap: 0.9rem;
}

.brand-mark {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: linear-gradient(135deg, #6366F1 0%, #EC4899 100%);
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 1.15rem;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.brand-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 1.22rem;
    color: #FFFFFF;
    margin: 0;
    line-height: 1.2;
}

.brand-sub {
    font-size: 0.8rem;
    color: #CBD5E1;
    margin: 0;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.42rem 0.95rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    background: rgba(16, 185, 129, 0.14);
    color: #6EE7B7;
    border: 1px solid rgba(16, 185, 129, 0.35);
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 8px #10B981;
}

/* Style Streamlit Native Bordered Containers as Clean Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 1.25rem 1.35rem !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}

/* Card Header Bar */
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 0.65rem;
    margin-bottom: 0.85rem;
    border-bottom: 1px solid #F1F5F9;
}

.card-title-wrap {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.92rem;
    font-weight: 700;
    color: #0F172A;
}

.dot-indigo { width: 8px; height: 8px; border-radius: 50%; background: #4F46E5; }
.dot-teal   { width: 8px; height: 8px; border-radius: 50%; background: #0D9488; }
.dot-sky    { width: 8px; height: 8px; border-radius: 50%; background: #0284C7; }
.dot-rose   { width: 8px; height: 8px; border-radius: 50%; background: #E11D48; }

.card-meta {
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748B;
}

/* Vertical Alignment inside Horizontal Columns */
div[data-testid="stHorizontalBlock"] {
    align-items: stretch;
}

/* Executive Summary Card */
.exec-card {
    background: linear-gradient(135deg, #EEF2FF 0%, #FFFFFF 60%, #F5F3FF 100%);
    border: 1px solid #C7D2FE;
    border-left: 5px solid #4F46E5;
    border-radius: 14px;
    padding: 1.35rem 1.55rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.05);
}

.exec-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.65rem;
}

.exec-badge {
    background: #4F46E5;
    color: #FFFFFF;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
}

.exec-mode-tag {
    font-size: 0.76rem;
    font-weight: 600;
    color: #4338CA;
}

.exec-text {
    font-size: 1.01rem;
    line-height: 1.7;
    color: #1E293B;
    margin: 0;
}

/* Color-Coded Metric Tiles */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.85rem;
    margin-bottom: 1rem;
}

.metric-tile {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.95rem 1.15rem;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.02);
}

.tile-indigo { border-top: 3px solid #4F46E5; background: linear-gradient(180deg, #F5F7FF 0%, #FFFFFF 45%); }
.tile-teal   { border-top: 3px solid #0D9488; background: linear-gradient(180deg, #F0FDFA 0%, #FFFFFF 45%); }
.tile-amber  { border-top: 3px solid #D97706; background: linear-gradient(180deg, #FFFBEB 0%, #FFFFFF 45%); }

.metric-label {
    font-size: 0.72rem;
    color: #64748B;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}

.metric-val-indigo { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.42rem; font-weight: 800; color: #3730A3; }
.metric-val-teal   { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.42rem; font-weight: 800; color: #0F766E; }
.metric-val-amber  { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.42rem; font-weight: 800; color: #B45309; }

.metric-unit {
    font-size: 0.78rem;
    font-weight: 500;
    color: #64748B;
}

/* Key Takeaways List */
.kp-item {
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
    font-size: 0.88rem;
    line-height: 1.55;
    color: #334155;
    padding: 0.5rem 0;
    border-bottom: 1px dashed #E2E8F0;
}
.kp-item:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.kp-num {
    min-width: 22px;
    height: 22px;
    border-radius: 6px;
    background: #E0F2FE;
    color: #0369A1;
    font-size: 0.72rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-top: 2px;
}

/* Multi-Color Keyword Pills */
.tag-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
}

.kw-0 { background: #EEF2FF; color: #4338CA; border: 1px solid #C7D2FE; }
.kw-1 { background: #F0FDFA; color: #0F766E; border: 1px solid #99F6E4; }
.kw-2 { background: #FFF1F2; color: #BE123C; border: 1px solid #FECDD3; }
.kw-3 { background: #FFFBEB; color: #B45309; border: 1px solid #FDE68A; }

.kw-tag {
    padding: 0.3rem 0.7rem;
    border-radius: 7px;
    font-size: 0.77rem;
    font-weight: 600;
}

/* Checkbox Polish inside Action Items */
div[data-testid="stCheckbox"] {
    padding: 0.3rem 0.4rem;
    border-radius: 8px;
    transition: background 0.15s ease;
}
div[data-testid="stCheckbox"]:hover {
    background: #FFF1F2;
}
div[data-testid="stCheckbox"] label p {
    font-size: 0.88rem !important;
    line-height: 1.48 !important;
    color: #1E293B !important;
}

/* Empty State Placeholder */
.empty-state {
    background: #FFFFFF;
    border: 1.5px dashed #C7D2FE;
    border-radius: 16px;
    padding: 6.2rem 2rem;
    text-align: center;
    color: #64748B;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.02);
}

.empty-badge {
    display: inline-block;
    background: #EEF2FF;
    color: #4F46E5;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.32rem 0.85rem;
    border-radius: 999px;
    margin-bottom: 0.85rem;
}

.empty-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.18rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.45rem;
}

/* Buttons & Inputs */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #6D28D9 100%);
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 0.68rem 1.25rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.28);
    transition: all 0.2s ease;
}

div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4338CA 0%, #5B21B6 100%);
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.38);
    transform: translateY(-1px);
}

div.stButton > button[kind="secondary"], div.stDownloadButton > button {
    background-color: #F8FAFC;
    color: #334155;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.84rem;
}

div.stButton > button[kind="secondary"]:hover, div.stDownloadButton > button:hover {
    background-color: #EEF2FF;
    border-color: #6366F1;
    color: #4338CA;
}

textarea {
    border-radius: 10px !important;
    border: 1px solid #CBD5E1 !important;
    background-color: #F8FAFC !important;
    font-size: 0.89rem !important;
    line-height: 1.55 !important;
}

textarea:focus {
    background-color: #FFFFFF !important;
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.14) !important;
}
</style>
""", unsafe_allow_html=True)

# 3. Active Model Badge
is_finetuned = os.path.basename(DEFAULT_MODEL) == "meetlens_model"
model_badge = "Fine-Tuned BART (Local)" if is_finetuned else "DistilBART-CNN (Pretrained)"

# 4. Top Navigation Header
st.markdown(f"""
<div class="top-nav">
    <div class="brand-wrap">
        <div class="brand-mark">M</div>
        <div>
            <p class="brand-title">MeetLens</p>
            <p class="brand-sub">Executive Meeting &amp; Lecture Intelligence &bull; Team Techmorph</p>
        </div>
    </div>
    <div class="status-pill">
        <span class="status-dot"></span>
        <span>{model_badge}</span>
    </div>
</div>
""", unsafe_allow_html=True)

if "transcript_input" not in st.session_state:
    st.session_state.transcript_input = ""

# 5. Balanced Two-Column Studio Layout
col_left, col_right = st.columns([5, 7], gap="large")

with col_left:
    # Card 1: Source Transcript
    with st.container(border=True):
        st.markdown("""
        <div class="card-header">
            <span class="card-title-wrap"><span class="dot-indigo"></span>Source Transcript</span>
            <span class="card-meta">Input</span>
        </div>
        """, unsafe_allow_html=True)

        util_c1, util_c2 = st.columns([3, 2], vertical_alignment="center")
        with util_c1:
            input_mode = st.radio(
                "Input source",
                ["Paste text", "Upload file"],
                horizontal=True,
                label_visibility="collapsed",
            )
        with util_c2:
            sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_transcript.txt")
            if os.path.exists(sample_path):
                if st.button("Load sample", use_container_width=True):
                    with open(sample_path, "r", encoding="utf-8") as sf:
                        st.session_state.transcript_input = sf.read()

        if input_mode == "Paste text":
            text = st.text_area(
                "Transcript content",
                key="transcript_input",
                height=265,
                placeholder="Paste meeting notes, Zoom/Teams transcript, or lecture text here...",
                label_visibility="collapsed",
            )
        else:
            uploaded = st.file_uploader(
                "Upload .txt or .pdf",
                type=["txt", "pdf"],
                label_visibility="collapsed",
            )
            text = ""
            if uploaded is not None:
                if uploaded.name.endswith(".pdf"):
                    from pypdf import PdfReader
                    text = "\n".join((p.extract_text() or "") for p in PdfReader(uploaded).pages)
                else:
                    text = uploaded.read().decode("utf-8", errors="ignore")
                st.caption(f"Loaded **{uploaded.name}** ({len(text.split())} words)")

    # Card 2: Synthesis Settings
    with st.container(border=True):
        st.markdown("""
        <div class="card-header">
            <span class="card-title-wrap"><span class="dot-teal"></span>Synthesis Settings</span>
            <span class="card-meta">Parameters</span>
        </div>
        """, unsafe_allow_html=True)

        METHOD_MAP = {
            "Hybrid (Recommended)": "hybrid",
            "Abstractive (Neural)": "abstractive",
            "Extractive (Fast)": "extractive",
        }
        selected_label = st.selectbox(
            "Summarisation mode",
            list(METHOD_MAP.keys()),
            help="Hybrid compresses key sentences with TextRank before rewriting with your fine-tuned BART model.",
        )
        method = METHOD_MAP[selected_label]

        n = st.slider(
            "Detail level (target sentences)",
            min_value=3,
            max_value=15,
            value=5,
        )

        run_clicked = st.button("Generate Executive Brief", type="primary", use_container_width=True)

with col_right:
    if run_clicked:
        if len(text.split()) < 50:
            st.warning("Please provide at least 50 words so the model has enough context to summarise.")
        else:
            with st.spinner("Analysing transcript and generating summary..."):
                st.session_state.last_result = summarize(text, method, n)
                st.session_state.last_method = selected_label

    if "last_result" in st.session_state:
        r = st.session_state.last_result
        compression = max(0, 100 - (100 * r["summ_words"] / max(r["orig_words"], 1)))

        # Executive Summary Hero Box
        st.markdown(f"""
        <div class="exec-card">
            <div class="exec-top">
                <span class="exec-badge">Executive Summary</span>
                <span class="exec-mode-tag">{st.session_state.get("last_method", "")}</span>
            </div>
            <p class="exec-text">{r["summary"]}</p>
        </div>
        """, unsafe_allow_html=True)

        # Color-Coded Metrics Row
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-tile tile-indigo">
                <div class="metric-label">Source Length</div>
                <div class="metric-val-indigo">{r["orig_words"]:,} <span class="metric-unit">words</span></div>
            </div>
            <div class="metric-tile tile-teal">
                <div class="metric-label">Brief Length</div>
                <div class="metric-val-teal">{r["summ_words"]:,} <span class="metric-unit">words</span></div>
            </div>
            <div class="metric-tile tile-amber">
                <div class="metric-label">Compression</div>
                <div class="metric-val-amber">{compression:.0f}% <span class="metric-unit">saved</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Equal-Height Bottom Insight Columns
        sub_left, sub_right = st.columns(2, gap="medium")

        with sub_left:
            with st.container(border=True):
                st.markdown(f"""
                <div class="card-header">
                    <span class="card-title-wrap"><span class="dot-sky"></span>Key Takeaways</span>
                    <span class="card-meta" style="color:#0284C7;">Top {len(r["key_points"])}</span>
                </div>
                """, unsafe_allow_html=True)

                if r["key_points"]:
                    kp_html = "".join(
                        f'<div class="kp-item"><span class="kp-num">{idx}</span><span>{k}</span></div>'
                        for idx, k in enumerate(r["key_points"], 1)
                    )
                    st.markdown(kp_html, unsafe_allow_html=True)
                else:
                    st.caption("No key points extracted.")

            with st.container(border=True):
                st.markdown("""
                <div class="card-header">
                    <span class="card-title-wrap"><span class="dot-indigo"></span>Core Topics</span>
                    <span class="card-meta">TF-IDF</span>
                </div>
                """, unsafe_allow_html=True)

                if r["keywords"]:
                    tags_html = "".join(
                        f'<span class="kw-tag kw-{idx % 4}">{kw}</span>'
                        for idx, kw in enumerate(r["keywords"])
                    )
                    st.markdown(f'<div class="tag-wrap">{tags_html}</div>', unsafe_allow_html=True)
                else:
                    st.caption("No topics extracted.")

        with sub_right:
            with st.container(border=True):
                st.markdown(f"""
                <div class="card-header">
                    <span class="card-title-wrap"><span class="dot-rose"></span>Action Items &amp; Deadlines</span>
                    <span class="card-meta" style="color:#E11D48;">{len(r["action_items"])} detected</span>
                </div>
                """, unsafe_allow_html=True)

                if r["action_items"]:
                    for idx, item in enumerate(r["action_items"]):
                        st.checkbox(item, key=f"act_{idx}")
                else:
                    st.caption("No explicit action items or deadlines detected in this transcript.")

                st.markdown("<div style='height:0.65rem;'></div>", unsafe_allow_html=True)

                export_txt = (
                    f"MEETLENS EXECUTIVE SUMMARY\n"
                    f"{'=' * 30}\n\n"
                    f"{r['summary']}\n\n"
                    f"KEY TAKEAWAYS\n"
                    + "\n".join(f"- {k}" for k in r["key_points"])
                    + "\n\nACTION ITEMS\n"
                    + ("\n".join(f"[ ] {a}" for a in r["action_items"]) if r["action_items"] else "None")
                )
                st.download_button(
                    "Export Brief (.txt)",
                    export_txt,
                    file_name="MeetLens_Brief.txt",
                    use_container_width=True,
                )
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-badge">NLP Summarisation Studio</div>
            <div class="empty-title">Ready to distil your transcript</div>
            <p style="font-size:0.9rem; max-width:390px; margin:0 auto;">
                Paste a meeting dialogue or click <strong>Load sample</strong> on the left, choose your synthesis mode, and generate an executive brief.
            </p>
        </div>
        """, unsafe_allow_html=True)