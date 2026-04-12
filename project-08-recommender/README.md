# Project 08 — Recommendation Engine with Implicit Feedback

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

## Target Companies
Netflix · Amazon · Meta

## Files
- `notebooks/recommender.ipynb` — full ALS pipeline
- `outputs/eval_metrics.csv` — NDCG@10 and genre match rate
- `outputs/genre_match_rates.csv` — per-user preference alignment
- `outputs/recommendation_frequency.csv` — item recommendation counts
- `outputs/items_metadata.csv` — item catalog with genres