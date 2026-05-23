# Partner Scorecard — بطاقة أداء الشريك

## Purpose
Monthly scorecard for every active partner. Activity, quality, and outcome — in that priority order. Triggers continuation, coaching, or amicable close.

## Owner
Founder. Ops manager maintains the data.

## Inputs
- Referral / introduction log.
- Joint engagement work log.
- Client feedback referencing the partner.
- Compliance and behavior incidents (banned practices, communications).

## Outputs
- Monthly scorecard under `evidence/partners/<partner_id>/scorecard/<YYYY-MM>.md`.
- Quarterly partner portfolio review.

## Scorecard Table
| Section | Metric | Target | Weight |
|---|---|---|---|
| Activity | Qualified introductions or active joint engagements | varies by type | 20 |
| Activity | Cadence: monthly check-ins held | 100% | 10 |
| Quality | Intro qualification rate (referral partners) | ≥ 60% qualified | 15 |
| Quality | Client satisfaction citing partner (agency / specialist) | ≥ 4/5 | 15 |
| Outcome | Closed deals (referral) or shipped milestones (agency) | varies | 20 |
| Outcome | Revenue contributed (verified, not estimated) | tracked | 10 |
| Discipline | Banned-practice incidents | 0 | 10 |

Total: 100 points.

## Bands
| Band | Range | Action |
|---|---|---|
| Strong | 80-100 | Continue, consider scope expansion |
| Stable | 60-79 | Continue with coaching |
| Watch | 40-59 | 30-day improvement plan |
| At-Risk | 0-39 | Amicable close conversation |

## Rules
1. Banned-practice incident drops score to 0 regardless of other signals.
2. No scope expansion proposed below Strong band.
3. At-Risk band triggers amicable close conversation within 14 days.
4. Verified revenue only; estimated revenue labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
5. Partner score not shared externally without partner consent.
6. Score below 70 for 2 consecutive months triggers founder review.

## Metrics
- Median partner score.
- Count by band.
- Band movement quarter-over-quarter.
- Amicable-close count (acceptable; signals discipline).

## Cadence
- Monthly scorecard.
- Quarterly portfolio review.

## Evidence
- Logs, feedback, incident records.

## Verifier
Founder.

## Runtime Command
`make partner-scorecard ID=<partner> MONTH=<YYYY-MM>` — pulls logs, computes score, refuses close without incident review.

## Arabic Summary — ملخص عربي
بطاقة أداء شهرية لكل شريك: نشاط، جودة، نتيجة، انضباط. حادثة ممارسة محظورة تُصفِّر النتيجة. دون 40 = خاتمة ودية خلال 14 يومًا. القيم التقديرية ليست مُتحقَّقة.
