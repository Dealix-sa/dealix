"""Action / approval / permission card builder for the WhatsApp Client OS.

Produces two things per card:
1. a logical ``ClientCard`` (governed: risk, evidence level, approval flag), and
2. a WhatsApp Cloud API–style interactive payload (buttons ≤3, else a list),
   reusing ``personal_operator.whatsapp_cards`` for the ≤3 button case.

No card ever sends anything; payloads are generation-only.
"""

from __future__ import annotations

import uuid
from typing import Any

from auto_client_acquisition.personal_operator.whatsapp_cards import _interactive_buttons
from auto_client_acquisition.whatsapp_client_os.schemas import (
    CardOption,
    ClientAssessment,
    ClientCard,
    PermissionRequest,
)

_SAFETY = "no_live_send_no_secrets_in_chat"


def _card_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


# ── Menus ────────────────────────────────────────────────────────────────
def welcome_menu() -> ClientCard:
    return ClientCard(
        card_id=_card_id("menu"),
        kind="menu",
        title_ar="أهلًا، أنا مساعد Dealix",
        body_ar="أقدر أساعدك في تشخيص المبيعات والمتابعة وتشغيل أول نظام داخل شركتك. اختر الخطوة:",
        options=[
            CardOption(id="menu:diagnose", label_ar="تشخيص سريع للشركة", intent="diagnose"),
            CardOption(
                id="menu:campaign_followup",
                label_ar="تجهيز حملة أو متابعة",
                intent="campaign_followup",
            ),
            CardOption(id="menu:connect_tools", label_ar="ربط CRM / تقويم", intent="connect_tools"),
            CardOption(
                id="menu:review_report", label_ar="مراجعة تقرير أو عرض", intent="review_report"
            ),
            CardOption(id="menu:support", label_ar="طلب دعم", intent="support"),
            CardOption(id="menu:not_sure", label_ar="ما أعرف — اقترح علي", intent="not_sure"),
        ],
        evidence_level="L0",
        safety_summary=_SAFETY,
    )


def support_menu() -> ClientCard:
    return ClientCard(
        card_id=_card_id("support"),
        kind="menu",
        title_ar="وش نوع المشكلة؟",
        options=[
            CardOption(id="support:not_working", label_ar="النظام لا يعمل", intent="support"),
            CardOption(id="support:missing_data", label_ar="البيانات ناقصة", intent="support"),
            CardOption(id="support:bad_messages", label_ar="الرسائل غير مناسبة", intent="support"),
            CardOption(id="support:report_unclear", label_ar="التقرير غير واضح", intent="support"),
            CardOption(id="support:human", label_ar="أحتاج شخص", intent="human_handoff"),
        ],
        evidence_level="L0",
        safety_summary=_SAFETY,
    )


def clarify_card() -> ClientCard:
    """«ما أعرف» → start the readiness scan (lowers friction)."""
    return ClientCard(
        card_id=_card_id("clarify"),
        kind="action",
        title_ar="تمام — بسأل أسئلة قصيرة وأقترح أفضل مسار",
        body_ar="فحص الجاهزية يأخذ دقائق ويعطيك توصية واحدة واضحة.",
        options=[
            CardOption(id="asmt:start", label_ar="ابدأ الفحص", intent="assessment_start"),
            CardOption(id="rec:book_call", label_ar="أفضل أتحدث مع شخص", intent="book_call"),
        ],
        evidence_level="L0",
        safety_summary=_SAFETY,
    )


# ── Assessment ─────────────────────────────────────────────────────────--
def assessment_question_card(axis_spec: dict[str, Any], *, step: int, total: int) -> ClientCard:
    opts = [
        CardOption(
            id=f"asmt:{axis_spec['axis']}:{o['id']}",
            label_ar=o["label_ar"],
            intent="assessment_answer",
            payload={"axis": axis_spec["axis"], "option_id": o["id"]},
        )
        for o in axis_spec["options"]
    ]
    return ClientCard(
        card_id=_card_id("asmt"),
        kind="action",
        title_ar=f"الخطوة {step} من {total}",
        body_ar=axis_spec["question_ar"],
        options=opts,
        evidence_level="L0",
        safety_summary=_SAFETY,
    )


def recommendation_card(assessment: ClientAssessment) -> ClientCard:
    score = assessment.score
    overall = score.overall if score else 0
    reason = "\n".join(f"- {r}" for r in assessment.rationale_ar)
    body = (
        f"النتيجة الكلية: {overall}/100\n"
        f"أنسب بداية: {assessment.recommended_offer_ar}\n"
        f"السبب:\n{reason}\n"
        f"أول workflow: {assessment.first_workflow_ar}"
    )
    return ClientCard(
        card_id=_card_id("rec"),
        kind="recommendation",
        title_ar="بناءً على إجاباتك، هذي أفضل خطوة",
        body_ar=body,
        reason_ar=assessment.next_action_ar,
        options=[
            CardOption(id="rec:start", label_ar="ابدأ", intent="assessment_start"),
            CardOption(id="rec:proposal", label_ar="أرسل لي العرض", intent="request_proposal"),
            CardOption(id="rec:book_call", label_ar="احجز مكالمة", intent="book_call"),
            CardOption(id="rec:simplify", label_ar="اشرح أبسط", intent="simplify"),
        ],
        risk=score.risk if score else "medium",
        evidence_level=assessment.evidence_level,
        catalog_ref=assessment.recommended_offer,
        safety_summary=_SAFETY,
    )


