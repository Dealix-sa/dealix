# Data Classification

Hermes uses five classification levels:

| Level | Examples | Default reach |
|---|---|---|
| **PUBLIC** | Marketing copy, GEO pages | All agents |
| **INTERNAL** | Internal notes, dashboards | All internal agents |
| **CONFIDENTIAL** | Customer emails, pricing | Customer-scoped agents only |
| **RESTRICTED** | PII, IBAN, salary, IDs | Trust-plane agents only |
| **SOVEREIGN** | Cap table, sovereign memory | Sami only |

## How it's enforced

### `data/classification.py`
`classify_field(name)` returns a `DataClass` heuristically from the field
name (password → RESTRICTED, iban → RESTRICTED, cap_table → SOVEREIGN,
email → CONFIDENTIAL, …).

### `data/boundaries.py`
Every agent has a `DataBoundary` declaring `max_classification`.
`can_read(cls)` checks the ordered list.

### `data/context_packets.py`
Agents never read the database. The orchestrator hydrates a
`ContextPacket` with `purpose`, `sensitivity`, `allowed_use`, `data`,
and `expires_at`. Packets are short-lived (default 1 hour) and never
cross workspaces.

### `data/redaction.py`
`redact_pii(text)` substitutes `[EMAIL] [PHONE] [ID] [IBAN]` placeholders.

### `data/memory.py`
Per-agent memory namespaced by `(agent_id, workspace_id)`. Never shared.

## Doctrine

- The default classification for unknown fields is `INTERNAL`, not
  `PUBLIC`.
- Any agent that asks for `CONFIDENTIAL`+ data is logged.
- Tools flagged `pdpl_relevant=True` get an extra check in the data
  policy rule.
