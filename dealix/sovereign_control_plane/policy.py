"""
Declarative policy engine — §87.

This sits on top of the kernel's PolicyEvaluator. It evaluates plain
event dicts against a registry of when→then policies and returns the
union of outcomes (approval, audit, outcome, block).
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Policy:
    policy_id: str
    name: str
    when: dict[str, Any]
    then: dict[str, Any]
    priority: int = 0
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "when": dict(self.when),
            "then": dict(self.then),
            "priority": self.priority,
            "enabled": self.enabled,
        }


@dataclass
class PolicyOutcome:
    policy_id: str
    name: str
    requires_approval: bool = False
    approval_role: str | None = None
    audit_required: bool = False
    outcome_required: bool = False
    block: bool = False
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "requires_approval": self.requires_approval,
            "approval_role": self.approval_role,
            "audit_required": self.audit_required,
            "outcome_required": self.outcome_required,
            "block": self.block,
            "details": dict(self.details),
        }


def _new_id() -> str:
    return f"pol_{uuid.uuid4().hex[:12]}"


def _seed_policies() -> list[Policy]:
    return [
        Policy(
            policy_id="sovereignty_policy_v1",
            name="Sovereignty",
            when={"workspace_kind": "SOVEREIGN"},
            then={"requires_approval": True, "approval_role": "sami",
                  "audit_required": True, "outcome_required": True},
            priority=100,
        ),
        Policy(
            policy_id="data_policy_v1",
            name="Data",
            when={"sensitivity": ["RESTRICTED", "SOVEREIGN"], "external_exit": True},
            then={"block": True, "audit_required": True},
            priority=95,
        ),
        Policy(
            policy_id="tool_policy_v1",
            name="Tool",
            when={"tool_risk": ["high", "critical"]},
            then={"requires_approval": True, "approval_role": "sami",
                  "audit_required": True},
            priority=80,
        ),
        Policy(
            policy_id="external_action_policy_v1",
            name="External Action",
            when={"action_type": "external"},
            then={"requires_approval": True, "approval_role": "sami",
                  "audit_required": True, "outcome_required": True},
            priority=90,
        ),
        Policy(
            policy_id="pricing_policy_v1",
            name="Pricing",
            when={"action_type": "pricing"},
            then={"requires_approval": True, "approval_role": "sami",
                  "audit_required": True},
            priority=85,
        ),
        Policy(
            policy_id="partner_policy_v1",
            name="Partner",
            when={"actor_kind": "PARTNER_ADMIN"},
            then={"requires_approval": True, "approval_role": "sami",
                  "audit_required": True},
            priority=70,
        ),
        Policy(
            policy_id="customer_data_policy_v1",
            name="CustomerData",
            when={"data_subject": "customer", "external_exit": True},
            then={"requires_approval": True, "approval_role": "compliance",
                  "audit_required": True},
            priority=75,
        ),
        Policy(
            policy_id="mcp_policy_v1",
            name="MCP",
            when={"channel": "mcp"},
            then={"requires_approval": True, "approval_role": "sami",
                  "audit_required": True},
            priority=80,
        ),
        Policy(
            policy_id="marketplace_policy_v1",
            name="Marketplace",
            when={"workspace_kind": "MARKETPLACE"},
            then={"requires_approval": True, "approval_role": "sami",
                  "audit_required": True},
            priority=65,
        ),
        Policy(
            policy_id="api_policy_v1",
            name="API",
            when={"workspace_kind": "API"},
            then={"audit_required": True, "outcome_required": True},
            priority=50,
        ),
    ]


class PolicyEngine:
    def __init__(self) -> None:
        self._policies: dict[str, Policy] = {}
        self._lock = threading.Lock()
        for p in _seed_policies():
            self._policies[p.policy_id] = p

    def register(self, policy: Policy) -> Policy:
        with self._lock:
            if not policy.policy_id:
                policy.policy_id = _new_id()
            self._policies[policy.policy_id] = policy
            return policy

    def list_policies(self) -> list[Policy]:
        return sorted(self._policies.values(), key=lambda p: -p.priority)

    def disable(self, policy_id: str) -> bool:
        with self._lock:
            p = self._policies.get(policy_id)
            if p is None:
                return False
            p.enabled = False
            return True

    def evaluate(self, event: dict[str, Any]) -> list[PolicyOutcome]:
        outcomes: list[PolicyOutcome] = []
        for p in self.list_policies():
            if not p.enabled:
                continue
            if not self._match(p.when, event):
                continue
            outcomes.append(
                PolicyOutcome(
                    policy_id=p.policy_id,
                    name=p.name,
                    requires_approval=bool(p.then.get("requires_approval", False)),
                    approval_role=p.then.get("approval_role"),
                    audit_required=bool(p.then.get("audit_required", False)),
                    outcome_required=bool(p.then.get("outcome_required", False)),
                    block=bool(p.then.get("block", False)),
                    details={"matched_when": dict(p.when)},
                )
            )
        return outcomes

    @staticmethod
    def _match(when: dict[str, Any], event: dict[str, Any]) -> bool:
        for key, expected in when.items():
            actual = event.get(key)
            if isinstance(expected, list):
                if actual not in expected:
                    return False
            else:
                if actual != expected:
                    return False
        return True
