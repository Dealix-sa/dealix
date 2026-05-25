# LLM Gateway

## Purpose

Control model selection, cost, quality, and safety.

## Routing Logic

- Low-risk classification: cheaper model
- Executive report: stronger model
- Governance check: strong model + rules
- RAG answer: retrieval + citation checks
- Outreach draft: claims safety check

## Rule

High-risk tasks require stronger validation.