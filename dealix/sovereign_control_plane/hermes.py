"""
Hermes Orchestrator — §94.

Implements the 14-step decision flow from spec item 94. Each step is a
small private method so the flow is easy to audit, extend, or short
circuit. The result is a ``RoutingPlan`` that downstream runtimes use
to actually execute work (or to surface an approval request).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from dealix.sovereign_control_plane.approvals import SovereignApprovalCenter
from dealix.sovereign_control_plane.classification import Classifier
from dealix.sovereign_control_plane.context_feed import ContextFeedEngine
from dealix.sovereign_control_plane.events import EventBus, make_event
from dealix.sovereign_control_plane.identity import IdentityRegistry
from dealix.sovereign_control_plane.memory import MemoryManager
from dealix.sovereign_control_plane.policy import PolicyEngine
from dealix.sovereign_control_plane.tool_gateway import HermesToolGateway
from dealix.sovereign_control_plane.types import (
    DataSensitivity,
    RiskLevel,
    SovereigntyLevel,
    WorkspaceType,
)
from dealix.sovereign_control_plane.workspace import WorkspaceRegistry


@dataclass
class RoutingPlan:
    opportunity_id: str
    score: float
    sovereignty_level: SovereigntyLevel
    selected_engine: str
    selected_agent: str
    context_id: str | None
    tool_allowlist: list[str]
    trust_check_result: dict[str, Any]
    approval_required: bool
    outcome_required: bool
    approval_id: str | None = None
    rationale: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "opportunity_id": self.opportunity_id,
            "score": self.score,
            "sovereignty_level": self.sovereignty_level.value,
            "selected_engine": self.selected_engine,
            "selected_agent": self.selected_agent,
            "context_id": self.context_id,
            "tool_allowlist": list(self.tool_allowlist),
            "trust_check_result": dict(self.trust_check_result),
            "approval_required": self.approval_required,
            "outcome_required": self.outcome_required,
            "approval_id": self.approval_id,
            "rationale": list(self.rationale),
        }


class HermesOrchestrator:
    def __init__(
        self,
        identities: IdentityRegistry,
        workspaces: WorkspaceRegistry,
        context_feed: ContextFeedEngine,
        policy_engine: PolicyEngine,
        approval_center: SovereignApprovalCenter,
        tool_gateway: HermesToolGateway,
        event_bus: EventBus,
        memory: MemoryManager,
    ) -> None:
        self.identities = identities
        self.workspaces = workspaces
        self.context = context_feed
        self.policy = policy_engine
        self.approvals = approval_center
        self.tools = tool_gateway
        self.bus = event_bus
        self.memory = memory
        self.classifier = Classifier()

    def route(self, signal: dict[str, Any]) -> RoutingPlan:
        rationale: list[str] = []
        opp_id = self._step1_ingest(signal, rationale)
        score = self._step2_score(signal, rationale)
        workspace = self._step3_workspace(signal, rationale)
        sovereignty = self._step4_sovereignty(workspace, rationale)
        sensitivity = self._step5_classify(signal, rationale)
        engine = self._step6_engine(signal, rationale)
        agent = self._step7_agent(signal, rationale)
        context = self._step8_context(agent, workspace.workspace_id, sensitivity, signal, rationale)
        tools = self._step9_tools(signal, rationale)
        trust = self._step10_trust_check(signal, rationale)
        outcomes = self._step11_policy(signal, workspace, rationale)
        approval_id = None
        approval_required = any(o.requires_approval for o in outcomes)
        outcome_required = any(o.outcome_required for o in outcomes)
        if approval_required:
            approval_id = self._step12_approval(signal, workspace.workspace_id, sovereignty, rationale).approval_id
        self._step13_memory(opp_id, signal, sovereignty, rationale)
        plan = RoutingPlan(
            opportunity_id=opp_id, score=score, sovereignty_level=sovereignty,
            selected_engine=engine, selected_agent=agent,
            context_id=context.context_id if context else None,
            tool_allowlist=tools, trust_check_result=trust,
            approval_required=approval_required,
            outcome_required=outcome_required,
            approval_id=approval_id, rationale=rationale,
        )
        self._step14_emit(plan)
        return plan

    # ─── 14 steps ──────────────────────────────────────────────
    def _step1_ingest(self, signal: dict[str, Any], r: list[str]) -> str:
        opp_id = signal.get("opportunity_id") or f"opp_{uuid.uuid4().hex[:12]}"
        r.append(f"ingest:{opp_id}")
        return opp_id

    def _step2_score(self, signal: dict[str, Any], r: list[str]) -> float:
        score = float(signal.get("score", 0.5))
        r.append(f"score:{score}")
        return score

    def _step3_workspace(self, signal: dict[str, Any], r: list[str]):
        kind_str = signal.get("workspace_kind", "DEALIX_INTERNAL")
        kind = WorkspaceType(kind_str)
        ws = self.workspaces.get_by_kind(kind)
        if ws is None:
            sami = self.identities.sami() or self.identities.register_sami()
            self.workspaces.bootstrap(sami_id=sami.identity_id)
            ws = self.workspaces.get_by_kind(kind)
        r.append(f"workspace:{kind.value}")
        return ws

    def _step4_sovereignty(self, workspace, r: list[str]) -> SovereigntyLevel:
        r.append(f"sovereignty:{workspace.sovereignty_level.value}")
        return workspace.sovereignty_level

    def _step5_classify(self, signal: dict[str, Any], r: list[str]) -> DataSensitivity:
        item = self.classifier.classify(signal.get("payload", {}))
        r.append(f"sensitivity:{item.sensitivity.value}")
        return item.sensitivity

    def _step6_engine(self, signal: dict[str, Any], r: list[str]) -> str:
        engine = signal.get("engine", "value_engine_os")
        r.append(f"engine:{engine}")
        return engine

    def _step7_agent(self, signal: dict[str, Any], r: list[str]) -> str:
        agent = signal.get("agent_id", "hermes")
        r.append(f"agent:{agent}")
        return agent

    def _step8_context(
        self, agent: str, workspace_id: str, sensitivity: DataSensitivity,
        signal: dict[str, Any], r: list[str],
    ):
        try:
            pkt = self.context.mint(
                agent_id=agent, workspace_id=workspace_id,
                purpose=signal.get("purpose", "route"),
                sensitivity=sensitivity, allowed_use=["read", "plan"],
                data=signal.get("payload", {}),
            )
            r.append(f"context:{pkt.context_id}")
            return pkt
        except PermissionError as exc:
            r.append(f"context:refused:{exc}")
            return None

    def _step9_tools(self, signal: dict[str, Any], r: list[str]) -> list[str]:
        tools = list(signal.get("tools_requested", []))
        r.append(f"tools:{len(tools)}")
        return tools

    def _step10_trust_check(self, signal: dict[str, Any], r: list[str]) -> dict[str, Any]:
        result = {"passed": True, "findings": []}
        if "guaranteed" in str(signal).lower():
            result = {"passed": False, "findings": ["forbidden_claim:guaranteed"]}
        r.append(f"trust:{result['passed']}")
        return result

    def _step11_policy(self, signal: dict[str, Any], workspace, r: list[str]):
        event = {
            "workspace_kind": workspace.kind.value,
            "action_type": signal.get("action_type", "internal"),
            "sensitivity": signal.get("sensitivity"),
            "tool_risk": signal.get("tool_risk"),
        }
        outcomes = self.policy.evaluate(event)
        r.append(f"policy_outcomes:{len(outcomes)}")
        return outcomes

    def _step12_approval(
        self, signal: dict[str, Any], workspace_id: str,
        sovereignty: SovereigntyLevel, r: list[str],
    ):
        req = self.approvals.submit(
            requested_by=signal.get("requested_by", "hermes"),
            workspace_id=workspace_id,
            action_type=signal.get("approval_action_type", "sensitive_workflow"),
            sovereignty_level=sovereignty,
            risk_level=RiskLevel(signal.get("risk_level", "medium")),
            summary=signal.get("summary", "hermes routing approval"),
            payload_preview={"signal": signal},
        )
        r.append(f"approval:{req.approval_id}")
        return req

    def _step13_memory(
        self, opp_id: str, signal: dict[str, Any],
        sovereignty: SovereigntyLevel, r: list[str],
    ) -> None:
        from dealix.sovereign_control_plane.memory import MemoryKind
        store = self.memory.store(MemoryKind.OUTCOME)
        store.write(opp_id, "last_signal", signal, DataSensitivity.INTERNAL)
        r.append("memory:written")

    def _step14_emit(self, plan: RoutingPlan) -> None:
        self.bus.publish(make_event(
            event_type="hermes.routed", source="hermes",
            payload=plan.to_dict(),
            sovereignty_level=plan.sovereignty_level.value,
        ))
