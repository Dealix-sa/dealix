"""Tests for ComplianceGate."""
from __future__ import annotations

import pytest

from auto_client_acquisition.omni_channel_os.compliance_gate import ComplianceGate
from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    ChannelAsset,
    ChannelType,
    Company,
    CompanySize,
    GCCCountry,
    Language,
    RiskLevel,
    Sector,
)


@pytest.fixture()
def gate() -> ComplianceGate:
    return ComplianceGate()


def _company(**kwargs) -> Company:
    defaults = dict(
        name="TestCo",
        sector=Sector.other,
        country=GCCCountry.KSA,
        language=Language.arabic,
        company_size=CompanySize.sme,
    )
    defaults.update(kwargs)
    return Company(**defaults)


def _asset(
    channel: ChannelType = ChannelType.email,
    asset_type: AssetType = AssetType.email_draft,
    body: str = "Hello, this is a professional test message to check if you have time to connect.",
    is_auto_sendable: bool = False,
    language: Language = Language.arabic,
) -> ChannelAsset:
    return ChannelAsset(
        company_id="test_co",
        asset_type=asset_type,
        channel=channel,
        language=language,
        body=body,
        cta="Schedule a call",
        is_auto_sendable=is_auto_sendable,
        approval_status="approval_required",
    )


class TestComplianceGate:
    def test_whatsapp_optin_asset_passes(self, gate: ComplianceGate) -> None:
        asset = _asset(
            channel=ChannelType.whatsapp_optin,
            asset_type=AssetType.whatsapp_optin_reply,
            body="Thank you for reaching out. What sector are you in?",
            is_auto_sendable=True,
        )
        company = _company()
        compliant, violations = gate.check(asset, company)
        assert compliant is True
        assert violations == []

    def test_cold_whatsapp_language_in_body_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(
            channel=ChannelType.whatsapp_optin,
            asset_type=AssetType.whatsapp_optin_reply,
            body="We use cold whatsapp blast to reach prospects in bulk.",
        )
        company = _company()
        compliant, violations = gate.check(asset, company)
        assert compliant is False
        assert len(violations) > 0

    def test_linkedin_asset_requires_founder_approval(self, gate: ComplianceGate) -> None:
        asset = _asset(
            channel=ChannelType.linkedin,
            asset_type=AssetType.linkedin_connection_note,
            body="Looking forward to connecting with your team to explore opportunities.",
            is_auto_sendable=False,
        )
        company = _company()
        compliant, violations = gate.check(asset, company)
        assert compliant is True

    def test_linkedin_auto_send_flag_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(
            channel=ChannelType.linkedin,
            asset_type=AssetType.linkedin_dm,
            body="Hello, this is a professional outreach message.",
            is_auto_sendable=True,
        )
        company = _company()
        compliant, violations = gate.check(asset, company)
        assert compliant is False
        assert any("linkedin_auto_send" in v for v in violations)

    def test_email_with_blast_language_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(
            channel=ChannelType.email,
            asset_type=AssetType.email_draft,
            body="This is a mass email blast to all our prospects in the list.",
        )
        company = _company()
        compliant, violations = gate.check(asset, company)
        assert compliant is False

    def test_auto_sendable_only_for_optin_channels(self, gate: ComplianceGate) -> None:
        assert gate.is_auto_sendable("whatsapp_optin", _asset()) is True
        assert gate.is_auto_sendable("linkedin", _asset()) is False
        assert gate.is_auto_sendable("email", _asset()) is False

    def test_high_sensitivity_sector_raises_risk_level(self, gate: ComplianceGate) -> None:
        risk = gate.get_risk_level("email", "healthcare")
        assert risk == RiskLevel.high

    def test_low_risk_channel_low_risk_level(self, gate: ComplianceGate) -> None:
        risk = gate.get_risk_level("whatsapp_optin", "local_sme")
        assert risk == RiskLevel.low

    def test_forbidden_pattern_in_body_fails(self, gate: ComplianceGate) -> None:
        asset = _asset(
            body="We will run linkedin automation to send messages automatically.",
        )
        company = _company()
        compliant, violations = gate.check(asset, company)
        assert compliant is False
        assert len(violations) > 0

    def test_clean_email_passes(self, gate: ComplianceGate) -> None:
        asset = _asset(
            channel=ChannelType.email,
            body=(
                "Hello, we help facilities management companies automate "
                "SLA reporting workflows. Would you be open to a brief call?"
            ),
        )
        company = _company(sector=Sector.facilities_management)
        compliant, violations = gate.check(asset, company)
        assert compliant is True
