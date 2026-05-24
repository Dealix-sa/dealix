"""
Section 58 — Policy Engine.

Policies are *named*, *kinded*, and evaluated against a structured action
context. The engine returns `ALLOW`, `ESCALATE` (approval required), or
`DENY`. The rule book is data — production swaps in OPA/Rego without
changing callers.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class PolicyKind(StrEnum):
    SOVEREIGNTY = "sovereignty"
    DATA = "data"
    TOOL = "tool"
    EXTERNAL_ACTION = "external_action"
    PRICING = "pricing"
    PARTNER = "partner"
    CUSTOMER_DATA = "customer_data"
    MCP = "mcp"
    MARKETPLACE = "marketplace"


class PolicyDecision(StrEnum):
    ALLOW = "allow"
    ESCALATE = "escalate"
    DENY = "deny"


@dataclass(frozen=True)
class PolicyResult:
    decision: PolicyDecision
    policy_id: str
    reason: str
    requires_approval_role: str | None = None
    audit_required: bool = True
    outcome_required: bool = False


PolicyMatcher = Callable[[Mapping[str, Any]], bool]
PolicyEvaluator = Callable[[Mapping[str, Any]], PolicyResult | None]


@dataclass
class Policy:
    policy_id: str
    kind: PolicyKind
    description: str
    matches: PolicyMatcher
    evaluate: PolicyEvaluator
    priority: int = 100
    enabled: bool = True


class PolicyEngine:
    def __init__(self) -> None:
        self._policies: list[Policy] = []

    def register(self, policy: Policy) -> Policy:
        self._policies.append(policy)
        self._policies.sort(key=lambda p: p.priority)
        return policy

    def disable(self, policy_id: str) -> None:
        for policy in self._policies:
            if policy.policy_id == policy_id:
                policy.enabled = False

    def policies(self, *, kind: PolicyKind | None = None) -> list[Policy]:
        if kind is None:
            return list(self._policies)
        return [p for p in self._policies if p.kind == kind]

    def evaluate(self, action: Mapping[str, Any]) -> PolicyResult:
        last_allow: PolicyResult | None = None
        for policy in self._policies:
            if not policy.enabled:
                continue
            if not policy.matches(action):
                continue
            result = policy.evaluate(action)
            if result is None:
                continue
            if result.decision is PolicyDecision.DENY:
                return result
            if result.decision is PolicyDecision.ESCALATE:
                return result
            last_allow = result
        if last_allow is not None:
            return last_allow
        return PolicyResult(
            decision=PolicyDecision.ALLOW,
            policy_id="default_allow",
            reason="no matching policy",
            audit_required=True,
        )

    def evaluate_all(self, action: Mapping[str, Any]) -> list[PolicyResult]:
        results: list[PolicyResult] = []
        for policy in self._policies:
            if not policy.enabled:
                continue
            if not policy.matches(action):
                continue
            outcome = policy.evaluate(action)
            if outcome is not None:
                results.append(outcome)
        return results


def standard_policies() -> Iterable[Policy]:
    """The doctrine policies that ship with every Control Plane."""

    yield Policy(
        policy_id="external_action_policy_v1",
        kind=PolicyKind.EXTERNAL_ACTION,
        description="No external action without Sami approval.",
        priority=10,
        matches=lambda a: bool(a.get("external_action")),
        evaluate=lambda a: PolicyResult(
            decision=PolicyDecision.ESCALATE,
            policy_id="external_action_policy_v1",
            reason="external action requires Sami approval",
            requires_approval_role="sami",
            outcome_required=True,
        ),
    )

    yield Policy(
        policy_id="sovereign_data_export_policy_v1",
        kind=PolicyKind.DATA,
        description="SOVEREIGN data export is denied by default.",
        priority=5,
        matches=lambda a: a.get("data_class") == "SOVEREIGN"
        and bool(a.get("export")),
        evaluate=lambda a: PolicyResult(
            decision=PolicyDecision.DENY,
            policy_id="sovereign_data_export_policy_v1",
            reason="SOVEREIGN data must not be exported",
        ),
    )

    yield Policy(
        policy_id="tool_activation_policy_v1",
        kind=PolicyKind.TOOL,
        description="Enabling a tool requires Sami.",
        priority=15,
        matches=lambda a: a.get("action_type") == "enable_tool",
        evaluate=lambda a: PolicyResult(
            decision=PolicyDecision.ESCALATE,
            policy_id="tool_activation_policy_v1",
            reason="tool activation requires Sami approval",
            requires_approval_role="sami",
            outcome_required=True,
        ),
    )

    yield Policy(
        policy_id="pricing_floor_policy_v1",
        kind=PolicyKind.PRICING,
        description="Refuse pricing under the offer floor.",
        priority=20,
        matches=lambda a: a.get("action_type") == "set_price",
        evaluate=lambda a: (
            PolicyResult(
                decision=PolicyDecision.DENY,
                policy_id="pricing_floor_policy_v1",
                reason="price below floor",
            )
            if a.get("offer_floor_sar") is not None
            and a.get("price_sar") is not None
            and float(a["price_sar"]) < float(a["offer_floor_sar"])
            else PolicyResult(
                decision=PolicyDecision.ALLOW,
                policy_id="pricing_floor_policy_v1",
                reason="price at or above floor",
            )
        ),
    )
