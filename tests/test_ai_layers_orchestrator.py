"""Tests for the AI Layers orchestrator + per-layer happy paths."""
from __future__ import annotations

import pytest

from auto_client_acquisition.ai_layers import (
    AI_LAYERS,
    LayerContext,
    run_layer,
    run_pipeline,
)


def _ctx(**overrides) -> LayerContext:
    base = dict(
        customer_id="acme_co",
        payload={},
        source_refs=("founder://warm_list/001",),
        actor="dealix-pm",
        external_action_requested=False,
        contains_pii_hint=False,
    )
    base.update(overrides)
    return LayerContext(**base)  # type: ignore[arg-type]


def test_canonical_layer_list_count_is_nine() -> None:
    assert len(AI_LAYERS) == 9
    expected = {
        "lead_scoring", "account_scoring", "content_generation",
        "decision_passport", "compliance_reasoning", "proof_curation",
        "customer_health", "growth_signals", "executive_intelligence",
    }
    assert set(AI_LAYERS) == expected


def test_lead_scoring_qualified_a() -> None:
    ctx = _ctx(
        payload={
            "title_founder_exec": True,
            "b2b_company": True,
            "crm_or_pipeline": True,
            "uses_or_plans_ai": True,
            "saudi_or_gcc": True,
            "urgent_within_30d": True,
        }
    )
    r = run_layer("lead_scoring", ctx)
    assert r.ok
    assert r.governance_decision == "ALLOW"
    assert r.output["route"] == "qualified_a"
    assert r.output["score"] >= 15


def test_lead_scoring_blocks_without_source_ref() -> None:
    ctx = _ctx(source_refs=())
    r = run_layer("lead_scoring", ctx)
    assert not r.ok
    assert r.governance_decision == "BLOCK"


def test_account_scoring_tier_a() -> None:
    ctx = _ctx(
        payload={
            "account_name": "Sample Corp",
            "icp_signals": {
                "saudi_b2b": True,
                "size_50_500_emp": True,
                "has_data_owner": True,
                "uses_crm": True,
                "has_ai_budget": True,
                "regulated_industry_bonus": True,
            },
            "readiness_signals": {
                "data_available": True,
                "owner_present": True,
                "accepts_governance": True,
                "workflow_pain_clear": True,
            },
            "estimated_acv_sar": 30_000,
        }
    )
    r = run_layer("account_scoring", ctx)
    assert r.ok
    assert r.output["tier"] == "A"
    assert r.output["composite"] >= 75
    assert "scoring_rule" in r.capital_asset_candidates


def test_account_scoring_blocks_without_source_ref() -> None:
    ctx = _ctx(payload={"account_name": "X"}, source_refs=())
    r = run_layer("account_scoring", ctx)
    assert not r.ok
    assert r.governance_decision == "BLOCK"


def test_content_generation_safe_default_is_draft_only() -> None:
    ctx = _ctx(payload={"topic": "Revenue Sprint", "audience": "fintech"})
    r = run_layer("content_generation", ctx)
    assert r.ok
    assert r.governance_decision == "DRAFT_ONLY"
    assert "ar" in r.output["drafts"]
    assert "en" in r.output["drafts"]
    assert "القيمة التقديرية" in r.output["disclaimer"]


def test_content_generation_external_action_requires_approval() -> None:
    ctx = _ctx(
        payload={"topic": "Diagnostic"}, external_action_requested=True
    )
    r = run_layer("content_generation", ctx)
    assert r.governance_decision == "REQUIRE_APPROVAL"


def test_content_generation_redacts_guaranteed_claim_topic() -> None:
    ctx = _ctx(payload={"topic": "guaranteed sales for Q3"})
    r = run_layer("content_generation", ctx)
    assert r.governance_decision == "REDACT"
    assert not r.ok


def test_decision_passport_assembles_with_evidence_chain() -> None:
    ctx = _ctx(
        payload={
            "action": "send_warm_outreach",
            "evidence_refs": ["proof://pack/PP-001", "value://event/VE-007"],
            "risk_class": "L2",
        }
    )
    r = run_layer("decision_passport", ctx)
    assert r.ok
    assert r.governance_decision == "ALLOW"
    assert len(r.output["evidence_chain"]) >= 3  # source_ref + 2 evidence


