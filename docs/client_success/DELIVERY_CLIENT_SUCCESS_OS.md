# Delivery & Client Success OS

## Purpose
A repeatable engagement so the first paying customer doesn't get lost, and so we can prove we can do this twice.

## Phases
1. **Intake** — confirm scope, success criteria, contacts.
2. **Kickoff** — agreed working channel, weekly check-in cadence.
3. **Build** — produce deliverables on the agreed schedule.
4. **QA** — internal QA score ≥ 75 before handoff.
5. **Handoff** — deliver in writing, log the artifact.
6. **Feedback** — request and log within 7 days.
7. **Health check + retention** — score, decide on retainer ask.

## Per-client folder template
Located at `dealix-ops-private/clients/_template/`. Copy to `clients/<client_slug>/` for each engagement.

Files:
- `client_os.md`
- `intake.md`
- `proposal.md`
- `lead_table.csv`
- `delivery_report.md`
- `qa_checklist.md`
- `handoff.md`
- `feedback.md`
- `health_score.md`
- `proof_approval.md`
- `renewal.md`

## Standards
- See `docs/delivery/KICKOFF_PROTOCOL.md`.
- See `docs/delivery/LEAD_TABLE_STANDARD.md`.
- See `docs/delivery/DELIVERY_QA_SCORE.md`.
- See `docs/delivery/HANDOFF_PROTOCOL.md`.
- See `docs/client_success/FEEDBACK_RETENTION_SYSTEM.md`.
- See `docs/client_success/CLIENT_HEALTH_SCORE_V2.md`.
- See `docs/content/PROOF_APPROVAL_SYSTEM.md`.

## Bootstrap a new client folder
```
cp -r ../dealix-ops-private/clients/_template ../dealix-ops-private/clients/<client_slug>
```
Or run `make delivery CLIENT=<client_slug>`.

## Operating cadence
- During delivery: weekly check-in with the client.
- After delivery: 7-day feedback ask, 30-day retainer ask.

## QA gate
No deliverable leaves the building without QA score ≥ 75 and the QA checklist filled in.

## Proof flow
Any proof candidate must pass `docs/content/PROOF_APPROVAL_SYSTEM.md` before reuse.
