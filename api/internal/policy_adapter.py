"""Policy-as-code adapter — loads policies/dealix_control_policy.yaml and
exposes a tiny evaluator the internal API uses to refuse unsafe actions
(no_a3_auto, no_suppressed_outreach, pricing_commit_requires_approval,
public_proof_requires_approval, etc).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore


@dataclass
class PolicyDecision:
    allowed: bool
    rule: str | None
    reason: str


def _policy_path() -> Path:
    return Path(os.getenv("DEALIX_POLICY_FILE", "policies/dealix_control_policy.yaml"))


@lru_cache(maxsize=1)
def _load() -> dict[str, Any]:
    p = _policy_path()
    if not p.exists() or yaml is None:
        return {"rules": []}
    with p.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {"rules": []}


def list_rules() -> list[dict[str, Any]]:
    data = _load()
    return list(data.get("rules", []))


def evaluate_action(action: str, context: dict[str, Any] | None = None) -> PolicyDecision:
    """Very simple policy evaluator. Each rule has id, applies_to, deny_when."""
    ctx = context or {}
    for rule in list_rules():
        rid = rule.get("id", "")
        applies = rule.get("applies_to") or []
        if action not in applies and "*" not in applies:
            continue
        deny_when = rule.get("deny_when") or {}
        if all(ctx.get(k) == v for k, v in deny_when.items()) and deny_when:
            return PolicyDecision(allowed=False, rule=rid, reason=rule.get("reason", "denied_by_policy"))
        # Hard rule: explicit external_send must always require approval
        if rid == "no_a3_auto" and action == "external_send" and not ctx.get("approval_class"):
            return PolicyDecision(allowed=False, rule=rid, reason="external_send_requires_approval")
    return PolicyDecision(allowed=True, rule=None, reason="ok")
