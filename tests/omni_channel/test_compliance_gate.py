"""Tests for ComplianceGate — forbidden patterns, channel-specific rules, risk levels."""
from __future__ import annotations

import pytest

from auto_client_acquisition.omni_channel_os.compliance_gate import (
    CHANNEL_RISK,
    FORBIDDEN_CHANNEL_ACTIONS,
    FORBIDDEN_TEXT_PATTERNS,
    ComplianceGate,
)
from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    ChannelAsset,
    ChannelType,
    Company,
    GCCCountry,
    Language,
    RiskLevel,
    Sector,
)


@pytest.fixture
def gate() -> ComplianceGate:
    return ComplianceGate()


def _company(sector: Sector = Sector.legal) -> Company:
    return Company(name="Test Co", sector=sector, country=GCCCountry.KSA)


def _asset(
    channel: ChannelType = ChannelType.email,
    body: str = "Hello, I'd like to introduce our AI workflow diagnostic service.",
    cta: str = "Get your free diagnostic",
    is_auto_sendable: bool = False,
    **kwargs,
) -> ChannelAsset:
    return ChannelAsset(
        company_id="abc123",
        asset_type=AssetType.email_draft,
        channel=channel,
        language=Language.english,
        body=body,
        cta=cta,
        is_auto_sendable=is_auto_sendable,
        **kwargs,
    )


class TestComplianceGate:
    def test_no_auto_send_flag(self) -> None:
        assert ComplianceGate._NO_AUTO_SEND is True

    def test_clean_email_passes(self, gate: ComplianceGate) -> None:
        asset = _asset()
        is_compliant, violations = gate.check(asset, _company())
        assert is_compliant
        assert violations == []

    def test_cold_whatsapp_blast_in_body_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(body="We will run a cold whatsapp blast to reach prospects")
        is_compliant, violations = gate.check(asset, _company())
        assert not is_compliant
        assert any("cold whatsapp blast" in v for v in violations)

    def test_linkedin_automation_in_body_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(
            channel=ChannelType.linkedin,
            body="Use linkedin automation tool to send mass DMs",
        )
        is_compliant, violations = gate.check(asset, _company())
        assert not is_compliant

    def test_linkedin_auto_sendable_flag_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(channel=ChannelType.linkedin, is_auto_sendable=True)
        is_compliant, violations = gate.check(asset, _company())
        assert not is_compliant
        assert "linkedin_auto_send_forbidden_tos" in violations

    def test_arabic_cold_whatsapp_in_body_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(body="سنرسل رسائل عبر واتساب بارد للجميع")
        is_compliant, violations = gate.check(asset, _company())
        assert not is_compliant

    def test_blast_campaign_pattern_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(body="Let us run a blast campaign for you")
        is_compliant, violations = gate.check(asset, _company())
        assert not is_compliant

    def test_mass_message_pattern_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(body="We will send a mass message to all contacts")
        is_compliant, violations = gate.check(asset, _company())
        assert not is_compliant

    def test_guaranteed_claim_high_sensitivity_sector_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(
            channel=ChannelType.email,
            body="We guarantee 200% ROI for your healthcare facility",
        )
        is_compliant, violations = gate.check(asset, _company(Sector.healthcare))
        assert not is_compliant
        assert "guaranteed_claim_high_sensitivity_sector" in violations

    def test_auto_sendable_true_for_whatsapp_optin(self, gate: ComplianceGate) -> None:
        asset = _asset(channel=ChannelType.whatsapp_optin)
        assert gate.is_auto_sendable("whatsapp_optin", asset) is True

    def test_auto_sendable_false_for_linkedin(self, gate: ComplianceGate) -> None:
        asset = _asset(channel=ChannelType.linkedin)
        assert gate.is_auto_sendable("linkedin", asset) is False

    def test_auto_sendable_false_for_email(self, gate: ComplianceGate) -> None:
        asset = _asset(channel=ChannelType.email)
        assert gate.is_auto_sendable("email", asset) is False

    def test_auto_sendable_true_for_meta_lead_ads(self, gate: ComplianceGate) -> None:
        asset = _asset(channel=ChannelType.meta_lead_ads)
        assert gate.is_auto_sendable("meta_lead_ads", asset) is True

    def test_get_risk_level_linkedin_is_high(self, gate: ComplianceGate) -> None:
        assert gate.get_risk_level("linkedin", "consulting") == RiskLevel.high

    def test_get_risk_level_webinar_is_low(self, gate: ComplianceGate) -> None:
        assert gate.get_risk_level("webinar", "consulting") == RiskLevel.low

    def test_get_risk_level_email_healthcare_escalates_to_high(self, gate: ComplianceGate) -> None:
        assert gate.get_risk_level("email", "healthcare") == RiskLevel.high

    def test_get_risk_level_email_consulting_is_medium(self, gate: ComplianceGate) -> None:
        assert gate.get_risk_level("email", "consulting") == RiskLevel.medium

    def test_check_text_content_clean_returns_empty(self, gate: ComplianceGate) -> None:
        violations = gate.check_text_content("Hello, how are you today?")
        assert violations == []

    def test_check_text_content_auto_send_flagged(self, gate: ComplianceGate) -> None:
        violations = gate.check_text_content("auto-send all emails tonight")
        assert any("auto-send" in v for v in violations)

    def test_forbidden_channel_actions_is_frozenset(self) -> None:
        assert isinstance(FORBIDDEN_CHANNEL_ACTIONS, frozenset)
        assert "cold_whatsapp_blast" in FORBIDDEN_CHANNEL_ACTIONS
        assert "linkedin_automation_tool" in FORBIDDEN_CHANNEL_ACTIONS

    def test_channel_risk_covers_all_15_channels(self) -> None:
        expected = {
            "email", "linkedin", "whatsapp_optin", "cold_whatsapp",
            "website_form", "phone_call", "partnership", "webinar",
            "procurement_portal", "community", "google_lead_form",
            "meta_lead_ads", "linkedin_lead_gen", "retargeting",
            "founder_brand", "seo_content",
        }
        assert expected.issubset(set(CHANNEL_RISK.keys()))

    def test_invalid_auto_sendable_flag_on_email_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(channel=ChannelType.email, is_auto_sendable=True)
        is_compliant, violations = gate.check(asset, _company())
        assert not is_compliant
        assert "auto_sendable_flag_invalid_for_channel" in violations
