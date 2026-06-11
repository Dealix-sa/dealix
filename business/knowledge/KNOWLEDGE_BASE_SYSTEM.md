# Dealix Knowledge Base System

## Purpose
Make Dealix's own playbooks, FAQ, and policies searchable for the founder and (later) for the customer-facing assistant.

## Sources
- `business/enterprise/*.md`
- `business/deal-desk/*.md`
- `business/contracts/*.md`
- `business/proof/*.md`
- `business/ai/*.md`
- `docs/**/*.md`

## Index format (v1)
Deterministic local index in `business/_data/knowledge_index.json`. Maps each markdown file to its title and first 500 chars. Search is substring + lowercased keyword match.

## Future
- Vector index (when an embedding provider is contracted).
- Per-customer knowledge slice.

## What we never index
- `business/contracts/signed/` (PII).
- `business/_data/audit_log.json` (PII).
- `.env*` files.
