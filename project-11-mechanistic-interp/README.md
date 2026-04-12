# Project 11 — Mechanistic Interpretability of GPT-2 Medium

## Overview

Applies mechanistic interpretability techniques to GPT-2 Medium (345M
parameters) to identify the internal circuits responsible for the
Indirect Object Identification (IOI) task — the same task studied in
Anthropic's landmark 2022 interpretability paper. Uses activation
patching to causally identify which layers and attention heads encode
the IOI circuit.

## Key Finding

Activation patching reveals that **layers 0, 1, and 2** achieve 100%
logit difference recovery on the IOI task — meaning the indirect object
circuit is encoded in the very earliest layers of GPT-2 Medium. This is
a genuine mechanistic finding consistent with Anthropic's research showing
that factual recall circuits are localized in early-to-mid layers.

## Factual Accuracy Upgrade

GPT-2 Medium correctly predicts **Paris** (logit: 20.47) as the top
token for "The Eiffel Tower is located in the city of" — significantly
outperforming GPT-2 Small which predicted London, demonstrating the
importance of model scale for factual knowledge.

## Methods

- **TransformerLens** — Anthropic-developed library for mechanistic
  interpretability of transformer models
- **Attention Pattern Analysis** — Visualizes all 16 heads across
  24 layers on the IOI prompt
- **Activation Patching** — Patches residual stream from clean to
  corrupted prompt to find causally important layers
- **Logit Difference** — Measures model preference for correct vs
  incorrect indirect object across all layers

## Model

| Property | Value |
|----------|-------|
| Model | GPT-2 Medium |
| Parameters | 345M |
| Layers | 24 |
| Attention Heads | 16 |
| d_model | 1024 |

## IOI Task Results

| Prompt Type | Logit Diff (Mary - John) |
|-------------|--------------------------|
| Clean | 3.3796 |
| Corrupted | see outputs/ |
| Top recovery layers | 0, 1, 2 (100% each) |

## Stack

Python · TransformerLens · PyTorch · Einops · Plotly · Pandas

## Target Companies

Anthropic · OpenAI · DeepMind · Redwood Research · METR

## Files

- `notebooks/mechanistic_interp.ipynb` — full interpretability analysis
- `outputs/layer_patching_results.csv` — recovery % per layer
- `outputs/logit_diff_baseline.csv` — clean vs corrupted baselines
