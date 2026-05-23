# النموذج المالي v1 — Financial Model v1

> Assumptions, three scenarios, break-even.

## Purpose
A single, transparent model the founder can defend to a board, an advisor, or themselves. Updated quarterly. Treated as a model, not a forecast.

## Owner
Founder/CEO.

## Inputs
- Revenue model (`docs/revenue/REVENUE_MODEL.md`).
- Cost base (founder + tools + vendors + legal).
- Conversion assumptions (from `REVENUE_METRICS.md` actuals once available).
- Capital allocation (`CAPITAL_ALLOCATION_SYSTEM.md`).

## Outputs
- The model in this file (assumptions, scenarios).
- A workbook export in `dealix-ops-private/finance/model-v1-YYYY-Q.xlsx` if used.

## Rules
1. Every assumption is named, dated, and sourced. No "industry standard" without a link.
2. Three scenarios exist at all times: base, bull, bear. Single-point forecasts are forbidden.
3. The model is refreshed Quarterly. Mid-quarter changes require Monthly Strategy Review.
4. Break-even is computed for each scenario.
5. The model includes a founder shadow rate (SAR 600/hour) so founder labor cost is visible.

## Metrics
- Break-even MRR.
- Break-even monthly sprints.
- Runway at current burn (also in `CASH_CONTROL.md`).
- Sensitivity: what move in proposal-to-payment rate closes the gap?

## Cadence
Refreshed Quarterly. Reviewed Monthly.

## Evidence
This file + the workbook export.

## Verifier
`make financial-model-verify` — checks every assumption has a source link and a date.

## Runtime Command
`make financial-model-refresh quarter=YYYY-Q`

---

## Assumptions (template — fill with current numbers)

| # | Assumption | Value | Source | Date |
|---|---|---|---|---|
| 1 | Signal Sample price | SAR 18,000 | `OFFER_LADDER.md` | YYYY-MM-DD |
| 2 | Revenue Sprint price | SAR 110,000 | `OFFER_LADDER.md` | YYYY-MM-DD |
| 3 | Revenue Desk price | SAR 35,000 / month | `OFFER_LADDER.md` | YYYY-MM-DD |
| 4 | Signal Sample → Sprint conversion | 60% | actual or estimate | YYYY-MM-DD |
| 5 | Sprint → Retainer attach | 30% | `REVENUE_METRICS.md` | YYYY-MM-DD |
| 6 | Sprint gross margin | 60% | `REVENUE_MODEL.md` | YYYY-MM-DD |
| 7 | Retainer gross margin | 65% | `REVENUE_MODEL.md` | YYYY-MM-DD |
| 8 | Monthly fixed costs (tools, legal, accounting) | SAR XX,XXX | bank records | YYYY-MM-DD |
| 9 | Founder shadow rate | SAR 600 / hour | this file | YYYY-MM-DD |
| 10 | Quarterly sprints capacity (solo founder) | 6 | `REVENUE_MODEL.md` capacity logic | YYYY-MM-DD |

## Scenarios

### Base (50% probability)
- Sprints/quarter: 4
- Retainer attach: 30%
- New retainers/quarter: 1.2
- Quarterly revenue: SAR XXX,XXX
- Monthly MRR end of quarter: SAR XX,XXX
- Net cash/quarter: +/- SAR XX,XXX
- Break-even MRR: SAR XX,XXX
- Months to break-even: M

### Bull (25% probability)
- Sprints/quarter: 6
- Retainer attach: 40%
- New retainers/quarter: 2.4
- Quarterly revenue: SAR XXX,XXX
- Monthly MRR end of quarter: SAR XXX,XXX
- Net cash/quarter: + SAR XXX,XXX

### Bear (25% probability)
- Sprints/quarter: 2
- Retainer attach: 20%
- New retainers/quarter: 0.4
- Quarterly revenue: SAR XX,XXX
- Net cash/quarter: - SAR XX,XXX
- Runway impact: -NN days vs base
- Triggers: `CASH_CONTROL.md` orange/red protocols

## Break-even

Break-even MRR = monthly fixed costs / retainer gross margin.

Worked example (illustrative):
- Monthly fixed costs: SAR 40,000
- Retainer gross margin: 65%
- Break-even MRR: SAR 40,000 / 0.65 = SAR 61,538/month

This is illustrative only. Replace with real numbers at refresh.

## Sensitivity table

| Driver | Move | Quarterly revenue impact |
|---|---|---|
| Proposal-to-payment rate | +5pp | + SAR XX,XXX |
| Sprint price | +SAR 10,000 | + SAR XX,XXX × sprints |
| Retainer attach | +10pp | + SAR XX,XXX (recurring) |
| Sprint capacity | +1 sprint/q | + SAR XX,XXX |

## What this model does NOT do
- Project specific customer wins by name.
- Replace cash control (`CASH_CONTROL.md`).
- Guarantee any outcome — all numbers are estimates.

## Disclosure footer (when shared internally)
> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

## القواعد العربية
1. كل افتراض مسمى، مؤرَّخ، ومصدره موثَّق.
2. ثلاثة سيناريوهات دائمًا: قاعدي، صاعد، هابط. الرقم الوحيد ممنوع.
3. ساعة المؤسس تُكلَّف 600 ريالًا في النموذج.

## Cross-links
- `CASH_CONTROL.md`
- `docs/revenue/REVENUE_MODEL.md`
- `docs/revenue/REVENUE_METRICS.md`
- `CAPITAL_ALLOCATION_SYSTEM.md`
- `MRR_DEFINITION.md`
