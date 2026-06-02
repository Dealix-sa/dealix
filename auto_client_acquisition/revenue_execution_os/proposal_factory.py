"""Proposal factory — governance-gated proposal drafts on the offer ladder.

Reuses ``sales_os.build_proposal_skeleton`` for the non-negotiable
statements (no-sales-guarantee + governance boundaries) and the canonical
offer ladder for pricing. Every proposal is born ``pending_approval`` and
carries a ``governance_decision``.
"""

from __future__ import annotations

from collections.abc import Sequence
from uuid import uuid4

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os import policy_check_draft
from auto_client_acquisition.revenue_execution_os import stores
from auto_client_acquisition.revenue_execution_os.models import (
    Proposal,
    ProposalStatus,
    Prospect,
    now_iso,
)
from auto_client_acquisition.revenue_execution_os.offers import Offer, offer_by_key, price_label
from auto_client_acquisition.sales_os.proposal_generator import build_proposal_skeleton

_TIMELINE_AR: dict[str, str] = {
    "free_diagnostic": "خلال أيام",
    "revenue_sprint": "٧ أيام",
    "data_revenue_pack": "أسبوع إلى أسبوعين",
    "managed_revenue_ops": "شهري متجدد",
    "custom_ai_setup": "٣–٦ أسابيع إعداد + تشغيل شهري",
    "ai_governance_review": "٤–٨ أسابيع (مسار بطيء)",
}


def _default_scope(offer: Offer) -> list[str]:
    return [
        f"تنفيذ {offer.name_ar} وفق نطاق متفق عليه.",
        "مراجعة الوضع الحالي وتحديد نقاط التسرّب.",
        "خطوة سريعة واحدة (Quick Win) قابلة للقياس.",
        "تقرير قيمة وخطوات تالية واضحة.",
    ]


def build_proposal(
    prospect: Prospect,
    offer_key: str,
    *,
    problem: str = "",
    solution: str = "",
    scope: Sequence[str] | None = None,
    evidence_level: int = 1,
) -> Proposal:
    """Build a proposal draft for a prospect on a given offer (pure)."""
    offer = offer_by_key(offer_key)
    skeleton = build_proposal_skeleton(
        client_label=prospect.company or prospect.prospect_id or "—",
        sprint_name=offer.name_en,
    )
    problem = problem or skeleton["problem"]
    solution = solution or (
        f"{offer.name_ar}: قدرة إيراد محوكمة مع إثبات جاهزية وأولويات وخطوات تالية. "
        f"{skeleton['no_sales_guarantee_statement']}"
    )
    scope_list = list(scope) if scope is not None else _default_scope(offer)
    out_of_scope = [
        skeleton["governance_boundaries"],
        "لا إرسال خارجي تلقائي — كل تواصل مسودة بانتظار موافقتكم.",
    ]
    assumptions = [
        "توفّر وصول للبيانات اللازمة لتأكيد التقديرات.",
        "الأرقام تقديرية حتى التحقق منها ببياناتكم.",
    ]
    risks = [
        "نقص البيانات قد يؤخر القياس.",
        "النتائج تعتمد على التنفيذ المشترك ولا تُضمن.",
    ]
    # Only the persuasive claim surface is gated. out_of_scope / risks are
    # governance meta-text that intentionally names forbidden terms to negate
    # them (e.g. "No guaranteed sales claims"); a substring gate would
    # false-positive on those.
    blob = "\n".join([problem, solution, *scope_list])
    pc = policy_check_draft(blob)
    decision = GovernanceDecision.BLOCK if not pc.allowed else GovernanceDecision.REQUIRE_APPROVAL
    return Proposal(
        proposal_id=f"prop_{uuid4().hex[:18]}",
        prospect_id=prospect.prospect_id,
        sector=prospect.sector,
        offer_key=offer.key,
        problem=problem,
        solution=solution,
        scope=scope_list,
        out_of_scope=out_of_scope,
        timeline=_TIMELINE_AR.get(offer.key, ""),
        price_label=price_label(offer, "ar"),
        evidence_level=int(evidence_level),
        assumptions=assumptions,
        risks=risks,
        next_step="مكالمة قصيرة لتأكيد النطاق والبدء.",
        status=ProposalStatus.PENDING_APPROVAL,
        governance_decision=str(decision),
        created_at=now_iso(),
    )


def generate_proposal(
    prospect: Prospect,
    offer_key: str,
    *,
    problem: str = "",
    solution: str = "",
    scope: Sequence[str] | None = None,
    evidence_level: int = 1,
) -> Proposal:
    """Build + persist a proposal draft."""
    proposal = build_proposal(
        prospect,
        offer_key,
        problem=problem,
        solution=solution,
        scope=scope,
        evidence_level=evidence_level,
    )
    return stores.PROPOSALS.add(proposal)


__all__ = ["build_proposal", "generate_proposal"]
