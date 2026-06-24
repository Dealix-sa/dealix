"""
Tests for dealix-gcc-marketing-os scripts:
quality_gate, compliance_checker, suppression_manager,
founder_review_report, reply_processor, company_scanner, draft_generator.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

# Add scripts directory to path so imports work without installation
_SCRIPTS_DIR = Path(__file__).parent.parent / "dealix-gcc-marketing-os" / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))


# ---------------------------------------------------------------------------
# quality_gate
# ---------------------------------------------------------------------------

from quality_gate import run_quality_gate


class TestRunQualityGate:
    def test_clean_english_email_passes(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "company": "Acme Legal",
            "subject": "Acme Legal — workflow question",
            "body": "Hi Sarah, noticed Acme Legal handles a lot of contract documents. Would it be useful if I sent a one-page summary of how we help law firms reduce document review time? If this is not relevant, I'm happy to stop following up.",
        }
        result = run_quality_gate(draft)
        assert result["pass"] is True
        assert result["score"] >= 70

    def test_generic_ai_agency_english_fails(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "company": "Test Co",
            "subject": "Leverage the power of AI",
            "body": "We help companies leverage the power of AI to transform their business. Would it be useful to schedule a call? If this is not relevant, I'm happy to stop following up.",
        }
        result = run_quality_gate(draft)
        assert "english_fail:generic_ai_agency" in result["flags"]

    def test_guaranteed_roi_english_fails(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "company": "Test Co",
            "subject": "Guaranteed ROI",
            "body": "We offer guaranteed ROI in 30 days. Would it be useful? I'm happy to stop following up.",
        }
        result = run_quality_gate(draft)
        assert "english_fail:fake_certainty" in result["flags"]

    def test_too_long_email_penalised(self) -> None:
        long_body = ("word " * 210).strip()
        draft = {
            "language": "en",
            "channel": "email",
            "company": "Test Co",
            "subject": "Test",
            "body": long_body + " Would it be useful? I'm happy to stop following up.",
        }
        result = run_quality_gate(draft)
        flags = result["flags"]
        assert any(f.startswith("too_long:") for f in flags)

    def test_missing_cta_penalised(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "company": "Test Co",
            "subject": "Test",
            "body": "We have a great product. It is very good. Please consider it. If this is not relevant, I'm happy to stop following up.",
        }
        result = run_quality_gate(draft)
        assert "missing_cta" in result["flags"]

    def test_company_not_in_body_penalised(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "company": "UniqueCompanyXYZ",
            "subject": "Hello",
            "body": "Would it be useful to schedule a call? I'm happy to stop following up.",
        }
        result = run_quality_gate(draft)
        assert "company_not_mentioned" in result["flags"]

    def test_arabic_overblown_claim_fails(self) -> None:
        draft = {
            "language": "ar",
            "channel": "email",
            "company": "شركة أ",
            "subject": "عرض",
            "body": "نضمن لك نتائج ممتازة. هل يناسبكم أرسل ملخص؟ أقدر أوقف المتابعة.",
        }
        result = run_quality_gate(draft)
        assert "arabic_fail:overblown_claims" in result["flags"]

    def test_arabic_missing_opt_out_penalised(self) -> None:
        draft = {
            "language": "ar",
            "channel": "email",
            "company": "شركة أ",
            "subject": "عرض",
            "body": "نحن نساعدك في تقليل العمل اليدوي. هل يناسبكم أرسل ملخص؟",
        }
        result = run_quality_gate(draft)
        assert "missing_arabic_opt_out" in result["flags"]

    def test_score_clamped_between_0_and_100(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "company": "XXXXXX",
            "subject": "guaranteed ROI leverage power AI",
            "body": ("word " * 250) + "guaranteed ROI we guarantee cutting-edge AI solutions",
        }
        result = run_quality_gate(draft)
        assert 0 <= result["score"] <= 100

    def test_linkedin_word_limit_lower_than_email(self) -> None:
        body = ("word " * 110).strip() + " Would it be useful? I'm happy to stop following up."
        draft_email = {"language": "en", "channel": "email", "company": "X", "subject": "Y", "body": body}
        draft_linkedin = {"language": "en", "channel": "linkedin", "company": "X", "subject": "Y", "body": body}
        result_email = run_quality_gate(draft_email)
        result_linkedin = run_quality_gate(draft_linkedin)
        # linkedin limit is 100 words, email is 200 — linkedin should have too_long flag
        assert any(f.startswith("too_long:") for f in result_linkedin["flags"])
        assert not any(f.startswith("too_long:") for f in result_email["flags"])


# ---------------------------------------------------------------------------
# compliance_checker
# ---------------------------------------------------------------------------

from compliance_checker import run_compliance_check


class TestRunComplianceCheck:
    def test_clean_draft_passes(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "country": "uae",
            "sector": "consulting",
            "body": "Hi, would it be useful if I sent a one-page summary? I'm happy to stop following up.",
            "subject": "Workflow question",
        }
        result = run_compliance_check(draft)
        assert result["pass"] is True
        assert result["score"] >= 70

    def test_missing_opt_out_penalised(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "country": "uae",
            "sector": "consulting",
            "body": "Hi, would it be useful if I sent a one-page summary?",
            "subject": "Workflow",
        }
        result = run_compliance_check(draft)
        assert "missing_opt_out" in result["flags"]

    def test_data_sourcing_claim_penalised(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "country": "uae",
            "sector": "b2b_services",
            "body": "We have your data from our database. I'm happy to stop following up.",
            "subject": "Test",
        }
        result = run_compliance_check(draft)
        assert any(f.startswith("data_sourcing_claim:") for f in result["flags"])

    def test_sensitive_sector_missing_privacy_language(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "country": "saudi_arabia",
            "sector": "legal",
            "body": "Hi, we can help your firm save time. Would it be useful? I'm happy to stop following up.",
            "subject": "Workflow",
        }
        result = run_compliance_check(draft)
        assert any("sensitive_sector_missing_privacy_language" in f for f in result["flags"])

    def test_sensitive_sector_with_privacy_language_passes(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "country": "saudi_arabia",
            "sector": "legal",
            "body": "Hi, our system is secure and built with confidentiality in mind. Would it be useful? I'm happy to stop following up.",
            "subject": "Confidential workflow",
        }
        result = run_compliance_check(draft)
        assert not any("sensitive_sector_missing_privacy_language" in f for f in result["flags"])

    def test_fake_urgency_deceptive_pattern(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "country": "uae",
            "sector": "b2b_services",
            "body": "Last chance to join our program. I'm happy to stop following up.",
            "subject": "Expires today",
        }
        result = run_compliance_check(draft)
        assert any("deceptive:fake_urgency" in f for f in result["flags"])

    def test_fake_familiarity_deceptive_pattern(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "country": "uae",
            "sector": "b2b_services",
            "body": "As we discussed, I wanted to follow up. I'm happy to stop following up.",
            "subject": "Following our conversation",
        }
        result = run_compliance_check(draft)
        assert any("deceptive:fake_familiarity" in f for f in result["flags"])

    def test_high_consent_country_production_data_reference(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "country": "oman",
            "sector": "b2b_services",
            "body": "We can process your current data immediately. I'm happy to stop following up.",
            "subject": "Data processing",
        }
        result = run_compliance_check(draft)
        assert any("high_consent_country_data_reference" in f for f in result["flags"])

    def test_score_clamped_between_0_and_100(self) -> None:
        draft = {
            "language": "en",
            "channel": "email",
            "country": "oman",
            "sector": "legal",
            "body": "We have your data from our database. We scraped your info. As we discussed, last chance, expires today. Your current data is ready.",
            "subject": "Test",
        }
        result = run_compliance_check(draft)
        assert 0 <= result["score"] <= 100

    def test_arabic_opt_out_signal_accepted(self) -> None:
        draft = {
            "language": "ar",
            "channel": "email",
            "country": "saudi_arabia",
            "sector": "b2b_services",
            "body": "السلام عليكم، هل يناسبكم نرسل ملخص؟ أقدر أوقف المتابعة.",
            "subject": "عرض",
        }
        result = run_compliance_check(draft)
        assert "missing_opt_out" not in result["flags"]


# ---------------------------------------------------------------------------
# suppression_manager
# ---------------------------------------------------------------------------

from suppression_manager import (
    add_to_suppression,
    filter_drafts,
    is_suppressed,
    load_suppression_set,
)


class TestSuppressionManager:
    def test_empty_suppression_file_returns_empty_set(self, tmp_path: Path) -> None:
        import suppression_manager as sm
        original = sm.SUPPRESSION_FILE
        sm.SUPPRESSION_FILE = tmp_path / "suppression.jsonl"
        try:
            result = load_suppression_set()
            assert result == set()
        finally:
            sm.SUPPRESSION_FILE = original

    def test_add_and_is_suppressed(self, tmp_path: Path) -> None:
        import suppression_manager as sm
        original = sm.SUPPRESSION_FILE
        sm.SUPPRESSION_FILE = tmp_path / "suppression.jsonl"
        try:
            add_to_suppression("test@example.com", "opt_out_reply")
            assert is_suppressed("test@example.com") is True
            assert is_suppressed("other@example.com") is False
        finally:
            sm.SUPPRESSION_FILE = original

    def test_is_suppressed_case_insensitive(self, tmp_path: Path) -> None:
        import suppression_manager as sm
        original = sm.SUPPRESSION_FILE
        sm.SUPPRESSION_FILE = tmp_path / "suppression.jsonl"
        try:
            add_to_suppression("TEST@EXAMPLE.COM", "bounce")
            assert is_suppressed("test@example.com") is True
        finally:
            sm.SUPPRESSION_FILE = original

    def test_filter_drafts_splits_clean_and_blocked(self, tmp_path: Path) -> None:
        import suppression_manager as sm
        original = sm.SUPPRESSION_FILE
        sm.SUPPRESSION_FILE = tmp_path / "suppression.jsonl"
        try:
            add_to_suppression("blocked@example.com", "opt_out")
            drafts = [
                {"contact_email": "blocked@example.com", "company": "Blocked Co"},
                {"contact_email": "clean@example.com", "company": "Clean Co"},
                {"contact_email": "", "company": "No Email Co"},
            ]
            clean, blocked = filter_drafts(drafts)
            assert len(clean) == 2
            assert len(blocked) == 1
            assert blocked[0]["company"] == "Blocked Co"
            assert blocked[0]["suppression_blocked"] is True
        finally:
            sm.SUPPRESSION_FILE = original

    def test_add_suppression_records_source_and_reason(self, tmp_path: Path) -> None:
        import suppression_manager as sm
        original = sm.SUPPRESSION_FILE
        sm.SUPPRESSION_FILE = tmp_path / "suppression.jsonl"
        try:
            add_to_suppression("x@y.com", reason="bounce_permanent", source="reply_processor")
            with open(sm.SUPPRESSION_FILE) as f:
                record = json.loads(f.readline())
            assert record["reason"] == "bounce_permanent"
            assert record["source"] == "reply_processor"
        finally:
            sm.SUPPRESSION_FILE = original


# ---------------------------------------------------------------------------
# founder_review_report
# ---------------------------------------------------------------------------

from founder_review_report import generate_report


class TestGenerateReport:
    def _sample_stats(self) -> dict:
        return {
            "qualified_companies": 10,
            "arabic_drafts": 5,
            "english_drafts": 5,
            "followup_drafts": 3,
            "rejected_drafts": 2,
            "founder_ready": 8,
        }

    def _sample_approved(self) -> list[dict]:
        return [
            {
                "company": "Alpha Legal",
                "country": "saudi_arabia",
                "sector": "legal",
                "language": "ar",
                "offer": "legal_knowledge_os",
                "quality_score": 90,
                "channel": "email",
                "angle": "document_search_and_retrieval",
            },
            {
                "company": "Beta FM",
                "country": "uae",
                "sector": "facilities_management",
                "language": "en",
                "offer": "maintenance_intelligence_os",
                "quality_score": 80,
                "channel": "linkedin",
                "angle": "sla_visibility",
            },
        ]

    def _sample_rejected(self) -> list[dict]:
        return [
            {
                "company": "Gamma Corp",
                "country": "qatar",
                "reject_reason": "missing_opt_out",
            }
        ]

    def test_report_contains_date(self) -> None:
        report = generate_report("2026-05-31", self._sample_stats(), self._sample_approved(), self._sample_rejected())
        assert "2026-05-31" in report

    def test_report_contains_founder_ready_count(self) -> None:
        report = generate_report("2026-05-31", self._sample_stats(), self._sample_approved(), self._sample_rejected())
        assert "8" in report

    def test_report_contains_risk_flags(self) -> None:
        report = generate_report("2026-05-31", self._sample_stats(), self._sample_approved(), self._sample_rejected())
        assert "missing_opt_out" in report

    def test_report_contains_company_names(self) -> None:
        report = generate_report("2026-05-31", self._sample_stats(), self._sample_approved(), self._sample_rejected())
        assert "Alpha Legal" in report
        assert "Beta FM" in report

    def test_empty_approved_generates_valid_report(self) -> None:
        stats = self._sample_stats()
        stats["founder_ready"] = 0
        report = generate_report("2026-05-31", stats, [], [])
        assert "Founder Report" in report
        assert "None flagged" in report

    def test_report_contains_tomorrow_strategy_section(self) -> None:
        report = generate_report("2026-05-31", self._sample_stats(), self._sample_approved(), [])
        assert "Tomorrow Strategy" in report


# ---------------------------------------------------------------------------
# reply_processor
# ---------------------------------------------------------------------------

from reply_processor import classify_reply, process_reply


class TestClassifyReply:
    def test_positive_interested_english(self) -> None:
        assert classify_reply("Yes, sounds good, please send more info") == "positive_interested"

    def test_positive_interested_arabic(self) -> None:
        assert classify_reply("نعم، يناسبنا ذلك") == "positive_interested"

    def test_hard_no_english(self) -> None:
        assert classify_reply("Not interested, please remove me") == "hard_no"

    def test_hard_no_arabic(self) -> None:
        assert classify_reply("لا نحتاج هذه الخدمة") == "hard_no"

    def test_soft_no_timing_english(self) -> None:
        assert classify_reply("Not now, maybe later") == "soft_no_timing"

    def test_auto_reply_detected(self) -> None:
        assert classify_reply("I am out of office until next Monday") == "auto_reply"

    def test_question_detected(self) -> None:
        assert classify_reply("What is your pricing?") == "question"

    def test_referral_detected(self) -> None:
        assert classify_reply("You should talk to our head of operations") == "referral"

    def test_unclassified_returns_unclassified(self) -> None:
        assert classify_reply("qwerty asdf zxcv") == "unclassified"


class TestProcessReply:
    def test_hard_no_adds_to_suppression(self, tmp_path: Path) -> None:
        import suppression_manager as sm
        import reply_processor as rp

        original_mem = rp.MEMORY_DIR
        original_sup = sm.SUPPRESSION_FILE

        rp.MEMORY_DIR = tmp_path
        sm.SUPPRESSION_FILE = tmp_path / "suppression.jsonl"

        try:
            reply = {
                "from_email": "opt-out@example.com",
                "body": "Not interested, please remove me",
                "company": "Test Co",
                "sector": "legal",
                "angle": "document_search_and_retrieval",
                "language": "en",
                "draft_id": "dq_123",
            }
            result = process_reply(reply)
            assert result["category"] == "hard_no"
            assert sm.is_suppressed("opt-out@example.com") is True
        finally:
            rp.MEMORY_DIR = original_mem
            sm.SUPPRESSION_FILE = original_sup

    def test_process_reply_writes_to_learning_log(self, tmp_path: Path) -> None:
        import reply_processor as rp

        original_mem = rp.MEMORY_DIR
        rp.MEMORY_DIR = tmp_path

        try:
            reply = {
                "from_email": "sender@example.com",
                "body": "Yes, sounds good, please send more",
                "company": "Test Co",
                "sector": "consulting",
                "angle": "proposal_reuse",
                "language": "en",
                "draft_id": "dq_456",
            }
            process_reply(reply)
            log_path = tmp_path / "learning_log.jsonl"
            assert log_path.exists()
            with open(log_path) as f:
                record = json.loads(f.readline())
            assert record["type"] == "reply"
            assert record["category"] == "positive_interested"
        finally:
            rp.MEMORY_DIR = original_mem

    def test_process_reply_writes_to_replies_file(self, tmp_path: Path) -> None:
        import reply_processor as rp

        original_mem = rp.MEMORY_DIR
        rp.MEMORY_DIR = tmp_path

        try:
            reply = {
                "from_email": "someone@example.com",
                "body": "Not now, maybe later",
                "company": "Test Co",
                "sector": "b2b_services",
                "language": "en",
                "draft_id": "dq_789",
            }
            process_reply(reply)
            replies_path = tmp_path / "replies.jsonl"
            assert replies_path.exists()
        finally:
            rp.MEMORY_DIR = original_mem


# ---------------------------------------------------------------------------
# company_scanner
# ---------------------------------------------------------------------------

from company_scanner import classify_company, scan_and_classify


class TestClassifyCompany:
    def _countries_cfg(self) -> dict:
        return {
            "countries": {
                "saudi_arabia": {
                    "languages": ["ar", "en"],
                    "priority_sectors": ["legal", "facilities_management"],
                },
                "uae": {
                    "languages": ["en", "ar"],
                    "priority_sectors": ["consulting", "legal"],
                },
            }
        }

    def _sectors_cfg(self) -> dict:
        return {
            "sectors": {
                "legal": {
                    "buyer_titles": ["Managing Partner", "Senior Partner"],
                    "primary_offer": "legal_knowledge_os",
                    "entry_offer": "ai_workflow_audit",
                    "preferred_tone": "trust_confidentiality_precision",
                    "language_preference": "formal_arabic_or_english_by_firm_type",
                },
                "consulting": {
                    "buyer_titles": ["Managing Partner", "Delivery Director"],
                    "primary_offer": "consulting_delivery_os",
                    "entry_offer": "ai_workflow_audit",
                    "preferred_tone": "expert_to_expert",
                    "language_preference": "english_first_bilingual",
                },
            }
        }

    def test_arabic_website_language_selects_arabic(self) -> None:
        company = {
            "name": "Test Legal",
            "country": "saudi_arabia",
            "sector_hint": "legal",
            "website_language": "ar",
        }
        result = classify_company(company, self._countries_cfg(), self._sectors_cfg())
        assert result["language"] == "ar"

    def test_english_first_sector_selects_english(self) -> None:
        company = {
            "name": "Test Consulting",
            "country": "uae",
            "sector_hint": "consulting",
            "website_language": "",
        }
        result = classify_company(company, self._countries_cfg(), self._sectors_cfg())
        assert result["language"] == "en"

    def test_priority_sector_flag_set(self) -> None:
        company = {
            "name": "Test Legal SA",
            "country": "saudi_arabia",
            "sector_hint": "legal",
            "website_language": "ar",
        }
        result = classify_company(company, self._countries_cfg(), self._sectors_cfg())
        assert result["sector_is_priority"] is True

    def test_non_priority_sector_flag_false(self) -> None:
        company = {
            "name": "Test Consulting SA",
            "country": "saudi_arabia",
            "sector_hint": "consulting",
            "website_language": "",
        }
        result = classify_company(company, self._countries_cfg(), self._sectors_cfg())
        assert result["sector_is_priority"] is False

    def test_classify_company_returns_required_fields(self) -> None:
        company = {
            "name": "Test Co",
            "country": "uae",
            "sector_hint": "legal",
            "website_language": "en",
            "contact_email": "info@test.com",
            "website": "https://test.com",
        }
        result = classify_company(company, self._countries_cfg(), self._sectors_cfg())
        for field in ["id", "company", "country", "sector", "language", "buyer_title", "primary_offer", "classified_at"]:
            assert field in result, f"Missing field: {field}"

    def test_scan_and_classify_writes_to_companies_jsonl(self, tmp_path: Path) -> None:
        import company_scanner as cs
        original = cs.MEMORY_DIR
        cs.MEMORY_DIR = tmp_path

        try:
            leads = [
                {
                    "name": "Alpha Legal",
                    "country": "saudi_arabia",
                    "sector_hint": "legal",
                    "website_language": "ar",
                    "contact_email": "info@alpha.sa",
                    "source": "test",
                }
            ]
            results = scan_and_classify(leads)
            assert len(results) == 1
            assert (tmp_path / "companies.jsonl").exists()
            with open(tmp_path / "companies.jsonl") as f:
                record = json.loads(f.readline())
            assert record["company"] == "Alpha Legal"
        finally:
            cs.MEMORY_DIR = original


# ---------------------------------------------------------------------------
# draft_generator
# ---------------------------------------------------------------------------

from draft_generator import (
    build_draft_metadata,
    generate_all_drafts,
    generate_draft_package,
    select_angle,
)


class TestBuildDraftMetadata:
    def test_returns_required_fields(self) -> None:
        company = {
            "company": "Test Legal",
            "country": "saudi_arabia",
            "sector": "legal",
            "language": "ar",
            "buyer_title": "Managing Partner",
            "primary_offer": "legal_knowledge_os",
            "entry_offer": "ai_workflow_audit",
        }
        result = build_draft_metadata(company, "email", "cold_email", "document_search_and_retrieval")
        for field in ["id", "company", "country", "sector", "language", "channel", "draft_type", "angle", "status", "send_allowed", "created_at"]:
            assert field in result, f"Missing field: {field}"

    def test_send_allowed_defaults_to_false(self) -> None:
        company = {"company": "X", "country": "uae", "sector": "legal", "language": "en",
                   "buyer_title": "CEO", "primary_offer": "ai_workflow_audit", "entry_offer": "ai_workflow_audit"}
        result = build_draft_metadata(company, "email", "cold_email", "workflow_efficiency")
        assert result["send_allowed"] is False

    def test_status_defaults_to_pending_quality_gate(self) -> None:
        company = {"company": "X", "country": "uae", "sector": "legal", "language": "en",
                   "buyer_title": "CEO", "primary_offer": "ai_workflow_audit", "entry_offer": "ai_workflow_audit"}
        result = build_draft_metadata(company, "email", "cold_email", "workflow_efficiency")
        assert result["status"] == "pending_quality_gate"

    def test_id_has_expected_prefix(self) -> None:
        company = {"company": "X", "country": "uae", "sector": "legal", "language": "en",
                   "buyer_title": "CEO", "primary_offer": "ai_workflow_audit", "entry_offer": "ai_workflow_audit"}
        result = build_draft_metadata(company, "email", "cold_email", "angle_a")
        assert result["id"].startswith("dq_")


class TestSelectAngle:
    def test_cold_email_selects_angle_a(self) -> None:
        persuasion_cfg = {
            "ab_testing_angles": {
                "legal": {
                    "angle_a": "document_search",
                    "angle_b": "deadline_extraction",
                    "angle_c": "knowledge_reuse",
                }
            }
        }
        assert select_angle("legal", "cold_email", persuasion_cfg) == "document_search"

    def test_followup_1_selects_angle_b(self) -> None:
        persuasion_cfg = {
            "ab_testing_angles": {
                "legal": {
                    "angle_a": "document_search",
                    "angle_b": "deadline_extraction",
                    "angle_c": "knowledge_reuse",
                }
            }
        }
        assert select_angle("legal", "followup_1", persuasion_cfg) == "deadline_extraction"

    def test_other_type_selects_angle_c(self) -> None:
        persuasion_cfg = {
            "ab_testing_angles": {
                "legal": {
                    "angle_a": "document_search",
                    "angle_b": "deadline_extraction",
                    "angle_c": "knowledge_reuse",
                }
            }
        }
        assert select_angle("legal", "followup_2", persuasion_cfg) == "knowledge_reuse"

    def test_missing_sector_returns_default(self) -> None:
        result = select_angle("unknown_sector", "cold_email", {})
        assert result == "workflow_efficiency"


class TestGenerateDraftPackage:
    def _company_tier_a(self) -> dict:
        return {
            "company": "Alpha Legal",
            "country": "saudi_arabia",
            "sector": "legal",
            "language": "ar",
            "buyer_title": "Managing Partner",
            "primary_offer": "legal_knowledge_os",
            "entry_offer": "ai_workflow_audit",
            "fit_score": 90,
        }

    def _company_tier_b(self) -> dict:
        return {
            "company": "Beta FM",
            "country": "uae",
            "sector": "facilities_management",
            "language": "en",
            "buyer_title": "FM Director",
            "primary_offer": "maintenance_intelligence_os",
            "entry_offer": "ai_workflow_audit",
            "fit_score": 75,
        }

    def _company_tier_c(self) -> dict:
        return {
            "company": "Gamma Local",
            "country": "kuwait",
            "sector": "b2b_services",
            "language": "ar",
            "buyer_title": "CEO",
            "primary_offer": "revenue_ai_os",
            "entry_offer": "ai_workflow_audit",
            "fit_score": 50,
        }

    def test_tier_a_generates_more_drafts_than_tier_c(self) -> None:
        drafts_a = generate_draft_package(self._company_tier_a())
        drafts_c = generate_draft_package(self._company_tier_c())
        assert len(drafts_a) > len(drafts_c)

    def test_tier_b_generates_standard_package(self) -> None:
        drafts = generate_draft_package(self._company_tier_b())
        channels = {d["channel"] for d in drafts}
        assert "email" in channels

    def test_tier_c_generates_minimal_package(self) -> None:
        drafts = generate_draft_package(self._company_tier_c())
        assert len(drafts) >= 1

    def test_all_drafts_have_send_allowed_false(self) -> None:
        drafts = generate_draft_package(self._company_tier_a())
        for draft in drafts:
            assert draft["send_allowed"] is False


class TestGenerateAllDrafts:
    def test_writes_to_draft_queue_jsonl(self, tmp_path: Path) -> None:
        import draft_generator as dg
        original = dg.MEMORY_DIR
        dg.MEMORY_DIR = tmp_path

        try:
            companies = [
                {
                    "company": "Test Co",
                    "country": "uae",
                    "sector": "consulting",
                    "language": "en",
                    "buyer_title": "Managing Partner",
                    "primary_offer": "consulting_delivery_os",
                    "entry_offer": "ai_workflow_audit",
                    "fit_score": 75,
                }
            ]
            all_drafts = generate_all_drafts(companies)
            assert len(all_drafts) > 0
            queue_path = tmp_path / "draft_queue.jsonl"
            assert queue_path.exists()
            lines = queue_path.read_text().strip().split("\n")
            assert len(lines) == len(all_drafts)
        finally:
            dg.MEMORY_DIR = original
