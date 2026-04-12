# Project 06 — Great Circle Routing & Fuel Optimization

## Overview
Implements Haversine and Vincenty great circle formulas to compute 
optimal flight routes between major international airports. Models 
wind-corrected fuel burn across three aircraft types and checks ETOPS 
regulatory compliance for twin-engine overwater operations.

## Methods
- **Haversine Formula** — Great circle distance and initial bearing
- **GC Arc Visualization** — Interpolated route points on a world map
- **Wind-Corrected Fuel Burn** — Headwind/tailwind impact on B737, B777, A320
- **ETOPS Compliance** — Diversion radius checks at 60/120/180 minute ratings

## Key Results
- BOS→LHR tailwind saves significant fuel vs headwind routing
- ETOPS-180 provides full transatlantic coverage with North Atlantic alternates
- Great circle routes arc far north — visually counter-intuitive but mathematically optimal

## Stack
Python · NumPy · Plotly · Pandas

## Target Companies
Delta Airlines · United Airlines

## Files
- `notebooks/great_circle_routing.ipynb` — full analysis
- `outputs/route_analysis.csv` — distance, time, fuel per route