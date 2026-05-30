"""
Tests for the Dealix Commercial Engine (class-based API).
اختبارات ماكينة التجارة في Dealix.
"""
from __future__ import annotations

import uuid

import pytest


# ── Diagnostic Engine ─────────────────────────────────────────────


class TestDiagnosticEngine:
    def test_diagnostic_request_defaults(self) -> None:
        from dealix.commercial.diagnostic_engine import DiagnosticRequest

        req = DiagnosticRequest(company_name="شركة اختبار")
        assert req.sector == "b2b_services"
        assert req.company_name == "شركة اختبار"

    def test_generate_returns_10_sections(self) -> None:
        from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest

        req = DiagnosticRequest(
            company_name="وكالة الإبداع",
            sector="marketing_agency",
            pain_points=["lead_gen", "sales_close"],
        )
        report = DiagnosticEngine().generate(req)
        assert len(report.sections) == 10
        assert report.company_name == "وكالة الإبداع"

    def test_report_has_arabic_content(self) -> None:
        from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest

        req = DiagnosticRequest(company_name="اختبار", sector="consulting")
        report = DiagnosticEngine().generate(req)
        assert "اختبار" in report.markdown_ar_en
        assert report.report_id

    def test_report_approval_status(self) -> None:
        from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest

        req = DiagnosticRequest(company_name="اختبار")
        report = DiagnosticEngine().generate(req)
        assert report.approval_status == "approval_required"

    def test_to_dict_serializable(self) -> None:
        from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest

        req = DiagnosticRequest(company_name="اختبار")
        report = DiagnosticEngine().generate(req)
        d = report.to_dict()
        assert "report_id" in d
        assert "sections" in d
        assert isinstance(d["sections"], list)


# ── Warm Intro Generator ──────────────────────────────────────────


class TestWarmIntroGenerator:
    def test_no_live_send_gate(self) -> None:
        from dealix.commercial.warm_intro_generator import _NO_LIVE_SEND

        assert _NO_LIVE_SEND is True, "NO_LIVE_SEND gate must always be True"

    def test_whatsapp_bundle_structure(self) -> None:
        from dealix.commercial.warm_intro_generator import WarmIntroGenerator, WarmIntroRequest

        req = WarmIntroRequest(
            prospect_name="أحمد",
            company_name="شركة اختبار",
            sector="marketing_agency",
        )
        bundle = WarmIntroGenerator().generate(req)
        assert bundle.bundle_id
        assert bundle.company_name == "شركة اختبار"
        assert len(bundle.whatsapp_drafts) == 5
        for draft in bundle.whatsapp_drafts:
            assert draft.approval_status == "approval_required"
            assert draft.channel == "whatsapp"
            assert draft.body_ar

    def test_email_bundle_structure(self) -> None:
        from dealix.commercial.warm_intro_generator import WarmIntroGenerator, WarmIntroRequest

        req = WarmIntroRequest(
            prospect_name="Ahmed",
            company_name="Test Company",
            sector="consulting",
        )
        bundle = WarmIntroGenerator().generate(req)
        assert len(bundle.email_drafts) == 3
        for draft in bundle.email_drafts:
            assert draft.approval_status == "approval_required"
            assert draft.channel == "email"
            assert draft.subject_line

    def test_all_drafts_pending_approval(self) -> None:
        from dealix.commercial.warm_intro_generator import WarmIntroGenerator, WarmIntroRequest

        req = WarmIntroRequest(prospect_name="X", company_name="شركة ما")
        bundle = WarmIntroGenerator().generate(req)
        for draft in bundle.whatsapp_drafts + bundle.email_drafts:
            assert draft.approval_status == "approval_required"

    def test_bundle_approval_status_in_dict(self) -> None:
        from dealix.commercial.warm_intro_generator import WarmIntroGenerator, WarmIntroRequest

        req = WarmIntroRequest(prospect_name="X", company_name="اختبار")
        bundle = WarmIntroGenerator().generate(req)
        assert bundle.approval_status == "approval_required"
        d = bundle.to_dict()
        assert "approval_status" in d
        assert d["approval_status"] == "approval_required"


# ── Pilot Delivery ────────────────────────────────────────────────


