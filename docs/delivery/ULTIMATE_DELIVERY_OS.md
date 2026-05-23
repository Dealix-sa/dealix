# Ultimate Delivery OS

Delivery starts the moment a proposal is won. Read by
`GET /api/v1/internal/delivery/queue`.

## Stages

- `won` — deal closed, awaiting kickoff.
- `kickoff` — scheduled kickoff.
- `delivery` — work in progress.
- `handover` — final deliverable handed over.
- `proof` — proof artefact ready for manual publish.

## Boundaries

- No proof publishes without founder approval (A2).
- No client artefact leaves the private ops tree without a recorded
  approval row referencing the proof id.
