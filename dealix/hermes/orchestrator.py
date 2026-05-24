"""HermesOrchestrator — wires the kernel + trust + engines into one object.

This is the only API external code should reach for when it needs to drive
the Hermes pipeline end-to-end. Stage modules remain importable for tests
and tight coupling cases.
"""

from __future__ import annotations

from dealix.hermes.core.assets import AssetBuilder
from dealix.hermes.core.decisions import DecisionJournal
from dealix.hermes.core.executions import ExecutionPlanner
from dealix.hermes.core.opportunities import OpportunityGraph
from dealix.hermes.core.outcomes import OutcomeLog
from dealix.hermes.core.scale import ScaleEngine
from dealix.hermes.core.signals import SignalIntake
from dealix.hermes.intelligence.market_radar import MarketRadar
from dealix.hermes.money.cash_scout import CashScout
from dealix.hermes.partners.scout import PartnerScout
from dealix.hermes.products.offer_builder import OfferLibrary
from dealix.hermes.products.offer_library import install_defaults as install_offer_defaults
from dealix.hermes.sovereignty import (
    Action,
    GateDecision,
    GateVerdict,
    SovereigntyGate,
)
from dealix.hermes.trust.agent_registry import AgentRegistry, install_defaults as install_agent_defaults
from dealix.hermes.trust.approvals import ApprovalCenter, ApprovalRequest
from dealix.hermes.trust.audit import AuditLog
from dealix.hermes.trust.evidence import EvidencePackBuilder
from dealix.hermes.trust.permissions import PermissionMatrix
from dealix.hermes.trust.tool_registry import ToolRegistry, install_defaults as install_tool_defaults


class HermesOrchestrator:
    def __init__(self) -> None:
        # core
        self.intake = SignalIntake()
        self.opportunities = OpportunityGraph()
        self.decisions = DecisionJournal()
        self.plans = ExecutionPlanner()
        self.outcomes = OutcomeLog()
        self.assets = AssetBuilder()
        self.scale = ScaleEngine()

        # trust
        self.agents = AgentRegistry()
        self.tools = ToolRegistry()
        install_agent_defaults(self.agents)
        install_tool_defaults(self.tools)
        self.permissions = PermissionMatrix(self.agents, self.tools)
        self.gate = SovereigntyGate()
        self.approvals = ApprovalCenter()
        self.audit = AuditLog()
        self.evidence = EvidencePackBuilder()

        # engines
        self.offers = OfferLibrary()
        install_offer_defaults(self.offers)
        self.cash_scout = CashScout(self.opportunities)
        self.market_radar = MarketRadar(self.intake)
        self.partner_scout = PartnerScout()

    # ── high-level pipeline ─────────────────────────────────────────

    def propose(self, action: Action) -> tuple[GateDecision, ApprovalRequest | None]:
        """Run an action through the gate. If approval is required, enqueue
        an ApprovalRequest. Always append an audit entry.
        """
        decision = self.gate.evaluate(action)

        self.audit.append(
            event_type="gate.decision",
            actor=action.proposed_by,
            payload={
                "action_id": action.action_id,
                "action_type": action.action_type,
                "verdict": decision.verdict.value,
                "enforced_level": decision.enforced_level.value,
                "reason": decision.reason,
            },
        )

        if decision.verdict is GateVerdict.QUEUE_APPROVAL:
            req = self.approvals.enqueue(action, decision)
            self.audit.append(
                event_type="approval.enqueued",
                actor=action.proposed_by,
                payload={
                    "request_id": req.request_id,
                    "action_id": action.action_id,
                    "enforced_level": decision.enforced_level.value,
                },
            )
            return decision, req

        return decision, None

    def decide_approval(
        self,
        request_id: str,
        *,
        granted: bool,
        approver: str,
        note: str = "",
    ) -> ApprovalRequest:
        req = self.approvals.decide(
            request_id, granted=granted, approver=approver, note=note
        )
        self.audit.append(
            event_type="approval.decision",
            actor=approver,
            payload={
                "request_id": request_id,
                "granted": granted,
                "note": note,
            },
        )
        return req


__all__ = ["HermesOrchestrator"]
