# Partner Referral Machine

The Partner Referral Machine handles introductions and accounts that
come through named partners. It is the highest-quality source in the
Dealix system, so it gets the most careful handling.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Track partner-introduced accounts, draft the appropriate follow-up, and
coordinate revenue share state — without sending anything externally on
behalf of the partner without consent.

## 2. Input

Sources:

- `customer_success/partner_registry.csv` — active partners and
  agreements.
- `customer_success/partner_intros.csv` — raw intros from partners.
- `growth/personas.csv`, `growth/icp_segments.csv`.
- `outreach/suppression.csv`.
- `customer_success/referral_terms.csv` — per-partner revenue share
  terms.

A partner intro is eligible only when:

- The partner has an active agreement.
- The introducer is named.
- The introduced account is not suppressed.
- The intro carries an explicit message or context.

## 3. Output

`customer_success/referral_queue.csv` columns:

- `referral_id`
- `partner_id`
- `account_id`
- `persona_id`
- `intro_context`
- `language`
- `recommended_next_step` — qualified_call | sample_send | proposal
- `suggested_draft_id` — references an outreach draft for follow-up
- `revenue_share_pct`
- `expected_close_band`
- `approval_state` — drafted | queued | approved | rejected
- `created_at`

A companion draft is produced in the relevant outreach queue
(`outreach/email_queue.csv` typically) for founder approval.

## 4. Source of truth

`customer_success/referral_queue.csv` in the private ops runtime.

## 5. Approval class

A2. The agent records the intro and drafts the follow-up; all external
action is approval-gated.

## 6. Trust gate

- Partner agreement check: an inactive or missing agreement blocks the
  intro from being processed.
- Suppression check on the introduced account.
- Guarantee scan on the follow-up draft.
- Brand voice check.
- Revenue-share commitment check: revenue share is recorded and
  surfaced for finance reconciliation; no external promise without
  finance confirmation.

## 7. Owner

`partner_revenue_agent`. Allowed write target: `customer_success/`.

## 8. Worker

`scripts/dealix_partner_referral.py` (planned). Idempotent on
`(partner_id, account_id)`.

## 9. KPI

- Partner Intro Conversion Rate (intros to qualified call).
- Revenue Share Realised vs. Promised.
- Time-to-First-Follow-up.
- Partner Repeat Rate.

## 10. Failure mode

- Intro arrives without context. Worker rejects; partner asked for a
  one-line context.
- Account is suppressed. Intro held; partner notified by operator.
- Revenue share term changes without approval. Finance halts; ledger
  entry.
- Partner agreement expires. Pipeline frozen for that partner until
  renewed.

## 11. Recovery path

- For context gap: partner re-engaged for context; intro re-processed.
- For suppression conflict: operator informs the partner with care.
- For revenue share mismatch: finance and partner reconcile; agreement
  updated.
- For agreement lapse: partner renewal sprint.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Daily | New intros processed |
| Weekly | Pipeline review with partner |
| Monthly | Revenue share reconciliation |
| Quarterly | Partner agreement review |

## 13. Saudi-specific overlays

- Partner introductions in Saudi B2B carry significant social weight;
  the response time on a partner intro is the most-watched signal.
- Bilingual handling required for many partner contexts.
- Revenue share terms vary; the system tracks each per-partner setup.

## 14. Non-negotiables

- No follow-up without partner-attributed context.
- No external promise of revenue share without finance approval.
- No guaranteed claims.
- A3 not used.

The partner channel is small and slow but consistently the highest-value
channel in the system. Speed of internal handling matters more than
volume of intros.

## 15. Worker contract

- Reads inputs idempotently.
- Writes only to `customer_success/referral_queue.csv` and a draft
  entry in the relevant outreach queue.
- Cannot send messages.
- Cannot commit to revenue share without finance approval.
- Logs every intro to the trust ledger.
- Honours the kill switch.

## 16. Audit trail

Every intro and its downstream follow-up share a `referral_id`. The
ledger captures the partner, the introduced account, the revenue share
band, and any finance event that derives from the eventual close.

## 17. Cross-references

- `docs/growth/EVENTS_AND_PARTNERSHIP_ENGINE.md` for events-side
  partner activity.
- `docs/finance/PAYMENT_CAPTURE_OS.md` for revenue share
  reconciliation.
- `docs/client_success/RETENTION_REFERRAL_OS.md` for customer-derived
  referrals.
