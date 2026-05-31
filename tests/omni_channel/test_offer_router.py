"""Tests for OfferRouter — all 13 sectors, bilingual angles, tier mapping."""
from __future__ import annotations

import pytest

from auto_client_acquisition.omni_channel_os.offer_router import OFFER_MAP, OfferRouter
from auto_client_acquisition.omni_channel_os.schemas import (
    Company,
    GCCCountry,
    Language,
    Sector,
)
from auto_client_acquisition.omni_channel_os.buyer_mapper import BuyerMapper


@pytest.fixture
def router() -> OfferRouter:
    return OfferRouter()


@pytest.fixture
def mapper() -> BuyerMapper:
    return BuyerMapper()


def _company(sector: Sector, language: Language = Language.arabic) -> Company:
    return Company(name="Test Co", sector=sector, country=GCCCountry.KSA, language=language)


REAL_SECTORS = [
    Sector.legal,
    Sector.facilities_management,
    Sector.consulting,
    Sector.real_estate,
    Sector.healthcare,
    Sector.education_training,
    Sector.international_company,
    Sector.local_sme,
    Sector.government_adjacent,
    Sector.technology,
    Sector.manufacturing,
    Sector.retail,
    Sector.financial_services,
]


class TestOfferRouter:
    def test_no_auto_send_flag(self) -> None:
        assert OfferRouter._NO_AUTO_SEND is True

    def test_all_13_sectors_in_offer_map(self) -> None:
        expected = {s.value for s in REAL_SECTORS}
        assert expected.issubset(set(OFFER_MAP.keys()))

    def test_route_returns_tuple_of_two_strings(self, router: OfferRouter, mapper: BuyerMapper) -> None:
        company = _company(Sector.legal)
        persona = mapper.map(company)
        offer, angle = router.route(company, persona)
        assert isinstance(offer, str) and len(offer) > 0
        assert isinstance(angle, str) and len(angle) > 0

    def test_route_arabic_language_returns_arabic_angle(self, router: OfferRouter, mapper: BuyerMapper) -> None:
        company = _company(Sector.legal, Language.arabic)
        persona = mapper.map(company)
        _, angle = router.route(company, persona)
        # Arabic angles contain Arabic characters
        assert any("؀" <= c <= "ۿ" for c in angle)

    def test_route_english_language_returns_english_angle(self, router: OfferRouter, mapper: BuyerMapper) -> None:
        company = _company(Sector.legal, Language.english)
        persona = mapper.map(company)
        _, angle = router.route(company, persona)
        # English angle should not be Arabic
        assert not all("؀" <= c <= "ۿ" for c in angle if c.strip())

    @pytest.mark.parametrize("sector", REAL_SECTORS)
    def test_all_sectors_route_successfully(
        self, router: OfferRouter, mapper: BuyerMapper, sector: Sector
    ) -> None:
        company = _company(sector)
        persona = mapper.map(company)
        offer, angle = router.route(company, persona)
        assert len(offer) > 0
        assert len(angle) > 0

    def test_get_lead_magnet_arabic(self, router: OfferRouter) -> None:
        result = router.get_lead_magnet("legal", Language.arabic)
        assert any("؀" <= c <= "ۿ" for c in result)

    def test_get_lead_magnet_english(self, router: OfferRouter) -> None:
        result = router.get_lead_magnet("legal", Language.english)
        assert isinstance(result, str) and len(result) > 0

    def test_get_lead_magnet_unknown_sector_falls_back_to_default(self, router: OfferRouter) -> None:
        result = router.get_lead_magnet("unknown_xyz", Language.english)
        assert isinstance(result, str) and len(result) > 0

    def test_get_cta_by_offer_name_arabic(self, router: OfferRouter) -> None:
        result = router.get_cta("Legal Knowledge OS", Language.arabic)
        assert any("؀" <= c <= "ۿ" for c in result)

    def test_get_cta_unknown_offer_falls_back(self, router: OfferRouter) -> None:
        result = router.get_cta("Nonexistent Offer", Language.english)
        assert isinstance(result, str) and len(result) > 0

    def test_get_tier_sprint_499_for_legal(self, router: OfferRouter) -> None:
        assert router.get_tier("legal") == "sprint_499"

    def test_get_tier_free_diagnostic_for_other(self, router: OfferRouter) -> None:
        assert router.get_tier("other") == "free_diagnostic"

    def test_get_tier_sprint_999_for_government_adjacent(self, router: OfferRouter) -> None:
        assert router.get_tier("government_adjacent") == "sprint_999"

    def test_get_full_offer_data_keys(self, router: OfferRouter) -> None:
        data = router.get_full_offer_data("legal", Language.english)
        assert set(data.keys()) == {"offer", "tier", "angle", "lead_magnet", "cta"}

    def test_get_full_offer_data_arabic_angle(self, router: OfferRouter) -> None:
        data = router.get_full_offer_data("legal", Language.arabic)
        assert any("؀" <= c <= "ۿ" for c in data["angle"])

    def test_offer_map_has_default_key(self) -> None:
        assert "default" in OFFER_MAP

    def test_all_offer_map_entries_have_required_keys(self) -> None:
        required = {"offer", "tier", "angle_ar", "angle_en", "lead_magnet_ar", "lead_magnet_en", "cta_ar", "cta_en"}
        for sector, data in OFFER_MAP.items():
            missing = required - set(data.keys())
            assert not missing, f"Sector '{sector}' missing keys: {missing}"
