import streamlit as st
import fitz  # PyMuPDF
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from utils.llm import call_llm, classify_task
from utils.prompts import (
    SUMMARIZATION_PROMPT,
    EXPLANATION_PROMPT,
    COMPARISON_PROMPT,
    EVALUATION_PROMPT,
    build_prompt_modifiers,
)
from utils.parser import parse_response, preprocess_input, validate_input
from utils.pdf_export import generate_pdf

st.set_page_config(
    page_title="AI Policy Analysis Assistant",
    page_icon="📜",
    layout="wide",
)

st.title("📜 AI Policy Analysis & Comparison Assistant")
st.caption("Analyze, simplify, compare, and critically evaluate public policy documents using AI.")

TASK_LABELS = {
    "summarize": "📋 Policy Summarization",
    "explain": "🔍 Plain-Language Explanation",
    "compare": "⚖️ Comparative Analysis",
    "evaluate": "🔬 Critical Evaluation",
}

TASK_DESCRIPTIONS = {
    "summarize": "Extract key objectives, implementation mechanisms, and stakeholder responsibilities from a policy.",
    "explain": "Translate technical or bureaucratic terminology into plain, accessible language.",
    "compare": "Conduct a structured side-by-side comparison of two policies across key dimensions.",
    "evaluate": "Identify a policy's strengths, weaknesses, risks, and real-world consequences.",
}

# Session state init
for key in ["result_1", "result_2", "result_3", "result_4",
            "input_1", "input_2", "input_3a", "input_3b", "input_4"]:
    if key not in st.session_state:
        st.session_state[key] = ""

if "history" not in st.session_state:
    st.session_state["history"] = []

if "history_view" not in st.session_state:
    st.session_state["history_view"] = None


def extract_pdf_text(uploaded_file) -> str:
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def settings_badge(opts: dict) -> str:
    parts = []
    if opts.get("key_insights"):
        parts.append("Top 5 Insights")
    elif opts.get("mode", "Detailed") != "Detailed":
        parts.append(opts["mode"] + " Mode")
    if opts.get("compression", "Full") != "Full":
        parts.append(opts["compression"] + " Length")
    if opts.get("rank_by_importance"):
        parts.append("Ranked")
    return " · ".join(parts) if parts else "Detailed · Full"


def save_to_history(task: str, input_text: str, result: str, opts: dict):
    entry = {
        "id": len(st.session_state["history"]),
        "task": task,
        "label": TASK_LABELS[task],
        "input_preview": input_text[:80].strip().replace("\n", " "),
        "result": result,
        "settings": settings_badge(opts),
        "timestamp": datetime.now().strftime("%b %d, %H:%M"),
    }
    st.session_state["history"].insert(0, entry)


def run_analysis(task: str, policy_input: str, policy_2: str = "", options: dict = None) -> str:
    opts = options or {}
    modifiers = build_prompt_modifiers(
        mode=opts.get("mode", "Detailed"),
        key_insights=opts.get("key_insights", False),
        compression=opts.get("compression", "Full"),
        rank_by_importance=opts.get("rank_by_importance", False),
    )

    if task == "summarize":
        prompt = SUMMARIZATION_PROMPT.format(policy_input=policy_input) + modifiers
    elif task == "explain":
        prompt = EXPLANATION_PROMPT.format(policy_input=policy_input) + modifiers
    elif task == "compare":
        prompt = COMPARISON_PROMPT.format(policy_1=policy_input, policy_2=policy_2) + modifiers
    elif task == "evaluate":
        prompt = EVALUATION_PROMPT.format(policy_input=policy_input) + modifiers
    else:
        prompt = SUMMARIZATION_PROMPT.format(policy_input=policy_input) + modifiers
    return call_llm(prompt)


