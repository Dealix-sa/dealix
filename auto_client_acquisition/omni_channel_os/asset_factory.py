"""Asset Factory — generates the full package of channel assets for a company brief."""
from __future__ import annotations

import logging
from dataclasses import dataclass

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


@dataclass
class OfferData:
    """Offer data passed into asset generation functions."""

    offer_name: str
    angle_ar: str
    angle_en: str
    lead_magnet_ar: str
    lead_magnet_en: str
    cta_ar: str
    cta_en: str
    tier: str


def _is_auto_sendable(asset_type: AssetType) -> bool:
    """Return True only for assets on opt-in / inbound-only channels."""
    _AUTO_SENDABLE_TYPES = {
        AssetType.whatsapp_optin_reply,
        AssetType.whatsapp_qualification,
        AssetType.lead_ad_followup,
    }
    return asset_type in _AUTO_SENDABLE_TYPES


def _build_body(
    template: str,
    company: Company,
    persona: BuyerPersona,
    offer: OfferData,
    language: Language,
) -> str:
    """Fill template placeholders with company/persona/offer data."""
    name = persona.typical_titles[0] if persona.typical_titles else "Decision Maker"
    pain = persona.pain_points[0] if persona.pain_points else "manual workflows"
    angle = offer.angle_ar if language == Language.arabic else offer.angle_en
    lead_magnet = offer.lead_magnet_ar if language == Language.arabic else offer.lead_magnet_en
    return (
        template
        .replace("[Company]", company.name)
        .replace("[Name]", name)
        .replace("[sector]", company.sector.value)
        .replace("[country]", company.country.value)
        .replace("[pain]", pain)
        .replace("[offer]", offer.offer_name)
        .replace("[angle]", angle)
        .replace("[lead_magnet]", lead_magnet)
    )


_ALL_CHANNELS = [
    "email",
    "linkedin",
    "whatsapp",
    "website_form",
    "call_script",
    "partnership",
    "webinar",
    "content",
    "founder",
    "proposal",
]


def _sector_to_partner_type(sector: str) -> str:
    """Map a company sector to the most relevant partner type."""
    _MAP: dict[str, str] = {
        "technology": "it_firm",
        "consulting": "consulting",
        "financial_services": "accounting",
        "legal": "legal_tech",
        "education_training": "training_company",
        "real_estate": "crm_implementer",
    }
    return _MAP.get(sector, "it_firm")


