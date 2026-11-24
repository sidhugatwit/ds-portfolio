# Project 32 — Resume Assistant (Streamlit console + n8n pipeline)

## Overview

A two-part tool that tailors a resume to a specific job posting.

- **CLI client (`app.py`)** reads a resume PDF and a job posting, then sends both to an
  n8n webhook pipeline that runs the LLM analysis and returns suggestions.
- **Streamlit console (`frontend/streamlit_app.py`)** is a chat-style workspace: upload a
  `.docx` resume to be embedded into ChromaDB, paste a job description, and watch the
  pipeline's agents stream their feedback. It also charts ATS-alignment scores over time
  and shows a simple application board.

> **Status: in development.** The console expects a FastAPI backend at
> `RESUME_BACKEND_URL` (default `http://127.0.0.1:8000/api/v1`) with
> `/process-document` and `/chat/stream` endpoints. That backend is not in this
> folder yet, so the console runs and renders, but chat and upload need the backend.

## Run it

```bash
pip install -r requirements.txt

# CLI: paste the job posting into a text file (recommended)
python app.py --resume path/to/resume.pdf --job-file job.txt

# or fetch a public posting page
python app.py --resume path/to/resume.pdf --url https://example.com/job

# Streamlit console
streamlit run frontend/streamlit_app.py
```

The CLI posts to `RESUME_WEBHOOK_URL` (default: a local n8n instance at
`http://localhost:5678/webhook/resume-assistant-pipeline`).

## Design notes

- **Paste-first job input.** Many job boards prohibit scraping. The client identifies
  itself honestly, and if a site blocks it, you paste the posting into a file.
- **No invented numbers.** The ATS chart only plots scores the backend actually returns
  (an `ats_score` field in the stream). It starts empty.
- **Private data stays local.** Your real application board lives in
  `data/applications.json`, which is git-ignored. Without it, the console shows labeled
  sample data. Format:

  ```json
  { "saved": ["Role, Company"], "active": ["Role, Company"], "offers": [] }
  ```

## Stack

Python · Streamlit · Plotly · httpx · n8n · ChromaDB (via backend) · pypdf · BeautifulSoup

## Files

- `app.py` — CLI client: resume PDF + job posting → n8n webhook
- `frontend/streamlit_app.py` — Streamlit workspace console
- `requirements.txt` — Python dependencies
