# مركز قيادة الإيرادات — Revenue Command Center

> The single revenue dashboard + offer ladder snapshot.

## Purpose
A single page showing pipeline, cash-in this week, offers in play, and any blocker that prevents payment. The founder opens this after the CEO Command Center each morning.

## Owner
Founder/CEO.

## Inputs
- Pipeline stages (`PIPELINE_STAGES.md`).
- Offer ladder (`OFFER_LADDER.md`).
- Revenue metrics (`REVENUE_METRICS.md`).
- Cash control (`docs/finance/CASH_CONTROL.md`).
- Pricing experiments (`PRICING_EXPERIMENTS.md`).

## Outputs
- Daily snapshot in `dealix-ops-private/revenue/YYYY-MM-DD.md`.
- Weekly summary in `dealix-ops-private/weekly/`.

## Rules
1. Updated daily before 9:00 AM Riyadh.
2. Numbers cite their source artifact. No "approximately".
3. Pipeline contains only ICP-fit ≥ 5 opportunities. Lower scores are recorded but flagged.
4. No opportunity sits in the same stage > 21 days without a written reason.
5. No celebration of "closed" until cash is received per `CASH_RULES.md`.

## Metrics
- Pipeline coverage (open SAR vs quarterly target): track and grow.
- Stage aging > 21 days: target 0.
- Proposal-to-payment rate (rolling 30d): ≥ 30% target.
- Retainer attach rate (post-sprint): ≥ 30% target.

## Cadence
Daily snapshot, Weekly summary, Monthly trend.

## Evidence
`dealix-ops-private/revenue/`.

## Verifier
`make revenue-command-verify` — checks today's snapshot exists and every open stage has age recorded.

## Runtime Command
`make revenue-daily`

---

## The Page

```
# Revenue Command Center — YYYY-MM-DD

## Headline
Cash this week (received): SAR X
Cash this week (expected): SAR X
Pipeline open: SAR X (N opportunities)
Coverage vs quarter target: NN%

## Stages (from PIPELINE_STAGES.md)
| Stage | Count | SAR | Oldest age (days) |
|---|---|---|---|
| Lead | N | X | D |
| DM identified | N | X | D |
| Reply | N | X | D |
| Call scheduled | N | X | D |
| Sample (paid Signal Sample) | N | X | D |
| Proposal sent | N | X | D |
| Proposal accepted | N | X | D |
| Invoiced | N | X | D |
| Paid | N | X | — |

## Offer ladder snapshot
| Rung | Active count | SAR booked this quarter |
|---|---|---|
| Signal Sample | N | X |
| Revenue Sprint | N | X |
| Managed Pilot | N | X |
| Revenue Desk (retainer) | N | X (MRR component) |
| Dealix OS | N | X |

## Blockers (one line each)
- <opportunity id>: <blocker> — action today

## Pricing experiments active
- <experiment id>: sample N of N, status, kill rule

## Today's revenue focus
<single sentence>
```

## What this page is NOT
- Not a forecast (forecasting lives in `docs/finance/FINANCIAL_MODEL_V1.md`).
- Not a CRM replacement. It is a daily snapshot derived from the CRM.
- Not for external sharing — pipeline counts and SAR are internal.

## Discipline rules
- "Closed" is replaced with "Paid" everywhere on this page.
- "Hot lead" is replaced with the stage name (e.g., "Proposal sent").
- "Big deal" is replaced with the SAR number.
- No customer name appears outside private internal copies; anonymized labels (Customer-A1) elsewhere.

## Escalation
| Signal | Action |
|---|---|
| Pipeline coverage < 50% of quarter target | Founder spends 60% of A-tier time on Revenue bucket |
| Proposal-to-payment rate < 20% (rolling 30d) | Trigger proposal-quality review |
| Cash expected this week < SAR threshold | Trigger `CASH_CONTROL.md` mid-week check |

## القواعد العربية
1. تُحدَّث يوميًا قبل التاسعة صباحًا.
2. الأرقام تستشهد بمصادرها.
3. الفرص الراكدة فوق 21 يومًا تحتاج تعليلًا مكتوبًا.

## Cross-links
- `PIPELINE_STAGES.md`
- `OFFER_LADDER.md`
- `REVENUE_METRICS.md`
- `docs/founder/CEO_COMMAND_CENTER.md`
- `docs/finance/CASH_CONTROL.md`
