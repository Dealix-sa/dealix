# Outbound Draft Machine

> Drafts personalised outbound. Never sends. Always queues for founder approval.

## 1. Purpose

Produce bilingual (AR + EN) outbound drafts for **A-priority** accounts on the recommended channel, carrying the required personalisation evidence.

## 2. Input

- The A-priority slice of `data/growth/account_scores.csv`.
- The buyer persona for each account.
- The recommended channel from `OFFER_CHANNEL_FIT_MATRIX.md`.
- The latest sector sample / proof artefact relevant to the account.

## 3. Output

Rows appended to `data/marketing/outreach_drafts.csv` with all required fields:

```
draft_id, account_id, target_contact, channel, language,
subject, body, personalisation_evidence, proof_attached,
recommended_offer, approval_state, created_at, queued_at
```

Initial `approval_state` is always `draft` or `queued`. Never `approved`. Never `sent`.

## 4. Data sources (whitelisted)

| Source              | Use                                                       |
|---------------------|-----------------------------------------------------------|
| Public LinkedIn     | Buyer title, posts, recent activity                       |
| Company website     | Sector focus, leadership page                             |
| KSA business press  | Hiring announcements, sector news                         |
| Customer intro      | Warm intros (with introducer approval)                    |

Sources NOT permitted: scrapers, data brokers without documented compliance, anything outside `DATA_SOURCES_POLICY.md`.

## 5. Approval class

**A1.** Founder must approve every draft individually. Bulk approval is not allowed in v1.

## 6. Owner

Distribution Operator agent + founder.

## 7. Worker name

`outbound_draft_worker`.

## 8. KPI

- Drafts per A-account per week: ≥ 1, ≤ 3.
- Evidence citation rate: 100% (no draft is queued without an evidence cell).
- Approval latency (queued → decision): median ≤ 24h.
- Approval rate (queued → approved without major edit): ≥ 60%.

## 9. Failure modes

| Failure                                          | Recovery                                                |
|--------------------------------------------------|---------------------------------------------------------|
| Draft has no evidence                            | Refuse to emit; escalate                                |
| Draft pitches a refused offer for the persona    | Refuse to emit; suggest alternative                     |
| Draft length exceeds limit                       | Truncate and re-draft; never queue oversize             |
| Same target contact drafted twice in 14 days     | Suppress; require founder override                      |
| Draft is monolingual when bilingual is required  | Refuse to emit; flag persona language config            |

## 10. Quality gates

The Brand Guardian Agent (see `docs/ai/BRAND_GUARDIAN_AGENT.md`) reads each draft and refuses any that:

- Uses banned phrases ("guaranteed revenue", "fully autonomous", "10x", "revolutionise", etc).
- Misuses the tagline.
- Contains emojis.
- Contains hype superlatives.

## 11. Audit

Every draft, approval, edit, hold, and reject writes a row to the internal approval ledger. The ledger is the source of truth for "what did the founder decide and when".

## 12. Doctrine

This machine does **not** send. It does not connect to email or LinkedIn APIs. It writes to CSVs and the internal approval queue. External send is a separate operation that only occurs after `approval_state = approved` and a human triggers it.
