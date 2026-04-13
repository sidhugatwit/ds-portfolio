# Project 14 — Geometric Brownian Motion: Simulating Asset Prices

## Overview

Simulates future stock price paths for SanDisk (SNDK) and ASML Holding
(ASML) using Geometric Brownian Motion — the mathematical engine behind
the Black-Scholes options pricing model. Derives the GBM solution from
first principles using Itô's Lemma and estimates real drift and volatility
parameters from historical market data.

## Mathematical Foundation

Starting from the stochastic differential equation:

dS_t = μ S_t dt + σ S_t dW_t

Applying Itô's Lemma yields the closed-form solution:

S_t = S_0 * exp[(μ - σ²/2)t + σW_t]

The σ²/2 term is the Itô correction arising from the convexity
of the exponential function.

## What's Covered

- Wiener process axioms and properties
- GBM SDE derivation and Itô's Lemma solution
- Parameter estimation (μ, σ) from historical SNDK and ASML data
- Monte Carlo simulation — 500 paths over 3-year horizon
- Black-Scholes-Merton European call option pricing
- Greeks — Delta calculation and interpretation
- Limitations of GBM and extensions (Heston, Jump-Diffusion, SABR)

## Key Results

| Metric | SNDK | ASML |
| ------- | ------ | ------ |
| Annualised Drift (μ) | see notebook | see notebook |
| Annualised Volatility (σ) | see notebook | see notebook |
| Prob(Price > S₀) in 3 years | 100.0% | 64.8% |
| 95th Percentile Price | $13,171,799 | $7,177 |

## Stack

Python · NumPy · SciPy · Matplotlib · yfinance

## Target Companies

Fidelity · Capital One · Chase · Anthropic

## Relation to Portfolio

This project is the mathematical foundation for Project 03
(Portfolio Optimizer), which extends GBM simulation to 10 assets
with Markowitz optimization and full Black-Scholes Greeks dashboard.

## Files

- `notebooks/Geometric_Brownian_Motion_-_Simulating_Asset_price.ipynb` — full analysis
- `notebooks/Project_-_Geometric_Brownian_Motion.docx` — written report
