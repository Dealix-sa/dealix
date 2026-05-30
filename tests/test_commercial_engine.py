"""
Tests for the Dealix Commercial Engine.
اختبارات ماكينة التجارة في Dealix.

Tests:
  - Diagnostic engine (draft generation, fallback, ledger save)
  - Warm intro generator (NO_LIVE_SEND gate, draft bundle)
  - Pilot delivery (7-day plan, day brief)
  - Proof builder (evidence levels, metrics calculation)
  - Upsell engine (gate logic, offer selection)
  - Case study generator (consent gate, NO_UNAPPROVED_TESTIMONIAL)
"""

from __future__ import annotations

import uuid

import pytest


# ── Diagnostic Engine ─────────────────────────────────────────────

class TestDiagnosticEngine:
    def test_diagnostic_request_defaults(self) -> None:
        from dealix.commercial.diagnostic_engine import DiagnosticRequest
        req = DiagnosticRequest(company_name="شركة اختبار")
        assert req.sector == "other"
        assert req.locale == "ar"
        assert req.account_id  # auto-generated

    def test_prompt_generation(self) -> None:
        from dealix.commercial.diagnostic_engine import DiagnosticRequest, _build_prompt
        req = DiagnosticRequest(
            company_name="وكالة الإبداع",
            sector="marketing_agency",
            pain_points="تأخر الرد على العملاء",
        )
        prompt = _build_prompt(req)
        assert "وكالة الإبداع" in prompt
        assert "وكالة تسويق" in prompt
        assert "executive_summary_ar" in prompt

    def test_fallback_data_structure(self) -> None:
        from dealix.commercial.diagnostic_engine import DiagnosticRequest, _fallback_data, _SECTION_PROMPTS
        req = DiagnosticRequest(company_name="اختبار", sector="consulting")
        data = _fallback_data(req)
        assert "executive_summary_ar" in data
        assert "sections" in data
        assert len(data["sections"]) == len(_SECTION_PROMPTS)
        assert data["next_step_ar"]

    def test_markdown_output(self) -> None:
        from dealix.commercial.diagnostic_engine import DiagnosticRequest, DiagnosticReport, DiagnosticSection, _SECTION_PROMPTS
        from datetime import UTC, datetime
        sections = [
            DiagnosticSection(title_ar=ar, title_en=en, content_ar="محتوى", content_en="content")
            for ar, en in _SECTION_PROMPTS[:3]
        ]
        report = DiagnosticReport(
            report_id=str(uuid.uuid4()),
            account_id=str(uuid.uuid4()),
            company_name="شركة الاختبار",
            sector="consulting",
            sections=sections,
            executive_summary_ar="ملخص تجريبي",
            executive_summary_en="Test summary",
            next_step_ar="الخطوة التالية",
            next_step_en="Next step",
            generated_at=datetime.now(UTC),
        )
        md = report.to_markdown_ar()
        assert "شركة الاختبار" in md
        assert "ملخص تجريبي" in md
        assert "الخطوة التالية" in md

    def test_ledger_save(self, tmp_path: "Path") -> None:
        from dealix.commercial.diagnostic_engine import DiagnosticReport, DiagnosticSection, _save_to_ledger
        from datetime import UTC, datetime

        report = DiagnosticReport(
            report_id=str(uuid.uuid4()),
            account_id=str(uuid.uuid4()),
            company_name="شركة تجريبية",
            sector="other",
            sections=[],
            executive_summary_ar="ملخص",
            executive_summary_en="Summary",
            next_step_ar="خطوة",
            next_step_en="Step",
            generated_at=datetime.now(UTC),
        )
        # Should not raise
        _save_to_ledger(report)


# ── Warm Intro Generator ──────────────────────────────────────────

