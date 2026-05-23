# Reply Routing System

The Reply Routing System classifies inbound replies to Dealix outreach and routes each to the correct human owner. It does not send replies on the customer's behalf without explicit approval.

**Source of truth:** `$PRIVATE_OPS/reply_routing_log.csv`
**Owner:** Revenue Lead
**Trust gate:** A1 — drafted replies require human send. A3 auto-reply is prohibited.

## Reply classes

| Class | Definition | Default route | Median SLA |
|-------|------------|---------------|------------|
| Hot | Asks for pricing, proposal, meeting | Founder | 2 hours |
| Warm | Asks a substantive question | Revenue Lead | 1 business day |
| Cold | Acknowledges receipt only | Revenue Lead | 2 business days |
| Objection | Raises a concern requiring evidence | Founder | 2 hours |
| Unsubscribe | Asks to stop contact | Compliance | Immediate |
| Out-of-office | Auto-reply with return date | Calendar follow-up | 0 |
| Hostile | Aggressive or accusatory | Founder + Compliance | Immediate |

Classification is deterministic where possible. Where the classifier is uncertain, the message routes to the Revenue Lead for human triage.

## Pipeline

1. Inbound reply lands in the unified inbox.
2. Classifier reads the message and writes a candidate class to `reply_routing_log.csv`.
3. Brand Guardian checks the suggested response template for tone, claim safety, and PII (`docs/ai/BRAND_GUARDIAN_AGENT.md`).
4. The drafted reply is queued for human send. The human owner sees the original message, the suggested class, the suggested response, and a one-line rationale.
5. The human either sends, edits-then-sends, or rejects. The decision is logged.

No reply leaves the system without a human send action.

## Objection handling

When an inbound reply is classified as an objection, the system attaches a reference excerpt from `docs/revenue/OBJECTION_LIBRARY_SYSTEM.md`. The founder reviews the suggested response and decides whether to send, modify, or escalate.

## Unsubscribe handling

Unsubscribe requests are honoured immediately. The contact is moved to the suppression list in `$PRIVATE_OPS/suppression_list.csv` and removed from any active sequence. PDPL-aware language applies (`docs/02_saudi_positioning/PDPL_AWARE_LANGUAGE.md`).

## Failure modes

- **Mis-classification:** the system labels a Hot lead as Cold. Detection: weekly sampling audit by Revenue Lead. Recovery: re-label, retrain classifier, surface in `docs/evals/PROMPT_OUTPUT_EVAL_MATRIX.md`.
- **Auto-send leak:** a drafted reply sends without human action. Detection: policy engine blocks; missed sends surface in audit log. Recovery: send rolled back where possible, contact apology issued, root cause filed.
- **Suppression bypass:** a contact on suppression receives a message. Detection: nightly diff against suppression list. Recovery: immediate stop, written apology, root cause filed.

## Recovery path

If the classifier fails (model outage, eval failure), all inbound replies route to the Revenue Lead with no classification. Triage is fully manual until the issue clears. No degraded mode silently auto-classifies.

## Metrics

- Reply volume by class (this week vs prior week).
- Median time-to-human-send by class.
- Misclassification rate (sampled).
- Suppression honour rate (target: 100%).

## Disclaimer

Reply routing is a triage aid for human responders. Dealix does not send replies on a customer's behalf without explicit approval. Estimated value is not Verified value.
