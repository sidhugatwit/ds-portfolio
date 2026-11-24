# RLHF

I trained a small reward model on preferences and simulated the effect of a KL penalty on policy rewards.

## Architecture

Preference pairs → DistilBERT reward model → chosen/rejected scores → KL-penalized reward simulation.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/rlhf_pipeline.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**Preference pairs** · 12. [Saved evidence](./outputs/preference_dataset.csv).

## Demo and deployment

TODO · Record a demo and verify any deployment. Capture a thumbnail from a real output or demo.

## Next steps

Report held-out preference ranking with data split details and keep the PPO simulation clearly labeled.

## Implementation notes

## Overview

Implements a complete Reinforcement Learning from Human Feedback pipeline
from scratch — the training methodology behind ChatGPT, Claude, and Gemini.
Trains a DistilBERT reward model on 12 human preference pairs across finance,
aviation, ML, and AI safety domains, then simulates PPO policy optimization
with KL divergence penalty.

## Pipeline Stages

1. **Human Preference Collection** — 12 prompt/chosen/rejected triplets
2. **Reward Model Training** — DistilBERT fine-tuned on preference pairs
3. **Reward Evaluation** — Accuracy of chosen > rejected ranking
4. **PPO Simulation** — KL-penalized reward shaping objective

## Key Results

| Metric | Value |
|--------|-------|
| Reward model train loss | 0.3455 (epoch 5) |
| Reward model test loss | 0.3522 (epoch 5) |
| Chosen > rejected accuracy | see outputs/ |
| Avg reward margin | see outputs/ |

## RLHF Objective

The PPO optimization objective implemented:

maximize: E[r(x,y)] - β * KL(π_RL || π_ref)

Where r(x,y) is the reward model score, β controls policy drift,
and KL divergence prevents the RL policy from deviating too far
from the reference model.

## Domains Covered

- Finance (credit scoring, Black-Scholes, portfolio theory)
- Aviation (ILS glide slope, safe landing procedures)
- ML/AI (overfitting, neural networks, gradient descent)
- AI Safety (alignment vs safety, RLHF itself)

## Stack

Python · PyTorch · HuggingFace Transformers · DistilBERT · Plotly · Pandas

## Files

- `notebooks/rlhf_pipeline.ipynb` — full RLHF implementation
- `outputs/preference_dataset.csv` — 12 human preference pairs
- `outputs/reward_scores.csv` — chosen vs rejected reward scores
- `outputs/ppo_simulation.csv` — KL-penalized reward per prompt
- `outputs/training_curves.csv` — loss curves across 5 epochs
