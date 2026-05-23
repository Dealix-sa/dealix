# Delivery Analyst Scorecard — بطاقة أداء محلل التسليم

## Purpose
Weekly scorecard for the delivery analyst — the role that runs sprints, drafts weekly client reports, and feeds productization. Tracks on-time delivery, quality of output, and contribution to playbooks.

## Owner
Founder pre-hire. Ops manager or founder post-hire.

## Inputs
- Sprint delivery log.
- Weekly report sent timestamps.
- Rework log.
- Productization signals captured.

## Outputs
- Weekly scorecard under `evidence/people/delivery-analyst/<YYYY-Www>.md`.
- Monthly trend.
- Quarterly review.

## Scorecard Table
| Section | Metric | Target | Weight |
|---|---|---|---|
| Delivery | Sprint milestones on time | 100% | 20 |
| Delivery | Weekly client reports on time | 100% | 15 |
| Quality | Rework rate (revisions before client accept) | ≤ 10% | 15 |
| Quality | Founder edits on weekly reports | ≤ 10% changes | 10 |
| Productization | New SOP / template contributions | ≥ 1/month | 10 |
| Productization | Productization signals filed | ≥ 1/month | 5 |
| Discipline | Evidence attached to every artifact | 100% | 15 |
| Discipline | PII compliance | 100% | 10 |

Total: 100 points.

## Rules
1. No client artifact shipped without evidence link.
2. No PII in shared workspaces; redacted before filing.
3. No promise to clients without founder approval.
4. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" on any estimated outcome.
5. Score below 70 for 2 consecutive weeks triggers SOP review and coaching.
6. No invented outcomes; "we don't know" is acceptable and required.

## Metrics
- On-time delivery rate.
- Rework rate.
- Founder-edit rate (proxy for trust and consistency).
- Productization contributions per quarter.

## Cadence
- Weekly scorecard.
- Weekly 30-min 1:1.
- Monthly trend.

## Evidence
- Sprint logs, report timestamps, rework log.

## Verifier
Founder.

## Runtime Command
`make analyst-scorecard WEEK=<YYYY-Www>` — pulls evidence, computes score, refuses without rework log entries.

## Arabic Summary — ملخص عربي
بطاقة أداء أسبوعية لمحلل التسليم: تسليم، جودة، مساهمة في الإجراءات. لا أرتيفاكت بدون دليل، لا بيانات شخصية في المشاركات. القيم التقديرية ليست مُتحقَّقة.