def show_download_button(result_text: str, task_key: str, policy_input: str, key_suffix: str):
    task_label = TASK_LABELS[task_key].replace("📋 ", "").replace("🔍 ", "").replace("⚖️ ", "").replace("🔬 ", "")
    short_input = policy_input[:60].strip().replace("\n", " ")
    title = short_input if short_input else task_label
    filename = f"policy_analysis_{task_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    try:
        pdf_bytes = generate_pdf(
            title=title,
            task_label=task_label,
            content=result_text,
            policy_input=policy_input,
        )
        st.download_button(
            label="⬇️ Download as PDF",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            key=f"dl_{key_suffix}",
        )
    except Exception as e:
        st.warning(f"PDF export unavailable: {str(e)}")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Output Settings")
    st.caption("These settings apply to every analysis you run.")

    summary_mode = st.radio(
        "Summary Mode",
        options=["Short", "Medium", "Detailed"],
        index=2,
        horizontal=True,
        help="Short: 5–7 bullet points only · Medium: 4 sections max · Detailed: full structured output",
    )

    st.write("")
    key_insights_only = st.toggle(
        "Key Insights Only (Top 5)",
        value=False,
        help="Extract only the 5 most important policy goals, ranked by national impact. Overrides Summary Mode.",
    )

    compression = st.select_slider(
        "Output Length",
        options=["30%", "50%", "80%", "Full"],
        value="Full",
        help="Compress the AI output to a fraction of its full length.",
    )

    rank_by_importance = st.toggle(
        "Rank by Importance",
        value=False,
        help="Sort all points so critical national goals come first and minor details come last.",
    )

    active = []
    if key_insights_only:
        active.append("Top 5 insights")
    elif summary_mode != "Detailed":
        active.append(f"{summary_mode} mode")
    if compression != "Full":
        active.append(f"{compression} length")
    if rank_by_importance:
        active.append("ranked")
    if active:
        st.info("Active: " + " · ".join(active))

    st.divider()

    # ── History Panel ────────────────────────────────────────────────────────
    history = st.session_state["history"]
    col_h, col_c = st.columns([3, 1])
    with col_h:
        st.subheader(f"📚 History ({len(history)})")
    with col_c:
        if history:
            if st.button("Clear", key="clear_history", help="Remove all saved analyses"):
                st.session_state["history"] = []
                st.session_state["history_view"] = None
                st.rerun()

    if not history:
        st.caption("Your analyses will appear here after you run them.")
    else:
        for entry in history:
            with st.expander(f"{entry['label']}  —  {entry['timestamp']}", expanded=False):
                st.caption(f"**Input:** {entry['input_preview']}{'…' if len(entry['input_preview']) == 80 else ''}")
                st.caption(f"**Settings:** {entry['settings']}")
                if st.button("📂 Load result", key=f"load_{entry['id']}"):
                    st.session_state["history_view"] = entry
                    st.rerun()

    st.divider()
    st.subheader("How to Use")
    st.markdown("""
1. **Select a function** from the tabs above
2. **Enter a policy name** or **upload a PDF**
3. Adjust **Output Settings** above as needed
4. Click **Analyze** to get AI-powered insights
5. **Download** the result as a formatted PDF
    """)
    st.divider()
    st.subheader("Sample Policies to Try")
    st.markdown("""
- National Education Policy 2017
- Digital Pakistan Vision
- CPEC Framework Agreement
- Pakistan Economic Survey
- National Health Vision 2016-2025
    """)

# Collect output options once
output_options = {
    "mode": summary_mode,
    "key_insights": key_insights_only,
    "compression": compression,
    "rank_by_importance": rank_by_importance,
}

# ── History Viewer (shown above tabs when a result is loaded) ─────────────────
if st.session_state["history_view"]:
    view = st.session_state["history_view"]
    st.info(
        f"**Viewing from history:** {view['label']}  ·  {view['timestamp']}  ·  Settings: {view['settings']}"
    )
    col_dismiss, _ = st.columns([1, 5])
    with col_dismiss:
        if st.button("✕ Dismiss", key="dismiss_history"):
            st.session_state["history_view"] = None
            st.rerun()
    st.markdown(view["result"])
    st.divider()
    show_download_button(view["result"], view["task"], view["input_preview"], "hist")
    st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Summarization",
    "🔍 Plain-Language Explanation",
    "⚖️ Comparative Analysis",
    "🔬 Critical Evaluation",
])

