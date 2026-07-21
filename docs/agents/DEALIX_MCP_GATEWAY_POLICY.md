# Dealix MCP Gateway Policy

## Purpose

MCP and tool servers are useful for connecting agents to data and systems, but Dealix must never expose powerful tools directly to an agent without a gateway.

This policy must exist before any Dealix PR enables MCP, tool servers, shell tools, browser tools, production database access, email actions, WhatsApp actions, or CRM writeback.

## Default status

```text
MCP_ENABLED=local_stdio_or_loopback_only
MCP_GATEWAY_REQUIRED=true
MCP_DIRECT_TOOL_ACCESS=false
MCP_PRODUCTION_DB_ACCESS=false
MCP_EXTERNAL_SEND_ACCESS=false
MCP_REMOTE_HTTP_ENABLED=false
MCP_LEGACY_SSE_EXPOSED=false
```

The current tool surface permits only `read` and `local_draft`. `local_draft` requires
human approval and never grants permission to send. External send, payments, production
mutation, shell, raw database access, filesystem writes, credential access, external
network access, and ambient browser sessions are denied.

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

The runtime-enforced subset is registered through `@governed_tool` and includes tool
name, capability, data classes, approval requirement, and external-side-effect status.
It also carries a bounded timeout and per-minute rate limit. The server enforces the rate
limit in-process and emits a metadata-only audit event for every success or error; tool
arguments and results are never written to that event.
Import fails on conflicting or unsafe declarations. `get_mcp_trust_manifest` returns the
sorted runtime manifest plus a deterministic SHA-256, so permission drift is reviewable.
A new tool that bypasses the governed decorator is a release blocker.

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
| Exact HTTP host/origin policy | yes for remote HTTP |
| Auth-enforcing trusted ingress | yes for remote HTTP |
| Public-IP resolution and pinning | yes for outbound MCP clients |

## Remote HTTP gate

Remote binding is allowed only when all conditions are true:

1. `DEALIX_MCP_REMOTE_HTTP_ENABLED=1` is an explicit deployment decision.
2. An upstream ingress actually enforces authentication and the operator attests it with
   `DEALIX_MCP_TRUSTED_INGRESS_AUTH=1`.
3. `DEALIX_MCP_ALLOWED_HOSTS` contains exact public hostnames only.
4. `DEALIX_MCP_ALLOWED_ORIGINS` contains exact HTTPS origins only.
5. FastMCP receives those lists through `allowed_hosts` and `allowed_origins`.

Wildcards, URL credentials, non-HTTPS origins, implicit public binding, and the legacy
SSE CLI transport are rejected.

## Outbound MCP endpoints

Candidate endpoints must pass `validate_mcp_endpoint()` before any client connection:

- exact hostname allowlist;
- HTTPS on port 443;
- no URL credentials, query, or fragment;
- DNS must resolve only to globally routable addresses;
- connect only to a returned address while preserving the original hostname for TLS.

Before reconnecting, `revalidate_mcp_endpoint()` compares the resolution fingerprint.
Any change is blocked pending fresh approval. This prevents an approved name from silently
rebinding to localhost, private networks, cloud metadata, or a new address.

## Dealix integration plan

Phase 1:

- documentation only
- no MCP runtime
- no server activation
- no production credentials

Phase 2 (current bounded implementation):

- local read-only/draft-only MCP sandbox
- manifest validator and fingerprint
- STDIO/loopback default
- no external send or production credentials

Phase 3:

- approved read-only connectors
- HubSpot read-only or CSV read-only
- no live send

Phase 4:

- controlled write tools only after human approval cards and audit logs exist

## Proof and rollback

Required verification:

```bash
python3 -m pytest tests/test_mcp_trust_gate.py tests/test_mcp_server.py -q --no-cov
ruff check mcp_server/trust_gate.py mcp_server/dealix_mcp.py tests/test_mcp_trust_gate.py
python3 -m compileall -q mcp_server/trust_gate.py mcp_server/dealix_mcp.py
```

Rollback is a normal PR revert. Do not weaken the gate to recover a deployment; restore
STDIO/loopback mode or fix the ingress, host, origin, authentication, or DNS proof.

## Safety reminder

Dealix's competitive edge is not uncontrolled autonomy. It is controlled operating leverage:

```text
prepare automatically -> review visibly -> act safely -> prove what happened
```
