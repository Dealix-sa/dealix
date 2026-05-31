"""Unit tests for api/routers/partner_referral.py"""
from __future__ import annotations

import pytest

from fastapi import HTTPException

from api.routers.partner_referral import (
    _PARTNER_TIERS,
    _PARTNER_ONBOARDING_STEPS,
    _REFERRAL_COMMISSION_RULES,
    _VALID_PARTNER_TIERS,
    ReferralEarningsInput,
    _calculate_referral_earnings,
    router,
)


def _make_input(**overrides) -> ReferralEarningsInput:
    data = dict(
        partner_tier="silver",
        referrals_closed=5,
        avg_deal_value_sar=20_000.0,
    )
    data.update(overrides)
    return ReferralEarningsInput(**data)


# ---------------------------------------------------------------------------
# Static data: partner tiers
# ---------------------------------------------------------------------------


class TestPartnerTiers:
    def test_has_three_tiers(self):
        assert len(_PARTNER_TIERS) == 3

    def test_tier_ids_are_correct(self):
        ids = {t["tier_id"] for t in _PARTNER_TIERS}
        assert ids == {"associate", "silver", "gold"}

    def test_all_have_tier_name_en(self):
        for t in _PARTNER_TIERS:
            assert t.get("tier_name_en"), f"{t.get('tier_id')} missing tier_name_en"

    def test_all_have_tier_name_ar(self):
        for t in _PARTNER_TIERS:
            assert t.get("tier_name_ar"), f"{t.get('tier_id')} missing tier_name_ar"

    def test_all_have_positive_referral_fee_pct(self):
        for t in _PARTNER_TIERS:
            assert t["referral_fee_pct"] > 0, f"{t.get('tier_id')} referral_fee_pct must be > 0"

    def test_associate_fee_pct(self):
        associate = next(t for t in _PARTNER_TIERS if t["tier_id"] == "associate")
        assert associate["referral_fee_pct"] == 5.0

    def test_silver_fee_pct(self):
        silver = next(t for t in _PARTNER_TIERS if t["tier_id"] == "silver")
        assert silver["referral_fee_pct"] == 10.0

    def test_gold_fee_pct(self):
        gold = next(t for t in _PARTNER_TIERS if t["tier_id"] == "gold")
        assert gold["referral_fee_pct"] == 15.0

    def test_all_have_requirements_en(self):
        for t in _PARTNER_TIERS:
            reqs = t.get("requirements_en", [])
            assert len(reqs) == 2, f"{t.get('tier_id')} must have 2 requirements_en"

    def test_all_have_requirements_ar(self):
        for t in _PARTNER_TIERS:
            reqs = t.get("requirements_ar", [])
            assert len(reqs) == 2, f"{t.get('tier_id')} must have 2 requirements_ar"

    def test_all_have_annual_quota_sar(self):
        for t in _PARTNER_TIERS:
            assert t.get("annual_quota_sar", 0) > 0

    def test_associate_quota(self):
        associate = next(t for t in _PARTNER_TIERS if t["tier_id"] == "associate")
        assert associate["annual_quota_sar"] == 50_000

    def test_silver_quota(self):
        silver = next(t for t in _PARTNER_TIERS if t["tier_id"] == "silver")
        assert silver["annual_quota_sar"] == 150_000

    def test_gold_quota(self):
        gold = next(t for t in _PARTNER_TIERS if t["tier_id"] == "gold")
        assert gold["annual_quota_sar"] == 500_000


# ---------------------------------------------------------------------------
# Static data: partner onboarding steps
# ---------------------------------------------------------------------------


class TestPartnerOnboardingSteps:
    def test_has_five_steps(self):
        assert len(_PARTNER_ONBOARDING_STEPS) == 5

    def test_ordered_1_to_5(self):
        orders = [s["order"] for s in _PARTNER_ONBOARDING_STEPS]
        assert orders == [1, 2, 3, 4, 5]

    def test_all_have_step_en(self):
        for s in _PARTNER_ONBOARDING_STEPS:
            assert s.get("step_en"), f"Step {s.get('order')} missing step_en"

    def test_all_have_step_ar(self):
        for s in _PARTNER_ONBOARDING_STEPS:
            assert s.get("step_ar"), f"Step {s.get('order')} missing step_ar"

    def test_all_have_duration_days(self):
        for s in _PARTNER_ONBOARDING_STEPS:
            assert isinstance(s.get("duration_days"), int)
            assert s["duration_days"] > 0

    def test_all_have_owner_en(self):
        for s in _PARTNER_ONBOARDING_STEPS:
            assert s.get("owner_en"), f"Step {s.get('order')} missing owner_en"

    def test_application_review_duration(self):
        step = next(s for s in _PARTNER_ONBOARDING_STEPS if s["order"] == 1)
        assert step["duration_days"] == 3

    def test_agreement_signing_duration(self):
        step = next(s for s in _PARTNER_ONBOARDING_STEPS if s["order"] == 2)
        assert step["duration_days"] == 2

    def test_portal_access_duration(self):
        step = next(s for s in _PARTNER_ONBOARDING_STEPS if s["order"] == 3)
        assert step["duration_days"] == 1

    def test_training_duration(self):
        step = next(s for s in _PARTNER_ONBOARDING_STEPS if s["order"] == 4)
        assert step["duration_days"] == 5

    def test_first_referral_target_duration(self):
        step = next(s for s in _PARTNER_ONBOARDING_STEPS if s["order"] == 5)
        assert step["duration_days"] == 30


# ---------------------------------------------------------------------------
# Static data: referral commission rules
# ---------------------------------------------------------------------------