# ── Tab 1: Summarization ──────────────────────────────────────────────────────
with tab1:
    st.subheader("Policy Summarization")
    st.caption(TASK_DESCRIPTIONS["summarize"])

    input_method_1 = st.radio(
        "Input method",
        ["Type policy name or paste text", "Upload PDF"],
        key="input_method_1",
        horizontal=True,
    )

    policy_text_1 = ""
    if input_method_1 == "Upload PDF":
        uploaded_file_1 = st.file_uploader("Upload a policy PDF", type=["pdf"], key="pdf_1")
        if uploaded_file_1:
            with st.spinner("Extracting text from PDF..."):
                policy_text_1 = extract_pdf_text(uploaded_file_1)
            st.success(f"PDF loaded — {len(policy_text_1)} characters extracted.")
    else:
        policy_text_1 = st.text_area(
            "Policy name or text",
            placeholder="e.g. National Education Policy 2017\n\nOr paste the full policy text here...",
            height=180,
            key="text_1",
        )

    if st.button("Generate Summary", type="primary", key="btn_1"):
        valid, err = validate_input(policy_text_1)
        if not valid:
            st.error(err)
        else:
            processed = preprocess_input(policy_text_1)
            with st.spinner("Analyzing policy… this may take a moment."):
                try:
                    raw = run_analysis("summarize", processed, options=output_options)
                    result = parse_response(raw, "summarize")
                    st.session_state["result_1"] = result["summary"]
                    st.session_state["input_1"] = processed
                    save_to_history("summarize", processed, result["summary"], output_options)
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")

    if st.session_state["result_1"]:
        st.divider()
        st.markdown(st.session_state["result_1"])
        st.divider()
        show_download_button(
            st.session_state["result_1"], "summarize",
            st.session_state["input_1"], "1"
        )

# ── Tab 2: Plain-Language Explanation ────────────────────────────────────────
with tab2:
    st.subheader("Plain-Language Explanation")
    st.caption(TASK_DESCRIPTIONS["explain"])

    input_method_2 = st.radio(
        "Input method",
        ["Type policy name or paste text", "Upload PDF"],
        key="input_method_2",
        horizontal=True,
    )

    policy_text_2 = ""
    if input_method_2 == "Upload PDF":
        uploaded_file_2 = st.file_uploader("Upload a policy PDF", type=["pdf"], key="pdf_2")
        if uploaded_file_2:
            with st.spinner("Extracting text from PDF..."):
                policy_text_2 = extract_pdf_text(uploaded_file_2)
            st.success(f"PDF loaded — {len(policy_text_2)} characters extracted.")
    else:
        policy_text_2 = st.text_area(
            "Policy name, term, or text to explain",
            placeholder="e.g. CPEC (China-Pakistan Economic Corridor)\n\nOr paste specific policy text you want simplified...",
            height=180,
            key="text_2",
        )

    if st.button("Explain in Plain Language", type="primary", key="btn_2"):
        valid, err = validate_input(policy_text_2)
        if not valid:
            st.error(err)
        else:
            processed = preprocess_input(policy_text_2)
            with st.spinner("Simplifying policy language…"):
                try:
                    raw = run_analysis("explain", processed, options=output_options)
                    result = parse_response(raw, "explain")
                    st.session_state["result_2"] = result["plain_language"]
                    st.session_state["input_2"] = processed
                    save_to_history("explain", processed, result["plain_language"], output_options)
                except Exception as e:
                    st.error(f"Explanation failed: {str(e)}")

    if st.session_state["result_2"]:
        st.divider()
        st.markdown(st.session_state["result_2"])
        st.divider()
        show_download_button(
            st.session_state["result_2"], "explain",
            st.session_state["input_2"], "2"
        )