def test_decision_passport_blocks_without_any_evidence() -> None:
    ctx = _ctx(payload={"action": "send_email"}, source_refs=())
    r = run_layer("decision_passport", ctx)
    assert not r.ok
    assert r.governance_decision == "BLOCK"


def test_decision_passport_high_risk_requires_approval() -> None:
    ctx = _ctx(
        payload={
            "action": "publish_post",
            "evidence_refs": ["proof://pack/001"],
            "risk_class": "L4",
        }
    )
    r = run_layer("decision_passport", ctx)
    assert r.governance_decision == "REQUIRE_APPROVAL"


def test_compliance_reasoning_allows_clean_case() -> None:
    ctx = _ctx(
        payload={
            "action": "internal_dashboard_view",
            "contains_pii": False,
            "data_classification": "internal",
            "processing_region": "sa",
        }
    )
    r = run_layer("compliance_reasoning", ctx)
    assert r.ok
    assert r.governance_decision == "ALLOW"


def test_compliance_reasoning_blocks_pii_without_lawful_basis() -> None:
    ctx = _ctx(
        payload={
            "action": "process_customer_data",
            "contains_pii": True,
            # No lawful_basis declared.
        }
    )
    r = run_layer("compliance_reasoning", ctx)
    assert r.governance_decision == "BLOCK"


def test_compliance_reasoning_blocks_non_saudi_region() -> None:
    ctx = _ctx(
        payload={
            "action": "store_data",
            "data_classification": "internal",
            "processing_region": "eu",
        }
    )
    r = run_layer("compliance_reasoning", ctx)
    assert r.governance_decision == "BLOCK"
    assert "NCA" in r.output["frameworks"]


def test_compliance_reasoning_zatca_missing_uuid_blocks() -> None:
    ctx = _ctx(
        payload={
            "action": "issue_invoice",
            "is_invoice": True,
            "vat_id": "300000000000003",
            # No invoice_uuid.
        }
    )
    r = run_layer("compliance_reasoning", ctx)
    assert r.governance_decision == "BLOCK"


def test_proof_curation_blocks_when_no_artifacts() -> None:
    ctx = _ctx(payload={"sector": "saas", "stage": "proposal", "artifacts": []})
    r = run_layer("proof_curation", ctx)
    assert not r.ok
    assert r.governance_decision == "BLOCK"


def test_proof_curation_blocks_when_no_source_ref_on_artifacts() -> None:
    ctx = _ctx(
        payload={
            "sector": "saas",
            "stage": "proposal",
            "artifacts": [
                {"id": "A", "type": "proof_example", "tier": "verified"},
            ],
        }
    )
    r = run_layer("proof_curation", ctx)
    assert not r.ok
    assert r.governance_decision == "BLOCK"


def test_proof_curation_picks_top_n() -> None:
    artifacts = [
        {
            "id": f"A{i}",
            "type": "proof_example",
            "tier": "verified",
            "source_ref": f"proof://{i}",
            "summary": f"case {i}",
        }
        for i in range(5)
    ]
    ctx = _ctx(
        payload={"sector": "saas", "stage": "proposal", "artifacts": artifacts, "top_n": 2}
    )
    r = run_layer("proof_curation", ctx)
    assert r.ok
    assert r.governance_decision == "ALLOW"
    assert len(r.output["selected"]) == 2


def test_customer_health_buckets() -> None:
    ctx = _ctx(
        payload={
            "adoption_pct": 80,
            "usage_last_7d": 10,
            "friction_high_severity_14d": 0,
            "last_value_event_tier": "verified",
        }
    )
    r = run_layer("customer_health", ctx)
    assert r.ok
    assert r.output["bucket"] == "healthy"


def test_customer_health_critical_with_high_friction() -> None:
    ctx = _ctx(
        payload={
            "adoption_pct": 20,
            "usage_last_7d": 0,
            "friction_high_severity_14d": 5,
            "last_value_event_tier": "estimated",
        }
    )
    r = run_layer("customer_health", ctx)
    assert r.output["bucket"] in ("at_risk", "critical")
    assert "low_adoption" in r.output["risk_flags"]


