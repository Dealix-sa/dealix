from __future__ import annotations

import json
from pathlib import Path

import pytest

from dealix.company_os.company_directory import DirectoryCandidate
from dealix.revenue_lab import CompanySignal, EvidenceReference, OutcomeEvent, run_revenue_lab
from dealix.revenue_lab.adapters import signal_from_directory_candidate
from dealix.revenue_lab.artifacts import write_bundle


def make_signal(
    *, demo: bool = False, permission: str = "warm", with_metrics: bool = False
) -> CompanySignal:
    evidence = EvidenceReference(
        source_ref=("demo://fixture" if demo else "https://example.com/company/news"),
        source_type="synthetic_fixture" if demo else "company_website",
        observed_at="2026-07-15T00:00:00Z",
        quality="demo" if demo else "primary",
    )
    metrics = {}
    if with_metrics:
        metrics = {
            "manual_hours_per_week": 20.0,
            "hourly_cost_sar": 80.0,
            "lost_leads_per_month": 4.0,
            "avg_deal_value_sar": 5000.0,
            "recovered_conversion_pct": 10.0,
            "setup_cost_sar": 5000.0,
            "monthly_cost_sar": 2500.0,
        }
    return CompanySignal(
        tenant_id="dealix",
        account_id="acct-1",
        company_name="Source-backed Company",
        sector="operations",
        company_size="sme",
        department="sales",
        relationship="prospect",
        permission=permission,
        decision_maker_role="Operations director",
        offer_match="Revenue Proof Sprint",
        why_now="A dated source shows an operational change.",
        value_exchange="Bounded workflow proof.",
        pain_hypotheses=("Manual follow-up may be slow.",),
        unknowns=("Baseline cycle time",),
        evidence=(evidence,),
        strategic_fit=80,
        urgency=70,
        known_metrics=metrics,
        demo=demo,
    )


def test_source_backed_signal_reuses_approval_and_proof_contracts() -> None:
    bundle = run_revenue_lab([make_signal()])

    assert bundle.mode == "source_backed"
    assert bundle.summary["external_actions_executed"] == 0
    assert bundle.summary["proof_events"] == 1
    assert bundle.opportunities[0].prediction_status == "not_calibrated"
    assert bundle.opportunities[0].conversion_probability is None
    assert bundle.approval_requests[0]["status"] == "pending"
    assert bundle.approval_requests[0]["action_mode"] == "approval_required"
    assert bundle.proof_events[0]["payload"]["outcome_claimed"] is False
    assert "approved_list_price" in bundle.strategies[0].negotiation_missing_inputs


def test_demo_signal_fails_closed_and_never_creates_proof() -> None:
    bundle = run_revenue_lab([make_signal(demo=True, permission="approved")])

    assert bundle.mode == "mixed_or_demo"
    assert bundle.proof_events == ()
    assert bundle.approval_requests[0]["status"] == "blocked"
    assert bundle.opportunities[0].evidence_status == "demo_only"
    assert bundle.opportunities[0].next_action == "validate_sources_and_permission"


def test_roi_is_only_a_scenario_when_all_baselines_are_supplied() -> None:
    pending = run_revenue_lab([make_signal()]).proposals[0].roi
    estimated = run_revenue_lab([make_signal(with_metrics=True)]).proposals[0].roi

    assert pending["status"] == "pending_client_baseline"
    assert "gross_annual_value_sar_min" not in pending
    assert estimated["status"] == "scenario_estimate"
    assert estimated["is_estimate"] is True
    assert "Estimates" in estimated["disclaimer"]


def test_learning_proposes_an_experiment_but_never_changes_weights() -> None:
    outcome = OutcomeEvent(
        account_id="acct-1",
        outcome="rejected",
        source_ref="crm:event-42",
        observed_at="2026-07-15T00:00:00Z",
    )
    recommendation = run_revenue_lab([make_signal()], outcomes=[outcome]).learning_recommendations[
        0
    ]

    assert recommendation.experiment_required is True
    assert recommendation.weight_change_applied is False
    assert recommendation.approval_status == "approval_required"


def test_real_outcome_requires_attributable_source() -> None:
    with pytest.raises(ValueError, match="source_ref"):
        OutcomeEvent(
            account_id="acct-1",
            outcome="meeting_booked",
            source_ref="",
            observed_at="2026-07-15T00:00:00Z",
        )


def test_artifacts_separate_priority_from_probability(tmp_path: Path) -> None:
    bundle = run_revenue_lab([make_signal(demo=True, permission="research_only")])
    paths = write_bundle(tmp_path, bundle)

    payload = json.loads(paths["latest_json"].read_text(encoding="utf-8"))
    proof = json.loads(paths["proof_log"].read_text(encoding="utf-8"))
    graph = paths["opportunity_graph"].read_text(encoding="utf-8")
    assert payload["opportunities"][0]["conversion_probability"] is None
    assert "priority_score" in graph
    assert proof["events"] == []
    assert proof["verified_customer_outcomes"] == 0


def test_directory_adapter_does_not_infer_permission_from_available_contacts() -> None:
    candidate = DirectoryCandidate(
        id="directory-1",
        company_name="Directory Company",
        normalized_name="directory company",
        city="Riyadh",
        activity="logistics",
        has_valid_email=True,
        has_valid_phone=True,
        email_masked="a***@example.com",
        phone_masked="+***1234",
        email_hmac=None,
        phone_hmac=None,
        source_sheet="companies",
        source_row_number=2,
        source_fingerprint="abc123",
        data_quality_score=80.0,
        fit_score=85.0,
        research_priority_score=82.0,
        priority="A",
        recommended_offer_id="operations_automation_os",
        value_angle_ar="فرضية تحسين المتابعة التشغيلية.",
        relationship_status="unknown",
        consent_status="unknown",
        targeting_status="research_only",
        suppression_reasons=("permission_not_proven",),
    )

    signal = signal_from_directory_candidate(
        candidate,
        tenant_id="dealix",
        evidence_ref="internal:directory-import:abc123",
        observed_at="2026-07-15T00:00:00Z",
    )
    bundle = run_revenue_lab([signal])

    assert signal.permission == "research_only"
    assert bundle.approval_requests[0]["status"] == "blocked"
    assert bundle.opportunities[0].next_action == "validate_sources_and_permission"
