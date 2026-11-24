# Parkinson’s Voice

I compared recording-level and speaker-grouped validation to see how much repeated speakers inflated performance.

## Architecture

Voice features → group recordings by speaker → classifier cross-validation → compare with recording-level splits.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/parkinsons_tremor_detector.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**Random forest mean speaker-grouped ROC-AUC** · 0.805. [Saved evidence](./outputs/grouped_cv_results.csv).

The headline uses groups by speaker, the relevant split for evaluating unseen people. The project is educational.

## Demo and deployment

TODO · Record a demo and verify any deployment.

## Next steps

Validate on independent participants. Keep the diabetes model as a separate companion study.

## Companion projects

- [project-23-diabetes-risk-predictor](../archive/project-23-diabetes-risk-predictor)

The companion experiments remain independently reproducible.

## Implementation notes

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
