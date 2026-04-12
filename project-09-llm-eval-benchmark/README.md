# Project 09 — LLM Evaluation & Hallucination Benchmark

## Overview
A domain-specific evaluation benchmark testing real LLMs on 20 
expert-verified QA pairs across finance and aviation. Compares 
GPT-4o-mini (OpenAI API) vs Mistral-7B (local via LM Studio) 
using ROUGE and BERTScore metrics — the same evaluation stack 
used by Perplexity and Meta AI research teams.

## What Makes This Unique
- Real API calls to GPT-4o-mini and Mistral-7B — not simulated
- Custom benchmark curated from domain expertise in finance and aviation
- Evaluates both lexical overlap (ROUGE) and semantic similarity (BERTScore)
- Per-question heatmap reveals where each model struggles by domain

## Methods
- **ROUGE-1/2/L** — Lexical overlap between model response and reference
- **BERTScore F1** — Semantic similarity using BERT embeddings
- **Domain Split** — Separate scoring for finance vs aviation questions
- **Per-Question Heatmap** — Identifies specific failure modes per model

## Models Evaluated
| Model | Provider | Inference |
|-------|----------|-----------|
| GPT-4o-mini | OpenAI API | Cloud |
| Mistral-7B-Instruct-v0.2 | LM Studio | Local |

## Stack
Python · OpenAI API · LM Studio · ROUGE · BERTScore · Plotly · Pandas

## Target Companies
Perplexity · Meta · Amazon · Anthropic · OpenAI

## Files
- `notebooks/llm_eval_benchmark.ipynb` — full evaluation pipeline
- `outputs/benchmark_qa.csv` — 20 verified QA pairs
- `outputs/llm_responses.csv` — raw model responses
- `outputs/eval_scores.csv` — ROUGE and BERTScore per question
- `outputs/leaderboard.csv` — aggregate scores by model