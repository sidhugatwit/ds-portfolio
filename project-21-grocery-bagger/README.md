# Project 21 — Grocery Bagger: Bin Packing Optimization

## Overview

A data science extension of a Java grocery bagger built in COMP 2000.
The bin packing problem — packing groceries into minimum bags without
exceeding weight capacity — is NP-Hard, making algorithm choice critical.
Three algorithms are implemented and benchmarked: First Fit, First Fit
Decreasing, and a custom Fragile-First approach mirroring the original
Java logic.

## Original Java Project

Built in Eclipse as a group project for COMP 2000. Source code cloned
from the team repository at github.com/identithree/grocery-bagger.
Handles item weights, fragile item constraints, and optimal bag assignment.

## Bin Packing Algorithms

| Algorithm | Bags Used | Efficiency | Notes |
|-----------|-----------|------------|-------|
| First Fit | 3 | 71.1% | Greedy — first available bag |
| First Fit Decreasing | 3 | 71.1% | Sort by weight first |
| Fragile First | 3 | 71.1% | Safety-aware — mirrors Java logic |

## Key Finding

All three algorithms reach the mathematically optimal solution of 3 bags
for this item set — confirming that the Java implementation was already
near-optimal. The Fragile First algorithm adds a safety constraint
ensuring fragile items are never crushed by heavy items.

## Problem Complexity

The bin packing problem is NP-Hard — no polynomial time exact solution
exists for large inputs. The approximation algorithms implemented here
achieve optimal results for realistic grocery orders while running in O(n²).

## Stack

Python · NumPy · Pandas · Plotly · Java (original Eclipse implementation)

## Files

- `notebooks/grocery_bagger_analysis.ipynb` — full optimization analysis
- `slides/Project_1_-_Grocery_Bagger_-_Presentation.pptx` — COMP 2000 presentation
- `src/grocery-bagger/` — original Java source code (cloned from team repo)
- `outputs/algorithm_comparison.csv` — efficiency metrics per algorithm
- `outputs/grocery_items.csv` — item weights and fragile flags
