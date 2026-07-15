"""
Sections 79–80 — ControlPlane facade.

> Dealix is a sovereign control plane that turns signals into governed
> execution, measurable outcomes, reusable assets, and scalable revenue.

The `ControlPlane` class wires every Level Max layer into a single
sovereign object. It exposes high-level operations that compose the
sub-systems while keeping every doctrine guardrail intact:

    - Only Sami may switch security modes.
    - No external action without an approved card.
    - Outcomes are required to complete an agent run.
    - Public API / Marketplace require S4 launch gates.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from dealix.control_plane.agent_runtime import (
    AgentRun,
    AgentRunRegistry,
    AgentRunStatus,
)
from dealix.control_plane.approval_center import (
    ApprovalCard,
    ApprovalCenter,
    ApprovalDecision,
    SovereigntyLevel,
)
from dealix.control_plane.asset_library import AssetLibrary, AssetType
from dealix.control_plane.audit_evidence import AuditLog, EvidenceTrigger
from dealix.control_plane.commercial_packaging import CommercialPackaging
from dealix.control_plane.context_feed import (
    AllowedUse,
    ContextFeedEngine,
    ContextPacket,
)
from dealix.control_plane.customer_loop import CustomerValueLoop
from dealix.control_plane.data_classification import (
    DataClass,
    DataClassificationPolicy,
)
from dealix.control_plane.health_dashboard import HealthDashboard, RedFlag
from dealix.control_plane.identity_access import (
    Identity,
    IdentityKind,
    IdentityRegistry,
    Permission,
)
from dealix.control_plane.incident_response import (
    Incident,
    IncidentLog,
    IncidentSeverity,
    IncidentType,
)
from dealix.control_plane.intelligence_graph import (
    EdgeKind,
    IntelligenceGraph,
    NodeKind,
)
from dealix.control_plane.marketplace import MarketplaceReadiness
from dealix.control_plane.mcp_gateway import MCPGateway
from dealix.control_plane.memory_system import MemorySystem
from dealix.control_plane.money_command import MoneyCommand
from dealix.control_plane.offer_system import OfferSystem
from dealix.control_plane.partner_loop import PartnerValueLoop
from dealix.control_plane.policy_engine import (
    Policy,
    PolicyDecision,
    PolicyEngine,
    PolicyResult,
    standard_policies,
)
from dealix.control_plane.public_api import PublicAPIReadiness
from dealix.control_plane.scale_kill_board import ScaleKillBoard
from dealix.control_plane.security_modes import SecurityMode, SecurityModeManager
from dealix.control_plane.sovereignty import SovereigntyTier
from dealix.control_plane.tenants import (
    Tenant,
    TenantRegistry,
    Workspace,
    WorkspaceKind,
)
from dealix.control_plane.tool_runtime import (
    ToolCall,
    ToolCallStatus,
    ToolDescriptor,
    ToolRegistry,
)
from dealix.control_plane.venture_loop import VentureValueLoop


@dataclass
class ControlPlane:
    """The sovereign control plane facade. Wire it once per process."""

    identities: IdentityRegistry = field(default_factory=IdentityRegistry)
    tenants: TenantRegistry = field(default_factory=TenantRegistry)
    context_feed: ContextFeedEngine = field(default_factory=ContextFeedEngine)
    memory: MemorySystem = field(default_factory=MemorySystem)
    policy_engine: PolicyEngine = field(default_factory=PolicyEngine)
    approvals: ApprovalCenter = field(default_factory=ApprovalCenter)
    audit: AuditLog = field(default_factory=AuditLog)
    agent_runs: AgentRunRegistry = field(default_factory=AgentRunRegistry)
    tool_registry: ToolRegistry = field(default_factory=ToolRegistry)
    mcp_gateway: MCPGateway = field(init=False)
    security_mode_manager: SecurityModeManager = field(
        default_factory=lambda: SecurityModeManager(SecurityMode.DRAFT_ONLY)
    )
    incidents: IncidentLog = field(default_factory=IncidentLog)
    money: MoneyCommand = field(default_factory=MoneyCommand)
    offers: OfferSystem = field(default_factory=OfferSystem)
    assets: AssetLibrary = field(default_factory=AssetLibrary)
    graph: IntelligenceGraph = field(default_factory=IntelligenceGraph)
    scale_kill: ScaleKillBoard = field(default_factory=ScaleKillBoard)
    customers: CustomerValueLoop = field(default_factory=CustomerValueLoop)
    partners: PartnerValueLoop = field(default_factory=PartnerValueLoop)
    ventures: VentureValueLoop = field(default_factory=VentureValueLoop)
    public_api: PublicAPIReadiness = field(default_factory=PublicAPIReadiness)
    marketplace: MarketplaceReadiness = field(default_factory=MarketplaceReadiness)
    health: HealthDashboard = field(default_factory=HealthDashboard)
    commercial: CommercialPackaging = field(default_factory=CommercialPackaging)
    sami_id: str = "sami"
    sovereign_tenant_id: str = "tenant_sovereign"
    sovereign_workspace_id: str = "ws_sovereign"

    def __post_init__(self) -> None:
        self.mcp_gateway = MCPGateway(tool_registry=self.tool_registry)
        for policy in standard_policies():
            self.policy_engine.register(policy)

    # ── Sovereign helpers ─────────────────────────────────────────

    def sami(self) -> Identity:
        return self.identities.get(self.sami_id)

    def evaluate(self, action: Mapping[str, Any]) -> PolicyResult:
        return self.policy_engine.evaluate(action)

    def request_external_action(
        self,
        *,
        requester: Identity,
        action_type: str,
        risk_level: str,
        summary: str,
        payload_preview: dict[str, Any] | None = None,
        evidence_pack_id: str | None = None,
    ) -> ApprovalCard:
        requester.require(Permission.REQUEST_APPROVAL)
        return self.approvals.request(
            requested_by=requester.identity_id,
            action_type=action_type,
            sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
            risk_level=risk_level,
            summary=summary,
            payload_preview=payload_preview,
            evidence_pack_id=evidence_pack_id,
        )

    def switch_mode(self, *, target: SecurityMode, note: str | None = None) -> SecurityMode:
        self.security_mode_manager.switch(actor=self.sami(), target=target, note=note)
        return self.security_mode_manager.mode

    def kill_switch(self) -> None:
        self.mcp_gateway.engage_kill_switch()
        self.security_mode_manager.switch(
            actor=self.sami(),
            target=SecurityMode.SOVEREIGN_LOCKDOWN,
            note="kill switch engaged",
        )

    # ── Context lifecycle ─────────────────────────────────────────

    def issue_context(
        self,
        *,
        agent_id: str,
        purpose: str,
        workspace_id: str,
        sensitivity: DataClass,
        allowed_use: Iterable[AllowedUse],
        seed: Mapping[str, Any] | None = None,
    ) -> ContextPacket:
        return self.context_feed.issue(
            agent_id=agent_id,
            purpose=purpose,
            workspace_id=workspace_id,
            sensitivity=sensitivity,
            allowed_use=frozenset(allowed_use),
            seed=seed,
        )

    # ── Agent run helpers ─────────────────────────────────────────

    def start_run(
        self,
        *,
        agent_id: str,
        workspace_id: str,
        input_hash: str,
        outcome_required: bool = True,
    ) -> AgentRun:
        run = self.agent_runs.start(
            agent_id=agent_id,
            workspace_id=workspace_id,
            input_hash=input_hash,
            outcome_required=outcome_required,
        )
        self.health.increment("agent_runs")
        self.audit.record(
            actor_type="agent",
            actor_id=agent_id,
            action_type="run_started",
            workspace_id=workspace_id,
        )
        return run

    def record_outcome(self, *, run_id: str, outcome_id: str) -> AgentRun:
        run = self.agent_runs.get(run_id)
        run.outcome_id = outcome_id
        run.status = AgentRunStatus.OUTCOME_PENDING
        run.complete()
        self.health.increment("executions_completed")
        self.health.increment("outcomes_logged")
        return run

    # ── Tool helpers ──────────────────────────────────────────────

    def request_tool(
        self,
        *,
        tool_id: str,
        agent_id: str,
        workspace_id: str,
        arguments: dict[str, Any] | None = None,
    ) -> ToolCall:
        call = self.tool_registry.request(
            tool_id=tool_id,
            agent_id=agent_id,
            workspace_id=workspace_id,
            arguments=arguments,
        )
        self.health.increment("tool_calls")
        self.mcp_gateway.vet_tool_call(call)
        return call

    # ── Doctrine cross-checks ─────────────────────────────────────

    def assert_can_send_external(self, *, data_class: DataClass) -> None:
        if not DataClassificationPolicy.can_send_external(data_class):
            raise PermissionError(
                f"data class {data_class.label} cannot be sent externally"
            )
        if not self.security_mode_manager.allow_external_send():
            raise PermissionError(
                f"security mode {self.security_mode_manager.mode.value} forbids external sends"
            )

    def refresh_health_flags(self) -> list[RedFlag]:
        flags: list[RedFlag] = []
        stuck = self.agent_runs.stuck_without_outcome()
        if stuck:
            flags.append(RedFlag.EXECUTIONS_WITHOUT_OUTCOMES)
        pending = self.approvals.pending()
        for card in pending:
            if card.sovereignty_level is SovereigntyLevel.S2_SAMI_APPROVAL:
                flags.append(RedFlag.EXTERNAL_ACTIONS_WITHOUT_APPROVAL)
                break
        for tool in self.tool_registry.all():
            if not tool.owner_identity_id:
                flags.append(RedFlag.TOOLS_WITHOUT_OWNER)
                break
        if self.assets.underused():
            flags.append(RedFlag.ASSETS_NOT_REUSED)
        if self.customers.without_value_reports():
            flags.append(RedFlag.CUSTOMERS_WITHOUT_VALUE_REPORTS)
        if self.partners.without_revenue():
            flags.append(RedFlag.PARTNERS_WITHOUT_REVENUE)
        self.health.red_flags = []
        for flag in flags:
            self.health.raise_flag(flag)
        return flags

    # ── Snapshot ──────────────────────────────────────────────────

    def snapshot(self) -> dict[str, Any]:
        return {
            "sovereignty_order": [t.value for t in SovereigntyTier],
            "security_mode": self.security_mode_manager.mode.value,
            "identities": [i.identity_id for i in self.identities.all()],
            "tenants": [t.tenant_id for t in self.tenants.all_tenants()],
            "money": self.money.snapshot().to_dict(),
            "intelligence_graph": self.graph.summary(),
            "scale_kill": self.scale_kill.render(),
            "public_api": self.public_api.status(),
            "marketplace": self.marketplace.status(),
            "health": self.health.to_dict(),
            "commercial_packaging": self.commercial.to_dict(),
            "memory_stats": self.memory.stats(),
            "open_incidents": [i.to_dict() for i in self.incidents.open()],
            "pending_approvals": [c.to_dict() for c in self.approvals.pending()],
        }


def build_default_control_plane() -> ControlPlane:
    """Construct a ControlPlane with Sami, sovereign tenant, and a workspace."""
    plane = ControlPlane()
    sovereign_tenant = Tenant(
        tenant_id=plane.sovereign_tenant_id,
        display_name="Sami Sovereign",
        is_sovereign=True,
    )
    plane.tenants.register_tenant(sovereign_tenant)
    plane.tenants.register_workspace(
        Workspace(
            workspace_id=plane.sovereign_workspace_id,
            tenant_id=sovereign_tenant.tenant_id,
            kind=WorkspaceKind.SOVEREIGN,
            display_name="Sovereign Workspace",
        )
    )
    plane.tenants.register_workspace(
        Workspace(
            workspace_id="ws_internal_dealix",
            tenant_id=sovereign_tenant.tenant_id,
            kind=WorkspaceKind.INTERNAL_DEALIX,
            display_name="Dealix Internal",
        )
    )
    plane.identities.register(
        Identity(
            identity_id=plane.sami_id,
            kind=IdentityKind.SAMI,
            display_name="Sami",
            tenant_id=sovereign_tenant.tenant_id,
            workspace_id=plane.sovereign_workspace_id,
        )
    )
    return plane
