# AI Policy Analysis & Comparison Assistant

An AI-powered Streamlit web app for analyzing, simplifying, and comparing public policy documents — built as an AI course assignment at UET Taxila.

## Run & Operate

- `cd artifacts/policy-assistant && streamlit run app.py` — start the Streamlit app (port 5000)
- Workflow "Start application" runs the app automatically

## Stack

- **Language**: Python
- **UI**: Streamlit
- **AI**: Google Gemini 2.5 Flash (via Replit AI Integrations — no API key needed)
- **PDF Parsing**: PyMuPDF (fitz)

## Where things live

- `artifacts/policy-assistant/app.py` — main Streamlit application (all 4 functions as tabs)
- `artifacts/policy-assistant/utils/prompts.py` — prompt templates for each of the 4 task types
- `artifacts/policy-assistant/utils/llm.py` — Gemini AI client + task classifier
- `artifacts/policy-assistant/utils/parser.py` — response parser and input validation
- `artifacts/policy-assistant/.streamlit/config.toml` — Streamlit server config
- `artifacts/policy-assistant/requirements.txt` — Python dependencies
- `README.md` — project documentation (for GitHub)

## Architecture

```
User Input → Input Validation → Task Classifier → Prompt Constructor → Gemini API → Response Parser → Streamlit UI
```

## Four Core Functions

1. **Policy Summarization** — key objectives, mechanisms, stakeholders
2. **Plain-Language Explanation** — bureaucratic terms → accessible language
3. **Comparative Analysis** — structured side-by-side policy comparison
4. **Critical Evaluation** — strengths, weaknesses, risks, societal impact

## Environment Variables

- `AI_INTEGRATIONS_GEMINI_BASE_URL` — auto-set by Replit AI Integrations
- `AI_INTEGRATIONS_GEMINI_API_KEY` — auto-set by Replit AI Integrations

## GitHub

Push to GitHub using Replit's Version Control panel (Git tab in the sidebar). The `.gitignore` is configured to exclude secrets, cache, and generated files.

## User preferences

- Python-based application
- Streamlit UI framework
- Strictly 4 core functions (no extras)
- GitHub-ready codebase

## Gotchas

- Run `pip install -r artifacts/policy-assistant/requirements.txt` if packages are missing after a fresh clone
- The Gemini env vars are provisioned by Replit — do not hardcode them
- PDF extraction uses PyMuPDF (imported as `fitz`)
