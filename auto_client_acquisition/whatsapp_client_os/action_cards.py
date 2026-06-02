"""WhatsApp Client OS — Action Cards.

Important things appear as structured cards, not long free text. Each card
carries bilingual title/body, a small set of explicit options, an evidence
level, a risk band, and a ``governance_decision`` derived from the outbound
policy guard. No card performs a live external send or a live charge.
"""

from __future__ import annotations

from auto_client_acquisition.governance_os import GovernanceDecision
from auto_client_acquisition.service_catalog import get_offering
from auto_client_acquisition.whatsapp_client_os.policy_guard import guard_outbound
from auto_client_acquisition.whatsapp_client_os.recommendation import OfferRecommendation
from auto_client_acquisition.whatsapp_client_os.schemas import (
    ActionCard,
    ActionCardKind,
    ClientAssessment,
    EvidenceLevel,
)


def _opt(option_id: str, label_ar: str, label_en: str) -> dict[str, str]:
    return {"id": option_id, "label_ar": label_ar, "label_en": label_en}


def _decision_for(*texts: str) -> str:
    """ALLOW unless any rendered text trips the outbound guard."""
    blob = "\n".join(t for t in texts if t)
    return guard_outbound(blob).governance_decision


def recommendation_card(session_id: str, assessment: ClientAssessment) -> ActionCard:
    body_ar = (
        f"جاهزية الإيرادات: {assessment.revenue_readiness}/100\n"
        f"نضج المتابعة: {assessment.follow_up_maturity}/100\n"
        f"المخاطر: {assessment.risk}\n"
        f"السبب: {assessment.recommendation_reason_ar}"
    )
    body_en = (
        f"Revenue readiness: {assessment.revenue_readiness}/100\n"
        f"Follow-up maturity: {assessment.follow_up_maturity}/100\n"
        f"Risk: {assessment.risk}\n"
        f"Why: {assessment.recommendation_reason_en}"
    )
    return ActionCard(
        session_id=session_id,
        kind=ActionCardKind.RECOMMENDATION.value,
        title_ar="التوصية: أفضل بداية لك",
        title_en="Recommendation: your best start",
        body_ar=body_ar,
        body_en=body_en,
        options=(
            _opt("start", "ابدأ", "Start"),
            _opt("send_proposal", "أرسل العرض", "Send proposal"),
            _opt("book_call", "احجز مكالمة", "Book a call"),
            _opt("explain", "اشرح أكثر", "Explain more"),
        ),
        evidence_level=assessment.evidence_level,
        risk=assessment.risk,
        governance_decision=GovernanceDecision.ALLOW.value,
    )


def approval_card(
    session_id: str,
    *,
    draft_text_ar: str,
    evidence_level: str = EvidenceLevel.L1.value,
    channel: str = "email",
) -> ActionCard:
    """Review card for a generated draft. Never sends; approval is manual.

    If the draft trips the outbound guard, the card is marked BLOCK and the
    approve option is withheld.
    """
    guard = guard_outbound(draft_text_ar)
    body_ar = (
        f'مسودة جاهزة للمراجعة (قناة: {channel}):\n"{draft_text_ar}"\n'
        f"التقييم — Evidence: {evidence_level} · Risk: low · إرسال آلي: لا"
    )
    body_en = (
        f"Draft ready for review (channel: {channel}).\n"
        f"Evidence: {evidence_level} · Risk: low · Auto-send: no"
    )
    if guard.allowed:
        options = (
            _opt("approve", "اعتماد (إرسال يدوي)", "Approve (manual send)"),
            _opt("edit", "تعديل", "Edit"),
            _opt("reject", "رفض", "Reject"),
            _opt("shorten", "اختصرها", "Shorten"),
            _opt("formal", "اجعلها رسمية أكثر", "More formal"),
        )
        decision = GovernanceDecision.REQUIRE_APPROVAL.value
        risk = "low"
    else:
        options = (
            _opt("edit", "تعديل", "Edit"),
            _opt("reject", "رفض", "Reject"),
        )
        decision = guard.governance_decision
        risk = "high"
    return ActionCard(
        session_id=session_id,
        kind=ActionCardKind.APPROVAL.value,
        title_ar="مراجعة مسودة",
        title_en="Draft review",
        body_ar=body_ar,
        body_en=body_en,
        options=options,
        evidence_level=evidence_level,
        risk=risk,
        governance_decision=decision,
    )


