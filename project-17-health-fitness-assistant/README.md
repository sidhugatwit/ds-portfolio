# Project 17 — AI Health & Fitness Assistant

> **Not medical advice or a medical device.** This is an educational data-science project. Its outputs are not a diagnosis and are not validated for clinical use.

## Overview

Two vision-to-action pipelines: one turns a photo of your gym equipment into a weekly workout plan on
IBM watsonx.ai, the other turns a food photo into a nutrition estimate and a recipe with a local LLM.

## Pipeline 1 — AI Personal Trainer on IBM watsonx.ai (`Personal_Trainer_IBM_Watsonx.ipynb`)

Equipment photos → watsonx vision model lists the equipment → watsonx text model writes a weekly plan →
plan is checked against the equipment → printable HTML report

- Vision: Llama 4 Maverick on watsonx.ai, returning JSON (equipment, category, workout type)
- Planning: Llama 3.3 70B Instruct on watsonx.ai, returning a structured table parsed into a DataFrame
- **Equipment check:** every exercise is compared with the detected equipment, and any that need
  equipment you don't have (a common LLM mistake) are flagged
- **Plan checks:** right number of training days, at least 4 exercises per day, lower body and core covered
- **Human check:** vision models misread machines (Maverick once called a multi-press a "seated row
  machine"), so detected equipment can be corrected before planning; the original reading is kept
- Each run is saved to `outputs/trainer_run.json` with the models and region that produced it

An earlier version silently substituted a hard-coded equipment description whenever the vision call
failed, so its saved run never showed real vision output. That fallback is gone: failures now stop with
the model's actual reply.

## Pipeline 2 — Agentic Food Analyzer (`MultiAgent.ipynb`)

Food photo → CLIP zero-shot ingredient detection → nutrition estimate from a small database →
recipe from a local LLM (LM Studio) → Gradio UI

## Models

| Where | Model | Task |
|-------|-------|------|
| IBM watsonx.ai | Llama 4 Maverick 17B (vision) | Gym equipment detection |
| IBM watsonx.ai | Llama 3.3 70B Instruct | Workout plan |
| Local (Hugging Face) | CLIP ViT-B/32 | Food detection |
| Local (LM Studio) | Any chat model, e.g. Qwen3.6 | Recipe generation |

watsonx models are set with `WATSONX_TEXT_MODEL` and `WATSONX_VISION_MODEL`; IBM retires models regularly.

## Run it

1. In the repo's `.env`: `WATSONX_APIKEY`, `WATSONX_PROJECT_ID`, `WATSONX_URL` (see `.env.example`).
   A watsonx.ai Runtime Lite plan is enough.
2. Put one or more equipment photos in `data/gym/`. The folder is git-ignored, so product photos you
   don't own stay out of the repo.
3. `uv run jupyter lab` in this folder.

## Stack

Python · IBM watsonx.ai · Llama · CLIP · Gradio · pandas · python-dotenv

## Files

- `notebooks/Personal_Trainer_IBM_Watsonx.ipynb`: watsonx personal trainer
- `notebooks/MultiAgent.ipynb`: food analyzer with Gradio UI
