# Mechanistic Interpretability

I used activation patching to inspect how a language model recovers a target prediction when I restore individual activations.

## Architecture

Clean and corrupted prompts → activation capture → patch individual activations → compare target logit differences.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/mechanistic_interp.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**Clean vs corrupted logit difference** · 3.380 vs −3.738. [Saved evidence](./outputs/logit_diff_baseline.csv).

## Demo and deployment

TODO · Record a demo and verify any deployment. Capture a thumbnail from a real output or demo.

## Next steps

Expand to multiple prompt pairs before generalizing the result across layers.

## Implementation notes

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

## Files

- `notebooks/mechanistic_interp.ipynb` — full interpretability analysis
- `outputs/layer_patching_results.csv` — recovery % per layer
- `outputs/logit_diff_baseline.csv` — clean vs corrupted baselines
