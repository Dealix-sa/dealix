# Retention and Referral OS

Retention is the only revenue line that compounds. The Retention and Referral OS is the system that keeps engaged clients engaged and turns satisfied clients into a credible source of new opportunities.

**Source of truth:** `$PRIVATE_OPS/retention_state.csv` plus `$PRIVATE_OPS/referral_pipeline.csv`
**Owner:** Customer Success Lead
**Trust gate:** A1 — published case stories, testimonials, and referral asks all require client written consent and founder approval (A2).

## Two parallel motions

| Motion | Goal | Signal |
|--------|------|--------|
| Retention | Renew the engagement | Health Score (see `docs/customer_success/CLIENT_HEALTH_SCORE_SYSTEM.md`) |
| Referral | Earn a warm introduction | Net promoter signal, explicit consent |

The two motions share a client view but never share a workflow: a renewal conversation is not a referral ask, and a referral ask is not a renewal conversation.

## Retention cadence

| Cadence | Activity | Owner |
|---------|----------|-------|
| Weekly | Health Score read | CS Lead |
| Bi-weekly | Working session with client | CS Lead |
| Monthly | Executive review with founder | Founder |
| Quarterly | Renewal posture review | Founder + CS Lead |
| 45 days before renewal | Renewal proposal drafted | Founder |

## Referral pathway

1. Identify client whose Health Score has been ≥ 8 for two consecutive months.
2. CS Lead drafts a referral ask, bilingual, with founder approval.
3. Client receives the ask in person or by founder DM, never by automated sequence.
4. If client agrees, client makes the introduction. Dealix never sends outreach on the client's behalf.
5. Referral is logged in `referral_pipeline.csv` with provenance.

## Consent and attribution

No client is named in any public material without written consent. Case studies follow `docs/07_proof_os/CASE_SAFE_SUMMARY.md`. Anonymised summaries can be published without naming, but never with metrics that would reverse-identify the client.

## Failure modes

- **Pressuring a referral ask:** a client says no and is asked again. Detection: client feedback or audit. Recovery: stop the ask, written apology, log entry.
- **Consent drift:** a story is published with stale consent. Detection: annual consent re-confirmation. Recovery: pull the story, re-obtain or remove.
- **Renewal blindspot:** a client renews quietly without strategic review. Detection: nightly job on `retention_state.csv`. Recovery: schedule the missed review.

## Recovery path

If the Retention and Referral data becomes unreliable, the founder freezes all referral asks and published stories until the data is re-certified. Renewal conversations continue manually.

## Metrics

- Gross retention rate (verified, rolling 12 months).
- Net dollar retention (verified, rolling 12 months).
- Health Score distribution.
- Referrals received vs referrals asked.
- Time from referral introduction to first qualified conversation.

## Disclaimer

Retention and referral motions are designed to be respectful and consent-based. Dealix does not guarantee renewals or referrals. Estimated value is not Verified value.
