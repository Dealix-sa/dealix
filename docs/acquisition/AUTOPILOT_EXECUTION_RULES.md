# Autopilot Execution Rules

## Scope
These rules govern any automated step inside the Dealix acquisition and
outreach autopilot. They apply to scripts, scheduled jobs, and any
Claude-driven flow that touches leads, outreach, samples, proposals,
or follow-ups.

## Approval Levels
- **A1 — Local artifact**
  - allowed automatically: research notes, batch CSVs, draft messages,
    Gmail draft queue rows, internal reports
- **A2 — External send**
  - requires Sami approval per batch: outbound emails, WhatsApp messages,
    LinkedIn DMs, proposal delivery, sample delivery
- **A3 — Commitment**
  - requires Sami written sign-off: pricing, refunds, contract changes,
    public proof, results claims

## Banned Automatic Actions
1. Sending external messages without explicit A2 approval.
2. Scraping platforms against their terms of service.
3. Storing sensitive personal data beyond what the public source exposes.
4. Making guarantees, projections, or revenue claims.
5. Pushing proposals before Sami signs them off.
6. Auto-charging or auto-invoicing.
7. Mass outbound that resembles spam under CST anti-nuisance rules.
8. Processing personal data in ways that conflict with PDPL controller duties.

## Required Logs
Every autopilot run that touches an external-facing artifact must log:
- date
- artifact path
- action taken
- approval status
- next action

## Idempotency
Scripts must be safe to run multiple times per day. Re-runs append, never
duplicate. CSVs use headers on first write only.

## Failure Behaviour
Scripts must exit non-zero on missing inputs and print a single-line PASS
on success. CI uses `scripts/verify_acquisition_autopilot.py` to confirm
the system is intact before merging.

## Founder Override
Sami can stop or pause any autopilot stream at any time by editing the
relevant queue file's `status` column to `Hold` or by removing the
`Approved` marker.

## Data Handling
- Only public, lawful sources.
- No personal data beyond business contact role/email/phone published by
  the company itself.
- Right-to-delete honoured on request: remove the row and log the removal
  in `acquisition/research_notes/`.

## Reporting
Daily report at `founder/daily_acquisition_report.md` is the single source
of truth for what the autopilot did and what Sami must do next.
