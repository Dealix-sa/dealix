"""Lead Capture OS — processes paid ad leads from Google, LinkedIn, and Meta."""
from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    ChannelAsset,
    ChannelType,
    InboundLead,
    Language,
    LeadCapture,
    RiskLevel,
)

log = logging.getLogger(__name__)
_NO_AUTO_SEND = False  # paid inbound can be auto-processed

LEAD_AD_FOLLOWUP_TEMPLATES: dict[str, dict[str, str]] = {
    "google_search": {
        "ar": (
            "السلام عليكم [Name]، وصلنا اهتمامكم بـ AI workflow. "
            "معك Sami من Dealix. "
            "نرسل لكم نبذة مختصرة عن كيفية تطبيقه في [sector]."
        ),
        "en": (
            "Hi [Name], we received your interest in AI workflow automation. "
            "This is Sami from Dealix. "
            "I'll send you a brief overview for [sector]."
        ),
    },
    "linkedin_lead_gen": {
        "ar": (
            "السلام عليكم [Name]، شكراً للاهتمام. "
            "نبني Dealix لأنظمة AI Workflow خليجية. "
            "أرسل لكم نبذة مختصرة تناسب [sector]."
        ),
        "en": (
            "Hi [Name], thanks for your interest. "
            "We build controlled AI workflow systems for GCC businesses. "
            "Sending you a relevant brief for [sector]."
        ),
    },
    "meta_lead_ads": {
        "ar": (
            "السلام عليكم [Name]، وصلنا طلبكم عبر الإعلان. "
            "Sami من Dealix. "
            "أرسل لكم مثال عملي على AI Workflow في [sector] خلال دقائق."
        ),
        "en": (
            "Hi [Name], we received your inquiry through our ad. "
            "Sami from Dealix. "
            "Sending you a practical AI workflow example for [sector] shortly."
        ),
    },
    "click_to_whatsapp": {
        "ar": (
            "السلام عليكم، معك Sami من Dealix. "
            "شكراً للتواصل. "
            "حتى أرسل لكم أفضل محتوى، ما القطاع الذي تعملون فيه؟"
        ),
        "en": (
            "Hello, this is Sami from Dealix. "
            "Thanks for reaching out. "
            "To send you the most relevant content, what sector are you in?"
        ),
    },
}

_SOURCE_CHANNEL_MAP: dict[str, ChannelType] = {
    "google_search": ChannelType.google_lead_form,
    "google_lead_form": ChannelType.google_lead_form,
    "linkedin_lead_gen": ChannelType.linkedin_lead_gen,
    "meta_lead_ads": ChannelType.meta_lead_ads,
    "click_to_whatsapp": ChannelType.whatsapp_optin,
}

_SOURCE_INTENT_BONUS: dict[str, float] = {
    "linkedin_lead_gen": 20.0,
    "google_search": 15.0,
    "meta_lead_ads": 10.0,
    "click_to_whatsapp": 8.0,
    "google_lead_form": 15.0,
}

RETARGETING_PIXEL_EVENTS = [
    "PageView",
    "Lead",
    "ViewContent",
    "InitiateCheckout",
    "CompleteRegistration",
]


