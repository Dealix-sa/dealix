"""
Output guardrails — detect overclaims, pricing surprises, sensitive data,
and external commitments before a draft becomes a message.

Guardrails do not delete content. They flag, escalate, and require Sami's
approval. Approval bypasses are not implemented intentionally.
"""

from __future__ import annotations

from pydantic import BaseModel

FORBIDDEN_CLAIMS: tuple[str, ...] = (
    "نضمن لك",
    "شراكة رسمية مع",
    "بدون أي مخاطر",
    "تشغيل ذاتي كامل بدون تدخل",
    "نتائج مضمونة",
    "guaranteed results",
    "no risk",
    "fully autonomous with no human",
)


class TrustCheckRequest(BaseModel):
    content: str
    action_type: str
    target_audience: str
    contains_pricing: bool = False
    contains_external_commitment: bool = False
    contains_sensitive_data: bool = False


class TrustCheckResult(BaseModel):
    allowed: bool
    risk_level: str  # low | medium | high | critical
    approval_required: bool
    reasons: list[str]
    safe_revision: str | None = None


def trust_check(req: TrustCheckRequest) -> TrustCheckResult:
    reasons: list[str] = []
    risk = "low"
    approval_required = False

    for claim in FORBIDDEN_CLAIMS:
        if claim in req.content:
            reasons.append(f"Potential overclaim detected: {claim}")
            risk = "high"
            approval_required = True

    if req.contains_sensitive_data:
        reasons.append("Sensitive data detected.")
        risk = "critical"
        approval_required = True

    if req.contains_external_commitment:
        reasons.append("External commitment detected.")
        risk = "high" if risk != "critical" else risk
        approval_required = True

    if req.contains_pricing and "enterprise" in req.action_type.lower():
        reasons.append("Enterprise pricing requires approval.")
        risk = "high" if risk not in {"critical"} else risk
        approval_required = True

    return TrustCheckResult(
        allowed=not approval_required,
        risk_level=risk,
        approval_required=approval_required,
        reasons=reasons,
        safe_revision=None,
    )
