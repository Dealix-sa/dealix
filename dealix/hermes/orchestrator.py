"""
HermesOrchestrator — the single entry point that wires the kernel,
sovereignty, trust plane, and MCP gateway together.

Use this in API routers and scripts instead of constructing every
store independently. Tests can build orchestrators per-test.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.agents.registry_cards import register_default_agents
from dealix.hermes.kernel.lifecycle import HermesKernel
from dealix.hermes.mcp.anomaly_detection import AnomalyDetector
from dealix.hermes.mcp.gateway import MCPGateway
from dealix.hermes.mcp.runtime_guardrails import RuntimeGuardrails
from dealix.hermes.mcp.server_registry import MCPServerRegistry
from dealix.hermes.sovereignty.approvals import ApprovalCenter
from dealix.hermes.sovereignty.capital_allocation import CapitalAllocator
from dealix.hermes.sovereignty.decision_journal import DecisionJournal
from dealix.hermes.sovereignty.kill_switch import KillSwitch
from dealix.hermes.sovereignty.sovereign_memory import SovereignMemory
from dealix.hermes.trust.agent_registry import AgentRegistry
from dealix.hermes.trust.audit import AuditLog
from dealix.hermes.trust.controls import ControlCatalog
from dealix.hermes.trust.evidence import EvidencePackStore
from dealix.hermes.trust.incident_response import IncidentRegister
from dealix.hermes.trust.permission_matrix import PermissionMatrix
from dealix.hermes.trust.risk_register import RiskRegister
from dealix.hermes.trust.tool_registry import ToolRegistry
from dealix.hermes.trust.trust_check import TrustCheck


@dataclass
class HermesOrchestrator:
    kernel: HermesKernel = field(default_factory=HermesKernel)

    # Sovereignty
    approvals: ApprovalCenter = field(default_factory=ApprovalCenter)
    kill_switch: KillSwitch = field(default_factory=KillSwitch)
    decision_journal: DecisionJournal = field(default_factory=DecisionJournal)
    capital_allocator: CapitalAllocator = field(default_factory=CapitalAllocator)
    sovereign_memory: SovereignMemory = field(default_factory=SovereignMemory)

    # Trust
    agent_registry: AgentRegistry = field(default_factory=AgentRegistry)
    tool_registry: ToolRegistry = field(default_factory=ToolRegistry)
    audit_log: AuditLog = field(default_factory=AuditLog)
    evidence_packs: EvidencePackStore = field(default_factory=EvidencePackStore)
    risk_register: RiskRegister = field(default_factory=RiskRegister)
    incident_register: IncidentRegister = field(default_factory=IncidentRegister)
    control_catalog: ControlCatalog = field(default_factory=ControlCatalog)
    trust_check: TrustCheck = field(default_factory=TrustCheck)
    permission_matrix: PermissionMatrix | None = None

    # MCP
    mcp_server_registry: MCPServerRegistry = field(default_factory=MCPServerRegistry)
    mcp_anomalies: AnomalyDetector = field(default_factory=AnomalyDetector)
    mcp_guardrails: RuntimeGuardrails = field(default_factory=RuntimeGuardrails)
    mcp_gateway: MCPGateway | None = None

    bootstrapped: bool = False

    def bootstrap(self) -> "HermesOrchestrator":
        """Wire derived components and seed default agent cards."""
        if self.bootstrapped:
            return self
        if self.permission_matrix is None:
            self.permission_matrix = PermissionMatrix(
                agents=self.agent_registry,
                tools=self.tool_registry,
            )
        if self.mcp_gateway is None:
            self.mcp_gateway = MCPGateway(
                server_registry=self.mcp_server_registry,
                agent_registry=self.agent_registry,
                audit_log=self.audit_log,
                guardrails=self.mcp_guardrails,
                anomalies=self.mcp_anomalies,
            )
        register_default_agents(self.agent_registry)
        self.bootstrapped = True
        return self


_default: HermesOrchestrator | None = None


def get_orchestrator() -> HermesOrchestrator:
    global _default
    if _default is None:
        _default = HermesOrchestrator().bootstrap()
    return _default


def reset_orchestrator() -> None:
    global _default
    _default = None
