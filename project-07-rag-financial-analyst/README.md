# Project 07 — RAG Financial Document Analyst

## Overview

Answers analyst questions about NVIDIA, Microsoft, JPMorgan, Amazon and Tesla from their latest **10-K filings
on SEC EDGAR**, cites every claim, and checks the answer against its sources.

| Step | What it does |
|------|--------------|
| Corpus | Each company's latest 10-K: Item 1A (Risk Factors) and Item 7 (MD&A), split into ~1,200-character chunks; reported revenue and net income from SEC XBRL company facts |
| Retrieval | Dense (BGE-small embeddings + FAISS), keyword (BM25), and hybrid (reciprocal rank fusion), with company filtering from the question |
| Evaluation | 20 labelled questions: hit@5, keyword hit@5 and MRR for each retrieval mode (`outputs/retrieval_eval.csv`) |
| Answers | An LLM answers only from retrieved passages and XBRL figures, citing `[S1]`, `[F]`; each answer is checked: citations must exist, and every number must appear in a cited source |

Retrieval and evaluation need no LLM, so CI re-runs them on every push. Figure questions ("which company had the
highest revenue?") get the XBRL table as a source, because top-k passage retrieval can't compare five companies.

## Results

Latest 10-Ks: NVIDIA (fiscal year ended Jan 2026), Microsoft (June 2026), JPMorgan, Amazon and Tesla (Dec 2025).
695 chunks from 9 sections; JPMorgan's MD&A is only cross-referenced in its 10-K (it sits in the annual report), so it is reported as missing.

**Retrieval** (20 labelled questions, top 5):

| Mode | hit@5 | keyword hit@5 | MRR |
|------|-------|---------------|-----|
| Dense (BGE-small) | 1.00 | 0.90 | 0.96 |
| BM25 | 0.85 | 0.70 | 0.76 |
| Hybrid (RRF) | 0.95 | 0.95 | 0.86 |
| Hybrid + company filter | 0.95 | 0.95 | 0.93 |

Dense retrieval finds the right section most often; the hybrid modes most often return the passage that contains
the expected terms, and the company filter recovers most of the ranking quality.

**Answers** (Qwen3.6-35B-A3B in LM Studio, 8 passages per question, `outputs/rag_run.json`): 3 grounded, 1 partial.
The partial one is honest: Tesla's MD&A passages give the 8% drop in cash deliveries but not the delivery count.

Two lessons from building it:
- With 5 passages, the AWS answer said "no information"; the segment-results passage ranked 6th. Answers now use 8.
- The grounding check first passed that non-answer because it cited real sources. Answers now get a verdict:
  grounded, partial, abstained, or check (an invented citation or number).

## Why it was rebuilt

The first version answered from 13 hand-written passages rather than filings, labelled them "10-K 2023", and never
called an LLM. Its revenue figures were off by -40% (NVIDIA), -21% (Microsoft), -11% (Amazon), +20% (Tesla) and
-4% (JPMorgan) against the filings; the notebook prints that audit (cell 3).

## Run it

1. Add `SEC_USER_AGENT=Your Name your.email@example.com` to the repo's `.env` (SEC requires a contact; EDGAR is free).
2. `uv run jupyter lab` and run `notebooks/rag_financial_analyst.ipynb`. The first run downloads the filings and saves
   the corpus to `corpus/`; later runs reuse it.
3. Cell 6 answers questions with the LLM set in `.env` (LM Studio works) and saves `outputs/rag_run.json`.
4. `uv run pytest -q` runs the offline tests (section extraction, chunking, retrieval, answer checks).

## Stack

Python · SEC EDGAR + XBRL APIs · BeautifulSoup · sentence-transformers (BGE) · FAISS · BM25 · OpenAI-compatible LLM · pytest

## Files

- `src/edgar.py`: fetch filings and facts, extract sections, chunk
- `src/rag.py`: dense, BM25 and hybrid retrieval; evaluation
- `src/answer.py`: cited answers and grounding checks
- `eval/questions.csv`: labelled questions
- `corpus/`: chunks, facts and section coverage built from EDGAR
- `outputs/`: retrieval scores and saved LLM runs
