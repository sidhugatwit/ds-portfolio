# Project 04 — ILS Glide Path & Localizer Deviation Model

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

## Target Companies
Delta Airlines · United Airlines

## Files
- `notebooks/ils_glide_path.ipynb` — full simulation
- `outputs/approach_data.csv` — full approach deviation dataset