# Distribution Portfolio v2

## Relationship to existing docs
Sits above the existing distribution machinery:
- `auto_client_acquisition/` modules — the operational primitives this portfolio coordinates.
- `docs/ops/pipeline_tracker.csv` and `docs/ops/CEO_TOP50_TRACKER.csv` — the existing tracking surfaces.
- `docs/distribution/EXPERIMENT_ENGINE_V2.md` — the evidence loop that gates the weekly decisions below.

## Purpose
Run Dealix across multiple channels so growth does not depend on one source.

## Channels

### Founder-Led Outbound
High-context, approved outreach to scored A/B leads.

### Contact Forms
Company-level low-risk contact via public forms.

### LinkedIn Manual
Founder-led manual conversations with decision makers.

### Email Drafts
Gmail drafts created only after approval (see `docs/distribution/EMAIL_DELIVERABILITY_V2.md`).

### Partner Referrals
Consultants, agencies, ERP/CRM implementers, cybersecurity advisors, ecosystem operators (see `docs/partners/PARTNER_REVENUE_MACHINE_V2.md`).

### Inbound Content
Founder posts, sector insights, proof-based content, checklists, and case studies.

### Strategic Accounts
Custom ABM briefs for high-value accounts (see `docs/distribution/ABM_STRATEGIC_ACCOUNT_MACHINE_V2.md`).

### Client Expansion
Delivery → feedback → retainer → referral → proof.

## Portfolio Rule
Each channel must produce one of:
- qualified conversation
- sample request
- proposal
- payment
- proof
- referral
- learning

## Weekly Decisions
Double Down / Maintain / Fix / Kill / Defer

## Scorecards
- `distribution/channel_scorecard.csv` (private ops): channel, leads, approved_outreach, sent, replies, positive_replies, samples, proposals, cash, trust_issues, decision, next_action.
- `distribution/sector_scorecard.csv` (private ops): sector, total_leads, a_leads, b_leads, approved, sent, replies, positive_replies, samples, proposals, cash, decision, next_action.

Both live under `/opt/dealix-ops-private/` and are seeded by `scripts/init_private_ops.sh`.
