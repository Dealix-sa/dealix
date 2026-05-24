# `dealix/control_plane/` — Level Max System

This package is the **sovereign kernel** of Dealix. It implements the Level Max
System Spec (sections 51–80) defined in
[`docs/level_max/DEALIX_LEVEL_MAX_SYSTEM_SPEC_AR.md`](../../docs/level_max/DEALIX_LEVEL_MAX_SYSTEM_SPEC_AR.md).

> **Dealix ≠ App.** Dealix **= Control Plane.**

## Module map

| Section | Module | Purpose |
| --- | --- | --- |
| 51 | `sovereignty.py` | `SovereigntyTier`, `SOVEREIGNTY_ORDER`, `assert_sovereignty` |
| 52 | `identity_access.py` | `Identity`, `IdentityKind`, `Permission`, `IdentityRegistry`, delegation |
| 53 | `tenants.py` | `Tenant`, `Workspace`, `WorkspaceKind`, `TenantRegistry` |
| 54 | `data_classification.py` | `DataClass`, `DataClassificationPolicy`, `DataRecord` |
| 55–56 | `context_feed.py` | `ContextFeedEngine`, `ContextPacket`, `AllowedUse` |
| 57 | `memory_system.py` | `MemorySystem`, `MemoryKind` (7 kinds) |
| 58 | `policy_engine.py` | `PolicyEngine`, `Policy`, `standard_policies()` |
| 59 | `approval_center.py` | `ApprovalCenter`, `ApprovalCard`, `SovereigntyLevel` |
| 60 | `audit_evidence.py` | `AuditLog`, `AuditEvent`, `EvidencePack`, `EvidenceTrigger` |
| 61 | `agent_runtime.py` | `AgentRun`, `AgentRunStatus`, `AgentRunRegistry` |
| 62 | `tool_runtime.py` | `ToolRegistry`, `ToolCall`, `ToolDescriptor`, `ToolRiskLevel` |
| 63 | `mcp_gateway.py` | `MCPGateway`, `MCPServer`, kill switch |
| 64 | `security_modes.py` | 5 `SecurityMode`s, `SecurityModeManager` (Sami-only switches) |
| 65 | `incident_response.py` | `IncidentLog`, `Incident`, 8 `IncidentType`s |
| 66 | `money_command.py` | `MoneyCommand`, `DealRoom`, `MoneySnapshot` |
| 67 | `offer_system.py` | `OfferSystem`, `Offer`, `OfferState`, `OfferMetrics` |
| 68 | `asset_library.py` | `AssetLibrary`, `Asset`, `AssetType` |
| 69 | `intelligence_graph.py` | `IntelligenceGraph`, `Node`, `Edge`, kinds |
| 70 | `scale_kill_board.py` | `ScaleKillBoard`, `ScaleScore`, `KillReason` |
| 71 | `customer_loop.py` | `CustomerValueLoop`, `CustomerValueReport` |
| 72 | `partner_loop.py` | `PartnerValueLoop`, `Partner`, `PartnerRiskKind` |
| 73 | `venture_loop.py` | `VentureValueLoop`, `Venture`, `VentureStage` |
| 74 | `public_api.py` | `PublicAPIReadiness` — S4 launch gate |
| 75 | `marketplace.py` | `MarketplaceReadiness` — S4 launch gate |
| 77 | `health_dashboard.py` | `HealthDashboard`, `HealthMetrics`, `RedFlag` |
| 78 | `commercial_packaging.py` | `CommercialPackaging` (Entry/Expansion/Enterprise) |
| 79–80 | `system.py` | `ControlPlane`, `build_default_control_plane()` |

## Quick start

```python
from dealix.control_plane import (
    build_default_control_plane,
    Identity,
    IdentityKind,
    SecurityMode,
)

cp = build_default_control_plane()  # Sami + sovereign workspace are pre-seeded

# Register a worker agent
cp.identities.register(
    Identity(identity_id="agent_x", kind=IdentityKind.AGENT, display_name="Agent X")
)

# Ask for an external action — gets a pending Approval Card
card = cp.request_external_action(
    requester=cp.identities.get("agent_x"),
    action_type="send_proposal",
    risk_level="medium",
    summary="Send proposal to Acme",
)

# Only Sami can decide
cp.approvals.approve(approval_id=card.approval_id, actor=cp.sami())

# When Sami is ready, switch out of Draft-Only
cp.switch_mode(target=SecurityMode.APPROVAL_GATED, note="audit + outcomes proven")
```

## Doctrine guarantees

- **Sami sovereignty** — the security mode can only be switched by `IdentityKind.SAMI`.
- **No external action without approval** — `request_external_action` always
  creates an `ApprovalCard` at `S2_SAMI_APPROVAL` level.
- **No raw context** — agents only receive `ContextPacket`s with TTL,
  `allowed_use`, and `sensitivity` stamped on the packet.
- **Outcome required** — an `AgentRun` cannot `complete()` if
  `outcome_required` is true and no `outcome_id` was set.
- **MCP rug-pull defence** — `MCPGateway.report_manifest()` quarantines any
  server whose manifest hash drifts from the registered value.
- **S4 launch gates** — Public API + Marketplace refuse to launch without an
  approved `S4_LAUNCH_GATE` card from Sami.

## HTTP surface

`api/routers/control_plane_os.py` exposes read-only snapshots:

```
GET /api/v1/control-plane/health
GET /api/v1/control-plane/snapshot
GET /api/v1/control-plane/sovereignty
GET /api/v1/control-plane/security-mode
GET /api/v1/control-plane/commercial-packaging
GET /api/v1/control-plane/health-flags
GET /api/v1/control-plane/scale-kill-board
GET /api/v1/control-plane/money-snapshot
GET /api/v1/control-plane/intelligence-graph/summary
GET /api/v1/control-plane/public-api-readiness
GET /api/v1/control-plane/marketplace-readiness
```

Mutating endpoints are intentionally not exposed over HTTP — the kernel is
mutated through Python only until an S4 launch gate has been approved.
