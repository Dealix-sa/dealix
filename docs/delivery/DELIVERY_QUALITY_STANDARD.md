# Delivery Quality Standard

> The bar every Dealix delivery must meet — Sprint, Data Pack, Managed Ops, Custom AI.
> Failing this standard once = log; failing twice = stop and rebuild the offer.

## The 7-Point Standard

Every delivery must:

1. **Be on time** against the published timeline (Sprint: 7 days; Data Pack: 5 days; Managed Ops: monthly)
2. **Match the scope** in the signed proposal — every deliverable bullet shipped
3. **Pass QA** per `QA_CHECKLIST.md`
4. **Include an evidence pack** — sources, methodology, sanitization notes
5. **Use only allow-listed data sources** — no scraping, no purchased lists
6. **Pass `claim_guard.py`** — no unsubstantiated claims in any artifact
7. **Have a handoff document** — what's done, what's open, what's next

## Per-Offer Detail

| Offer | Time | Deliverables | QA owner |
|---|---|---|---|
| Sprint (499 SAR) | 7 days | 50 scored leads · 3 message variants · 3 objection responses · evidence pack | Founder |
| Data Pack (1,500 SAR) | 5 days | 200 enriched leads · sector benchmark · top-10 personalized · suppression cleanup | Founder |
| Managed Ops (2,999–4,999/mo) | Monthly | 100 leads/mo · weekly drafts · bi-weekly report · monthly sample · trust audit | Founder + agent |
| Custom AI (5K–25K/mo) | Scoped | Custom per SOW + dedicated approval matrix + quarterly review | Founder + advisor |

## Common Failure Modes (and prevention)

- **Scope creep** → defended by `SCOPE_CONTROL.md`; any addition = new proposal
- **Late delivery** → defended by daily progress note in `delivery/active_sprints/{client}/progress.md`
- **Sample-vs-real mismatch** → defended by `SAMPLE_GENERATION_SYSTEM.md` discipline
- **Overclaim in handoff** → defended by `claim_guard.py` on report templates
- **Privacy leak** → defended by `dealix/trust/data_retention.py` + private-only client data rule

## QA Pass Criteria

A delivery passes QA when:
- Every deliverable has a checked-off entry in `QA_CHECKLIST.md`
- Every external-facing artifact passed `claim_guard.py`
- Evidence pack is complete (sources, dates, methodology)
- Handoff doc exists and is reviewed
- No open items > 24 hours past planned date

## When A Delivery Misses

Severity classification:
- **L1** — < 24 hr late, scope intact → log + apologize in handoff
- **L2** — > 24 hr late OR partial scope → credit/refund per `BILLING_POLICY.md` + root cause
- **L3** — failed scope OR trust incident → refund + advisor review + offer pause

Every miss appears in `clients/{client}/delivery_misses.md` (private) and aggregates to `learning/`.

## Throughput Limits

Until throughput proven:
- Max 2 active Sprints simultaneously (founder bandwidth)
- Max 2 active Managed Ops + 1 active Sprint
- Max 1 active Custom AI build (high attention required)

Exceed these → either delay accepting work or trigger hire (per `HIRING_TRIGGERS.md`).

## Quality Metrics

- Delivery on-time rate: target ≥ 95%
- QA failure rate: target < 5%
- Client feedback score: target ≥ 8/10
- Rework count per delivery: target < 1
- Evidence pack completeness: target 100%

## Review Cadence

- Per delivery: QA pass before handoff
- Weekly: delivery metrics in Weekly CEO Review
- Monthly: failure pattern review → does the offer need to be re-productized?

## What This Standard Refuses

- "Almost done" shipped as "done"
- Verbal handoff (everything written)
- Skipping QA "just this once"
- Delivering without evidence pack
- Telling the client we'll fix it later without a written remediation date