class AssetFactory:
    """Generates a full channel asset package for one company. All drafts require approval."""

    _NO_AUTO_SEND = True

    def __init__(self) -> None:
        from auto_client_acquisition.omni_channel_os.email_os import EmailOS
        from auto_client_acquisition.omni_channel_os.linkedin_os import LinkedInOS
        from auto_client_acquisition.omni_channel_os.whatsapp_os import WhatsAppOS
        from auto_client_acquisition.omni_channel_os.website_form_os import WebsiteFormOS
        from auto_client_acquisition.omni_channel_os.call_script_os import CallScriptOS
        from auto_client_acquisition.omni_channel_os.partnership_os import PartnershipOS
        from auto_client_acquisition.omni_channel_os.webinar_os import WebinarOS
        from auto_client_acquisition.omni_channel_os.content_engine import ContentEngine
        from auto_client_acquisition.omni_channel_os.founder_brand_os import FounderBrandOS
        from auto_client_acquisition.omni_channel_os.proposal_seed_os import ProposalSeedOS

        self._email_os = EmailOS()
        self._linkedin_os = LinkedInOS()
        self._whatsapp_os = WhatsAppOS()
        self._website_form_os = WebsiteFormOS()
        self._call_script_os = CallScriptOS()
        self._partnership_os = PartnershipOS()
        self._webinar_os = WebinarOS()
        self._content_engine = ContentEngine()
        self._founder_brand_os = FounderBrandOS()
        self._proposal_seed_os = ProposalSeedOS()

        # Public aliases (matching spec)
        self.linkedin = self._linkedin_os
        self.email = self._email_os
        self.whatsapp = self._whatsapp_os
        self.website_form = self._website_form_os
        self.call_script = self._call_script_os
        self.partnership = self._partnership_os
        self.webinar = self._webinar_os
        self.content = self._content_engine
        self.founder = self._founder_brand_os
        self.proposal = self._proposal_seed_os

    def generate(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: OfferData,
        channels: list[str],
    ) -> dict[str, ChannelAsset]:
        """Generate requested channel assets. Returns dict[asset_key -> ChannelAsset].

        Supported channel keys: email, linkedin, whatsapp, website_form, call_script,
        partnership, webinar, content, founder, proposal.
        """
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        assets: dict[str, ChannelAsset] = {}

        for channel in channels:
            try:
                new = self._dispatch_channel(company, persona, offer, channel)
                assets.update(new)
            except Exception as exc:
                log.warning(
                    "asset_factory.generate_channel_failed channel=%s company_id=%s error=%s",
                    channel,
                    company.id,
                    exc,
                )
        return assets

    def generate_full_package(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: OfferData,
    ) -> dict[str, ChannelAsset]:
        """Generate all applicable channel assets for the company. Returns {asset_key: ChannelAsset}."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        log.debug(
            "asset_factory.generate_full_package company=%s sector=%s",
            company.name,
            company.sector.value,
        )
        return self.generate(company, persona, offer, channels=_ALL_CHANNELS)

    # ------------------------------------------------------------------
    # Channel dispatcher
    # ------------------------------------------------------------------

    def _dispatch_channel(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: OfferData,
        channel: str,
    ) -> dict[str, ChannelAsset]:
        if channel == "email":
            asset = self._email_os.draft(company, persona, offer)
            asset.approval_status = "approval_required"
            return {AssetType.email_draft.value: asset}

        if channel == "linkedin":
            pkg = self._linkedin_os.draft_package(company, persona, offer)
            for asset in pkg.values():
                asset.approval_status = "approval_required"
            return pkg

        if channel == "whatsapp":
            lead = {
                "name": persona.typical_titles[0] if persona.typical_titles else "[Name]",
                "company_id": company.id,
            }
            wa_asset = self._whatsapp_os.welcome_message(lead, company.language)
            return {AssetType.whatsapp_optin_reply.value: wa_asset}

        if channel == "website_form":
            asset = self._website_form_os.draft_message(company, persona, offer)
            return {AssetType.website_form_message.value: asset}

        if channel == "call_script":
            asset = self._call_script_os.generate_script(company, persona, offer)
            return {AssetType.call_script.value: asset}

        if channel == "partnership":
            asset = self._partnership_os.draft_intro(
                partner_company=company.name,
                partner_type=_sector_to_partner_type(company.sector.value),
                contact_name="[Name]",
                language=company.language,
            )
            return {AssetType.partner_intro.value: asset}

        if channel == "webinar":
            asset = self._webinar_os.invitation_message(
                sector=company.sector.value,
                company=company.name,
                name=persona.typical_titles[0] if persona.typical_titles else "[Name]",
                language=company.language,
            )
            return {AssetType.webinar_invite.value: asset}

        if channel == "content":
            posts = self._content_engine.daily_posts(n_ar=1, n_en=1)
            return {f"content_{i}": p for i, p in enumerate(posts)}

        if channel == "founder":
            pkg = self._founder_brand_os.daily_package()
            return {f"founder_{k}": v for k, v in pkg.items()}

        if channel == "proposal":
            asset = self._proposal_seed_os.generate_memo(company, persona, offer)
            return {AssetType.proposal_seed.value: asset}

        log.warning("asset_factory.unknown_channel channel=%s", channel)
        return {}

    def _generate_whatsapp_optin(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: OfferData,
    ) -> ChannelAsset:
        """Generate an opt-in WhatsApp reply asset (inbound only — auto-sendable)."""
        lang = company.language
        name = persona.typical_titles[0] if persona.typical_titles else "Decision Maker"
        if lang == Language.arabic:
            body = (
                f"السلام عليكم [Name]، شكراً للتواصل.\n"
                f"نبني {offer.offer_name} للشركات الخليجية.\n"
                f"حتى نرسل لكم المعلومات المناسبة، ما القطاع الذي تعملون فيه؟\n"
                f"{offer.lead_magnet_ar}"
            ).replace("[Name]", name)
            cta = offer.cta_ar
        else:
            body = (
                f"Hello [Name], thank you for reaching out.\n"
                f"We build {offer.offer_name} for GCC businesses.\n"
                f"To send you the most relevant information, what sector are you in?\n"
                f"{offer.lead_magnet_en}"
            ).replace("[Name]", name)
            cta = offer.cta_en

        return ChannelAsset(
            company_id=company.id,
            asset_type=AssetType.whatsapp_optin_reply,
            channel=ChannelType.whatsapp_optin,
            language=lang,
            body=body,
            cta=cta,
            is_auto_sendable=True,
            requires_founder_approval=False,
            risk_level=RiskLevel.low,
            approval_status="approval_required",
            sector=company.sector.value,
            country=company.country.value,
        )

    def _generate_website_form(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: OfferData,
    ) -> ChannelAsset:
        """Generate a website contact form message."""
        lang = company.language
        name = persona.typical_titles[0] if persona.typical_titles else "Decision Maker"
        pain = persona.pain_points[0] if persona.pain_points else "manual workflows"
        if lang == Language.arabic:
            body = (
                f"السلام عليكم،\n"
                f"نبني {offer.offer_name} لشركات قطاع {company.sector.value} في {company.country.value}.\n"
                f"لاحظنا أن تحديات مثل {pain} شائعة في هذا القطاع.\n"
                f"نقدم تشخيصاً مجانياً على workflow واحد لمدة 7 أيام.\n"
                f"{offer.lead_magnet_ar}\n"
                f"هل يناسبكم نحدد موعداً مدته 20 دقيقة؟"
            )
            cta = offer.cta_ar
        else:
            body = (
                f"Hi,\n"
                f"We build {offer.offer_name} for {company.sector.value} companies in {company.country.value}.\n"
                f"We noticed that challenges like {pain} are common in your sector.\n"
                f"We offer a free 7-day diagnostic on one workflow.\n"
                f"{offer.lead_magnet_en}\n"
                f"Would you be available for a 20-minute call?"
            )
            cta = offer.cta_en

        return ChannelAsset(
            company_id=company.id,
            asset_type=AssetType.website_form_message,
            channel=ChannelType.website_form,
            language=lang,
            body=body,
            cta=cta,
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.medium,
            approval_status="approval_required",
            sector=company.sector.value,
            country=company.country.value,
        )

    def _generate_call_script(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: OfferData,
    ) -> ChannelAsset:
        """Generate a phone call script."""
        lang = company.language
        name = persona.typical_titles[0] if persona.typical_titles else "Decision Maker"
        pain = persona.pain_points[0] if persona.pain_points else "manual workflows"
        if lang == Language.arabic:
            body = (
                f"[مقدمة]\n"
                f"السلام عليكم، معك Sami من Dealix، هل أتحدث مع {name} في {company.name}؟\n\n"
                f"[الهدف]\n"
                f"أتواصل لأن شركات مثل {company.name} في قطاع {company.sector.value} "
                f"كثيراً ما تواجه تحديات مثل {pain}.\n\n"
                f"[العرض]\n"
                f"نقدم {offer.offer_name} — {offer.angle_ar}\n"
                f"نبدأ بتشخيص مجاني لمدة 7 أيام على workflow واحد.\n\n"
                f"[السؤال]\n"
                f"هل يناسبكم 20 دقيقة هذا الأسبوع نرى كيف يطبق على عملياتكم؟\n\n"
                f"[المتابعة]\n"
                f"إذا لم يكن مناسباً الآن: متى يكون الوقت المناسب للتواصل مجدداً؟"
            )
            cta = offer.cta_ar
        else:
            body = (
                f"[Opening]\n"
                f"Hello, this is Sami from Dealix. Am I speaking with {name} at {company.name}?\n\n"
                f"[Purpose]\n"
                f"I'm reaching out because companies like {company.name} in {company.sector.value} "
                f"commonly face challenges like {pain}.\n\n"
                f"[Offer]\n"
                f"We provide {offer.offer_name} — {offer.angle_en}\n"
                f"We start with a free 7-day diagnostic on one workflow.\n\n"
                f"[Ask]\n"
                f"Would 20 minutes work this week to see how it applies to your operations?\n\n"
                f"[Follow-up]\n"
                f"If now isn't a good time: when would be a better time to reconnect?"
            )
            cta = offer.cta_en

        return ChannelAsset(
            company_id=company.id,
            asset_type=AssetType.call_script,
            channel=ChannelType.phone_call,
            language=lang,
            body=body,
            cta=cta,
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.medium,
            approval_status="approval_required",
            sector=company.sector.value,
            country=company.country.value,
        )


__all__ = ["AssetFactory", "OfferData"]
