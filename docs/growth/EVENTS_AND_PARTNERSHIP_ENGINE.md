# Events and Partnership Engine

The Events and Partnership Engine plans and tracks Dealix presence in
events, roundtables, and partnership activations. It is run as a small,
high-care channel — never a volume play.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Plan and produce drafts for invitations, follow-ups, and partnership
activations linked to events Dealix attends, hosts, or sponsors.

## 2. Input

Sources:

- `marketing/event_registry.csv` — events Dealix participates in.
- `marketing/event_attendees.csv` — attendees with opt-in posture.
- `customer_success/partner_registry.csv` — active partner agreements.
- `customer_success/event_partners.csv` — partners co-hosting or
  co-presenting.
- `growth/personas.csv`, `growth/icp_segments.csv`.
- `outreach/suppression.csv`.

An event activity is sanctioned only when the attendee or partner has
opted into being contacted for that purpose.

## 3. Output

`marketing/events_queue.csv` columns:

- `entry_id`
- `event_id`
- `activity_type` — invite | reminder | followup | thank_you |
  partner_brief
- `audience_type` — attendee | partner | speaker
- `account_id` (where applicable)
- `partner_id` (where applicable)
- `persona_id`
- `language`
- `subject`
- `body`
- `referenced_proof_id` (optional)
- `brand_voice_pass`
- `suppression_check`
- `guarantee_scan`
- `approval_state`
- `drafted_by`
- `drafted_at`

## 4. Source of truth

`marketing/events_queue.csv` in the private ops runtime.

## 5. Approval class

A2. Drafts autonomous; external send approval-gated.

## 6. Trust gate

- Opt-in evidence: the attendee or partner has opted into this activity
  type.
- Suppression check.
- Guarantee scan.
- Brand voice check.
- Partner agreement integrity (where partner_id is set).
- Proof integrity (where referenced).

## 7. Owner

`partner_revenue_agent`. Allowed write target: `customer_success/`.
Coordinates with `content_strategist` for promotional content and
`distribution_operator` for attendee follow-ups.

## 8. Worker

`scripts/dealix_events_engine.py` (planned). Idempotent on
`(event_id, account_id or partner_id, activity_type)`.

## 9. KPI

- Event-to-Qualified-Call Rate.
- Partnership Activation Conversion (co-events that generate joint
  pipeline).
- Brand voice first-pass rate.
- Opt-in hygiene (every activity backed by recorded opt-in).
- Attendee complaints (target: 0).

## 10. Failure mode

- Activity without opt-in. Worker rejects.
- Partner agreement lapsed. Worker rejects activity for that partner.
- Spam-like reminder cadence. Brand Guardian rewrites; cadence reset.
- Proof confidentiality breach in event collateral. Critical incident.

## 11. Recovery path

- For opt-in gap: opt-in re-acquired (manually, by named operator) or
  activity dropped.
- For partner lapse: partner renewal sprint.
- For cadence drift: paused; rewrite; resume.
- For confidentiality breach: incident opened.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Per event | Pre/during/post draft batches |
| Monthly | Event pipeline planning |
| Quarterly | Event ROI review |

## 13. Saudi-specific overlays

- In-person events are particularly high-value in Saudi B2B; the
  engine prioritises a small number of well-prepared events over a
  large number of attended ones.
- Bilingual operating reality is mandatory across event collateral.
- Many partner co-events are by-invitation; the engine respects
  invitation-only protocols.

## 14. Non-negotiables

- No external send without per-attendee or per-partner opt-in.
- No guaranteed claims in event collateral.
- No partner activity without an active agreement.
- A3 not used.

Events generate fewer drafts than any other channel, and that is the
correct answer. The point is presence done right, not presence done
often.

## 15. Worker contract

- Reads inputs idempotently.
- Writes only to `marketing/events_queue.csv`.
- Cannot send messages.
- Cannot generate activity without opt-in evidence.
- Logs every draft to the trust ledger.
- Honours the kill switch.

## 16. Audit trail

Every event activity generates a ledger entry with `entry_id`,
`event_id`, `activity_type`, `audience_type`, opt-in reference,
brand_voice_pass, and guarantee_scan.

## 17. Cross-references

- `docs/growth/PARTNER_REFERRAL_MACHINE.md` for partner-introduced
  attendees.
- `docs/growth/CONTENT_TO_DEMAND_ENGINE.md` for event content.
- `docs/finance/PAYMENT_CAPTURE_OS.md` for any event-related cost or
  partnership economics.
