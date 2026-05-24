"""Policy-as-code adapter.

Loads policies/dealix_control_policy.yaml and exposes a single
``decide(context)`` function that returns one of:
    ALLOW | ALLOW_AFTER_APPROVAL | REQUIRE_EVIDENCE | ESCALATE | DENY

The adapter is intentionally tiny: it is a guardrail, not a planner.
Every external-impacting action MUST call this before doing anything.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Reuse the policy parser in scripts/_dealix_cert_common.py to keep one source of truth.
_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))
from _dealix_cert_common import load_yaml  # noqa: E402

POLICY_PATH = _REPO / "policies" / "dealix_control_policy.yaml"

Decision = str  # one of: ALLOW | ALLOW_AFTER_APPROVAL | REQUIRE_EVIDENCE | ESCALATE | DENY


@dataclass
class PolicyContext:
    """All facts the policy may consult. Anything not provided is treated as false."""
    approval_class: str = "A0"
    action: str = ""
    surface: str = "server"        # server | frontend | cron
    route_prefix: str = ""
    app_env: str = field(default_factory=lambda: os.environ.get("APP_ENV", "development"))
    suppressed: bool = False
    founder_approved: bool = False
    founder_escalation: bool = False
    evidence_attached: bool = False
    live_send_safe: bool = False
    embeds_secret: bool = False
    calls_external_send: bool = False
    content_contains_guarantee: bool = False
    token_present: bool = True     # for internal API calls

    def as_dict(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in self.__annotations__}


_cache: dict[str, Any] = {}


def _policy() -> dict[str, Any]:
    if "policy" not in _cache:
        _cache["policy"] = load_yaml(POLICY_PATH)
    return _cache["policy"]


def reload_policy() -> None:
    _cache.clear()


def _matches(rule_when: dict[str, Any], ctx: dict[str, Any]) -> bool:
    """A rule fires when every `when` key matches the context exactly."""
    if not isinstance(rule_when, dict):
        return False
    for k, v in rule_when.items():
        if ctx.get(k) != v:
            return False
    return True


def decide(context: PolicyContext) -> Decision:
    rules = _policy().get("rules") or []
    ctx = context.as_dict()
    final: Decision = "ALLOW"  # default-allow only matters if no rule fires
    # Precedence: DENY > ESCALATE > REQUIRE_EVIDENCE > ALLOW_AFTER_APPROVAL > ALLOW
    rank = {"DENY": 4, "ESCALATE": 3, "REQUIRE_EVIDENCE": 2,
            "ALLOW_AFTER_APPROVAL": 1, "ALLOW": 0}
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        if _matches(rule.get("when") or {}, ctx):
            r = rule.get("result", "ALLOW")
            if rank.get(r, 0) > rank.get(final, 0):
                final = r
    # Safe default for external-impacting actions that no rule allowed:
    if context.surface == "frontend" and context.calls_external_send:
        return "DENY"
    return final
