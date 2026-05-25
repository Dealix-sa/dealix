# Data Boundaries

Hermes enforces the following rules at runtime:

- An agent never reads data from a workspace it isn't scoped to.
- A partner never sees data from a customer it isn't bound to.
- A customer never sees Dealix-internal tools or outcomes.
- Sovereign data never leaves the platform.

## Context Packets

Agents receive a `ContextPacket`, not a database handle. The packet
declares purpose, allowed uses, sensitivity, included objects, and
excluded objects. The global exclude list always covers:

- `sovereign_memory`
- `internal_strategy`
- `payment_secrets`

## Tenant Isolation

`tenant_isolation.enforce_isolation(records, workspace_id)` rejects
any record whose `workspace_id` does not match the caller's. Cross-
tenant joins are impossible by construction.

## Retention

Datasets carry retention policies:

| Dataset | Classification | Retain | Purge |
| --- | --- | --- | --- |
| `audit_log` | CONFIDENTIAL | 365d | 1825d |
| `outcome_records` | INTERNAL | 730d | 1825d |
| `lead_data` | REGULATED | 180d | 365d |
| `customer_deliverables` | CONFIDENTIAL | 1095d | 1825d |
| `sovereign_memory` | SOVEREIGN | 36500d | 36500d |
