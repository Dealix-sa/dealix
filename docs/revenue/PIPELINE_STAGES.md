# Pipeline Stages

## Stages

| # | Stage | Definition | Exit Criterion | Weight |
|---|---|---|---|---:|
| 0 | Sourced | Lead identified, ICP-matched | Replied to outreach | 5% |
| 1 | Qualified | Replied, fits ICP, has trigger | Discovery call booked | 15% |
| 2 | Discovery | 30-min call completed | Free Diagnostic agreed | 30% |
| 3 | Diagnostic | Async diagnostic delivered | Sprint proposal accepted | 50% |
| 4 | Proposal | Proposal sent, scope agreed | Invoice issued | 70% |
| 5 | Invoiced | Invoice sent | Payment received | 90% |
| 6 | Paid | Cash received | Delivery kickoff | 100% |
| 7 | Delivered | Sprint/Pack delivered with proof pack | Retainer pitch | n/a |
| 8 | Retainer | Recurring contract live | Quarterly review | n/a |

## Stage Rules

1. A lead moves backward only with a written reason.
2. A stuck stage (no movement in 14 days) auto-flags in the Daily Brief.
3. Stage 4 (Proposal) requires A2 approval per `docs/trust/APPROVAL_MATRIX.md`.
4. Stage 5 (Invoiced) requires the proposal to be on file in the proof library.

## Forecast Math

Pipeline value = Σ (opportunity_value × stage_weight) across open deals.

## Definitions

- **Open** = stages 0–5.
- **Won** = stages 6–8.
- **Lost** = explicitly marked with a loss reason recorded in `WIN_LOSS_REVIEW.md`.

## Hygiene

Pipeline is reviewed every Monday in the weekly CEO Review. Any deal in
the same stage for 21 days is moved to Lost unless the CEO documents a
reason to keep it open.
