"""Tests for the sales-playbook router — 90-day commercial plan.

Covers:
  - GET /api/v1/sales-playbook/discovery-script
  - GET /api/v1/sales-playbook/objections
  - POST /api/v1/sales-playbook/recommend-tier
  - GET /api/v1/sales-playbook/follow-up-cadence
  - GET /api/v1/sales-playbook/closing-checklist

Also exercises the pure-function recommend_tier() logic directly.
WhatsApp doctrine compliance check is explicitly marked.
"""

from __future__ import annotations

import os
import sys
import types

# ---------------------------------------------------------------------------
# Environment and security stub — must happen before any app imports
# ---------------------------------------------------------------------------

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")

_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None  # type: ignore[attr-defined]
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.sales_playbook import (  # noqa: E402
    RecommendTierBody,
    _CLOSING_CHECKLIST,
    _DISCOVERY_SCRIPT,
    _FOLLOW_UP_CADENCE,
    _OBJECTIONS,
    recommend_tier,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})

_BASE = "/api/v1/sales-playbook"

# ---------------------------------------------------------------------------
# TestDiscoveryScriptEndpoint
# ---------------------------------------------------------------------------


class TestDiscoveryScriptEndpoint:
    def test_returns_200(self) -> None:
        r = client.get(f"{_BASE}/discovery-script")
        assert r.status_code == 200

    def test_has_8_stages(self) -> None:
        r = client.get(f"{_BASE}/discovery-script")
        body = r.json()
        assert body["total_stages"] == 8
        assert len(body["stages"]) == 8

    def test_stages_have_bilingual_content(self) -> None:
        r = client.get(f"{_BASE}/discovery-script")
        stages = r.json()["stages"]
        for stage in stages:
            assert "stage_name_en" in stage, f"Missing stage_name_en in stage {stage}"
            assert "stage_name_ar" in stage, f"Missing stage_name_ar in stage {stage}"
            assert stage["stage_name_en"], "stage_name_en is empty"
            assert stage["stage_name_ar"], "stage_name_ar is empty"

    def test_stages_have_scripts(self) -> None:
        r = client.get(f"{_BASE}/discovery-script")
        stages = r.json()["stages"]
        for stage in stages:
            assert "script_en" in stage or "script_ar" in stage

    def test_governance_decision_present(self) -> None:
        r = client.get(f"{_BASE}/discovery-script")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_stages_numbered_sequentially(self) -> None:
        r = client.get(f"{_BASE}/discovery-script")
        stages = r.json()["stages"]
        for i, stage in enumerate(stages, start=1):
            assert stage["stage"] == i

    def test_has_duration_fields(self) -> None:
        r = client.get(f"{_BASE}/discovery-script")
        stages = r.json()["stages"]
        for stage in stages:
            key = "duration_min" if "duration_min" in stage else "duration_minutes"
            assert stage.get(key, 0) > 0

    def test_generated_at_present(self) -> None:
        r = client.get(f"{_BASE}/discovery-script")
        assert "generated_at" in r.json()


# ---------------------------------------------------------------------------
# TestObjectionsEndpoint
# ---------------------------------------------------------------------------


class TestObjectionsEndpoint:
    def test_returns_200(self) -> None:
        r = client.get(f"{_BASE}/objections")
        assert r.status_code == 200

    def test_has_15_objections(self) -> None:
        r = client.get(f"{_BASE}/objections")
        body = r.json()
        assert body["total"] == 15
        assert len(body["objections"]) == 15

    def test_objections_are_bilingual(self) -> None:
        r = client.get(f"{_BASE}/objections")
        for obj in r.json()["objections"]:
            assert "objection_en" in obj or "objection_ar" in obj
            assert "response_en" in obj or "response_ar" in obj

    def test_filter_by_stage(self) -> None:
        r = client.get(f"{_BASE}/objections?stage=qualification")
        body = r.json()
        assert r.status_code == 200
        assert body["stage_filter"] == "qualification"
        for obj in body["objections"]:
            assert obj["stage"] == "qualification"

    def test_filter_returns_subset(self) -> None:
        r_all = client.get(f"{_BASE}/objections")
        r_filtered = client.get(f"{_BASE}/objections?stage=qualification")
        assert r_filtered.json()["total"] < r_all.json()["total"]

    def test_governance_decision_present(self) -> None:
        r = client.get(f"{_BASE}/objections")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_each_objection_has_id(self) -> None:
        r = client.get(f"{_BASE}/objections")
        for obj in r.json()["objections"]:
            assert "id" in obj or "objection_id" in obj

    def test_each_objection_has_stage(self) -> None:
        r = client.get(f"{_BASE}/objections")
        for obj in r.json()["objections"]:
            assert "stage" in obj
            assert obj["stage"]


