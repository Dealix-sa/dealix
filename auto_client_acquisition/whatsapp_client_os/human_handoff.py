"""WhatsApp Client OS — Human Handoff OS.

The bot must know when to stop and bring a human in. Faster access to a human
after a bot reaches its limit increases trust, so handoff is explicit, fast,
and always offered. Triggers: anger, final-price asks, legal/contract,
sensitive data, deletion requests, dissatisfaction, low confidence, looping,
or an explicit request for a person.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from auto_client_acquisition.whatsapp_client_os.schemas import HandoffReason

_LOOP_LIMIT = 3  # turns without resolution before we escalate

_TRIGGERS: tuple[tuple[HandoffReason, re.Pattern[str]], ...] = (
    (
        HandoffReason.ANGRY,
        re.compile(
            r"غاضب|زعلان|سيّئ|سيء\s+جدا|تعب(?:ت|نا)\s+منكم|angry|terrible|awful|furious",
            re.IGNORECASE,
        ),
    ),
    (
        HandoffReason.PRICING_COMMITMENT,
        re.compile(
            r"السعر\s+النهائي|كم\s+بالضبط\s+السعر|أعطني\s+سعر\s+نهائي|final\s+price|exact\s+price",
            re.IGNORECASE,
        ),
    ),
    (
        HandoffReason.LEGAL_CONTRACT,
        re.compile(
            r"عقد|اتفاقية|التزام\s+قانوني|بند\s+قانوني|contract|legal|agreement|nda|sla",
            re.IGNORECASE,
        ),
    ),
    (
        HandoffReason.DATA_DELETION,
        re.compile(
            r"احذف\s+بيانات|حذف\s+بياناتي|امسح\s+بياناتي|delete\s+my\s+data|erase\s+my\s+data",
            re.IGNORECASE,
        ),
    ),
    (
        HandoffReason.SENSITIVE_DATA,
        re.compile(
            r"بيانات\s+بنكية|رقم\s+الهوية|رقم\s+بطاقة|آيبان|iban|national\s+id|bank\s+details|credit\s+card",
            re.IGNORECASE,
        ),
    ),
    (
        HandoffReason.DISSATISFIED,
        re.compile(
            r"غير\s+راضٍ|غير\s+راضي|مو\s+راضي|مب\s+عاجبني|not\s+satisfied|unhappy|disappointed",
            re.IGNORECASE,
        ),
    ),
    (
        HandoffReason.EXPLICIT_REQUEST,
        re.compile(
            r"أبغى\s+(?:إنسان|شخص|موظف)|كلموني|اتصلوا\s+فيني|human|real\s+person|call\s+me",
            re.IGNORECASE,
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class HandoffDecision:
    needed: bool
    reasons: tuple[str, ...]


def should_handoff(
    text: str,
    *,
    turn_count: int = 0,
    low_confidence: bool = False,
) -> HandoffDecision:
    """Decide whether to escalate to a human, and why."""
    reasons: list[str] = []
    raw = text or ""
    for reason, pattern in _TRIGGERS:
        if pattern.search(raw):
            reasons.append(reason.value)
    if low_confidence:
        reasons.append(HandoffReason.LOW_CONFIDENCE.value)
    if turn_count >= _LOOP_LIMIT:
        reasons.append(HandoffReason.LOOP_LIMIT.value)
    uniq = tuple(dict.fromkeys(reasons))
    return HandoffDecision(needed=bool(uniq), reasons=uniq)


def client_handoff_message(lang: str = "ar") -> str:
    if lang == "en":
        return (
            "I'll bring a teammate in so we answer you precisely. "
            "I've prepared a summary of the conversation and the point you need."
        )
    return (
        "أحتاج أُدخل أحد من الفريق عشان نرد عليك بدقة. " "جهّزت لهم ملخص المحادثة والنقطة المطلوبة."
    )


def build_handoff_brief(
    *,
    session_id: str,
    company: str,
    reasons: tuple[str, ...],
    last_text_redacted: str,
    suggested_response_ar: str = "",
) -> dict[str, object]:
    """Internal brief for the founder/team. Text must already be PII-redacted."""
    risk = (
        "high"
        if any(
            r
            in {
                HandoffReason.ANGRY.value,
                HandoffReason.LEGAL_CONTRACT.value,
                HandoffReason.SENSITIVE_DATA.value,
                HandoffReason.DATA_DELETION.value,
            }
            for r in reasons
        )
        else "medium"
    )
    return {
        "session_id": session_id,
        "company": company,
        "reasons": list(reasons),
        "last_message_redacted": last_text_redacted,
        "suggested_response_ar": suggested_response_ar,
        "risk": risk,
        "next_action": "call_or_approve_proposal_range",
    }


__all__ = [
    "HandoffDecision",
    "build_handoff_brief",
    "client_handoff_message",
    "should_handoff",
]
