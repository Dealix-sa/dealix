"""Unit tests for roi_calculator."""

import pytest

from auto_client_acquisition.value_os.roi_calculator import (
    PainMonetization,
    ProspectProfile,
    ROIProjection,
    ServiceTier,
    build_roi_summary,
    calculate_roi,
    monetize_pain,
    recommend_tier,
)


def _profile(**kwargs) -> ProspectProfile:
    defaults = dict(
        monthly_leads=40,
        current_close_rate_pct=20.0,
        avg_deal_sar=5000,
        wasted_follow_up_hrs_weekly=8,
        team_size=5,
        monthly_revenue_sar=80_000,
    )
    defaults.update(kwargs)
    return ProspectProfile(**defaults)


class TestMonetizePain:
    def test_returns_pain_monetization(self):
        result = monetize_pain(_profile())
        assert isinstance(result, PainMonetization)

    def test_total_is_sum_of_components(self):
        result = monetize_pain(_profile())
        expected = (
            result.monthly_lead_leak_sar
            + result.monthly_time_waste_sar
            + result.monthly_proof_gap_cost_sar
        )
        assert result.total_monthly_pain_sar == expected

    def test_annual_is_12x_monthly(self):
        result = monetize_pain(_profile())
        assert result.annual_pain_sar == result.total_monthly_pain_sar * 12

    def test_all_components_nonnegative(self):
        result = monetize_pain(_profile())
        assert result.monthly_lead_leak_sar >= 0
        assert result.monthly_time_waste_sar >= 0
        assert result.monthly_proof_gap_cost_sar >= 0

    def test_zero_leads_zero_lead_leak(self):
        result = monetize_pain(_profile(monthly_leads=0))
        assert result.monthly_lead_leak_sar == 0

    def test_zero_wasted_hrs_zero_time_waste(self):
        result = monetize_pain(_profile(wasted_follow_up_hrs_weekly=0))
        assert result.monthly_time_waste_sar == 0

    def test_zero_revenue_zero_proof_gap(self):
        result = monetize_pain(_profile(monthly_revenue_sar=0))
        assert result.monthly_proof_gap_cost_sar == 0


class TestCalculateROI:
    def test_returns_roi_projection(self):
        result = calculate_roi(_profile())
        assert isinstance(result, ROIProjection)

    def test_tier_value_matches(self):
        result = calculate_roi(_profile(), ServiceTier.SPRINT)
        assert result.service_tier == ServiceTier.SPRINT.value

    def test_investment_matches_tier_cost(self):
        result = calculate_roi(_profile(), ServiceTier.DIAGNOSTIC)
        assert result.investment_sar == 499

    def test_annual_is_12x_monthly_recovered(self):
        result = calculate_roi(_profile())
        assert result.annual_recovered_sar == result.monthly_recovered_sar * 12

    def test_roi_multiple_positive(self):
        result = calculate_roi(_profile(monthly_revenue_sar=200_000, monthly_leads=100))
        assert result.roi_multiple >= 0

    def test_payback_weeks_positive(self):
        result = calculate_roi(_profile())
        assert result.payback_weeks >= 1

    def test_narrative_ar_nonempty(self):
        result = calculate_roi(_profile())
        assert len(result.narrative_ar) > 0

    def test_narrative_en_nonempty(self):
        result = calculate_roi(_profile())
        assert len(result.narrative_en) > 0

    def test_close_rate_improvement_bounded(self):
        result = calculate_roi(_profile())
        assert 0 <= result.close_rate_improvement_pct <= 20

    @pytest.mark.parametrize("tier", list(ServiceTier))
    def test_all_tiers_compute(self, tier: ServiceTier):
        result = calculate_roi(_profile(), tier)
        assert result.investment_sar > 0


class TestRecommendTier:
    def test_large_company_gets_managed_ops(self):
        tier = recommend_tier(_profile(monthly_revenue_sar=300_000, team_size=25))
        assert tier == ServiceTier.MANAGED_OPS

    def test_mid_company_gets_sprint(self):
        tier = recommend_tier(_profile(monthly_revenue_sar=60_000, team_size=6))
        assert tier == ServiceTier.SPRINT

    def test_small_company_gets_diagnostic(self):
        tier = recommend_tier(_profile(monthly_revenue_sar=10_000, team_size=2))
        assert tier == ServiceTier.DIAGNOSTIC


class TestBuildROISummary:
    def test_has_all_keys(self):
        summary = build_roi_summary(_profile())
        assert "pain_monetization" in summary
        assert "recommended_tier" in summary
        assert "tiers" in summary

    def test_all_tiers_in_summary(self):
        summary = build_roi_summary(_profile())
        for tier in ServiceTier:
            assert tier.value in summary["tiers"]

    def test_recommended_tier_is_valid(self):
        summary = build_roi_summary(_profile())
        assert summary["recommended_tier"] in {t.value for t in ServiceTier}
