"""Tests for the unified Autonomous Distribution Engine."""

from __future__ import annotations

import pytest

from auto_client_acquisition.adoption_os import AdoptionDimensions
from auto_client_acquisition.autonomous_distribution import (
    assemble_proof_pack,
    assess_retainer,
    process_lead,
    process_payment,
)
from auto_client_acquisition.autonomous_distribution.engine import (
    DISCLAIMER_AR_EN,
    audit_outreach_draft,
)
from auto_client_acquisition.compliance_trust_os.approval_engine import (
    GovernanceDecision,
)
from auto_client_acquisition.data_os import SourcePassport
from auto_client_acquisition.sales_os import ICPDimensions


def _passport(source_type: str = "inbound_form", ai_ok: bool = True) -> SourcePassport:
    return SourcePassport(
        source_id="t1",
        source_type=source_type,
        owner="founder",
        allowed_use=frozenset({"ai_processing", "internal_analysis"}),
        contains_pii=False,
        sensitivity="internal",
        retention_policy="90_days",
        ai_access_allowed=ai_ok,
        external_use_allowed=False,
    )


def _icp(high: bool = True) -> ICPDimensions:
    if high:
        return ICPDimensions(
            b2b_service_fit=80,
            data_maturity=70,
            governance_posture=75,
            budget_signal=70,
            decision_velocity=65,
        )
    return ICPDimensions(
        b2b_service_fit=20,
        data_maturity=10,
        governance_posture=20,
        budget_signal=10,
        decision_velocity=20,
    )


def _full_answers() -> dict:
    return {
        "pain_clear": True,
        "owner_present": True,
        "data_available": True,
        "accepts_governance": True,
        "has_budget": True,
        "wants_safe_methods": True,
        "proof_path_visible": True,
        "retainer_path_visible": True,
    }


class TestProcessLead:
    def test_accept_high_quality_warm_inbound(self):
        d = process_lead(
            lead_row={"company_name": "Acme", "sector": "fintech", "city": "Riyadh"},
            source_passport=_passport(),
            icp_dims=_icp(True),
            discovery_answers=_full_answers(),
            raw_request_text="We need governed AI ops",
        )
        assert d.governance_decision is GovernanceDecision.REQUIRE_APPROVAL
        assert d.recommended_offer == "revenue_intelligence_sprint"
        assert d.rung == 1
        assert d.icp >= 60
        assert d.dq_score > 0
        assert "qualification:accept" in d.evidence_refs

    def test_block_scraping_source(self):
        d = process_lead(
            lead_row={"company_name": "X"},
            source_passport=_passport(source_type="scraping"),
            icp_dims=_icp(True),
            discovery_answers=_full_answers(),
        )
        assert d.governance_decision is GovernanceDecision.BLOCK
        assert d.rung == -1
        assert any("blocked_source" in v or "scraping" in v for v in d.doctrine_violations)

    def test_block_doctrine_violation_in_text(self):
        d = process_lead(
            lead_row={"company_name": "Acme"},
            source_passport=_passport(),
            icp_dims=_icp(True),
            discovery_answers=_full_answers(),
            raw_request_text="We want to scrape LinkedIn for leads",
        )
        assert d.governance_decision is GovernanceDecision.BLOCK
        assert "scraping" in d.doctrine_violations

    def test_low_icp_routes_to_diagnostic(self):
        ans = _full_answers()
        ans["data_available"] = False
        ans["has_budget"] = False
        ans["proof_path_visible"] = False
        d = process_lead(
            lead_row={"company_name": "Acme"},
            source_passport=_passport(),
            icp_dims=_icp(False),
            discovery_answers=ans,
        )
        assert d.rung in (0, -1)

    def test_to_dict_serializable(self):
        d = process_lead(
            lead_row={"company_name": "Acme", "sector": "fintech", "city": "Riyadh"},
            source_passport=_passport(),
            icp_dims=_icp(True),
            discovery_answers=_full_answers(),
        )
        out = d.to_dict()
        assert out["governance_decision"] in {v.value for v in GovernanceDecision}
        assert isinstance(out["dq_score"], int)
        assert isinstance(out["evidence_refs"], list)


class TestAuditOutreachDraft:
    def test_email_clean_draft_allowed(self):
        d = audit_outreach_draft(
            "نقدم تشخيص مجاني لتحليل البيانات تحت حوكمة PDPL، اتصل بنا للاستفسار.",
            channel="email",
        )
        assert d.governance_decision is not GovernanceDecision.BLOCK
        assert d.safe_to_queue

    def test_linkedin_always_blocked(self):
        d = audit_outreach_draft("Hi, want to chat?", channel="linkedin")
        assert d.governance_decision is GovernanceDecision.BLOCK
        assert any("linkedin" in r for r in d.reasons)

    def test_whatsapp_always_blocked(self):
        d = audit_outreach_draft("Hello", channel="whatsapp")
        assert d.governance_decision is GovernanceDecision.BLOCK
        assert any("whatsapp" in r for r in d.reasons)

    def test_guaranteed_claim_blocked(self):
        d = audit_outreach_draft(
            "نضمن لك زيادة المبيعات 200% خلال شهرين", channel="email"
        )
        assert d.governance_decision is GovernanceDecision.BLOCK


