# Project 25 — Anxiety & Isolation Sentiment Tracker

## Overview

A zero-shot NLP classifier that detects anxiety, isolation, depression,
and neutral mental states from text posts — no labeled training data
required. Uses Facebook's BART-large-MNLI model for inference and
simulates a 30-day longitudinal mental health tracking journey showing
progression from acute anxiety through depression, isolation, and recovery.

## Key Results

| Metric | Value |
|--------|-------|
| Overall accuracy | 68.75% (zero-shot, no training) |
| Dataset | 48 curated mental health posts across 4 labels |
| Model | facebook/bart-large-mnli (zero-shot) |
| Longitudinal tracking | 30-day simulated journey |

## Key Finding

Depression and isolation labels are frequently confused — clinically
meaningful since both conditions co-occur and share linguistic markers
(withdrawal, hopelessness, low energy). High-confidence misclassifications
suggest genuine semantic overlap rather than model failure.

## Pipeline

1. Zero-shot classification — no fine-tuning, labels as natural language
2. Confidence analysis — per-label accuracy and misclassification review  
3. Confusion matrix — cross-label semantic overlap visualization
4. Longitudinal tracking — 30-day mental state trajectory simulation
5. Weekly rollup — dominant state per week across recovery arc

## Clinical Note

This project is for research and educational purposes only. If you or
someone you know is experiencing mental health difficulties, please
contact a qualified healthcare professional or crisis line.

## Stack

Python · HuggingFace Transformers · BART-large-MNLI · Plotly · Pandas

## Files

- `notebooks/anxiety_sentiment_tracker.ipynb` — full pipeline
- `outputs/classification_results.csv` — zero-shot results per post
- `outputs/longitudinal_tracking.csv` — 30-day tracking data
