"""
Policy Enforcement Gate — يطبّق السياسات وقت التشغيل (policies-as-code) بدل
وثائق نظرية. كل سياسة دالة بسيطة `(context, intent, signals) -> verdict`
تُسجَّل في registry قابل للتوسعة.

أي سياسة ترجع `block=True` يعني الـ runtime يوقف الطلب فورًا قبل ما يصل
الـ trust/agent.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ..contracts import ContextPacket, GateResult


@dataclass
class PolicyVerdict:
    policy_id: str
    block: bool = False
    reasons: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


PolicyFn = Callable[[ContextPacket, str, dict[str, Any]], PolicyVerdict]


class PolicyRegistry:
    def __init__(self) -> None:
        self._policies: dict[str, PolicyFn] = {}

    def register(self, policy_id: str, fn: PolicyFn) -> None:
        if policy_id in self._policies:
            raise ValueError(f"policy `{policy_id}` already registered")
        self._policies[policy_id] = fn

    def all(self) -> list[tuple[str, PolicyFn]]:
        return list(self._policies.items())


# ────────────────────────────────────────────────────────────────
# Default policies (Section 57 — policies_seed equivalent in code).
# ────────────────────────────────────────────────────────────────


def external_action_policy(
    context: ContextPacket, intent: str, signals: dict[str, Any]
) -> PolicyVerdict:
    """No external action without approval ticket attached."""
    if intent.startswith("external."):
        if not signals.get("approval_ticket_id"):
            return PolicyVerdict(
                policy_id="external_action_policy",
                block=False,  # سيُحوَّل لاحقًا في approval_gate
                reasons=["external action requires approval before execute"],
                metadata={"requires_approval": True},
            )
    return PolicyVerdict(policy_id="external_action_policy")


def sensitive_data_policy(
    context: ContextPacket, intent: str, signals: dict[str, Any]
) -> PolicyVerdict:
    if signals.get("touches_regulated_data") and intent.startswith("export."):
        return PolicyVerdict(
            policy_id="sensitive_data_policy",
            block=True,
            reasons=["regulated data export is blocked by default"],
        )
    return PolicyVerdict(policy_id="sensitive_data_policy")


def pricing_policy(
    context: ContextPacket, intent: str, signals: dict[str, Any]
) -> PolicyVerdict:
    if signals.get("involves_pricing"):
        return PolicyVerdict(
            policy_id="pricing_policy",
            block=False,
            reasons=["pricing changes require founder approval"],
            metadata={"requires_approval": True},
        )
    return PolicyVerdict(policy_id="pricing_policy")


def mcp_policy(
    context: ContextPacket, intent: str, signals: dict[str, Any]
) -> PolicyVerdict:
    if signals.get("mcp_server_unreviewed"):
        return PolicyVerdict(
            policy_id="mcp_policy",
            block=True,
            reasons=["unreviewed MCP server cannot be used"],
        )
    return PolicyVerdict(policy_id="mcp_policy")


def partner_claim_policy(
    context: ContextPacket, intent: str, signals: dict[str, Any]
) -> PolicyVerdict:
    if intent.startswith("partner.claim.") and not signals.get("evidence_pack_id"):
        return PolicyVerdict(
            policy_id="partner_claim_policy",
            block=True,
            reasons=["partner-facing claims require an evidence pack id"],
        )
    return PolicyVerdict(policy_id="partner_claim_policy")


def revenue_verification_policy(
    context: ContextPacket, intent: str, signals: dict[str, Any]
) -> PolicyVerdict:
    if intent == "money.revenue.record":
        if not signals.get("payment_received") and not signals.get(
            "signed_agreement"
        ):
            return PolicyVerdict(
                policy_id="revenue_verification_policy",
                block=True,
                reasons=["revenue requires payment_received or signed_agreement"],
            )
    return PolicyVerdict(policy_id="revenue_verification_policy")


def default_registry() -> PolicyRegistry:
    reg = PolicyRegistry()
    reg.register("external_action_policy", external_action_policy)
    reg.register("sensitive_data_policy", sensitive_data_policy)
    reg.register("pricing_policy", pricing_policy)
    reg.register("mcp_policy", mcp_policy)
    reg.register("partner_claim_policy", partner_claim_policy)
    reg.register("revenue_verification_policy", revenue_verification_policy)
    return reg


class PolicyEnforcementGate:
    STAGE = "gate.policy"

    def __init__(self, registry: PolicyRegistry | None = None) -> None:
        self._registry = registry or default_registry()

    def evaluate(
        self,
        context: ContextPacket,
        intent: str,
        signals: dict[str, Any] | None = None,
    ) -> GateResult:
        signals = signals or {}
        triggered: list[str] = []
        reasons: list[str] = []
        requires_approval = False
        for policy_id, fn in self._registry.all():
            verdict = fn(context, intent, signals)
            if verdict.block:
                triggered.append(policy_id)
                return GateResult(
                    stage=self.STAGE,
                    passed=False,
                    risk_delta=triggered,
                    reason="; ".join(verdict.reasons),
                    metadata={"blocked_by": policy_id, "reasons": verdict.reasons},
                )
            if verdict.reasons:
                triggered.append(policy_id)
                reasons.extend(verdict.reasons)
            if verdict.metadata.get("requires_approval"):
                requires_approval = True
        return GateResult(
            stage=self.STAGE,
            passed=True,
            risk_delta=triggered,
            approval_required=requires_approval,
            metadata={"reasons": reasons},
        )


__all__ = [
    "PolicyEnforcementGate",
    "PolicyFn",
    "PolicyRegistry",
    "PolicyVerdict",
    "default_registry",
    "external_action_policy",
    "mcp_policy",
    "partner_claim_policy",
    "pricing_policy",
    "revenue_verification_policy",
    "sensitive_data_policy",
]
