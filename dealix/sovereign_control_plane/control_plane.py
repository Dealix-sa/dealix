"""
Sovereign Control Plane facade — §110.

Owns one instance of every component and wires them together. A
module-level singleton is exposed via ``get_control_plane()``.
"""

from __future__ import annotations

import threading
from typing import Any

from dealix.sovereign_control_plane.agent_runtime import AgentRuntime
from dealix.sovereign_control_plane.approvals import SovereignApprovalCenter
from dealix.sovereign_control_plane.assets import AssetLibrary
from dealix.sovereign_control_plane.classification import Classifier
from dealix.sovereign_control_plane.context_feed import ContextFeedEngine
from dealix.sovereign_control_plane.customer_loop import CustomerValueLoop
from dealix.sovereign_control_plane.events import EventBus
from dealix.sovereign_control_plane.health import SystemHealth
from dealix.sovereign_control_plane.hermes import HermesOrchestrator, RoutingPlan
from dealix.sovereign_control_plane.identity import IdentityRegistry
from dealix.sovereign_control_plane.incidents import IncidentLog
from dealix.sovereign_control_plane.intelligence_graph import IntelligenceGraph
from dealix.sovereign_control_plane.marketplace import MarketplaceReadiness
from dealix.sovereign_control_plane.mcp_gateway import MCPGateway
from dealix.sovereign_control_plane.memory import MemoryManager
from dealix.sovereign_control_plane.money_command import MoneyCommand
from dealix.sovereign_control_plane.observability import Dashboard, RedFlags
from dealix.sovereign_control_plane.offers import OfferRegistry
from dealix.sovereign_control_plane.partner_loop import PartnerValueLoop
from dealix.sovereign_control_plane.policy import PolicyEngine
from dealix.sovereign_control_plane.public_api import PublicAPIReadiness
from dealix.sovereign_control_plane.security_modes import SecurityModeManager
from dealix.sovereign_control_plane.tool_gateway import HermesToolGateway, ToolRegistry
from dealix.sovereign_control_plane.tool_runtime import ToolRuntimeLog
from dealix.sovereign_control_plane.types import IncidentSeverity, SecurityMode
from dealix.sovereign_control_plane.venture_loop import VentureValueLoop
from dealix.sovereign_control_plane.workspace import WorkspaceRegistry


class SovereignControlPlane:
    def __init__(self) -> None:
        self.identities = IdentityRegistry()
        self.workspaces = WorkspaceRegistry()
        self.classifier = Classifier()
        self.memory = MemoryManager()
        self.bus = EventBus()
        self.context_feed = ContextFeedEngine()
        self.policy = PolicyEngine()
        self.approvals = SovereignApprovalCenter(self.bus)
        self.security = SecurityModeManager(self.identities)
        self.incidents = IncidentLog(self.bus, self.security)
        self.bus.set_incident_sink(
            lambda kind, summary: self.incidents.create(
                kind, IncidentSeverity.MEDIUM, source="event_bus", summary=summary,
            )
        )
        self.tool_registry = ToolRegistry()
        self.tool_log = ToolRuntimeLog()
        self.tool_gateway = HermesToolGateway(
            self.tool_registry, self.policy, self.approvals, self.tool_log, self.bus,
        )
        self.mcp_gateway = MCPGateway()
        self.hermes = HermesOrchestrator(
            self.identities, self.workspaces, self.context_feed,
            self.policy, self.approvals, self.tool_gateway,
            self.bus, self.memory,
        )
        self.runtime = AgentRuntime(
            self.context_feed, self.policy, self.approvals,
            self.tool_gateway, self.tool_log, self.security, self.bus,
        )
        self.offer_registry = OfferRegistry()
        self.asset_library = AssetLibrary()
        self.money_command = MoneyCommand()
        self.intelligence = IntelligenceGraph()
        self.customers = CustomerValueLoop()
        self.partners = PartnerValueLoop()
        self.ventures = VentureValueLoop()
        self.public_api = PublicAPIReadiness()
        self.marketplace = MarketplaceReadiness()
        self.red_flags = RedFlags(
            self.runtime, self.tool_log, self.tool_registry, self.approvals,
        )
        self.dashboard = Dashboard(
            self.runtime, self.tool_log, self.tool_registry,
            self.approvals, self.incidents, self.bus,
        )
        self.system_health = SystemHealth(
            bus=self.bus, runtime=self.runtime, tool_log=self.tool_log,
            approvals=self.approvals, money=self.money_command,
            assets=self.asset_library, incidents=self.incidents,
            security=self.security, red_flags=self.red_flags,
        )
        # Bootstrap Sami + one workspace per kind.
        sami = self.identities.register_sami()
        self.workspaces.bootstrap(sami_id=sami.identity_id)

    # ─── High-level API ────────────────────────────────────────
    def submit_signal(self, signal: dict[str, Any]) -> RoutingPlan:
        return self.hermes.route(signal)

    def pending_approvals(self, workspace_id: str | None = None):
        return self.approvals.list_pending(workspace_id)

    def health(self) -> dict[str, Any]:
        return self.system_health.snapshot()

    def money(self) -> dict[str, Any]:
        return self.money_command.snapshot()

    def offers(self):
        return self.offer_registry.list()

    def assets(self):
        return self.asset_library.list()

    def incidents_list(self):
        return self.incidents.list()

    def events_tail(self, n: int = 100):
        return self.bus.tail(n)

    def set_security_mode(self, mode: SecurityMode, actor_id: str) -> dict[str, Any]:
        change = self.security.set_mode(mode, actor_id)
        return change.to_dict()


_GLOBAL: SovereignControlPlane | None = None
_GLOBAL_LOCK = threading.Lock()


def get_control_plane() -> SovereignControlPlane:
    global _GLOBAL
    if _GLOBAL is None:
        with _GLOBAL_LOCK:
            if _GLOBAL is None:
                _GLOBAL = SovereignControlPlane()
    return _GLOBAL
