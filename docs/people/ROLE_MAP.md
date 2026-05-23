# Role Map — خريطة الأدوار

## Purpose
The current org chart and the 12-month role roadmap. Maps named accountabilities to people (or to the founder, where no one is hired). Public-safe version omits personal data.

## Owner
Founder.

## Inputs
- Active contracts and employment relationships.
- `docs/people/HIRING_TRIGGERS.md` planned roles.
- `docs/founder/CEO_OPERATING_MODEL.md` accountabilities.

## Outputs
- Current org chart (markdown).
- 12-month role roadmap.
- Accountability index (one accountability → one role).

## Current State (T-0)
| Function | Role | Holder | Status |
|---|---|---|---|
| Strategy / CEO | Founder | Bassam | Permanent |
| Sales (SDR + AE) | Founder | Bassam | Until SDR trigger |
| Delivery lead | Founder | Bassam | Until analyst trigger |
| Content / voice | Founder | Bassam | Permanent (drafts may be delegated) |
| Finance | Founder + bookkeeper (contract) | Bassam + TBD | Bookkeeper contract |
| Legal / compliance | External counsel (contract) | TBD | Per-engagement |
| Engineering (build) | Founder + contractor (per-build) | Bassam + TBD | Per-build |

## 12-Month Role Roadmap (Conditional on Triggers)
| Month | Role | Trigger Source |
|---|---|---|
| 0-3 | None hired. Founder runs everything. | Pre-trigger |
| 3-6 | Delivery analyst (contract → part-time) | 3 sprint reports/week consistent |
| 6-9 | SDR (contract → part-time) | 100 DMs/week consistent |
| 9-12 | Ops manager (contract) | 6 active clients OR ops hours > 15/week |
| 12-18 | Engineer (contract → full-time) | SaaS candidate passed gate |

## Rules
1. One accountability has exactly one role; no shared accountability.
2. No role added without a trigger fired (`docs/people/HIRING_TRIGGERS.md`).
3. Contract before full-time; trial period mandatory.
4. Role description in writing; scorecard attached.
5. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to projected role economics.
6. PII (full names, contacts) limited to founder-only files; this file uses first name + initial.

## Metrics
- Roles filled vs roadmap.
- Time from trigger to hire (target ≤ 60 days).
- Trial-period conversion rate.
- Accountability gaps (target 0; gap = a function with no named owner).

## Cadence
- Monthly role-map review.
- Quarterly roadmap reshuffle.

## Evidence
- `evidence/people/role-map/<YYYY-MM>.md`.

## Verifier
Founder.

## Runtime Command
`make role-map` — prints current state and roadmap, flags accountability gaps.

## Arabic Summary — ملخص عربي
خريطة الأدوار الحالية وخطة 12 شهرًا. كل مسؤولية لها مالك واحد. لا دور يُضاف دون مُحفِّز يطلق، وعقد مرحلي قبل التفرغ. القيم التقديرية ليست مُتحقَّقة.
