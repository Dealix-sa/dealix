# CSV to Postgres Migration Plan

## Purpose
Move Dealix from private CSV ops to production database without losing execution speed.

## Phase 1 — CSV Control
Use private ops CSV for:
- quick execution
- founder review
- early lead batches
- weekly learning

## Phase 2 — Shadow Database
Mirror CSV into Postgres:
- accounts
- outreach queue
- conversation log
- proposals
- payments
- approvals

## Phase 3 — Database Primary
Postgres becomes source of truth.
CSV exports become reports.

## Phase 4 — Command Center UI
CEO uses UI for:
- approvals
- sales cockpit
- distribution dashboard
- finance center
- trust center

## Rule
Do not migrate for elegance.
Migrate only when daily operation needs it.
