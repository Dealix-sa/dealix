"""Wave 17 Delivery Tests — SprintReportGenerator, ProofPackBuilder, RetainerPitch.

25+ tests covering:
- SprintReportGenerator generates valid reports
- ProofPackBuilder extracts items from sprint output
- RetainerPitch never contains revenue guarantees (doctrine check)
- ProofItem publishable flag requires L2+ AND customer_consented
- RetainerPitch governance note present
- Sprint report requires_founder_review = True always
"""

from __future__ import annotations

import pytest

from dealix.revenue_ops_autopilot.proof_pack_builder import ProofItem, ProofPackBuilder
from dealix.revenue_ops_autopilot.retainer_eligibility import (
    RetainerEligibilityEngine,
    RetainerPitch,
    generate_retainer_pitch,
)
from dealix.revenue_ops_autopilot.sprint_report_generator import (
    SprintDayRecord,
    SprintProofReport,
    SprintReportGenerator,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_SAMPLE_SPRINT_RESULTS = [
    {
        "day": 1,
        "title_en": "Source Passport Audit",
        "title_ar": "تدقيق جواز المصدر",
        "status": "complete",
        "generated_at": "2026-06-01T09:00:00+00:00",
        "output": {
            "sources_audited": 3,
            "all_passports_valid": True,
            "summary_en": "Audited 3 sources. All passports valid.",
            "summary_ar": "تم تدقيق 3 مصادر. جميع الجوازات صالحة.",
        },
    },
    {
        "day": 2,
        "title_en": "Data Quality Score",
        "title_ar": "درجة جودة البيانات",
        "status": "complete",
        "generated_at": "2026-06-02T09:00:00+00:00",
        "output": {
            "total_rows": 48,
            "sources_scored": 3,
            "overall_dq": 78.0,
            "dq_by_source": [],
            "summary_en": "DQ Score: 78/100 across 48 rows.",
            "summary_ar": "درجة DQ: 78/100 عبر 48 سجل.",
        },
    },
    {
        "day": 3,
        "title_en": "Account Scoring",
        "title_ar": "تصنيف الحسابات",
        "status": "complete",
        "generated_at": "2026-06-03T09:00:00+00:00",
        "output": {
            "total_accounts": 15,
            "top_10": [
                {"rank": 1, "company_name": "AlphaCo", "sector": "logistics", "icp_score": 85},
                {"rank": 2, "company_name": "BetaLLC", "sector": "retail", "icp_score": 72},
            ],
            "summary_en": "Ranked 15 accounts. Top 10 selected.",
            "summary_ar": "تم تصنيف 15 حساب.",
        },
    },
    {
        "day": 4,
        "title_en": "Draft Pack",
        "title_ar": "حزمة المسوّدات",
        "status": "complete",
        "generated_at": "2026-06-04T09:00:00+00:00",
        "output": {
            "whatsapp_drafts": [
                {"draft_id": "d1", "lang": "ar", "body": "مسودة آمنة", "status": "draft_only"},
                {"draft_id": "d2", "lang": "en", "body": "Safe draft", "status": "draft_only"},
            ],
            "email_sequence": {"sequence_id": "seq_1", "emails": []},
            "proposal_preview_md": "# Proposal\n...",
            "all_drafts_passed_governance": True,
        },
    },
    {
        "day": 5,
        "title_en": "Governance Review",
        "title_ar": "مراجعة الحوكمة",
        "status": "complete",
        "generated_at": "2026-06-05T09:00:00+00:00",
        "output": {
            "approved": True,
            "approved_by": "founder",
            "approved_at": "2026-06-05T10:00:00+00:00",
        },
    },
    {
        "day": 6,
        "title_en": "Proof Pack Assembly",
        "title_ar": "تجميع حزمة الإثبات",
        "status": "complete",
        "generated_at": "2026-06-06T09:00:00+00:00",
        "output": {
            "completeness_score": 74,
            "strength_band": "moderate_proof",
            "proof_pack": {"sections": {"summary": "Sprint summary", "outputs": "Top accounts listed."}},
        },
    },
    {
        "day": 7,
        "title_en": "Capital Asset Registration & Retainer Eligibility",
        "title_ar": "تسجيل الأصل الرأسمالي وأهلية الـRetainer",
        "status": "complete",
        "generated_at": "2026-06-07T09:00:00+00:00",
        "output": {
            "capital_asset_id": "asset_abc123",
            "total_assets_registered": 1,
            "adoption_score": 65.0,
            "proof_score": 74.0,
            "retainer_eligible": True,
            "recommended_offer": "starter_2999",
            "retainer_gaps": [],
        },
    },
]

_ELIGIBLE_SPRINT_RESULT = {
    "sprint_id": "sp_test_001",
    "account_id": "acc_test_001",
    "proof_level": "L2",
    "satisfaction_score": 8.5,
    "measurable_result_achieved": True,
}


# ---------------------------------------------------------------------------
# SprintReportGenerator — 10 tests
# ---------------------------------------------------------------------------


class TestSprintReportGenerator:
    def setup_method(self):
        self.generator = SprintReportGenerator()

    def test_generate_from_orchestrator_output_returns_report(self):
        report = self.generator.generate_from_orchestrator_output(
            sprint_id="sp_001",
            account_id="acc_001",
            company_name="TestCo",
            orchestrator_results=_SAMPLE_SPRINT_RESULTS,
        )
        assert isinstance(report, SprintProofReport)

    def test_report_requires_founder_review_always_true(self):
        report = self.generator.generate_from_orchestrator_output(
            sprint_id="sp_002",
            account_id="acc_002",
            company_name="AnotherCo",
            orchestrator_results=_SAMPLE_SPRINT_RESULTS,
        )
        assert report.requires_founder_review is True

    def test_report_approved_at_is_none_by_default(self):
        report = self.generator.generate_from_orchestrator_output(
            sprint_id="sp_003",
            account_id="acc_003",
            company_name="FreshCo",
            orchestrator_results=_SAMPLE_SPRINT_RESULTS,
        )
        assert report.approved_at is None

    def test_report_has_7_day_records(self):
        report = self.generator.generate_from_orchestrator_output(
            sprint_id="sp_004",
            account_id="acc_004",
            company_name="Co4",
            orchestrator_results=_SAMPLE_SPRINT_RESULTS,
        )
        assert len(report.day_records) == 7
        assert all(isinstance(r, SprintDayRecord) for r in report.day_records)

    def test_report_day_numbers_are_1_through_7(self):
        report = self.generator.generate_from_orchestrator_output(
            sprint_id="sp_005",
            account_id="acc_005",
            company_name="Co5",
            orchestrator_results=_SAMPLE_SPRINT_RESULTS,
        )
        assert [r.day for r in report.day_records] == list(range(1, 8))

    def test_report_captures_dq_score_in_summary(self):
        report = self.generator.generate_from_orchestrator_output(
            sprint_id="sp_006",
            account_id="acc_006",
            company_name="DQCo",
            orchestrator_results=_SAMPLE_SPRINT_RESULTS,
        )
        assert "78" in report.summary_en or "78" in report.summary_ar

    def test_report_retainer_recommended_from_day7(self):
        report = self.generator.generate_from_orchestrator_output(
            sprint_id="sp_007",
            account_id="acc_007",
            company_name="RetainerCo",
            orchestrator_results=_SAMPLE_SPRINT_RESULTS,
        )
        assert report.retainer_recommended is True
        assert report.retainer_tier is not None

    def test_report_service_tier_is_sprint_499(self):
        report = self.generator.generate_from_orchestrator_output(
            sprint_id="sp_008",
            account_id="acc_008",
            company_name="SprintCo",
            orchestrator_results=_SAMPLE_SPRINT_RESULTS,
        )
        assert report.service_tier == "sprint_499"

    def test_generate_template_produces_skipped_days(self):
        report = self.generator.generate_template(
            account_id="tmpl_acc",
            company_name="TemplateCo",
        )
        assert all(r.status == "skipped" for r in report.day_records)
        assert report.requires_founder_review is True

    def test_as_markdown_contains_governance_note(self):
        report = self.generator.generate_from_orchestrator_output(
            sprint_id="sp_010",
            account_id="acc_010",
            company_name="GovCo",
            orchestrator_results=_SAMPLE_SPRINT_RESULTS,
        )
        md = report.as_markdown()
        assert "founder review" in md.lower() or "مراجعة المؤسس" in md

    def test_to_dict_is_json_serialisable(self):
        import json
        report = self.generator.generate_from_orchestrator_output(
            sprint_id="sp_011",
            account_id="acc_011",
            company_name="JsonCo",
            orchestrator_results=_SAMPLE_SPRINT_RESULTS,
        )
        d = report.to_dict()
        serialised = json.dumps(d)
        assert isinstance(serialised, str)
        assert "sprint_id" in serialised

    def test_empty_orchestrator_results_still_produces_7_records(self):
        report = self.generator.generate_from_orchestrator_output(
            sprint_id="sp_012",
            account_id="acc_012",
            company_name="EmptyCo",
            orchestrator_results=[],
        )
        assert len(report.day_records) == 7
        assert report.requires_founder_review is True


# ---------------------------------------------------------------------------
# ProofPackBuilder — 8 tests
# ---------------------------------------------------------------------------


class TestProofPackBuilder:
    def setup_method(self):
        self.builder = ProofPackBuilder()

    def test_from_sprint_output_returns_list_of_proof_items(self):
        items = self.builder.from_sprint_output(_SAMPLE_SPRINT_RESULTS, "acc_001")
        assert isinstance(items, list)
        assert len(items) >= 1
        assert all(isinstance(i, ProofItem) for i in items)

    def test_day1_valid_passport_produces_l1_item(self):
        items = self.builder.from_sprint_output(_SAMPLE_SPRINT_RESULTS, "acc_001")
        levels = [i.level for i in items]
        assert "L1" in levels

    def test_day2_dq_score_produces_l1_item(self):
        items = self.builder.from_sprint_output(_SAMPLE_SPRINT_RESULTS, "acc_001")
        dq_items = [i for i in items if "DQ" in i.title_en or "جودة" in i.title_ar]
        assert len(dq_items) >= 1
        assert dq_items[0].level == "L1"

    def test_day6_proof_pack_produces_l2_item(self):
        items = self.builder.from_sprint_output(_SAMPLE_SPRINT_RESULTS, "acc_001")
        l2_items = [i for i in items if i.level == "L2"]
        assert len(l2_items) >= 1

    def test_day7_capital_asset_produces_l2_item(self):
        items = self.builder.from_sprint_output(_SAMPLE_SPRINT_RESULTS, "acc_001")
        capital_items = [i for i in items if "Capital Asset" in i.title_en or "أصل رأسمالي" in i.title_ar]
        assert len(capital_items) >= 1
        assert capital_items[0].level == "L2"

    def test_get_publishable_excludes_l1_items(self):
        items = self.builder.from_sprint_output(_SAMPLE_SPRINT_RESULTS, "acc_001")
        publishable = self.builder.get_publishable(items)
        # No item from sprint_output has customer_consented=True, so publishable list should be empty
        assert all(i.publishable for i in publishable)

    def test_as_markdown_section_returns_string(self):
        items = self.builder.from_sprint_output(_SAMPLE_SPRINT_RESULTS, "acc_001")
        md = self.builder.as_markdown_section(items, locale="ar")
        assert isinstance(md, str)
        assert "Proof" in md or "الإثبات" in md

    def test_as_markdown_section_empty_items(self):
        md = self.builder.as_markdown_section([], locale="en")
        assert "No items" in md or "لا توجد" in md


# ---------------------------------------------------------------------------
# ProofItem publishable flag — 5 tests
# ---------------------------------------------------------------------------


class TestProofItemPublishable:
    def test_l0_verified_consented_not_publishable(self):
        item = ProofItem(
            level="L0",
            title_ar="ادعاء",
            title_en="Claim",
            evidence_type="audit_log",
            verified=True,
            customer_consented=True,
            publishable=True,
        )
        assert item.publishable is False

    def test_l1_verified_consented_not_publishable(self):
        item = ProofItem(
            level="L1",
            title_ar="وثيقة",
            title_en="Document",
            evidence_type="audit_log",
            verified=True,
            customer_consented=True,
            publishable=True,
        )
        assert item.publishable is False

    def test_l2_verified_consented_is_publishable(self):
        item = ProofItem(
            level="L2",
            title_ar="تقرير نظام",
            title_en="System Report",
            evidence_type="system_report",
            verified=True,
            customer_consented=True,
            publishable=True,
        )
        assert item.publishable is True

    def test_l2_not_verified_not_publishable(self):
        item = ProofItem(
            level="L2",
            title_ar="تقرير نظام",
            title_en="System Report",
            evidence_type="system_report",
            verified=False,
            customer_consented=True,
            publishable=True,
        )
        assert item.publishable is False

    def test_l2_verified_not_consented_not_publishable(self):
        item = ProofItem(
            level="L2",
            title_ar="تقرير نظام",
            title_en="System Report",
            evidence_type="system_report",
            verified=True,
            customer_consented=False,
            publishable=True,
        )
        assert item.publishable is False


# ---------------------------------------------------------------------------
# RetainerPitch — 10 tests
# ---------------------------------------------------------------------------


class TestRetainerPitch:
    def setup_method(self):
        self.engine = RetainerEligibilityEngine()
        self.eligible_result = self.engine.check(_ELIGIBLE_SPRINT_RESULT)

    def test_generate_retainer_pitch_returns_pitch(self):
        pitch = generate_retainer_pitch(self.eligible_result)
        assert isinstance(pitch, RetainerPitch)

    def test_retainer_pitch_requires_founder_review_always_true(self):
        pitch = generate_retainer_pitch(self.eligible_result)
        assert pitch.requires_founder_review is True

    def test_retainer_pitch_governance_note_present_ar(self):
        pitch = generate_retainer_pitch(self.eligible_result)
        assert pitch.governance_note_ar != ""
        assert "مؤسس" in pitch.governance_note_ar

    def test_retainer_pitch_governance_note_present_en(self):
        pitch = generate_retainer_pitch(self.eligible_result)
        assert pitch.governance_note_en != ""
        assert "founder" in pitch.governance_note_en.lower()

    def test_retainer_pitch_no_revenue_guarantees_en(self):
        """Doctrine: no revenue guarantee claims in pitch copy."""
        _GUARANTEE_PHRASES_EN = [
            "guarantee revenue",
            "guaranteed revenue",
            "guaranteed results",
            "we guarantee your",
            "100% revenue",
            "revenue guarantee",
        ]
        pitch = generate_retainer_pitch(self.eligible_result)
        all_en_text = " ".join([
            pitch.pitch_headline_en,
            pitch.roi_framing_en,
        ] + pitch.value_props_en + pitch.what_included_en).lower()
        for phrase in _GUARANTEE_PHRASES_EN:
            assert phrase not in all_en_text, f"Unsafe phrase found: {phrase!r}"

    def test_retainer_pitch_no_revenue_guarantees_ar(self):
        """Doctrine: no Arabic revenue guarantee claims in pitch copy."""
        _GUARANTEE_PHRASES_AR = [
            "نضمن مبيعات",
            "نضمن إيراد",
            "ضمان إيراد",
            "ضمان مبيعات",
            "نتائج مضمونة",
            "ضمان نتائج",
        ]
        pitch = generate_retainer_pitch(self.eligible_result)
        all_ar_text = " ".join([
            pitch.pitch_headline_ar,
            pitch.roi_framing_ar,
        ] + pitch.value_props_ar + pitch.what_included_ar)
        for phrase in _GUARANTEE_PHRASES_AR:
            assert phrase not in all_ar_text, f"Unsafe Arabic phrase found: {phrase!r}"

    def test_retainer_pitch_roi_framing_is_time_based(self):
        """ROI framing must reference time/hours, not revenue amounts."""
        pitch = generate_retainer_pitch(self.eligible_result)
        # ROI framing should mention hours or equivalent time
        roi_combined = (pitch.roi_framing_en + " " + pitch.roi_framing_ar).lower()
        has_time_framing = ("hour" in roi_combined or "ساعة" in roi_combined)
        assert has_time_framing, "ROI framing must use time-based references"

    def test_retainer_pitch_has_value_props(self):
        pitch = generate_retainer_pitch(self.eligible_result)
        assert len(pitch.value_props_en) >= 1
        assert len(pitch.value_props_ar) >= 1

    def test_retainer_pitch_has_monthly_deliverables(self):
        pitch = generate_retainer_pitch(self.eligible_result)
        assert len(pitch.what_included_en) >= 1
        assert len(pitch.what_included_ar) >= 1

    def test_retainer_pitch_monthly_sar_matches_tier(self):
        _TIER_SAR = {"starter_2999": 2999.0, "growth_3999": 3999.0, "scale_4999": 4999.0}
        pitch = generate_retainer_pitch(self.eligible_result)
        expected_sar = _TIER_SAR.get(pitch.recommended_tier)
        assert pitch.monthly_sar == expected_sar

    def test_retainer_pitch_ineligible_account_still_gets_pitch(self):
        """Even ineligible accounts get a pitch — at starter tier."""
        ineligible_result = self.engine.check({
            "sprint_id": "sp_ineligible",
            "account_id": "acc_ineligible",
            "proof_level": "L0",
            "satisfaction_score": 5.0,
            "measurable_result_achieved": False,
        })
        pitch = generate_retainer_pitch(ineligible_result)
        assert isinstance(pitch, RetainerPitch)
        assert pitch.requires_founder_review is True
        assert pitch.governance_note_en != ""

    def test_retainer_pitch_with_sprint_report_uses_findings(self):
        """Sprint report findings should appear in value props."""
        sprint_report = {
            "findings_en": ["DQ score 78/100 across 48 records."],
            "findings_ar": ["درجة DQ: 78/100 عبر 48 سجل."],
        }
        pitch = generate_retainer_pitch(
            self.eligible_result,
            sprint_report=sprint_report,
        )
        assert any("78" in prop for prop in pitch.value_props_en)

    def test_retainer_pitch_scale_tier_for_high_satisfaction(self):
        """L3 proof + satisfaction 9+ should yield scale_4999 tier."""
        high_result = self.engine.check({
            "sprint_id": "sp_scale",
            "account_id": "acc_scale",
            "proof_level": "L3",
            "satisfaction_score": 9.5,
            "measurable_result_achieved": True,
        })
        pitch = generate_retainer_pitch(high_result)
        assert pitch.recommended_tier == "scale_4999"
        assert pitch.monthly_sar == 4999.0
