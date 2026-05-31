"""Tests for BuyerMapper — all 13 sectors covered, language-aware title selection."""
from __future__ import annotations

import pytest

from auto_client_acquisition.omni_channel_os.buyer_mapper import BuyerMapper
from auto_client_acquisition.omni_channel_os.schemas import (
    Company,
    GCCCountry,
    Language,
    Sector,
)


@pytest.fixture
def mapper() -> BuyerMapper:
    return BuyerMapper()


def _company(sector: Sector, language: Language = Language.arabic) -> Company:
    return Company(name="Acme", sector=sector, country=GCCCountry.KSA, language=language)


class TestBuyerMapper:
    def test_all_sectors_have_persona(self, mapper: BuyerMapper) -> None:
        non_other_sectors = [s for s in Sector if s != Sector.other]
        for sector in non_other_sectors:
            company = _company(sector)
            persona = mapper.map(company)
            assert persona is not None
            assert persona.sector != "" or sector == Sector.other

    def test_legal_persona_channels(self, mapper: BuyerMapper) -> None:
        from auto_client_acquisition.omni_channel_os.schemas import ChannelType
        persona = mapper.map(_company(Sector.legal))
        assert ChannelType.website_form in persona.preferred_channels

    def test_facilities_management_roi_first(self, mapper: BuyerMapper) -> None:
        persona = mapper.map(_company(Sector.facilities_management))
        assert persona.decision_style == "roi_first"

    def test_healthcare_compliance_first(self, mapper: BuyerMapper) -> None:
        persona = mapper.map(_company(Sector.healthcare))
        assert persona.decision_style == "compliance_first"

    def test_government_adjacent_compliance_first(self, mapper: BuyerMapper) -> None:
        persona = mapper.map(_company(Sector.government_adjacent))
        assert persona.decision_style == "compliance_first"

    def test_financial_services_compliance_first(self, mapper: BuyerMapper) -> None:
        persona = mapper.map(_company(Sector.financial_services))
        assert persona.decision_style == "compliance_first"

    def test_unknown_sector_returns_default(self, mapper: BuyerMapper) -> None:
        company = _company(Sector.other)
        persona = mapper.map(company)
        assert persona.sector == "other"

    def test_get_offer_fit_returns_string(self, mapper: BuyerMapper) -> None:
        result = mapper.get_offer_fit("legal")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_offer_fit_unknown_sector_returns_default(self, mapper: BuyerMapper) -> None:
        result = mapper.get_offer_fit("unknown_sector_xyz")
        assert "Diagnostic" in result

    def test_get_angle_returns_string(self, mapper: BuyerMapper) -> None:
        company = _company(Sector.consulting)
        angle = mapper.get_angle("consulting", company)
        assert isinstance(angle, str)
        assert len(angle) > 0

    def test_get_decision_maker_title_arabic(self, mapper: BuyerMapper) -> None:
        title = mapper.get_decision_maker_title("legal", Language.arabic)
        # Should contain Arabic characters
        assert any("؀" <= c <= "ۿ" for c in title)

    def test_get_decision_maker_title_english(self, mapper: BuyerMapper) -> None:
        title = mapper.get_decision_maker_title("legal", Language.english)
        assert isinstance(title, str)
        assert len(title) > 0

    def test_get_decision_maker_title_unknown_sector_arabic(self, mapper: BuyerMapper) -> None:
        title = mapper.get_decision_maker_title("unknown_xyz", Language.arabic)
        assert title == "مدير"

    def test_get_decision_maker_title_unknown_sector_english(self, mapper: BuyerMapper) -> None:
        title = mapper.get_decision_maker_title("unknown_xyz", Language.english)
        assert title == "Manager"

    def test_persona_map_has_all_13_real_sectors(self, mapper: BuyerMapper) -> None:
        expected = {
            "legal", "facilities_management", "consulting", "real_estate",
            "healthcare", "education_training", "international_company",
            "local_sme", "government_adjacent", "technology",
            "manufacturing", "retail", "financial_services",
        }
        assert set(mapper.PERSONA_MAP.keys()) == expected

    def test_all_personas_have_pain_points(self, mapper: BuyerMapper) -> None:
        for sector, persona in mapper.PERSONA_MAP.items():
            assert len(persona.pain_points) >= 2, f"{sector} has too few pain points"

    def test_all_personas_have_preferred_channels(self, mapper: BuyerMapper) -> None:
        for sector, persona in mapper.PERSONA_MAP.items():
            assert len(persona.preferred_channels) >= 2, f"{sector} has too few channels"
