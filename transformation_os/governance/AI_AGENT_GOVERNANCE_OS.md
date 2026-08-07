# AI Agent Governance OS

## Purpose
Make AI agents useful without letting them become uncontrolled operational risk.

## Governance model
- Every agent has an owner
- Every agent has a scope
- Every agent has allowed tools
- Every agent has forbidden actions
- Every agent logs decisions
- High-risk actions require human approval
- Every month includes performance and risk review

## Agent registry fields
| Field | Description |
|---|---|
| Agent name | Clear role name |
| Owner | Human accountable person |
| Scope | What it can do |
| Data access | What it can read |
| Actions | What it can execute |
| Approval gate | When human approval is required |
| Logs | What must be recorded |
| KPI | How success is measured |
| Risk | Main failure modes |

## Human approval required for
- Sending external messages at scale
- Changing prices/offers
- Deleting data
- Exporting customer data
- Making financial commitments
- Making legal claims
- Publishing content
