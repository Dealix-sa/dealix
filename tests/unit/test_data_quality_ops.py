"""Unit tests for api/routers/data_quality_ops.py"""
from __future__ import annotations

import pytest

from api.routers.data_quality_ops import (
    _DQ_DIMENSIONS,
    _DQ_REMEDIATION_PLAYBOOKS,
    _ZATCA_DQ_REQUIREMENTS,
    DQAssessmentInput,
    _assess_data_quality,
    router,
)


def _make_input(**overrides) -> DQAssessmentInput:
    data = dict(
        client_name="SABIC Digital",
        completeness_score=80.0,
        accuracy_score=85.0,
        timeliness_score=75.0,
        consistency_score=70.0,
        uniqueness_score=90.0,
    )
    data.update(overrides)
    return DQAssessmentInput(**data)


# ---------------------------------------------------------------------------
# Static data: DQ dimensions
# ---------------------------------------------------------------------------


class TestDQDimensions:
    def test_has_five_dimensions(self):
        assert len(_DQ_DIMENSIONS) == 5

    def test_weights_sum_to_100(self):
        total = sum(d["weight"] for d in _DQ_DIMENSIONS)
        assert total == 100

    def test_dimension_ids(self):
        ids = {d["dimension_id"] for d in _DQ_DIMENSIONS}
        assert ids == {"completeness", "accuracy", "timeliness", "consistency", "uniqueness"}

    def test_all_have_dimension_name_en(self):
        for d in _DQ_DIMENSIONS:
            assert d.get("dimension_name_en"), f"{d.get('dimension_id')} missing dimension_name_en"

    def test_all_have_dimension_name_ar(self):
        for d in _DQ_DIMENSIONS:
            assert d.get("dimension_name_ar"), f"{d.get('dimension_id')} missing dimension_name_ar"

    def test_all_have_description_en(self):
        for d in _DQ_DIMENSIONS:
            assert d.get("description_en"), f"{d.get('dimension_id')} missing description_en"

    def test_all_have_measurement_method_en(self):
        for d in _DQ_DIMENSIONS:
            assert d.get("measurement_method_en"), f"{d.get('dimension_id')} missing measurement_method_en"

    def test_completeness_weight(self):
        dim = next(d for d in _DQ_DIMENSIONS if d["dimension_id"] == "completeness")
        assert dim["weight"] == 25

    def test_accuracy_weight(self):
        dim = next(d for d in _DQ_DIMENSIONS if d["dimension_id"] == "accuracy")
        assert dim["weight"] == 25

    def test_timeliness_weight(self):
        dim = next(d for d in _DQ_DIMENSIONS if d["dimension_id"] == "timeliness")
        assert dim["weight"] == 20

    def test_consistency_weight(self):
        dim = next(d for d in _DQ_DIMENSIONS if d["dimension_id"] == "consistency")
        assert dim["weight"] == 20

    def test_uniqueness_weight(self):
        dim = next(d for d in _DQ_DIMENSIONS if d["dimension_id"] == "uniqueness")
        assert dim["weight"] == 10


# ---------------------------------------------------------------------------
# Static data: remediation playbooks
# ---------------------------------------------------------------------------


class TestDQRemediationPlaybooks:
    def test_has_three_keys(self):
        assert len(_DQ_REMEDIATION_PLAYBOOKS) == 3

    def test_has_critical_key(self):
        assert "critical" in _DQ_REMEDIATION_PLAYBOOKS

    def test_has_needs_work_key(self):
        assert "needs_work" in _DQ_REMEDIATION_PLAYBOOKS

    def test_has_healthy_key(self):
        assert "healthy" in _DQ_REMEDIATION_PLAYBOOKS

    def test_all_have_label_en(self):
        for key, pb in _DQ_REMEDIATION_PLAYBOOKS.items():
            assert pb.get("label_en"), f"{key} missing label_en"

    def test_all_have_label_ar(self):
        for key, pb in _DQ_REMEDIATION_PLAYBOOKS.items():
            assert pb.get("label_ar"), f"{key} missing label_ar"

    def test_all_have_three_priority_actions_en(self):
        for key, pb in _DQ_REMEDIATION_PLAYBOOKS.items():
            assert len(pb.get("priority_actions_en", [])) == 3, f"{key} must have 3 priority_actions_en"

    def test_all_have_three_priority_actions_ar(self):
        for key, pb in _DQ_REMEDIATION_PLAYBOOKS.items():
            assert len(pb.get("priority_actions_ar", [])) == 3, f"{key} must have 3 priority_actions_ar"