# ── Approval / permission / refusals ─────────────────────────────────────
def approval_card(*, draft_text_ar: str, catalog_ref: str = "", risk: str = "medium") -> ClientCard:
    cid = _card_id("appr")
    return ClientCard(
        card_id=cid,
        kind="approval",
        title_ar="جاهز Draft — يحتاج موافقتك قبل أي إرسال",
        body_ar=draft_text_ar,
        options=[
            CardOption(id=f"card:{cid}:approve", label_ar="اعتماد", intent="approve"),
            CardOption(id=f"card:{cid}:edit", label_ar="تعديل", intent="edit"),
            CardOption(id=f"card:{cid}:reject", label_ar="رفض", intent="reject"),
            CardOption(id=f"card:{cid}:simplify", label_ar="اختصرها", intent="simplify"),
        ],
        risk=risk,  # type: ignore[arg-type]
        evidence_level="L2",
        requires_approval=True,
        catalog_ref=catalog_ref,
        safety_summary=_SAFETY,
    )


def permission_card(req: PermissionRequest) -> ClientCard:
    body = (
        f"النظام: {req.system or '—'}\n"
        f"الغرض: {req.purpose_ar}\n"
        f"الصلاحية: {req.scope or req.level}\n"
        f"الخطورة: {req.risk} · المدة: {req.duration_days} يوم"
    )
    if req.secure_portal_required:
        body += "\n🔒 لأمان البيانات: لا ترسل المفتاح هنا — أكمل عبر الرابط الآمن."
    return ClientCard(
        card_id=_card_id("perm"),
        kind="permission",
        title_ar="نحتاج صلاحية واحدة لإكمال الربط",
        body_ar=body,
        options=[
            CardOption(
                id=f"perm:{req.permission_id}:grant", label_ar="أوافق", intent="permission_grant"
            ),
            CardOption(
                id=f"perm:{req.permission_id}:deny", label_ar="أرفض", intent="permission_deny"
            ),
            CardOption(
                id=f"perm:{req.permission_id}:explain", label_ar="اشرح لي", intent="simplify"
            ),
        ],
        risk=req.risk,
        evidence_level="L1",
        requires_approval=req.level in {"L4", "L5"},
        safety_summary=_SAFETY,
    )


def secrets_refusal_card(secure_portal_url: str = "") -> ClientCard:
    body = "لا ترسل المفاتيح أو كلمات السر هنا — لأمان بياناتك لا نحفظها في الشات."
    opts = [
        CardOption(
            id="perm:secure_portal:open", label_ar="فتح الرابط الآمن", intent="connect_tools"
        ),
        CardOption(id="perm:manual:steps", label_ar="أرسل خطوات يدوية", intent="connect_tools"),
        CardOption(
            id="perm:readonly:grant", label_ar="صلاحية قراءة فقط", intent="permission_grant"
        ),
    ]
    if secure_portal_url:
        body += f"\nالرابط الآمن: {secure_portal_url}"
    return ClientCard(
        card_id=_card_id("secref"),
        kind="action",
        title_ar="🔒 الأمان أولًا",
        body_ar=body,
        options=opts,
        risk="high",
        evidence_level="L0",
        safety_summary=_SAFETY,
    )


def unsafe_refusal_card(reasons_ar: str) -> ClientCard:
    return ClientCard(
        card_id=_card_id("unsafe"),
        kind="action",
        title_ar="هذا الطلب خارج سياسة Dealix",
        body_ar=f"{reasons_ar}\nنتواصل فقط مع جهات على علاقة قائمة، بمسودة + موافقة صريحة منك.",
        options=[
            CardOption(id="menu:diagnose", label_ar="ابدأ تشخيص بدلًا من ذلك", intent="diagnose"),
            CardOption(id="menu:not_sure", label_ar="ما أعرف — اقترح علي", intent="not_sure"),
        ],
        risk="high",
        evidence_level="L0",
        safety_summary=_SAFETY,
    )


# ── WhatsApp interactive payload ─────────────────────────────────────────
def to_whatsapp_payload(card: ClientCard) -> dict[str, Any]:
    """Render a card as a Cloud API interactive payload (generation only)."""
    body_text = (card.title_ar + ("\n\n" + card.body_ar if card.body_ar else ""))[:1024]
    if len(card.options) <= 3 and card.options:
        payload = _interactive_buttons([{"id": o.id, "title": o.label_ar} for o in card.options])
        payload["interactive"]["body"] = {"text": body_text}
        return payload
    # >3 options → list message (rows capped at WhatsApp's 10)
    rows = [{"id": o.id, "title": o.label_ar[:24]} for o in card.options[:10]]
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": body_text},
            "action": {
                "button": "اختر",
                "sections": [{"title": "الخيارات", "rows": rows}],
            },
        },
    }


__all__ = [
    "approval_card",
    "assessment_question_card",
    "clarify_card",
    "permission_card",
    "recommendation_card",
    "secrets_refusal_card",
    "support_menu",
    "to_whatsapp_payload",
    "unsafe_refusal_card",
    "welcome_menu",
]
