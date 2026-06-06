# Revenue Board — لوحة الإيراد

The standing snapshot of the commercial pipeline. Refreshed from
`data/revenue/pipeline.jsonl` and `data/revenue/proof_assets.jsonl` by the
operating rhythm (`scripts/founder_daily_command.py`).

## Stages

| Stage | Meaning |
|---|---|
| `outreach_drafted` | Warm intro drafted, queued for founder approval |
| `diagnostic_delivered` | Free AI Ops Diagnostic delivered |
| `offer_sent` | A rung-1+ offer proposed |
| `won` | Engagement agreed (real or simulated for dry-run) |

## Current pipeline (seed)

| Event | Target | Stage | Offer | SAR | Governance |
|---|---|---|---|---|---|
| REV-0001 | T001 | outreach_drafted | free_diagnostic | 0 | queued_for_approval |
| REV-0002 | T003 | diagnostic_delivered | free_diagnostic | 0 | approved |
| REV-0003 | T003 | offer_sent | sprint_499 | 499 | queued_for_approval |
| REV-0004 | T008 | diagnostic_delivered | free_diagnostic | 0 | approved |
| REV-0005 | T008 | won (simulated) | sprint_499 | 499 | approved |

> The `won (simulated)` row exists to validate the E2E dry run — it is **not** a
> real charge. Real wins are recorded only after founder approval and an actual,
> approved payment.

## Capital assets registered

| Asset | Customer | Proof score | Capital? |
|---|---|---|---|
| PROOF-0001 | T008 | 78 | yes |
| CAP-0001 | T008 | 78 | yes |

## Rungs (reference)

0 Free Diagnostic · 1 Sprint 499 · 2 Data Pack 1,500 · 3 Managed Ops 2,999–4,999/mo
· 4 Custom AI 5,000–25,000 + 1,000/mo · Enterprise Governance Review 25,000–50,000.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
