# Project 02 — Real-Time Fraud Detection Pipeline

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
- Random Forest achieves highest Average Precision across all models
- Threshold of 0.55 balances fraud catch rate with false positive volume
- Streaming simulation processes 100 transactions with live alert firing

## Stack
Python · Scikit-learn · Imbalanced-learn · River · Plotly · Pandas

## Target Companies
Capital One · Chase · Amazon

## Files
- `notebooks/fraud_detection.ipynb` — full pipeline
- `outputs/stream_alerts.csv` — timestamped real-time alerts
- `outputs/fraud_dataset.csv` — engineered feature dataset
- `outputs/model_comparison.csv` — AUC and precision scores