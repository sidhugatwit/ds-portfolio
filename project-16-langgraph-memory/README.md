# Project 16 — Agentic Email Triage System (LangGraph)

A production-style agentic AI system that classifies and responds to emails using structured reasoning, decision routing, and tool-based execution.

## Overview

This project implements an end-to-end agentic workflow using LangGraph to simulate a real-world AI assistant that:

- classifies incoming emails (ignore / notify / respond)
- routes decisions using a stateful graph
- executes actions via tools (email, scheduling, calendar)

The system goes beyond prompt-response by incorporating structured outputs, multi-step reasoning, and autonomous decision-making.

## Architecture

START → Triage Router → Decision → Response Agent → END
↘ END (ignore / notify)

- **Triage Router**
  - Uses GPT-4o-mini with structured output (Pydantic)
  - Classifies emails into ignore / notify / respond
  - Applies user-specific triage rules

- **Response Agent**
  - ReAct-based agent with tool integration
  - Executes actions such as drafting replies and scheduling meetings
  - Maintains state through LangGraph message passing

## Features

- Structured email classification using Pydantic schemas  
- LangGraph StateGraph for decision routing  
- ReAct agent with tool calling  
- Multi-step reasoning before action  
- Real-world test scenarios (spam, technical, meeting requests)  

## Tools Implemented

- `write_email` → draft and send responses  
- `schedule_meeting` → schedule calendar events  
- `check_calendar_availability` → retrieve available time slots  

## Key Concepts

- Stateful agent orchestration (LangGraph)  
- Structured LLM outputs (Pydantic)  
- Tool-augmented AI workflows  
- Decision routing and control flow  
- Agent-based system design  

## Tech Stack

Python · LangGraph · LangChain · GPT-4o-mini · Pydantic · python-dotenv  

## Requirements

```bash
pip install langchain langgraph openai python-dotenv pydantic
