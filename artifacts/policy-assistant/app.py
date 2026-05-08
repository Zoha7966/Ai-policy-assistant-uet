import streamlit as st
import fitz  # PyMuPDF
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from utils.llm import call_llm, classify_task
from utils.prompts import (
    SUMMARIZATION_PROMPT,
    EXPLANATION_PROMPT,
    COMPARISON_PROMPT,
    EVALUATION_PROMPT,
)
from utils.parser import parse_response, preprocess_input, validate_input

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

def extract_pdf_text(uploaded_file) -> str:
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def run_analysis(task: str, policy_input: str, policy_2: str = "") -> str:
    if task == "summarize":
        prompt = SUMMARIZATION_PROMPT.format(policy_input=policy_input)
    elif task == "explain":
        prompt = EXPLANATION_PROMPT.format(policy_input=policy_input)
    elif task == "compare":
        prompt = COMPARISON_PROMPT.format(policy_1=policy_input, policy_2=policy_2)
    elif task == "evaluate":
        prompt = EVALUATION_PROMPT.format(policy_input=policy_input)
    else:
        prompt = SUMMARIZATION_PROMPT.format(policy_input=policy_input)

    return call_llm(prompt)

with st.sidebar:
    st.header("How to Use")
    st.markdown("""
1. **Select a function** from the tabs above
2. **Enter a policy name** or **upload a PDF**
3. Click **Analyze** to get AI-powered insights
    """)
    st.divider()
    st.subheader("Four Core Functions")
    for key, label in TASK_LABELS.items():
        st.markdown(f"**{label}**")
        st.caption(TASK_DESCRIPTIONS[key])
        st.write("")
    st.divider()
    st.subheader("Sample Policies to Try")
    st.markdown("""
- National Education Policy 2017
- Digital Pakistan Vision
- CPEC Framework Agreement
- Pakistan Economic Survey
- National Health Vision 2016-2025
    """)

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Summarization",
    "🔍 Plain-Language Explanation",
    "⚖️ Comparative Analysis",
    "🔬 Critical Evaluation",
])

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
            with st.spinner("Analyzing policy... this may take a moment."):
                try:
                    raw = run_analysis("summarize", processed)
                    result = parse_response(raw, "summarize")
                    st.divider()
                    st.markdown(result["summary"])
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")

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
            with st.spinner("Simplifying policy language..."):
                try:
                    raw = run_analysis("explain", processed)
                    result = parse_response(raw, "explain")
                    st.divider()
                    st.markdown(result["plain_language"])
                except Exception as e:
                    st.error(f"Explanation failed: {str(e)}")

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
            with st.spinner("Comparing policies... this may take a moment."):
                try:
                    raw = run_analysis("compare", p1, p2)
                    result = parse_response(raw, "compare")
                    st.divider()
                    st.markdown(result["comparison"])
                except Exception as e:
                    st.error(f"Comparison failed: {str(e)}")

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
            with st.spinner("Conducting critical evaluation..."):
                try:
                    raw = run_analysis("evaluate", processed)
                    result = parse_response(raw, "evaluate")
                    st.divider()
                    st.markdown(result["critical_analysis"])
                except Exception as e:
                    st.error(f"Evaluation failed: {str(e)}")

st.divider()
st.caption("AI Policy Analysis & Comparison Assistant · Developed for AI Course Assignment · UET Taxila · Department of Software Engineering")
