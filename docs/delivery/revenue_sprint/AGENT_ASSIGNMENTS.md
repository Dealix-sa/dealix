---
title: Revenue Sprint Agent Assignments
owner: Delivery Lead
status: active
cadence: review-quarterly
last_review: 2026-05-23
---

# Revenue Sprint Agent Assignments

Each sprint draws on a small fixed set of internal agents. This document maps the agent to the task and to the governance level.

## Agents in the sprint loop

| Agent | Task | Governance |
|---|---|---|
| Sales OS qualifier | Filter incoming lead against the scoring rules | A0 |
| Sales OS proposal generator | Draft proposal from template | A1 (human sends) |
| Delivery OS scope tracker | Track in-scope vs out-of-scope work | A0 |
| Proof OS pack assembler | Assemble the Proof Pack snippet | A0 (review before sharing) |
| Trust OS claim filter | Flag banned phrases in any draft | A0 (mandatory) |
| Value OS recorder | Tag every reported number as estimated / observed / verified | A0 |

## Rules

- Every agent run produces an AI Run Ledger entry.
- No agent run is auto-sent externally; A1+ approvals required.
- A failing Trust OS claim filter blocks the artefact from being delivered.

## On-call humans

- Delivery Lead is the named human in the loop for every sprint.
- Trust Lead reviews any A2 escalation.
- Founder is the named A2 signer.

## Owner

Delivery Lead.
