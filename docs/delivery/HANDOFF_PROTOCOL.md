# Handoff Protocol

## Purpose
A clean delivery moment that the client can clearly recognize as "done".

## Steps
1. QA score recorded (≥ 75).
2. Final files placed in `clients/<slug>/` and zipped / shared with the client.
3. A handoff email is sent including:
   - One-paragraph summary of what was delivered.
   - List of files and where to find them.
   - The one most important insight.
   - Two suggested next steps.
4. `clients/<slug>/handoff.md` updated with date, channel, recipients.

## Acknowledgement
Ask the client to confirm receipt in writing within 48 hours.

## What NOT to do at handoff
- Don't surprise the client with extras outside scope.
- Don't ask for the renewal in the handoff email — that's a separate moment.
- Don't promise capabilities the operating system can't repeat.

## Evidence
Log a row in `evidence/execution_evidence_ledger.csv`:
- `system=delivery, evidence_type=handoff, evidence_path=clients/<slug>/handoff.md, status=Closed`.

## Follow-up timing
- Day 1: handoff sent.
- Day 3: light check-in ("any quick questions on what I sent?").
- Day 7: formal feedback request.
- Day 30: retainer / next-engagement conversation.
