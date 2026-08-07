# Dealix AI Governance Statement

## Default mode is deterministic

Dealix's operator scripts and review tooling do not require an LLM to run. The default produces deterministic, reproducible output. LLM-assist is opt-in and per task.

## What we never do

- We do not auto-send AI-generated messages.
- We do not let AI write contractual or pricing language without founder review.
- We do not use customer data to train shared models.
- We do not claim AI-generated proof items.

## Where AI is allowed

- Outreach drafts (always queued for human review).
- Proposal section drafts (always queued for human review).
- Objection response drafts.
- Translation AR↔EN of human-written content.
- Sales call summaries.
- Internal compliance review preflight (final review is human).

## Provider posture

- Provider plug-in architecture (`scripts/lib/ai_router.py`).
- Per-call audit log: provider, model, prompt version, review_status.
- Per-customer opt-in: AI mode is OFF until customer signs an AI usage addendum.

## Human review gates

Every AI-generated outbound artifact must pass:
- `review_status` must be `pending` until a human approves.
- A founder approval signature is recorded in `business/_data/audit_log.json`.

## Banned claims

- "Guaranteed revenue", "guaranteed ROI", "نضمن نتائج", etc. — enforced by `tests/test_no_guaranteed_revenue_claims.py`.

## Evaluation

- `scripts/run_ai_evals.py` runs deterministic eval cases against every prompt version.
- Failed evals block release via `scripts/release_guard.py`.
