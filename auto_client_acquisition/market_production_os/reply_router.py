"""Reply Handling OS — classify inbound replies and route to a next action.

Heuristic, deterministic classifier (no PII stored in the routing layer).
Unsubscribe / angry / bounce always lead to suppression.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.market_production_os.schemas import ReplyClass

# action per class + whether the address must be suppressed.
ROUTING: dict[str, tuple[str, bool]] = {
    ReplyClass.POSITIVE.value: ("send_discovery_invite", False),
    ReplyClass.INTERESTED_LATER.value: ("move_to_nurture", False),
    ReplyClass.PRICE_QUESTION.value: ("send_offer_card", False),
    ReplyClass.SEND_MORE_INFO.value: ("send_proof_pack", False),
    ReplyClass.WRONG_PERSON.value: ("ask_for_referral", False),
    ReplyClass.NOT_INTERESTED.value: ("close_polite", False),
    ReplyClass.UNSUBSCRIBE.value: ("suppress_immediately", True),
    ReplyClass.ANGRY.value: ("apologize_and_suppress", True),
    ReplyClass.AUTO_REPLY.value: ("hold_no_action", False),
    ReplyClass.BOUNCE.value: ("suppress_email", True),
}

_KEYWORDS: list[tuple[ReplyClass, tuple[str, ...]]] = [
    (ReplyClass.UNSUBSCRIBE, ("unsubscribe", "إيقاف", "ألغ", "stop", "إلغاء الاشتراك", "remove me")),
    (ReplyClass.ANGRY, ("angry", "lawyer", "spam", "إزعاج", "بلاغ", "محامي", "أبلغ عنكم")),
    (ReplyClass.BOUNCE, ("mailer-daemon", "delivery failed", "undeliverable", "بريد مرتجع")),
    (ReplyClass.AUTO_REPLY, ("out of office", "auto-reply", "خارج المكتب", "رد تلقائي")),
    (ReplyClass.WRONG_PERSON, ("wrong person", "الشخص الخطأ", "لست المسؤول", "حول")),
    (ReplyClass.PRICE_QUESTION, ("price", "cost", "السعر", "التكلفة", "كم")),
    (ReplyClass.SEND_MORE_INFO, ("more info", "details", "تفاصيل", "مزيد من المعلومات")),
    (ReplyClass.NOT_INTERESTED, ("not interested", "غير مهتم", "لا نحتاج", "لا شكرا")),
    (ReplyClass.INTERESTED_LATER, ("later", "next quarter", "لاحقًا", "مستقبلا", "بعدين")),
    (ReplyClass.POSITIVE, ("interested", "yes", "call", "demo", "مهتم", "نعم", "اتصل", "موعد")),
]


@dataclass(frozen=True, slots=True)
class ReplyRouting:
    reply_class: str
    next_action: str
    suppress: bool


def classify_reply(text: str) -> ReplyClass:
    """Classify a reply by keyword priority (unsubscribe/angry win first)."""
    blob = (text or "").lower()
    for cls, keywords in _KEYWORDS:
        if any(k.lower() in blob for k in keywords):
            return cls
    return ReplyClass.NOT_INTERESTED


def route_reply(reply_class: ReplyClass | str) -> ReplyRouting:
    """Return the action + suppression flag for a classified reply."""
    value = reply_class.value if isinstance(reply_class, ReplyClass) else str(reply_class)
    action, suppress = ROUTING.get(value, ("close_polite", False))
    return ReplyRouting(reply_class=value, next_action=action, suppress=suppress)


def classify_and_route(text: str) -> ReplyRouting:
    """Convenience: classify then route in one call."""
    return route_reply(classify_reply(text))


__all__ = ["ROUTING", "ReplyRouting", "classify_and_route", "classify_reply", "route_reply"]
