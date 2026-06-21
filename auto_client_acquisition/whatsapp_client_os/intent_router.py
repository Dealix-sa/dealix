"""Deterministic intent router for the WhatsApp Client OS.

The Client OS is a *business workflow assistant*, not a general-purpose
chatbot. Intent is resolved by, in order:
1. structured button ids (e.g. ``menu:diagnose``, ``asmt:lead_flow:lead_flow_high``),
2. the policy guard (secrets / unsafe requests short-circuit to a blocked intent),
3. a small Arabic+English keyword map,
4. fallback → ``unknown`` (the engine then re-shows the menu + «ما أعرف»).

An LLM may later *draft* copy, but routing/decisions stay deterministic here.
"""

from __future__ import annotations

import re

from auto_client_acquisition.whatsapp_client_os.schemas import ClientIntent, IntentResult
from auto_client_acquisition.whatsapp_client_os.whatsapp_policy_guard import guard_inbound

# ── Button-id namespaces → intent ────────────────────────────────────────
_MENU_INTENTS: frozenset[str] = frozenset(
    {
        "diagnose",
        "campaign_followup",
        "connect_tools",
        "review_report",
        "support",
        "not_sure",
        "assessment_start",
        "request_proposal",
        "book_call",
        "human_handoff",
    }
)

# ── Keyword map (free text). Each tuple: (intent, compiled pattern). ──────
_KEYWORDS: tuple[tuple[ClientIntent, re.Pattern[str]], ...] = (
    (
        "not_sure",
        re.compile(
            r"ما\s*أعرف|لا\s*أعرف|مو\s*متأكد|غير\s*متأكد|اقترح|ساعدني|وش\s*تنصح|don'?t\s*know|not\s*sure|suggest",
            re.IGNORECASE,
        ),
    ),
    (
        "human_handoff",
        re.compile(
            r"أحتاج\s*(شخص|إنسان|موظف)|كلّموني|اتصلوا|تحدث\s*مع\s*شخص|human|agent|representative|اشكي|شكوى|مشكلة\s*كبيرة",
            re.IGNORECASE,
        ),
    ),
    (
        "support",
        re.compile(r"دعم|مشكلة|ما\s*يشتغل|خطأ|عطل|support|help|issue|bug|broken", re.IGNORECASE),
    ),
    (
        "diagnose",
        re.compile(
            r"تشخيص|فحص|جاهزية|قيّم|قيم(ني|نا)?|diagnos|assess|readiness|scan", re.IGNORECASE
        ),
    ),
    (
        "assessment_start",
        re.compile(r"ابدأ\s*(التشخيص|الفحص|التقييم)|start\s*(scan|assessment)", re.IGNORECASE),
    ),
    (
        "campaign_followup",
        re.compile(r"متابعة|حملة|leads|ليدز|follow.?up|campaign|reminders?", re.IGNORECASE),
    ),
    (
        "connect_tools",
        re.compile(r"ربط|اربط|تكامل|connect|integrat|crm|hubspot|تقويم|calendar", re.IGNORECASE),
    ),
    ("review_report", re.compile(r"تقرير|عرض|proposal|report|عرض\s*سعر|review", re.IGNORECASE)),
    (
        "request_proposal",
        re.compile(r"أرسل\s*(لي\s*)?العرض|عرض\s*سعر|quote|proposal\s*please", re.IGNORECASE),
    ),
    ("book_call", re.compile(r"احجز|موعد|مكالمة|اجتماع|book|call|meeting|demo", re.IGNORECASE)),
    (
        "send_file_link",
        re.compile(r"رابط|ملف|csv|excel|ارفع|أرفع|file|link|upload|sheet", re.IGNORECASE),
    ),
    ("approve", re.compile(r"^\s*(اعتمد|موافق|نعم|تمام|approve|ok|yes)\s*$", re.IGNORECASE)),
    ("reject", re.compile(r"^\s*(ارفض|لا|إلغاء|الغاء|reject|no|cancel)\s*$", re.IGNORECASE)),
    ("edit", re.compile(r"عدّل|عدل|تعديل|غيّر|edit|change", re.IGNORECASE)),
    ("simplify", re.compile(r"اختصر|أبسط|بسّط|اشرح\s*أبسط|simpler|shorter|explain", re.IGNORECASE)),
    (
        "welcome",
        re.compile(r"^\s*(مرحبا|أهلا|اهلا|السلام|هلا|hi|hello|hey|start|ابدأ)\s*", re.IGNORECASE),
    ),
)


