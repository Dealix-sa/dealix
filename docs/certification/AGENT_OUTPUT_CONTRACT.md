# Agent Output Contract

## Purpose

Ensure all Dealix agents and workers produce reviewable, auditable, safe
outputs. Any output that violates this contract is treated as draft-only
and is never used externally.

## Required Fields

Every output JSON under `outputs/agents/*.json` must include:

- `summary` (string)
- `evidence` (string or non-empty array of strings)
- `risk_level` (`Low` | `Medium` | `High` | `Critical`)
- `approval_class` (`A0` | `A1` | `A2` | `A3`)
- `next_action` (string)
- `owner` (string)
- `safe_to_use` (`Yes` | `No` | `Needs Review`)

Schema: [`dealix/contracts/schemas/agent_output_contract.schema.json`](../../dealix/contracts/schemas/agent_output_contract.schema.json).

## Approval Classes

| Class | Meaning |
|---|---|
| `A0` | Internal use, no approval needed. |
| `A1` | Reviewer sign-off required before external use. |
| `A2` | Founder (Sami) approval required before external use. |
| `A3` | Must not be automated. Manual action only. |

## Rules

- Any **A2** output requires Sami approval before external use.
- Any **A3** output **must not** be automated and **must not** be marked
  `safe_to_use=Yes` programmatically.
- Any output without `evidence` is draft-only.
- Any output with sensitive data is private-only — must not be committed.

## Validation

```
python scripts/verify_agent_outputs.py
```

The check passes if `outputs/agents/` is empty (warns) or every file
matches the schema and the A3/safe_to_use rule.
