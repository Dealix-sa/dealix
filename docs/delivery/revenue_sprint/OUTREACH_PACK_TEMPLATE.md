# Outreach Pack Template — قالب حزمة التواصل

## Purpose
Define the exact shape of the deliverable pack Dealix ships at handoff. The pack is the artifact the client uses to run their own outreach. It is not a campaign Dealix runs.

## Owner
Head of Delivery.

## Inputs
- Validated `lead_table.csv`.
- Sector notes and intake.
- Approved language from `docs/trust/SAFE_LANGUAGE_LIBRARY.md`.

## Outputs
- `pack/lead_table.csv`
- `pack/excluded.csv`
- `pack/sector_notes.md`
- `pack/messages/AR/` and `pack/messages/EN/` with two variants per channel.
- `pack/sequence_map.md`
- `pack/sources/` evidence index.
- `pack/README.md` orientation file.

## Rules (numbered)
1. Two message variants per channel, AR + EN parallel.
2. No banned phrases (`docs/trust/NO_OVERCLAIM_POLICY.md`).
3. No personalization that implies private knowledge of the recipient; only public signals.
4. Every claim in a message references a source path under `pack/sources/`.
5. Dealix does not send. Sending is the client's account and choice.
6. Pack ships as a single ZIP with a SHA256 manifest.
7. Schema and language checks run at QA; failures block ship.

## Metrics
- Pack schema validation pass rate: 100%.
- Banned-phrase scan hits: 0.
- Source-coverage per message claim: 100%.

## Cadence
Per sprint at G3 and again at G4.

## Evidence (paths)
- `docs/audit/sprints/SPRINT_<ID>/pack/`
- `docs/audit/sprints/SPRINT_<ID>/pack_manifest.sha256`

## Verifier
QA operator at G4. Head of Delivery final signoff.

## Runtime Command
`make sprint.pack.build SPRINT=<ID>` — assembles the pack and writes the manifest.

## Pack structure

```
pack/
  README.md
  lead_table.csv
  excluded.csv
  sector_notes.md
  sequence_map.md
  messages/
    AR/
      channel_email_v1.md
      channel_email_v2.md
      channel_form_v1.md
      channel_form_v2.md
    EN/
      channel_email_v1.md
      channel_email_v2.md
      channel_form_v1.md
      channel_form_v2.md
  sources/
    index.md
    <one file per cited source>
  pack_manifest.sha256
```

## Message variant rules

Each message is between 80 and 160 words. Each message has:
- A subject line (or first line for form channels) that names the public signal.
- Two evidence anchors with source paths.
- One concrete next step (a meeting request, a question, or a doc share).
- No claims about future outcomes.
- No urgency manipulation ("limited time").
- No fabricated personalization.

## Sequence map

The sequence map is a written description of when each variant is intended to be used, e.g., variant 1 first, variant 2 on a 5-business-day follow-up if no reply. The map is a recommendation, not an automation. The client decides what to send and when.

## Operating substance
The pack is built backwards from the client's audit moment. Six months after handoff, the client (or their auditor) must be able to open the ZIP and trace every claim to a public source captured at a known time. That is the standard.

Variants exist to give the client room to A/B without re-briefing Dealix. AR and EN run in parallel because Saudi buyers respond differently to each, and because some recipients prefer one language regardless of corporate norms.

The sources/ folder is not optional. It is the difference between a sales pack and an evidence pack. Each cited source has its own file containing the URL, the capture timestamp, and a short note on relevance. If a URL goes dark later, the note remains.

Dealix does not send. If the client requests assistance with sending, the request is routed to A3 approval (`docs/trust/APPROVAL_MATRIX.md`) and the sending workflow is documented separately. The default pack is built-to-hand-over.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