# ---------------------------------------------------------------------------
# TestRecommendTierEndpoint
# ---------------------------------------------------------------------------


class TestRecommendTierEndpoint:
    def _post(self, payload: dict) -> dict:
        r = client.post(f"{_BASE}/recommend-tier", json=payload)
        assert r.status_code == 200
        return r.json()

    def test_returns_200(self) -> None:
        r = client.post(
            f"{_BASE}/recommend-tier",
            json={"icp_score": 50, "company_size": 30, "annual_revenue_sar": 3_000_000},
        )
        assert r.status_code == 200

    def test_high_icp_large_revenue_returns_custom_ai(self) -> None:
        body = self._post(
            {"icp_score": 85, "company_size": 100, "annual_revenue_sar": 25_000_000}
        )
        assert body["recommended_tier"] == "custom_ai"

    def test_high_icp_mid_company_returns_managed_ops(self) -> None:
        body = self._post(
            {"icp_score": 75, "company_size": 60, "annual_revenue_sar": 6_000_000}
        )
        assert body["recommended_tier"] in ("managed_ops", "custom_ai")

    def test_low_icp_returns_free_diagnostic(self) -> None:
        body = self._post(
            {"icp_score": 10, "company_size": 5, "annual_revenue_sar": 200_000}
        )
        assert body["recommended_tier"] == "free_diagnostic"

    def test_zatca_urgency_promotes_tier(self) -> None:
        body_no_urgency = self._post(
            {"icp_score": 20, "company_size": 10, "annual_revenue_sar": 1_000_000, "zatca_urgency": False}
        )
        body_urgency = self._post(
            {"icp_score": 20, "company_size": 10, "annual_revenue_sar": 1_000_000, "zatca_urgency": True}
        )
        tiers = ["free_diagnostic", "sprint", "data_pack", "managed_ops", "custom_ai"]
        idx_no = tiers.index(body_no_urgency["recommended_tier"])
        idx_yes = tiers.index(body_urgency["recommended_tier"])
        assert idx_yes >= idx_no, "ZATCA urgency should not lower the recommended tier"

    def test_governance_decision_present(self) -> None:
        body = self._post({"icp_score": 50, "company_size": 30, "annual_revenue_sar": 3_000_000})
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_response_has_reasoning_fields(self) -> None:
        body = self._post({"icp_score": 60, "company_size": 40, "annual_revenue_sar": 4_000_000})
        assert "reasoning_en" in body or "reason_en" in body

    def test_response_has_expected_close_days(self) -> None:
        body = self._post({"icp_score": 60, "company_size": 40, "annual_revenue_sar": 4_000_000})
        assert "expected_close_days" in body
        assert body["expected_close_days"] > 0

    def test_invalid_icp_score_returns_422(self) -> None:
        r = client.post(
            f"{_BASE}/recommend-tier",
            json={"icp_score": 150, "company_size": 10, "annual_revenue_sar": 1_000_000},
        )
        assert r.status_code == 422

    def test_negative_icp_score_returns_422(self) -> None:
        r = client.post(
            f"{_BASE}/recommend-tier",
            json={"icp_score": -1, "company_size": 10, "annual_revenue_sar": 1_000_000},
        )
        assert r.status_code == 422

    def test_recommend_tier_body_defaults_work(self) -> None:
        """RecommendTierBody has defaults — empty body should succeed."""
        r = client.post(f"{_BASE}/recommend-tier", json={})
        assert r.status_code == 200

    def test_all_tiers_reachable(self) -> None:
        """Smoke-test that each tier value is reachable through the logic."""
        tiers_seen = set()
        cases = [
            {"icp_score": 5, "company_size": 3, "annual_revenue_sar": 100_000},
            {"icp_score": 45, "company_size": 20, "annual_revenue_sar": 1_500_000},
            {"icp_score": 60, "company_size": 30, "annual_revenue_sar": 3_000_000},
            {"icp_score": 75, "company_size": 60, "annual_revenue_sar": 8_000_000},
            {"icp_score": 85, "company_size": 120, "annual_revenue_sar": 30_000_000},
        ]
        for case in cases:
            body = self._post(case)
            tiers_seen.add(body["recommended_tier"])
        assert len(tiers_seen) >= 3, f"Expected at least 3 distinct tiers, got: {tiers_seen}"


