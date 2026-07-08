"""Message generation — builds channel-specific drafts for a scored target.

Every message is pain-hypothesis-based, permission-first, has a clear CTA, uses
the canonical founder email, and never claims guaranteed results. Draft-only —
nothing is sent.
"""

from __future__ import annotations

from typing import Any

from dealix.conversation_engine import company_brain
from dealix.conversation_engine.channel_adapter import (
    CALL,
    EMAIL,
    LINKEDIN,
    WHATSAPP,
)

CTA_AR = "هل يناسب أرسل لكم ملخص صفحة واحدة بدون التزام؟"
CTA_EN = "Would it be useful if I send a one-page snapshot, no commitment?"


def _pain(target: dict[str, Any]) -> str:
    return (
        target.get("pain_hypothesis_ar")
        or "غالبًا بعض الفرص تضيع بسبب المتابعة أو ترتيب العملاء."
    ).strip()


def _company(target: dict[str, Any]) -> str:
    return (target.get("company") or "فريقكم").strip()


def _contact(target: dict[str, Any]) -> str:
    return (target.get("contact_name") or "").strip()


def build_email(target: dict[str, Any], offer: dict[str, Any]) -> dict[str, Any]:
    company = _company(target)
    name = _contact(target) or "there"
    pain = _pain(target)
    offer_name = offer.get("name_en") or offer.get("name_ar") or "a short pilot"
    email = company_brain.founder_email()

    short = (
        f"Hi {name}, I'm Sami from Dealix in Riyadh. I help B2B teams turn "
        f"scattered leads, WhatsApp threads, and follow-ups into a daily revenue "
        f"command queue. For {company}, the likely opportunity is that "
        f"follow-up may be leaking. {CTA_EN}"
    )
    detailed = (
        f"Hi {name},\n\n"
        f"I'm Sami from Dealix in Riyadh. I help B2B teams turn scattered leads, "
        f"WhatsApp conversations, and follow-ups into a daily revenue command queue.\n\n"
        f"For {company}, the likely opportunity is:\n{pain}\n\n"
        f"I can prepare a simple one-page snapshot showing:\n"
        f"1. where follow-up may be leaking,\n"
        f"2. who should be contacted next,\n"
        f"3. what message should be sent,\n"
        f"4. what proof should be tracked.\n\n"
        f"No system replacement needed. It can start as a small pilot "
        f"({offer_name}). We measure the improvement — we do not promise revenue.\n\n"
        f"{CTA_EN}\n\n"
        f"{company_brain.founder_signature('en')}"
    )

    return {
        "subject": f"Quick revenue follow-up snapshot for {company}",
        "short_version": short,
        "detailed_version": detailed,
        "followup_1": (
            f"Hi {name}, following up on the one-page snapshot for {company}. "
            f"Happy to keep it to a 7-day pilot if that's easier. Should I send it over?"
        ),
        "followup_2": (
            f"Hi {name}, last note from me for now — if follow-up isn't the priority "
            f"right now, no problem. If it is, the snapshot takes me a short time to prepare. "
            f"Just reply and I'll send it."
        ),
        "objection_response": (
            "We don't guarantee revenue — that wouldn't be honest. What we do is show "
            "where opportunities leak and measure the improvement during a small pilot."
        ),
        "cta": CTA_EN,
        "risk_flags": _risk_flags(EMAIL),
        "from_email": email,
    }


def build_whatsapp(target: dict[str, Any], offer: dict[str, Any]) -> dict[str, Any]:
    company = _company(target)
    name = _contact(target) or "الفاضل"
    pain = _pain(target)

    opening = (
        f"السلام عليكم {name}،\n"
        f"أنا سامي من Dealix. أشتغل على نظام يساعد الشركات ترتب فرص المبيعات والمتابعة "
        f"وتطلع تقرير يومي واضح: من نتابع، ماذا نقول، وما الخطوة التالية."
    )
    short_value = (
        f"لاحظت أن عند {company} احتمال تضيع بعض الفرص بسبب المتابعة أو ترتيب العملاء. "
        f"أقدر أجهز لكم صفحة واحدة توضح أين ممكن تزيدون التحويل بدون تغيير نظامكم الحالي."
    )

    return {
        "opening_message": opening,
        "short_value_message": short_value,
        "permission_cta": CTA_AR,
        "followup": (
            f"مرحباً {name}، فقط أتابع بخصوص ملخص الصفحة الواحدة لـ{company}. "
            f"لو ما يناسب الآن ولا يهمّني، وإذا يناسب أرسله لك."
        ),
        "objection_response": (
            "ما نضمن زيادة إيراد — هذا غير مهني. نثبت أين تضيع الفرص ونقيس التحسن خلال pilot صغير."
        ),
        "pain_context_ar": pain,
        "risk_flags": _risk_flags(WHATSAPP),
        "cold_send_forbidden": True,
        "note_ar": "warm فقط — لا يُرسل إلا بعد إذن أو علاقة سابقة، وبعد اعتماد المؤسس.",
    }


