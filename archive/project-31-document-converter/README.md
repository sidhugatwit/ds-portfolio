# Project 31 — Universal Document Converter & Summarizer

## Overview

An AI-powered document processing system that reads any file format,
generates intelligent summaries in four styles, answers questions about
document content, and exports to multiple output formats. Supports
PDF, DOCX, PPTX, XLSX, TXT, CSV, and Markdown input.

## Features

### Document Reading

- PDF — PyPDF2 text extraction
- DOCX — python-docx paragraph extraction
- PPTX — slide-by-slide text extraction
- XLSX — multi-sheet data extraction
- TXT / MD / CSV — plain text reading
- Auto-detection by file extension

### AI Summarization (4 styles)

- Executive — 3-sentence decision-focused summary
- Bullet — 5-7 key points
- Detailed — 2-paragraph comprehensive summary
- Technical — methods, metrics, and results focused

### Document Q&A

- Answer any question about document content
- Confidence scoring (high/medium/low)
- Source quote from document

### Format Conversion

- Input → Markdown (clean, structured)
- Input → DOCX (formatted Word document)
- Input → HTML (web-ready)

## Stack

Python · OpenAI API · PyPDF2 · python-docx · python-pptx ·
openpyxl · markdown · Pandas

## Files

- `notebooks/document_converter.ipynb` — full pipeline
- `outputs/converted.md` — Markdown output
- `outputs/converted.docx` — Word document output
- `outputs/converted.html` — HTML output
- `outputs/summary.json` — AI-generated summary
