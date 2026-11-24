# ILS Glide Path

I simulated glide slope and localizer deviation so pilots and students can see how the geometry changes along an approach.

## Architecture

Approach geometry → generated aircraft positions → glide slope and localizer errors → trace and visualization.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/ils_glide_path.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**Simulated approach points** · 500. [Saved evidence](./outputs/approach_data.csv).

## Demo and deployment

TODO · Record a demo and verify any deployment. Capture a thumbnail from a real output or demo.

## Next steps

Record a visual walkthrough and compare the geometry against hand-worked cases.

## Implementation notes

> **Not for navigation or flight planning.** This is an educational project. Always use official FAA sources, current charts, and a certificated briefing for real flights.

## Overview
Mathematical model of an Instrument Landing System (ILS) approach 
derived from ICAO Annex 10 standards. Simulates aircraft deviation 
from the ideal glide slope with crosswind, turbulence, and pilot 
corrections — rendering a full 3D approach path and cockpit needle 
display, culminating in a CAT I decision height assessment.

## Methods
- **ILS Geometry** — Glide slope angle, DDM thresholds per ICAO Annex 10
- **GBM-style Simulation** — Crosswind drift + turbulence perturbations
- **CDI/GS Needle Display** — Deviation in dots across full final approach
- **CAT I Assessment** — LAND / GO AROUND decision at 200ft decision height

## Stack
Python · NumPy · SciPy · Plotly 3D

## Files
- `notebooks/ils_glide_path.ipynb` — full simulation
- `outputs/approach_data.csv` — full approach deviation dataset
