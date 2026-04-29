# Project 24 — Parkinson's Tremor Detector (Voice Analysis)

## Overview

Detects Parkinson's disease from voice recordings using biomedical
voice measurements. Trains four classifiers on 22 voice features
including MDVP jitter, shimmer, HNR, RPDE, and DFA — achieving
clinical-grade sensitivity for non-invasive screening.

## Key Results

| Model | ROC-AUC |
|-------|---------|
| XGBoost | 0.9828 |
| SVM (RBF) | 0.9828 |
| Random Forest | 0.9690 |
| Gradient Boosting | 0.9655 |

## Clinical Performance (XGBoost)

| Metric | Value | Meaning |
|--------|-------|---------|
| Sensitivity | 96.6% | Parkinson's cases correctly detected |
| Specificity | 80.0% | Healthy patients correctly identified |
| PPV | 93.3% | Precision when test is positive |
| NPV | 88.9% | Precision when test is negative |
| Accuracy | 92.3% | Overall correct classifications |

## Voice Biomarkers

- **Jitter** — cycle-to-cycle frequency variation (tremor indicator)
- **Shimmer** — amplitude variation between cycles
- **HNR** — harmonics-to-noise ratio (vocal clarity)
- **RPDE** — recurrence period density entropy (nonlinear dynamics)
- **DFA** — detrended fluctuation analysis (signal fractal scaling)

## Feature Engineering

- Jitter × Shimmer interaction
- HNR/NHR ratio
- Spread1 × Spread2 interaction
- RPDE × DFA interaction

## Stack

Python · XGBoost · Scikit-learn · SVM · Plotly · Pandas

## Files

- `notebooks/parkinsons_tremor_detector.ipynb` — full pipeline
- `outputs/feature_importance.csv` — top voice biomarkers
- `outputs/model_results.csv` — ROC-AUC comparison
- `outputs/predictions.csv` — patient predictions and risk scores
