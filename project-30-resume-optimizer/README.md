# Career Tools

I built a resume workflow that surfaces keyword gaps and prepares drafts. I’m keeping my interview-prep and resume-assistant prototypes alongside it.

## Architecture

Resume and job description → keyword comparison → rewritten draft and cover-letter exports.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/resume_optimizer.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**Saved keyword checks** · 50. [Saved evidence](./outputs/ats_analysis.csv).

## Demo and deployment

TODO · Record a demo and verify any deployment. Capture a thumbnail from a real output or demo.

## Next steps

Add a shared example and check that generated drafts preserve supplied facts before combining the tools.

## Companion projects

- [project-22-interview-prep-agent](../archive/project-22-interview-prep-agent)
- [project-32-resume-assistant](../archive/project-32-resume-assistant)

The companion experiments remain independently reproducible.

## Implementation notes

## Overview

An AI-powered resume optimization system that analyzes job descriptions,
scores ATS keyword compatibility, rewrites resume bullets for maximum
impact, and generates tailored cover letters — all exported as
production-ready DOCX files.

## Key Results

| Metric | Value |
|--------|-------|
| Original ATS Score | 22.0% |
| Optimized ATS Score | 90% |
| ATS Improvement | +68 percentage points |
| Bullets Rewritten | 6 |
| Keywords Analyzed | 50 JD keywords |

## Pipeline

1. **ATS Analysis** — NLTK keyword extraction comparing resume vs JD
2. **Gap Identification** — Missing keywords ranked by JD frequency
3. **Resume Rewriter** — GPT-4o-mini rewrites bullets with missing keywords
4. **Cover Letter Generator** — Tailored 3-paragraph cover letter
5. **DOCX Export** — Professional Word document ready to send

## Stack

Python · OpenAI API · NLTK · python-docx · Pandas

## Files

- `notebooks/resume_optimizer.ipynb` — full pipeline
- `outputs/cover_letter.docx` — tailored cover letter
- `outputs/ats_analysis.csv` — keyword match/miss breakdown
- `outputs/rewritten_resume.json` — optimized bullet points
