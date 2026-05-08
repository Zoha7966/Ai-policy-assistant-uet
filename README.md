# AI Policy Analysis & Comparison Assistant

An AI-powered web application for analyzing, simplifying, and comparing public policy documents — with a focus on Pakistan's governance, education, economy, and social welfare policies.

Built as an AI course assignment at **UET Taxila, Department of Software Engineering**.

## Four Core Functions

| Function | Description |
|----------|-------------|
| **Policy Summarization** | Extracts key objectives, implementation mechanisms, and stakeholder responsibilities |
| **Plain-Language Explanation** | Translates bureaucratic/technical terminology into accessible language |
| **Comparative Analysis** | Structured side-by-side comparison of two policies across key dimensions |
| **Critical Evaluation** | Identifies strengths, weaknesses, risks, and real-world societal impact |

## Tech Stack

- **Language**: Python
- **UI**: Streamlit
- **AI**: Google Gemini 2.5 Flash (via Replit AI Integrations)
- **PDF Parsing**: PyMuPDF

## Architecture

```
User Input → Input Layer → Task Classifier → Prompt Constructor → LLM API → Response Parser → Output Layer
```

Each of the four tasks uses a dedicated prompt template engineered specifically for policy analysis.

## Running Locally

```bash
pip install -r artifacts/policy-assistant/requirements.txt
cd artifacts/policy-assistant
streamlit run app.py --server.port 5000
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AI_INTEGRATIONS_GEMINI_BASE_URL` | Gemini API proxy base URL |
| `AI_INTEGRATIONS_GEMINI_API_KEY` | Gemini API key |

## Sample Policies to Analyze

- National Education Policy 2017
- Digital Pakistan Vision
- CPEC Framework Agreement
- Pakistan Economic Survey
- National Health Vision 2016-2025

## Submitted By

- Laiba Muzammal (23-SE-06)
- Zoha Malik (23-SE-32)

**Submitted to:** Ma'am Kanwal  
**Course:** Artificial Intelligence — 6th Semester  
**Date:** April 23, 2026