class TestProcessPayment:
    def test_unpaid_blocked(self):
        d = process_payment(
            invoice_ref="inv_1",
            amount_sar=499.0,
            moyasar_status="pending",
            moyasar_mode="test",
            customer_id="c1",
            rung=1,
            proof_pack_score=85,
        )
        assert d.governance_decision is GovernanceDecision.BLOCK
        assert not d.capital_asset_eligible

    def test_low_proof_pack_no_asset(self):
        d = process_payment(
            invoice_ref="inv_1",
            amount_sar=499.0,
            moyasar_status="paid",
            moyasar_mode="live",
            customer_id="c1",
            rung=1,
            proof_pack_score=50,
        )
        assert d.governance_decision is GovernanceDecision.ALLOW_WITH_REVIEW
        assert not d.capital_asset_eligible

    def test_paid_with_strong_proof_eligible(self):
        d = process_payment(
            invoice_ref="inv_1",
            amount_sar=499.0,
            moyasar_status="paid",
            moyasar_mode="live",
            customer_id="c1",
            rung=1,
            proof_pack_score=85,
        )
        assert d.governance_decision is GovernanceDecision.ALLOW
        assert d.capital_asset_eligible
        assert d.asset_type is not None

    def test_test_mode_still_eligible_but_with_review(self):
        d = process_payment(
            invoice_ref="inv_test_1",
            amount_sar=499.0,
            moyasar_status="paid",
            moyasar_mode="test",
            customer_id="c1",
            rung=1,
            proof_pack_score=85,
        )
        assert d.governance_decision is GovernanceDecision.ALLOW_WITH_REVIEW
        assert d.capital_asset_eligible


class TestAssembleProofPack:
    def test_empty_pack_blocked(self):
        pp = assemble_proof_pack()
        assert pp.governance_decision is GovernanceDecision.BLOCK
        assert not pp.publish_eligible
        assert pp.score == 0

    def test_complete_pack_publish_eligible(self):
        sections = {
            "executive_summary": "Delivered Revenue Intelligence Sprint",
            "problem": "Sales lacked source attribution",
            "inputs": "CRM, Calendly",
            "source_passports": "inbound_form Tier 1",
            "work_completed": "Source passport ledger",
            "outputs": "DQ dashboard",
            "quality_scores": "DQ=82",
            "governance_decisions": "0 violations",
            "blocked_risks": "no PII external",
            "value_metrics": "+22% conv (estimated)",
            "limitations": "Estimated != verified",
            "recommended_next_step": "Move to Data Pack",
            "retainer_expansion_path": "Eligible in 30d",
            "capital_assets_created": "Source passport template",
        }
        pp = assemble_proof_pack(sections=sections)
        assert pp.publish_eligible
        assert pp.score_with_penalty >= 70
        assert pp.governance_decision is GovernanceDecision.REQUIRE_APPROVAL

    def test_governance_penalty_drops_score(self):
        sections = {
            "executive_summary": "X",
            "problem": "X",
            "inputs": "X",
            "source_passports": "X",
            "work_completed": "X",
            "outputs": "X",
            "quality_scores": "X",
            "governance_decisions": "X",
            "blocked_risks": "X",
            "value_metrics": "X",
            "limitations": "X",
            "recommended_next_step": "X",
            "retainer_expansion_path": "X",
            "capital_assets_created": "X",
        }
        clean = assemble_proof_pack(sections=sections, governance_blocked=False)
        penalized = assemble_proof_pack(sections=sections, governance_blocked=True)
        assert penalized.score_with_penalty <= clean.score_with_penalty


class TestAssessRetainer:
    def test_eligible_when_all_gates_pass(self):
        ad = AdoptionDimensions(
            executive_sponsor=80,
            workflow_owner=80,
            data_readiness=80,
            user_engagement=80,
            approval_completion=80,
            proof_visibility=80,
            monthly_cadence=80,
            expansion_pull=80,
        )
        r = assess_retainer(
            adoption_dims=ad,
            customer_id="c1",
            proof_score=85,
            workflow_owner_exists=True,
            monthly_workflow_exists=True,
            governance_risk_controlled=True,
        )
        assert r.eligible
        assert r.governance_decision is GovernanceDecision.REQUIRE_APPROVAL

    def test_blocked_when_missing_gate(self):
        ad = AdoptionDimensions(
            executive_sponsor=80,
            workflow_owner=80,
            data_readiness=80,
            user_engagement=80,
            approval_completion=80,
            proof_visibility=80,
            monthly_cadence=80,
            expansion_pull=80,
        )
        r = assess_retainer(
            adoption_dims=ad,
            customer_id="c1",
            proof_score=85,
            workflow_owner_exists=False,
            monthly_workflow_exists=True,
            governance_risk_controlled=True,
        )
        assert not r.eligible
        assert r.governance_decision is GovernanceDecision.BLOCK
        assert r.blockers


class TestDisclaimer:
    def test_disclaimer_bilingual(self):
        assert "Estimated value" in DISCLAIMER_AR_EN
        assert "القيمة التقديرية" in DISCLAIMER_AR_EN
