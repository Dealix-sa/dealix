# Handoff Template — قالب التسليم النهائي

## Purpose
Define the client-facing handoff document and the handoff meeting structure. Handoff is when the engagement transfers from Dealix's hands into the client's. The document is what they keep.

## Owner
Head of Delivery. Client lead at the client side.

## Inputs
- Cleared QA log (G4).
- Final pack.
- Delivery narrative.

## Outputs
- `pack/HANDOFF.md` (AR + EN sections).
- 30-minute handoff meeting recording or notes.
- Written acknowledgement from the client.

## Rules (numbered)
1. No handoff without a cleared QA log.
2. Handoff is a meeting, not just a file send. Async-only is allowed when the client explicitly requests it.
3. Acknowledgement must be in writing (email reply or signed PDF).
4. The document includes the evidence index path so the client can self-audit.
5. The document lists what Dealix did NOT do, to prevent scope creep in conversation later.
6. Any post-handoff request follows `docs/delivery/CHANGE_REQUEST_PROCESS.md`.

## Metrics
- Handoff held within 7 calendar days of sprint start.
- Written acknowledgement within 48h: target ≥ 90%.
- Post-handoff defects raised by client within 30 days: target ≤ 1 per sprint.

## Cadence
Once per sprint at G5.

## Evidence (paths)
- `docs/audit/sprints/SPRINT_<ID>/pack/HANDOFF.md`
- `docs/audit/sprints/SPRINT_<ID>/handoff_ack.md`
- `docs/audit/sprints/SPRINT_<ID>/handoff_meeting_notes.md`

## Verifier
Head of Delivery. Founder for first sprint per client.

## Runtime Command
`make sprint.handoff.scaffold SPRINT=<ID>` — writes the handoff skeleton.

## Handoff document structure

**Section 1 — What was contracted.** One paragraph each in AR + EN restating the SOW scope.

**Section 2 — What was delivered.** Bullet list of artifacts with paths inside the pack: lead table, excluded list, sector notes, messages folders, sequence map, evidence index, manifest.

**Section 3 — What we did NOT do.** Explicit boundary statement. We did not send messages on the client's behalf. We did not capture personal contact data. We did not promise outcomes. We did not include sources outside the agreed channels.

**Section 4 — How to read the pack.** Three-step orientation: start with the narrative; open the lead table; consult sources/ for any specific row.

**Section 5 — Limitations.** Restate from the narrative.

**Section 6 — Change requests.** Path to the change-request process, and the cost / time bands for common requests (additional rows, new sector slice, re-scoring, message rewrites).

**Section 7 — Acknowledgement.** Signature block for the client.

## Meeting structure

The 30-minute handoff call follows a fixed agenda: 5 minutes scope recap; 10 minutes walking the lead table and source paths; 5 minutes on findings and recommendations; 5 minutes on limitations; 5 minutes on next steps and change-request paths. The meeting is not a sales call for follow-on work. Discussion of future engagements happens in a separate call scheduled after acknowledgement.

## Operating substance
Handoff is the moment the engagement either becomes a clean reference or a quiet complaint. The variance is almost entirely controlled by clarity. A client who knows exactly what they got, exactly what they did not get, and exactly how to use what they got is a client who will renew or refer.

The "what we did not do" section is uncomfortable for some operators because it reads as defensive. It is not defensive; it is honest. It prevents the conversation three weeks later where the client asks "why didn't you also..." and we lose goodwill explaining scope. The boundary is set in writing at handoff.

Written acknowledgement closes G5. Until acknowledgement is in writing, the sprint stays open and the operator keeps following up. Acknowledgement is not a courtesy; it is the audit anchor.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