class TestPilotDelivery:
    def test_build_pilot_plan_7_days(self) -> None:
        from dealix.commercial.pilot_delivery import PilotDeliveryKit, PilotStartRequest

        req = PilotStartRequest(
            account_id=str(uuid.uuid4()),
            company_name="شركة اختبار",
            contact_name="أحمد",
            sector="marketing_agency",
            pain_points=["تأخر الرد"],
        )
        plan = PilotDeliveryKit().create_pilot_plan(req)
        assert len(plan.day_plans) == 7
        assert plan.company_name == "شركة اختبار"

    def test_days_have_required_fields(self) -> None:
        from dealix.commercial.pilot_delivery import PilotDeliveryKit, PilotStartRequest

        req = PilotStartRequest(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            sector="other",
        )
        plan = PilotDeliveryKit().create_pilot_plan(req)
        for day in plan.day_plans:
            assert day.title_ar
            assert day.title_en
            assert len(day.tasks_ar) >= 3

    def test_approval_days_flagged(self) -> None:
        from dealix.commercial.pilot_delivery import PilotDeliveryKit, PilotStartRequest

        req = PilotStartRequest(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            sector="other",
        )
        plan = PilotDeliveryKit().create_pilot_plan(req)
        approval_days = [d.day for d in plan.day_plans if d.approval_required]
        assert 3 in approval_days
        assert 4 in approval_days
        assert 5 in approval_days

    def test_day_brief_returns_correct_day(self) -> None:
        from dealix.commercial.pilot_delivery import PilotDeliveryKit, PilotStartRequest

        req = PilotStartRequest(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            sector="other",
        )
        plan = PilotDeliveryKit().create_pilot_plan(req)
        day3 = next(d for d in plan.day_plans if d.day == 3)
        assert day3.day == 3
        assert day3.approval_required is True

    def test_plan_contains_arabic(self) -> None:
        from dealix.commercial.pilot_delivery import PilotDeliveryKit, PilotStartRequest

        req = PilotStartRequest(
            account_id=str(uuid.uuid4()),
            company_name="شركة النجاح",
            sector="other",
        )
        plan = PilotDeliveryKit().create_pilot_plan(req)
        assert "شركة النجاح" in plan.week1_report_template
        assert "2,999" in plan.upsell_script


# ── Proof Builder ─────────────────────────────────────────────────


class TestProofBuilder:
    def test_evidence_level_0_no_events(self) -> None:
        from dealix.commercial.proof_builder import ProofBuilder

        assert ProofBuilder()._compute_level([]) == "L0"

    def test_evidence_level_1_three_events(self) -> None:
        from dealix.commercial.proof_builder import ProofBuilder, ProofEvent

        events = [
            ProofEvent(event_type="reply", description_ar="رد", description_en="reply")
            for _ in range(3)
        ]
        assert ProofBuilder()._compute_level(events) == "L1"

    def test_evidence_level_2_six_events(self) -> None:
        from dealix.commercial.proof_builder import ProofBuilder, ProofEvent

        events = [
            ProofEvent(event_type="meeting", description_ar="اجتماع", description_en="meeting")
            for _ in range(6)
        ]
        assert ProofBuilder()._compute_level(events) == "L2"

    def test_build_proof_pack_complete(self) -> None:
        from dealix.commercial.proof_builder import ProofBuildRequest, ProofBuilder, ProofEvent

        req = ProofBuildRequest(
            account_id=str(uuid.uuid4()),
            company_name="شركة اختبار",
            pilot_id=str(uuid.uuid4()),
            approved_by_founder=True,
            events=[
                ProofEvent(
                    event_type="meeting_booked",
                    description_ar="اجتماع محجوز",
                    description_en="Meeting booked",
                    metric_before="24h",
                    metric_after="0.5h",
                    delta_pct=95.0,
                )
                for _ in range(3)
            ],
        )
        pack = ProofBuilder().build(req)
        assert pack.proof_level == "L1"
        assert "شركة اختبار" in pack.markdown_ar_en
        assert pack.is_fake_proof_gate_passed is True

    def test_no_fake_proof_zero_events(self) -> None:
        from dealix.commercial.proof_builder import ProofBuildRequest, ProofBuilder

        req = ProofBuildRequest(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            approved_by_founder=False,
        )
        pack = ProofBuilder().build(req)
        assert pack.proof_level == "L0"
        assert pack.is_fake_proof_gate_passed is False

    def test_consent_required_for_founder_approval(self) -> None:
        from dealix.commercial.proof_builder import ProofBuildRequest, ProofBuilder

        req = ProofBuildRequest(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            customer_consent=False,
            approved_by_founder=False,
        )
        pack = ProofBuilder().build(req)
        assert pack.is_fake_proof_gate_passed is False

    def test_response_time_improvement_in_markdown(self) -> None:
        from dealix.commercial.proof_builder import ProofBuildRequest, ProofBuilder, ProofEvent

        req = ProofBuildRequest(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            events=[
                ProofEvent(
                    event_type="response_time",
                    description_ar="تحسن وقت الاستجابة",
                    description_en="Response time improved",
                    metric_before="24h",
                    metric_after="1h",
                    delta_pct=95.8,
                )
                for _ in range(3)
            ],
        )
        pack = ProofBuilder().build(req)
        assert "95.8" in pack.markdown_ar_en or "%" in pack.markdown_ar_en


