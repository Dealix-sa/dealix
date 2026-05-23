"""Policy-as-code adapter.

The Founder Console asks two questions before letting any agent action
move from "drafted" to "queued for execution":

1. **What approval class** does this action fall under?
   (A0 read, A1 internal draft, A2 external impact, A3 high-risk never auto.)

2. **Does any rule reject it?**
   (e.g. ``no_a3_auto``, ``no_suppressed_outreach``.)

This adapter loads ``policies/dealix_control_policy.yaml`` and provides
the ``evaluate(...)`` function used by the internal router. If the YAML
file is missing or unparseable, the adapter falls back to a safe-by-default
posture: every external action is blocked.

PyYAML is optional. If it's not installed, we fall back to a very small
indentation-based parser sufficient for our flat schema.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

POLICY_PATH = Path("policies/dealix_control_policy.yaml")


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    approval_class: str
    matched_rules: list[str]
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "approval_class": self.approval_class,
            "matched_rules": self.matched_rules,
            "reason": self.reason,
        }


def _load_yaml() -> dict[str, Any] | None:
    if not POLICY_PATH.exists():
        return None
    text = POLICY_PATH.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore[import-not-found]

        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else None
    except ImportError:
        return _shallow_yaml(text)
    except Exception:
        return None


def _shallow_yaml(text: str) -> dict[str, Any]:
    """Tiny fallback parser — extracts list-of-id and list-of-name entries.

    Sufficient for ``approval_classes`` and ``rules`` which are flat YAML
    sequences in our policy file.
    """
    classes: list[str] = []
    rules: list[str] = []
    current: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            current = line.rstrip(":").strip()
            continue
        stripped = line.strip()
        if current == "approval_classes" and stripped.startswith("- id:"):
            classes.append(stripped.split(":", 1)[1].strip())
        elif current == "rules" and stripped.startswith("- name:"):
            rules.append(stripped.split(":", 1)[1].strip())
    return {
        "approval_classes": [{"id": c} for c in classes],
        "rules": [{"name": r} for r in rules],
    }


def evaluate(action: str, *, external_impact: bool, suppressed: bool = False) -> PolicyDecision:
    """Evaluate an action against the loaded policy.

    Inputs are kept deliberately small. The router that wants to ship an
    action calls ``evaluate("send_outreach", external_impact=True, ...)``
    and reads ``decision.allowed`` plus ``decision.matched_rules``.
    """
    policy = _load_yaml()
    if not policy:
        return PolicyDecision(
            allowed=False,
            approval_class="A2",
            matched_rules=["fail_closed_no_policy_loaded"],
            reason="policy file missing or unparseable; failing closed",
        )

    rule_names = {r.get("name") for r in policy.get("rules", []) if isinstance(r, dict)}

    approval_class = _approval_class_for(action, external_impact=external_impact)
    matched: list[str] = []

    if approval_class == "A3" and "no_a3_auto" in rule_names:
        matched.append("no_a3_auto")
    if suppressed and "no_suppressed_outreach" in rule_names:
        matched.append("no_suppressed_outreach")
    if external_impact and approval_class == "A2" and "approved_a2_can_request_execution" in rule_names:
        # A2 is allowed but ONLY after recorded approval. The router
        # checks the approval record before invoking us.
        matched.append("approved_a2_can_request_execution")

    blocking = [r for r in matched if r in {"no_a3_auto", "no_suppressed_outreach"}]
    allowed = not blocking

    reason = (
        "blocked by " + ", ".join(blocking)
        if blocking
        else f"permitted under class {approval_class}"
    )
    return PolicyDecision(
        allowed=allowed,
        approval_class=approval_class,
        matched_rules=matched,
        reason=reason,
    )


def _approval_class_for(action: str, *, external_impact: bool) -> str:
    """Map a coarse action label onto an approval class."""
    a3 = {
        "publish_proof",
        "commit_pricing_change",
        "change_contract",
        "change_payment_terms",
        "export_sensitive_data",
        "destructive_repo_operation",
    }
    a2 = {
        "send_outreach",
        "send_proposal",
        "approve_discount",
        "create_invoice",
    }
    if action in a3:
        return "A3"
    if external_impact or action in a2:
        return "A2"
    return "A1"
