# Risk Register — سجل المخاطر

## Purpose
A summary of business and AI risks, with current mitigation, owner, and review cadence. Investor-safe view. Mirrors the operating risk log in `docs/14_trust_os/` but redacted of client-specific detail.

## Owner
Founder. Reviewed monthly.

## Inputs
- Incident log from `docs/14_trust_os/`.
- A3 entries from operating reviews.
- Engineering health reviews.
- Compliance assessments.

## Outputs
- This register.
- Risk pack in data room `08_risk/`.

## Register Schema
| ID | Category | Risk | Likelihood | Impact | Mitigation | Owner | Last review |
|---|---|---|---|---|---|---|---|
| R-001 | Concentration | Single client > 30% revenue | M | H | Tier+upsell+pipeline diversification | Founder | quarterly |
| R-002 | Data | PDPL non-compliance | L | H | Trust OS, audits, training | Founder | quarterly |
| R-003 | AI | Hallucination in client artifact | M | H | Provenance log, human review, refusal rules | Founder | monthly |
| R-004 | AI | Model deprecation breaks workflow | M | M | Model portfolio, fallback paths | Founder | monthly |
| R-005 | Vendor | LLM provider outage | M | M | Multi-provider gateway design | Founder | quarterly |
| R-006 | Talent | Founder over-allocation | H | H | Delegation rules, hiring triggers | Founder | weekly |
| R-007 | Cash | Runway < 6 months | M | H | Cash dashboard, kill criteria | Founder | weekly |
| R-008 | Legal | Banned-practice incident | L | H | Acknowledgment forms, training, audits | Founder | quarterly |
| R-009 | Reputation | Client public dissatisfaction | L | H | Retention playbook, weekly reports | Founder | monthly |
| R-010 | Productization | Premature SaaS bet | L | H | Productization gates, no-overbuild policy | Founder | quarterly |
| R-011 | Compliance | SDAIA AI policy change | M | M | Policy watch, quarterly review | Founder | quarterly |
| R-012 | Market | Sector slowdown affects pipeline | M | M | Sector diversification (long term), conservative model | Founder | quarterly |

## Rules
1. Every risk has a named owner, a mitigation, and a review cadence.
2. New risks added when observed; not invented for theatre.
3. Critical risks (M+H) reviewed monthly; others quarterly.
4. PII never in this register.
5. Estimated impact figures labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
6. No risk silently retired; explicit decision when closed.

## Metrics
- Risk count by likelihood × impact band.
- Open critical risks.
- Review on-time rate.
- Mitigation completion (where time-bound).

## Cadence
- Monthly: critical risks.
- Quarterly: full register.

## Evidence
- `evidence/investor/risk/<YYYY-Qn>.md`.

## Verifier
Founder.

## Runtime Command
`make risk-review` — prints the register, flags overdue reviews, sorts by likelihood × impact.

## Arabic Summary — ملخص عربي
سجل مخاطر بفئات: تركيز، بيانات، ذكاء اصطناعي، مورد، كادر، نقد، قانون، سمعة، تحويل لمنتج، التزام، سوق. لكل خطر مالك، تخفيف، إيقاع مراجعة. القيم التقديرية ليست مُتحقَّقة.
