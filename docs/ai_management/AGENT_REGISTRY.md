---
title: AI Agent Registry
owner: Trust Lead
status: active
cadence: review-monthly
last_review: 2026-05-23
---

# AI Agent Registry

Every agent in production is listed here with: name, task, governance level, owner, and the AI Run Ledger tag.

## Registry

| Agent | Task | Governance | Owner | Tag |
|---|---|---|---|---|
| Sales OS qualifier | Score and filter incoming leads | A0 | Revenue Lead | `sales.qualify` |
| Sales OS proposal generator | Draft Revenue Sprint proposals | A1 | Revenue Lead | `sales.propose` |
| Delivery OS scope tracker | Track in-scope vs out-of-scope work | A0 | Delivery Lead | `delivery.scope` |
| Proof OS assembler | Build a Proof Pack from event sources | A0 | Trust Lead | `proof.assemble` |
| Trust OS claim filter | Flag banned phrases pre-send | A0 | Trust Lead | `trust.claim_filter` |
| Value OS recorder | Tag reported numbers by tier | A0 | Trust Lead | `value.record` |
| Friction Log writer | Capture friction signals | A0 | Delivery Lead | `friction.emit` |
| Renewal scheduler | Maintain renewal calendar | A1 | Revenue Lead | `renewals.schedule` |

## Registry rules

- Adding an agent requires Trust Lead sign-off and a passing EVAL.
- Removing an agent requires a logged reason and replacement plan.
- An agent that fails three consecutive EVALs is auto-paused (governance: `blocked`).

## Owner

Trust Lead.
