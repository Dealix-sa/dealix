"""Routes each Company to its optimal channel mix based on sector, country, size, and language."""
from __future__ import annotations

import logging

from auto_client_acquisition.omni_channel_os.schemas import (
    AutomationLevel,
    ChannelDecision,
    ChannelType,
    Company,
    CompanySize,
    GCCCountry,
    Language,
    Sector,
)

log = logging.getLogger(__name__)

_NO_AUTO_SEND = True

AUTOMATION_LEVELS: dict[str, AutomationLevel] = {
    "inbound_website": AutomationLevel.full,
    "lead_ad_followup": AutomationLevel.full,
    "whatsapp_optin": AutomationLevel.full,
    "webinar_followup": AutomationLevel.full,
    "newsletter": AutomationLevel.full,
    "google_lead_form": AutomationLevel.full,
    "linkedin_lead_gen": AutomationLevel.full,
    "meta_lead_ads": AutomationLevel.full,
    "email": AutomationLevel.partial,
    "website_form": AutomationLevel.partial,
    "partner_intro": AutomationLevel.partial,
    "content_seo": AutomationLevel.partial,
    "linkedin": AutomationLevel.manual,
    "cold_whatsapp": AutomationLevel.manual,
    "phone_call": AutomationLevel.manual,
    "proposal_submission": AutomationLevel.manual,
    "procurement_portal": AutomationLevel.manual,
    "community_post": AutomationLevel.manual,
}

SEGMENT_ROUTES: dict[str, dict] = {
    "legal_local_arabic": {
        "primary": [ChannelType.website_form, ChannelType.email, ChannelType.linkedin],
        "secondary": [ChannelType.webinar, ChannelType.partnership],
        "avoid": ["cold_whatsapp_blast", "mass_linkedin_automation"],
    },
    "international_gcc": {
        "primary": [ChannelType.linkedin, ChannelType.email, ChannelType.linkedin_lead_gen],
        "secondary": [ChannelType.webinar, ChannelType.retargeting],
        "avoid": ["cold_whatsapp_blast"],
    },
    "local_sme": {
        "primary": [ChannelType.website_form, ChannelType.phone_call, ChannelType.meta_lead_ads],
        "secondary": [ChannelType.email, ChannelType.whatsapp_optin],
        "avoid": [],
    },
    "facilities_management": {
        "primary": [ChannelType.email, ChannelType.phone_call, ChannelType.linkedin],
        "secondary": [ChannelType.website_form, ChannelType.partnership],
        "avoid": [],
    },
    "government_related": {
        "primary": [ChannelType.partnership, ChannelType.email, ChannelType.procurement_portal],
        "secondary": [ChannelType.linkedin, ChannelType.webinar],
        "avoid": ["cold_whatsapp_blast", "cold_call"],
    },
    "healthcare_local": {
        "primary": [ChannelType.website_form, ChannelType.email, ChannelType.webinar],
        "secondary": [ChannelType.phone_call, ChannelType.linkedin],
        "avoid": [],
    },
    "consulting_professional": {
        "primary": [ChannelType.linkedin, ChannelType.email, ChannelType.webinar],
        "secondary": [ChannelType.partnership, ChannelType.retargeting],
        "avoid": [],
    },
    "real_estate": {
        "primary": [ChannelType.meta_lead_ads, ChannelType.website_form, ChannelType.phone_call],
        "secondary": [ChannelType.whatsapp_optin, ChannelType.retargeting],
        "avoid": [],
    },
    "technology_startup": {
        "primary": [ChannelType.linkedin, ChannelType.email, ChannelType.community],
        "secondary": [ChannelType.webinar, ChannelType.retargeting],
        "avoid": [],
    },
    "retail_ecommerce": {
        "primary": [ChannelType.meta_lead_ads, ChannelType.retargeting, ChannelType.email],
        "secondary": [ChannelType.website_form, ChannelType.google_lead_form],
        "avoid": [],
    },
    "financial_services": {
        "primary": [ChannelType.email, ChannelType.linkedin, ChannelType.webinar],
        "secondary": [ChannelType.partnership, ChannelType.website_form],
        "avoid": ["cold_whatsapp_blast"],
    },
    "default": {
        "primary": [ChannelType.email, ChannelType.website_form, ChannelType.linkedin],
        "secondary": [ChannelType.phone_call, ChannelType.webinar],
        "avoid": [],
    },
}

