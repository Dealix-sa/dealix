# مؤشر رافعة المؤسس — Founder Leverage Index

> One number that says: is the founder buying back time or selling it?

## Purpose
Quantify how much value each founder hour produces and how much the system runs without the founder. Track the move from "founder does everything" to "founder designs systems."

## Owner
Founder/CEO.

## Inputs
- `FOUNDER_TIME_ACCOUNTING.md` weekly logs.
- Revenue recognized this week (`docs/revenue/REVENUE_METRICS.md`).
- Sprints completed without founder execution (`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md` flags).
- Decisions delegated (logged with non-founder owner).

## Outputs
- Weekly Leverage Index score in `dealix-ops-private/leverage/YYYY-WW.json`.
- Quarterly trend chart (manually plotted or scripted).

## Rules
1. Compute every Sunday during the Weekly CEO Review.
2. Use only verified hours from `FOUNDER_TIME_ACCOUNTING.md`.
3. Use only recognized revenue (not booked, not committed) per `MRR_DEFINITION.md` and `CASH_RULES.md`.
4. Score below 40 two weeks in a row triggers a Build-bucket priority next week.
5. Score is for self-management, never reported externally.

## Metrics
- Leverage Index (0–100), weekly.
- Revenue per founder-hour (SAR), rolling 30 days.
- % founder time on A-tier work.
- % sprints requiring zero founder execution hours.

## Cadence
Weekly compute. Quarterly target reset.

## Evidence
`dealix-ops-private/leverage/`.

## Verifier
`make leverage-verify` — checks this week's file exists and pulls from valid time logs.

## Runtime Command
`make leverage-compute`

---

## The Formula

Leverage = (A-tier % × 0.30) + (Rev/hour scaled × 0.30) + (Sprints w/o founder % × 0.25) + (Delegated decisions % × 0.15)

Each input is scaled 0–100.

### A-tier %
A-tier hours (Revenue + Build) / total logged hours, × 100. Target ≥ 55.

### Revenue per founder-hour (scaled)
Rolling 30-day recognized revenue (SAR) / founder hours logged in same window.

Scaling (illustrative, reset quarterly):
| SAR/hour | Score |
|---|---|
| ≥ 1,500 | 100 |
| 1,000–1,499 | 80 |
| 600–999 | 60 |
| 300–599 | 40 |
| < 300 | 20 |

### Sprints without founder execution %
Sprints completed this month where founder logged 0 Delivery hours / total sprints completed.

### Delegated decisions %
Decisions logged with non-founder owner / total decisions logged.

## Interpretation

| Score | State | Implication |
|---|---|---|
| 80–100 | Designing | Founder is building systems, others execute |
| 60–79 | Steering | Founder leads strategy, intervenes selectively |
| 40–59 | Operating | Founder is hands-on; system is fragile |
| < 40 | Doing | Founder is the bottleneck; growth capped |

## What this index does NOT do
- It does not measure founder happiness.
- It does not penalize early-stage hands-on work; it makes the trade-off visible.
- It does not justify hiring before unit economics support it.

## Pairing with bets
A bet that requires the founder's hands for execution must list this explicitly. Two such concurrent bets trigger a kill review.

## القواعد العربية
1. يُحسب كل أحد ضمن المراجعة الأسبوعية.
2. درجة أقل من 40 لأسبوعين متتاليين تستدعي أولوية لساعات "البناء" الأسبوع التالي.
3. الدرجة للإدارة الذاتية، لا للنشر الخارجي.

## Cross-links
- `FOUNDER_TIME_ACCOUNTING.md`
- `CEO_BUSINESS_AUDIT.md`
- `docs/revenue/REVENUE_METRICS.md`
- `docs/strategy/STRATEGIC_BETS.md`
