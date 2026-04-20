# Project 18 — Love at First Agent

## Overview

Can AI predict if two people will fall in love? Yes — with a ROC AUC of 0.8553. This project builds a LangGraph ReAct agent that autonomously profiles data, guards against leakage, selects features, trains an XGBoost classifier, and predicts match probability — all from a single natural language instruction.

## The Agent Pipeline

"Clean the data, select top features, and predict match probability."
↓
DataProfilerAgent → LeakageGuardAgent → ModelTrainerAgent → EvaluatorAgent

## Key Results

| Metric | Value |
|--------|-------|
| Dataset | 8,378 speed dates, 195 features |
| Match rate | 16.5% (class imbalanced) |
| ROC AUC | 0.8553 (clean, no leakage) |
| Top predictor | Attractiveness, Fun, Shared Interests |

## Leakage Detection

The agent correctly identified `dec` and `dec_o` as data leakage 
columns — decisions made during the date that would give the model 
unfair information unavailable at prediction time.

## LangGraph Tools

- **profile_data** — dataset statistics and metric recommendation
- **check_leakage** — flags decision columns before training
- **train_model** — XGBoost training with ROC AUC evaluation
- **evaluate_match_probability** — live prediction for new couples

## Stack

Python · LangGraph · LangChain · GPT-4o-mini · XGBoost ·
Scikit-learn · Plotly · python-dotenv

## Files

- `notebooks/love_at_first_agent.ipynb` — full pipeline
- `src/agents.py` — modular agent definitions
- `slides/LoveAtFirstAgent.pptx` — original group presentation
- `outputs/top_features_clean.csv` — RFE selected features
- `outputs/model_results.csv` — ROC AUC comparison
