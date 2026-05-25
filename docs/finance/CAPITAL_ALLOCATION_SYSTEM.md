# نظام تخصيص رأس المال — Capital Allocation System

> Seven tiers, ordered. Revenue gen → delivery quality → trust → repeatability → automation → brand proof → optionality.

## Purpose
Force every SAR spent (and every founder hour beyond delivery) to compete against the seven tiers. Prevent silent drift.

## Owner
Founder/CEO.

## Inputs
- Strategic bets (`docs/strategy/STRATEGIC_BETS.md`).
- Cash position (`CASH_CONTROL.md`).
- Moat scores (`docs/strategy/MONTHLY_MOAT_REVIEW.md`).
- Founder Leverage Index (`docs/founder/FOUNDER_LEVERAGE_INDEX.md`).

## Outputs
- Monthly allocation table (% per tier).
- Variance vs target (actual SAR + hours per tier).
- Decision: continue / shift / kill, per Monthly Strategy Review.

## Rules
1. Allocation is set Monthly in the Monthly Strategy Review.
2. Tier 1 (revenue gen) cannot drop below 25% while runway < 12 months.
3. Tier 4 (repeatability) and Tier 5 (automation) cannot increase if Tier 1 actuals are missing targets.
4. Tier 7 (optionality) is capped at 10% until break-even MRR is reached.
5. Re-allocation mid-month is allowed only via A2 Go/No-Go gate.

## Metrics
- % variance from target per tier: target ≤ 15%.
- Tier 1 share while runway < 12 months: ≥ 25%.
- Tier 7 share: ≤ 10% pre-break-even.

## Cadence
Set Monthly. Variance reviewed Weekly.

## Evidence
`dealix-ops-private/finance/allocation-YYYY-MM.md`.

## Verifier
`make capital-allocation-verify` — checks current month allocation totals 100% and respects the floors/ceilings.

## Runtime Command
`make allocation-set month=YYYY-MM`

---

## The Seven Tiers (ordered by priority)

### Tier 1 — Revenue Generation
Activities that directly produce new paid sprints.
- Founder hours in Revenue bucket (per `docs/founder/FOUNDER_TIME_ACCOUNTING.md`).
- Proposal preparation tooling.
- Inbound infrastructure (founder voice publishing, content discipline).

### Tier 2 — Delivery Quality
Activities that ensure delivered sprints produce evidence and acceptance.
- Sprint templates, playbooks.
- Quality checks, acceptance criteria.
- Delivery tooling.

### Tier 3 — Trust
Activities that strengthen the Trust moat.
- Trust pack updates.
- Disclosure surfaces.
- Refund handling, compliance.
- Legal reviews.

### Tier 4 — Repeatability
Activities that fold the 3rd-success into a doc, 5th into a template.
- Documentation effort.
- Standardization.
- Capturing learnings from each sprint.

### Tier 5 — Automation
Activities that reduce founder hours on repeatable tasks.
- Internal scripts, makefile additions.
- Templates that generate proposals/invoices.
- Verifier scripts.

### Tier 6 — Brand Proof
Activities that compound founder voice and external proof.
- Bilingual case-safe artifacts.
- Sector reports.
- Founder publishing.

### Tier 7 — Optionality
Activities that buy future strategic choice without short-term return.
- New market exploration (within `MARKET_ENTRY_DECISION.md` rules).
- Adjacent ICP scoping.
- Productization R&D.

## Default allocation table (illustrative, pre-break-even)

| Tier | Name | Target % |
|---|---|---|
| 1 | Revenue gen | 30 |
| 2 | Delivery quality | 20 |
| 3 | Trust | 12 |
| 4 | Repeatability | 12 |
| 5 | Automation | 10 |
| 6 | Brand proof | 8 |
| 7 | Optionality | 8 |
| | Total | 100 |

Adjust per month based on KPI tree state, moat scores, and runway.

## What "allocation" counts
- SAR spent on tools, vendors, contractors.
- Founder hours (counted at shadow rate SAR 600/hour for variance math).
- New software licenses.

## What allocation does NOT count
- Delivery hours on customer sprints (those are the product, not capital).
- One-off legal or accounting expenses that are mandatory.

## Tier shift rules
- Increasing a tier requires the source tier to be at or above target.
- Decreasing Tier 1 below 25% while runway < 12 months is forbidden.
- Adding to Tier 7 requires written reason and a kill criterion.

## القواعد العربية
1. التخصيص يُحدَّد شهريًا في المراجعة الاستراتيجية.
2. الطبقة 1 لا تنزل تحت 25% ما دام المدرج النقدي أقل من 12 شهرًا.
3. الطبقة 7 سقفها 10% قبل بلوغ التعادل.

## Cross-links
- `FINANCIAL_MODEL_V1.md`
- `CASH_CONTROL.md`
- `docs/strategy/STRATEGIC_BETS.md`
- `docs/strategy/MONTHLY_MOAT_REVIEW.md`
- `docs/founder/MONTHLY_STRATEGY_REVIEW.md`
