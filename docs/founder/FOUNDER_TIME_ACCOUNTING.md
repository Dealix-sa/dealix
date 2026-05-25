# محاسبة وقت المؤسس — Founder Time Accounting

> Log founder time across five buckets. Optimize toward A-tier work.

## Purpose
Make founder time visible. Without measurement, the founder drifts to whatever is loudest, not most leveraged.

## Owner
Founder/CEO.

## Inputs
- Calendar (work blocks).
- Manual log entries (any block ≥ 30 min must be logged).
- Bucket definitions below.

## Outputs
- `dealix-ops-private/time/YYYY-WW.csv` with rows: date, bucket, hours, tag, note.
- Weekly summary in the Weekly CEO Review.

## Rules
1. Log every block ≥ 30 minutes. Block < 30 min is rounded down to 0.
2. Bucket assignment is exclusive — one block = one bucket.
3. Logs are written within 24 hours. No back-fill beyond 2 days.
4. Personal time is excluded; only Dealix work hours are accounted.
5. The week's hours are summarized Sunday in the Weekly Review.
6. Quarterly: target distribution is computed and compared to actual.

## Metrics
- Logging coverage: ≥ 85% of working hours.
- % time in A-tier buckets (Revenue + Build): target ≥ 55%.
- % time in C-tier (administrative): target ≤ 15%.
- Revenue per founder-hour (rolling 30 days): track and grow.

## Cadence
Daily logging. Weekly summary. Quarterly target reset.

## Evidence
`dealix-ops-private/time/`.

## Verifier
`make time-verify` — checks today's and last 7 days' logs exist and have at least 20 logged hours (assuming 40h week).

## Runtime Command
`make time-log entry="bucket=Revenue hours=2.5 tag=proposal-A2"`

---

## The Five Buckets

| Tier | Bucket | Definition | Example |
|---|---|---|---|
| A | Revenue | Direct selling, customer calls, proposals, payment chase | Demo call, sending a proposal |
| A | Build | Building offers, productizing, evidence creation | Writing a sprint template, case study |
| B | Delivery | Doing the work in active sprints | Implementing analysis for Customer-A1 |
| B | Trust | Governance, compliance, trust artifacts | Updating disclosures, refund policy |
| C | Admin | Email, scheduling, finance ops, vendor management | Bank, accounting, expense receipts |

## Target distribution (weekly, while pre-product-market-fit)

| Tier | Bucket | Target % |
|---|---|---|
| A | Revenue | 30 |
| A | Build | 25 |
| B | Delivery | 25 |
| B | Trust | 10 |
| C | Admin | 10 |

## Log format
```
date,bucket,hours,tag,note
2026-05-23,Revenue,2.0,proposal,Customer-A2 revised scope
2026-05-23,Delivery,3.5,sprint,Customer-A1 analysis
2026-05-23,Admin,0.5,bank,reconcile May invoices
```

## Anti-patterns
- "Mixed bucket" entries — pick one.
- Logging at end of week from memory.
- Tagging delivery as Build to inflate A-tier %.
- Excluding low-energy weeks "because it would skew the data" — log them.

## How this feeds Founder Leverage
The `FOUNDER_LEVERAGE_INDEX.md` formula uses these logs. Skip a week and the index becomes unreliable; the weekly audit will flag it.

## القواعد العربية
1. سجّل كل كتلة من 30 دقيقة فأكثر.
2. سطل واحد لكل كتلة، لا "مختلط".
3. السجل خلال 24 ساعة. لا تأجيل أكثر من يومين.

## Cross-links
- `FOUNDER_LEVERAGE_INDEX.md`
- `CEO_BUSINESS_AUDIT.md`
- `WEEKLY_CEO_REVIEW.md`