class TestReferralCommissionRules:
    def test_has_four_rules(self):
        assert len(_REFERRAL_COMMISSION_RULES) == 4

    def test_all_have_rule_en(self):
        for r in _REFERRAL_COMMISSION_RULES:
            assert r.get("rule_en"), "Rule missing rule_en"

    def test_all_have_rule_ar(self):
        for r in _REFERRAL_COMMISSION_RULES:
            assert r.get("rule_ar"), "Rule missing rule_ar"


# ---------------------------------------------------------------------------
# _calculate_referral_earnings
# ---------------------------------------------------------------------------


class TestCalculateReferralEarnings:
    def test_returns_dict(self):
        result = _calculate_referral_earnings(_make_input())
        assert isinstance(result, dict)

    def test_has_gross_revenue_generated_sar(self):
        result = _calculate_referral_earnings(_make_input())
        assert "gross_revenue_generated_sar" in result

    def test_has_commission_rate_pct(self):
        result = _calculate_referral_earnings(_make_input())
        assert "commission_rate_pct" in result

    def test_has_estimated_commission_sar(self):
        result = _calculate_referral_earnings(_make_input())
        assert "estimated_commission_sar" in result

    def test_has_quota_attainment_pct(self):
        result = _calculate_referral_earnings(_make_input())
        assert "quota_attainment_pct" in result

    def test_has_next_tier_upgrade_eligible(self):
        result = _calculate_referral_earnings(_make_input())
        assert "next_tier_upgrade_eligible" in result

    def test_has_partner_tier(self):
        result = _calculate_referral_earnings(_make_input(partner_tier="silver"))
        assert result["partner_tier"] == "silver"

    def test_gross_revenue_calculation(self):
        result = _calculate_referral_earnings(_make_input(referrals_closed=5, avg_deal_value_sar=20_000.0))
        assert result["gross_revenue_generated_sar"] == pytest.approx(100_000.0)

    def test_estimated_commission_equals_gross_times_rate(self):
        result = _calculate_referral_earnings(_make_input(partner_tier="silver", referrals_closed=5, avg_deal_value_sar=20_000.0))
        expected = 100_000.0 * (10.0 / 100)
        assert result["estimated_commission_sar"] == pytest.approx(expected)

    def test_associate_commission_rate(self):
        result = _calculate_referral_earnings(_make_input(partner_tier="associate"))
        assert result["commission_rate_pct"] == pytest.approx(5.0)

    def test_gold_commission_rate(self):
        result = _calculate_referral_earnings(_make_input(partner_tier="gold"))
        assert result["commission_rate_pct"] == pytest.approx(15.0)

    def test_quota_attainment_pct_partial(self):
        # silver quota = 150_000; gross = 5 * 20_000 = 100_000 → 66.67%
        result = _calculate_referral_earnings(_make_input(partner_tier="silver", referrals_closed=5, avg_deal_value_sar=20_000.0))
        assert result["quota_attainment_pct"] == pytest.approx(100_000 / 150_000 * 100)

    def test_quota_attainment_pct_caps_at_100(self):
        # Generate revenue well above quota
        result = _calculate_referral_earnings(_make_input(partner_tier="associate", referrals_closed=100, avg_deal_value_sar=10_000.0))
        assert result["quota_attainment_pct"] == pytest.approx(100.0)

    def test_zero_referrals_gives_zero_earnings(self):
        result = _calculate_referral_earnings(_make_input(referrals_closed=0, avg_deal_value_sar=50_000.0))
        assert result["gross_revenue_generated_sar"] == pytest.approx(0.0)
        assert result["estimated_commission_sar"] == pytest.approx(0.0)

    def test_next_tier_upgrade_eligible_when_quota_met_silver(self):
        # silver quota = 150_000; generate 200_000
        result = _calculate_referral_earnings(_make_input(partner_tier="silver", referrals_closed=10, avg_deal_value_sar=20_000.0))
        assert result["quota_attainment_pct"] == pytest.approx(100.0)
        assert result["next_tier_upgrade_eligible"] is True

    def test_next_tier_upgrade_eligible_when_quota_met_associate(self):
        # associate quota = 50_000; generate 60_000
        result = _calculate_referral_earnings(_make_input(partner_tier="associate", referrals_closed=3, avg_deal_value_sar=20_000.0))
        assert result["next_tier_upgrade_eligible"] is True

    def test_next_tier_upgrade_not_eligible_below_quota(self):
        # silver quota = 150_000; gross = 100_000 → 66.7% attainment
        result = _calculate_referral_earnings(_make_input(partner_tier="silver", referrals_closed=5, avg_deal_value_sar=20_000.0))
        assert result["next_tier_upgrade_eligible"] is False

    def test_gold_never_upgrade_eligible(self):
        # gold quota = 500_000; generate 600_000 — still no upgrade
        result = _calculate_referral_earnings(_make_input(partner_tier="gold", referrals_closed=100, avg_deal_value_sar=10_000.0))
        assert result["next_tier_upgrade_eligible"] is False

    def test_invalid_tier_raises_http_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _calculate_referral_earnings(_make_input(partner_tier="platinum"))
        assert exc_info.value.status_code == 422

    def test_governance_decision_approval_first(self):
        result = _calculate_referral_earnings(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"


# ---------------------------------------------------------------------------
# Valid partner tiers set
# ---------------------------------------------------------------------------


class TestValidPartnerTiers:
    def test_contains_associate(self):
        assert "associate" in _VALID_PARTNER_TIERS

    def test_contains_silver(self):
        assert "silver" in _VALID_PARTNER_TIERS

    def test_contains_gold(self):
        assert "gold" in _VALID_PARTNER_TIERS

    def test_size_is_three(self):
        assert len(_VALID_PARTNER_TIERS) == 3


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/partner-referral"

    def test_tags_contain_sales(self):
        assert "Sales" in router.tags