def build_linkedin(target: dict[str, Any], offer: dict[str, Any]) -> dict[str, Any]:
    company = _company(target)
    name = _contact(target) or "there"

    return {
        "connection_note": (
            f"Hi {name}, I work with Saudi B2B teams on turning scattered follow-up "
            f"into a daily revenue command queue. Would love to connect."
        ),
        "dm_after_acceptance": (
            f"Thanks for connecting, {name}. For teams like {company}, the common gap "
            f"is follow-up leaking after leads come in. I can share a one-page snapshot "
            f"on where that might be happening — no commitment. Useful?"
        ),
        "value_followup": (
            "Quick note: the snapshot shows who to contact next, what to say, and what "
            "to measure. We measure improvement during a pilot — we don't promise revenue."
        ),
        "founder_post_draft": (
            "Most Saudi B2B teams don't have a lead problem — they have a follow-up "
            "problem. Leads come in, WhatsApp threads pile up, and the best opportunities "
            "go cold. At Dealix we turn that into one daily command queue: who to follow "
            "up, what to say, what to prove. Draft-first, founder approves every message."
        ),
        "risk_flags": _risk_flags(LINKEDIN) + ["no scraping", "no automation", "manual DM only"],
    }


def build_call_script(target: dict[str, Any], offer: dict[str, Any]) -> dict[str, Any]:
    company = _company(target)
    offer_name = offer.get("name_ar") or offer.get("name_en") or "سبرنت صغير"

    return {
        "opening": (
            f"السلام عليكم، معك سامي من Dealix. أشتغل مع شركات B2B سعودية على تنظيم "
            f"المتابعة والفرص. عندك دقيقتين؟"
        ),
        "discovery_questions": [
            "كم lead أو استفسار يوصلكم أسبوعيًا تقريبًا؟",
            "كيف تتابعونهم حاليًا — واتساب، إكسل، CRM؟",
            "وش أكثر شيء يضيع أو ينسى في المتابعة؟",
        ],
        "pain_confirmation": (
            f"إذًا التحدي عند {company} هو أن بعض الفرص تضيع بسبب ترتيب المتابعة، صح؟"
        ),
        "value_pitch": (
            f"نقدر نجهز لكم تقرير يومي واضح: من نتابع، ماذا نقول، وما الخطوة. نبدأ بـ"
            f"«{offer_name}» يثبت القيمة، وكل رسالة تعتمدها أنت قبل أي إرسال."
        ),
        "objection_handling": (
            "لو السعر أو الوقت عائق، نبدأ بأصغر نطاق. ولا نعد بنتيجة — نقيس التحسن."
        ),
        "close_next_step": (
            "هل يناسب أجهز لك ملخص صفحة واحدة هذا الأسبوع وتراجعه؟"
        ),
        "risk_flags": _risk_flags(CALL) + ["no auto-dial", "founder places call manually"],
    }


def _risk_flags(channel: str) -> list[str]:
    flags = ["draft_only", "approval_required", f"channel:{channel}"]
    if channel == WHATSAPP:
        flags.append("warm_only_no_cold")
    return flags


def build_all_channels(target: dict[str, Any], offer: dict[str, Any]) -> dict[str, Any]:
    return {
        EMAIL: build_email(target, offer),
        WHATSAPP: build_whatsapp(target, offer),
        LINKEDIN: build_linkedin(target, offer),
        CALL: build_call_script(target, offer),
    }
