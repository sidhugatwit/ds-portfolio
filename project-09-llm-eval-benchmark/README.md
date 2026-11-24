# LLM Eval

I built a repeatable benchmark for comparing local and hosted models on aviation and finance questions.

## Architecture

Curated questions → saved model responses → lexical and semantic scoring → comparison by model.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen python src/rescore.py --skip-bert` to rescore saved responses offline.

## Results

**Mean ROUGE-L, 20 questions per model** · 0.421 vs 0.306. [Saved evidence](./outputs/leaderboard.csv).

The saved leaderboard compares GPT-4o-mini and Mistral-7B in that order. Text overlap is one measure of answer quality.

## Demo and deployment

TODO · Record a demo and verify any deployment.

## Next steps

Instrument per-request cost and latency, then build a dashboard that explains which calls and models drive the differences.

## Implementation notes

## Overview
A domain-specific evaluation benchmark testing real LLMs on 20 
hand-curated QA pairs across finance and aviation. Compares 
GPT-4o-mini (OpenAI API) vs Mistral-7B (local via LM Studio) 
using ROUGE and BERTScore metrics.

> Scope note: 20 QA pairs is a small benchmark — useful for spotting
> failure modes per domain, not for statistically significant model rankings.

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

## Reproducing v1

The original v1 notebook is no longer available, but every model response was saved.
`src/rescore.py` recomputes the scores from `outputs/llm_responses.csv`:
ROUGE reproduces the published scores exactly on all 40 rows.

```bash
pip install -r requirements.txt
python src/rescore.py            # ROUGE + BERTScore (downloads roberta-large once)
python src/rescore.py --skip-bert
```

A larger v2 benchmark is in progress.

## Files
- `src/rescore.py` — recomputes v1 scores from saved responses
- `outputs/benchmark_qa.csv` — 20 verified QA pairs
- `outputs/llm_responses.csv` — raw model responses
- `outputs/eval_scores.csv` — ROUGE and BERTScore per question
- `outputs/leaderboard.csv` — aggregate scores by model