def _blocked_result(text: str) -> IntentResult | None:
    guard = guard_inbound(text)
    if guard.allowed:
        return None
    reasons: list[str] = []
    if guard.secret_scan.found:
        reasons.append("secrets_in_chat")
        reasons.extend(guard.secret_scan.kinds)
    if guard.unsafe_scan.blocked:
        reasons.extend(guard.unsafe_scan.reasons)
    return IntentResult(
        intent="blocked_unsafe",
        confidence=1.0,
        matched=reasons,
        requires_human=guard.secret_scan.found,  # secrets attempt → human review
        blocked_reasons=list(guard.doctrine_violations) or reasons,
        raw_text=text,
    )


def route_button(button_id: str) -> IntentResult:
    """Map a structured WhatsApp button id to an intent."""
    bid = (button_id or "").strip()
    if not bid:
        return IntentResult(intent="unknown", confidence=0.0, raw_text=bid)

    if ":" in bid:
        ns, _, rest = bid.partition(":")
        if ns == "menu" and rest in _MENU_INTENTS:
            return IntentResult(intent=rest, confidence=1.0, matched=[bid], raw_text=bid)  # type: ignore[arg-type]
        if ns == "asmt":
            if rest == "start":
                return IntentResult(
                    intent="assessment_start", confidence=1.0, matched=[bid], raw_text=bid
                )
            return IntentResult(
                intent="assessment_answer", confidence=1.0, matched=[bid], raw_text=bid
            )
        if ns == "card":
            action = bid.rsplit(":", 1)[-1]
            mapping: dict[str, ClientIntent] = {
                "approve": "approve",
                "reject": "reject",
                "edit": "edit",
                "simplify": "simplify",
            }
            return IntentResult(
                intent=mapping.get(action, "unknown"), confidence=1.0, matched=[bid], raw_text=bid
            )
        if ns == "perm":
            action = bid.rsplit(":", 1)[-1]
            intent: ClientIntent = (
                "permission_grant" if action in {"grant", "approve", "yes"} else "permission_deny"
            )
            return IntentResult(intent=intent, confidence=1.0, matched=[bid], raw_text=bid)
        if ns == "rec":
            mapping2: dict[str, ClientIntent] = {
                "proposal": "request_proposal",
                "book_call": "book_call",
                "start": "assessment_start",
                "simplify": "simplify",
            }
            return IntentResult(
                intent=mapping2.get(rest, "unknown"), confidence=1.0, matched=[bid], raw_text=bid
            )
        if ns == "handoff":
            return IntentResult(intent="human_handoff", confidence=1.0, matched=[bid], raw_text=bid)
        if ns == "support":
            if rest == "human":
                return IntentResult(
                    intent="human_handoff", confidence=1.0, matched=[bid], raw_text=bid
                )
            return IntentResult(intent="support", confidence=1.0, matched=[bid], raw_text=bid)

    # bare token that equals a menu intent
    if bid in _MENU_INTENTS:
        return IntentResult(intent=bid, confidence=1.0, matched=[bid], raw_text=bid)  # type: ignore[arg-type]
    return IntentResult(intent="unknown", confidence=0.0, raw_text=bid)


def route_text(text: str) -> IntentResult:
    """Classify free text — guard first, then keywords, then unknown."""
    blocked = _blocked_result(text)
    if blocked is not None:
        return blocked
    t = (text or "").strip()
    if not t:
        return IntentResult(intent="welcome", confidence=0.5, raw_text=t)
    for intent, pat in _KEYWORDS:
        if pat.search(t):
            return IntentResult(
                intent=intent, confidence=0.8, matched=[pat.pattern[:30]], raw_text=t
            )
    return IntentResult(intent="unknown", confidence=0.0, raw_text=t)


def classify(*, text: str = "", button_id: str = "") -> IntentResult:
    """Unified entry — prefer a structured button, else classify free text."""
    if button_id:
        return route_button(button_id)
    return route_text(text)


__all__ = ["classify", "route_button", "route_text"]
