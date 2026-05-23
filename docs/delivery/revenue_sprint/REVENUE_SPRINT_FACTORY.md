# Revenue Sprint Factory — مصنع سبرنت الإيرادات

## Purpose
Define the repeatable production model that converts a paid 7-day Revenue Sprint into a shippable evidence pack. The Factory enforces input quality, stage gates, and a single delivery shape so every sprint is reproducible by a new operator in under one hour of reading.

## Owner
Head of Delivery. Backup: Founder.

## Inputs
- Signed SOW + paid invoice.
- Completed `CLIENT_INTAKE.md`.
- Sector reference set under `docs/sector-reports/`.
- Approved outreach pack template (`OUTREACH_PACK_TEMPLATE.md`).

## Outputs
- One outreach pack ZIP per sprint (lead table, message variants, sector notes, report).
- One delivery report (`REPORT_TEMPLATE.md`).
- One QA log under `docs/audit/sprints/SPRINT_<ID>/`.
- One handoff doc per client.

## Rules (numbered)
1. No sprint starts without signed SOW + completed intake.
2. Every lead row carries a source URL and capture timestamp.
3. No external messages are sent by Dealix on behalf of the client unless explicit written approval (see `docs/trust/AUTONOMY_POLICY.md`).
4. No phrase from `docs/trust/NO_OVERCLAIM_POLICY.md` may appear in any deliverable.
5. QA checklist is mandatory before handoff; failures block ship.
6. Every claim in the report must cite an evidence path.
7. A3 actions (anything irreversible, anything that touches the client's audience) require human approval logged in the sprint folder.
8. Sprint closes only after handoff acknowledgement is received.

## Metrics
- Sprint cycle time (intake-to-handoff): target ≤ 7 calendar days.
- QA pass rate on first review: target ≥ 80%.
- Evidence coverage: 100% of claims linked to a source path.
- Client acknowledgement within 48h of handoff: target ≥ 90%.

## Cadence
Sprint cadence is per-engagement. Factory review (this document) is reviewed monthly during the strategy update (`docs/learning/MONTHLY_STRATEGY_UPDATE.md`).

## Evidence (paths)
- `docs/audit/sprints/SPRINT_<ID>/intake.md`
- `docs/audit/sprints/SPRINT_<ID>/lead_table.csv`
- `docs/audit/sprints/SPRINT_<ID>/qa_log.md`
- `docs/audit/sprints/SPRINT_<ID>/handoff.md`

## Verifier
Head of Delivery signs each QA log. Founder spot-checks one sprint per month.

## Runtime Command
`make sprint.factory.audit SPRINT=<ID>` — runs schema + evidence coverage check and prints pass/fail.

## Operating substance
The Factory is built around five fixed stations: Intake, Research, Outreach Pack Build, QA, Handoff. Each station has one owner, one input artifact, one output artifact, and one verifier. Operators do not skip stations; they fail forward by writing a short defect note into the QA log and rerunning the affected station.

Inputs are normalized at intake. The intake form (`CLIENT_INTAKE.md`) is the single source of truth for ICP, geo, deal size band, channels in scope, and exclusions. If any of these are missing, the sprint is paused and the founder is alerted. We do not start work on assumptions.

Research is constrained to public, lawful sources. We do not scrape gated platforms, we do not bulk-pull from social networks, and we do not buy lists from unverifiable resellers. Every row in the lead table carries a source URL and capture timestamp so the client can audit any record.

The Outreach Pack is a deliverable, not a campaign. Dealix prepares the messages, the lead context, and the sequence map. Sending is the client's choice and the client's account. If the client requests Dealix to send on their behalf, the request is routed to A3 approval with documented consent.

QA is independent. The QA reviewer is never the same person who built the pack. The reviewer runs `QA_CHECKLIST.md` end-to-end and writes the result into the audit folder. Only a clean QA log unlocks Handoff.

Handoff is a one-meeting protocol with a written follow-up. The follow-up references the sprint's evidence paths so the client can audit independently. After handoff, the sprint is logged into `docs/learning/COMPANY_MEMORY.md` for the next factory review.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
