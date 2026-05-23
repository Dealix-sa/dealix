# Ops Manager Scorecard — بطاقة أداء مدير العمليات

## Purpose
Weekly scorecard for the ops manager — the role that runs the back office, maintains scorecards, coordinates contractors, and protects the founder's calendar. Tracks reliability, founder-time reclaimed, and process improvement.

## Owner
Founder.

## Inputs
- Calendar audit (founder hours by category).
- Scorecard completion log.
- Contractor coordination log.
- SOP additions and updates.
- Process incidents (missed deadlines, errors).

## Outputs
- Weekly scorecard under `evidence/people/ops-manager/<YYYY-Www>.md`.
- Monthly process-improvement report.
- Quarterly review.

## Scorecard Table
| Section | Metric | Target | Weight |
|---|---|---|---|
| Reliability | Scheduled tasks completed | 100% | 20 |
| Reliability | Scorecards filed on time | 100% | 10 |
| Founder time | Founder hours reclaimed (estimated, labelled) | ≥ 10/week | 20 |
| Coordination | Contractor reviews completed | 100% | 10 |
| Process | SOP additions or improvements | ≥ 2/month | 15 |
| Process | Process incidents (missed, errors) | ≤ 2/month | 15 |
| Discipline | Evidence attached | 100% | 10 |

Total: 100 points.

## Rules
1. Ops manager does not make strategic decisions (see `docs/people/DELEGATION_RULES.md`).
2. Founder-time reclaimed is estimated and labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
3. Process incidents are logged with 5-Why; no blame-naming.
4. Contractor coordination follows `docs/people/CONTRACTOR_ONBOARDING.md`.
5. PII compliance per `docs/14_trust_os/`.
6. Score below 70 for 2 weeks triggers founder review.

## Metrics
- Founder hours reclaimed (rolling 4-week).
- Process incident rate.
- SOP additions per quarter.
- Scorecard on-time rate across the org.

## Cadence
- Weekly scorecard.
- Weekly 30-min 1:1.
- Monthly process report.

## Evidence
- Calendar diffs, scorecard logs, SOP commits.

## Verifier
Founder.

## Runtime Command
`make ops-scorecard WEEK=<YYYY-Www>` — pulls logs, computes score, prints incident log.

## Arabic Summary — ملخص عربي
بطاقة أداء أسبوعية لمدير العمليات: موثوقية، وقت مُستردّ للمؤسس، عمليات. لا قرارات استراتيجية في هذا الدور. القيم التقديرية ليست مُتحقَّقة.
