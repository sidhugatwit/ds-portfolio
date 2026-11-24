# Fraud Detection

I compared anomaly detection and supervised baselines, then examined how alert thresholds change the queue.

## Architecture

Synthetic transactions → anomaly and supervised models → threshold sweep → simulated alert queue.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/fraud_detection.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**Average precision, synthetic holdout** · 1.00. [Saved evidence](./outputs/model_comparison.csv).

All three models reached 1.00 average precision on this synthetic holdout. Treat this as a property of the experiment.

## Demo and deployment

TODO · Record a demo and verify any deployment. Capture a thumbnail from a real output or demo.

## Next steps

Check for generator artifacts and benchmark on a harder held-out dataset before making any performance claim about real transactions.

## Implementation notes

## Overview
End-to-end fraud detection system trained on 10,000 imbalanced transactions 
with a 3% fraud rate. Compares Isolation Forest (unsupervised anomaly 
detection), Random Forest, and Logistic Regression with SMOTE resampling. 
Includes a real-time streaming simulation with configurable alert thresholds.

## Methods
- **SMOTE** — Synthetic Minority Oversampling to handle class imbalance
- **Isolation Forest** — Unsupervised anomaly detection baseline
- **Random Forest** — Supervised classifier with balanced class weights
- **Threshold Analysis** — Precision/recall tradeoff at 6 alert thresholds
- **Stream Simulation** — Real-time transaction scoring with timestamped alerts

## Key Results
- The checked-in synthetic comparison reports average precision of 1.00 for all three models
- Threshold of 0.55 balances fraud catch rate with false positive volume
- Streaming simulation processes 100 transactions with live alert firing

## Stack
Python · Scikit-learn · Imbalanced-learn · River · Plotly · Pandas

## Files
- `notebooks/fraud_detection.ipynb` — full pipeline
- `outputs/stream_alerts.csv` — timestamped real-time alerts
- `outputs/fraud_dataset.csv` — engineered feature dataset
- `outputs/model_comparison.csv` — AUC and precision scores
