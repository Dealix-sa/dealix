---
title: Revenue Sprint Evidence Pack
owner: Delivery Lead
status: active
cadence: review-per-sprint
last_review: 2026-05-23
---

# Revenue Sprint Evidence Pack

The evidence pack is the internal record that proves the sprint was actually delivered. It is never sent to the buyer; it lives in the private ops repo.

## What goes in the evidence pack

- AI Run Ledger IDs for every agent run touching this sprint.
- A copy of the kickoff note.
- A copy of the wrap-up brief.
- Sync agendas and one-paragraph notes from each sync.
- QA Checklist (signed).
- Handoff Checklist (signed).
- Refund posture (yes/no triggered).

## Where it lives

`dealix-ops-private/sprints/<sprint_id>/evidence/`

## Indexing

- A `manifest.csv` lists every file in the evidence pack with a SHA hash.
- The manifest is written by the evidence scanner; see `execution_engine.evidence_scanner`.

## Retention

- Evidence packs are kept for 24 months minimum.
- Any deletion requires Trust Lead sign-off and is logged.

## Owner

Delivery Lead.
