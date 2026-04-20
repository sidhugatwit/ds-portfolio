# Project 20 — BlackJack to Five: Probability Analysis & Optimal Strategy

## Overview

An extension of a Java card game built in COMP 2000
(Data Structures). The original BlackJack-to-Five game — first player
to 5 round victories wins — is translated to Python and analyzed with
10,000 Monte Carlo simulations, bust probability tables, and dynamic
programming to find the optimal hit/stand strategy.

## Original Java Project

Built in Eclipse as a group project for COMP 2000 with Will Weeks
and Troy Gayle. Features rotating dealer, CPU-controlled players,
automatic ace handling (hard→soft), and house-advantage tie rules.

## Data Science Layer

| Analysis | Method | Finding |
|----------|--------|---------|
| Win rates | Monte Carlo (10K games) | Dealer wins 39.5% — house advantage confirmed |
| Game length | Simulation | Average 9.7 rounds to reach 5 wins |
| Bust probability | Probabilistic simulation | 100% bust rate at hand value 20 |
| Optimal strategy | Dynamic programming | See outputs/ |

## Key Findings

- Dealer position wins 39.5% vs Player 1 at 32.9% and Player 2 at 27.7%
- Bust probability climbs from 39% at 12 to 100% at 20
- Dynamic programming identifies the optimal hit threshold
- Conservative strategy (hit below 17) matches standard casino basic strategy

## Stack

Python · NumPy · Pandas · Plotly · Java (original Eclipse implementation)

## Files

- `notebooks/blackjack_analysis.ipynb` — full probability analysis
- `slides/BlackJack_To_Five_Presentation.pptx` — COMP 2000 presentation
- `outputs/simulation_results.csv` — 10K Monte Carlo results
- `outputs/bust_probabilities.csv` — bust rate per hand value
- `outputs/strategy_optimization.csv` — DP strategy sweep
- `outputs/strategy_comparison.csv` — four strategy head-to-head