def permission_card(session_id: str, *, integration: str = "") -> ActionCard:
    """Route any integration to the Secure Portal. Never asks for a key here."""
    label = integration or "النظام الخارجي"
    body_ar = (
        f"نحتاج ربط {label}.\n"
        "لأمانك، لا ترسل أي مفتاح هنا. اختر الطريقة المناسبة عبر البوابة الآمنة."
    )
    body_en = (
        f"We need to connect {integration or 'the external system'}.\n"
        "For your safety, never send a key here. Choose a method via the secure portal."
    )
    return ActionCard(
        session_id=session_id,
        kind=ActionCardKind.PERMISSION.value,
        title_ar="ربط آمن للصلاحيات",
        title_en="Secure permission setup",
        body_ar=body_ar,
        body_en=body_en,
        options=(
            _opt("open_portal", "فتح رابط آمن لإدخال المفتاح", "Open secure link"),
            _opt("manual_steps", "أرسل لي خطوات يدوية", "Send manual steps"),
            _opt("csv", "استخدم ملف CSV بدل الربط", "Use CSV instead"),
            _opt("skip", "تجاوز الآن", "Skip for now"),
        ),
        evidence_level=EvidenceLevel.L0.value,
        risk="medium",
        governance_decision=GovernanceDecision.REQUIRE_APPROVAL.value,
    )


def proposal_card(session_id: str, *, offer_id: str) -> ActionCard:
    offering = get_offering(offer_id)
    if offering is None:
        body_ar = "العرض غير متوفر حاليًا. نحوّلك لأحد الفريق."
        body_en = "Offer not available. Routing you to the team."
        return ActionCard(
            session_id=session_id,
            kind=ActionCardKind.PROPOSAL.value,
            title_ar="عرض",
            title_en="Proposal",
            body_ar=body_ar,
            body_en=body_en,
            options=(_opt("book_call", "احجز مكالمة", "Book a call"),),
            evidence_level=EvidenceLevel.L0.value,
            risk="medium",
            governance_decision=GovernanceDecision.REQUIRE_APPROVAL.value,
        )
    price = "مجاني" if offering.price_sar == 0 else f"{offering.price_sar:.0f} ر.س (تقديري)"
    body_ar = (
        f"{offering.name_ar}\n"
        f"المدة: {offering.duration_days} يوم · السعر: {price}\n"
        f"الالتزام: {offering.kpi_commitment_ar}\n"
        f"الاسترجاع: {offering.refund_policy_ar}"
    )
    body_en = (
        f"{offering.name_en}\n"
        f"Duration: {offering.duration_days}d · Price: "
        f"{'Free' if offering.price_sar == 0 else f'{offering.price_sar:.0f} SAR (estimate)'}\n"
        f"Commitment: {offering.kpi_commitment_en}"
    )
    return ActionCard(
        session_id=session_id,
        kind=ActionCardKind.PROPOSAL.value,
        title_ar=f"عرض: {offering.name_ar}",
        title_en=f"Proposal: {offering.name_en}",
        body_ar=body_ar,
        body_en=body_en,
        options=(
            _opt("start", "ابدأ", "Start"),
            _opt("book_call", "احجز مكالمة", "Book a call"),
            _opt("adjust_scope", "عدّل النطاق", "Adjust scope"),
            _opt("explain", "اشرح أكثر", "Explain more"),
        ),
        evidence_level=EvidenceLevel.L2.value,
        risk="low",
        governance_decision=_decision_for(body_ar, body_en),
    )


def proof_pack_card(
    session_id: str, *, summary_ar: str, evidence_level: str = EvidenceLevel.L3.value
) -> ActionCard:
    body_ar = f"{summary_ar}\nالقيمة التقديرية ليست قيمة مُتحقَّقة."
    body_en = "Proof pack ready. Estimated value is not verified value."
    return ActionCard(
        session_id=session_id,
        kind=ActionCardKind.PROOF_PACK.value,
        title_ar="حزمة الإثبات",
        title_en="Proof pack",
        body_ar=body_ar,
        body_en=body_en,
        options=(
            _opt("open_portal", "افتح في البوابة", "Open in portal"),
            _opt("book_call", "ناقشها بمكالمة", "Discuss on a call"),
        ),
        evidence_level=evidence_level,
        risk="low",
        governance_decision=_decision_for(body_ar, body_en),
    )


def payment_handoff_card(session_id: str, *, offer_id: str) -> ActionCard:
    offering = get_offering(offer_id)
    name_ar = offering.name_ar if offering else offer_id
    body_ar = (
        f"للمتابعة مع {name_ar}: الدفع يتم عبر رابط آمن، وليس داخل واتساب.\n"
        "تختار الطريقة المناسبة لك."
    )
    body_en = "Payment is completed via a secure link, never inside WhatsApp."
    return ActionCard(
        session_id=session_id,
        kind=ActionCardKind.PAYMENT_HANDOFF.value,
        title_ar="إتمام الدفع بأمان",
        title_en="Secure payment",
        body_ar=body_ar,
        body_en=body_en,
        options=(
            _opt("secure_link", "رابط دفع آمن", "Secure payment link"),
            _opt("invoice_email", "فاتورة عبر الإيميل", "Invoice by email"),
            _opt("book_call", "احجز مكالمة", "Book a call"),
        ),
        evidence_level=EvidenceLevel.L0.value,
        risk="medium",
        governance_decision=GovernanceDecision.REQUIRE_APPROVAL.value,
    )