class TestWarmIntroGenerator:
    def test_no_live_send_gate(self) -> None:
        import dealix.commercial.warm_intro_generator as wig
        assert wig._NO_LIVE_SEND is True, "NO_LIVE_SEND gate must always be True"

    @pytest.mark.asyncio
    async def test_whatsapp_bundle_structure(self) -> None:
        from dealix.commercial.warm_intro_generator import ProspectContext, generate_warm_intros
        ctx = ProspectContext(
            company_name="شركة اختبار",
            contact_name="أحمد",
            sector="marketing_agency",
            channel="whatsapp",
            locale="ar",
        )
        bundle = await generate_warm_intros(ctx, num_variants=5)
        assert bundle.bundle_id
        assert bundle.company_name == "شركة اختبار"
        assert len(bundle.drafts) == 5
        for draft in bundle.drafts:
            assert draft.status == "pending_approval"
            assert draft.channel == "whatsapp"
            assert draft.body  # has content
            assert "شركة اختبار" in draft.body

    @pytest.mark.asyncio
    async def test_email_bundle_structure(self) -> None:
        from dealix.commercial.warm_intro_generator import ProspectContext, generate_warm_intros
        ctx = ProspectContext(
            company_name="Test Company",
            contact_name="Ahmed",
            sector="consulting",
            channel="email",
            locale="ar",
        )
        bundle = await generate_warm_intros(ctx, num_variants=3)
        assert len(bundle.drafts) == 3
        for draft in bundle.drafts:
            assert draft.status == "pending_approval"
            assert draft.channel == "email"
            assert draft.subject  # email must have subject

    @pytest.mark.asyncio
    async def test_all_drafts_pending_approval(self) -> None:
        from dealix.commercial.warm_intro_generator import ProspectContext, generate_warm_intros
        ctx = ProspectContext(company_name="شركة ما")
        bundle = await generate_warm_intros(ctx)
        for draft in bundle.drafts:
            assert draft.status == "pending_approval", f"Draft {draft.draft_id} is not pending_approval"

    def test_constitutional_note_in_bundle(self) -> None:
        from dealix.commercial.warm_intro_generator import WarmIntroDraftBundle, WarmIntroDraft
        from datetime import UTC, datetime
        bundle = WarmIntroDraftBundle(
            bundle_id=str(uuid.uuid4()),
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            drafts=[],
        )
        d = bundle.to_dict()
        assert "NO_LIVE_SEND" in d["constitutional_note"]


# ── Pilot Delivery ────────────────────────────────────────────────

class TestPilotDelivery:
    def test_build_pilot_plan_7_days(self) -> None:
        from dealix.commercial.pilot_delivery import PilotContext, build_pilot_plan
        ctx = PilotContext(
            pilot_id=str(uuid.uuid4()),
            account_id=str(uuid.uuid4()),
            company_name="شركة اختبار",
            contact_name="أحمد",
            sector="marketing_agency",
            pain_points="تأخر الرد",
            payment_ref="TEST-001",
            payment_confirmed=True,
        )
        plan = build_pilot_plan(ctx)
        assert len(plan.days) == 7
        assert plan.company_name == "شركة اختبار"
        assert plan.payment_confirmed is True

    def test_days_have_required_fields(self) -> None:
        from dealix.commercial.pilot_delivery import PilotContext, build_pilot_plan
        ctx = PilotContext(
            pilot_id=str(uuid.uuid4()),
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            contact_name="",
            sector="other",
            pain_points="",
            payment_ref="REF-001",
            payment_confirmed=True,
        )
        plan = build_pilot_plan(ctx)
        for day in plan.days:
            assert day.title_ar
            assert day.title_en
            assert len(day.tasks_ar) >= 3
            assert day.deliverable_ar

    def test_approval_days_flagged(self) -> None:
        from dealix.commercial.pilot_delivery import PilotContext, build_pilot_plan
        ctx = PilotContext(
            pilot_id=str(uuid.uuid4()),
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            contact_name="",
            sector="other",
            pain_points="",
            payment_ref="REF-001",
            payment_confirmed=True,
        )
        plan = build_pilot_plan(ctx)
        # Days 3, 4, 5 should require approval
        approval_days = [d.day for d in plan.days if d.requires_approval]
        assert 3 in approval_days
        assert 4 in approval_days
        assert 5 in approval_days

    def test_day_brief_returns_correct_day(self) -> None:
        from dealix.commercial.pilot_delivery import PilotContext, build_pilot_plan, get_day_brief
        ctx = PilotContext(
            pilot_id=str(uuid.uuid4()),
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            contact_name="",
            sector="other",
            pain_points="",
            payment_ref="REF-001",
            payment_confirmed=True,
        )
        plan = build_pilot_plan(ctx)
        brief = get_day_brief(plan, 3)
        assert brief["day"] == 3
        assert brief["requires_approval"] is True

    def test_markdown_contains_arabic(self) -> None:
        from dealix.commercial.pilot_delivery import PilotContext, build_pilot_plan
        ctx = PilotContext(
            pilot_id=str(uuid.uuid4()),
            account_id=str(uuid.uuid4()),
            company_name="شركة النجاح",
            contact_name="",
            sector="other",
            pain_points="",
            payment_ref="REF-001",
            payment_confirmed=True,
        )
        plan = build_pilot_plan(ctx)
        md = plan.to_markdown_ar()
        assert "شركة النجاح" in md
        assert "499" in md
        assert "اليوم" in md


