# Project 23 — Type 2 Diabetes Risk Predictor

> **Not medical advice or a medical device.** This is an educational data-science project. Its outputs are not a diagnosis and are not validated for clinical use.

## Overview

End-to-end diabetes risk prediction system trained on the Pima Indians
Diabetes dataset. Handles biologically impossible zero values in medical
features, engineers 5 clinically meaningful features, and trains XGBoost
and Random Forest classifiers. Assigns patients to Low/Moderate/High risk
tiers with personalized lifestyle intervention recommendations.

## Key Results

| Model | Holdout ROC-AUC | 5-fold CV ROC-AUC |
|-------|-----------------|-------------------|
| XGBoost | 0.822 | 0.829 ± 0.026 |
| Random Forest | 0.810 | 0.840 ± 0.020 |

## Methods

- **Data Cleaning** — Biologically impossible zeros (glucose, BMI, insulin,
  blood pressure, skin thickness) treated as missing; medians learned on the
  training split only (and per fold in CV) so no test statistics leak
- **Feature Engineering** — BMI×Age interaction, Glucose×Insulin,
  High_Glucose flag, Obese flag, High_Risk_Age flag
- **XGBoost** — Gradient boosted classifier with 200 estimators
- **Risk Tiering** — Low (<30%), Moderate (30-60%), High (>60%)
  predicted probability
- **Interventions** — Clinically grounded lifestyle recommendations
  per risk tier

## Top Predictive Features

Glucose, BMI, Age, DiabetesPedigreeFunction, and engineered interaction
features rank highest — consistent with clinical literature on diabetes risk.

## Stack

Python · XGBoost · Scikit-learn · Plotly · Pandas · NumPy

## Files

- `notebooks/diabetes_risk_predictor.ipynb` — full pipeline
- `outputs/feature_importance.csv` — RF feature rankings
- `outputs/risk_scores.csv` — patient risk scores and tiers
- `outputs/model_results.csv` — ROC-AUC comparison