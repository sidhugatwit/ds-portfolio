# Project 26 — PilotGPT v2: IFR Full Suite

> **Not for navigation or flight planning.** This is an educational project. Always use official FAA sources, current charts, and a certificated briefing for real flights.

## Overview

A complete IFR flight planning and training system powered by a LangGraph
ReAct agent with GPT-4o-mini. Built by an FAA private pilot (300+ hours) from first
principles — all aviation mathematics derived from FAA standards with no
external aviation libraries. Covers holding pattern entries, E6B wind
correction, density altitude, and full IFR flight plan generation.

## Features

### IFR Mathematics Engine

- **E6B Wind Correction** — WCA, ground speed, magnetic heading
- **Density Altitude** — from elevation, OAT, and altimeter setting
- **TAS from CAS** — altitude and temperature corrected
- **Fuel & Time** — enroute fuel, 45-minute IFR reserve
- **Great Circle Routing** — Haversine distance and initial bearing

### Holding Pattern Calculator

- **Direct entry** — 0-70° and 290-360° relative bearing zones
- **Teardrop entry** — 71-180° zone with 30° offset outbound
- **Parallel entry** — 181-290° zone with parallel outbound leg
- **Timing** — 1 min below 14,000 ft, 1.5 min above, wind corrected

### IFR Flight Plan Generator

Complete FAA-style flight plans including:

- True course, magnetic heading, wind correction
- Ground speed, estimated time enroute
- Enroute fuel + 45-minute IFR alternate reserve
- Density altitude at departure

### PilotGPT AI Agent

LangGraph ReAct agent with 5 tools:

- `calculate_holding_entry` — holding pattern entry type and procedure
- `calculate_wind_correction` — E6B wind triangle solution
- `calculate_density_altitude` — performance planning
- `generate_ifr_flight_plan` — complete IFR plan
- `get_airport_info` — airport database lookup

## Sample Output

KBOS → KATL at 10,000 ft
Distance:      821.3 NM
Magnetic HDG:  228.8°
Ground Speed:  120.3 kts
Est Time:      6h 49m
Total Fuel:    68.2 gal

## Stack

Python · LangGraph · LangChain · GPT-4o-mini · NumPy · Pandas · Plotly

## Files

- `notebooks/pilotgpt_v2.ipynb` — full IFR suite
- `outputs/flight_plans.csv` — sample IFR flight plans
- `outputs/holding_pattern_entries.csv` — holding entry calculations

## Known issues (fixed in v3.1, project 28)

This version's holding-entry sectors swap teardrop and parallel, and its magnetic heading subtracts Boston's
West variation instead of adding it. Both are corrected and tested in
[DirectTo](../project-28-pilotgpt-v3/) (project 28, formerly PilotGPT v3). The saved outputs here are kept as a record of v2.
