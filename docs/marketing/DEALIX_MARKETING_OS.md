# Dealix Marketing OS

The Marketing OS is the system that turns Dealix positioning into a continuous stream of evidence-forward artifacts that earn attention without manufactured urgency.

**Source of truth:** `$PRIVATE_OPS/marketing_state.csv`
**Owner:** Marketing Lead + Founder
**Trust gate:** A1 for content publish; A2 for paid distribution, partner channels, and public proof.

## Charter

Marketing is responsible for:

1. Publishing artifacts that demonstrate Dealix understands Saudi B2B revenue mechanics.
2. Producing distribution that respects the no-cold-automation rule.
3. Sourcing inbound that the Revenue Factory can convert.
4. Stewarding the brand voice and the disclosure discipline.

Marketing does not own pricing, scope, or contract decisions.

## Surfaces

| Surface | Artifact | Cadence | Doc |
|---------|----------|---------|-----|
| Public site | Landing pages | Monthly review | `docs/marketing/LANDING_PAGE_CONVERSION_SYSTEM.md` |
| Founder voice | Posts | 2-3 / week | `docs/marketing/FOUNDER_LED_CONTENT_SYSTEM.md` |
| Newsletter | Weekly digest | Weekly | `docs/marketing/NEWSLETTER_SYSTEM.md` |
| Sector reports | Long-form study | Monthly | `docs/marketing/SECTOR_REPORT_SYSTEM.md` |
| Partner | Enablement pack | Quarterly | `docs/marketing/PARTNER_OUTREACH_GUIDE.md` |
| Email | Considered outreach | Per opportunity | `docs/marketing/EMAIL_OUTREACH_GUIDE.md` |
| LinkedIn | Considered outreach | Per opportunity | `docs/marketing/LINKEDIN_OUTREACH_GUIDE.md` |

## Production process

1. Calendar: planned in `docs/marketing/CONTENT_CALENDAR_SYSTEM.md`.
2. Brief: source links, claim list, citation list.
3. Draft: produced by human or by agent under Content Strategist supervision (`docs/ai/CONTENT_STRATEGIST_AGENT.md`).
4. Lint: copywriting rules check (`docs/marketing/COPYWRITING_RULES.md`).
5. Bilingual: EN and AR with parity.
6. Review: Brand Guardian (`docs/ai/BRAND_GUARDIAN_AGENT.md`).
7. Founder approves at A1.
8. Publish and log.

## Disclosure

Every public artifact carries the disclaimer "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" where any quantitative claim is made.

## Failure modes

- **Hype drift:** copy slides toward marketing fluff. Detection: weekly audit. Recovery: rewrite against `docs/marketing/COPYWRITING_RULES.md`.
- **Source missing:** a claim is published without a traceable source. Detection: lint. Recovery: cite or remove.
- **Bilingual asymmetry:** EN published, AR delayed. Detection: parity check. Recovery: AR is a publish blocker.

## Recovery path

If marketing publishes a defective artifact (false claim, PII leak), the founder pulls it within 24 hours, issues a public correction in EN and AR, and files a root cause in `$PRIVATE_OPS/marketing_incidents.csv`.

## Metrics

- Artifacts published per week by surface.
- Inbound leads by artifact (estimated).
- Founder-approval-cycle time.
- Correction count per quarter (target: 0).

## Disclaimer

Marketing creates conversation. The Revenue Factory creates revenue. Dealix does not guarantee revenue from marketing activity. Estimated value is not Verified value.
