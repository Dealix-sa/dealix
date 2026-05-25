# Suppression and Opt-Out System

## Relationship to existing docs
Operationalizes:
- `dealix/trust/policy.py` — the policy evaluation engine that gates external actions.
- `docs/trust/HUMAN_OVERSIGHT_MODEL.md` — the human-in-the-loop model.
- `docs/00_constitution/NON_NEGOTIABLES.md` — the trust boundaries that forbid contacting opt-outs or ignoring complaints.

The suppression list defined in `docs/data/GROWTH_DATABASE_MODEL_V2.md` is the source of truth for the checks below.

## Purpose
Respect opt-outs, rejections, bad-fit leads, and legal/trust boundaries.

## Suppress When
- opt-out
- not interested
- complaint
- bad fit
- duplicate
- risky source
- personal data uncertainty

## Rule
No outreach to suppressed records.

## Required Check
Every sending queue must be checked against `suppression_list.csv` (per the growth database model) before any outreach reaches the send queue. The check is a hard gate — the approval center surface (`docs/founder/approval_center.md`) must show the result for every queued message.
