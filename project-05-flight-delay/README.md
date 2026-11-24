# Flight Delay Causal ML

I modeled how congestion, weather and carrier operations affect delay estimates in a seeded flight simulation.

## Architecture

Seeded flight simulator → causal graph and adjustment sets → effect estimation and refutation → saved effects.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/flight_delay_causal.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**Modeled congestion effect, simulated data** · 0.0968. [Saved evidence](./outputs/causal_effects.csv).

This is an estimate under the notebook’s assumptions. It is not a real-world causal validation.

## Demo and deployment

TODO · Record a demo and verify any deployment. Capture a thumbnail from a real output or demo.

## Next steps

Validate on an independent flight dataset and document causal assumptions and uncertainty before generalizing.

## Implementation notes

## Overview
Predicts and explains flight delays using a structural causal model 
built with DoWhy. Isolates the true causal effect of weather, NAS 
congestion, carrier issues, and late aircraft on delay probability — 
going beyond correlation to answer *why* flights are delayed.

> **Data:** 8,000 simulated flights generated in the notebook (seeded, so results reproduce exactly). Because the true causes are known, the analysis can check whether causal inference recovers them. A version on real BTS on-time data is planned.

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

## Files
- `notebooks/flight_delay_causal.ipynb` — full causal analysis
- `outputs/causal_effects.csv` — ATE per delay cause
- `outputs/feature_importance.csv` — GBM feature importances
- `outputs/flight_delay_dataset.csv` — full simulated dataset
