# Trigger Event System

Time-bound signals that earn a recommendation to act.

## 1. Trigger taxonomy

| Class | Examples | Owner |
|---|---|---|
| Funding / corporate event | Funding round, M&A, leadership move. | distribution_operator |
| Hiring | Job posts indicating new function or scale. | growth_strategist |
| Regulatory | New PDPL note, ZATCA wave, sector circular. | trust_guardian |
| Product / launch | Public launch, RFP issuance. | offer_architect |
| Customer-shared | Email forward, conference card scan (with consent). | sales operator |

## 2. Trigger shape

```
trigger_id,class,account_id,event_summary,evidence_url,
collected_at,decay_days,confidence,recommended_action,
status (queued/approved/dismissed)
```

`decay_days` is how long the trigger is considered fresh (default 14).
After that, it expires automatically.

## 3. Confidence levels

- `high` — primary source, < 7 days old.
- `medium` — secondary source or 7–14 days old.
- `low` — fallback / inferred — needs human review before acting.

## 4. From trigger to action

Triggers never auto-send. They produce a **recommended draft** that
sits in the approval queue. The founder either approves the draft or
dismisses the trigger (with a reason that improves future scoring).

## 5. Refresh cadence

- Daily ingestion.
- Weekly summary in the founder digest.
- Monthly retro: which trigger classes converted?

## 6. Guardrails

- No PII scraping.
- No commercial surveillance vendors.
- Public signals only.
- Every trigger has an `evidence_url`. No URL → no trigger.
