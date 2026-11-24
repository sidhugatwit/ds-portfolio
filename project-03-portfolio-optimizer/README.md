# Portfolio Optimizer

I used simulation and constrained optimization to explore the return and volatility tradeoffs in a portfolio.

## Architecture

Asset prices → return and covariance estimates → allocation simulation and constrained optimization → frontier and weights.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/portfolio_optimizer.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**Max Sharpe, in-sample** · 1.3912. [Saved evidence](./outputs/summary.json).

The saved figure is in-sample and does not estimate future performance.

## Demo and deployment

TODO · Record a demo and verify any deployment. Capture a thumbnail from a real output or demo.

## Next steps

Add held-out evaluation and transaction-cost assumptions. Preserve the earlier GBM notebook as a companion experiment.

## Companion projects

- [project-14-gbm-sandisk-asml](../archive/project-14-gbm-sandisk-asml)
- TODO · Locate project 34 source.

The companion experiments remain independently reproducible.

## Implementation notes

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

## Files
- `notebooks/portfolio_optimizer.ipynb` — full analysis
- `outputs/asset_statistics.csv` — annualized return, vol, Sharpe per asset
- `outputs/optimal_weights.csv` — Max Sharpe & Min Vol allocations
- `outputs/summary.json` — key metrics for portfolio website
