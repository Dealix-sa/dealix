# Client Health Score — مؤشر صحة العميل

## Purpose
A single 0-100 score per active client, computed from 5 factors. Drives the client success dashboard, triggers retention playbook below threshold, and supports renewal conversation timing.

## Owner
Delivery analyst computes. Founder reviews weekly.

## Inputs
- Weekly report acknowledgment.
- Outcome delivery vs SOW.
- Feedback log entries.
- Payment timeliness.
- Engagement signals (response time, attendance at calls).

## The Five Factors (20 points each)
| Factor | Definition | Scoring |
|---|---|---|
| Delivery | On-time, on-scope shipments | 20 if 100%, -5 per miss |
| Outcome | Verified outcome vs goal | 20 if ≥ 100%, scaled down |
| Engagement | Calls attended, replies within agreed SLA | 20 if 100%, -5 per miss |
| Sentiment | Feedback tone, NPS, escalations | 20 if positive, 10 neutral, 0 negative |
| Payment | Invoices paid within terms | 20 if on time, -10 per late invoice |

Total: 0-100.

## Bands
| Band | Range | Action |
|---|---|---|
| Strong | 80-100 | Standard cadence, upsell readiness review |
| Stable | 60-79 | Standard cadence, watch for drift |
| Watch | 40-59 | Founder review within 7 days |
| At-Risk | 0-39 | Trigger `docs/client_success/RETENTION_PLAYBOOK.md` within 48h |

## Rules
1. Score updated every Friday based on the week's evidence.
2. No score without evidence for each factor; missing evidence scores zero.
3. A negative sentiment incident drops Sentiment to 0 regardless of other signals.
4. Late payment > 30 days drops Payment to 0 and flags At-Risk.
5. No score visible to client without founder approval.
6. Estimated outcome figures labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Metrics
- Median health score across book.
- Count at-risk.
- Score volatility (week-over-week change).
- False-positive at-risk rate.

## Cadence
- Weekly: scored every Friday.
- Monthly: trend review.
- Quarterly: factor weighting recalibration.

## Evidence
- `evidence/client-success/health/<client_id>/<YYYY-Www>.md`.

## Verifier
Founder spot-checks 1 random score per week.

## Runtime Command
`make health-score CLIENT=<id> WEEK=<YYYY-Www>` — computes the score from logged evidence; refuses to score without minimum evidence per factor.

## Arabic Summary — ملخص عربي
مؤشر صحة من 0 إلى 100 لكل عميل، مبني على خمسة عوامل بـ 20 نقطة لكل عامل. تحت 40 = خطر، يُفعَّل دليل الاحتفاظ خلال 48 ساعة. القيم التقديرية ليست مُتحقَّقة.
