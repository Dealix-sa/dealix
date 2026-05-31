"""LinkedIn OS — draft packages for connection notes, DMs, and follow-ups. MANUAL ONLY."""
from __future__ import annotations

import logging

from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    BuyerPersona,
    ChannelAsset,
    ChannelType,
    Company,
    Language,
    RiskLevel,
)

log = logging.getLogger(__name__)

_NO_AUTO_SEND = True
_LINKEDIN_TOS_NOTE = (
    "LinkedIn prohibits automated messaging tools. "
    "All drafts require human manual sending."
)


def _ar_connection_note(company_name: str, sector: str) -> str:
    return (
        f"السلام عليكم أستاذ [Name]، لاحظت أن {company_name} تعمل في مجال {sector}. "
        "أبني Dealix لأنظمة AI Workflow للشركات الخليجية. "
        "حبيت أضيفك لأن المجال قريب من عملياتكم."
    )


def _en_connection_note(company_name: str, sector: str) -> str:
    return (
        f"Hi [Name], I'm building Dealix — controlled AI workflow systems for GCC "
        f"operations-heavy companies. I noticed {company_name} is in {sector}, "
        "so I thought it would be relevant to connect."
    )


def _ar_dm_after_connect(company_name: str, sector: str) -> str:
    return (
        "السلام عليكم [Name]، شكراً للقبول.\n"
        "سريعاً: نبني أنظمة AI تحول workflows المتكررة مثل التقارير والمستندات "
        "والمتابعة إلى مسارات منظمة مع موافقة بشرية.\n"
        f"رأيت أن {company_name} في مجال {sector} — غالباً فيه workflows يمكن تحسينها.\n"
        "حابب أرسل لكم نبذة قصيرة عن كيفية تطبيقها؟ 10 دقائق بس."
    )


def _en_dm_after_connect(company_name: str, sector: str) -> str:
    return (
        "Hi [Name], thanks for connecting.\n"
        "Quick note: we build AI systems that turn repetitive workflows — reporting, "
        "documents, follow-up — into structured, human-approved processes.\n"
        f"I noticed {company_name} is in {sector}, which usually has workflows worth improving.\n"
        "Would it be useful if I sent a short overview? Just 10 minutes of reading."
    )


def _ar_followup_1(company_name: str) -> str:
    return (
        "السلام عليكم [Name]،\n"
        "أرسلت لكم رسالة قبل 5 أيام عن تحسين workflows في شركتكم.\n"
        f"فقط أتأكد أنها وصلت — إذا لم يكن الوقت مناسباً الآن يمكنكم إعلامي.\n"
        f"نبني في Dealix أنظمة AI Workflow لشركات مثل {company_name} — بدون مخاطرة على البيانات."
    )


def _en_followup_1(company_name: str) -> str:
    return (
        "Hi [Name],\n"
        "I sent you a note 5 days ago about improving workflows at your company.\n"
        "Just checking it reached you — if the timing is off, no problem at all.\n"
        f"We build AI workflow systems for companies like {company_name} — "
        "safely and without data risk."
    )


def _ar_followup_2(sector: str) -> str:
    return (
        "السلام عليكم [Name]،\n"
        "أشارككم هذا السؤال الذي يسأله كثيرون في مجال "
        f"{sector}:\n"
        "ما أصعب workflow تكرر يومياً ويستهلك أكثر وقت؟\n"
        "هذا السؤال يحدد أين يبدأ AI Workflow Audit.\n"
        "إذا أردتم نناقش هذا لدقيقتين — أنا متاح."
    )


def _en_followup_2(sector: str) -> str:
    return (
        "Hi [Name],\n"
        "Sharing a question that comes up often in the "
        f"{sector} space:\n"
        "Which repetitive workflow consumes the most time daily?\n"
        "That answer usually shows exactly where an AI Workflow Audit should start.\n"
        "Happy to discuss if you have two minutes."
    )


def _ar_comment_idea(sector: str) -> str:
    return (
        f"نقطة مهمة في مجال {sector} — "
        "الـ AI الأكثر فائدة ليس chatbot، بل workflow يعمل في الخلفية ويرفع القرار "
        "للمسؤول. هل رأيتم نماذج تطبيقية في السوق؟"
    )


def _en_comment_idea(sector: str) -> str:
    return (
        f"Important point for {sector} — "
        "the most useful AI is not a chatbot but a background workflow that "
        "escalates decisions to the right person. Have you seen working examples in this market?"
    )


def _ar_founder_intro(company_name: str, sector: str) -> str:
    return (
        "أبني Dealix — أنظمة AI Workflow للشركات الخليجية في قطاعات "
        "operations-heavy.\n\n"
        "هدفنا بسيط: تحويل المهام المتكررة مثل التقارير والمستندات والمتابعة "
        "إلى مسارات منظمة مع موافقة بشرية كاملة.\n\n"
        f"رأيت أن {company_name} في مجال {sector} وأعتقد أن هناك "
        "workflows تستحق النقاش.\n\n"
        "إذا كان الموضوع مناسباً أرحب بالتواصل."
    )


