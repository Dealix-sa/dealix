"""Unit tests for api/routers/contract_intelligence.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.contract_intelligence import (
    _CONTRACT_CLAUSES,
    _SAUDI_CONTRACT_REQUIREMENTS,
    _CONTRACT_RISK_MATRIX,
    _VALID_CONTRACT_STAGES,
    ContractReviewInput,
    _review_contract,
    router,
)


def _make_input(**overrides) -> ContractReviewInput:
    data = dict(
        contract_stage="review",
        deal_value_sar=50_000.0,
        includes_arabic_version=False,
        has_pdpl_clause=False,
        has_zatca_clause=False,
        payment_terms_days=30,
        auto_renewal_included=False,
    )
    data.update(overrides)
    return ContractReviewInput(**data)


def _make_perfect_input(**overrides) -> ContractReviewInput:
    data = dict(
        contract_stage="review",
        deal_value_sar=100_000.0,
        includes_arabic_version=True,
        has_pdpl_clause=True,
        has_zatca_clause=True,
        payment_terms_days=30,
        auto_renewal_included=False,
    )
    data.update(overrides)
    return ContractReviewInput(**data)


# ---------------------------------------------------------------------------
# Static data: _CONTRACT_CLAUSES
# ---------------------------------------------------------------------------


class TestContractClauses:
    def test_has_six_clauses(self):
        assert len(_CONTRACT_CLAUSES) == 6

    def test_all_have_clause_id(self):
        for c in _CONTRACT_CLAUSES:
            assert c.get("clause_id"), "Clause missing clause_id"

    def test_all_have_clause_name_en(self):
        for c in _CONTRACT_CLAUSES:
            assert c.get("clause_name_en"), f"{c.get('clause_id')} missing clause_name_en"

    def test_all_have_clause_name_ar(self):
        for c in _CONTRACT_CLAUSES:
            assert c.get("clause_name_ar"), f"{c.get('clause_id')} missing clause_name_ar"

    def test_all_have_risk_level(self):
        valid_levels = {"high", "medium", "low"}
        for c in _CONTRACT_CLAUSES:
            assert c.get("risk_level") in valid_levels, (
                f"{c.get('clause_id')} has invalid risk_level"
            )

    def test_all_have_negotiable_field(self):
        for c in _CONTRACT_CLAUSES:
            assert isinstance(c.get("negotiable"), bool), (
                f"{c.get('clause_id')} missing negotiable bool"
            )

    def test_all_have_dealix_standard_en(self):
        for c in _CONTRACT_CLAUSES:
            assert c.get("dealix_standard_en"), f"{c.get('clause_id')} missing dealix_standard_en"

    def test_all_have_dealix_standard_ar(self):
        for c in _CONTRACT_CLAUSES:
            assert c.get("dealix_standard_ar"), f"{c.get('clause_id')} missing dealix_standard_ar"

    def test_payment_terms_is_medium_risk(self):
        clause = next(c for c in _CONTRACT_CLAUSES if c["clause_id"] == "payment_terms")
        assert clause["risk_level"] == "medium"

    def test_payment_terms_is_negotiable(self):
        clause = next(c for c in _CONTRACT_CLAUSES if c["clause_id"] == "payment_terms")
        assert clause["negotiable"] is True

    def test_liability_cap_is_high_risk(self):
        clause = next(c for c in _CONTRACT_CLAUSES if c["clause_id"] == "liability_cap")
        assert clause["risk_level"] == "high"

    def test_liability_cap_is_negotiable(self):
        clause = next(c for c in _CONTRACT_CLAUSES if c["clause_id"] == "liability_cap")
        assert clause["negotiable"] is True

    def test_data_ownership_is_high_risk(self):
        clause = next(c for c in _CONTRACT_CLAUSES if c["clause_id"] == "data_ownership")
        assert clause["risk_level"] == "high"

    def test_data_ownership_is_not_negotiable(self):
        clause = next(c for c in _CONTRACT_CLAUSES if c["clause_id"] == "data_ownership")
        assert clause["negotiable"] is False

    def test_governing_law_is_low_risk(self):
        clause = next(c for c in _CONTRACT_CLAUSES if c["clause_id"] == "governing_law")
        assert clause["risk_level"] == "low"

    def test_governing_law_is_not_negotiable(self):
        clause = next(c for c in _CONTRACT_CLAUSES if c["clause_id"] == "governing_law")
        assert clause["negotiable"] is False


# ---------------------------------------------------------------------------
# Static data: _SAUDI_CONTRACT_REQUIREMENTS
# ---------------------------------------------------------------------------


class TestSaudiContractRequirements:
    def test_has_five_requirements(self):
        assert len(_SAUDI_CONTRACT_REQUIREMENTS) == 5

    def test_all_have_requirement_en(self):
        for r in _SAUDI_CONTRACT_REQUIREMENTS:
            assert r.get("requirement_en"), "Requirement missing requirement_en"

    def test_all_have_requirement_ar(self):
        for r in _SAUDI_CONTRACT_REQUIREMENTS:
            assert r.get("requirement_ar"), "Requirement missing requirement_ar"

    def test_all_have_mandatory_field(self):
        for r in _SAUDI_CONTRACT_REQUIREMENTS:
            assert isinstance(r.get("mandatory"), bool), "Requirement missing mandatory bool"

    def test_four_mandatory_requirements(self):
        mandatory = [r for r in _SAUDI_CONTRACT_REQUIREMENTS if r["mandatory"]]
        assert len(mandatory) == 4

    def test_one_non_mandatory_requirement(self):
        non_mandatory = [r for r in _SAUDI_CONTRACT_REQUIREMENTS if not r["mandatory"]]
        assert len(non_mandatory) == 1


# ---------------------------------------------------------------------------
# Static data: _CONTRACT_RISK_MATRIX
# ---------------------------------------------------------------------------


class TestContractRiskMatrix:
    def test_has_high_key(self):
        assert "high" in _CONTRACT_RISK_MATRIX

    def test_has_medium_key(self):
        assert "medium" in _CONTRACT_RISK_MATRIX

    def test_has_low_key(self):
        assert "low" in _CONTRACT_RISK_MATRIX

    def test_all_have_risk_label_en(self):
        for level, data in _CONTRACT_RISK_MATRIX.items():
            assert data.get("risk_label_en"), f"{level} missing risk_label_en"

    def test_all_have_risk_label_ar(self):
        for level, data in _CONTRACT_RISK_MATRIX.items():
            assert data.get("risk_label_ar"), f"{level} missing risk_label_ar"

    def test_all_have_mitigation_strategy_en(self):
        for level, data in _CONTRACT_RISK_MATRIX.items():
            assert data.get("mitigation_strategy_en"), f"{level} missing mitigation_strategy_en"

    def test_all_have_mitigation_strategy_ar(self):
        for level, data in _CONTRACT_RISK_MATRIX.items():
            assert data.get("mitigation_strategy_ar"), f"{level} missing mitigation_strategy_ar"


# ---------------------------------------------------------------------------
# _review_contract
# ---------------------------------------------------------------------------


class TestReviewContract:
    def test_returns_dict(self):
        result = _review_contract(_make_input())
        assert isinstance(result, dict)

    def test_has_compliance_score(self):
        result = _review_contract(_make_input())
        assert "compliance_score" in result

    def test_has_compliance_label(self):
        result = _review_contract(_make_input())
        assert "compliance_label" in result

    def test_has_missing_requirements(self):
        result = _review_contract(_make_input())
        assert "missing_requirements" in result

    def test_has_high_risk_clauses(self):
        result = _review_contract(_make_input())
        assert "high_risk_clauses" in result

    def test_has_negotiable_clauses(self):
        result = _review_contract(_make_input())
        assert "negotiable_clauses" in result

    def test_has_contract_stage(self):
        result = _review_contract(_make_input(contract_stage="draft"))
        assert result["contract_stage"] == "draft"

    def test_perfect_compliance_score_is_100(self):
        result = _review_contract(_make_perfect_input())
        assert result["compliance_score"] == 100

    def test_perfect_compliance_label_is_compliant(self):
        result = _review_contract(_make_perfect_input())
        assert result["compliance_label"] == "compliant"

    def test_no_flags_score_is_0(self):
        result = _review_contract(_make_input(payment_terms_days=60))
        assert result["compliance_score"] == 0

    def test_no_flags_label_is_non_compliant(self):
        result = _review_contract(_make_input(payment_terms_days=60))
        assert result["compliance_label"] == "non_compliant"

    def test_no_flags_missing_requirements_non_empty(self):
        result = _review_contract(_make_input(payment_terms_days=60))
        assert len(result["missing_requirements"]) > 0

    def test_all_flags_true_missing_requirements_empty(self):
        result = _review_contract(_make_perfect_input())
        assert len(result["missing_requirements"]) == 0

    def test_partial_compliance_label(self):
        result = _review_contract(_make_input(includes_arabic_version=True, has_pdpl_clause=True))
        assert result["compliance_label"] == "partial"

    def test_high_risk_clauses_only_high(self):
        result = _review_contract(_make_input())
        for clause in result["high_risk_clauses"]:
            assert clause["risk_level"] == "high"

    def test_high_risk_clauses_count(self):
        result = _review_contract(_make_input())
        expected_high = [c for c in _CONTRACT_CLAUSES if c["risk_level"] == "high"]
        assert len(result["high_risk_clauses"]) == len(expected_high)

    def test_negotiable_clauses_only_negotiable(self):
        result = _review_contract(_make_input())
        for clause in result["negotiable_clauses"]:
            assert clause["negotiable"] is True

    def test_negotiable_clauses_excludes_non_negotiable(self):
        result = _review_contract(_make_input())
        non_negotiable_ids = {c["clause_id"] for c in _CONTRACT_CLAUSES if not c["negotiable"]}
        result_ids = {c["clause_id"] for c in result["negotiable_clauses"]}
        assert result_ids.isdisjoint(non_negotiable_ids)

    def test_governance_decision_is_approval_first(self):
        result = _review_contract(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_invalid_contract_stage_raises_http_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _review_contract(_make_input(contract_stage="unknown"))
        assert exc_info.value.status_code == 422

    def test_all_four_valid_stages_work(self):
        for stage in _VALID_CONTRACT_STAGES:
            result = _review_contract(_make_input(contract_stage=stage))
            assert result["contract_stage"] == stage

    def test_payment_terms_30_adds_10_points(self):
        result_30 = _review_contract(_make_input(payment_terms_days=30))
        result_60 = _review_contract(_make_input(payment_terms_days=60))
        assert result_30["compliance_score"] - result_60["compliance_score"] == 10

    def test_arabic_version_adds_30_points(self):
        result_with = _review_contract(_make_input(includes_arabic_version=True, payment_terms_days=60))
        result_without = _review_contract(_make_input(includes_arabic_version=False, payment_terms_days=60))
        assert result_with["compliance_score"] - result_without["compliance_score"] == 30

    def test_pdpl_clause_adds_30_points(self):
        result_with = _review_contract(_make_input(has_pdpl_clause=True, payment_terms_days=60))
        result_without = _review_contract(_make_input(has_pdpl_clause=False, payment_terms_days=60))
        assert result_with["compliance_score"] - result_without["compliance_score"] == 30

    def test_zatca_clause_adds_30_points(self):
        result_with = _review_contract(_make_input(has_zatca_clause=True, payment_terms_days=60))
        result_without = _review_contract(_make_input(has_zatca_clause=False, payment_terms_days=60))
        assert result_with["compliance_score"] - result_without["compliance_score"] == 30


# ---------------------------------------------------------------------------
# _VALID_CONTRACT_STAGES
# ---------------------------------------------------------------------------


class TestValidContractStages:
    def test_has_four_stages(self):
        assert len(_VALID_CONTRACT_STAGES) == 4

    def test_contains_draft(self):
        assert "draft" in _VALID_CONTRACT_STAGES

    def test_contains_review(self):
        assert "review" in _VALID_CONTRACT_STAGES

    def test_contains_negotiation(self):
        assert "negotiation" in _VALID_CONTRACT_STAGES

    def test_contains_signed(self):
        assert "signed" in _VALID_CONTRACT_STAGES


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/contract-intelligence"

    def test_tags_contain_sales(self):
        assert "Sales" in router.tags
