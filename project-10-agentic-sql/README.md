# Project 10 — Agentic SQL Analyst with Natural Language Interface

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

## Target Companies
Fidelity · Capital One · Delta · United · Amazon

## Files
- `notebooks/agentic_sql_analyst.ipynb` — full agent pipeline
- `outputs/schema.json` — database schema summary
- `outputs/*.csv` — query results per analyst question