# ---------------------------------------------------------------------------
# Static data: ZATCA DQ requirements
# ---------------------------------------------------------------------------


class TestZATCADQRequirements:
    def test_has_four_requirements(self):
        assert len(_ZATCA_DQ_REQUIREMENTS) == 4

    def test_all_have_requirement_en(self):
        for r in _ZATCA_DQ_REQUIREMENTS:
            assert r.get("requirement_en"), "Requirement missing requirement_en"

    def test_all_have_requirement_ar(self):
        for r in _ZATCA_DQ_REQUIREMENTS:
            assert r.get("requirement_ar"), "Requirement missing requirement_ar"

    def test_all_have_minimum_score(self):
        for r in _ZATCA_DQ_REQUIREMENTS:
            assert isinstance(r.get("minimum_score"), int)
            assert 0 <= r["minimum_score"] <= 100

    def test_completeness_minimum_score(self):
        scores = [r["minimum_score"] for r in _ZATCA_DQ_REQUIREMENTS]
        assert 95 in scores

    def test_accuracy_minimum_score(self):
        scores = [r["minimum_score"] for r in _ZATCA_DQ_REQUIREMENTS]
        assert 99 in scores

    def test_timeliness_minimum_score(self):
        scores = [r["minimum_score"] for r in _ZATCA_DQ_REQUIREMENTS]
        assert 90 in scores

    def test_uniqueness_minimum_score(self):
        scores = [r["minimum_score"] for r in _ZATCA_DQ_REQUIREMENTS]
        assert 100 in scores


# ---------------------------------------------------------------------------
# _assess_data_quality
# ---------------------------------------------------------------------------


