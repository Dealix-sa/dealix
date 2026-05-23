# نموذج الإيرادات — Revenue Model

> Unit economics for the 5-rung offer ladder.

## Purpose
State the assumed unit economics per rung so pricing, capital allocation, and capacity decisions are evidence-based, not aspirational.

## Owner
Founder/CEO.

## Inputs
- Offer ladder (`OFFER_LADDER.md`).
- Delivery effort estimates (`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`).
- Cost base (`docs/finance/FINANCIAL_MODEL_V1.md`).
- Pricing experiments (`PRICING_EXPERIMENTS.md`).

## Outputs
- The table below, refreshed quarterly with actuals.
- Updates to `docs/finance/FINANCIAL_MODEL_V1.md`.

## Rules
1. Numbers in this file are estimates labeled as such until ≥ 5 runs of a rung produce actuals.
2. Margin assumptions exclude founder time below SAR 600/hour shadow rate (force the founder to value their time).
3. Retainer revenue is recognized monthly per `MRR_DEFINITION.md`, not as a lump.
4. No rung is offered until its delivery template exists in `docs/03_commercial_mvp/`.
5. Negative-margin rungs are allowed only as deliberate market-entry investments, declared as a bet.

## Metrics
- % of revenue from each rung (per quarter).
- Gross margin per rung.
- Retention (renewal) rate of Revenue Desk retainers.
- Productization progress per rung (3/5/10 thresholds).

## Cadence
Reviewed Quarterly.

## Evidence
This file + `FINANCIAL_MODEL_V1.md`.

## Verifier
`make revenue-model-verify` — checks each rung has all six fields and at least one actual or estimate label.

## Runtime Command
`make revenue-model-refresh`

---

## The Five Rungs (estimates; refresh quarterly)

| # | Rung | Price (SAR) | Effort (founder hours) | Direct cost (SAR) | Estimated gross margin | Delivery time |
|---|---|---|---|---|---|---|
| 1 | Signal Sample | 15,000 – 25,000 | 20 – 30 | 2,000 | 50–65% | 5–10 days |
| 2 | Revenue Sprint | 75,000 – 150,000 | 80 – 120 | 8,000 – 15,000 | 55–70% | 4–6 weeks |
| 3 | Managed Pilot | 100,000 – 200,000 | 100 – 140 | 12,000 – 20,000 | 50–65% | 6–8 weeks |
| 4 | Revenue Desk (retainer) | 25,000 – 60,000 / month | 20 – 40 / month | 3,000 – 6,000 / month | 60–75% | ongoing, 3-month minimum |
| 5 | Dealix OS | 100,000 / year + services | varies | varies | TBD post-productization | annual license |

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

## Founder shadow rate
A founder hour is costed at SAR 600/hour for margin calculations. This forces the question: would a fully delegated team produce the same margin at the same price?

## Capacity logic
- Solo founder: max 2 active Revenue Sprints + 1 retainer at any time.
- After Motion 2 transition: capacity multiplied by delivery-lead headcount.

## Pricing principles
- Anchor on outcome value, not hours.
- Saudi market pricing: SAR currency, AR-primary contracts, VAT noted per `docs/finance/BILLING_POLICY.md`.
- Discounts are allowed but logged with reason; > 20% discount requires founder approval and a written justification in the proposal file.

## Bundling
- Signal Sample + Revenue Sprint discount: up to 10% combined, if signed together.
- Revenue Sprint + Revenue Desk discount: up to 15% combined.
- No "free pilot" bundles — every paid rung is paid.

## Negative-margin allowance
Up to one negative-margin rung at a time, declared as a bet with kill criteria. Used to enter a new ICP or sector with a strategic anchor customer.

## How rungs feed each other
- Signal Sample is the qualifier for Revenue Sprint.
- Revenue Sprint is the qualifier for Revenue Desk.
- Revenue Sprint × 10 successful runs is the trigger for Managed Pilot productization.
- Managed Pilot × productized = candidate Dealix OS module.

## What this model excludes
- Speculative SaaS pricing for unbuilt modules.
- White-label arrangements (require legal review).
- Reseller margins (no resellers in Motion 1).

## القواعد العربية
1. الأرقام هنا تقديرات حتى يكتمل خمس جولات لكل درجة.
2. ساعة المؤسس تُكلَّف 600 ريالًا في حسابات الهامش.
3. لا درجة تُعرض دون وجود قالب تسليم لها.

## Cross-links
- `OFFER_LADDER.md`
- `PRICING_EXPERIMENTS.md`
- `docs/finance/FINANCIAL_MODEL_V1.md`
- `docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`
- `MRR_DEFINITION.md`
