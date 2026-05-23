# SDR Scorecard — بطاقة أداء مندوب التطوير

## Purpose
Weekly scorecard for the SDR role (Sales Development Representative). Pre-hire, the founder fills this for their own outbound. Post-hire, used in 1:1 reviews. Tracks activity, quality, and outcomes — in that priority order.

## Owner
Founder pre-hire. Ops manager or founder post-hire.

## Inputs
- Outreach log (manual entries, no scraping, no automation).
- Reply log.
- Qualified-meeting log.
- Pipeline contribution.

## Outputs
- Weekly scorecard filed under `evidence/people/sdr/<YYYY-Www>.md`.
- Monthly trend.
- Quarterly performance review.

## Scorecard Table
| Section | Metric | Target | Weight |
|---|---|---|---|
| Activity | Qualified outreach attempts | 100/week | 20 |
| Activity | Personalized touches (≥ 3 sentences) | 80/week | 10 |
| Quality | Reply rate | ≥ 8% | 15 |
| Quality | Qualified-reply rate | ≥ 3% | 15 |
| Outcome | Qualified meetings booked | ≥ 5/week | 20 |
| Outcome | Pipeline value added (estimated, labelled) | tracked, not scored | 0 |
| Discipline | SOP compliance | 100% | 10 |
| Discipline | No banned channels (cold WhatsApp, scraped lists) | 100% | 10 |

Total: 100 points.

## Rules
1. No cold WhatsApp, no LinkedIn automation, no scraped or purchased lists.
2. Every outreach individually composed; templates allowed, automation not.
3. The SDR cannot promise outcomes Dealix cannot deliver.
4. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" appears on any pipeline projection.
5. PII handling per `docs/14_trust_os/`.
6. Score below 70 for 2 consecutive weeks triggers SOP review and coaching.

## Metrics
- Activity-quality-outcome ratio (balanced, not stuffed at activity).
- Cost per qualified meeting.
- Conversion meeting → SOW.
- Banned-channel incidents (target 0).

## Cadence
- Weekly scorecard filed Monday for prior week.
- Weekly 30-min 1:1.
- Monthly trend review.

## Evidence
- Outreach log, reply log, meeting log.

## Verifier
Founder.

## Runtime Command
`make sdr-scorecard WEEK=<YYYY-Www>` — pulls logs, computes score, refuses to close without all sections.

## Arabic Summary — ملخص عربي
بطاقة أداء أسبوعية لمندوب التطوير: نشاط، جودة، نتيجة — بهذا الترتيب. لا قنوات محظورة، لا أتمتة، لا قوائم مسروقة. القيم التقديرية ليست مُتحقَّقة.
