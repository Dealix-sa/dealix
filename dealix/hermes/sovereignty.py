"""
Sovereignty classifier — يصنّف كل فعل إلى S0..S5.

القاعدة المركزية: لا أحد يستدعي `approval_gate` مباشرة. الـ runtime يستدعي
`classify()` ثم يقرر هل يفتح approval ticket أم لا. هذا يضمن:

    - تصنيف موحّد لكل المسارات.
    - منع تجاوز الحوكمة عن طريق وكيل ذكي.
    - قابلية تتبّع كاملة (كل تصنيف معه `reasons`).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .contracts import (
    ActorKind,
    ContextPacket,
    DataSensitivity,
    OutputKind,
    RiskAssessment,
    RiskLevel,
    SovereigntyLevel,
)


# الأفعال التي تستدعي مراجعة المؤسس مباشرة بصرف النظر عن أي شيء آخر.
FOUNDER_ONLY_ACTIONS: frozenset[str] = frozenset(
    {
        "external.send.email",
        "external.send.whatsapp",
        "external.send.linkedin",
        "external.publish.content",
        "external.proposal.send",
        "external.partner.commit",
        "external.contract.sign",
        "external.invoice.issue",
        "external.refund.issue",
        "pricing.enterprise.commit",
        "mcp.server.enable",
        "agent.tool.permission.grant",
    }
)

LEGAL_ONLY_ACTIONS: frozenset[str] = frozenset(
    {
        "external.contract.sign",
        "legal.commitment.bind",
        "regulated.data.share",
    }
)

BOARD_ONLY_ACTIONS: frozenset[str] = frozenset(
    {
        "company.acquisition.commit",
        "venture.spinout.commit",
        "equity.grant.issue",
    }
)

BLOCKED_ACTIONS: frozenset[str] = frozenset(
    {
        "external.send.bulk.unverified",
        "scraping.public.directories",
        "credential.exfiltrate",
        "model.train.on.customer.regulated.data",
    }
)


@dataclass
class SovereigntyDecision:
    sovereignty_level: SovereigntyLevel
    risk_level: RiskLevel
    approval_required: bool
    reasons: list[str]


def _is_external_output(kind: OutputKind, intent: str) -> bool:
    if kind in {OutputKind.ACTION, OutputKind.MESSAGE}:
        return True
    if intent.startswith("external."):
        return True
    return False


def classify(
    *,
    context: ContextPacket,
    intent: str | None = None,
    extra_signals: dict[str, Any] | None = None,
) -> SovereigntyDecision:
    """
    Map a request to (sovereignty, risk, approval).

    `extra_signals` يقبل مفاتيح اختيارية:
        - bulk_count: int
        - touches_regulated_data: bool
        - involves_pricing: bool
        - involves_legal_commitment: bool
        - mcp_server_unreviewed: bool
    """
    sig = extra_signals or {}
    intent = (intent or context.intent or "").strip()
    reasons: list[str] = []

    # 1. أفعال محظورة مطلقًا.
    if intent in BLOCKED_ACTIONS:
        return SovereigntyDecision(
            sovereignty_level=SovereigntyLevel.S5_BLOCKED,
            risk_level=RiskLevel.CRITICAL,
            approval_required=False,
            reasons=[f"intent `{intent}` is hard-blocked"],
        )

    # 2. أفعال board-only.
    if intent in BOARD_ONLY_ACTIONS:
        reasons.append("intent requires board approval")
        return SovereigntyDecision(
            sovereignty_level=SovereigntyLevel.S4_BOARD_APPROVAL,
            risk_level=RiskLevel.CRITICAL,
            approval_required=True,
            reasons=reasons,
        )

    # 3. أفعال legal-only.
    if intent in LEGAL_ONLY_ACTIONS or sig.get("involves_legal_commitment"):
        reasons.append("legal commitment in scope")
        return SovereigntyDecision(
            sovereignty_level=SovereigntyLevel.S3_LEGAL_APPROVAL,
            risk_level=RiskLevel.HIGH,
            approval_required=True,
            reasons=reasons,
        )

    # 4. أفعال founder-only (S2).
    if intent in FOUNDER_ONLY_ACTIONS:
        reasons.append(f"intent `{intent}` requires founder approval")
        return SovereigntyDecision(
            sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
            risk_level=RiskLevel.HIGH,
            approval_required=True,
            reasons=reasons,
        )

    # 5. إشارات إضافية ترفع المستوى إلى S2.
    if sig.get("involves_pricing"):
        reasons.append("pricing decision in scope")
        return SovereigntyDecision(
            sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
            risk_level=RiskLevel.HIGH,
            approval_required=True,
            reasons=reasons,
        )

    if sig.get("mcp_server_unreviewed"):
        reasons.append("unreviewed MCP server")
        return SovereigntyDecision(
            sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
            risk_level=RiskLevel.HIGH,
            approval_required=True,
            reasons=reasons,
        )

    if context.data_sensitivity == DataSensitivity.REGULATED or sig.get(
        "touches_regulated_data"
    ):
        reasons.append("regulated data in scope")
        return SovereigntyDecision(
            sovereignty_level=SovereigntyLevel.S3_LEGAL_APPROVAL,
            risk_level=RiskLevel.HIGH,
            approval_required=True,
            reasons=reasons,
        )

    bulk_count = int(sig.get("bulk_count") or 0)
    if bulk_count >= 50 and _is_external_output(
        context.declared_output_kind, intent
    ):
        reasons.append(f"bulk external action ({bulk_count} recipients)")
        return SovereigntyDecision(
            sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
            risk_level=RiskLevel.HIGH,
            approval_required=True,
            reasons=reasons,
        )

    # 6. مخرجات خارجية بأي شكل → موافقة بشرية (default-deny).
    if _is_external_output(context.declared_output_kind, intent):
        reasons.append("output crosses external boundary")
        return SovereigntyDecision(
            sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
            risk_level=RiskLevel.MEDIUM,
            approval_required=True,
            reasons=reasons,
        )

    # 7. أفعال داخلية يمكن أتمتتها لو الجهة موثوقة.
    if context.actor and context.actor.kind in {
        ActorKind.FOUNDER,
        ActorKind.INTERNAL_USER,
        ActorKind.SYSTEM,
        ActorKind.AGENT,
    }:
        reasons.append("internal automated action")
        return SovereigntyDecision(
            sovereignty_level=SovereigntyLevel.S1_INTERNAL_AUTO,
            risk_level=RiskLevel.LOW,
            approval_required=False,
            reasons=reasons,
        )

    # 8. الافتراضي: مسودة داخلية فقط.
    reasons.append("default internal draft mode")
    return SovereigntyDecision(
        sovereignty_level=SovereigntyLevel.S0_INTERNAL_DRAFT,
        risk_level=RiskLevel.LOW,
        approval_required=False,
        reasons=reasons,
    )


def to_risk(decision: SovereigntyDecision) -> RiskAssessment:
    return RiskAssessment(
        risk_level=decision.risk_level,
        sovereignty_level=decision.sovereignty_level,
        approval_required=decision.approval_required,
        reasons=list(decision.reasons),
    )


__all__ = [
    "BLOCKED_ACTIONS",
    "BOARD_ONLY_ACTIONS",
    "FOUNDER_ONLY_ACTIONS",
    "LEGAL_ONLY_ACTIONS",
    "SovereigntyDecision",
    "classify",
    "to_risk",
]
