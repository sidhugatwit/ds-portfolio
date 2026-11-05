# Project 28 — PilotGPT v3: VFR & IFR Flight Assistant

> **Not for navigation or flight planning.** This is an educational project. Always use official FAA sources, current charts, and a certificated briefing for real flights.

## Overview

A LangGraph ReAct agent that answers preflight questions the way a flight instructor would check them:
every number comes from a tool, and every tool is tested against hand-worked examples.
Built by an FAA private pilot (300+ hours). Third version of PilotGPT (v2 is project 26).

## Tools

| Tool | What it does | Source of truth |
|------|-------------|-----------------|
| `airport_info` | Elevation, airspace class, entry rules, magnetic variation | FAA airport data, NOAA World Magnetic Model 2025 |
| `plan_leg` | Distance, true course, wind correction, magnetic heading, ground speed, time en route | Great-circle math, E6B wind triangle |
| `check_vfr` | Day VFR go/no-go for an airspace class and cruise altitude | 14 CFR 91.155 |
| `holding_entry` | Direct, teardrop or parallel entry and how to fly it | AIM 5-3-8 |
| `density_altitude` | Pressure and density altitude | FAA rule of thumb (118.8 ft per °C from ISA) |
| `live_metar` / `live_taf` | Current observation and forecast, decoded, with flight category | aviationweather.gov (NOAA), free and keyless |
| `web_search` (optional) | Background only, never weather or NOTAMs | SerpAPI, needs `SERPAPI_KEY` |

## What changed in v3.1

An audit of v3's aviation logic found errors a checkride examiner would catch. They are fixed and covered by tests:

- **Holding entries**: teardrop and parallel sectors were swapped and one boundary was off, so the demo question
  (inbound 090°, heading 200°) got "teardrop" instead of the correct parallel entry. The parallel entry also turned
  the wrong way back to the inbound course.
- **Magnetic heading**: a fixed 14° was subtracted. Boston's variation is about 14° West, which is added
  ("West is best"), so headings were about 28° off. Variation now comes from WMM2025 for each airport.
- **VFR check**: it ignored airspace class and cruise altitude, and called 1–3 SM in controlled airspace "marginal".
  It now applies the 91.155 table, the 500 ft-below-clouds rule, and the surface-area ceiling and visibility limits
  that require Special VFR.
- **Live weather**: v3 used Google search snippets. It now reads real METARs and TAFs from the Aviation Weather Center.
- **Density altitude**: ISA temperature is now taken at pressure altitude, not field elevation.
- **Map**: the third-party sectional tile URL had expired; the route map now uses OpenStreetMap.

## Run it

1. Set an OpenAI-compatible endpoint in the repo's `.env` (see `.env.example`; LM Studio with a local model works).
2. `uv run pytest -q` runs the 31 aviation tests (no network or LLM needed).
3. `uv run jupyter lab` and run `notebooks/pilotgpt_v3.ipynb`. The agent's answers are saved to
   `outputs/agent_run.json` with the name of the model that produced them.

## Stack

Python · LangGraph · LangChain · any OpenAI-compatible LLM · aviationweather.gov API · pygeomag (WMM2025) ·
Folium · pandas · pytest

## Files

- `src/aviation.py`: wind triangle, magnetic variation, density altitude, holding entries, VFR minimums
- `src/weather.py`: METAR/TAF from aviationweather.gov, optional SerpAPI search
- `src/airports.py`: demo airport table and airspace rules
- `tests/`: hand-worked checks for every calculation
- `notebooks/pilotgpt_v3.ipynb`: worked examples and the agent
- `outputs/`: holding entries, VFR scenarios, route map, agent run
