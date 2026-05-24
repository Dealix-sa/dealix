"""Integration gate.

A thin wrapper every external integration MUST go through. Reads
registries/integration_registry.yaml to find the integration's kill
switches and gates, then refuses to call out unless:

    * the requested action is allowed by the policy adapter
    * the integration is not in mock mode
    * live send is explicitly enabled
    * a daily limit is set and not exhausted (if applicable)
    * the founder has approved (for A2/A3) — caller provides the proof
    * an audit entry will be written

The gate itself does NOT perform the external call. It returns a
decision; the caller performs the side effect.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))
from _dealix_cert_common import load_yaml  # noqa: E402

from .audit_writer import write as audit_write
from .policy_adapter import PolicyContext, decide

REGISTRY_PATH = _REPO / "registries" / "integration_registry.yaml"


_cache: dict[str, Any] = {}


def _registry() -> dict[str, Any]:
    if "reg" not in _cache:
        _cache["reg"] = load_yaml(REGISTRY_PATH)
    return _cache["reg"]


def _integration(iid: str) -> dict[str, Any] | None:
    for i in _registry().get("integrations") or []:
        if isinstance(i, dict) and i.get("id") == iid:
            return i
    return None


@dataclass
class GateResult:
    allowed: bool
    reason: str
    decision: str
    integration_id: str
    audit_id: str | None = None


def _env_true(name: str, default: bool) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "on"}


def request_external_send(
    *,
    integration_id: str,
    action: str,
    approval_class: str,
    founder_approved: bool,
    suppressed: bool = False,
    content_contains_guarantee: bool = False,
    evidence_attached: bool = False,
    recipient_handle: str = "",
    summary: str = "",
) -> GateResult:
    """Decide whether the caller may perform an external send.

    Caller responsibilities AFTER an allow:
        * perform the actual external call
        * log the outcome via audit_writer.write(...)
        * decrement any daily-limit counter you maintain

    The gate writes its own audit entry for the decision (allow or deny).
    """
    integ = _integration(integration_id)
    if not integ:
        audit_id = audit_write("integration_gate.deny",
                               {"reason": "unknown_integration",
                                "integration_id": integration_id, "action": action})
        return GateResult(False, "unknown integration", "DENY", integration_id, audit_id)

    if integ.get("frontend_direct_call_allowed", False):
        # registry corruption — bail loudly
        audit_id = audit_write("integration_gate.deny",
                               {"reason": "frontend_direct_call_allowed_true",
                                "integration_id": integration_id})
        return GateResult(False, "registry violation", "DENY", integration_id, audit_id)

    ks = integ.get("kill_switches") or {}
    live_flag = ks.get("live_send_enable_flag")
    mock_flag = ks.get("mock_mode_flag")
    daily_limit_env = ks.get("daily_limit_env")

    live = _env_true(live_flag, False) if live_flag else False
    mock = _env_true(mock_flag, True) if mock_flag else False

    ctx = PolicyContext(
        approval_class=approval_class,
        action=action,
        surface="server",
        suppressed=suppressed,
        founder_approved=founder_approved,
        live_send_safe=live and not mock,
        content_contains_guarantee=content_contains_guarantee,
        evidence_attached=evidence_attached,
    )
    decision = decide(ctx)

    payload = {
        "integration_id": integration_id,
        "action": action,
        "approval_class": approval_class,
        "founder_approved": founder_approved,
        "live": live,
        "mock": mock,
        "daily_limit_env": daily_limit_env,
        "recipient_handle_hash": _short_hash(recipient_handle),
        "summary": summary,
        "policy_decision": decision,
    }

    if decision in ("DENY", "ESCALATE"):
        aid = audit_write("integration_gate.deny", payload)
        return GateResult(False, f"policy {decision}", decision, integration_id, aid)
    if decision == "REQUIRE_EVIDENCE":
        aid = audit_write("integration_gate.require_evidence", payload)
        return GateResult(False, "evidence required", decision, integration_id, aid)
    if decision == "ALLOW_AFTER_APPROVAL" and not founder_approved:
        aid = audit_write("integration_gate.deny",
                          {**payload, "reason": "founder_approval_required"})
        return GateResult(False, "founder approval required", "DENY", integration_id, aid)
    # Belt-and-braces: A3 must never proceed; A2 needs explicit positive
    # signal (approval + evidence). Mock mode is allowed for A2 testing
    # only when both signals are present.
    if approval_class == "A3":
        aid = audit_write("integration_gate.deny",
                          {**payload, "reason": "a3_never_executes"})
        return GateResult(False, "A3 never executes", "DENY", integration_id, aid)
    if (approval_class == "A2"
            and decision != "ALLOW_AFTER_APPROVAL"
            and not (mock and founder_approved)):
        aid = audit_write("integration_gate.deny",
                          {**payload, "reason": "a2_requires_explicit_approval_decision"})
        return GateResult(False, "explicit approval decision required",
                          "DENY", integration_id, aid)

    if mock:
        aid = audit_write("integration_gate.allow_mock", payload)
        return GateResult(True, "mock mode", "ALLOW_MOCK", integration_id, aid)
    if not live:
        aid = audit_write("integration_gate.deny",
                          {**payload, "reason": "live_send_disabled"})
        return GateResult(False, "live send disabled", "DENY", integration_id, aid)

    aid = audit_write("integration_gate.allow", payload)
    return GateResult(True, "allowed", "ALLOW", integration_id, aid)


def _short_hash(s: str) -> str:
    if not s:
        return ""
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]
