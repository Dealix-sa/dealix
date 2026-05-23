# Reply Routing System (Revenue Side)

This document defines the human-facing reply routing playbook in the
Revenue Factory. It is the counterpart to `growth/REPLY_ROUTER_MACHINE.md`
(the agent-side classifier). Where the machine produces a routing
decision, this system tells the operator what to do with it.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Make sure every classified reply gets a fast, accurate, brand-aligned
next step from a named operator, with the right artefact at the right
time.

## 2. Routing classes and next steps

| Reply class | Next step | Default SLA | Owner |
|---|---|---|---|
| interested | Qualification call invite (draft from EM machine) | 4 working hours | Distribution Operator + Founder |
| objection | Objection response (draft, with library reference) | 1 working day | Distribution Operator |
| opt_out | Add to suppression; brief polite acknowledgement | 1 working hour | Trust Guardian |
| unsure | Move to nurture queue; tag for later | 1 working day | Content Strategist |
| non_buyer | Polite thank-you; suppression only on request | 1 working day | Distribution Operator |
| spam | Discard; raise pattern flag if recurring | n/a | Trust Guardian |
| escalate (sensitive) | Founder review immediately | 30 minutes | Founder |
| other | Operator review; classify manually | 1 working day | Distribution Operator |

## 3. Decision flow

```
Reply arrives (operator-imported)
        |
        v
Reply Router Machine (A1) classifies
        |
        v
Routing decision written to outreach/reply_routing.csv
        |
        v
This system (the Revenue Factory side) reads the decision
        |
        v
Triggers the relevant downstream draft (qualification, objection,
suppression, nurture) at A2
        |
        v
Founder approval before any external action
        |
        v
Named operator sends the reply manually
        |
        v
State written to sales/pipeline.csv (if applicable) and audit ledger
```

## 4. Source of truth

- `outreach/reply_routing.csv` — classification.
- `sales/pipeline.csv` — pipeline-side state changes.
- `outreach/suppression.csv` — opt-outs.
- `trust/incidents.csv` — escalations.

## 5. Approval class

A2 for any draft produced as a next step. A1 for classification only.
Sensitive escalations always go to the founder (manual review).

## 6. Trust gate

- Opt-out detection is treated as a hard rule — any opt-out adds the
  identity to suppression immediately.
- Sensitive content (legal threats, distress signals, accusations)
  must be human-reviewed within the escalation SLA (30 minutes).
- No automated reply.
- No proposal or pricing commit in a reply without founder approval.
- Reply drafts are checked for brand voice, guarantee scan, and
  suppression before queueing.

## 7. Owner

Operator: `distribution_operator`. Approver: founder. Auditor: trust
guardian. Escalation handler: founder (for sensitive class).

## 8. Worker

Reading is automated; routing is automated; drafting the next-step
message is automated through the OUTBOUND/EMAIL/LINKEDIN draft
machines. Sending is manual, by a named operator, after approval.

## 9. KPI

- Routing SLA (per class).
- Misroute Rate (sampled, e.g. 50 replies per week).
- Opt-out Honour Rate (target 100%).
- Sensitive-Escalation Latency (target under 30 minutes).
- Reply-to-Qualified-Call Conversion.

## 10. Failure modes

| Failure | Recovery |
|---|---|
| Misroute (interest classified as non-buyer) | Operator-spot-check; calibration |
| Opt-out missed | Hard-rule overlay; ledger entry; root cause |
| Sensitive escalation delayed | Paging path reviewed; SLA re-set |
| Multiple replies to same opportunity not linked | Reply router state re-synced |

## 11. Cadence

| Cadence | Activity |
|---|---|
| Continuous | Reply ingestion and routing |
| Daily | Routing review; SLA check |
| Weekly | Misroute sample (50 replies) |
| Monthly | Reply-class definitions reviewed |

## 12. Saudi specifics

- "We will revisit next quarter" is its own class (unsure / non_buyer
  context); operators treat it as nurture, not opt-out.
- Bilingual replies handled with care; the next step matches the
  buyer's language.
- Polite deferral can hide real interest; operators check for trigger
  recency before assuming a no.

## 13. Non-negotiables

- No autoreply.
- No commit on pricing, terms, or contract changes in a reply without
  founder approval.
- No external action without an approved A2 draft.
- A3 not used.

The router is the seam where the system either respects the buyer or
fails them. Restraint is the differentiator.

## 14. Worker contract

- The classifier worker writes only to `outreach/reply_routing.csv`
  and (on opt-out) `outreach/suppression.csv`.
- The downstream draft worker writes to the relevant outreach queue.
- No worker sends replies; no worker reads mailboxes directly.
- All workers honour the kill switch.

## 15. Audit trail

Each reply has a ledger entry with `reply_id`, classification,
routing decision, the next-step draft id, and the operator who
ultimately sends the reply. Opt-out and escalation events are
double-logged.

## 16. Cross-references

- `docs/growth/REPLY_ROUTER_MACHINE.md` for the classifier machine.
- `docs/revenue/OBJECTION_LIBRARY_SYSTEM.md` for objection responses.
- `docs/proof/PROOF_APPROVAL_OS.md` for proof handling in
  proof-attached replies.