# ── Upsell Engine ─────────────────────────────────────────────────


class TestUpsellEngine:
    def test_not_eligible_with_zero_proof_events(self) -> None:
        from dealix.commercial.upsell_engine import UpsellEngine

        result = UpsellEngine().check(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            proof_event_count=0,
            proof_level="L0",
        )
        assert result.is_eligible is False

    def test_eligible_with_three_l1_events(self) -> None:
        from dealix.commercial.upsell_engine import UpsellEngine

        result = UpsellEngine().check(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            proof_event_count=3,
            proof_level="L1",
        )
        assert result.is_eligible is True
        assert result.recommended_tier == "managed_ops_2999"

    def test_not_eligible_returns_no_proposal(self) -> None:
        from dealix.commercial.upsell_engine import UpsellEngine

        result = UpsellEngine().check(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            proof_event_count=0,
            proof_level="L0",
        )
        assert result.proposal_draft_ar == ""
        assert result.proposal_draft_en == ""

    def test_approval_status_always_required(self) -> None:
        from dealix.commercial.upsell_engine import UpsellEngine

        result = UpsellEngine().check(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            proof_event_count=3,
            proof_level="L1",
        )
        assert result.approval_status == "approval_required"
        d = result.to_dict()
        assert "NO_LIVE_SEND" in result.reason_ar or "approval_required" == d["approval_status"]


# ── Case Study Generator ──────────────────────────────────────────


class TestCaseStudyGenerator:
    def test_quote_requires_consent(self) -> None:
        from dealix.commercial.case_study_generator import CaseStudyGenerator, CaseStudyRequest

        req = CaseStudyRequest(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            customer_quote_ar="ممتاز",
            customer_consent=False,
        )
        with pytest.raises(AssertionError, match="NO_UNAPPROVED_TESTIMONIAL"):
            CaseStudyGenerator().generate(req)

    def test_anonymize_hides_company_name(self) -> None:
        from dealix.commercial.case_study_generator import CaseStudyGenerator, CaseStudyRequest

        req = CaseStudyRequest(
            account_id=str(uuid.uuid4()),
            company_name="شركة سرية",
            anonymize=True,
            customer_consent=False,
        )
        study = CaseStudyGenerator().generate(req)
        assert "شركة سرية" not in study.display_name
        assert "قطاع" in study.display_name or study.display_name != "شركة سرية"

    def test_linkedin_post_shorter_than_full(self) -> None:
        from dealix.commercial.case_study_generator import CaseStudyGenerator, CaseStudyRequest

        req = CaseStudyRequest(
            account_id=str(uuid.uuid4()),
            company_name="شركة اختبار",
            customer_consent=True,
            result_ar="نتيجة رائعة",
            result_en="Great result",
        )
        study = CaseStudyGenerator().generate(req)
        assert len(study.linkedin_post_ar) < len(study.markdown_ar_en)
        assert "#Dealix" in study.linkedin_post_ar
