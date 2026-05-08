# Project 28 — PilotGPT v3: VFR & IFR Flight Assistant

## Overview

Expanded PilotGPT with full VFR capabilities alongside the IFR suite from v2.
Built by an IFR-rated pilot — all aviation mathematics derived from FAA standards.
LangGraph ReAct agent with 7 tools providing comprehensive flight assistance for both VFR and IFR operations.

## New in v3 vs v2

- VFR airspace classification (Class A/B/C/D/E/G)
- VFR weather go/no-go checker with legal minimums
- Interactive FAA VFR sectional chart (Folium + FAA tile server)
- Live weather and NOTAM lookup via SerpAPI
- Airport database expanded with airspace class

## 7 Agent Tools

| Tool | Description |
|------|-------------|
| `get_airspace_info` | VFR requirements per airspace class |
| `check_vfr_conditions` | Go/no-go based on visibility and ceiling |
| `calculate_holding_entry` | Direct/teardrop/parallel IFR entry |
| `calculate_wind_correction` | E6B wind triangle solution |
| `calculate_density_altitude_tool` | Performance planning |
| `get_live_weather` | Live METAR via SerpAPI |
| `get_airport_details` | Airport info with airspace class |

## VFR Airspace Rules Implemented

| Class | Clearance | Visibility | Cloud Clearance |
|-------|-----------|------------|-----------------|
| B | ATC clearance | 3 SM | Clear of clouds |
| C | Radio contact | 3 SM | 500/1000/2000 |
| D | Radio contact | 3 SM | 500/1000/2000 |
| E | None | 3 SM | 500/1000/2000 |
| G | None | 1 SM | Clear of clouds |

## IFR Features (from v2)

- E6B wind correction, TAS, ground speed
- Holding pattern entry (direct/teardrop/parallel)
- Density altitude from OAT and altimeter
- Full IFR flight plan generation

## Stack

Python · LangGraph · LangChain · GPT-4o-mini · Folium ·
SerpAPI · NumPy · Pandas

## Files

- `notebooks/pilotgpt_v3.ipynb` — full VFR & IFR suite
- `outputs/vfr_sectional_map.html` — interactive FAA sectional chart
- `outputs/airport_database.csv` — airport info with airspace class
- `outputs/airspace_classification.csv` — VFR rules per airport
- `outputs/vfr_scenarios.csv` — weather go/no-go scenarios
