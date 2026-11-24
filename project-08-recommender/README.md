# Recommender

I used implicit feedback to rank recommendations and measured the quality of the resulting lists.

## Architecture

Interaction matrix → implicit-feedback ALS → ranked items → held-out ranking and exposure analysis.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/recommender.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**NDCG@10** · 0.4862. [Saved evidence](./outputs/eval_metrics.csv).

## Demo and deployment

TODO · Record a demo and verify any deployment. Capture a thumbnail from a real output or demo.

## Next steps

Add a popularity baseline on the same split and record a ranking walkthrough.

## Implementation notes

## Overview
Netflix/Amazon-style recommendation engine built on Alternating Least 
Squares (ALS) matrix factorization using implicit feedback signals 
(play counts, engagement depth). Trained on 1,000 users and 500 items 
with genre-aware evaluation and popularity bias analysis.

## Methods
- **Implicit Feedback** — Confidence matrix: C = 1 + alpha * plays
- **ALS Matrix Factorization** — 64 latent factors, 30 iterations
- **NDCG@10** — Normalized Discounted Cumulative Gain for ranking quality
- **Genre Match Rate** — Preference alignment metric across 200 users
- **Popularity Bias Analysis** — Recommendation frequency vs item popularity

## Key Results
- ALS successfully surfaces genre-preferred items for most users
- Genre match rate shows strong preference alignment
- NDCG@10 evaluated across 200 held-out users

## Stack
Python · Implicit · SciPy Sparse · Scikit-learn · Plotly · Pandas

## Files
- `notebooks/recommender.ipynb` — full ALS pipeline
- `outputs/eval_metrics.csv` — NDCG@10 and genre match rate
- `outputs/genre_match_rates.csv` — per-user preference alignment
- `outputs/recommendation_frequency.csv` — item recommendation counts
- `outputs/items_metadata.csv` — item catalog with genres
