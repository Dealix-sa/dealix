"""Compliance gate — checks channel assets for policy violations before they enter the review queue."""
from __future__ import annotations

import logging

from auto_client_acquisition.omni_channel_os.schemas import (
    ChannelAsset,
    ChannelType,
    Company,
    RiskLevel,
    Sector,
)

log = logging.getLogger(__name__)

_NO_AUTO_SEND = True

FORBIDDEN_CHANNEL_ACTIONS = frozenset([
    "cold_whatsapp_blast",
    "linkedin_autobot_dm",
    "contact_form_blasting",
    "group_spam",
    "mass_sms_cold",
    "unsolicited_whatsapp_without_template",
    "linkedin_automation_tool",
    "browser_extension_linkedin_spam",
])

FORBIDDEN_TEXT_PATTERNS = (
    "cold whatsapp blast",
    "linkedin automation",
    "auto-send",
    "send automatically",
    "blast campaign",
    "mass message",
    "إرسال تلقائي بدون موافقة",
    "واتساب بارد",
)

CHANNEL_RISK: dict[str, str] = {
    "email": "medium",
    "linkedin": "high",
    "whatsapp_optin": "low",
    "cold_whatsapp": "high",
    "website_form": "medium",
    "phone_call": "medium",
    "partnership": "low",
    "webinar": "low",
    "procurement_portal": "low",
    "community": "medium",
    "google_lead_form": "low",
    "meta_lead_ads": "low",
    "linkedin_lead_gen": "low",
    "retargeting": "low",
    "founder_brand": "low",
    "seo_content": "low",
}

_HIGH_SENSITIVITY_SECTORS = {
    Sector.government_adjacent.value,
    Sector.healthcare.value,
    Sector.financial_services.value,
    Sector.legal.value,
}

_AUTO_SENDABLE_CHANNELS = frozenset({
    "whatsapp_optin",
    "lead_ad_followup",
    "webinar_followup",
    "google_lead_form",
    "meta_lead_ads",
    "linkedin_lead_gen",
})


class ComplianceGate:
    _NO_AUTO_SEND = True

    def check(self, asset: ChannelAsset, company: Company) -> tuple[bool, list[str]]:
        violations: list[str] = []
        channel_val = asset.channel.value if hasattr(asset.channel, "value") else str(asset.channel)

        if channel_val == ChannelType.linkedin.value:
            violations.extend(self.check_linkedin(asset))
        elif channel_val == ChannelType.whatsapp_optin.value:
            violations.extend(self.check_whatsapp(asset))
        elif channel_val == ChannelType.email.value:
            violations.extend(self.check_email(asset, company))
        elif channel_val == ChannelType.website_form.value:
            violations.extend(self.check_website_form(asset))

        violations.extend(self.check_text_content(asset.body))
        if asset.subject_or_hook:
            violations.extend(self.check_text_content(asset.subject_or_hook))
        if asset.cta:
            violations.extend(self.check_text_content(asset.cta))

        if asset.is_auto_sendable and not self.is_auto_sendable(channel_val, asset):
            violations.append("auto_sendable_flag_invalid_for_channel")

        is_compliant = len(violations) == 0
        if not is_compliant:
            log.warning(
                "compliance_gate.check_failed asset_id=%s channel=%s violations=%s",
                asset.asset_id,
                channel_val,
                violations,
            )
        return is_compliant, violations

    def check_linkedin(self, asset: ChannelAsset) -> list[str]:
        violations: list[str] = []
        if asset.is_auto_sendable:
            violations.append("linkedin_auto_send_forbidden_tos")
        text = (asset.body + " " + (asset.subject_or_hook or "")).lower()
        if "automation" in text and "linkedin" in text:
            violations.append("linkedin_automation_language_detected")
        return violations

    def check_whatsapp(self, asset: ChannelAsset) -> list[str]:
        violations: list[str] = []
        text = (asset.body + " " + (asset.subject_or_hook or "")).lower()
        if "واتساب بارد" in text or "cold whatsapp" in text:
            violations.append("cold_whatsapp_language_detected")
        return violations

    def check_email(self, asset: ChannelAsset, company: Company) -> list[str]:
        violations: list[str] = []
        text = asset.body.lower()
        if "blast" in text or "mass email" in text:
            violations.append("email_blast_language_detected")
        if company.sector.value in _HIGH_SENSITIVITY_SECTORS:
            if "guarantee" in text or "نضمن" in text:
                violations.append("guaranteed_claim_high_sensitivity_sector")
        return violations

    def check_website_form(self, asset: ChannelAsset) -> list[str]:
        violations: list[str] = []
        text = asset.body.lower()
        if "scraping" in text or "scrape" in text:
            violations.append("scraping_language_detected")
        return violations

    def check_text_content(self, text: str) -> list[str]:
        violations: list[str] = []
        lower = text.lower()
        for pattern in FORBIDDEN_TEXT_PATTERNS:
            if pattern.lower() in lower:
                violations.append(f"forbidden_pattern:{pattern}")
        return violations

    def get_risk_level(self, channel: str, sector: str) -> RiskLevel:
        base = CHANNEL_RISK.get(channel, "medium")
        if sector in _HIGH_SENSITIVITY_SECTORS and base == "medium":
            base = "high"
        mapping = {"low": RiskLevel.low, "medium": RiskLevel.medium, "high": RiskLevel.high}
        return mapping.get(base, RiskLevel.medium)

    def is_auto_sendable(self, channel: str, asset: ChannelAsset) -> bool:
        return channel in _AUTO_SENDABLE_CHANNELS


__all__ = [
    "CHANNEL_RISK",
    "FORBIDDEN_CHANNEL_ACTIONS",
    "FORBIDDEN_TEXT_PATTERNS",
    "ComplianceGate",
]
