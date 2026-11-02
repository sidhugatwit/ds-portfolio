# Project 24 — Parkinson's Tremor Detector (Voice Analysis)

> **Not medical advice or a medical device.** This is an educational data-science project. Its outputs are not a diagnosis and are not validated for clinical use.

## Overview

Detects Parkinson's disease from voice recordings using biomedical
voice measurements. Trains four classifiers on 22 voice features
including MDVP jitter, shimmer, HNR, RPDE, and DFA, and — critically —
validates at the **subject level**, because the dataset has 195 recordings
from only 32 people.

## Key Results

| Model | Random recording split (5-fold) | **Subject-grouped (5-fold)** |
|-------|------|------|
| Random Forest | 0.962 | **0.805 ± 0.042** |
| XGBoost | 0.965 | 0.754 ± 0.133 |
| Gradient Boosting | 0.963 | 0.696 ± 0.099 |
| SVM (RBF) | 0.897 | 0.633 ± 0.242 |

**Why two columns?** A random row split puts the same person's voice in
train and test, so models partly learn to recognise the *speaker*. Grouping
all of a subject's recordings into one fold (`StratifiedGroupKFold`) mimics
screening a new patient. The ~0.16 AUC gap is speaker leakage, not skill —
the subject-grouped column is the number to quote.

## Single holdout split (recording-level, for reference only)

XGBoost on a 39-recording holdout: ROC-AUC 0.990, sensitivity 96.6% (28/29),
specificity 80.0% (8/10). Optimistic for the reason above.

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
- `outputs/model_results.csv` — holdout ROC-AUC comparison
- `outputs/grouped_cv_results.csv` — recording-split vs subject-grouped CV
- `outputs/predictions.csv` — patient predictions and risk scores
