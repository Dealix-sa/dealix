"""خادم الثقة — agent registry.

Stores every agent the kernel knows about, with permission level,
allowed tools and workspace scopes. Spec §37 enumerates agent families
(Sovereign, Core, Money, Trust, Product, Market, Partner, Customer,
Venture); the seed factory pre-populates one canonical agent per family
so the orchestrator can resolve agent_id lookups out of the box.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from dealix.hermes.core.schemas import WorkspaceScope, utcnow
from dealix.trust.permissions import PermissionLevel


class AgentStatus(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    RETIRED = "retired"


class AgentFamily(StrEnum):
    """Spec §37 — the nine canonical families."""

    SOVEREIGN = "sovereign"
    CORE = "core"
    MONEY = "money"
    TRUST = "trust"
    PRODUCT = "product"
    MARKET = "market"
    PARTNER = "partner"
    CUSTOMER = "customer"
    VENTURE = "venture"


@dataclass
class AgentEntry:
    """One agent's static profile."""

    agent_id: str
    name: str
    family: AgentFamily
    permission_level: PermissionLevel
    allowed_tools: set[str] = field(default_factory=set)
    workspace_scopes: set[WorkspaceScope] = field(default_factory=set)
    owner: str = "sami"
    status: AgentStatus = AgentStatus.ACTIVE
    created_at: datetime = field(default_factory=utcnow)
    pause_reason: str | None = None


class AgentRegistry:
    """In-memory agent registry with simple lookup + assertions."""

    def __init__(self) -> None:
        self._entries: dict[str, AgentEntry] = {}

    # ── CRUD ─────────────────────────────────────────────────
    def register(self, entry: AgentEntry) -> AgentEntry:
        if entry.agent_id in self._entries:
            raise ValueError(f"agent already registered: {entry.agent_id}")
        self._entries[entry.agent_id] = entry
        return entry

    def get(self, agent_id: str) -> AgentEntry:
        try:
            return self._entries[agent_id]
        except KeyError as exc:
            raise KeyError(f"unknown agent: {agent_id}") from exc

    def all(self) -> list[AgentEntry]:
        return list(self._entries.values())

    def list_by_family(self, family: AgentFamily | str) -> list[AgentEntry]:
        target = AgentFamily(family) if isinstance(family, str) else family
        return [e for e in self._entries.values() if e.family == target]

    # ── enforcement ─────────────────────────────────────────
    def assert_active(self, agent_id: str) -> AgentEntry:
        entry = self.get(agent_id)
        if entry.status != AgentStatus.ACTIVE:
            raise PermissionError(
                f"agent {agent_id} is {entry.status.value}"
                + (f" ({entry.pause_reason})" if entry.pause_reason else "")
            )
        return entry

    def assert_can_use_tool(self, agent_id: str, tool_id: str) -> AgentEntry:
        entry = self.assert_active(agent_id)
        if tool_id not in entry.allowed_tools:
            raise PermissionError(
                f"agent {agent_id} not allowed to use tool {tool_id}"
            )
        return entry

    def pause(self, agent_id: str, reason: str) -> AgentEntry:
        entry = self.get(agent_id)
        entry.status = AgentStatus.PAUSED
        entry.pause_reason = reason
        return entry

    def resume(self, agent_id: str) -> AgentEntry:
        entry = self.get(agent_id)
        entry.status = AgentStatus.ACTIVE
        entry.pause_reason = None
        return entry

    def retire(self, agent_id: str) -> AgentEntry:
        entry = self.get(agent_id)
        entry.status = AgentStatus.RETIRED
        return entry


# ─────────────────────────────────────────────────────────────
# Seed registry — one canonical agent per family (spec §37)
# ─────────────────────────────────────────────────────────────


