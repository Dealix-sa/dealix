"""
Unit tests for api/routers/partner_ecosystem.py

Tests cover:
- 5 partner categories with bilingual names and relevance
- 3 partnership tiers (referral, reseller, strategic)
- _build_partnership_brief: revenue estimate, next steps, governance
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.partner_ecosystem import (
    _PARTNERS,
    _PARTNERSHIP_TIERS,
    _build_partnership_brief,
    PartnershipEnquiryRequest,
    router,
)


class TestPartnerCategories:
    def test_five_categories(self):
        assert len(_PARTNERS) == 5

    def test_all_categories_bilingual(self):
        for k, v in _PARTNERS.items():
            assert v.get("category_en"), f"{k} missing category_en"
            assert v.get("category_ar"), f"{k} missing category_ar"

    def test_all_have_relevance(self):
        for k, v in _PARTNERS.items():
            assert v.get("relevance_en"), f"{k} missing relevance_en"

    def test_zatca_isv_present(self):
        assert "zatca_isv" in _PARTNERS

    def test_cloud_providers_present(self):
        assert "cloud_providers" in _PARTNERS

    def test_sama_fintechs_present(self):
        assert "sama_fintechs" in _PARTNERS

    def test_vision2030_accelerators_present(self):
        assert "vision2030_accelerators" in _PARTNERS

    def test_system_integrators_present(self):
        assert "system_integrators" in _PARTNERS

    def test_referral_opportunities_flagged(self):
        referral_categories = [k for k, v in _PARTNERS.items() if v.get("referral_opportunity")]
        assert len(referral_categories) >= 3

    def test_cloud_not_referral(self):
        # Cloud providers are infrastructure partners, not referral
        assert not _PARTNERS["cloud_providers"].get("referral_opportunity")

    def test_zatca_mentions_pdpl(self):
        relevance = _PARTNERS["zatca_isv"].get("dealix_pitch_en", "") + _PARTNERS["zatca_isv"].get("relevance_en", "")
        text = relevance.lower()
        assert "zatca" in text or "arabic" in text or "saudi" in text

    def test_all_have_partner_types(self):
        for k, v in _PARTNERS.items():
            assert len(v.get("partner_types", [])) >= 2, f"{k} needs ≥2 partner types"


class TestPartnershipTiers:
    def test_three_tiers(self):
        assert len(_PARTNERSHIP_TIERS) == 3

    def test_tiers_are_referral_reseller_strategic(self):
        tiers = {t["tier"] for t in _PARTNERSHIP_TIERS}
        assert tiers == {"referral", "reseller", "strategic"}

    def test_all_bilingual(self):
        for t in _PARTNERSHIP_TIERS:
            assert t.get("tier_ar"), f"{t['tier']} missing tier_ar"
            assert t.get("description_en"), f"{t['tier']} missing description_en"

    def test_referral_has_commission(self):
        referral = next(t for t in _PARTNERSHIP_TIERS if t["tier"] == "referral")
        assert referral["commission_pct"] == 15

    def test_reseller_has_higher_commission(self):
        reseller = next(t for t in _PARTNERSHIP_TIERS if t["tier"] == "reseller")
        assert reseller["commission_pct"] == 20

    def test_strategic_no_fixed_commission(self):
        strategic = next(t for t in _PARTNERSHIP_TIERS if t["tier"] == "strategic")
        assert strategic["commission_pct"] is None


class TestBuildPartnershipBrief:
    def _make_request(self, **overrides) -> PartnershipEnquiryRequest:
        data = dict(
            company_name="Tamara",
            partner_category="sama_fintechs",
            preferred_tier="referral",
            annual_client_base_size=500,
        )
        data.update(overrides)
        return PartnershipEnquiryRequest(**data)

    def test_company_name_in_result(self):
        result = _build_partnership_brief(self._make_request())
        assert result["company_name"] == "Tamara"

    def test_governance_approval_first(self):
        result = _build_partnership_brief(self._make_request())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_estimated_revenue_positive(self):
        result = _build_partnership_brief(self._make_request(annual_client_base_size=100))
        assert result["estimated_annual_referral_revenue_sar"] > 0

    def test_four_next_steps(self):
        result = _build_partnership_brief(self._make_request())
        assert len(result["next_steps_en"]) == 4

    def test_unknown_category_handled_gracefully(self):
        result = _build_partnership_brief(self._make_request(partner_category="unknown_xyz"))
        assert result["company_name"] == "Tamara"
        assert "unknown_xyz" in result["category_en"] or "not found" in result["partnership_value_en"].lower()

    def test_commission_in_result(self):
        result = _build_partnership_brief(self._make_request(preferred_tier="referral"))
        assert result["commission_pct"] == 15

    def test_larger_base_higher_revenue(self):
        small = _build_partnership_brief(self._make_request(annual_client_base_size=10))
        large = _build_partnership_brief(self._make_request(annual_client_base_size=500))
        assert large["estimated_annual_referral_revenue_sar"] > small["estimated_annual_referral_revenue_sar"]


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/partner-ecosystem"

    def test_router_tags(self):
        assert "Sales" in router.tags
