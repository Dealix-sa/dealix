# Feedback Loop — حلقة التغذية الراجعة

## Purpose
Define when and how feedback is collected from active clients, ex-clients, and lost prospects. Feedback is structured evidence, not vibes. Feeds productization, content, and retention.

## Owner
Founder. Analyst administers.

## Inputs
- Active engagements.
- Closed engagements (renewal or churn).
- Lost-deal prospects.

## Outputs
- Structured feedback entries under `evidence/feedback/<id>/`.
- Themes summary monthly.
- Productization signal fed into `docs/product/PRODUCTIZATION_COMMAND_CENTER.md`.
- Content idea backlog updates.

## Touchpoints
| Stage | Method | When |
|---|---|---|
| Day 7 onboarding | 15-min call, 5 questions | Once |
| Mid-sprint | 1 message, 3 questions | Every 2 weeks |
| Sprint close | 30-min call, structured | Once per sprint |
| Renewal | 45-min call, full questionnaire | 30 days before renewal |
| Churn | 30-min call, structured exit | Within 14 days of churn |
| Lost deal | 1 short call or written reply | Within 14 days of loss |

## Question Frames
- Did Dealix deliver what was promised in the SOW? (yes/no + evidence)
- What would have made the engagement 1 point higher on NPS?
- What did Dealix do that surprised you (positive or negative)?
- Would you renew, expand, or stop? Why?
- (Renewal) What new outcome would justify expansion?
- (Churn) What would change your decision?
- (Lost) What did the winning option offer?

## Rules
1. No leading questions. No "great call, right?".
2. All feedback recorded in writing within 24 hours of capture.
3. Direct quotes used only with verbal or written permission; otherwise paraphrased.
4. PII removed before storing in shared evidence folders.
5. Themes summarized monthly; counted by frequency, not strength of voice.
6. Estimated impact figures shared in feedback recap labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Metrics
- Touchpoint completion rate (target 100% for onboarding and sprint-close).
- NPS-style score (median).
- Theme frequency (top 5 monthly).
- Productization signals captured per quarter.

## Cadence
- Per touchpoint as above.
- Monthly theme review.
- Quarterly recalibration of questions.

## Evidence
- Per-feedback entry with date, channel, summary.
- Permission record for quotes.

## Verifier
Founder.

## Runtime Command
`make feedback-collect CLIENT=<id> STAGE=<name>` — opens the question set, refuses to file without all required fields and permission tag.

## Arabic Summary — ملخص عربي
حلقة تغذية راجعة منظمة عبر مراحل العمل: بعد سبعة أيام، منتصف السباق، إغلاق السباق، التجديد، الانفصال، الصفقة المفقودة. لا أسئلة موجِّهة. الاقتباسات بإذن. القيم التقديرية ليست مُتحقَّقة.
