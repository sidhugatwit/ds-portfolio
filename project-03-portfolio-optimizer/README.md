# Project 03 — Portfolio Optimizer with Monte Carlo & Black-Scholes

## Overview
Multi-asset portfolio optimizer using Markowitz mean-variance theory, 
10,000 Monte Carlo simulations, and Black-Scholes-Merton options pricing 
across 10 assets spanning tech, finance, and market benchmarks.

## Key Results
| Portfolio | Annual Return | Volatility | Sharpe Ratio |
|-----------|--------------|------------|--------------|
| Max Sharpe | see outputs/ | see outputs/ | see outputs/ |
| Min Volatility | see outputs/ | see outputs/ | — |

## Methods
- **Efficient Frontier** — 10,000 randomly sampled portfolios via Monte Carlo
- **GBM Simulation** — Geometric Brownian Motion price paths using Itô's Lemma
- **SciPy Optimization** — SLSQP solver for exact Max Sharpe & Min Vol portfolios
- **Black-Scholes-Merton** — Options pricing + Greeks (Delta, Gamma, Theta, Vega)

## Stack
Python · NumPy · SciPy · Plotly · yfinance

## Target Companies
Fidelity · Capital One · Chase

## Files
- `notebooks/portfolio_optimizer.ipynb` — full analysis
- `outputs/asset_statistics.csv` — annualized return, vol, Sharpe per asset
- `outputs/optimal_weights.csv` — Max Sharpe & Min Vol allocations
- `outputs/summary.json` — key metrics for portfolio website