"""Policy-as-code adapter.

Loads policies/dealix_control_policy.yaml and exposes evaluator helpers.
Does NOT execute external actions — only returns allow/block/escalate.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

try:  # Optional dependency: YAML loader.
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover - graceful fallback for thin envs
    yaml = None  # type: ignore[assignment]

POLICY_PATH = Path("policies/dealix_control_policy.yaml")


@dataclass(frozen=True)
class PolicyDecision:
    decision: str  # allow | block | escalate
    rule_id: str | None
    severity: str | None
    reason: str | None


@lru_cache(maxsize=1)
def load_policy(path: str | None = None) -> dict[str, Any]:
    p = Path(path) if path else POLICY_PATH
    if not p.exists() or yaml is None:
        return {"version": 0, "rules": [], "routing": {}, "approval_classes": {}}
    with p.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def evaluate(action: dict[str, Any], path: str | None = None) -> PolicyDecision:
    """Evaluate a proposed action against loaded policy rules.

    Action shape (best effort, fields are optional):
      {
        "action_type": "outreach",
        "action_class": "A2",
        "action_risk": "high",
        "auto_execute": False,
        "target_in_suppression_list": False,
        "evidence_attached": True,
        "content_contains_guarantee_claim": False,
        "approval_recorded": True,
        "named_approver": True,
        ...
      }
    """
    policy = load_policy(path)
    rules = policy.get("rules", [])
    for rule in rules:
        when = rule.get("when", {})
        if not when:
            continue
        if all(action.get(k) == v for k, v in when.items()):
            decision = rule.get("decision", "block")
            return PolicyDecision(
                decision=decision,
                rule_id=rule.get("id"),
                severity=rule.get("severity"),
                reason=rule.get("description"),
            )
    # No matching rule — default to require approval for external impact.
    if action.get("external_action_requested"):
        return PolicyDecision(
            decision="escalate",
            rule_id="default_external_action",
            severity="medium",
            reason="No matching rule; defer to approval queue.",
        )
    return PolicyDecision(
        decision="allow",
        rule_id=None,
        severity=None,
        reason="No matching rule; internal-only action.",
    )
