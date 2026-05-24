# Nurture Machine

| Field | Value |
|---|---|
| Purpose | Warm long-cycle accounts via insights, proof, and selected content |
| Inputs | not-yet-ready accounts, content calendar, approved proof |
| Outputs | `nurture_queue.csv` |
| Approval class | Per-touch approval; cadence enforced |
| Trust gate | Brand check, suppression, frequency cap |
| Owner | Distribution Operator |
| KPI | Re-engagement rate, eventual conversion lag |
| Failure mode | Account opt-out → cadence stops, suppression updated |

## Cadence

- 1 touch every 30 days minimum.
- Mix of: insight, proof, sector report, founder note.
- Always cite source.
- Never repeat content within a 6-month window.

## Brand notes

- Tone is calm, useful, no-ask.
- Asks return only after two prior value touches.
- Bilingual.

## Surface

Nurture state is visible in Sales Cockpit per account, and aggregated in `/distribution`.
