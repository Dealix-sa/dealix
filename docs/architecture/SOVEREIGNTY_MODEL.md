# Sovereignty Model

Sovereignty is the doctrine that Sami's authority is non-delegable for
the actions that move the company. Every action carries one of six
levels, and the Execution Plane refuses to dispatch unless the level's
gate is satisfied.

## The Six Levels

| Level | Meaning | Gate |
|---|---|---|
| **S0_AUTO_SAFE** | Read-only or low-risk internal computation | None |
| **S1_INTERNAL** | Internal write inside `dealix_internal` workspace | None |
| **S2_SAMI_APPROVAL** | External or customer-visible action | `ApprovalCenter.approve` (one approver) |
| **S3_SOVEREIGN_MEMO** | Pricing, strategic, partner-affecting | Approval + a memo in `DecisionJournal` |
| **S4_SOVEREIGN_ONLY** | Public API, marketplace, brand position | Approval + Sami-only |
| **S5_NEVER_AUTONOMOUS** | Money, contracts, equity | Two approvers + memo |

## Classifier

`sovereignty/classifier.py` maps an `ActionContext` to a level:

- `moves_money` or `binds_contract` → **S5**
- `affects_marketplace` or specific sovereign-only actions → **S4**
- `affects_pricing` or `affects_partner` → **S3**
- `external`, `customer_visible`, `pdpl_sensitive`, `affects_public_brand` → **S2**
- workspace = `dealix_internal` → **S1**
- otherwise → **S0**

## Approval Center

`sovereignty/approvals.py` — every S2+ action opens an `ApprovalRequest`.
Required approvers double automatically for S5. Until the request is
`approved`, the Execution Plane will refuse to dispatch.

## Kill Switch

`sovereignty/kill_switch.py` — Sami can suspend any agent, tool,
workflow, MCP server, workspace, public API, marketplace listing, or
"all external actions" with a single call. `is_killed` is checked at
every gateway boundary.

## Decision Journal, Capital Allocator, Sovereign Memory

- **DecisionJournal** — permanent record of every S3+ decision with
  observed outcome + learnings.
- **CapitalAllocator** — per-bucket budget vs spend; spending past a
  budget raises `PermissionError`.
- **SovereignMemory** — append-only facts only Sami can write; can be
  sealed during agent runs to guarantee immutability.
