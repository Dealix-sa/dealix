# Reply Router Machine

The Reply Router Machine reads inbound replies and routes them to the
correct next step — qualified call, objection handling, opt-out, or
nurture. It does not auto-reply. It produces a router decision and a
suggested draft for the next step, both gated by the founder.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Make sure every inbound reply gets a fast, accurate next step. The
machine is the front door of the Revenue Factory's reply routing.

## 2. Input

Sources:

- Operator-imported reply messages (in `outreach/inbound_replies.csv`).
  No mailbox auto-fetching is performed by an agent; the operator
  imports replies into the runtime under controlled access.
- `outreach/outreach_queue.csv`, `outreach/email_queue.csv`,
  `outreach/linkedin_queue.csv` (for context lookup).
- `marketing/objection_library.csv`.
- `growth/personas.csv`.

The reply must be linked back to a known `account_id` and the original
draft (`previous_send_id`). Replies that cannot be linked are
quarantined for operator review.

## 3. Output

`outreach/reply_routing.csv` columns:

- `reply_id`
- `account_id`
- `persona_id`
- `previous_send_id`
- `classification` — interested | objection | opt_out | unsure |
  non_buyer | spam | other
- `routing_decision` — call_request | objection_response | suppress |
  nurture | escalate
- `suggested_draft_id` — references the appropriate downstream queue
- `confidence_score` — 0..1
- `language`
- `analysed_at`
- `analysed_by`
- `notes`

For `opt_out`, the account is added to `outreach/suppression.csv` and
no further drafts are produced for that identity.

## 4. Source of truth

`outreach/reply_routing.csv` in the private ops runtime.

## 5. Approval class

A1. The reply router observes and classifies; it does not send. Any
suggested next-step draft must be approved per A2 rules before any
external action.

## 6. Trust gate

- Classification confidence: replies with confidence_score < 0.7 are
  flagged for operator review.
- Opt-out detection is treated as a hard rule — any opt-out adds the
  identity to the suppression list immediately.
- Sensitive content detection: replies that include legal threats,
  distress signals, or accusations are escalated, not auto-classified.
- PII handling: no re-export of reply content outside the runtime.

## 7. Owner

`distribution_operator`. Allowed write target: `outreach/`. Coordinates
with `trust_guardian` for opt-out additions to suppression.

## 8. Worker

`scripts/dealix_reply_router.py` (planned). The worker:

1. Reads new reply rows.
2. Classifies each reply.
3. Updates `outreach/reply_routing.csv`.
4. Triggers a suggested-draft entry in the appropriate downstream queue
   (follow-up, objection response, call request, or nurture move).
5. On opt-out, writes to `outreach/suppression.csv` and ledgers the
   action.

## 9. KPI

- Classification Accuracy (sampled).
- Time-to-Route (minutes from reply import to classified).
- Opt-out Honoured (target: 100 percent, immediate).
- Escalation Latency (sensitive content escalated within 30 minutes).

## 10. Failure mode

- Misclassification of opt-out as interest. Operator-spot-check
  required; rule-based override forces opt-out keywords to win.
- Sensitive content auto-classified. Trust Guardian halts; manual
  review required.
- Reply unlinkable. Quarantined for operator.
- Confidence drift downward. Worker tuning session.

## 11. Recovery path

- For opt-out miss: hard-rule overlay added; ledger entry; root cause.
- For sensitive content: escalation playbook in
  `docs/revenue/REPLY_ROUTING_SYSTEM.md`.
- For confidence drift: paused; calibration with labelled examples.
- For unlinkable replies: operator-assisted match; rules tightened.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Continuous | Reply classification |
| Daily | Confidence audit |
| Weekly | Calibration sample (50 replies) |
| Monthly | Worker tuning |

## 13. Saudi-specific overlays

- Polite deferral ("we will revisit next quarter") is a routing class
  in itself — moved to nurture, not opt-out.
- Bilingual replies are common; the worker handles Arabic and English
  and respects the buyer's language at the next step.
- Cultural register: many replies are warm but non-committal; the
  classifier does not treat warmth as readiness.

## 14. Non-negotiables

- No auto-reply.
- Opt-outs honoured immediately.
- Sensitive content escalated, not auto-classified.
- A3 not used.
- No re-export of reply content.

The router's job is to give the operator a confident next step in
seconds, not to take the action itself.

## 15. Worker contract

- Reads inputs idempotently.
- Writes only to `outreach/reply_routing.csv` and (on opt-out)
  `outreach/suppression.csv`.
- Cannot send replies.
- Cannot summarise replies to external recipients.
- Logs every classification to the trust ledger.
- Honours the kill switch.

## 16. Audit trail

Every classification generates a ledger entry with `reply_id`,
`account_id`, `classification`, `routing_decision`, `confidence_score`,
and the analyst (agent or operator) that produced it. Opt-out events
are double-logged: one entry on the router, one entry on the
suppression list.

## 17. Cross-references

- `docs/revenue/REPLY_ROUTING_SYSTEM.md` for the human-facing
  playbook.
- `docs/revenue/OBJECTION_LIBRARY_SYSTEM.md` for objection responses.
- `policies/dealix_control_policy.yaml` for opt-out and suppression
  rules.
