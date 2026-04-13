# Project 15 — RAG Implementation with Chunking & Context Windows

## Overview

Two complementary notebooks exploring Retrieval-Augmented Generation
from different angles. The first implements a full production-grade RAG
pipeline with LangChain, ChromaDB, and OpenAI. The second explores
context window management and embeddings using a local LLM via Ollama
— demonstrating both cloud and local inference approaches.

## Notebooks

### 1. RAG Implementation with Chunking

Full RAG pipeline that loads PDF documents, splits them into chunks
using RecursiveCharacterTextSplitter, embeds them into ChromaDB, and
answers questions with source citations using GPT-4o-mini.

**Key concepts:**

- Document loading and chunking strategies
- Chunk size and overlap experimentation
- ChromaDB vector store with OpenAI embeddings
- LangChain LCEL pipeline with RunnableParallel
- Interactive chat interface for document Q&A
- Student exercises for extending the pipeline

### 2. Context Window & Embeddings RAG

Explores how context window size affects retrieval quality using a
local LLM via Ollama — no API costs, fully offline inference.

**Key concepts:**

- Context window management strategies
- Local embedding models via Ollama
- Retrieval quality vs context length tradeoffs

## Stack

Python · LangChain · ChromaDB · OpenAI API · Ollama · PyPDF ·
RecursiveCharacterTextSplitter

## Target Companies

Perplexity · Meta · Amazon · Anthropic

## Relation to Portfolio

Complements Project 07 (RAG Financial Analyst) by showing the
underlying chunking and retrieval mechanics in detail, and
demonstrating local LLM inference as an alternative to cloud APIs.

## Files

- `notebooks/RAG_Implementation_with_chunking.ipynb` — full RAG pipeline
- `notebooks/ContextWindow_Embeddings_RAG.ipynb` — local LLM context exploration
