# Dealix MCP Gateway Policy

## Purpose

MCP and tool servers are useful for connecting agents to data and systems, but Dealix must never expose powerful tools directly to an agent without a gateway.

This policy must exist before any Dealix PR enables MCP, tool servers, shell tools, browser tools, production database access, email actions, WhatsApp actions, or CRM writeback.

## Default status

```text
MCP_ENABLED=false
MCP_GATEWAY_REQUIRED=true
MCP_DIRECT_TOOL_ACCESS=false
MCP_PRODUCTION_DB_ACCESS=false
MCP_EXTERNAL_SEND_ACCESS=false
```

## Approved path

```text
Agent request
-> Gateway policy check
-> Tool manifest check
-> Permission scope check
-> Input validation
-> Secret redaction
-> Network boundary check
-> Human approval if external action
-> Tool call
-> Audit event
-> Proof/provenance log
```

## Tool manifest requirements

Every tool must declare:

```text
tool_name:
owner:
purpose:
allowed_inputs:
blocked_inputs:
allowed_outputs:
network_access:
write_access:
external_action:
requires_human_approval:
timeout_seconds:
rate_limit:
secret_handling:
logging:
rollback_plan:
```

## Blocked by default

Do not allow MCP tools to:

- read unrestricted filesystem paths
- run arbitrary shell commands
- access production Postgres directly
- send email
- send WhatsApp
- send SMS
- scrape websites aggressively
- bypass site protections
- read secrets or `.env` values into prompts
- modify CRM records without approval
- create invoices or payments without approval
- publish public content without approval

## Required security gates

| Gate | Required |
|---|---|
| Tool allowlist | yes |
| Tool manifest review | yes |
| Secret redaction | yes |
| Input validation | yes |
| Timeout | yes |
| Rate limit | yes |
| Audit log | yes |
| Human approval for external actions | yes |
| Production data minimization | yes |
| Rollback plan | yes |

## Dealix integration plan

Phase 1:

- documentation only
- no MCP runtime
- no server activation
- no production credentials

Phase 2:

- local read-only MCP sandbox
- fake/demo data only
- manifest validator
- audit report

Phase 3:

- approved read-only connectors
- HubSpot read-only or CSV read-only
- no live send

Phase 4:

- controlled write tools only after human approval cards and audit logs exist

## Safety reminder

Dealix's competitive edge is not uncontrolled autonomy. It is controlled operating leverage:

```text
prepare automatically -> review visibly -> act safely -> prove what happened
```
