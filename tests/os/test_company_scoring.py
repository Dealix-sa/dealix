"""
Company Scoring Tests
=====================
Detailed tests for the company scoring system.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.os_runtime.company_scorer import (
    score_company,
    score_from_dict,
    CompanySignal,
    WEIGHTS,
)


class TestWeightsSum:
    def test_weights_sum_to_100(self):
        total = sum(WEIGHTS.values())
        assert total == 100, f"Weights must sum to 100, got {total}"

    def test_all_expected_factors_present(self):
        expected = {
            "operations_heavy",
            "maintenance_or_field_work",
            "repeated_reporting",
            "multi_branch_or_multi_site",
            "clear_buyer_title",
            "public_growth_signal",
            "likely_data_or_api",
            "founder_domain_fit",
        }
        assert set(WEIGHTS.keys()) == expected


class TestTierThresholds:
    def test_tier_a_at_85(self):
        signal = CompanySignal(
            company="Tier A Co",
            operations_heavy=True,       # 20
            maintenance_or_field_work=True,  # 20
            repeated_reporting=True,     # 15
            multi_branch_or_multi_site=True,  # 10
            clear_buyer_title=True,      # 10
            public_growth_signal=True,   # 10
        )
        result = score_company(signal)
        assert result["fit_score"] == 85
        assert result["tier"] == "A"

    def test_tier_b_at_70(self):
        signal = CompanySignal(
            company="Tier B Co",
            operations_heavy=True,       # 20
            maintenance_or_field_work=True,  # 20
            repeated_reporting=True,     # 15
            multi_branch_or_multi_site=True,  # 10
            clear_buyer_title=True,      # 10
        )
        result = score_company(signal)
        assert result["fit_score"] == 75
        assert result["tier"] == "B"

    def test_tier_c_at_55(self):
        signal = CompanySignal(
            company="Tier C Co",
            operations_heavy=True,       # 20
            maintenance_or_field_work=True,  # 20
            repeated_reporting=True,     # 15
        )
        result = score_company(signal)
        assert result["fit_score"] == 55
        assert result["tier"] == "C"

    def test_tier_d_below_55(self):
        signal = CompanySignal(
            company="Tier D Co",
            operations_heavy=True,       # 20
            repeated_reporting=True,     # 15
        )
        result = score_company(signal)
        assert result["fit_score"] == 35
        assert result["tier"] == "D"

    def test_score_0_is_tier_d(self):
        signal = CompanySignal(company="Zero Co")
        result = score_company(signal)
        assert result["fit_score"] == 0
        assert result["tier"] == "D"

    def test_score_100_is_tier_a(self):
        signal = CompanySignal(
            company="Perfect Co",
            operations_heavy=True,
            maintenance_or_field_work=True,
            repeated_reporting=True,
            multi_branch_or_multi_site=True,
            clear_buyer_title=True,
            public_growth_signal=True,
            likely_data_or_api=True,
            founder_domain_fit=True,
        )
        result = score_company(signal)
        assert result["fit_score"] == 100
        assert result["tier"] == "A"


class TestScoringOutput:
    def test_output_has_all_required_fields(self):
        signal = CompanySignal(company="Test Co", country="ksa", sector="legal")
        result = score_company(signal)
        required = ["company", "country", "sector", "fit_score", "tier", "recommended_action", "reasons", "governance_decision"]
        for field in required:
            assert field in result, f"Missing field: {field}"

    def test_reasons_only_include_true_factors(self):
        signal = CompanySignal(
            company="Test Co",
            operations_heavy=True,
            maintenance_or_field_work=False,
            repeated_reporting=True,
        )
        result = score_company(signal)
        factors = [r["factor"] for r in result["reasons"]]
        assert "operations_heavy" in factors
        assert "repeated_reporting" in factors
        assert "maintenance_or_field_work" not in factors

    def test_score_from_dict_handles_missing_fields(self):
        data = {"company": "Sparse Co"}
        result = score_from_dict(data)
        assert result["fit_score"] == 0
        assert result["company"] == "Sparse Co"

    def test_score_from_dict_boolean_coercion(self):
        data = {
            "company": "Bool Co",
            "operations_heavy": 1,  # int 1 → True (20 points)
            "maintenance_or_field_work": 1,  # int 1 → True (20 points)
        }
        result = score_from_dict(data)
        assert result["fit_score"] == 40  # Both coerced to True

    def test_score_from_dict_string_bool_rejected(self):
        data = {
            "company": "String Bool Co",
            "operations_heavy": "true",  # String not accepted — treated as False
        }
        result = score_from_dict(data)
        assert result["fit_score"] == 0  # String booleans not accepted

    def test_governance_decision_has_correct_module(self):
        signal = CompanySignal(company="Test Co")
        result = score_company(signal)
        assert result["governance_decision"]["module"] == "company_scorer"

    def test_governance_decision_has_tier(self):
        signal = CompanySignal(company="Test Co")
        result = score_company(signal)
        assert "tier" in result["governance_decision"]

    def test_country_and_sector_preserved(self):
        signal = CompanySignal(company="Test Co", country="uae", sector="legal")
        result = score_company(signal)
        assert result["country"] == "uae"
        assert result["sector"] == "legal"


class TestFMCompanyScenario:
    """End-to-end scenario: large FM company in KSA."""

    def test_fm_ksa_scores_tier_a(self):
        data = {
            "company": "Al Seha Facilities Management",
            "country": "ksa",
            "sector": "facilities_management",
            "operations_heavy": True,
            "maintenance_or_field_work": True,
            "repeated_reporting": True,
            "multi_branch_or_multi_site": True,
            "clear_buyer_title": True,
            "public_growth_signal": True,
            "likely_data_or_api": True,
            "founder_domain_fit": False,
        }
        result = score_from_dict(data)
        assert result["fit_score"] == 95
        assert result["tier"] == "A"
        assert result["recommended_action"] == "deep_research_custom_pack"
