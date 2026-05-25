# Hiring Triggers — مُحفِّزات التوظيف

## Purpose
Define the specific repetition-based volume triggers that justify each hire. Hiring before triggers fire burns runway; hiring after triggers fire is the discipline. No hire is based on ambition or comfort.

## Owner
Founder. Triggers reviewed monthly; no hire without trigger satisfied.

## Inputs
- Volume metrics from delivery analyst.
- Founder hour audit.
- Cash and runway from `docs/finance/`.
- Active engagements list.

## Outputs
- A green/red flag per role.
- Job specification when trigger fires.
- Hire decision logged.

## The Trigger Table
| Role | Trigger (any one) | Trigger (and) | Pre-hire SOP requirement |
|---|---|---|---|
| **SDR** | ≥ 100 qualified DMs/replies per week consistent for 4 weeks | Cash ≥ 6 months runway | Outreach SOP documented and run 50+ times |
| **Delivery Analyst** | ≥ 3 sprint reports per week | 5 weekly reports per week consistent for 4 weeks | Report template stable for 8 weeks |
| **Ops Manager** | ≥ 6 active clients OR founder hours on ops > 15/week | Cash ≥ 9 months runway | Ops SOP catalogue ≥ 80% of recurring tasks |
| **Sector Analyst** | ≥ 2 sector reports per quarter required | Pipeline value justifies it | Methodology document stable |
| **Engineer (contract)** | ≥ 1 SaaS candidate passed gate | Build decision = BUILD | Architecture decision recorded |
| **Engineer (full-time)** | ≥ 2 SaaS candidates passed gate OR ≥ 1 SaaS live with ≥ 10 paying customers | Cash ≥ 12 months runway | DORA tracking active |
| **Account Executive** | ≥ 4 Strategic-tier clients on founder | Pipeline ≥ 12 month book | Sales playbook documented |

## Rules
1. Both columns must be true before posting a role.
2. Pre-hire SOP requirement is non-negotiable; you do not hire a person to figure out a process.
3. Contract before full-time wherever possible.
4. No hire to "build the company"; hire to remove a documented bottleneck.
5. Estimated savings from a hire are labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
6. Cash gate is hard; runway shortage overrides volume signal.

## Metrics
- Triggers fired per quarter.
- Hire decision time (target ≤ 60 days from trigger fire).
- Post-hire scorecard achievement at 90 days.
- Founder hours reclaimed (target ≥ 10/week per hire).

## Cadence
- Monthly trigger review.
- Quarterly recalibration.

## Evidence
- `evidence/hiring/triggers/<YYYY-MM>.md` snapshot.

## Verifier
Founder.

## Runtime Command
`make hiring-check` — prints which triggers are armed, which are red, runway status.

## Arabic Summary — ملخص عربي
لا توظيف دون تكرار يثبت الحاجة، إجراء مُوثَّق سابق التشغيل، ومخزون نقدي كافٍ. لا توظيف لاستكشاف دور، فقط لإزالة عنق زجاجة موثَّق. القيم التقديرية ليست مُتحقَّقة.
