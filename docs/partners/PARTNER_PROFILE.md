# Ideal Partner Profile — ملف الشريك المثالي

## Purpose
Define the ideal partner — what they look like, what they do, what they don't. Tighter profile = stronger partnerships. Avoids "anyone who'll talk to us" partner sprawl.

## Owner
Founder.

## Inputs
- ICP definition.
- Sector signals.
- Past partnership outcomes (good and bad).

## Outputs
- This profile.
- Inbound partner filter — Yes / Defer / No.

## Profile Dimensions
### Agency Partner
- Saudi-registered, 3+ years operating.
- 5+ active B2B clients in Dealix's target sectors.
- A documented delivery methodology (we are not their methodology).
- Bilingual operating team.
- No competing AI-services brand they want to favor.

### Sector Specialist
- 7+ years operating in the named sector.
- Published or referenced work (LinkedIn, sector report, regulator).
- No active competing engagement with a Dealix competitor.
- Bilingual fluency.

### Referral Partner
- Active relationships with our ICP (Saudi B2B founders, commercial leaders).
- Reputation we are comfortable being associated with publicly.
- Willing to follow `docs/partners/REFERRAL_TERMS.md`.

## Disqualifiers (Any One)
1. History of scraping, cold blast, or PDPL violation.
2. Reputation for over-promising or hidden fees.
3. Equity or exclusivity demands.
4. Pressure to skip Dealix's non-negotiables (banned practices).
5. Conflict of interest with a strategic Dealix client.
6. Misalignment with Saudi business norms or compliance expectations.

## Rules
1. Founder personally interviews every potential partner before signing.
2. Reference checks: minimum 2 named references contacted.
3. Trial deal before any long-term commitment.
4. Profile is reviewed quarterly; tightened when partner sprawl signals appear.
5. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to projected joint economics.

## Metrics
- Inbound partner inquiries: filtered Yes / Defer / No counts.
- Trial-to-permanent conversion rate.
- Partner-sourced deal close rate (vs direct).
- Disqualifier hits (target small but non-zero; signals discipline).

## Cadence
- Quarterly profile review.

## Evidence
- `evidence/partners/profile/<YYYY-Qn>.md`.

## Verifier
Founder.

## Runtime Command
`make partner-profile-check NAME=<partner>` — runs the disqualifier checklist before any further onboarding step.

## Arabic Summary — ملخص عربي
ملف شريك مثالي مُحدَّد بدقة: وكالة، متخصص قطاع، مُحيل. مرفوض من تجاوز الممارسات المحظورة، أو طالب حصرية وأسهم، أو تعارض مصالح. القيم التقديرية ليست مُتحقَّقة.
