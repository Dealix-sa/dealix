# AI Unit Economics System | نظام اقتصاديات الوحدة بالذكاء الاصطناعي

## Purpose | الغرض
Measure the actual economics of an AI-powered, founder-led revenue operating
company. Show, transparently, whether every AI dollar spent generates more pipeline,
more proposals, more paid clients — and how much founder time it saves.

These metrics drive capital allocation and tooling decisions.

## Inputs | المدخلات
- Payment Capture OS (cash, invoices)
- Revenue Factory OS (pipeline, proposals, paid clients)
- LLM Gateway cost telemetry (per worker, per stage)
- Tooling cost ledger (LinkedIn tools, email infra, CRM, design, hosting)
- Time-tracking on founder hours saved (semi-automatic, per workflow)
- Cost stack from Ultimate Finance OS

## Outputs | المخرجات
- `unit_econ.snapshots`: snapshot_date + every metric below
- Monthly unit-economics dashboard (founder-facing)
- Quarterly investor-grade summary (drafted, founder approves)

## Tracked metrics | المقاييس المتتبعة
| Metric | Definition | Source |
|---|---|---|
| Cash collected | Sum of payments captured in period | Payment Capture OS |
| MRR | Recurring monthly revenue at period end | Ultimate Finance OS |
| Pipeline | Sum of all open opportunities by stated value | Revenue Factory OS |
| Weighted pipeline | Pipeline × stage probability | Revenue Factory OS |
| Proposal value | Sum of all proposals sent in period | Proposal Factory |
| Payment follow-ups | # follow-up sends needed per invoice | Payment Capture OS |
| Gross margin | (Revenue - direct costs) / Revenue | Ultimate Finance OS |
| AI cost per lead | LLM + tool cost / # qualified leads | LLM Gateway + Intelligence |
| AI cost per proposal | LLM + tool cost / # proposals sent | LLM Gateway + Proposal Factory |
| AI cost per paid client | LLM + tool cost / # paid clients | LLM Gateway + Revenue Factory |
| Founder hours saved | Estimated hours saved by automation | Workflow telemetry |
| Tool cost | Monthly recurring tooling spend | Cost ledger |
| Runway | Months of cash at current burn | Ultimate Finance OS |

## Allocation rules | قواعد التوزيع
- AI cost is split per worker, per stage, then attributed to the lead / proposal
  / paid client that triggered it
- Tooling cost is split prorata across active workers
- Founder time saved is estimated using before/after workflow timings,
  recalibrated quarterly

## Decision rules | قواعد القرار
- If AI cost per paid client > 5% of gross margin per client → triage spend
- If founder hours saved per dollar of AI cost falls below threshold → revisit
- If runway < 6 months → triage all discretionary spend, draft memo

## Data source | مصدر البيانات
`unit_econ.snapshots`, `llm.gateway.cost_log`, `finance.ledger`,
`workflow.timings`.

## Approval class | فئة الموافقة
- A1: monthly snapshot computation, internal dashboards
- A2: investor-grade quarterly summary publication
- A3: any external benchmark publication

## Trust gate | بوابة الثقة
- No metric presented without source attribution
- No forecasts presented as guarantees
- No client-identifying data in published unit-economics summaries
- Policy snapshot + audit row per snapshot publication

## Owner | المالك
Founder owns capital allocation decisions; worker owns computation accuracy.

## Worker name
`finance.ai_unit_economics`

## KPI | المؤشرات
- AI cost per paid client (trend should fall)
- Founder hours saved per month (trend should rise)
- Gross margin % (trend should rise)
- Forecast accuracy of unit-economics projections

## Failure mode | حالات الفشل
- Cost attribution drift (LLM cost attributed to wrong stage)
- Founder-hours-saved estimate becomes wishful thinking
- Runway computation excludes a known commitment

## Recovery path | مسار الاسترداد
- Quarterly cost-attribution audit; recalibrate per-stage shares
- Hours-saved estimates require periodic ground-truth measurement
- Runway includes a "known commitments" sweep before publish
