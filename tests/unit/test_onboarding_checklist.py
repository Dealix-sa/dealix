"""
Unit tests for api/routers/onboarding_checklist.py

Tests cover:
- 3 tier checklists (sprint, data_pack, managed_ops) with phases
- Compliance requirements: PDPL is blocking
- _assess_onboarding: health states, risk detection
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.onboarding_checklist import (
    _TIER_CHECKLISTS,
    _COMPLIANCE_REQUIREMENTS,
    _assess_onboarding,
    OnboardingProgressInput,
    router,
)


class TestTierChecklists:
    def test_three_tiers(self):
        assert len(_TIER_CHECKLISTS) == 3

    def test_sprint_present(self):
        assert "sprint" in _TIER_CHECKLISTS

    def test_data_pack_present(self):
        assert "data_pack" in _TIER_CHECKLISTS

    def test_managed_ops_present(self):
        assert "managed_ops" in _TIER_CHECKLISTS

    def test_all_bilingual(self):
        for k, v in _TIER_CHECKLISTS.items():
            assert v.get("tier_en"), f"{k} missing tier_en"
            assert v.get("tier_ar"), f"{k} missing tier_ar"

    def test_all_have_phases(self):
        for k, v in _TIER_CHECKLISTS.items():
            assert len(v.get("phases", [])) >= 2, f"{k} needs ≥2 phases"

    def test_all_phases_have_bilingual_tasks(self):
        for k, v in _TIER_CHECKLISTS.items():
            for phase in v["phases"]:
                assert len(phase.get("tasks_en", [])) >= 2, f"{k} phase {phase['phase']} needs ≥2 en tasks"
                assert len(phase.get("tasks_ar", [])) >= 2, f"{k} phase {phase['phase']} needs ≥2 ar tasks"

    def test_phase_task_counts_match(self):
        for k, v in _TIER_CHECKLISTS.items():
            for phase in v["phases"]:
                assert len(phase["tasks_en"]) == len(phase["tasks_ar"]), f"{k} phase {phase['phase']} mismatch"

    def test_sprint_7_days(self):
        assert _TIER_CHECKLISTS["sprint"]["duration_days"] == 7

    def test_managed_ops_30_days(self):
        assert _TIER_CHECKLISTS["managed_ops"]["duration_days"] == 30

    def test_sprint_first_phase_is_blocking(self):
        first_phase = _TIER_CHECKLISTS["sprint"]["phases"][0]
        assert first_phase["blocking"] is True

    def test_all_have_success_criteria(self):
        for k, v in _TIER_CHECKLISTS.items():
            assert len(v.get("success_criteria_en", [])) >= 2, f"{k} needs ≥2 success criteria"

    def test_all_have_churn_signals(self):
        for k, v in _TIER_CHECKLISTS.items():
            assert len(v.get("churn_risk_signals_en", [])) >= 2, f"{k} needs ≥2 churn signals"

    def test_first_phase_pdpl_required(self):
        for k, v in _TIER_CHECKLISTS.items():
            first_phase = v["phases"][0]
            assert first_phase.get("pdpl_required") is True, f"{k} phase 1 must require PDPL"


class TestComplianceRequirements:
    def test_four_requirements(self):
        assert len(_COMPLIANCE_REQUIREMENTS) == 4

    def test_pdpl_is_blocking(self):
        pdpl = next(r for r in _COMPLIANCE_REQUIREMENTS if "PDPL" in r["requirement"])
        assert pdpl["blocking"] is True

    def test_pdpl_applies_to_all_tiers(self):
        pdpl = next(r for r in _COMPLIANCE_REQUIREMENTS if "PDPL" in r["requirement"])
        assert "sprint" in pdpl["applies_to_tiers"]
        assert "managed_ops" in pdpl["applies_to_tiers"]

    def test_all_bilingual(self):
        for r in _COMPLIANCE_REQUIREMENTS:
            assert r.get("requirement_ar"), f"{r['requirement']} missing AR"
            assert r.get("description_en"), f"{r['requirement']} missing description_en"
            assert r.get("description_ar"), f"{r['requirement']} missing description_ar"

    def test_pdpl_has_template(self):
        pdpl = next(r for r in _COMPLIANCE_REQUIREMENTS if "PDPL" in r["requirement"])
        assert pdpl["template_available"] is True

    def test_nca_applies_to_managed_ops(self):
        nca = next(r for r in _COMPLIANCE_REQUIREMENTS if "NCA" in r["requirement"] or "Cybersecurity" in r["requirement"])
        assert "managed_ops" in nca["applies_to_tiers"]

    def test_data_residency_requirement_present(self):
        residency = next(
            (r for r in _COMPLIANCE_REQUIREMENTS if "residency" in r["requirement"].lower() or "Residency" in r["requirement"]),
            None,
        )
        assert residency is not None


class TestAssessOnboarding:
    def _healthy_input(self, **overrides) -> OnboardingProgressInput:
        data = dict(
            client_name="ACME Saudi",
            tier="sprint",
            day_number=3,
            pdpl_signed=True,
            champion_active=True,
            data_received=True,
        )
        data.update(overrides)
        return OnboardingProgressInput(**data)

    def test_on_track_when_all_ok(self):
        result = _assess_onboarding(self._healthy_input())
        assert result["engagement_health"] == "On Track"

    def test_blocked_when_pdpl_not_signed(self):
        result = _assess_onboarding(self._healthy_input(pdpl_signed=False))
        assert result["engagement_health"] == "Blocked"

    def test_pdpl_risk_in_risks(self):
        result = _assess_onboarding(self._healthy_input(pdpl_signed=False))
        risk_text = " ".join(result["risks"]).lower()
        assert "pdpl" in risk_text or "data processing" in risk_text

    def test_champion_inactive_is_risk(self):
        result = _assess_onboarding(self._healthy_input(champion_active=False))
        risk_text = " ".join(result["risks"]).lower()
        assert "champion" in risk_text

    def test_no_data_by_day3_is_risk(self):
        result = _assess_onboarding(self._healthy_input(data_received=False, day_number=3))
        risk_text = " ".join(result["risks"]).lower()
        assert "data" in risk_text

    def test_progress_pct_increases_with_day(self):
        day3 = _assess_onboarding(self._healthy_input(day_number=3))
        day7 = _assess_onboarding(self._healthy_input(day_number=7))
        assert day7["progress_pct"] > day3["progress_pct"]

    def test_progress_capped_at_100(self):
        result = _assess_onboarding(self._healthy_input(day_number=100))
        assert result["progress_pct"] <= 100.0

    def test_invalid_tier_raises(self):
        with pytest.raises(Exception):
            OnboardingProgressInput(
                client_name="Test",
                tier="invalid_tier",
                day_number=1,
            )

    def test_governance_allow_with_review(self):
        result = _assess_onboarding(self._healthy_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_multiple_risks_is_at_risk(self):
        result = _assess_onboarding(self._healthy_input(
            pdpl_signed=False, champion_active=False, data_received=False
        ))
        assert result["engagement_health"] in ("At Risk", "Blocked")


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/onboarding-checklist"

    def test_router_tags(self):
        assert "Analytics" in router.tags
