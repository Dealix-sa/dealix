# Email Deliverability v2

## Relationship to existing docs
Extends, does not replace:
- `docs/ops/EMAIL_DELIVERABILITY.md` — the existing operational checklist.
- `docs/trust/SUPPRESSION_AND_OPTOUT_SYSTEM.md` — the suppression gate every send must pass.
- `docs/distribution/DISTRIBUTION_PORTFOLIO_V2.md` (Email Drafts channel).

## Purpose
Protect Dealix sending reputation while running approved outbound.

## Setup
- dedicated sending domain/subdomain
- SPF
- DKIM
- DMARC
- bounce tracking
- suppression list
- opt-out handling
- daily volume caps

## Warmup Rules
- Start 10–25 approved sends/day.
- Increase only when bounce and negative signals are low.
- Reduce if opt-outs or bad replies increase.
- Do not use purchased personal lists.

## Sending Rules
- relevant only
- personalized context
- no guaranteed claims
- no misleading subject lines
- stop after opt-out

## Approval Gate
Every Gmail draft is created **after** the approval gate in `docs/founder/approval_center.md` records an explicit approval. No draft is created from the outreach queue while `approval_status` is `pending` or `needs edit`.
