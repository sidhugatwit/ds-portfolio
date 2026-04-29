# Project 27 — Recipe Maker with Gemma 4 Vision

## Overview

A multi-model AI pipeline that takes a food photo, detects ingredients
using Gemma 4 vision (local inference), generates a complete recipe with
nutrition information using GPT-4o-mini, and produces a professional
plated food photo using DALL-E 3.

## Pipeline

Food Photo Input
→ Gemma 4 Vision (local, 9.6GB) — ingredient detection
→ GPT-4o-mini — recipe + nutrition generation
→ DALL-E 3 — professional food photo generation

## Sample Result

**Input:** Salad bowl photo
**Gemma 4 detected:** Lettuce, Avocado, Cherry Tomatoes, Yellow Bell
Pepper, Beetroot, Purple Cabbage, Chickpeas, Sweet Potato,
Sprouts, Dressing
**Recipe generated:** Mediterranean Chickpea Salad with Roasted Sweet Potato
**Cuisine:** Mediterranean / Plant-based
**DALL-E output:** Professional restaurant-quality plated photo

## AI Models Used

| Model | Provider | Task |
|-------|----------|------|
| Gemma 4 (9.6GB) | Local via Ollama | Food ingredient detection |
| GPT-4o-mini | OpenAI API | Recipe + nutrition generation |
| DALL-E 3 | OpenAI API | Professional food photo |

## Features

- Local vision inference — no cloud cost for detection
- Complete recipe with ingredients, instructions, and nutrition
- Chef tips and wine pairing suggestions
- DALL-E 3 restaurant-quality food photography
- Supports any dietary preference (vegetarian, vegan, etc.)

## Stack

Python · Gemma 4 · Ollama · OpenAI API · DALL-E 3 · Pillow · Pandas

## Files

- `notebooks/recipe_maker.ipynb` — full pipeline
- `outputs/recipe.json` — generated recipe
- `outputs/detected_ingredients.csv` — Gemma 4 detection results
- `outputs/generated_food_photo.jpg` — DALL-E 3 food photo
- `data/sample_food.jpg` — input test image
