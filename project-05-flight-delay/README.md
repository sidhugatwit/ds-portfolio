# Project 05 — Flight Delay Prediction with Causal ML

## Overview
Predicts and explains flight delays using a structural causal model 
built with DoWhy. Isolates the true causal effect of weather, NAS 
congestion, carrier issues, and late aircraft on delay probability — 
going beyond correlation to answer *why* flights are delayed.

## Methods
- **Causal DAG** — Directed Acyclic Graph encoding domain knowledge
- **Backdoor Criterion** — Identifies valid adjustment sets for causal estimation
- **Linear Regression Estimator** — Estimates Average Treatment Effect (ATE)
- **Placebo Refutation** — Validates causal estimate by permuting treatment
- **GBM Predictor** — Gradient Boosting for delay classification (ROC-AUC)

## Key Results
| Cause | Causal Effect on Delay Probability |
|-------|-----------------------------------|
| Weather Severity | 0.0811 |
| NAS Congestion | see outputs/ |
| Carrier Issues | see outputs/ |
| Late Aircraft | see outputs/ |

## Stack
Python · DoWhy · Scikit-learn · Plotly · Pandas

## Target Companies
Delta Airlines · United Airlines · Amazon

## Files
- `notebooks/flight_delay_causal.ipynb` — full causal analysis
- `outputs/causal_effects.csv` — ATE per delay cause
- `outputs/feature_importance.csv` — GBM feature importances
- `outputs/flight_delay_dataset.csv` — full simulated dataset