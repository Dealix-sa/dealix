# Control Plane

## Purpose
Define the single operating state Dealix reads from to understand the company, generate the CEO brief, and detect risks early.

## Owner
Sami / Control Plane owner.

## Review Cadence
Monthly, plus whenever new systems are added.

## Inputs
- Pipeline data.
- Revenue data.
- Delivery status.
- Trust logs.
- Product status.
- Learning reviews.

## Outputs
- Company State Schema.
- CEO brief.
- Decision queue.
- Risk flags.
- System scorecard.

## Rules
- The control plane reads from sources of truth; it does not invent numbers.
- Unknown values are marked `unknown` rather than guessed.
- Sensitive client and financial data stays in the private ops repo; the control plane stores schema and rules only.
- Any new operating system must be representable in the Company State Schema before it ships.

## Metrics
- Completeness of state (fields populated vs. total).
- Number of `unknown` values trending down.
- Decisions supported per week from the CEO brief.
- Risks detected before they become incidents.

## Evidence
- `COMPANY_STATE_SCHEMA.md` in this folder.
- private state snapshots.
- daily briefs derived from this state.
- weekly reviews.

## Last Reviewed
YYYY-MM-DD
