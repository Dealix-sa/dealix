# Investor Metrics Definitions — تعريفات مقاييس المستثمر

## Purpose
Definitions of every metric Dealix reports to investors and board. Eliminates ambiguity. What is included, what is excluded, who computes it, and how it ties to operating evidence.

## Owner
Founder. Definitions reviewed annually.

## Inputs
- `docs/finance/` for revenue and cost definitions.
- `docs/client_success/` for retention metrics.
- `docs/product/` for product / engineering metrics.
- `docs/people/` for delivery capacity metrics.

## Outputs
- This document.
- Per-metric methodology note used in any investor pack.

## Revenue Metrics
| Metric | Definition | Source |
|---|---|---|
| Cash Revenue | SAR collected in period | Bank statements |
| Accrual Revenue | SAR earned in period (services rendered) | Sprint completion log |
| MRR (when retainer) | Sum of monthly recurring fees of active retainers | Active SOWs |
| ARR | MRR × 12 | Computed |
| New ARR | ARR added from new SOWs | Computed |
| Churned ARR | ARR lost from non-renewals + downgrades | Computed |
| Net Revenue Retention | (Starting ARR + Expansion − Churn − Contraction) / Starting ARR | 12-month rolling |

## Sales / Pipeline Metrics
| Metric | Definition |
|---|---|
| Qualified opportunity | Confirmed buyer intent, scope discussion held |
| Pipeline value | Sum of qualified opportunity expected SAR |
| Win rate | Closed-won / (Closed-won + Closed-lost) |
| Sales cycle (median) | Days from qualified opp to signed SOW |

## Delivery / Operations Metrics
| Metric | Definition |
|---|---|
| Sprint on-time rate | % of sprint milestones delivered on or before due date |
| Rework rate | % of artifacts revised after client first review |
| Gross margin per sprint | (Sprint revenue − direct delivery cost) / Sprint revenue |
| Founder hours per sprint | Tracked manually |

## Trust / Risk Metrics
| Metric | Definition |
|---|---|
| Incident count | Per `docs/14_trust_os/` log |
| Critical incidents | Severity 1-2 |
| Banned-practice incidents | Hard zero target |
| PDPL findings | From audits |

## Product Metrics (Post-SaaS Only)
DORA four, defined in `docs/product/DORA_METRICS_POLICY.md`.

## Rules
1. Every metric reported to an investor has a methodology footnote.
2. Estimated values labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
3. PII not exposed in any metric report; aggregate or anonymized only.
4. No metric invented for an investor; if we don't track it, we say so.
5. Definitions modified only at year-end; no mid-year redefinitions.

## Metrics About Metrics
- Definition stability (changes per year, target ≤ 2).
- Methodology completeness (every reported metric has a note).
- Reconciliation accuracy (computed vs source, target 100%).

## Cadence
- Annual definitions review.
- Monthly metric refresh.

## Evidence
- `evidence/investor/metrics/<YYYY-MM>_methodology.md`.

## Verifier
Founder. External accountant verifies financial definitions.

## Runtime Command
`make metrics-pack MONTH=<YYYY-MM>` — generates the monthly metric pack with footnotes.

## Arabic Summary — ملخص عربي
تعريفات مقاييس المستثمر: إيراد، خط مبيعات، تسليم، ثقة، منتج. كل مقياس له هامش منهجي. لا تعريف يُعدَّل في منتصف العام. لا اختراع مقاييس للمستثمرين. القيم التقديرية ليست مُتحقَّقة.