# ── Tab 3: Comparative Analysis ───────────────────────────────────────────────
with tab3:
    st.subheader("Comparative Analysis")
    st.caption(TASK_DESCRIPTIONS["compare"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Policy 1**")
        input_method_3a = st.radio(
            "Input method",
            ["Type name or text", "Upload PDF"],
            key="input_method_3a",
            horizontal=True,
        )
        policy_text_3a = ""
        if input_method_3a == "Upload PDF":
            uploaded_file_3a = st.file_uploader("Upload Policy 1 PDF", type=["pdf"], key="pdf_3a")
            if uploaded_file_3a:
                with st.spinner("Extracting..."):
                    policy_text_3a = extract_pdf_text(uploaded_file_3a)
                st.success(f"{len(policy_text_3a)} characters extracted.")
        else:
            policy_text_3a = st.text_area(
                "Policy 1 name or text",
                placeholder="e.g. National Education Policy 2017",
                height=150,
                key="text_3a",
            )

    with col2:
        st.markdown("**Policy 2**")
        input_method_3b = st.radio(
            "Input method",
            ["Type name or text", "Upload PDF"],
            key="input_method_3b",
            horizontal=True,
        )
        policy_text_3b = ""
        if input_method_3b == "Upload PDF":
            uploaded_file_3b = st.file_uploader("Upload Policy 2 PDF", type=["pdf"], key="pdf_3b")
            if uploaded_file_3b:
                with st.spinner("Extracting..."):
                    policy_text_3b = extract_pdf_text(uploaded_file_3b)
                st.success(f"{len(policy_text_3b)} characters extracted.")
        else:
            policy_text_3b = st.text_area(
                "Policy 2 name or text",
                placeholder="e.g. National Education Policy 2009",
                height=150,
                key="text_3b",
            )

    if st.button("Compare Policies", type="primary", key="btn_3"):
        valid1, err1 = validate_input(policy_text_3a)
        valid2, err2 = validate_input(policy_text_3b)
        if not valid1:
            st.error(f"Policy 1: {err1}")
        elif not valid2:
            st.error(f"Policy 2: {err2}")
        else:
            p1 = preprocess_input(policy_text_3a)
            p2 = preprocess_input(policy_text_3b)
            with st.spinner("Comparing policies… this may take a moment."):
                try:
                    raw = run_analysis("compare", p1, p2, options=output_options)
                    result = parse_response(raw, "compare")
                    st.session_state["result_3"] = result["comparison"]
                    st.session_state["input_3a"] = p1
                    st.session_state["input_3b"] = p2
                    combined = f"{p1[:40]} vs {p2[:40]}"
                    save_to_history("compare", combined, result["comparison"], output_options)
                except Exception as e:
                    st.error(f"Comparison failed: {str(e)}")

    if st.session_state["result_3"]:
        st.divider()
        st.markdown(st.session_state["result_3"])
        st.divider()
        combined_input = f"{st.session_state['input_3a'][:40]} vs {st.session_state['input_3b'][:40]}"
        show_download_button(
            st.session_state["result_3"], "compare",
            combined_input, "3"
        )

# ── Tab 4: Critical Evaluation ────────────────────────────────────────────────
with tab4:
    st.subheader("Critical Evaluation")
    st.caption(TASK_DESCRIPTIONS["evaluate"])

    input_method_4 = st.radio(
        "Input method",
        ["Type policy name or paste text", "Upload PDF"],
        key="input_method_4",
        horizontal=True,
    )

    policy_text_4 = ""
    if input_method_4 == "Upload PDF":
        uploaded_file_4 = st.file_uploader("Upload a policy PDF", type=["pdf"], key="pdf_4")
        if uploaded_file_4:
            with st.spinner("Extracting text from PDF..."):
                policy_text_4 = extract_pdf_text(uploaded_file_4)
            st.success(f"PDF loaded — {len(policy_text_4)} characters extracted.")
    else:
        policy_text_4 = st.text_area(
            "Policy name or text to evaluate",
            placeholder="e.g. Digital Pakistan Vision\n\nOr paste the full policy text for in-depth critical evaluation...",
            height=180,
            key="text_4",
        )

    if st.button("Run Critical Evaluation", type="primary", key="btn_4"):
        valid, err = validate_input(policy_text_4)
        if not valid:
            st.error(err)
        else:
            processed = preprocess_input(policy_text_4)
            with st.spinner("Conducting critical evaluation…"):
                try:
                    raw = run_analysis("evaluate", processed, options=output_options)
                    result = parse_response(raw, "evaluate")
                    st.session_state["result_4"] = result["critical_analysis"]
                    st.session_state["input_4"] = processed
                    save_to_history("evaluate", processed, result["critical_analysis"], output_options)
                except Exception as e:
                    st.error(f"Evaluation failed: {str(e)}")

    if st.session_state["result_4"]:
        st.divider()
        st.markdown(st.session_state["result_4"])
        st.divider()
        show_download_button(
            st.session_state["result_4"], "evaluate",
            st.session_state["input_4"], "4"
        )

st.divider()
st.caption("AI Policy Analysis & Comparison Assistant · Developed for AI Course Assignment · UET Taxila · Department of Software Engineering")