class TestAssessDataQuality:
    def test_returns_dict(self):
        result = _assess_data_quality(_make_input())
        assert isinstance(result, dict)

    def test_has_overall_score(self):
        result = _assess_data_quality(_make_input())
        assert "overall_score" in result

    def test_has_dq_label(self):
        result = _assess_data_quality(_make_input())
        assert "dq_label" in result

    def test_has_playbook(self):
        result = _assess_data_quality(_make_input())
        assert "playbook" in result

    def test_has_dimension_scores(self):
        result = _assess_data_quality(_make_input())
        assert "dimension_scores" in result

    def test_dimension_scores_has_five_items(self):
        result = _assess_data_quality(_make_input())
        assert len(result["dimension_scores"]) == 5

    def test_has_zatca_compliant(self):
        result = _assess_data_quality(_make_input())
        assert "zatca_compliant" in result

    def test_has_weakest_dimension(self):
        result = _assess_data_quality(_make_input())
        assert "weakest_dimension" in result

    def test_has_client_name(self):
        result = _assess_data_quality(_make_input(client_name="Aramco"))
        assert result["client_name"] == "Aramco"

    def test_overall_score_weighted_average_known_inputs(self):
        # completeness=80, accuracy=85, timeliness=75, consistency=70, uniqueness=90
        # 80*0.25 + 85*0.25 + 75*0.20 + 70*0.20 + 90*0.10
        # = 20 + 21.25 + 15 + 14 + 9 = 79.25
        result = _assess_data_quality(_make_input())
        assert result["overall_score"] == pytest.approx(79.25)

    def test_perfect_scores_overall_100(self):
        result = _assess_data_quality(_make_input(
            completeness_score=100, accuracy_score=100,
            timeliness_score=100, consistency_score=100, uniqueness_score=100,
        ))
        assert result["overall_score"] == pytest.approx(100.0)

    def test_perfect_scores_label_healthy(self):
        result = _assess_data_quality(_make_input(
            completeness_score=100, accuracy_score=100,
            timeliness_score=100, consistency_score=100, uniqueness_score=100,
        ))
        assert result["dq_label"] == "healthy"

    def test_perfect_scores_zatca_compliant_true(self):
        result = _assess_data_quality(_make_input(
            completeness_score=100, accuracy_score=100,
            timeliness_score=100, consistency_score=100, uniqueness_score=100,
        ))
        assert result["zatca_compliant"] is True

    def test_low_scores_all_30_label_critical(self):
        result = _assess_data_quality(_make_input(
            completeness_score=30, accuracy_score=30,
            timeliness_score=30, consistency_score=30, uniqueness_score=30,
        ))
        assert result["dq_label"] == "critical"
        assert result["overall_score"] == pytest.approx(30.0)

    def test_score_below_80_label_needs_work(self):
        # overall_score = 79.25 → needs_work
        result = _assess_data_quality(_make_input())
        assert result["dq_label"] == "needs_work"

    def test_score_above_80_label_healthy(self):
        result = _assess_data_quality(_make_input(
            completeness_score=90, accuracy_score=90,
            timeliness_score=85, consistency_score=85, uniqueness_score=90,
        ))
        assert result["dq_label"] == "healthy"

    def test_completeness_below_95_zatca_false(self):
        result = _assess_data_quality(_make_input(
            completeness_score=94, accuracy_score=100,
            timeliness_score=95, consistency_score=95, uniqueness_score=100,
        ))
        assert result["zatca_compliant"] is False

    def test_accuracy_below_99_zatca_false(self):
        result = _assess_data_quality(_make_input(
            completeness_score=100, accuracy_score=98,
            timeliness_score=95, consistency_score=95, uniqueness_score=100,
        ))
        assert result["zatca_compliant"] is False

    def test_timeliness_below_90_zatca_false(self):
        result = _assess_data_quality(_make_input(
            completeness_score=100, accuracy_score=100,
            timeliness_score=89, consistency_score=95, uniqueness_score=100,
        ))
        assert result["zatca_compliant"] is False

    def test_uniqueness_below_100_zatca_false(self):
        result = _assess_data_quality(_make_input(
            completeness_score=100, accuracy_score=100,
            timeliness_score=95, consistency_score=95, uniqueness_score=99,
        ))
        assert result["zatca_compliant"] is False

    def test_weakest_dimension_identifies_lowest(self):
        result = _assess_data_quality(_make_input(
            completeness_score=90, accuracy_score=85,
            timeliness_score=75, consistency_score=80, uniqueness_score=95,
        ))
        assert result["weakest_dimension"] == "timeliness"

    def test_dimension_scores_each_have_required_keys(self):
        result = _assess_data_quality(_make_input())
        for ds in result["dimension_scores"]:
            assert "dimension_id" in ds
            assert "score" in ds
            assert "weight" in ds
            assert "weighted_contribution" in ds

    def test_dimension_scores_weighted_contribution_correct(self):
        result = _assess_data_quality(_make_input(
            completeness_score=80, accuracy_score=85,
            timeliness_score=75, consistency_score=70, uniqueness_score=90,
        ))
        completeness_ds = next(ds for ds in result["dimension_scores"] if ds["dimension_id"] == "completeness")
        assert completeness_ds["weighted_contribution"] == pytest.approx(80 * 25 / 100)

    def test_governance_decision_allow_with_review(self):
        result = _assess_data_quality(_make_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_playbook_matches_label(self):
        result = _assess_data_quality(_make_input(
            completeness_score=30, accuracy_score=30,
            timeliness_score=30, consistency_score=30, uniqueness_score=30,
        ))
        assert result["playbook"]["label_en"] == "Critical"

    def test_healthy_playbook_has_actions(self):
        result = _assess_data_quality(_make_input(
            completeness_score=95, accuracy_score=95,
            timeliness_score=90, consistency_score=90, uniqueness_score=95,
        ))
        assert len(result["playbook"]["priority_actions_en"]) == 3


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/data-quality-ops"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
