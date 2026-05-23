# Retention and Referral OS

The Retention and Referral OS owns the post-delivery loop. It tracks
client health, runs retention reviews, and converts happy clients into
named referrals — without ever assuming a referral or commitments on
their behalf.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Keep clients close to the work, surface health risks early, and
generate referrals through real, named, consented introductions — not
through opaque "incentive programs."

## 2. Input

Sources:

- `delivery/sprint_log.csv` (sprint state).
- `delivery/handoff_queue.csv` (handoffs and acceptances).
- `sales/pipeline.csv` (closed_won opportunities).
- `customer_success/client_health.csv` (health scores).
- `customer_success/check_in_template.md`.
- `customer_success/referral_terms.csv` (revenue share posture).
- `proof/proof_library.csv` (existing proof; may seed an upsell case).
- `outreach/suppression.csv`.

Every active engagement has a row in `customer_success/client_health.csv`.

## 3. Output

Queues:

- `customer_success/check_in_queue.csv` — scheduled check-ins.
- `customer_success/referral_queue.csv` — referral intros (also used
  by Partner Referral Machine).
- `customer_success/retention_actions.csv` — actions tagged to client
  health movement.
- `customer_success/upsell_queue.csv` — drafted upsell offers
  (approval-gated).

`customer_success/client_health.csv` columns:

- `engagement_id`
- `account_id`
- `health_score` — 0..100
- `health_band` — green | amber | red
- `last_review_at`
- `next_review_at`
- `risk_signals` — pipe-delimited
- `positive_signals` — pipe-delimited
- `notes`

Health score factors:
- Sprint completion track record.
- QA first-pass rate on this engagement.
- Client review frequency and tone.
- Payment posture (on-time vs. overdue).
- Open change requests not closed in SLA.
- Open incidents.

## 4. Source of truth

`customer_success/client_health.csv` for health. `referral_queue.csv`
for referrals. `upsell_queue.csv` for upsell drafts.

## 5. Approval class

A1 for health observation. A2 for any client-facing or partner-facing
draft (referral asks, upsell offers, check-in notes). A3 banned.

## 6. Trust gate

- Suppression check on referred accounts.
- Guarantee scan on every client-facing draft.
- Brand voice check.
- Consent: a referral is recorded only when the client has opted in to
  be named as a referrer.
- Confidentiality respect: upsell drafts do not reveal data from other
  clients.
- Proof integrity: any embedded proof must be approved.

## 7. Owner

`partner_revenue_agent` (referrals) + the founder for upsell offers.
Allowed write targets: `customer_success/`. Coordinates with
`delivery_copilot` on health signals, `proof_safety_agent` on proof
references, and `finance_copilot` on revenue share.

## 8. Worker

`scripts/dealix_retention_referral.py` (planned). The worker:

1. Computes health scores daily.
2. Schedules check-ins based on band and last review.
3. Surfaces referral candidates after positive milestones.
4. Drafts upsell offers when client health is green and trigger
   conditions are met.

## 9. KPI

- Net Retention Rate (revenue retained from cohort).
- Logo Retention Rate.
- Referral Conversion Rate.
- Upsell Win Rate.
- Health Band Drift (green -> amber -> red counts).
- Time-to-Recovery on amber/red.

## 10. Failure mode

- Health score lags reality. Worker tuning; manual override entry.
- Referral asked without consent. Worker blocks; ledger entry.
- Upsell drafted into a red-band engagement. Worker blocks; recovery
  first.
- Confidentiality breach in upsell. Critical incident.

## 11. Recovery path

- For score lag: factor weights tuned; manual overrides ledgered.
- For consent gap: consent re-acquired or referral dropped.
- For drafted-into-red: upsell paused; recovery actions tracked in
  `retention_actions.csv`.
- For confidentiality breach: incident opened.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Daily | Health update |
| Weekly | Check-in queue review |
| Monthly | Retention scorecard with founder |
| Quarterly | Cohort review; offer ladder feedback |

## 13. Saudi specifics

- Relationship density: regular, low-pressure check-ins outperform
  formal QBRs in many Saudi accounts; the worker offers both formats.
- Bilingual handling on every client-facing artefact.
- Referrals are often informal and warm; the worker records the
  introducer-account chain with care.
- PDPL alignment in client communications.

## 14. Non-negotiables

- No referral request without consent.
- No upsell into a red-band engagement.
- No guaranteed claims.
- No other-customer data in any client artefact.
- A3 not used.

The retention OS treats the post-sale relationship as the most
productive surface in the business. The system makes that easy to
maintain.
