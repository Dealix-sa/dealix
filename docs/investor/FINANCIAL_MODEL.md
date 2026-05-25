# Investor-View Financial Model Summary — ملخص النموذج المالي للمستثمر

## Purpose
A summary of Dealix's financial model for investor conversations. Links to the operating finance documents in `docs/finance/`. Lean, conservative, evidence-anchored. Every projection is explicitly labelled.

## Owner
Founder. External accountant verifies actuals.

## Inputs
- `docs/finance/CASH_FLOW.md` (or equivalent).
- `docs/finance/P_AND_L.md`.
- `docs/finance/UNIT_ECONOMICS.md`.
- Active SOW pipeline.
- `docs/investor/METRICS.md` definitions.

## Outputs
- This summary.
- PDF in data room `04_financials/04_financial-model.md`.

## Model Structure
### Section 1 — Today (Last 6 Months Actuals)
- Cash revenue.
- Operating costs (founder, contractors, tools, overhead).
- Gross margin per sprint (median).
- Cash balance and runway (months).
- Sources: links to `docs/finance/`.

### Section 2 — Next 12 Months (Conservative Plan)
- Revenue assumption: ≤ historical 6-month average × 1.5.
- Cost assumption: full burn including all triggered hires per `docs/people/HIRING_TRIGGERS.md`.
- Margin assumption: at or below historical median.
- Runway projection.

### Section 3 — Scenario Analysis
- **Base**: as above.
- **Down**: -30% revenue, costs held.
- **Up**: historical median × 2, costs proportionate.
- Each scenario carries the disclosure.

### Section 4 — Unit Economics
- Average sprint price.
- Average direct delivery cost.
- Gross margin per sprint.
- Customer acquisition cost (founder hours valued at internal rate).
- Payback period.

## Rules
1. No projection beyond 12 months in this document; longer is speculation.
2. Every projected number labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
3. No "hockey stick" curves; growth assumptions conservative.
4. Costs include known hires triggered, not aspirational hires.
5. Real client data anonymized; no PII.
6. Updated quarterly with the new actuals.

## Metrics
- Variance: actuals vs prior projection (transparent reporting).
- Runway months.
- Gross margin trend.
- Burn multiple (net burn / net new ARR).

## Cadence
- Quarterly refresh.
- Re-run on every proof-gate pass.

## Evidence
- `evidence/investor/financials/<YYYY-Qn>_summary.md`.
- Source spreadsheet under access control.

## Verifier
Founder + external accountant.

## Runtime Command
`make financial-summary` — regenerates the summary from the latest actuals; refuses to publish without accountant sign-off.

## Arabic Summary — ملخص عربي
ملخص نموذج مالي للمستثمر: واقع 6 شهور، خطة 12 شهرًا متحفظة، ثلاث سيناريوهات، اقتصاديات الوحدة. لا توقعات تتجاوز 12 شهرًا. كل توقع يحمل تنويه. القيم التقديرية ليست مُتحقَّقة.
