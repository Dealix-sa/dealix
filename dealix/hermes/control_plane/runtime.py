"""
Hermes Runtime — الـ orchestrator العام لكل request يدخل النظام.

Pipeline:

    1. authorization_gate.check       ─ هل actor مسموح له؟
    2. policy_enforcement.evaluate    ─ هل السياسات تسمح؟ (block ممكن هنا)
    3. sovereignty_gate.assess        ─ ما هو الـ sovereignty level؟ S5 = block
    4. kill_switch                    ─ هل الـ target مُعطَّل؟
    5. (handed to execution / draft   ─ إنتاج draft عبر agent_runtime)
    6. trust_gate.assess              ─ هل المخرج آمن؟
    7. approval_gate.open_ticket      ─ إذا approval_required: HOLD
    8. audit_gate.record (في كل مرحلة)
    9. outcome_required: outcome logger مسؤول عن الإغلاق

`run()` يعيد `RuntimeOutcome` فيه `HermesResponse` جاهز.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..contracts import (
    ContextPacket,
    GateResult,
    HermesResponse,
    RiskAssessment,
    RiskLevel,
    SovereigntyLevel,
)
from .approval_gate import ApprovalGate, ApprovalTicket
from .audit_gate import AuditGate
from .authorization import AuthorizationGate
from .kill_switch import KillSwitch, KillTargetKind
from .policy_enforcement import PolicyEnforcementGate
from .sovereignty_gate import SovereigntyGate
from .trust_gate import TrustGate


@dataclass
class RuntimeOutcome:
    response: HermesResponse
    gate_trace: list[GateResult] = field(default_factory=list)
    approval_ticket: ApprovalTicket | None = None
    request_id: str = ""

    @property
    def held_for_approval(self) -> bool:
        return self.approval_ticket is not None and self.response.success is False is False and bool(
            self.response.risk.get("approval_required")
        )


@dataclass
class DraftBundle:
    """ما ينتجه caller (عادةً execution plane) قبل ما يمر بـ trust gate."""

    text: str
    prices_sar: list[int] = field(default_factory=list)
    urls: list[str] = field(default_factory=list)
    structured: dict[str, Any] = field(default_factory=dict)


class HermesRuntime:
    def __init__(
        self,
        *,
        authorization_gate: AuthorizationGate | None = None,
        policy_gate: PolicyEnforcementGate | None = None,
        sovereignty_gate: SovereigntyGate | None = None,
        trust_gate: TrustGate | None = None,
        approval_gate: ApprovalGate | None = None,
        audit_gate: AuditGate | None = None,
        kill_switch: KillSwitch | None = None,
    ) -> None:
        self.authorization = authorization_gate or AuthorizationGate()
        self.policy = policy_gate or PolicyEnforcementGate()
        self.sovereignty = sovereignty_gate or SovereigntyGate()
        self.trust = trust_gate or TrustGate()
        self.approval = approval_gate or ApprovalGate()
        self.audit = audit_gate or AuditGate()
        self.kill_switch = kill_switch or KillSwitch()

    # ─────────────────────────────────────────────────────────

    def run(
        self,
        *,
        context: ContextPacket,
        intent: str,
        draft: DraftBundle | None = None,
        signals: dict[str, Any] | None = None,
        target_agent_id: str | None = None,
        target_workflow_id: str | None = None,
    ) -> RuntimeOutcome:
        trace: list[GateResult] = []
        actor_id = context.actor.actor_id if context.actor else None

        # 1. authorization
        auth = self.authorization.check(context, intent)
        trace.append(auth)
        self.audit.record(
            request_id=context.request_id,
            stage=auth.stage,
            outcome="pass" if auth.passed else "deny",
            actor_id=actor_id,
            payload_summary={"intent": intent, "reason": auth.reason},
        )
        if not auth.passed:
            return self._deny(context, trace, auth.reason or "unauthorized")

        # 2. policy
        policy = self.policy.evaluate(context, intent, signals)
        trace.append(policy)
        self.audit.record(
            request_id=context.request_id,
            stage=policy.stage,
            outcome="pass" if policy.passed else "deny",
            actor_id=actor_id,
            payload_summary={"intent": intent, "reasons": policy.metadata.get("reasons")},
        )
        if not policy.passed:
            return self._deny(context, trace, policy.reason or "policy denied")

        # 3. sovereignty
        sov = self.sovereignty.assess(context, intent, signals)
        trace.append(sov)
        self.audit.record(
            request_id=context.request_id,
            stage=sov.stage,
            outcome="pass" if sov.passed else "deny",
            actor_id=actor_id,
            payload_summary={
                "sovereignty": sov.sovereignty_override.value if sov.sovereignty_override else None,
                "risk_level": sov.metadata.get("risk_level"),
            },
        )
        if not sov.passed:
            return self._deny(context, trace, sov.reason or "sovereignty block")

        # 4. kill switch (agent / workflow)
        for kind, target in [
            (KillTargetKind.AGENT, target_agent_id),
            (KillTargetKind.WORKFLOW, target_workflow_id),
        ]:
            if target and not self.kill_switch.is_active(kind, target):
                reason = f"{kind.value} `{target}` is killed"
                self.audit.record(
                    request_id=context.request_id,
                    stage="gate.kill_switch",
                    outcome="deny",
                    actor_id=actor_id,
                    payload_summary={"target": target, "kind": kind.value},
                )
                return self._deny(context, trace, reason)

        # 5. trust (only if a draft was produced)
        trust_passed = True
        if draft is not None:
            trust = self.trust.assess(
                context,
                draft.text,
                draft_prices_sar=draft.prices_sar or None,
                urls=draft.urls or None,
            )
            trace.append(trust)
            trust_passed = trust.passed
            self.audit.record(
                request_id=context.request_id,
                stage=trust.stage,
                outcome="pass" if trust.passed else "deny",
                actor_id=actor_id,
                payload_summary={"findings": trust.metadata.get("findings")},
            )
            if not trust.passed:
                return self._deny(context, trace, trust.reason or "trust check failed")

        # 6. approval (HOLD if needed)
        approval_required = sov.approval_required or policy.approval_required or (
            draft is not None and any(g.approval_required for g in trace)
        )
        ticket: ApprovalTicket | None = None
        if approval_required:
            ticket = self.approval.open_ticket(
                context=context,
                intent=intent,
                sovereignty_level=sov.sovereignty_override or SovereigntyLevel.S2_SAMI_APPROVAL,
                summary={
                    "intent": intent,
                    "actor": actor_id,
                    "preview": (draft.text[:300] if draft else None),
                    "reasons": sov.metadata.get("reasons", []),
                },
            )
            self.audit.record(
                request_id=context.request_id,
                stage="gate.approval",
                outcome="hold",
                actor_id=actor_id,
                payload_summary={
                    "ticket_id": ticket.ticket_id,
                    "approver_role": ticket.approver_role,
                    "level": ticket.sovereignty_level.value,
                },
            )

        risk = RiskAssessment(
            risk_level=RiskLevel(sov.metadata.get("risk_level", "low")),
            sovereignty_level=sov.sovereignty_override or SovereigntyLevel.S0_INTERNAL_DRAFT,
            approval_required=approval_required,
            reasons=list(sov.metadata.get("reasons", [])),
            controls_triggered=list(policy.risk_delta) + list(
                trace[-1].risk_delta if draft is not None and not approval_required else []
            ),
        )

        data: dict[str, Any] = {
            "intent": intent,
            "draft": draft.__dict__ if draft else None,
        }
        next_actions: list[dict[str, Any]] = []
        if ticket:
            data["approval_ticket_id"] = ticket.ticket_id
            next_actions.append(
                {
                    "action": "approve_or_reject",
                    "ticket_id": ticket.ticket_id,
                    "approver_role": ticket.approver_role,
                }
            )
        else:
            next_actions.append({"action": "execute_or_log_outcome"})

        events: list[str] = ["hermes.request.accepted"]
        if approval_required:
            events.append("hermes.approval.opened")

        response = HermesResponse.from_risk(
            data=data, risk=risk, next_actions=next_actions, events_emitted=events
        )
        return RuntimeOutcome(
            response=response,
            gate_trace=trace,
            approval_ticket=ticket,
            request_id=context.request_id,
        )

    # ─────────────────────────────────────────────────────────

    def _deny(
        self, context: ContextPacket, trace: list[GateResult], reason: str
    ) -> RuntimeOutcome:
        risk = RiskAssessment(
            risk_level=RiskLevel.HIGH,
            sovereignty_level=SovereigntyLevel.S0_INTERNAL_DRAFT,
            approval_required=False,
            reasons=[reason],
        )
        return RuntimeOutcome(
            response=HermesResponse.denied(reason=reason, risk=risk),
            gate_trace=trace,
            request_id=context.request_id,
        )


__all__ = ["DraftBundle", "HermesRuntime", "RuntimeOutcome"]
