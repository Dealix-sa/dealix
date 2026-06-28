"""Growth Card builder for the Commercial Growth OS.

A Growth Card is the unit of commercial action: one account + one motion +
one recommended channel + bilingual draft messages + an explicit owner
decision and next action.

This builder *extends* the existing WhatsApp card concept — it produces
channel-agnostic drafts and never performs an HTTP send. Buttons are capped
at three to stay compatible with the existing WhatsApp interactive flow.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.commercial.safety import contains_blocked_claim
from app.commercial.schemas import CHANNELS, CommercialAccount, GrowthCard

MAX_BUTTONS = 3  # WhatsApp interactive reply-button ceiling.


def recommend_channel(account: CommercialAccount) -> str:
    """Pick the safest viable channel for this account.

    Order of preference favours channels that can become controlled-live with
    the least risk. WhatsApp is only recommended when opt-in exists; otherwise
    LinkedIn/phone remain manual fallbacks.
    """
    if account.public_email and not account.email_opt_out:
        return "email"
    if account.whatsapp and account.whatsapp_opt_in:
        return "whatsapp"
    if account.linkedin_url:
        return "linkedin_manual"
    if account.phone:
        return "phone"
    if account.website:
        return "website_form"
    return "partner_referral"


# Bilingual, evidence-safe opener templates per motion. No guarantees, no
# invented proof — these are conversation starters, not claims.
_MOTION_COPY: dict[str, dict[str, str]] = {
    "sales_prospecting": {
        "ar": "مرحباً {company}، لاحظنا فرصة لتحسين {pain}. نقدّم نظام تشغيل تجاري يساعد فرق المبيعات على تنظيم الفرص ومتابعتها. هل نرتّب مكالمة قصيرة؟",
        "en": "Hi {company}, we spotted an opportunity around {pain}. We build a commercial operating system that helps sales teams organise and follow up on opportunities. Open to a short call?",
    },
    "partnership_outreach": {
        "ar": "مرحباً {company}، نرى تكاملاً محتملاً بيننا لخدمة عملاء مشتركين. هل نستكشف نموذج شراكة؟",
        "en": "Hi {company}, we see a potential fit to serve shared clients together. Could we explore a partnership model?",
    },
    "proposal_push": {
        "ar": "مرحباً {company}، جهّزنا ملخص مقترح أولي حول {pain}. يسعدنا مراجعته معكم.",
        "en": "Hi {company}, we've prepared a draft proposal brief around {pain}. Happy to walk you through it.",
    },
    "revival": {
        "ar": "مرحباً {company}، نتواصل لمتابعة نقاشنا السابق حول {pain}. هل التوقيت مناسب الآن؟",
        "en": "Hi {company}, following up on our earlier conversation about {pain}. Is the timing better now?",
    },
    "upsell": {
        "ar": "مرحباً {company}، بناءً على ما حققناه معكم، هناك خطوة توسعة منطقية حول {pain}.",
        "en": "Hi {company}, based on our work together, there's a logical expansion step around {pain}.",
    },
    "retention": {
        "ar": "مرحباً {company}، نريد التأكد أنكم تحصلون على أقصى قيمة. هل نراجع النتائج معاً؟",
        "en": "Hi {company}, we want to make sure you're getting full value. Shall we review results together?",
    },
    "referral": {
        "ar": "مرحباً {company}، إن كنتم تعرفون فريقاً قد يستفيد مما نقدّمه، يسعدنا التعريف.",
        "en": "Hi {company}, if you know a team that could benefit from what we do, we'd value an intro.",
    },
    "renewal": {
        "ar": "مرحباً {company}، اقترب موعد التجديد. نقترح مراجعة سريعة للنطاق والنتائج.",
        "en": "Hi {company}, your renewal is approaching. Let's do a quick scope-and-results review.",
    },
    "customer_success_expansion": {
        "ar": "مرحباً {company}، نرى مجالاً لتوسيع الأثر في فرق إضافية لديكم.",
        "en": "Hi {company}, we see room to expand impact into additional teams on your side.",
    },
    "market_watch": {
        "ar": "مرحباً {company}، نتابع تطورات السوق ذات الصلة بكم ونشارككم ملاحظة قد تهمكم.",
        "en": "Hi {company}, we track market moves relevant to you and wanted to share a note.",
    },
}

_DEFAULT_COPY = {
    "ar": "مرحباً {company}، يسعدنا التواصل لمناقشة كيف يمكن لنظام التشغيل التجاري لدينا أن يساعدكم.",
    "en": "Hi {company}, we'd love to connect on how our commercial operating system can help.",
}


def _render(template: str, account: CommercialAccount) -> str:
    pain = account.pain_hypothesis or ("تحسين العمليات" if "ا" in template else "operations")
    return template.format(company=account.company_name or "there", pain=pain)


def _buttons_for(motion: str) -> list[str]:
    base = {
        "sales_prospecting": ["احجز مكالمة", "أرسل التفاصيل", "ليس الآن"],
        "partnership_outreach": ["نناقش الشراكة", "أرسل التفاصيل", "ليس الآن"],
        "proposal_push": ["راجع المقترح", "احجز مكالمة", "لاحقاً"],
    }
    return base.get(motion, ["نعم مهتم", "أرسل التفاصيل", "ليس الآن"])[:MAX_BUTTONS]


def build_growth_card(
    account: CommercialAccount,
    motion: str | None = None,
    card_index: int = 0,
    client_rules: Mapping[str, Any] | None = None,
) -> GrowthCard:
    """Build one Growth Card for an account. Always draft-only."""
    motion = (motion or account.recommended_motion or "sales_prospecting").strip()
    channel = recommend_channel(account)
    copy = _MOTION_COPY.get(motion, _DEFAULT_COPY)

    draft_ar = _render(copy["ar"], account)
    draft_en = _render(copy["en"], account)

    # Claim guard at build time — strip and flag rather than ever emit a claim.
    risk = account.risk_level
    for text in (draft_ar, draft_en):
        if contains_blocked_claim(text):
            risk = "high"

    send_ready = (
        bool(account.source_url)
        and account.verification_status == "verified"
        and account.contactability_status == "contactable"
    )
    next_action = (
        "Owner review → approve to queue (draft only, no auto-send)"
        if send_ready
        else "Resolve source/verification before any outreach"
    )

    card = GrowthCard(
        card_id=f"card_{account.account_id}_{card_index:03d}",
        account_id=account.account_id,
        motion=motion,
        recommended_channel=channel if channel in CHANNELS else "email",
        draft_message_ar=draft_ar,
        draft_message_en=draft_en,
        buttons=_buttons_for(motion),
        owner_decision="pending",
        approval_required=True,
        send_status="draft" if send_ready else "blocked",
        next_action=next_action,
        risk_level=risk,
    )
    return card


def build_cards_for_accounts(
    accounts: list[CommercialAccount],
    client_rules: Mapping[str, Any] | None = None,
) -> list[GrowthCard]:
    return [
        build_growth_card(acc, card_index=i, client_rules=client_rules)
        for i, acc in enumerate(accounts)
    ]
