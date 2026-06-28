"""Reply classification for the Smart Reply / Negotiation Desk.

Given an inbound reply (text), classify it into one of the controlled reply
types, infer sentiment and intent, and recommend a safe next action. The
classifier is keyword/heuristic based and bilingual (AR + EN). It never
auto-replies — it only proposes.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.commercial.schemas import ReplyClassification

# Ordered most-specific → least-specific so the first match wins.
_RULES: list[tuple[str, list[str]]] = [
    ("unsubscribe", ["unsubscribe", "stop", "remove me", "ايقاف", "إيقاف", "الغاء الاشتراك", "لا ترسل"]),
    ("contract_request", ["contract", "agreement", "sign", "عقد", "اتفاقية", "توقيع"]),
    ("meeting_request", ["meeting", "call", "demo", "schedule", "اجتماع", "مكالمة", "موعد", "عرض"]),
    ("price_objection", ["expensive", "too much", "budget", "discount", "price", "غالي", "ميزانية", "خصم", "السعر"]),
    ("partnership_interest", ["partner", "partnership", "collaborate", "شراكة", "تعاون"]),
    ("referral", ["refer", "introduce", "colleague", "another team", "أحول", "أعرّفك", "زميل"]),
    ("send_details", ["send details", "more info", "brochure", "deck", "ارسل", "تفاصيل", "معلومات"]),
    ("wrong_person", ["wrong person", "not me", "not the right", "لست", "الشخص الخطأ", "ليس انا"]),
    ("not_now", ["later", "next quarter", "not now", "busy", "لاحقا", "لاحقاً", "ليس الآن", "مشغول"]),
    ("no_interest", ["not interested", "no thanks", "no thank", "غير مهتم", "لا شكرا", "لا أرغب"]),
    ("support_question", ["how does", "question", "support", "issue", "كيف", "سؤال", "مشكلة", "دعم"]),
    ("interested", ["interested", "yes", "sounds good", "tell me more", "مهتم", "نعم", "ممتاز", "أوافق"]),
]

_SENTIMENT = {
    "interested": "positive",
    "meeting_request": "positive",
    "partnership_interest": "positive",
    "send_details": "positive",
    "referral": "neutral",
    "contract_request": "positive",
    "support_question": "neutral",
    "not_now": "neutral",
    "price_objection": "neutral",
    "wrong_person": "neutral",
    "no_interest": "negative",
    "unsubscribe": "negative",
    "unknown": "neutral",
}

_RECOMMENDED_ACTION = {
    "interested": "Move to meeting_ready; draft booking options",
    "send_details": "Draft details pack; keep draft-only until approved",
    "price_objection": "Route to Negotiation Desk (guardrailed, no discount authority)",
    "not_now": "Schedule D7 nurture follow-up",
    "no_interest": "Close as lost (requires approval); add to suppression",
    "wrong_person": "Ask for correct contact; do not re-target without source",
    "referral": "Capture referral; new account needs its own source_url",
    "partnership_interest": "Route to partnership motion; draft partnership pitch",
    "contract_request": "ESCALATE: legal/pricing is A3-restricted, founder only",
    "meeting_request": "Generate 3 booking options (no calendar write by default)",
    "support_question": "Draft answer; flag if it implies a delivery commitment",
    "unsubscribe": "Honour immediately: opt-out, suppress, stop all outreach",
    "unknown": "Human review required",
}

# High-risk reply types that must be surfaced in the decision queue.
HIGH_RISK_TYPES = ("contract_request", "unsubscribe")


def classify_reply(
    reply_text: str,
    card_id: str,
    reply_id: str | None = None,
) -> ReplyClassification:
    low = (reply_text or "").lower()
    reply_type = "unknown"
    for rtype, keywords in _RULES:
        if any(k in low for k in keywords):
            reply_type = rtype
            break

    risk = "high" if reply_type in HIGH_RISK_TYPES else "low"
    if reply_type in ("price_objection", "no_interest"):
        risk = "medium"

    return ReplyClassification(
        reply_id=reply_id or f"reply_{card_id}",
        card_id=card_id,
        reply_type=reply_type,
        sentiment=_SENTIMENT.get(reply_type, "neutral"),
        intent=reply_type,
        recommended_action=_RECOMMENDED_ACTION.get(reply_type, "Human review required"),
        risk_level=risk,
    )


def classify_replies(records: list[Mapping[str, Any]]) -> list[ReplyClassification]:
    out: list[ReplyClassification] = []
    for rec in records:
        out.append(
            classify_reply(
                reply_text=str(rec.get("text") or rec.get("reply_text") or ""),
                card_id=str(rec.get("card_id", "")),
                reply_id=str(rec.get("reply_id")) if rec.get("reply_id") else None,
            )
        )
    return out