class LeadCaptureOS:
    """Processes paid ad leads from Google, LinkedIn, and Meta."""

    _NO_AUTO_SEND = False  # inbound/paid leads can be auto-processed

    def process_lead(self, raw_lead: dict[str, Any], source: str) -> InboundLead:
        """Process a raw lead from any paid source into an InboundLead."""
        capture = self.enrich_from_form(raw_lead, source)
        score = self.score_intent(capture, source)
        offer_route = self._derive_offer(capture)

        inbound_lead = InboundLead(
            lead=capture,
            qualification_score=score,
            offer_route=offer_route,
        )
        log.info(
            "lead_capture_os.process_lead source=%s score=%.1f offer=%s",
            source,
            score,
            offer_route,
        )
        return inbound_lead

    def generate_followup(self, lead: InboundLead, source: str) -> ChannelAsset:
        """Generate an auto-followup message for the lead source."""
        lang = lead.lead.language_preference
        name = lead.lead.name or "there"
        sector = lead.lead.sector or "your sector"

        templates = LEAD_AD_FOLLOWUP_TEMPLATES.get(
            source, LEAD_AD_FOLLOWUP_TEMPLATES["meta_lead_ads"]
        )
        if lang == Language.arabic:
            body = templates["ar"].replace("[Name]", name).replace("[sector]", sector)
        else:
            body = templates["en"].replace("[Name]", name).replace("[sector]", sector)

        channel = _SOURCE_CHANNEL_MAP.get(source, ChannelType.google_lead_form)
        asset_type = AssetType.lead_ad_followup

        return ChannelAsset(
            company_id=lead.lead.lead_id,
            asset_type=asset_type,
            channel=channel,
            language=lang,
            body=body,
            cta="احصل على نبذة مختصرة" if lang == Language.arabic else "Get a brief overview",
            is_auto_sendable=True,
            requires_founder_approval=False,
            risk_level=RiskLevel.low,
            approval_status="approval_required",
            sector=lead.lead.sector or "",
            country=lead.lead.country,
        )

    def enrich_from_form(self, form_data: dict, source: str) -> LeadCapture:
        """Map raw form fields to a LeadCapture model."""
        lang_raw = (form_data.get("language") or form_data.get("language_preference") or "ar").lower()
        language = Language.arabic
        if "english" in lang_raw or lang_raw in ("en", "english"):
            language = Language.english
        elif "both" in lang_raw or "bilingual" in lang_raw:
            language = Language.bilingual

        return LeadCapture(
            source=source,
            name=form_data.get("name") or form_data.get("full_name") or "Unknown",
            email=form_data.get("email"),
            phone=form_data.get("phone") or form_data.get("phone_number"),
            company=form_data.get("company") or form_data.get("company_name"),
            sector=form_data.get("sector") or form_data.get("industry"),
            country=form_data.get("country") or "KSA",
            language_preference=language,
            campaign_name=form_data.get("campaign_name"),
            utm_source=form_data.get("utm_source") or source,
            utm_medium=form_data.get("utm_medium") or "paid",
            raw_form_data=form_data,
        )

    def score_intent(self, lead: LeadCapture, source: str) -> float:
        """Score lead intent 0-100 based on source, sector, form completeness."""
        score = 10.0  # baseline for being a paid lead

        # Source-based bonus
        score += _SOURCE_INTENT_BONUS.get(source, 5.0)

        # Form completeness
        if lead.email:
            score += 15.0
        if lead.phone:
            score += 15.0
        if lead.company:
            score += 10.0
        if lead.sector:
            score += 10.0

        # High-value sectors
        high_value = {
            "legal",
            "healthcare",
            "financial_services",
            "government_adjacent",
            "international_company",
        }
        if lead.sector and any(kw in (lead.sector or "").lower() for kw in high_value):
            score += 15.0

        return min(100.0, max(0.0, score))

    def _derive_offer(self, capture: LeadCapture) -> str:
        """Derive the offer name based on sector."""
        sector_offer: dict[str, str] = {
            "legal": "Legal Knowledge OS",
            "facilities_management": "Maintenance SLA AI",
            "consulting": "Consulting Ops AI",
            "real_estate": "Real Estate Lead OS",
            "healthcare": "Healthcare Admin AI",
            "education_training": "Training Ops AI",
            "international_company": "GCC Market Entry AI",
            "local_sme": "SME Growth OS",
            "government_adjacent": "Gov Procurement AI",
            "technology": "Tech Revenue OS",
            "manufacturing": "Manufacturing Ops AI",
            "retail": "Retail Intelligence OS",
            "financial_services": "FinOps AI",
        }
        if capture.sector:
            for key, offer in sector_offer.items():
                if key in (capture.sector or "").lower():
                    return offer
        return "Free AI Workflow Diagnostic"

    def get_retargeting_pixel_events(self) -> list[str]:
        """Return the standard pixel events to fire for retargeting."""
        return list(RETARGETING_PIXEL_EVENTS)


__all__ = ["LEAD_AD_FOLLOWUP_TEMPLATES", "LeadCaptureOS"]