# ── Proof Builder ─────────────────────────────────────────────────

class TestProofBuilder:
    def test_evidence_level_0_no_messages(self) -> None:
        from dealix.commercial.proof_builder import ProofEvidence, _calculate_evidence_level
        ev = ProofEvidence()
        assert _calculate_evidence_level(ev) == 0

    def test_evidence_level_1_sprint_proof(self) -> None:
        from dealix.commercial.proof_builder import ProofEvidence, _calculate_evidence_level
        ev = ProofEvidence(
            messages_sent=3,
            replies_received=1,
            proof_events=[{"type": "reply"}],
        )
        assert _calculate_evidence_level(ev) >= 1

    def test_evidence_level_2_data_pack(self) -> None:
        from dealix.commercial.proof_builder import ProofEvidence, _calculate_evidence_level
        ev = ProofEvidence(
            messages_sent=5,
            replies_received=2,
            proof_events=[{"type": "reply"}, {"type": "meeting"}],
        )
        assert _calculate_evidence_level(ev) >= 2

    def test_build_proof_pack_complete(self) -> None:
        from dealix.commercial.proof_builder import ProofEvidence, build_proof_pack
        ev = ProofEvidence(
            messages_drafted=6,
            messages_sent=6,
            replies_received=2,
            meetings_booked=1,
            response_time_before_hours=24.0,
            response_time_after_hours=0.5,
            proof_events=[{"type": "meeting_booked"}],
        )
        pack = build_proof_pack(
            pilot_id=str(uuid.uuid4()),
            account_id=str(uuid.uuid4()),
            company_name="شركة اختبار",
            contact_name="أحمد",
            sector="marketing_agency",
            pain_point="تأخر الرد",
            evidence=ev,
        )
        assert pack.is_complete is True
        assert pack.evidence_level >= 1
        assert "شركة اختبار" in pack.to_markdown_ar()

    def test_no_fake_proof_zero_evidence(self) -> None:
        from dealix.commercial.proof_builder import ProofEvidence, build_proof_pack
        ev = ProofEvidence()  # all zeros
        pack = build_proof_pack(
            pilot_id=str(uuid.uuid4()),
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            contact_name="",
            sector="other",
            pain_point="",
            evidence=ev,
        )
        assert pack.evidence_level == 0
        assert pack.is_complete is False

    def test_response_time_improvement_calculation(self) -> None:
        from dealix.commercial.proof_builder import _response_time_improvement
        result = _response_time_improvement(24.0, 0.5)
        assert "%" in result
        assert "تحسّن" in result or "improvement" in result.lower() or "%" in result

    def test_can_use_as_case_study_requires_consent(self) -> None:
        from dealix.commercial.proof_builder import ProofEvidence, build_proof_pack
        ev = ProofEvidence(
            messages_sent=3,
            replies_received=1,
            proof_events=[{"type": "reply"}],
            testimonial_text="ممتاز",
            testimonial_consented=False,  # No consent
        )
        pack = build_proof_pack(
            pilot_id=str(uuid.uuid4()),
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            contact_name="",
            sector="other",
            pain_point="",
            evidence=ev,
        )
        assert pack.can_use_as_case_study is False


# ── Upsell Engine ─────────────────────────────────────────────────

