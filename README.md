# AI Policy Analysis & Comparison Assistant

> An AI-powered web application for analyzing, simplifying, and comparing public policy documents — built for Pakistan's governance, education, economy, and social welfare contexts.

---

## About the Project

Policy documents are often written in complex, bureaucratic language that is difficult for students, researchers, and ordinary citizens to understand. This tool uses Google's Gemini AI to make policy analysis fast, clear, and accessible.

You can upload a PDF or paste any policy text and get an instant structured analysis in seconds.

---

## Live Demo

> Run the app directly — no installation needed:  
> **[Launch App](https://ai-doc-reader--zohamalik66.replit.app)**

---

## Four Core Functions

| # | Function | What It Does |
|---|----------|-------------|
| 1 | **Policy Summarization** | Extracts key objectives, implementation mechanisms, stakeholders, and expected outcomes |
| 2 | **Plain-Language Explanation** | Rewrites complex bureaucratic or legal language into simple, everyday English |
| 3 | **Comparative Analysis** | Produces a structured side-by-side comparison of two policies across 8+ dimensions |
| 4 | **Critical Evaluation** | Assesses a policy's strengths, weaknesses, risks, societal impact, and feasibility |

---

## Key Features

- **PDF Upload** — Upload any policy document and extract text automatically
- **Output Settings** — Choose between Short / Medium / Detailed response modes
- **Key Insights Mode** — Extract only the top 5 most important policy goals
- **Output Length Control** — Compress responses to 30%, 50%, 80%, or full length
- **Rank by Importance** — AI sorts all points with critical national goals first
- **Session History** — Every analysis is saved in-session with timestamp and settings used
- **PDF Export** — Download any result as a formatted PDF report

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3 |
| UI Framework | Streamlit |
| AI Model | Google Gemini 2.5 Pro |
| PDF Parsing | PyMuPDF (fitz) |
| PDF Export | fpdf2 |

---

## Project Structure

```
artifacts/policy-assistant/
├── app.py                  # Main Streamlit application (4 tabs, sidebar, history)
├── utils/
│   ├── llm.py              # Gemini AI client
│   ├── prompts.py          # Prompt templates for all 4 task types + output modifiers
│   ├── parser.py           # Input validation and response parser
│   └── pdf_export.py       # PDF generation with formatting
└── requirements.txt        # Python dependencies
```

---

## Architecture

```
User Input (text / PDF)
        ↓
  Input Validation
        ↓
  Output Settings (mode, compression, ranking)
        ↓
  Prompt Constructor  ←  Prompt Templates
        ↓
  Gemini 2.5 Pro API
        ↓
  Response Parser
        ↓
  Streamlit UI  →  PDF Export  /  Session History
```

---

## Running Locally

**1. Clone the repository**
```bash
git clone https://github.com/Zoha7966/Ai-policy-assistant-uet.git
cd Ai-policy-assistant-uet
```

**2. Install dependencies**
```bash
pip install -r artifacts/policy-assistant/requirements.txt
```

**3. Set your Gemini API key**

Get a free key from [Google AI Studio](https://aistudio.google.com/):
```bash
export AI_INTEGRATIONS_GEMINI_API_KEY=your_key_here
export AI_INTEGRATIONS_GEMINI_BASE_URL=https://generativelanguage.googleapis.com
```

**4. Run the app**
```bash
cd artifacts/policy-assistant
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Sample Policies to Try

- National Education Policy 2017
- Digital Pakistan Vision
- CPEC Framework Agreement
- Pakistan Economic Survey 2023-24
- National Health Vision 2016-2025
- Climate Change Policy of Pakistan

---

## Assignment Details

| Field | Details |
|-------|---------|
| **Students** | Laiba Muzammal (23-SE-06) · Zoha Malik (23-SE-32) |
| **Course** | Artificial Intelligence — 6th Semester |
| **Instructor** | Ma'am Kanwal |
| **Department** | Software Engineering |
| **University** | University of Engineering & Technology, Taxila |
| **Submitted** | May 2026 |

---

## License

This project was developed for academic purposes at UET Taxila.
