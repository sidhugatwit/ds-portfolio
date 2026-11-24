# Agentic SQL

I built a natural-language SQL workflow and saved example results for questions across aviation and finance.

## Architecture

Analyst question → pattern-based SQL translation → DuckDB execution → result tables and plots.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/agentic_sql_analyst.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**Saved query result sets** · 5. [Saved evidence](./outputs).

## Demo and deployment

TODO · Record a demo and verify any deployment. Capture a thumbnail from a real output or demo.

## Next steps

Add a labeled execution-accuracy benchmark and record a walkthrough.

## Implementation notes

## Overview
An AI agent that translates plain English questions into verified SQL 
queries, executes them against a multi-table operational database, 
visualizes results, and explains findings in plain language. Built on 
a DuckDB in-memory database with 15,000+ rows across flight operations 
and financial transactions domains.

## Methods
- **NL-to-SQL Engine** — pattern-based translator mapping analyst 
  questions to optimized SQL queries
- **Agentic Loop** — generate → execute → validate → explain pipeline
- **Dual Domain DB** — flights (5,000 rows) + transactions (10,000 rows)
- **Auto-Visualization** — Plotly dashboards generated per query result

## Key Questions Answered
- Which airline has the highest average delay?
- What are the most expensive fuel routes?
- Which airport has the most traffic?
- What are fraud rates by spending category?
- What is total spending by merchant?

## Stack
Python · DuckDB · Pandas · Plotly · JSON

## Files
- `notebooks/agentic_sql_analyst.ipynb` — full agent pipeline
- `outputs/schema.json` — database schema summary
- `outputs/*.csv` — query results per analyst question
