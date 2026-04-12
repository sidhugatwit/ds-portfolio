# Project 01 — Credit Risk Engine

## Overview
End-to-end credit default prediction system trained on 1,000 real loan 
records. Compares Logistic Regression, Random Forest, and XGBoost, with 
full SHAP explainability and a three-tier risk scoring system.

## Key Results
| Model | ROC-AUC |
|-------|---------|
| Logistic Regression | see outputs/ |
| Random Forest | see outputs/ |
| XGBoost | see outputs/ |

## Methods
- **Feature Engineering** — credit/duration ratio, high-credit flag, one-hot encoding
- **Three Models** — Logistic Regression, Random Forest, XGBoost
- **SHAP Explainability** — feature importance for every prediction
- **Risk Tiers** — Low / Medium / High based on predicted default probability

## Stack
Python · XGBoost · Scikit-learn · SHAP · Plotly

## Target Companies
Capital One · Chase · Fidelity

## Files
- `notebooks/credit_risk.ipynb` — full analysis
- `outputs/shap_summary.png` — SHAP feature importance plot
- `outputs/risk_scores.csv` — predicted risk scores per borrower
- `outputs/model_comparison.csv` — AUC scores across all models