# Maps string avoid-channel tokens to ChannelType where a direct mapping exists.
_AVOID_TO_CHANNEL: dict[str, ChannelType] = {}


class ChannelRouter:
    _NO_AUTO_SEND = True

    def route(self, company: Company) -> ChannelDecision:
        segment = self.get_segment(company)
        route_cfg = SEGMENT_ROUTES.get(segment, SEGMENT_ROUTES["default"])
        primary: list[ChannelType] = list(route_cfg["primary"])
        secondary: list[ChannelType] = list(route_cfg["secondary"])

        avoid_channels: list[ChannelType] = []
        automation: dict[str, AutomationLevel] = {}
        for ch in primary + secondary:
            automation[ch.value] = self.get_automation_level(ch.value)

        rationale = (
            f"segment={segment} sector={company.sector.value} "
            f"country={company.country.value} size={company.company_size.value} "
            f"language={company.language.value}"
        )
        log.debug("channel_router.route company_id=%s segment=%s", company.id, segment)
        return ChannelDecision(
            company_id=company.id,
            segment=segment,
            primary_channels=primary,
            secondary_channels=secondary,
            avoid_channels=avoid_channels,
            automation_levels=automation,
            rationale=rationale,
        )

    def get_segment(self, company: Company) -> str:
        sector = company.sector
        country = company.country
        size = company.company_size
        language = company.language

        if sector == Sector.government_adjacent:
            return "government_related"

        if sector == Sector.facilities_management:
            return "facilities_management"

        if sector == Sector.healthcare:
            return "healthcare_local"

        if sector in (Sector.consulting,):
            return "consulting_professional"

        if sector == Sector.legal:
            if language == Language.arabic:
                return "legal_local_arabic"
            return "consulting_professional"

        if sector == Sector.international_company:
            return "international_gcc"

        if sector == Sector.real_estate:
            return "real_estate"

        if sector == Sector.technology:
            if size in (CompanySize.micro, CompanySize.sme):
                return "technology_startup"
            return "consulting_professional"

        if sector == Sector.retail:
            return "retail_ecommerce"

        if sector == Sector.financial_services:
            return "financial_services"

        if sector == Sector.local_sme:
            return "local_sme"

        if sector == Sector.manufacturing:
            return "facilities_management"

        if sector == Sector.education_training:
            return "consulting_professional"

        if size in (CompanySize.micro, CompanySize.sme):
            if language == Language.arabic:
                return "local_sme"
        if country not in (GCCCountry.KSA,):
            return "international_gcc"

        return "default"

    def get_automation_level(self, channel: str) -> AutomationLevel:
        return AUTOMATION_LEVELS.get(channel, AutomationLevel.manual)

    def should_auto_send(self, channel: str) -> bool:
        return self.get_automation_level(channel) == AutomationLevel.full

    def get_primary_channel(self, company: Company) -> ChannelType:
        segment = self.get_segment(company)
        route_cfg = SEGMENT_ROUTES.get(segment, SEGMENT_ROUTES["default"])
        primary: list[ChannelType] = list(route_cfg["primary"])
        return primary[0] if primary else ChannelType.email

    def get_backup_channel(self, company: Company) -> ChannelType | None:
        segment = self.get_segment(company)
        route_cfg = SEGMENT_ROUTES.get(segment, SEGMENT_ROUTES["default"])
        secondary: list[ChannelType] = list(route_cfg["secondary"])
        return secondary[0] if secondary else None


__all__ = ["AUTOMATION_LEVELS", "SEGMENT_ROUTES", "ChannelRouter"]
