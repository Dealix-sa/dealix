"""HermesKernel — the single entry point that wires every module.

Constructing a HermesKernel gives you a fully-wired in-memory sovereign
OS. The Trust Gateway interposes between agents and tools; the
Sovereignty layer guards every decision; the No-Orphan auditor watches
everything.

    from dealix.hermes.kernel import HermesKernel
    k = HermesKernel()
    sig = k.signals.receive(Signal.make(source='email', domain='money', summary='lead'))
    ...

Stateless. Pass a kernel to a function rather than mutating module
globals. Production should subclass and override the storage hooks.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.audit.no_orphan import NoOrphanAudit, OrphanReport
from dealix.hermes.audit.red_flags import RedFlagDetector
from dealix.hermes.core.assets import AssetRegistry
from dealix.hermes.core.decisions import DecisionLog
from dealix.hermes.core.events import EventBus
from dealix.hermes.core.executions import ExecutionPlanner
from dealix.hermes.core.opportunities import OpportunityBook
from dealix.hermes.core.outcomes import OutcomeLedger
from dealix.hermes.core.scoring import OpportunityScorer
from dealix.hermes.core.signals import SignalInbox
from dealix.hermes.sovereignty.approval_rules import ApprovalRules
from dealix.hermes.sovereignty.capital_allocation import CapitalLedger
from dealix.hermes.sovereignty.classifier import SovereigntyClassifier
from dealix.hermes.sovereignty.decision_journal import DecisionJournal
from dealix.hermes.sovereignty.kill_switch import KillSwitch
from dealix.hermes.sovereignty.sovereign_memory import SovereignMemory
from dealix.hermes.trust.agent_registry import AgentRegistry
from dealix.hermes.trust.approvals import ApprovalCenter
from dealix.hermes.trust.audit import AuditLog
from dealix.hermes.trust.evidence import EvidenceStore
from dealix.hermes.trust.guardrails import Guardrails
from dealix.hermes.trust.incident_response import IncidentRegister
from dealix.hermes.trust.mcp_security import MCPGateway
from dealix.hermes.trust.permissions import PermissionMatrix, PermissionVerdict
from dealix.hermes.trust.risk_scores import RiskScoreboard
from dealix.hermes.trust.tool_registry import ToolRegistry


@dataclass
class HermesKernel:
    # Sovereignty
    kill_switch: KillSwitch = field(default_factory=KillSwitch)
    classifier: SovereigntyClassifier = field(default_factory=SovereigntyClassifier)
    journal: DecisionJournal = field(default_factory=DecisionJournal)
    sovereign_memory: SovereignMemory = field(default_factory=SovereignMemory)
    capital_ledger: CapitalLedger = field(default_factory=CapitalLedger)

    # Trust
    agents: AgentRegistry = field(default_factory=AgentRegistry)
    tools: ToolRegistry = field(default_factory=ToolRegistry)
    approval_center: ApprovalCenter = field(default_factory=ApprovalCenter)
    guardrails: Guardrails = field(default_factory=Guardrails)
    evidence: EvidenceStore = field(default_factory=EvidenceStore)
    audit_log: AuditLog = field(default_factory=AuditLog)
    mcp: MCPGateway = field(default_factory=MCPGateway)
    incidents: IncidentRegister = field(default_factory=IncidentRegister)
    risk: RiskScoreboard = field(default_factory=RiskScoreboard)

    # Core kernel
    signals: SignalInbox = field(default_factory=SignalInbox)
    opportunities: OpportunityBook = field(default_factory=OpportunityBook)
    executions: ExecutionPlanner = field(default_factory=ExecutionPlanner)
    outcomes: OutcomeLedger = field(default_factory=OutcomeLedger)
    assets: AssetRegistry = field(default_factory=AssetRegistry)
    scorer: OpportunityScorer = field(default_factory=OpportunityScorer)
    bus: EventBus = field(default_factory=EventBus)

    def __post_init__(self) -> None:
        # Wire derived components that need other parts of the kernel.
        self.approval_rules = ApprovalRules(kill_switch=self.kill_switch)
        self.decisions = DecisionLog(approval_rules=self.approval_rules, journal=self.journal)
        self.permissions = PermissionMatrix(self.agents, self.tools)

    # ------------------------------------------------------------------
    # Trust Gateway — single doorway every tool call must pass through.
    # ------------------------------------------------------------------
    def call_tool(
        self,
        *,
        agent_id: str,
        tool_id: str,
        action: str,
        args: dict,
        evidence_decision_id: str | None = None,
    ) -> PermissionVerdict:
        """Vet a tool call. Records every gate decision in the audit log."""
        verdict = self.permissions.check(agent_id=agent_id, tool_id=tool_id)
        level, reason = self.classifier.classify(action)
        approval = self.approval_rules.evaluate(action=action, level=level, domain="trust")

        allowed = verdict.allowed and approval.allowed and approval.auto and not approval.requires_approver
        if verdict.allowed and approval.allowed and not approval.auto:
            # External-facing or approval-required path — queue, don't run.
            self.approval_center.request(
                requested_by=agent_id,
                action=action,
                payload={"tool_id": tool_id, "args": args, "level": level.label, "reason": approval.reason},
            )

        self.audit_log.record(
            actor=agent_id,
            action=action,
            target=tool_id,
            verdict="allow" if allowed else "deny",
            detail={
                "permission_reason": verdict.reason,
                "sovereignty_reason": approval.reason,
                "level": level.label,
            },
        )

        if evidence_decision_id is not None and (verdict.allowed and approval.allowed):
            pack = self.evidence.open(evidence_decision_id)
            pack.add("tool_call", tool_id, {"action": action, "args": args, "level": level.label})
            pack.seal()

        return PermissionVerdict(
            allowed=allowed,
            reason=f"perm: {verdict.reason} | sovereignty: {approval.reason}",
            requires_approval=not approval.auto and approval.allowed,
        )

    # ------------------------------------------------------------------
    # Audit + red flags.
    # ------------------------------------------------------------------
    def no_orphan_audit(
        self,
        *,
        active_customers: list[str] | None = None,
        customer_value_reports: dict[str, bool] | None = None,
        active_partners: list[str] | None = None,
        partner_reviews: dict[str, bool] | None = None,
    ) -> OrphanReport:
        audit = NoOrphanAudit(
            signals=self.signals,
            opportunities=self.opportunities,
            executions=self.executions,
            outcomes=self.outcomes,
            tools=self.tools,
            agents=self.agents,
            assets=self.assets,
        )
        return audit.run(
            active_customers=active_customers,
            customer_value_reports=customer_value_reports,
            active_partners=active_partners,
            partner_reviews=partner_reviews,
        )

    def red_flags(self) -> list:
        report = self.no_orphan_audit()
        return RedFlagDetector().detect(
            orphan_report=report,
            approval_center=self.approval_center,
            incidents=self.incidents,
        )


__all__ = ["HermesKernel"]
