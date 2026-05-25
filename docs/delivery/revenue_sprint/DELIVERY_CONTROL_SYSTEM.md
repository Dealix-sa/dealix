# Delivery Control System — نظام التحكم في التسليم

## Purpose
Define the stage gates between intake and handoff. A sprint cannot advance to the next stage unless the previous gate is closed with evidence. The Control System is how we make delivery quality independent of the operator.

## Owner
Head of Delivery. Founder is the escalation owner for any blocked gate older than 24 hours.

## Inputs
- Signed SOW.
- Completed `CLIENT_INTAKE.md`.
- Current `SCORING_RULES.md`, `LEAD_TABLE_SCHEMA.md`, `OUTREACH_PACK_TEMPLATE.md`.

## Outputs
- Gate log file per sprint (`docs/audit/sprints/SPRINT_<ID>/gate_log.md`).
- Pass/fail timestamp per gate.
- Defect notes for any failed gate.

## Rules (numbered)
1. Five gates: G1 Intake Closed, G2 Research Closed, G3 Pack Built, G4 QA Cleared, G5 Handoff Acknowledged.
2. No gate is closed verbally; each requires a written log line with timestamp + verifier initials.
3. G3 cannot close without the lead table validating against `LEAD_TABLE_SCHEMA.md`.
4. G4 cannot close without an independent reviewer signing the QA log.
5. G5 cannot close without client acknowledgement in writing.
6. Any defect at G4 sends the pack back to G3, not forward.
7. Skipping gates is a Sev-2 incident under `docs/trust/INCIDENT_RESPONSE.md`.
8. A3 actions require named human approval logged in the gate file.

## Metrics
- Median time per gate.
- Gate failure rate (failed/total).
- Mean time to recover after a gate failure.
- Percentage of sprints closing all 5 gates within 7 days.

## Cadence
Per sprint. Aggregate gate metrics reviewed weekly in `docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md`.

## Evidence (paths)
- `docs/audit/sprints/SPRINT_<ID>/gate_log.md`
- `docs/audit/sprints/SPRINT_<ID>/qa_log.md`
- `docs/audit/sprints/SPRINT_<ID>/handoff_ack.md`

## Verifier
Head of Delivery for G1–G4. Founder for G5 on first three sprints of any new sector.

## Runtime Command
`make sprint.gates.status SPRINT=<ID>` — prints the gate table with status, timestamp, verifier.

## Operating substance
The Control System reframes delivery as five binary states. At any moment a sprint sits in exactly one of: G1 open, G2 open, G3 open, G4 open, or G5 open. There are no half-passed gates. This binary discipline removes the most common delivery failure: silent slippage.

G1 Intake Closed means the intake form is filled in full, sectors and exclusions are unambiguous, and the founder has countersigned. If any cell is empty, G1 stays open. We do not start research while G1 is open.

G2 Research Closed means the raw research set meets coverage and source-quality thresholds. Coverage is defined as ≥ 120% of the contracted lead count (we research more than we will deliver so we can drop weak rows). Source quality means every row has a verifiable public URL.

G3 Pack Built means the deliverable matches `OUTREACH_PACK_TEMPLATE.md` and the lead table validates against the schema with zero errors. Soft warnings (e.g., missing optional fields) are listed in the gate log but do not block.

G4 QA Cleared means an independent operator ran the full `QA_CHECKLIST.md` and signed off. The QA operator is not the builder. If QA fails, the sprint returns to G3 with a defect list. We do not patch in place during G4.

G5 Handoff Acknowledged means the client received the pack, attended (or declined in writing) the handoff call, and replied with acknowledgement. Only at G5 is the sprint considered closed and revenue recognized.

The Control System feeds the learning loop. Gate failure patterns surface in the weekly review and become checklist updates within one cycle.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
