"""Tests for BuyerMapper."""
from __future__ import annotations

import pytest

from auto_client_acquisition.omni_channel_os.buyer_mapper import BuyerMapper
from auto_client_acquisition.omni_channel_os.schemas import (
    Company,
    CompanySize,
    GCCCountry,
    Language,
    Sector,
)


@pytest.fixture()
def mapper() -> BuyerMapper:
    return BuyerMapper()


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


class TestBuyerMapper:
    def test_legal_sector_returns_legal_persona(self, mapper: BuyerMapper) -> None:
        company = _company(sector=Sector.legal)
        persona = mapper.map(company)
        assert persona.sector == "legal"

    def test_fm_sector_returns_fm_persona(self, mapper: BuyerMapper) -> None:
        company = _company(sector=Sector.facilities_management)
        persona = mapper.map(company)
        assert persona.sector == "facilities_management"

    def test_unknown_sector_returns_default_persona(self, mapper: BuyerMapper) -> None:
        company = _company(sector=Sector.other)
        persona = mapper.map(company)
        assert persona.sector == "other"
        assert len(persona.typical_titles) > 0

    def test_arabic_company_gets_arabic_language_preference(self, mapper: BuyerMapper) -> None:
        company = _company(sector=Sector.legal, language=Language.arabic)
        persona = mapper.map(company)
        assert persona.language_preference == Language.arabic

    def test_international_company_gets_english_preference(self, mapper: BuyerMapper) -> None:
        company = _company(sector=Sector.international_company)
        persona = mapper.map(company)
        assert persona.language_preference == Language.english

    def test_get_offer_fit_returns_string_for_all_known_sectors(self, mapper: BuyerMapper) -> None:
        for sector_val in [
            "legal",
            "facilities_management",
            "consulting",
            "real_estate",
            "healthcare",
            "education_training",
            "international_company",
            "local_sme",
            "government_adjacent",
            "technology",
            "manufacturing",
            "retail",
            "financial_services",
        ]:
            result = mapper.get_offer_fit(sector_val)
            assert isinstance(result, str) and len(result) > 0

    def test_get_offer_fit_returns_default_for_unknown(self, mapper: BuyerMapper) -> None:
        result = mapper.get_offer_fit("totally_unknown_sector_xyz")
        assert isinstance(result, str) and len(result) > 0

    def test_map_returns_non_empty_pain_points(self, mapper: BuyerMapper) -> None:
        company = _company(sector=Sector.healthcare)
        persona = mapper.map(company)
        assert len(persona.pain_points) > 0

    def test_map_returns_preferred_channels(self, mapper: BuyerMapper) -> None:
        company = _company(sector=Sector.consulting)
        persona = mapper.map(company)
        assert len(persona.preferred_channels) > 0

    def test_get_angle_returns_string(self, mapper: BuyerMapper) -> None:
        company = _company(sector=Sector.legal)
        angle = mapper.get_angle("legal", company)
        assert isinstance(angle, str) and len(angle) > 0