class TestUpsellEngine:
    def test_all_gated_with_zero_pilots(self) -> None:
        from dealix.commercial.upsell_engine import evaluate_upsell
        opps = evaluate_upsell(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            sector="other",
            pain_point="",
            pilot_count=0,
            proof_event_count=0,
            evidence_level=0,
        )
        eligible = [o for o in opps if not o.is_gated]
        assert len(eligible) == 0, "No offers should be eligible with 0 pilots"

    def test_s3_eligible_after_one_pilot(self) -> None:
        from dealix.commercial.upsell_engine import evaluate_upsell
        opps = evaluate_upsell(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            sector="marketing_agency",
            pain_point="تأخر الرد",
            pilot_count=1,
            proof_event_count=1,
            evidence_level=1,
        )
        eligible_keys = {o.offer_key for o in opps if not o.is_gated}
        assert "s3_managed_ops" in eligible_keys, "s3_managed_ops should be eligible after 1 pilot + 1 proof event"

    def test_best_upsell_returns_none_when_gated(self) -> None:
        from dealix.commercial.upsell_engine import best_upsell
        result = best_upsell(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            sector="other",
            pain_point="",
            pilot_count=0,
            proof_event_count=0,
            evidence_level=0,
        )
        assert result is None

    def test_all_pending_approval_status(self) -> None:
        from dealix.commercial.upsell_engine import evaluate_upsell
        opps = evaluate_upsell(
            account_id=str(uuid.uuid4()),
            company_name="اختبار",
            sector="other",
            pain_point="",
            pilot_count=1,
            proof_event_count=1,
            evidence_level=1,
        )
        for opp in opps:
            assert opp.status == "pending_approval"
        # All have constitutional note
        for opp in opps:
            d = opp.to_dict()
            assert "NO_LIVE_SEND" in d["constitutional_note"]


# ── Case Study Generator ──────────────────────────────────────────

class TestCaseStudyGenerator:
    def test_requires_consent_ref(self) -> None:
        from dealix.commercial.case_study_generator import CaseStudyConsent, build_case_study
        consent = CaseStudyConsent(
            customer_name="أحمد",
            company_name="اختبار",
            consent_type="full_named",
            consent_date="2026-01-01",
            consent_ref="",  # Empty — should fail
            signed_by="أحمد",
        )
        pack_data = {
            "company_name": "اختبار",
            "sector": "other",
        }
        with pytest.raises(ValueError, match="NO_UNAPPROVED_TESTIMONIAL"):
            build_case_study(
                pack_id=str(uuid.uuid4()),
                pack_data=pack_data,
                consent=consent,
            )

    def test_anonymous_consent_hides_company_name(self) -> None:
        from dealix.commercial.case_study_generator import CaseStudyConsent, build_case_study
        consent = CaseStudyConsent(
            customer_name="أحمد",
            company_name="شركة سرية",
            consent_type="anonymous",
            consent_date="2026-01-01",
            consent_ref="CONSENT-001",
            signed_by="أحمد",
        )
        pack_data = {
            "company_name": "شركة سرية",
            "sector": "consulting",
        }
        study = build_case_study(
            pack_id=str(uuid.uuid4()),
            pack_data=pack_data,
            consent=consent,
        )
        assert "شركة سرية" not in study.company_name
        assert "قطاع" in study.company_name  # Should be anonymized

    def test_linkedin_format_shorter(self) -> None:
        from dealix.commercial.case_study_generator import CaseStudyConsent, build_case_study
        consent = CaseStudyConsent(
            customer_name="أحمد",
            company_name="شركة اختبار",
            consent_type="full_named",
            consent_date="2026-01-01",
            consent_ref="CONSENT-002",
            signed_by="أحمد",
        )
        pack_data = {
            "company_name": "شركة اختبار",
            "sector": "marketing_agency",
            "messages_sent": 6,
            "replies_received": 2,
        }
        study = build_case_study(
            pack_id=str(uuid.uuid4()),
            pack_data=pack_data,
            consent=consent,
        )
        linkedin_md = study.to_markdown_ar(for_linkedin=True)
        full_md = study.to_markdown_ar(for_linkedin=False)
        assert len(linkedin_md) < len(full_md)
        assert "#Dealix" in linkedin_md
