"""Load policies, agent registry, and eval gate as plain dicts.

We deliberately do not import a heavyweight policy engine here. The
adapter just loads the YAML and exposes safe accessors; runtime checks
are performed by the trust gates that consume these dicts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:  # pragma: no cover — yaml is available in this repo's deps
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
POLICY_PATH = REPO_ROOT / "policies" / "dealix_control_policy.yaml"
AGENTS_PATH = REPO_ROOT / "registries" / "agent_registry.yaml"
EVAL_GATE_PATH = REPO_ROOT / "evals" / "gates" / "dealix_agent_eval_gate.yaml"


def _load_yaml(path: Path) -> dict[str, Any] | None:
    if yaml is None or not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
            return data if isinstance(data, dict) else None
    except Exception:
        return None


def load_policy() -> dict[str, Any] | None:
    return _load_yaml(POLICY_PATH)


def load_agents() -> dict[str, Any] | None:
    return _load_yaml(AGENTS_PATH)


def load_eval_gate() -> dict[str, Any] | None:
    return _load_yaml(EVAL_GATE_PATH)


def evaluate_action(action: dict[str, Any]) -> dict[str, Any]:
    """Lightweight policy evaluator used by approval endpoints.

    Input ``action`` shape::

        {"class": "A2", "type": "outreach", "evidence": "<url>"}

    Returns a verdict dict with allow/block reasons.
    """

    policy = load_policy() or {}
    classes = {c["id"]: c for c in policy.get("approval_classes", []) if isinstance(c, dict)}
    cls_id = str(action.get("class", "A0"))
    cls = classes.get(cls_id, {})
    requires_approval = bool(cls.get("requires_approval", False))
    requires_evidence = bool(cls.get("requires_evidence", False))
    requires_escalation = bool(cls.get("requires_escalation", False))

    reasons: list[str] = []
    if requires_approval and not action.get("approved_by"):
        reasons.append("requires_founder_approval")
    if requires_evidence and not action.get("evidence"):
        reasons.append("requires_evidence")
    if requires_escalation and not action.get("escalated_by"):
        reasons.append("requires_escalation")

    return {
        "class": cls_id,
        "allowed": not reasons,
        "block_reasons": reasons,
        "audit_required": True,
    }