def test_growth_signals_rejects_forbidden_kind() -> None:
    ctx = _ctx(
        payload={
            "signals": [
                {"kind": "scraped_linkedin", "timestamp": "2026-05-01T00:00:00Z",
                 "account_hint": "X", "source_ref": "x"},
            ]
        }
    )
    r = run_layer("growth_signals", ctx)
    assert r.governance_decision in ("ALLOW", "ALLOW_WITH_REVIEW")
    assert r.output["rejected_count"] == 1
    assert r.output["accepted_count"] == 0


def test_growth_signals_ranks_warm_intro_first() -> None:
    ctx = _ctx(
        payload={
            "signals": [
                {"kind": "manual_research_note", "timestamp": "2026-05-23T00:00:00Z",
                 "account_hint": "B", "source_ref": "note://2"},
                {"kind": "warm_intro", "timestamp": "2026-05-23T00:00:00Z",
                 "account_hint": "A", "source_ref": "intro://1"},
            ]
        }
    )
    r = run_layer("growth_signals", ctx)
    assert r.ok
    assert r.output["ranked"][0]["kind"] == "warm_intro"


def test_executive_intelligence_grade_on_strong_inputs() -> None:
    ctx = _ctx(
        payload={
            "customer_health_composite": 88,
            "proof_artifact_count_sourced": 5,
            "growth_signal_acceptance_pct": 80,
            "compliance_overall": "ALLOW",
            "partnership_active_count": 3,
        }
    )
    r = run_layer("executive_intelligence", ctx)
    assert r.ok
    assert r.output["grade"] in ("A", "B")
    assert r.output["composite"] >= 70


def test_pipeline_overall_decision_is_strictest() -> None:
    # A run where compliance_reasoning will BLOCK (PII without lawful basis).
    ctx = _ctx(
        payload={
            "topic": "Diagnostic",
            "action": "send_email",
            "contains_pii": True,
            "evidence_refs": ["proof://1"],
            "account_name": "X",
            "icp_signals": {"saudi_b2b": True},
            "readiness_signals": {"data_available": True},
            "artifacts": [
                {"id": "A1", "type": "proof_example", "tier": "verified",
                 "source_ref": "proof://1"}
            ],
            "sector": "saas",
            "stage": "diagnosis",
        },
        contains_pii_hint=True,
    )
    pr = run_pipeline(ctx)
    assert pr.overall_decision in ("BLOCK", "REQUIRE_APPROVAL", "REDACT")
    assert "compliance_reasoning" in pr.results
    assert len(pr.results) == len(AI_LAYERS)


def test_pipeline_subset_runs_only_selected_layers() -> None:
    ctx = _ctx(
        payload={
            "title_founder_exec": True,
            "b2b_company": True,
        }
    )
    pr = run_pipeline(ctx, layers=("lead_scoring",))
    assert pr.layers_run == ("lead_scoring",)
    assert "lead_scoring" in pr.results
    assert "account_scoring" not in pr.results


def test_every_layer_result_carries_governance_decision() -> None:
    """Doctrine: every output object must carry a governance_decision."""
    ctx = _ctx(
        payload={
            "title_founder_exec": True,
            "account_name": "X",
            "icp_signals": {"saudi_b2b": True},
            "readiness_signals": {"data_available": True},
            "estimated_acv_sar": 500,
            "topic": "Diagnostic",
            "action": "internal_view",
            "evidence_refs": ["proof://1"],
            "data_classification": "internal",
            "processing_region": "sa",
            "artifacts": [
                {"id": "A", "type": "proof_example", "tier": "verified",
                 "source_ref": "proof://1"}
            ],
            "signals": [
                {"kind": "warm_intro", "timestamp": "2026-05-20T00:00:00Z",
                 "account_hint": "X", "source_ref": "intro://1"}
            ],
            "sector": "saas",
            "stage": "discovery",
        }
    )
    pr = run_pipeline(ctx)
    for layer_name, result in pr.results.items():
        assert result.governance_decision, f"missing governance_decision on {layer_name}"
        assert result.governance_decision in {
            "ALLOW", "ALLOW_WITH_REVIEW", "DRAFT_ONLY",
            "REQUIRE_APPROVAL", "REDACT", "BLOCK", "ESCALATE",
        }


def test_unknown_layer_returns_block() -> None:
    ctx = _ctx()
    r = run_layer("nonexistent_layer", ctx)  # type: ignore[arg-type]
    assert not r.ok
    assert r.governance_decision == "BLOCK"
