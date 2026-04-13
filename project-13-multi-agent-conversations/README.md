# Project 13 — Multi-Agent Conversations with GPT-4o-mini

## Overview

Implements multi-agent conversation systems where multiple GPT-4o-mini
instances simulate distinct personas engaging in realistic dialogue.
Each agent has its own role instruction, personality, and communication
style while sharing a common conversation history — demonstrating
stateful multi-agent architecture using the OpenAI API.

## Simulations

### 1. Father & Son — Parking Dispute

Two-agent simulation where a frustrated father and an empathetic son
navigate a recurring household conflict. Demonstrates turn-based
agent dialogue with role-specific system prompts.

### 2. Father, Mother & Son — Motorcycle Purchase

Three-agent simulation of a family negotiation. Each agent has distinct
goals: the son wants independence, the mother prioritizes safety, and
the father seeks compromise. Demonstrates multi-stakeholder agent
orchestration with fallback model handling.

## Key Concepts

- **Role-based system prompts** — each agent has a distinct persona
- **Shared conversation history** — all agents see the full dialogue
- **Turn orchestration** — structured turn order across multiple agents
- **Fallback handling** — automatic retry with secondary model on failure
- **Stateful context** — conversation state passed across all turns

## Stack

Python · OpenAI API (GPT-4o-mini) · python-dotenv

## Target Companies

Meta · Amazon · Perplexity · Anthropic

## Files

- `notebooks/father-son-agents.ipynb` — 2-agent parking dispute
- `notebooks/father-mother-son-motorcycle.ipynb` — 3-agent family negotiation
