# Delivery Workspace System

## Purpose
Make delivery visible to the customer, structured for the founder, and auditable.

## Components
- `client_workspaces.json` — registry of all live engagements.
- `client_portal.demo.json` — demo seed.
- `/client-portal/[id]` — customer-facing surface.
- Scripts in `scripts/`:
  - `create_client_workspace.py`
  - `add_deliverable.py`
  - `mark_deliverable_done.py`
  - `request_client_approval.py`
  - `record_client_approval.py`
  - `generate_client_status_report.py`

## Lifecycle
1. Deal won → workspace created (`create_client_workspace.py`).
2. Kickoff workshop → deliverables added (`add_deliverable.py`).
3. Each completed item → `mark_deliverable_done.py`.
4. Each item needing customer sign-off → `request_client_approval.py`.
5. Customer approval recorded → `record_client_approval.py`.
6. Weekly → `generate_client_status_report.py` produces bilingual review.

## Guarantees
- Every status change is timestamped.
- Every approval has a named reviewer.
- Customer-facing pages show only what the customer is meant to see.
- Internal risks log is founder-only.
