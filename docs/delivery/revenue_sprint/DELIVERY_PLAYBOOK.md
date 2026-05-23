# Delivery Playbook — دليل التسليم اليومي

## Purpose
Day-by-day operating instructions for the 7-day Revenue Sprint. The playbook is what an operator opens every morning during a sprint. It is concrete, time-boxed, and tied to the gate model in `DELIVERY_CONTROL_SYSTEM.md`.

## Owner
Head of Delivery.

## Inputs
- Signed SOW.
- Completed `CLIENT_INTAKE.md`.
- Sector reference notes.

## Outputs
- Daily progress note in the sprint folder.
- All gate artifacts.
- Final outreach pack and report.

## Rules (numbered)
1. The playbook is followed in order; days may be compressed but not reordered.
2. Each day ends with a written progress note logged to `docs/audit/sprints/SPRINT_<ID>/day_<N>.md`.
3. Any day overrunning by more than 4 hours triggers an escalation to the founder.
4. No client communication outside the agreed touchpoints unless explicitly requested.
5. No sending on behalf of the client without A3 approval.
6. Every Day-7 handoff includes evidence paths.

## Metrics
- On-time day completion rate.
- Defects caught per day.
- Hours spent per day vs budget.

## Cadence
Per sprint; reviewed in monthly factory retro.

## Evidence (paths)
- `docs/audit/sprints/SPRINT_<ID>/day_1.md` through `day_7.md`
- `docs/audit/sprints/SPRINT_<ID>/handoff.md`

## Verifier
Head of Delivery initials each daily note.

## Runtime Command
`make sprint.day.note SPRINT=<ID> DAY=<N>` — creates the day note from template.

## Operating substance

**Day 1 — Intake & Frame.** Re-read the SOW. Reconcile with `CLIENT_INTAKE.md`. Open the sprint folder under `docs/audit/sprints/SPRINT_<ID>/`. Build the working ICP statement, the geo set, the deal-size band, the in-scope channels, and the exclusion list. Close G1 by end of day.

**Day 2 — Research Spine.** Build the source list: associations, public registers, sector reports, public tenders, news indexes. Capture ≥ 120% of the contracted lead count as raw rows. Every row carries source URL + capture timestamp. No social scraping. No bought lists.

**Day 3 — Enrichment & Scoring.** Apply `SCORING_RULES.md`. Compute fit, signal strength, and reachability per row. Cut the bottom decile. Mark any row with weak reachability for exclusion or re-check. Move to lead table per `LEAD_TABLE_SCHEMA.md`.

**Day 4 — Outreach Pack Build.** Draft the message variants per `OUTREACH_PACK_TEMPLATE.md`. Two variants per channel, AR + EN. Sector context note. Sequence map. Save the pack to the sprint folder. Close G3 when schema validates.

**Day 5 — Self-Review & Sector Notes.** Read the entire pack as if you were the client. Fix tone, claims, evidence gaps. Apply the no-overclaim filter (`docs/trust/NO_OVERCLAIM_POLICY.md`). Write the sector notes section of the delivery report.

**Day 6 — Independent QA.** A second operator runs `QA_CHECKLIST.md`. The QA operator owns the gate. Defects route back to the builder; the builder fixes; QA re-runs. Close G4 only on a clean pass.

**Day 7 — Handoff.** 30-minute handoff call. Walk the client through the report, the lead table, the message variants, and the evidence paths. Send the handoff doc (`HANDOFF_TEMPLATE.md`). Request written acknowledgement. Log the sprint into `docs/learning/COMPANY_MEMORY.md` and queue lessons for the weekly review.

Hard rules. We do not promise replies, meetings, or revenue. We deliver an evidence pack and a sequence map. The client owns sending and the client owns outcomes. We measure ourselves on pack quality, evidence coverage, and on-time handoff.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