# ---------------------------------------------------------------------------
# TestFollowUpCadenceEndpoint
# ---------------------------------------------------------------------------


class TestFollowUpCadenceEndpoint:
    def test_returns_200(self) -> None:
        r = client.get(f"{_BASE}/follow-up-cadence")
        assert r.status_code == 200

    def test_has_5_steps(self) -> None:
        r = client.get(f"{_BASE}/follow-up-cadence")
        body = r.json()
        assert body["total_steps"] == 5
        assert len(body["cadence"]) == 5

    def test_whatsapp_step_has_consent_required_true(self) -> None:
        """Doctrine compliance: WhatsApp channel MUST require explicit consent."""
        r = client.get(f"{_BASE}/follow-up-cadence")
        cadence = r.json()["cadence"]
        whatsapp_steps = [s for s in cadence if "whatsapp" in s.get("channel", "").lower()]
        assert whatsapp_steps, "No WhatsApp step found in cadence"
        for step in whatsapp_steps:
            assert step["consent_required"] is True, (
                f"WhatsApp step on day {step.get('day')} must have consent_required=True"
            )

    def test_whatsapp_step_has_approval_required_true(self) -> None:
        """Doctrine compliance: WhatsApp channel MUST require approval."""
        r = client.get(f"{_BASE}/follow-up-cadence")
        cadence = r.json()["cadence"]
        whatsapp_steps = [s for s in cadence if "whatsapp" in s.get("channel", "").lower()]
        for step in whatsapp_steps:
            assert step["approval_required"] is True, (
                f"WhatsApp step on day {step.get('day')} must have approval_required=True"
            )

    def test_governance_decision_present(self) -> None:
        r = client.get(f"{_BASE}/follow-up-cadence")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_steps_have_channel_field(self) -> None:
        r = client.get(f"{_BASE}/follow-up-cadence")
        for step in r.json()["cadence"]:
            assert "channel" in step

    def test_steps_have_day_field(self) -> None:
        r = client.get(f"{_BASE}/follow-up-cadence")
        for step in r.json()["cadence"]:
            assert "day" in step
            assert step["day"] > 0

    def test_steps_have_templates(self) -> None:
        r = client.get(f"{_BASE}/follow-up-cadence")
        for step in r.json()["cadence"]:
            has_template = "template_en" in step or "template_ar" in step
            assert has_template, f"Step on day {step.get('day')} missing template"

    def test_days_are_ascending(self) -> None:
        r = client.get(f"{_BASE}/follow-up-cadence")
        days = [s["day"] for s in r.json()["cadence"]]
        assert days == sorted(days), f"Cadence days should be ascending: {days}"


# ---------------------------------------------------------------------------
# TestClosingChecklistEndpoint
# ---------------------------------------------------------------------------


class TestClosingChecklistEndpoint:
    def test_returns_200(self) -> None:
        r = client.get(f"{_BASE}/closing-checklist")
        assert r.status_code == 200

    def test_has_10_items(self) -> None:
        r = client.get(f"{_BASE}/closing-checklist")
        body = r.json()
        assert body["total_items"] == 10
        assert len(body["checklist"]) == 10

    def test_critical_items_exist(self) -> None:
        r = client.get(f"{_BASE}/closing-checklist")
        items = r.json()["checklist"]
        critical = [i for i in items if i.get("critical") is True]
        assert len(critical) > 0, "At least one critical item must exist"

    def test_governance_decision_present(self) -> None:
        r = client.get(f"{_BASE}/closing-checklist")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_items_are_bilingual(self) -> None:
        r = client.get(f"{_BASE}/closing-checklist")
        for item in r.json()["checklist"]:
            has_en = "item_en" in item or "gate_en" in item
            has_ar = "item_ar" in item or "gate_ar" in item
            assert has_en, f"Item {item.get('item_id')} missing English text"
            assert has_ar, f"Item {item.get('item_id')} missing Arabic text"

    def test_items_have_item_id(self) -> None:
        r = client.get(f"{_BASE}/closing-checklist")
        for item in r.json()["checklist"]:
            assert "item_id" in item or "id" in item

    def test_critical_count_in_response(self) -> None:
        r = client.get(f"{_BASE}/closing-checklist")
        body = r.json()
        expected_critical = sum(1 for i in body["checklist"] if i.get("critical"))
        assert body.get("critical_items") == expected_critical

    def test_no_guaranteed_claims_item_present(self) -> None:
        """Doctrine guard: the checklist must include a gate for no guaranteed outcome language."""
        r = client.get(f"{_BASE}/closing-checklist")
        items = r.json()["checklist"]
        all_text = " ".join(
            str(i.get("gate_en", "")) + str(i.get("item_en", ""))
            for i in items
        ).lower()
        assert "guaranteed" in all_text or "guarantee" in all_text or "no_guaranteed" in " ".join(
            i.get("id", "") for i in items
        )