_DEFAULT_AGENTS: list[AgentEntry] = [
    AgentEntry(
        agent_id="SamiCouncilAgent",
        name="Sami Council Agent",
        family=AgentFamily.SOVEREIGN,
        permission_level=PermissionLevel.L6_NEVER_AUTONOMOUS,
        allowed_tools={"crm_sync", "proposal_render"},
        workspace_scopes={WorkspaceScope.SOVEREIGN},
        owner="sami",
    ),
    AgentEntry(
        agent_id="HermesOrchestratorAgent",
        name="Hermes Orchestrator",
        family=AgentFamily.CORE,
        permission_level=PermissionLevel.L5_LOW_RISK_AUTONOMOUS,
        allowed_tools={"crm_sync"},
        workspace_scopes={WorkspaceScope.INTERNAL, WorkspaceScope.TRUST},
    ),
    AgentEntry(
        agent_id="ProposalFactoryAgent",
        name="Proposal Factory",
        family=AgentFamily.MONEY,
        permission_level=PermissionLevel.L4_EXTERNAL_WITH_APPROVAL,
        allowed_tools={"proposal_render", "email_send", "crm_sync"},
        workspace_scopes={WorkspaceScope.CUSTOMER},
    ),
    AgentEntry(
        agent_id="GuardrailAgent",
        name="Guardrail Auditor",
        family=AgentFamily.TRUST,
        permission_level=PermissionLevel.L2_INTERNAL_TASK,
        allowed_tools={"crm_sync", "data_export"},
        workspace_scopes={WorkspaceScope.TRUST},
    ),
    AgentEntry(
        agent_id="OfferBuilderAgent",
        name="Offer Builder",
        family=AgentFamily.PRODUCT,
        permission_level=PermissionLevel.L4_EXTERNAL_WITH_APPROVAL,
        allowed_tools={"landing_page_publish", "crm_sync"},
        workspace_scopes={WorkspaceScope.INTERNAL, WorkspaceScope.MARKETPLACE},
    ),
    AgentEntry(
        agent_id="MarketRadarAgent",
        name="Market Radar",
        family=AgentFamily.MARKET,
        permission_level=PermissionLevel.L1_DRAFT,
        allowed_tools={"crm_sync"},
        workspace_scopes={WorkspaceScope.INTERNAL},
    ),
    AgentEntry(
        agent_id="PartnerPitchAgent",
        name="Partner Pitch",
        family=AgentFamily.PARTNER,
        permission_level=PermissionLevel.L4_EXTERNAL_WITH_APPROVAL,
        allowed_tools={"proposal_render", "email_send", "crm_sync"},
        workspace_scopes={WorkspaceScope.PARTNER},
    ),
    AgentEntry(
        agent_id="CustomerHealthAgent",
        name="Customer Health Monitor",
        family=AgentFamily.CUSTOMER,
        permission_level=PermissionLevel.L3_INTERNAL_UPDATE,
        allowed_tools={"crm_sync", "email_send"},
        workspace_scopes={WorkspaceScope.CUSTOMER},
    ),
    AgentEntry(
        agent_id="VentureScoutAgent",
        name="Venture Scout",
        family=AgentFamily.VENTURE,
        permission_level=PermissionLevel.L1_DRAFT,
        allowed_tools={"crm_sync"},
        workspace_scopes={WorkspaceScope.VENTURE},
    ),
    AgentEntry(
        agent_id="KnowledgeCuratorAgent",
        name="Knowledge Curator",
        family=AgentFamily.CORE,
        permission_level=PermissionLevel.L2_INTERNAL_TASK,
        allowed_tools={"crm_sync"},
        workspace_scopes={WorkspaceScope.INTERNAL},
    ),
    AgentEntry(
        agent_id="RiskOpsAgent",
        name="Risk Ops",
        family=AgentFamily.TRUST,
        permission_level=PermissionLevel.L3_INTERNAL_UPDATE,
        allowed_tools={"crm_sync"},
        workspace_scopes={WorkspaceScope.TRUST},
    ),
]


def seed_default_registry() -> AgentRegistry:
    """Return a pre-populated AgentRegistry covering the §37 families."""
    registry = AgentRegistry()
    for entry in _DEFAULT_AGENTS:
        registry.register(
            AgentEntry(
                agent_id=entry.agent_id,
                name=entry.name,
                family=entry.family,
                permission_level=entry.permission_level,
                allowed_tools=set(entry.allowed_tools),
                workspace_scopes=set(entry.workspace_scopes),
                owner=entry.owner,
            )
        )
    return registry


__all__ = [
    "AgentEntry",
    "AgentFamily",
    "AgentRegistry",
    "AgentStatus",
    "seed_default_registry",
]