def _en_founder_intro(company_name: str, sector: str) -> str:
    return (
        "I'm building Dealix — controlled AI workflow systems for GCC "
        "operations-heavy companies.\n\n"
        "The goal: turn repetitive tasks like reporting, documentation, and follow-up "
        "into structured, human-approved workflows.\n\n"
        f"I noticed {company_name} is in {sector} and believe there are "
        "workflows worth discussing.\n\n"
        "Happy to connect if this is relevant."
    )


class LinkedInOS:
    """Generates LinkedIn draft packages. All assets are manual-only."""

    _NO_AUTO_SEND = True

    def draft_package(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: "OfferData",  # type: ignore[name-defined]  # noqa: F821
    ) -> dict[str, ChannelAsset]:
        """Return dict with keys: connection_note, dm_after_connect, followup_1,
        followup_2, comment_idea, founder_intro.
        """
        lang = company.language
        return {
            "linkedin_connection_note": self.connection_note(company, persona, offer, lang),
            "linkedin_dm": self.dm_after_connect(company, persona, offer, lang),
            "linkedin_followup_1": self.followup_1(company, persona, offer, lang),
            "linkedin_followup_2": self.followup_2(company, persona, offer, lang),
            "linkedin_comment_idea": self.comment_idea(company, persona, lang),
            "linkedin_founder_intro": self.founder_intro(company, persona, offer, lang),
        }

    def connection_note(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: object,
        language: Language,
    ) -> ChannelAsset:
        """Max 300 chars for LinkedIn connection note."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        sector = company.sector.value
        if language == Language.arabic:
            body = _ar_connection_note(company.name, sector)
        else:
            body = _en_connection_note(company.name, sector)
        # Trim to 280 chars for safety
        body = body[:280]
        return self._make_asset(
            company=company,
            asset_type=AssetType.linkedin_connection_note,
            language=language,
            subject_or_hook=f"Connection request — {company.name}",
            body=body,
            cta="Connect",
        )

    def dm_after_connect(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: object,
        language: Language,
    ) -> ChannelAsset:
        """First DM after connection is accepted."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        sector = company.sector.value
        if language == Language.arabic:
            body = _ar_dm_after_connect(company.name, sector)
        else:
            body = _en_dm_after_connect(company.name, sector)
        return self._make_asset(
            company=company,
            asset_type=AssetType.linkedin_dm,
            language=language,
            subject_or_hook="First DM after connection",
            body=body,
            cta="نبذة مختصرة" if language == Language.arabic else "Short overview",
        )

    def followup_1(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: object,
        language: Language,
    ) -> ChannelAsset:
        """Follow-up 1 — 5 days after DM if no reply."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        if language == Language.arabic:
            body = _ar_followup_1(company.name)
        else:
            body = _en_followup_1(company.name)
        return self._make_asset(
            company=company,
            asset_type=AssetType.linkedin_followup_1,
            language=language,
            subject_or_hook="Follow-up 1 (day 5)",
            body=body,
            cta="تأكيد الاستلام" if language == Language.arabic else "Confirm receipt",
        )

    def followup_2(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: object,
        language: Language,
    ) -> ChannelAsset:
        """Follow-up 2 — value add, not a push."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        sector = company.sector.value
        if language == Language.arabic:
            body = _ar_followup_2(sector)
        else:
            body = _en_followup_2(sector)
        return self._make_asset(
            company=company,
            asset_type=AssetType.linkedin_followup_2,
            language=language,
            subject_or_hook="Follow-up 2 — value add",
            body=body,
            cta="نقاش قصير" if language == Language.arabic else "Short discussion",
        )

    def comment_idea(
        self,
        company: Company,
        persona: BuyerPersona,
        language: Language,
    ) -> ChannelAsset:
        """Smart comment to post on decision-maker's latest post."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        sector = company.sector.value
        if language == Language.arabic:
            body = _ar_comment_idea(sector)
        else:
            body = _en_comment_idea(sector)
        return self._make_asset(
            company=company,
            asset_type=AssetType.linkedin_comment_idea,
            language=language,
            subject_or_hook="Comment idea for decision-maker post",
            body=body,
            cta="",
        )

    def founder_intro(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: object,
        language: Language,
    ) -> ChannelAsset:
        """Short founder-voice intro post."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        sector = company.sector.value
        if language == Language.arabic:
            body = _ar_founder_intro(company.name, sector)
        else:
            body = _en_founder_intro(company.name, sector)
        return self._make_asset(
            company=company,
            asset_type=AssetType.linkedin_post_ar
            if language == Language.arabic
            else AssetType.linkedin_post_en,
            language=language,
            subject_or_hook="Founder intro post",
            body=body,
            cta="تواصل" if language == Language.arabic else "Connect",
        )

    def _make_asset(
        self,
        company: Company,
        asset_type: AssetType,
        language: Language,
        subject_or_hook: str,
        body: str,
        cta: str,
    ) -> ChannelAsset:
        return ChannelAsset(
            company_id=company.id,
            asset_type=asset_type,
            channel=ChannelType.linkedin,
            language=language,
            subject_or_hook=subject_or_hook,
            body=body,
            cta=cta,
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.high,
            approval_status="approval_required",
            sector=company.sector.value,
            country=company.country.value,
        )


__all__ = ["LinkedInOS"]
