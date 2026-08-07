# AI Review Gates

Every AI-touched artifact passes these gates before any external use.

## Gate 1 — Safety check (pre-call)
- Refuse banned phrases (guarantee, scrape, fake review, etc.).
- Refuse oversized prompts.
- Refuse if customer hasn't opted into LLM-assist.

## Gate 2 — Eval check (post-call)
- No banned claims in output.
- No autosend language.
- review_status set to `pending_human_review`.

## Gate 3 — Human review
- Founder reads, edits, approves.
- Approval recorded in `business/_data/ai_audit_log.json` AND `business/_data/audit_log.json`.

## Gate 4 — Delivery
- Approved artifact delivered through the customer's own channel by the founder. No bot send.

## Failure routing
- Gate 1 fail → refusal logged; no output produced.
- Gate 2 fail → deterministic fallback regenerated; LLM output discarded.
- Gate 3 fail → artifact deleted; revised draft generated.
