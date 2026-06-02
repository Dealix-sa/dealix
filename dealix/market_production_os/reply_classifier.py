"""Reply classification + routed next action (AR + EN heuristics).

Keyword-based and deterministic. 'unsubscribe', 'bounce', and 'angry' force
immediate suppression. Anything ambiguous routes to the founder.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# classification -> (recommended_action, requires_founder, suppress)
_ACTIONS: dict[str, tuple[str, bool, bool]] = {
    "positive": ("discovery_invite", True, False),
    "interested_but_later": ("nurture_followup", True, False),
    "price_question": ("offer_card", True, False),
    "send_more_info": ("proof_pack", True, False),
    "not_interested": ("nurture", False, False),
    "wrong_person": ("ask_referral", True, False),
    "unsubscribe": ("suppress_immediately", False, True),
    "angry": ("apologize_and_suppress", True, True),
    "auto_reply": ("retry_later", False, False),
    "bounce": ("suppress_email", False, True),
}

# Ordered: high-priority / safety classes first.
_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("unsubscribe", ("unsubscribe", "opt out", "opt-out", "remove me", "stop emailing me",
                     "إيقاف", "ايقاف", "الغاء", "إلغاء", "أزل", "ازل", "لا ترسل", "لا تراسلني")),
    ("bounce", ("delivery failed", "undeliverable", "mailer-daemon", "address not found",
                "could not be delivered", "فشل التسليم", "لم يتم التسليم")),
    ("auto_reply", ("out of office", "auto-reply", "autoreply", "automatic reply", "on vacation",
                    "رسالة تلقائية", "خارج المكتب", "في إجازة")),
    ("angry", ("this is spam", "stop spamming", "do not contact", "report you", "report this",
               "شكوى", "مزعج", "لا تزعجني", "بلاغ")),
    ("wrong_person", ("wrong person", "not the right person", "i am not responsible", "forward you to",
                      "لست المسؤول", "الشخص الخطأ", "حوّلتك", "ليست من اختصاصي")),
    ("price_question", ("price", "pricing", "how much", "what is the cost", "كم السعر", "التكلفة",
                        "بكم", "الأسعار", "كم تكلفة")),
    ("send_more_info", ("more info", "more information", "send details", "tell me more", "send me",
                        "معلومات أكثر", "تفاصيل أكثر", "ابعث", "أرسل لي", "ارسل لي")),
    ("interested_but_later", ("later", "next quarter", "next month", "not now", "after ramadan",
                              "لاحقاً", "لاحقا", "بعدين", "الربع القادم", "الشهر القادم", "مشغول حالياً")),
    ("not_interested", ("not interested", "no thanks", "no thank you", "غير مهتم", "غير مهتمين",
                        "لا شكراً", "لا شكرا", "ما يناسبنا", "لا نحتاج")),
    ("positive", ("interested", "let's talk", "lets talk", "book", "schedule", "set up a call", "sounds good",
                  "مهتم", "مهتمين", "موعد", "اجتماع", "تواصل معي", "ابدأ", "نبدأ", "يناسبنا", "تفضل")),
)


@dataclass(frozen=True, slots=True)
class ReplyClassification:
    classification: str
    recommended_action: str
    requires_founder: bool
    suppress: bool
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "classification": self.classification,
            "recommended_action": self.recommended_action,
            "requires_founder": self.requires_founder,
            "suppress": self.suppress,
            "confidence": self.confidence,
        }


def classify(text: str, language: str = "ar") -> ReplyClassification:
    _ = language
    blob = (text or "").lower()
    for label, keywords in _PATTERNS:
        if any(k in blob for k in keywords):
            action, requires_founder, suppress = _ACTIONS[label]
            return ReplyClassification(label, action, requires_founder, suppress, 0.8)
    # Ambiguous: route to founder, low confidence, no suppression.
    action, requires_founder, _suppress = _ACTIONS["send_more_info"]
    return ReplyClassification("send_more_info", action, True, False, 0.3)
