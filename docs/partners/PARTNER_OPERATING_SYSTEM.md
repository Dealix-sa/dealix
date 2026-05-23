# Partner Operating System

## Purpose
Grow capacity through partners without losing trust or margin.

## Partner types
1. **Referral** — sends qualified leads in exchange for a one-time fee.
2. **Reseller** — sells Dealix engagements to their customers with a margin.
3. **White-label** — embeds Dealix output under their brand (with restrictions).
4. **Implementation** — does paid implementation on top of Dealix engagements.

## Lifecycle
1. Identified — listed in `partners/partner_pipeline.csv`.
2. Conversation — meeting notes captured.
3. Agreement — written terms; signed.
4. Active — sending or receiving work.
5. Paused / Ended — recorded with reason.

## Pre-conditions before signing any partner
- Aligned ICP.
- Pricing alignment (no race-to-the-bottom).
- Written terms covering: scope, exclusivity (if any), payment terms, IP, confidentiality, exit.
- Trust workflow approval.

## Cadence
- Monthly: partner pipeline review.
- Quarterly: review active partners; confirm value flowing both ways.

## Tracking
- `partners/partner_pipeline.csv`: prospects.
- `partners/partner_tracker.csv`: active relationships.

## Anti-partners
- Anyone who asks for white-label without quality control.
- Anyone who refuses written terms.
- Anyone who positions Dealix as a junior brand.

## Verifier
`python scripts/verify_people_partner_os.py`
