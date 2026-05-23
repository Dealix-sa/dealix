# Dealix Document Standard

Every operating document inside Dealix Company OS must contain the following sections, in this exact order. A file that does not satisfy this standard is considered "not yet operational" — it exists, but the system cannot rely on it.

## Purpose
Why this document exists. One paragraph that explains the operating role it plays inside Dealix.

## Owner
Who owns the system this document describes today. There is always exactly one owner. If no owner can be named, the document is not ready.

## Review Cadence
Daily, weekly, monthly, or quarterly. Pick one — never leave blank.

## Inputs
What this system needs to function: data, signals, decisions, customer evidence, upstream artifacts.

## Outputs
What this system produces: decisions, rules, templates, evidence, downstream artifacts.

## Rules
The non-negotiable rules that govern this system. These are constraints, not goals.

## Metrics
How performance is measured. Numeric where possible. No vanity metrics.

## Evidence
What proves this system is working — linked files, workflow runs, customer feedback, payments, delivered artifacts, decision logs.

## Last Reviewed
`YYYY-MM-DD` — the date this document was last reviewed by its owner.

---

## The Rule

Any operating document that does not contain `Purpose + Owner + Metrics + Evidence` is considered **not ready**. The deep verifier (`scripts/verify_document_quality.py`) enforces this and will fail the build for any non-compliant file in the operating tree.

## Why
- Empty placeholders rot. Templates do not.
- Anyone joining Dealix should be able to read any operating doc and know who owns it, how it is measured, and what evidence proves it is working.
- The AI cannot run the loops if the loops are not written down with owner, metric, and evidence.

## Last Reviewed
2026-05-23
