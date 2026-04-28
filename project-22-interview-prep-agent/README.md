# Project 22 — DS & AI Interview Prep Agent

## Overview

An AI-powered interview preparation system that analyzes a job description
against your resume, identifies skill gaps, selects tailored questions from
a 49-question bank across 9 domains, and scores your answers in real time
using GPT-4o-mini. Built as a Streamlit web app with SQLite session tracking
for progress monitoring over time.

## Features

- JD vs Resume analyzer with fit score (0-100)
- Skill gap identification and strength mapping
- 49 questions across 9 domains: ML, Deep Learning, Statistics, SQL,
  AI Safety, LLM Agents, MLOps, Finance, and Aviation DS
- Real-time rubric-based answer scoring
- Instant feedback with missing points and model answer hints
- SQLite session history for tracking improvement over time
- Historical progress chart across sessions

## How to Run

```bash
cd project-22-interview-prep-agent/src
streamlit run app.py
```

## Domains Covered

- Machine Learning (8 questions)
- Deep Learning (5 questions)
- Statistics & Probability (6 questions)
- SQL & Data Engineering (6 questions)
- AI Safety & Alignment (6 questions)
- LLM & Agentic Systems (6 questions)
- MLOps & Production (4 questions)
- Finance & Quantitative DS (4 questions)
- Aviation Data Science (4 questions)

## Stack

Python · OpenAI API · Streamlit · SQLite · Pandas · python-dotenv

## Files

- `notebooks/interview_prep_agent.ipynb` — full pipeline and analysis
- `src/app.py` — Streamlit interview app
- `data/sessions.db` — SQLite session history
- `outputs/latest_session.csv` — most recent session results