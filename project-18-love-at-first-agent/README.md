# Project 18 — Love at First Agent

## Overview

Can you predict whether two people will match at a speed-dating event before they meet?
This project trains XGBoost on the Columbia speed-dating experiment (8,378 dates) and gives a
LangGraph ReAct agent tools to profile the data, check features for leakage, train models and
score a new couple.

The main finding is about leakage. Most columns in this dataset were filled in **during or
after** each date: how attractive, fun or likeable the partner seemed, and how likely a "yes"
felt. A model that uses them scores about 0.85 ROC AUC, but it can't be used before the date,
because the inputs don't exist yet. With only sign-up information, the honest score is about 0.68.

## Results

Held-out ROC AUC; splits are grouped so the same couple is never in both train and test.

| Model | ROC AUC |
|---|---|
| Naive: top 10 features, includes date ratings (`attr`, `like`, `prob`, `attr_o`, ...) | 0.85 |
| Honest: all 67 pre-date features | 0.68 |
| Honest: 5-fold CV grouped by couple | 0.68 ± 0.03 |
| Honest: 5-fold CV grouped by event (people the model has never seen) | 0.59 ± 0.03 |

Exact values are in `outputs/model_results.csv`. Match rate is 16.5%, so ROC AUC is the main metric.

An earlier version of this project reported 0.8553 as "clean, no leakage". It removed the
decision columns (`dec`, `dec_o`) but kept the date ratings, so that number was still leaked.
The table above replaces it.

## Leakage rules

| Group | Examples | Used? |
|---|---|---|
| Outcome | `match`, `dec`, `dec_o` | no |
| Scorecard and follow-ups | `attr`, `sinc`, `intel`, `fun`, `amb`, `shar`, `like`, `prob`, `met` and their `_o` versions, `match_es`, `*_s`, `*_2`, `*_3` | no |
| Sign-up survey | `age`, `age_o`, `int_corr`, `samerace`, stated preferences (`attr1_1`, `pf_o_att`, ...), interests | yes |

## Agent tools

- **profile_data**: size, match rate and the recommended metric
- **check_leakage**: flags outcome columns and anything recorded during or after the date
- **train_model**: XGBoost with held-out ROC AUC; drops leaky features unless `allow_leakage` is set, so the agent can show the difference
- **predict_match**: match probability for a new couple from pre-date inputs only

## Run it

1. Download `Speed Dating Data.csv` from Kaggle's "Speed Dating Experiment" dataset into `data/raw/`.
2. Set an OpenAI-compatible endpoint in the repo's `.env` (see `.env.example`; LM Studio with a local model works, and reasoning models need `LLM_REASONING_TOKENS`).
3. `uv run jupyter lab` and run `notebooks/love_at_first_agent.ipynb`.

The agent's answers are saved to `outputs/agent_run.json` with the model name that produced them.

## Stack

Python · LangGraph · LangChain · XGBoost · scikit-learn · Plotly · any OpenAI-compatible LLM

## Files

- `notebooks/love_at_first_agent.ipynb`: full pipeline and agent
- `src/agents.py`: the leakage check and agent as an importable module
- `outputs/model_results.csv`: ROC AUC for each model
- `outputs/features.json`: naive and honest feature lists
