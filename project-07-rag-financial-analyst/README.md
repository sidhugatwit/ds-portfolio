# Project 07 — RAG Financial Document Analyst

## Overview
Retrieval-Augmented Generation system that ingests financial passages 
from 2024-2025 earnings reports for NVIDIA, Microsoft, JPMorgan, Amazon, 
and Tesla. Uses FAISS vector search and sentence transformers to retrieve 
relevant context and answer analyst-style questions with source citations.

## Methods
- **Sentence Transformers** — all-MiniLM-L6-v2 for local embeddings (no API cost)
- **FAISS Index** — L2 similarity search across document corpus
- **RAG Pipeline** — retrieve → contextualize → cite sources
- **Retrieval Evaluation** — distance scores per company and section

## Key Queries Answered
- Which company had the highest revenue in 2025?
- What AI chips is NVIDIA selling and how do they perform?
- How is JPMorgan using AI in banking operations?
- Compare AWS vs Microsoft Azure AI investments
- What are the biggest risks facing NVIDIA?

## Stack
Python · FAISS · Sentence-Transformers · NumPy · Pandas

## Target Companies
Perplexity · Meta · Amazon · Fidelity

## Files
- `notebooks/rag_financial_analyst.ipynb` — full RAG pipeline
- `outputs/retrieval_eval.csv` — retrieval quality scores per query
- `outputs/corpus.csv` — full 2025 financial document corpus