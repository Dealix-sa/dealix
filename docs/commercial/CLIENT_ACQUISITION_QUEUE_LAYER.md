# Client Acquisition Queue Layer

## Purpose

This layer turns Dealix commercial signals into a daily review queue that helps the founder know which company to prioritize, what pain to address, what offer fits, what proof to show, and what next step should be reviewed.

It is intentionally safe and internal-first. The first version writes files only and does not perform external actions.

## What it creates

- Client cards with segment, signal, likely pain, offer fit, and scores.
- Ranked queue items with local angle, next action, suggested copy, likely objection, and proof to show.
- JSON output under `reports/client_acquisition/`.
- A verifier that confirms the queue stays draft-only and review-gated.

## Commercial use

The queue supports the active Money Now path:

- #864 Money Now Sprint
- #865 Payment path
- #866 Client acquisition queue layer

The operating sequence is:

1. Capture or import a warm/manual signal.
2. Build a client card.
3. Score the opportunity.
4. Generate the review queue.
5. Review the next action.
6. Log real evidence after confirmed actions.
7. Connect proof output to the relevant offer.

## Guardrails

- Founder review remains required.
- Price, delivery, and scope commitments require review.
- Revenue status requires confirmed payment.
- Proof is required before public or client-facing claims.
- This layer is not a mass outreach tool.

## How to run

```bash
python scripts/commercial/run_client_acquisition_queue.py --mode draft-only --limit 10
python scripts/commercial/verify_client_acquisition_queue.py
```

## Next iteration

After this foundation is merged, the next small PR should add source adapters for safe signals:

- Gmail warm reply summaries.
- HubSpot or Sheet rows.
- Calendar meeting notes.
- GitHub issue links for revenue blockers.

All source adapters should feed the same `ClientCard` shape so the queue stays simple and auditable.
