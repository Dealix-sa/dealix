"""WhatsApp Client OS — intent router.

Deterministic classifier: menu numbers first, then AR/EN keyword matching.
There is no open-ended LLM routing here — the front door is a controlled set
of intents. Unsafe outreach requests (cold WhatsApp, blasts, purchased lists)
short-circuit to ``BLOCKED_UNSAFE`` via the canonical decision-bot policy.
"""

from __future__ import annotations

import re

from auto_client_acquisition.whatsapp_client_os.schemas import Intent
from auto_client_acquisition.whatsapp_decision_bot.policy import is_unsafe_command

# Numbered welcome menu (see WHATSAPP_CLIENT_EXPERIENCE_AR.md §first message).
_MENU: dict[str, Intent] = {
    "1": Intent.START_SCAN,
    "2": Intent.BUILD_FOLLOWUP,
    "3": Intent.VIEW_SERVICES,
    "4": Intent.REVIEW_PROPOSAL,
    "5": Intent.REQUEST_SUPPORT,
    "6": Intent.RECOMMEND_ME,
}

# Cold-outreach / scraping requests the bot must refuse outright. Broader and
# more Arabic-tolerant than the founder-layer policy (handles missing hamza,
# "ارقام مشتراة", harvest/blast wording).
_UNSAFE_EXTRA: tuple[re.Pattern[str], ...] = (
    re.compile(
        r"(?:ارسل|أرسل|ابعث|رسائل?)\s*(?:واتساب|رسائل?|sms|اي?ميل|إيميل)?\s*(?:لكل|للجميع|لجميع|لكافة)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:قائم|قائمه|أرقام|ارقام|الأرقام|الارقام)\s*\S*\s*(?:مشترا|المشترا)", re.IGNORECASE
    ),
    re.compile(r"(?:اسحب|سحب|اجمع)\s*(?:أرقام|ارقام|الأرقام|الارقام|بيانات)", re.IGNORECASE),
    re.compile(
        r"\bcold\s+(?:whatsapp|outreach|dm|message)|broadcast|blast|scrap(?:e|ing)|harvest",
        re.IGNORECASE,
    ),
)

# Ordered keyword patterns — first match wins. Order matters:
# - "اقترح علي" (recommend-me) before generic service browsing.
# - Support (problem/issue words) before proposal/payment so a *problem with
#   an invoice/report* routes to support, not to billing/proposal.
_KEYWORDS: tuple[tuple[Intent, re.Pattern[str]], ...] = (
    (
        Intent.REQUEST_HUMAN,
        re.compile(
            r"أبغى\s+(?:إنسان|شخص|موظف|أحد)|كلم\s+(?:شخص|إنسان)|human|agent|talk\s+to\s+(?:someone|a\s+person)",
            re.IGNORECASE,
        ),
    ),
    (
        Intent.RECOMMEND_ME,
        re.compile(
            r"ما\s*أعرف|ماأعرف|اقترح\s*عل[يى]|مو\s*متأكد|not\s+sure|recommend\s+me|suggest",
            re.IGNORECASE,
        ),
    ),
    (
        Intent.START_SCAN,
        re.compile(r"فحص|جاهز|تقييم|قياس|readiness|assess|scan|diagnos", re.IGNORECASE),
    ),
    (
        Intent.BUILD_FOLLOWUP,
        re.compile(r"متابع|فولو|follow.?up|حمل[ةه]\s+متابع|تذكير\s+leads", re.IGNORECASE),
    ),
    (Intent.REVIEW_DRAFT, re.compile(r"مسودة|مسوده|راجع\s+الرسالة|draft", re.IGNORECASE)),
    (
        Intent.REQUEST_SUPPORT,
        re.compile(
            r"دعم|مشكلة|مشكله|ما\s+يشتغل|عطل|شكوى|support|issue|problem|help|broken|not\s+working",
            re.IGNORECASE,
        ),
    ),
    (
        Intent.REVIEW_PROPOSAL,
        re.compile(r"عرض|تقرير|بروبوزال|proposal|report|quote", re.IGNORECASE),
    ),
    (Intent.PROOF_PACK, re.compile(r"proof|إثبات|دليل|حزمة\s+الإثبات", re.IGNORECASE)),
    (Intent.START_PAYMENT, re.compile(r"دفع|ادفع|فاتورة|سداد|pay|invoice|checkout", re.IGNORECASE)),
    (Intent.RENEWAL, re.compile(r"تجديد|renew|upsell|ترقية", re.IGNORECASE)),
    (
        Intent.GIVE_PERMISSION,
        re.compile(r"صلاحي|ربط|تكامل|permission|connect|integrat", re.IGNORECASE),
    ),
    (
        Intent.VIEW_SERVICES,
        re.compile(r"خدم|باقات|أسعار|service|pricing|package|plans?", re.IGNORECASE),
    ),
    (Intent.START_SCAN, re.compile(r"ابدأ|نبدأ|start|begin", re.IGNORECASE)),
)

_GREETING = re.compile(
    r"^\s*(?:السلام|مرحبا|اهلا|أهلا|هلا|hi|hello|hey|مساء|صباح)\b", re.IGNORECASE
)


def classify_intent(text: str, *, is_first_turn: bool = False) -> tuple[Intent, float]:
    """Return (intent, confidence in 0..1).

    Menu numbers are high confidence. Unsafe outreach is hard-blocked.
    """
    raw = (text or "").strip()
    if not raw:
        return (Intent.WELCOME if is_first_turn else Intent.UNKNOWN, 1.0 if is_first_turn else 0.0)

    unsafe, _ = is_unsafe_command(raw)
    if unsafe or any(p.search(raw) for p in _UNSAFE_EXTRA):
        return (Intent.BLOCKED_UNSAFE, 1.0)

    token = raw.split()[0].strip(".)-")
    if token in _MENU:
        return (_MENU[token], 1.0)

    for intent, pattern in _KEYWORDS:
        if pattern.search(raw):
            return (intent, 0.8)

    if is_first_turn or _GREETING.match(raw):
        return (Intent.WELCOME, 0.9)

    return (Intent.UNKNOWN, 0.3)


__all__ = ["classify_intent"]
