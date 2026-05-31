"""Tests for ChannelRouter."""
from __future__ import annotations

import pytest

from auto_client_acquisition.omni_channel_os.channel_router import (
    AUTOMATION_LEVELS,
    ChannelRouter,
)
from auto_client_acquisition.omni_channel_os.schemas import (
    AutomationLevel,
    ChannelType,
    Company,
    CompanySize,
    GCCCountry,
    Language,
    Sector,
)


@pytest.fixture()
def router() -> ChannelRouter:
    return ChannelRouter()


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


class TestChannelRouterSegments:
    def test_legal_arabic_company_segment(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.legal, language=Language.arabic)
        assert router.get_segment(company) == "legal_local_arabic"

    def test_legal_arabic_primary_channel_is_website_form(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.legal, language=Language.arabic)
        decision = router.route(company)
        assert ChannelType.website_form in decision.primary_channels

    def test_fm_company_primary_channels(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.facilities_management)
        decision = router.route(company)
        assert ChannelType.email in decision.primary_channels or ChannelType.phone_call in decision.primary_channels

    def test_international_company_linkedin_primary(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.international_company)
        decision = router.route(company)
        assert ChannelType.linkedin in decision.primary_channels

    def test_government_adjacent_uses_referral_and_procurement(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.government_adjacent)
        decision = router.route(company)
        assert (
            ChannelType.partnership in decision.primary_channels
            or ChannelType.procurement_portal in decision.primary_channels
        )

    def test_small_sme_local_segment(self, router: ChannelRouter) -> None:
        company = _company(
            sector=Sector.local_sme,
            company_size=CompanySize.sme,
            language=Language.arabic,
        )
        assert router.get_segment(company) == "local_sme"

    def test_international_company_segment(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.international_company)
        assert router.get_segment(company) == "international_gcc"

    def test_automation_level_linkedin_is_manual(self, router: ChannelRouter) -> None:
        level = router.get_automation_level("linkedin")
        assert level == AutomationLevel.manual

    def test_automation_level_inbound_website_is_full(self, router: ChannelRouter) -> None:
        level = router.get_automation_level("inbound_website")
        assert level == AutomationLevel.full

    def test_automation_level_whatsapp_optin_is_full(self, router: ChannelRouter) -> None:
        level = router.get_automation_level("whatsapp_optin")
        assert level == AutomationLevel.full

    def test_route_returns_channel_decision(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.consulting)
        decision = router.route(company)
        assert decision.company_id == company.id
        assert len(decision.primary_channels) > 0

    def test_should_auto_send_false_for_linkedin(self, router: ChannelRouter) -> None:
        assert router.should_auto_send("linkedin") is False
