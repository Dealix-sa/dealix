"""Permission guard — builds and evaluates client permission requests.

Enforces the L0–L5 rules from ``permission_levels``:
- L2+ requires an explanation in the request.
- L4+ requires an explicit approval step (``requires_explicit_approval``).
- L5 (and any credential-bearing connection) can never be completed inside
  WhatsApp alone — it routes to a secure portal and/or a human.

A credential (API key / secret) is NEVER requested in WhatsApp text; the
request always carries a ``secure_portal_required`` flag and a manual
alternative.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from auto_client_acquisition.whatsapp_client_os import permission_levels as pl
from auto_client_acquisition.whatsapp_client_os.schemas import (
    PermissionGrant,
    PermissionLevel,
    PermissionRequest,
    RiskLevel,
)


@dataclass(frozen=True, slots=True)
class GrantDecision:
    allowed: bool
    requires_secure_portal: bool
    requires_human: bool
    reason_ar: str


def build_permission_request(
    *,
    level: PermissionLevel,
    system: str = "",
    scope: str = "",
    purpose_ar: str = "",
    duration_days: int = 30,
    needs_secret: bool = False,
    risk: RiskLevel | None = None,
) -> PermissionRequest:
    """Construct a governed permission request card payload.

    ``needs_secret=True`` (e.g. an API key would be involved) forces the
    secure-portal route regardless of level — secrets never enter WhatsApp.
    """
    spec = pl.spec(level)
    secure_portal = (
        needs_secret or pl.escalate_needed(level) or pl.level_index(level) >= pl.level_index("L2")
    )
    resolved_risk: RiskLevel = risk or spec.risk
    manual_alt = "أرسل لي خطوات الربط اليدوية، أو امنحنا صلاحية قراءة فقط، أو تجاوز الربط الآن."
    return PermissionRequest(
        permission_id=f"perm_{uuid.uuid4().hex[:10]}",
        level=level,
        system=system,
        scope=scope,
        purpose_ar=purpose_ar or spec.meaning_ar,
        risk=resolved_risk,
        duration_days=int(duration_days),
        secure_portal_required=secure_portal,
        manual_alternative_ar=manual_alt,
    )


def evaluate_grant(
    request: PermissionRequest,
    *,
    granted: bool,
    via_secure_portal: bool = False,
) -> GrantDecision:
    """Decide whether a grant can proceed under the L-rules."""
    if not granted:
        return GrantDecision(
            allowed=False,
            requires_secure_portal=False,
            requires_human=False,
            reason_ar="العميل رفض الصلاحية — نكمل بمسار يدوي بديل.",
        )

    # L5 can never complete in WhatsApp alone.
    if pl.escalate_needed(request.level):
        return GrantDecision(
            allowed=False,
            requires_secure_portal=True,
            requires_human=True,
            reason_ar="هذه عملية حسّاسة (L5) — لا تتم عبر واتساب وحده؛ نحوّلها لمسار آمن ومراجعة بشرية.",
        )

    # Secrets / L2+ must go through the secure portal.
    if request.secure_portal_required and not via_secure_portal:
        return GrantDecision(
            allowed=False,
            requires_secure_portal=True,
            requires_human=False,
            reason_ar="لا ترسل المفتاح هنا — أكمل الربط عبر الرابط الآمن.",
        )

    return GrantDecision(
        allowed=True,
        requires_secure_portal=request.secure_portal_required,
        requires_human=False,
        reason_ar="تم اعتماد الصلاحية ضمن الحدود المطلوبة.",
    )


def record_grant(
    request: PermissionRequest,
    *,
    client_handle: str,
    granted: bool,
    via_secure_portal: bool = False,
    note: str = "",
) -> PermissionGrant:
    """Build the audit row for a grant/deny decision."""
    return PermissionGrant(
        permission_id=request.permission_id,
        client_handle=client_handle,
        level=request.level,
        granted=granted,
        via_secure_portal=via_secure_portal,
        note=note,
    )


__all__ = [
    "GrantDecision",
    "build_permission_request",
    "evaluate_grant",
    "record_grant",
]
