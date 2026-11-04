# Project 20 — BlackJack to Five: Probability Analysis & Optimal Strategy

## Overview

An extension of a Java card game built in COMP 2000
(Data Structures). The original BlackJack-to-Five game — first player
to 5 round victories wins — is translated to Python and analyzed with
10,000 Monte Carlo simulations, exact bust probabilities, and dynamic
programming to find the optimal hit/stand strategy, validated by simulation.

## Original Java Project

Built in Eclipse as a group project for COMP 2000 with Will Weeks
and Troy Gayle. Features rotating dealer, CPU-controlled players,
automatic ace handling (hard→soft), and house-advantage tie rules.

## Data Science Layer

| Analysis | Method | Finding |
|----------|--------|---------|
| Win rates | Monte Carlo, 10,000 full games (seed 42) | Player who deals first wins 39.2% — ties go to the dealer |
| Game length | Simulation | Average 9.7 rounds to reach 5 wins |
| Bust probability | Exact calculation | 30.8% when hitting hard 12, 92.3% at hard 20 |
| Optimal strategy | Dynamic programming (Bellman equation) | Optimal policy wins 42.5% of rounds |
| Validation | Monte Carlo, 100,000 hands, common random numbers | Every strategy within its 95% CI of the DP model |

## Key Findings

- **The best simple rule is "hit below 14," not "hit below 17."** In this game the player
  never sees the dealer's cards, and the dealer busts 28.2% of the time, so standing on
  14 or more wins more often (41.8%) than the casino-style "hit below 17" (40.8%).
- **The full DP policy does better still: 42.5%.** Stand on hard 14+, but keep hitting
  soft hands (an ace counted as 11) up to 18, because a soft hand can't bust on one card.
- On the real 52-card deck, the optimal policy beats "hit below 17" by **+1.8 points
  (95% CI ±0.23)**, measured on identical shuffles.

## What changed from the first version

The first version searched thresholds with 5,000 random games each and picked the
highest score. With roughly ±0.7 points of noise per estimate, the "winner" was partly
luck (the *winner's curse*): its threshold scored 42.6% in the search but 40.1% when
re-tested. It also counted an ace as 11 in the bust table, which inflated every bust
rate (e.g. 100% at 20 instead of 92.3%), and it was unseeded. This version replaces the
search with an exact dynamic program, fixes the ace logic, seeds every run, and checks
the model against simulation with confidence intervals.

## Stack

Python · NumPy · Pandas · Plotly · Java (original Eclipse implementation)

## Files

- `notebooks/blackjack_analysis.ipynb` — full probability analysis
- `slides/BlackJack_To_Five_Presentation.pptx` — COMP 2000 presentation
- `outputs/simulation_results.csv` — 10K Monte Carlo results
- `outputs/bust_probabilities.csv` — bust rate per hand value
- `outputs/strategy_optimization.csv` — exact win probability for each fixed threshold
- `outputs/optimal_policy.csv` — DP hit/stand decision for every hard and soft total
- `outputs/strategy_comparison.csv` — five strategies: simulated win rate, 95% CI and DP model
