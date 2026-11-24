# Credit Risk

I benchmarked default models and used SHAP to inspect which borrower features drove predictions.

## Architecture

Lending data → split and train-fold preprocessing → baseline and tree models → ROC-AUC comparison and SHAP explanations.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/credit_risk.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**XGBoost holdout ROC-AUC** · 0.794. [Saved evidence](./outputs/model_comparison.csv).

## Demo and deployment

TODO · Record a demo and verify any deployment.

## Next steps

Add drift monitoring and an automatic retraining workflow with a baseline comparison and promotion gate.

## Implementation notes

## Overview
End-to-end credit default prediction system trained on 1,000 real loan 
records. Compares Logistic Regression, Random Forest, and XGBoost, with 
full SHAP explainability and a three-tier risk scoring system.

## Key Results
| Model | Holdout ROC-AUC | 5-fold CV ROC-AUC |
|-------|-----------------|-------------------|
| Logistic Regression | 0.816 | 0.784 ± 0.021 |
| Random Forest | 0.813 | 0.794 ± 0.020 |
| XGBoost | 0.794 | 0.793 ± 0.023 |

**Takeaway:** on 1,000 loans, gradient boosting does not beat a well-specified
logistic-regression baseline — the simpler model is the defensible choice.

### Leakage fix (Oct 2026)
An earlier version reported ROC-AUC = 1.00 for every model. Root cause:
`fetch_openml('credit-g').frame` still contains the raw label column `class`,
and one-hot encoding turned it into `class_good` — the target itself. The
notebook now drops `class` explicitly and asserts no label-derived column
reaches `X`.

## Methods
- **Feature Engineering** — credit/duration ratio, high-credit flag, one-hot encoding
- **Three Models** — Logistic Regression, Random Forest, XGBoost
- **Validation** — stratified 80/20 holdout + 5-fold stratified CV (scaling inside the pipeline)
- **SHAP Explainability** — feature importance for every prediction
- **Risk Tiers** — Low / Medium / High based on predicted default probability

## Stack
Python · XGBoost · Scikit-learn · SHAP · Plotly

## Files
- `notebooks/credit_risk.ipynb` — full analysis
- `outputs/shap_summary.png` — SHAP feature importance plot
- `outputs/risk_scores.csv` — predicted risk scores per borrower
- `outputs/model_comparison.csv` — holdout and 5-fold CV AUC per model
