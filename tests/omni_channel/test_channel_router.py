"""Tests for ChannelRouter — segment classification and automation levels."""
from __future__ import annotations

import pytest

from auto_client_acquisition.omni_channel_os.channel_router import (
    AUTOMATION_LEVELS,
    SEGMENT_ROUTES,
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


@pytest.fixture
def router() -> ChannelRouter:
    return ChannelRouter()


def _company(**kwargs) -> Company:
    defaults = dict(name="Test Co", sector=Sector.other, country=GCCCountry.KSA)
    defaults.update(kwargs)
    return Company(**defaults)


class TestChannelRouter:
    def test_no_auto_send_flag(self) -> None:
        assert ChannelRouter._NO_AUTO_SEND is True

    def test_route_returns_channel_decision(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.legal)
        decision = router.route(company)
        assert decision.company_id == company.id
        assert len(decision.primary_channels) > 0

    def test_route_legal_arabic_segment(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.legal, language=Language.arabic)
        assert router.get_segment(company) == "legal_local_arabic"

    def test_route_legal_english_segment(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.legal, language=Language.english)
        assert router.get_segment(company) == "consulting_professional"

    def test_route_government_adjacent(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.government_adjacent)
        assert router.get_segment(company) == "government_related"

    def test_route_facilities_management(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.facilities_management)
        assert router.get_segment(company) == "facilities_management"

    def test_route_healthcare(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.healthcare)
        assert router.get_segment(company) == "healthcare_local"

    def test_route_international_company(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.international_company)
        assert router.get_segment(company) == "international_gcc"

    def test_route_local_sme(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.local_sme)
        assert router.get_segment(company) == "local_sme"

    def test_route_real_estate(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.real_estate)
        assert router.get_segment(company) == "real_estate"

    def test_route_technology_startup(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.technology, company_size=CompanySize.sme)
        assert router.get_segment(company) == "technology_startup"

    def test_route_technology_enterprise(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.technology, company_size=CompanySize.enterprise)
        assert router.get_segment(company) == "consulting_professional"

    def test_route_retail(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.retail)
        assert router.get_segment(company) == "retail_ecommerce"

    def test_route_financial_services(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.financial_services)
        assert router.get_segment(company) == "financial_services"

    def test_route_manufacturing_maps_to_facilities(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.manufacturing)
        assert router.get_segment(company) == "facilities_management"

    def test_linkedin_automation_level_is_manual(self, router: ChannelRouter) -> None:
        assert router.get_automation_level("linkedin") == AutomationLevel.manual

    def test_whatsapp_optin_automation_level_is_full(self, router: ChannelRouter) -> None:
        assert router.get_automation_level("whatsapp_optin") == AutomationLevel.full

    def test_email_automation_level_is_partial(self, router: ChannelRouter) -> None:
        assert router.get_automation_level("email") == AutomationLevel.partial

    def test_should_auto_send_false_for_linkedin(self, router: ChannelRouter) -> None:
        assert router.should_auto_send("linkedin") is False

    def test_should_auto_send_true_for_whatsapp_optin(self, router: ChannelRouter) -> None:
        assert router.should_auto_send("whatsapp_optin") is True

    def test_get_primary_channel_returns_channel_type(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.legal, language=Language.arabic)
        ch = router.get_primary_channel(company)
        assert isinstance(ch, ChannelType)

    def test_get_backup_channel_returns_channel_or_none(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.legal, language=Language.arabic)
        backup = router.get_backup_channel(company)
        assert backup is None or isinstance(backup, ChannelType)

    def test_automation_levels_dict_has_all_channels(self) -> None:
        expected_keys = {
            "inbound_website", "lead_ad_followup", "whatsapp_optin", "webinar_followup",
            "newsletter", "google_lead_form", "linkedin_lead_gen", "meta_lead_ads",
            "email", "website_form", "partner_intro", "content_seo",
            "linkedin", "cold_whatsapp", "phone_call", "proposal_submission",
            "procurement_portal", "community_post",
        }
        assert set(AUTOMATION_LEVELS.keys()) == expected_keys

    def test_route_decision_rationale_contains_segment(self, router: ChannelRouter) -> None:
        company = _company(sector=Sector.legal, language=Language.arabic)
        decision = router.route(company)
        assert "legal_local_arabic" in decision.rationale
