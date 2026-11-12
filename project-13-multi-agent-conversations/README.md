# Project 13 — Multi-Agent Conversations

## Overview

Role-played conversations between LLM agents, with each agent's view of the conversation built correctly and every
turn checked. Two scenes: a father and son settling a parking dispute, and a father, mother and son deciding on a
motorcycle purchase. Runs on any OpenAI-compatible model (LM Studio with a local model works).

## How it works

- **Per-agent perspective.** Each agent sees its own past lines as its own (`assistant`) and everyone else's as
  `user` messages labelled with the speaker's name. The first version gave all agents one shared history, so an
  agent saw other people's lines as its own and the father's prompts arrived as the son's.
- **Turn checks.** Every reply is checked for an agent writing lines for someone else ("MOTHER: ..." inside the
  son's turn), a common failure in multi-agent role-play. Reasoning blocks and stray name prefixes are removed.
- **Outcome as data.** A neutral moderator states whether they agreed, the agreed terms and the open issues, as JSON.
- Each run is saved to `outputs/` with the model that produced it.

## Run it

1. Set an LLM endpoint in the repo's `.env` (see `.env.example`).
2. `uv run jupyter lab` and run either notebook.
3. `uv run pytest -q` runs the offline tests (a scripted model, no LLM needed); CI runs them too.

## Stack

Python · OpenAI-compatible chat API · python-dotenv · pytest

## Files

- `src/conversation.py`: agents, perspective, turn checks, moderator summary
- `notebooks/father-son-agents.ipynb`: two-agent parking dispute
- `notebooks/father-mother-son-motorcycle.ipynb`: three-agent motorcycle decision
- `tests/test_conversation.py`: offline tests
