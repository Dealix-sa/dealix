# Workspace Model

Workspaces are the unit of isolation. Eight types exist:

| Type | Owner | Reach |
|---|---|---|
| `sovereign` | Sami only | Cap table, sovereign memory, S4/S5 actions |
| `dealix_internal` | Internal operators + Sami | Default for kernel rows |
| `customer` | Customer admin | Customer's own pipeline, drafts, value reports |
| `partner` | Partner admin | Partner-attributed deals, lead packs |
| `trust` | Trust operators | Risk register, incidents, audit, MCP review |
| `venture` | Sami + venture team | Vertical experiments |
| `marketplace` | Marketplace publisher | Listings |
| `api` | API client | API surface tenants |

## Identity model (`dealix/hermes/identity/`)

- `User` — typed users (Sami, internal operator, customer admin/user,
  partner admin, agent identity, tool identity, API client, marketplace
  publisher).
- `Tenant` — top-level isolation; carries `data_residency`.
- `Workspace` — typed workspace with `tenant_id` + `sovereignty_isolated`.
- `Role` + `RoleAssignment` — named permission sets per workspace.
- `Permission` + `PermissionSet` — primitive (resource, action) tuples.
- `evaluate_access(request, permissions)` — pure function for tests.

## Cross-workspace rules

- An agent's workspace allow list is set on its `AgentCard`.
- Context packets carry `workspace_id`; the gateway refuses to deliver a
  packet to an agent whose `WorkspaceBoundary` doesn't include it.
- `MCPGateway.invoke` uses the call's implicit workspace (the agent's
  default) and audits it.
