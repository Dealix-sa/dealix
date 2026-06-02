"""Human handoff router for the WhatsApp Client OS.

Escalates to a human (founder/CSM) — with full context — on:
- explicit request («أحتاج شخص»),
- a secrets-in-chat attempt,
- sensitive data,
- pricing negotiation / contracts,
- complaints,
- L5 (sensitive) permissions,
- repeated «unknown» (the bot is lost — never loop the client).

The handoff packet preserves the last messages and a suggested action, with
no raw PII leaked into logs (handles only).
"""

from __future__ import annotations

import uuid

from auto_client_acquisition.whatsapp_client_os.schemas import (
    ClientIntent,
    HandoffReason,
    HandoffRequest,
    PermissionLevel,
    SessionStage,
    WhatsAppSession,
)

_REASON_TEXT_AR: dict[HandoffReason, str] = {
    "ambiguity": "غموض في الطلب يحتاج توضيح بشري.",
    "sensitive_data": "وجود بيانات حسّاسة يحتاج مراجعة بشرية.",
    "pricing_negotiation": "تفاوض على السعر — خارج صلاحية المساعد.",
    "contract": "طلب يتعلق بعقد — يحتاج مراجعة بشرية/قانونية.",
    "complaint": "شكوى تحتاج تدخل بشري.",
    "explicit_request": "العميل طلب التحدث مع شخص.",
    "permission_l5": "صلاحية حسّاسة (L5) لا تتم عبر واتساب وحده.",
    "secrets_attempt": "محاولة إرسال مفتاح/سر في الشات — مراجعة أمنية.",
    "repeated_unknown": "تكرار عدم فهم الطلب — نصعّد بدل تكرار القوائم.",
}

_SUGGESTED_ACTION_AR: dict[HandoffReason, str] = {
    "ambiguity": "اتصال 10 دقائق لتوضيح الهدف.",
    "sensitive_data": "مراجعة DPA + مسار آمن قبل أي ربط.",
    "pricing_negotiation": "مكالمة مؤسس لمناقشة النطاق والسعر.",
    "contract": "تحويل لمراجعة العقد + توقيع DPA.",
    "complaint": "اتصال خلال ساعة + تلخيص المشكلة.",
    "explicit_request": "اتصال 10 دقائق.",
    "permission_l5": "إكمال عبر بوابة آمنة + تأكيد بشري.",
    "secrets_attempt": "تأكيد عدم تسجيل السر + إرشاد للبوابة الآمنة.",
    "repeated_unknown": "اتصال قصير لفهم الاحتياج.",
}


def detect_reason(
    *,
    intent: ClientIntent,
    stage: SessionStage,
    has_sensitive_data: bool = False,
    is_complaint: bool = False,
    secrets_attempt: bool = False,
    permission_level: PermissionLevel | None = None,
    unknown_streak: int = 0,
) -> HandoffReason | None:
    """Return the first matching handoff reason, or None."""
    if intent == "human_handoff":
        return "explicit_request"
    if secrets_attempt:
        return "secrets_attempt"
    if permission_level == "L5":
        return "permission_l5"
    if is_complaint:
        return "complaint"
    if has_sensitive_data:
        return "sensitive_data"
    if stage in {"proposal", "payment_handoff"} and intent in {"reject", "edit"}:
        return "pricing_negotiation"
    if unknown_streak >= 2:
        return "repeated_unknown"
    return None


def should_handoff(**kwargs: object) -> bool:
    return detect_reason(**kwargs) is not None  # type: ignore[arg-type]


def build_handoff(
    session: WhatsAppSession,
    *,
    reason: HandoffReason,
    last_messages: list[str] | None = None,
    urgency: str = "medium",
) -> HandoffRequest:
    msgs = [m[:280] for m in (last_messages or [])][-10:]
    summary = (
        f"عميل ({session.company_name or session.client_handle}) "
        f"عند مرحلة «{session.stage}» — {_REASON_TEXT_AR.get(reason, reason)}"
    )
    return HandoffRequest(
        handoff_id=f"handoff_{uuid.uuid4().hex[:10]}",
        session_id=session.session_id,
        client_handle=session.client_handle,
        reason=reason,
        summary_ar=summary,
        last_messages=msgs,
        suggested_action_ar=_SUGGESTED_ACTION_AR.get(reason, "اتصال قصير."),
        urgency=urgency,  # type: ignore[arg-type]
    )


__all__ = ["build_handoff", "detect_reason", "should_handoff"]
