"""Policy-as-Code adapter.

Loads policies/dealix_control_policy.yaml when present and falls back to
safe built-in rules. Used by the internal API to decide whether a proposed
action may produce an externally visible side effect.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

POLICY_PATH = Path(__file__).resolve().parents[2] / "policies" / "dealix_control_policy.yaml"

BANNED_PHRASES_FALLBACK = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed meetings",
    "guaranteed replies",
    "guaranteed conversions",
    "fully compliant",
    "no-risk",
    "zero risk",
    "sent automatically without approval",
]


@dataclass
class PolicyResult:
    decision: str  # allow | deny
    external_action_allowed: bool
    reason: str
    rule_id: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "external_action_allowed": self.external_action_allowed,
            "reason": self.reason,
            "rule_id": self.rule_id,
        }


def _load_yaml() -> dict[str, Any] | None:
    if not POLICY_PATH.exists():
        return None
    try:
        import yaml  # type: ignore
    except ImportError:
        return None
    try:
        with POLICY_PATH.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except OSError:
        return None


@lru_cache(maxsize=1)
def load_policy() -> dict[str, Any]:
    data = _load_yaml()
    if data is None:
        return {
            "version": 0,
            "source": "fallback",
            "approval_classes": ["A0", "A1", "A2", "A3"],
            "rules": [],
        }
    data["source"] = "runtime"
    return data


def _banned_phrases() -> list[str]:
    policy = load_policy()
    for rule in policy.get("rules", []) or []:
        if rule.get("id") == "no_guaranteed_revenue_claims":
            phrases = rule.get("banned_phrases")
            if phrases:
                return [p.lower() for p in phrases]
    return [p.lower() for p in BANNED_PHRASES_FALLBACK]


def evaluate(
    *,
    approval_class: str,
    action_type: str = "",
    risk_level: str = "low",
    evidence_present: bool = False,
    recipient_suppressed: bool = False,
    actor_type: str = "agent",
    decision_state: str = "pending",
    output_text: str = "",
) -> PolicyResult:
    """Evaluate a proposed action against the policy.

    Returns a PolicyResult with decision (allow|deny), whether external
    action may proceed, and the matched rule id + reason.
    """

    approval_class = (approval_class or "").upper().strip() or "A1"
    risk_level = (risk_level or "low").lower().strip()

    if approval_class == "A3" and actor_type == "agent":
        return PolicyResult(
            decision="deny",
            external_action_allowed=False,
            reason="A3 actions are founder-only and may not be agent-initiated.",
            rule_id="no_a3_auto",
        )

    if action_type == "outreach" and recipient_suppressed:
        return PolicyResult(
            decision="deny",
            external_action_allowed=False,
            reason="Recipient is on the suppression list.",
            rule_id="no_suppressed_outreach",
        )

    if risk_level in {"high", "critical"} and not evidence_present:
        return PolicyResult(
            decision="deny",
            external_action_allowed=False,
            reason="Evidence is required for high or critical risk actions.",
            rule_id="high_risk_requires_evidence",
        )

    lowered = (output_text or "").lower()
    for phrase in _banned_phrases():
        if phrase in lowered:
            return PolicyResult(
                decision="deny",
                external_action_allowed=False,
                reason=f"Output contains banned phrasing: {phrase!r}.",
                rule_id="no_guaranteed_revenue_claims",
            )

    if approval_class == "A2" and decision_state == "approved" and not recipient_suppressed:
        return PolicyResult(
            decision="allow",
            external_action_allowed=True,
            reason="Approved A2 action with valid evidence and recipient.",
            rule_id="approved_a2_can_request_execution",
        )

    if approval_class in {"A0", "A1"}:
        return PolicyResult(
            decision="allow",
            external_action_allowed=(approval_class == "A0"),
            reason=f"{approval_class} action permitted without external side effect.",
            rule_id=f"default_{approval_class.lower()}",
        )

    return PolicyResult(
        decision="deny",
        external_action_allowed=False,
        reason="No matching policy rule; default deny.",
        rule_id="default_deny",
    )


def summary() -> dict[str, Any]:
    policy = load_policy()
    classes = policy.get("approval_classes")
    if isinstance(classes, dict):
        class_ids = sorted(classes.keys())
    elif isinstance(classes, list):
        class_ids = list(classes)
    else:
        class_ids = []
    rules = policy.get("rules") or []
    rule_ids = [r.get("id") for r in rules if isinstance(r, dict) and r.get("id")]
    return {
        "version": policy.get("version", 0),
        "approval_classes": class_ids,
        "rules": rule_ids,
        "source": policy.get("source", "fallback"),
    }