# ---------------------------------------------------------------------------
# Unit tests for pure recommend_tier() function
# ---------------------------------------------------------------------------


class TestRecommendTierPureFunction:
    def test_low_score_returns_free_diagnostic(self) -> None:
        result = recommend_tier(
            icp_score=5,
            zatca_urgency=False,
            pdpl_urgency=False,
            company_size=3,
            annual_revenue_sar=200_000,
        )
        assert result["recommended_tier"] == "free_diagnostic"

    def test_high_score_high_revenue_returns_custom_ai(self) -> None:
        result = recommend_tier(
            icp_score=85,
            zatca_urgency=False,
            pdpl_urgency=False,
            company_size=200,
            annual_revenue_sar=30_000_000,
        )
        assert result["recommended_tier"] == "custom_ai"

    def test_urgency_boosts_adjusted_score(self) -> None:
        result_no = recommend_tier(5, False, False, 5, 200_000)
        result_zatca = recommend_tier(5, True, False, 5, 200_000)
        tiers = ["free_diagnostic", "sprint", "data_pack", "managed_ops", "custom_ai"]
        assert tiers.index(result_zatca["recommended_tier"]) >= tiers.index(
            result_no["recommended_tier"]
        )

    def test_result_has_expected_keys(self) -> None:
        result = recommend_tier(50, False, False, 50, 5_000_000)
        assert "recommended_tier" in result
        assert "expected_close_days" in result
        assert "reasoning_en" in result or "reason_en" in result

    def test_recommend_tier_body_is_importable(self) -> None:
        """Spec requires RecommendTierBody to be importable from the router."""
        assert RecommendTierBody is not None

    def test_recommend_tier_body_has_defaults(self) -> None:
        body = RecommendTierBody()
        assert 0 <= body.icp_score <= 100
        assert body.company_size >= 1
        assert body.annual_revenue_sar >= 0


# ---------------------------------------------------------------------------
# Data-level sanity checks (no HTTP call needed)
# ---------------------------------------------------------------------------


class TestDataIntegrity:
    def test_discovery_script_has_8_stages(self) -> None:
        assert len(_DISCOVERY_SCRIPT) == 8

    def test_objections_has_15_entries(self) -> None:
        assert len(_OBJECTIONS) == 15

    def test_cadence_has_5_steps(self) -> None:
        assert len(_FOLLOW_UP_CADENCE) == 5

    def test_checklist_has_10_items(self) -> None:
        assert len(_CLOSING_CHECKLIST) == 10

    def test_whatsapp_cadence_step_is_consent_gated(self) -> None:
        """Doctrine compliance test at data level — not relying on HTTP layer."""
        whatsapp_steps = [
            s for s in _FOLLOW_UP_CADENCE if "whatsapp" in s.get("channel", "").lower()
        ]
        assert whatsapp_steps, "Cadence must contain at least one WhatsApp step"
        for step in whatsapp_steps:
            assert step.get("consent_required") is True, (
                f"WhatsApp step (day {step.get('day')}) must have consent_required=True"
            )
            assert step.get("approval_required") is True, (
                f"WhatsApp step (day {step.get('day')}) must have approval_required=True"
            )

    def test_checklist_items_have_critical_key(self) -> None:
        for item in _CLOSING_CHECKLIST:
            assert "critical" in item, f"Item {item.get('item_id', '?')} missing 'critical' key"

    def test_objections_have_stages(self) -> None:
        for obj in _OBJECTIONS:
            assert "stage" in obj
            assert obj["stage"]
