# Ultimate Finance OS | نظام المالية الشامل

## Purpose | الغرض
The single source of truth for Dealix's money: cash, MRR, pipeline, costs, runway,
and unit economics. Powers the founder's daily and weekly decisions about where to
spend time and where to allocate capital.

Finance OS reports. It does not transact externally without explicit founder
approval (via Payment Capture OS).

## Inputs | المدخلات
- Payment Capture OS (invoices, payments, refunds)
- Bank reconciliation feed
- Pipeline data from Revenue Factory OS
- Cost ledger (tooling, AI, infra, contractors, taxes)
- AI Unit Economics System inputs
- Founder personal-burn data (optional)

## Outputs | المخرجات
- `finance.ledger`: canonical transaction store
- Daily cash position dashboard
- Weekly P&L snapshot
- Monthly close package (cash, MRR, AR, AP, runway)
- Quarterly capital allocation memo (drafted, founder approves)

## Core reports | التقارير الأساسية
1. **Cash position** — bank balance + AR aging + AP aging
2. **MRR + ARR** — by client, by service line, with churn breakdown
3. **Pipeline value** — raw and weighted (by stage probability)
4. **Cost stack** — AI, infra, tools, contractors, taxes, founder cost
5. **Unit economics** — see AI Unit Economics System
6. **Runway** — months of cash given current burn + commitments
7. **Cohort retention** — by client onboard cohort

## Close rhythm | إيقاع الإقفال
- Daily: cash position refresh
- Weekly: pipeline + AR/AP refresh, founder review
- Monthly: P&L close, unit-economics refresh, runway update
- Quarterly: capital allocation memo + board-style deck (internal)

## Capital allocation | تخصيص رأس المال
- All capital allocation decisions made by founder
- Worker drafts memo with options and tradeoffs
- No automated capital movements; all transfers manual

## Data source | مصدر البيانات
`finance.ledger`, `finance.invoices`, `finance.payments`, `finance.costs`,
`pipeline.snapshots`.

## Approval class | فئة الموافقة
- A1: reporting, close calculations, dashboards
- A2: capital allocation memo publication, anything externally shared
- A3: any movement of capital, any tax / regulatory filing

## Trust gate | بوابة الثقة
- No forecast presented as a guarantee
- All numbers traceable to ledger entries
- Forex rates pinned at transaction time
- No external sharing of finance data without founder approval
- Policy snapshot + audit row per published report

## Owner | المالك
Founder owns capital allocation. Worker owns reporting accuracy.

## Worker name
`finance.ultimate_os`

## KPI | المؤشرات
- Cash collected (monthly)
- MRR + ARR
- Runway (months)
- Gross margin %
- AR aging health
- Forecast accuracy (forecast vs actual over rolling 90d)

## Failure mode | حالات الفشل
- Ledger mismatch between bank feed and internal records
- Forecast drift unnoticed
- Manual cost categorization errors inflate apparent gross margin

## Recovery path | مسار الاسترداد
- Daily bank-to-ledger reconciliation; mismatches halt reports until resolved
- Forecast-vs-actual scorecard weekly
- Random sample of cost categorizations reviewed monthly by founder
