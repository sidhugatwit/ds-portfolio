# Project 23 — Type 2 Diabetes Risk Predictor

## Overview

End-to-end diabetes risk prediction system trained on the Pima Indians
Diabetes dataset. Handles biologically impossible zero values in medical
features, engineers 5 clinically meaningful features, and trains XGBoost
and Random Forest classifiers. Assigns patients to Low/Moderate/High risk
tiers with personalized lifestyle intervention recommendations.

## Key Results

| Model | ROC-AUC |
|-------|---------|
| XGBoost | 0.8220 |
| Random Forest | see outputs/ |

## Methods

- **Data Cleaning** — Zero imputation for glucose, BMI, insulin, blood
  pressure using median substitution (biologically impossible zeros)
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