def onboarding_card(session_id: str) -> ActionCard:
    body_ar = (
        "خطوات البدء:\n"
        "1) تأكيد نطاق العمل\n"
        "2) ربط آمن للبيانات عبر البوابة\n"
        "3) أول workflow\n"
        "4) تقرير القيمة الأسبوعي"
    )
    body_en = "Onboarding: confirm scope, secure data connect, first workflow, weekly value report."
    return ActionCard(
        session_id=session_id,
        kind=ActionCardKind.ONBOARDING.value,
        title_ar="بدء التشغيل",
        title_en="Onboarding",
        body_ar=body_ar,
        body_en=body_en,
        options=(
            _opt("confirm_scope", "تأكيد النطاق", "Confirm scope"),
            _opt("open_portal", "فتح البوابة", "Open portal"),
            _opt("book_call", "احجز مكالمة", "Book a call"),
        ),
        evidence_level=EvidenceLevel.L1.value,
        risk="low",
        governance_decision=GovernanceDecision.ALLOW.value,
    )


def support_escalation_card(session_id: str, *, category: str, needs_human: bool) -> ActionCard:
    body_ar = f"تم تصنيف طلبك: {category}.\n" + (
        "نُدخل أحد الفريق للرد بدقة." if needs_human else "نعالجها ونعود لك بخطوة واضحة."
    )
    body_en = f"Support categorized: {category}. " + (
        "Routing to a teammate."
        if needs_human
        else "We'll resolve and reply with a clear next step."
    )
    options = [
        _opt("wait_team", "انتظار الفريق", "Wait for team"),
        _opt("book_call", "احجز مكالمة", "Book a call"),
        _opt("add_details", "أرسل التفاصيل", "Add details"),
    ]
    return ActionCard(
        session_id=session_id,
        kind=ActionCardKind.SUPPORT_ESCALATION.value,
        title_ar="الدعم",
        title_en="Support",
        body_ar=body_ar,
        body_en=body_en,
        options=tuple(options),
        evidence_level=EvidenceLevel.L0.value,
        risk="high" if needs_human else "medium",
        governance_decision=(
            GovernanceDecision.ESCALATE.value if needs_human else GovernanceDecision.ALLOW.value
        ),
    )


def renewal_card(session_id: str, *, offer_id: str, value_summary_ar: str) -> ActionCard:
    offering = get_offering(offer_id)
    name_ar = offering.name_ar if offering else offer_id
    body_ar = (
        f"{value_summary_ar}\n"
        f"الخطوة المقترحة: الاستمرار مع {name_ar}.\n"
        "القيمة التقديرية ليست قيمة مُتحقَّقة."
    )
    body_en = "Renewal suggested based on observed value. Estimated value is not verified value."
    return ActionCard(
        session_id=session_id,
        kind=ActionCardKind.RENEWAL.value,
        title_ar="التجديد",
        title_en="Renewal",
        body_ar=body_ar,
        body_en=body_en,
        options=(
            _opt("renew", "تجديد", "Renew"),
            _opt("upsell", "ترقية الباقة", "Upgrade"),
            _opt("book_call", "احجز مكالمة", "Book a call"),
        ),
        evidence_level=EvidenceLevel.L3.value,
        risk="low",
        governance_decision=_decision_for(body_ar, body_en),
    )


def recommendation_from_offer(session_id: str, rec: OfferRecommendation) -> ActionCard:
    """Build a recommendation card directly from an OfferRecommendation."""
    body_ar = (
        f"التوصية: {rec.name_ar}\n"
        f"السبب: {rec.reason_ar}\n"
        f"الخطة: " + " · ".join(rec.plan_steps_ar)
    )
    body_en = f"Recommendation: {rec.name_en}\nWhy: {rec.reason_en}"
    return ActionCard(
        session_id=session_id,
        kind=ActionCardKind.RECOMMENDATION.value,
        title_ar="التوصية",
        title_en="Recommendation",
        body_ar=body_ar,
        body_en=body_en,
        options=(
            _opt("start", "ابدأ", "Start"),
            _opt("send_proposal", "أرسل العرض", "Send proposal"),
            _opt("book_call", "احجز مكالمة", "Book a call"),
            _opt("explain", "اشرح أكثر", "Explain more"),
        ),
        evidence_level=rec.evidence_level,
        risk="low",
        governance_decision=_decision_for(body_ar, body_en),
    )


__all__ = [
    "approval_card",
    "onboarding_card",
    "payment_handoff_card",
    "permission_card",
    "proof_pack_card",
    "proposal_card",
    "recommendation_card",
    "recommendation_from_offer",
    "renewal_card",
    "support_escalation_card",
]
