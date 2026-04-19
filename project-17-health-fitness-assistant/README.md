# Project 17 — AI Health & Fitness Assistant

## Overview

A multi-provider AI health assistant combining two specialized pipelines
into one unified system. Uses three different AI providers — Gemma 4
(local via Ollama), IBM Watsonx (Llama vision), and OpenAI — for food
analysis, nutrition tracking, recipe generation, and personalized
workout planning from gym equipment photos.

## Two Pipelines

### Pipeline 1 — Agentic Food Analyzer (MultiAgent.ipynb)

Food Photo → Vision Agent → Nutrition Agent → Recipe Agent → Gradio UI

- Upload a food photo → detect top-3 ingredients
- Estimate macros and calories per ingredient with totals
- Generate a personalized recipe based on dietary preferences
- Adjustable servings (1-6) and calorie targets (200-1200)
- Full Gradio web interface with live share link

### Pipeline 2 — AI Personal Trainer (Personal_Trainer_IBM_Watsonx.ipynb)

Gym Equipment Photo → Watsonx Llama Vision → Workout Planner → HTML Export

- Upload gym equipment photo → IBM Watsonx identifies equipment
- Llama 3.3 70B generates a personalized weekly workout plan
- Structured pipe-delimited output parsed into a DataFrame
- Exports a print-ready HTML workout plan with daily tables

## AI Providers Used

| Provider | Model | Task |
|----------|-------|------|

| IBM Watsonx | Llama 3.2 11B Vision | Gym equipment detection |
| IBM Watsonx | Llama 3.3 70B Instruct | Workout plan generation |
| OpenAI / Gradio | Vision + LLM | Food detection and recipe generation |
| Local (Ollama) | Gemma 4 | Upgrade path for vision layer |

## Key Concepts

- **Multi-provider orchestration** — three AI providers in one system
- **Vision-to-action pipelines** — image input drives structured outputs
- **Structured output parsing** — pipe-delimited LLM output → DataFrame
- **HTML report generation** — printable workout plans from AI output
- **Gradio UI** — interactive web interface for food pipeline

## Stack

Python · IBM Watsonx AI · Gradio · PIL · Pandas · HuggingFace ·
python-dotenv · OpenAI API

## Target Companies

IBM · Amazon Health · Meta · Anthropic · Perplexity

## Files

- `notebooks/MultiAgent.ipynb` — agentic food analyzer with Gradio UI
- `notebooks/Personal_Trainer_IBM_Watsonx.ipynb` — IBM Watsonx personal trainer
  