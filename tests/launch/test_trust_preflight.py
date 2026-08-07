"""Tests for dealix.launch_os.trust_preflight.

Actual interface (from implementation):
    run_preflight(draft: dict) -> tuple[bool, list[TrustViolation]]
    TrustViolation: dataclass with rule_id, severity, message_ar, message_en

10 rules:
  R01  No guarantee language (English)
  R02  No competitor defamation
  R03  No PII exposure
  R04  No spam trigger patterns
  R05  WhatsApp channel requires consent_record_ref
  R06  Arabic informal tone markers
  R07  Claim accuracy — evidence_level must be L2+
  R08  Legal entity check — drafted_by must be set
  R09  Pricing within approved range (pricing_status != draft_only)
  R10  Enterprise proposals require approval_required flag

Each test class covers one rule.  A clean draft with all-green fields passes
all checks (no block violations).
"""

from __future__ import annotations

from typing import Any

import pytest

from dealix.launch_os.trust_preflight import TrustViolation, run_preflight

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean_draft(**overrides: Any) -> dict[str, Any]:
    """Return a minimal draft that passes all 10 rules."""
    base: dict[str, Any] = {
        "channel": "email",
        "body": "We can help you improve your sales operations.",
        "body_ar": "يمكننا مساعدتك في تحسين عمليات المبيعات لديك.",
        "body_en": "We can help you improve your sales operations.",
        "subject_ar": "تحسين منظومة المبيعات",
        "subject_en": "Improving your sales system",
        "evidence_level": "L3",
        "drafted_by": "founder",
        "pricing_status": "approved_range_required",
        "approval_required": False,
        "consent_record_ref": "",
    }
    base.update(overrides)
    return base


def _run(draft: dict[str, Any]) -> tuple[bool, list[TrustViolation]]:
    return run_preflight(draft)


def _has_rule(violations: list[TrustViolation], rule_id: str) -> bool:
    return any(v.rule_id == rule_id for v in violations)


def _has_block(violations: list[TrustViolation]) -> bool:
    return any(v.severity == "block" for v in violations)


# ---------------------------------------------------------------------------
# Rule R01: No guarantee language
# ---------------------------------------------------------------------------

class TestRuleR01NoGuarantee:
    def test_guarantee_language_en_blocks_draft(self) -> None:
        draft = _clean_draft(body="We guarantee 100% ROI in 30 days.")
        passed, violations = _run(draft)
        assert not passed
        assert _has_rule(violations, "R01")

    def test_guaranteed_keyword_is_detected(self) -> None:
        draft = _clean_draft(body="Guaranteed results for your team.")
        _, violations = _run(draft)
        assert _has_rule(violations, "R01")

    def test_arabic_guarantee_term_nadhman_blocks(self) -> None:
        draft = _clean_draft(body_ar="نضمن لك نتائج مبيعات خلال أسبوع.")
        passed, violations = _run(draft)
        assert not passed
        assert _has_rule(violations, "R01")

    def test_arabic_guarantee_term_mamdoun_blocks(self) -> None:
        draft = _clean_draft(body_ar="النتيجة مضمونة لعملائنا.")
        _, violations = _run(draft)
        assert _has_rule(violations, "R01")

    def test_arabic_guarantee_kafalah_blocks(self) -> None:
        draft = _clean_draft(body_ar="نقدم كفالة نتائج كاملة.")
        _, violations = _run(draft)
        assert _has_rule(violations, "R01")

    def test_clean_body_without_guarantee_passes_r01(self) -> None:
        draft = _clean_draft()
        _, violations = _run(draft)
        assert not _has_rule(violations, "R01")


# ---------------------------------------------------------------------------
# Rule R02: No competitor defamation
# ---------------------------------------------------------------------------

class TestRuleR02NoDefamation:
    def test_competitor_bad_language_blocks(self) -> None:
        draft = _clean_draft(body="Unlike our competitor who is a scam and fraud.")
        _, violations = _run(draft)
        assert _has_rule(violations, "R02")

    def test_rival_terrible_language_blocks(self) -> None:
        draft = _clean_draft(body="Our rival's product is terrible and fails constantly.")
        _, violations = _run(draft)
        assert _has_rule(violations, "R02")

    def test_neutral_competitor_mention_passes_r02(self) -> None:
        draft = _clean_draft(body="We work alongside other providers in the market.")
        _, violations = _run(draft)
        assert not _has_rule(violations, "R02")


# ---------------------------------------------------------------------------
# Rule R03: No PII exposure
# ---------------------------------------------------------------------------

class TestRuleR03NoPII:
    def test_saudi_phone_number_in_body_blocks(self) -> None:
        draft = _clean_draft(body="Call us at +966501234567 for details.")
        _, violations = _run(draft)
        assert _has_rule(violations, "R03")

    def test_national_id_in_body_blocks(self) -> None:
        draft = _clean_draft(body="Your national ID 1234567890 is on file.")
        _, violations = _run(draft)
        assert _has_rule(violations, "R03")

    def test_clean_body_without_pii_passes_r03(self) -> None:
        draft = _clean_draft()
        _, violations = _run(draft)
        assert not _has_rule(violations, "R03")


# ---------------------------------------------------------------------------
# Rule R04: No spam trigger patterns
# ---------------------------------------------------------------------------

class TestRuleR04NoSpam:
    def test_urgent_keyword_blocks(self) -> None:
        draft = _clean_draft(body="URGENT: Act now before this expires!")
        _, violations = _run(draft)
        assert _has_rule(violations, "R04")

    def test_act_now_keyword_blocks(self) -> None:
        draft = _clean_draft(body="ACT NOW to claim your free gift.")
        _, violations = _run(draft)
        assert _has_rule(violations, "R04")

    def test_arabic_limited_time_blocks(self) -> None:
        draft = _clean_draft(body_ar="فرصة محدودة — لا تفوت هذا العرض.")
        _, violations = _run(draft)
        assert _has_rule(violations, "R04")

    def test_clean_draft_passes_r04(self) -> None:
        draft = _clean_draft()
        _, violations = _run(draft)
        assert not _has_rule(violations, "R04")


# ---------------------------------------------------------------------------
# Rule R05: WhatsApp channel requires consent_record_ref
# ---------------------------------------------------------------------------

class TestRuleR05WhatsAppConsent:
    def test_whatsapp_without_consent_ref_blocks(self) -> None:
        draft = _clean_draft(channel="whatsapp_after_consent", consent_record_ref="")
        _, violations = _run(draft)
        assert _has_rule(violations, "R05")

    def test_whatsapp_with_consent_ref_passes_r05(self) -> None:
        draft = _clean_draft(channel="whatsapp_after_consent", consent_record_ref="consent_ref_001")
        _, violations = _run(draft)
        assert not _has_rule(violations, "R05")

    def test_email_channel_does_not_trigger_r05(self) -> None:
        draft = _clean_draft(channel="email", consent_record_ref="")
        _, violations = _run(draft)
        assert not _has_rule(violations, "R05")


# ---------------------------------------------------------------------------
# Rule R06: Arabic informal tone
# ---------------------------------------------------------------------------

class TestRuleR06ArabicTone:
    def test_informal_arabic_yaa_am_warns(self) -> None:
        draft = _clean_draft(body_ar="يا عم كيف حالك، عندنا عرض رائع.")
        _, violations = _run(draft)
        assert _has_rule(violations, "R06")

    def test_clean_arabic_body_passes_r06(self) -> None:
        draft = _clean_draft()
        _, violations = _run(draft)
        assert not _has_rule(violations, "R06")


# ---------------------------------------------------------------------------
# Rule R07: Evidence level must be L2+
# ---------------------------------------------------------------------------

class TestRuleR07EvidenceLevel:
    @pytest.mark.parametrize("level", ["L0", "L1"])
    def test_low_evidence_level_blocks(self, level: str) -> None:
        draft = _clean_draft(evidence_level=level)
        _, violations = _run(draft)
        assert _has_rule(violations, "R07")

    @pytest.mark.parametrize("level", ["L2", "L3", "L4", "L5"])
    def test_adequate_evidence_level_passes_r07(self, level: str) -> None:
        draft = _clean_draft(evidence_level=level)
        _, violations = _run(draft)
        assert not _has_rule(violations, "R07")


# ---------------------------------------------------------------------------
# Rule R08: drafted_by must be set
# ---------------------------------------------------------------------------

class TestRuleR08LegalEntity:
    def test_missing_drafted_by_blocks(self) -> None:
        draft = _clean_draft(drafted_by="")
        _, violations = _run(draft)
        assert _has_rule(violations, "R08")

    def test_drafted_by_set_passes_r08(self) -> None:
        draft = _clean_draft(drafted_by="founder")
        _, violations = _run(draft)
        assert not _has_rule(violations, "R08")


# ---------------------------------------------------------------------------
# Rule R09: Pricing status must not be draft_only
# ---------------------------------------------------------------------------

class TestRuleR09PricingStatus:
    def test_draft_only_pricing_blocks(self) -> None:
        draft = _clean_draft(pricing_status="draft_only")
        _, violations = _run(draft)
        assert _has_rule(violations, "R09")

    def test_approved_range_pricing_passes_r09(self) -> None:
        draft = _clean_draft(pricing_status="approved_range_required")
        _, violations = _run(draft)
        assert not _has_rule(violations, "R09")


# ---------------------------------------------------------------------------
# Rule R10: Enterprise proposals require approval_required flag
# ---------------------------------------------------------------------------

class TestRuleR10EnterpriseApproval:
    def test_founder_approval_required_pricing_without_flag_blocks(self) -> None:
        draft = _clean_draft(
            pricing_status="founder_approval_required",
            approval_required=False,
        )
        _, violations = _run(draft)
        assert _has_rule(violations, "R10")

    def test_founder_approval_required_with_flag_passes_r10(self) -> None:
        draft = _clean_draft(
            pricing_status="founder_approval_required",
            approval_required=True,
        )
        _, violations = _run(draft)
        assert not _has_rule(violations, "R10")

    def test_normal_pricing_status_ignores_r10(self) -> None:
        draft = _clean_draft(pricing_status="approved_range_required", approval_required=False)
        _, violations = _run(draft)
        assert not _has_rule(violations, "R10")


# ---------------------------------------------------------------------------
# Compound violation test
# ---------------------------------------------------------------------------

class TestCompoundViolations:
    def test_multiple_violations_in_one_draft(self) -> None:
        """A draft with guarantee language AND low evidence level surfaces multiple violations."""
        draft = _clean_draft(
            body="We guarantee ROI in 30 days.",
            evidence_level="L0",
        )
        _, violations = _run(draft)
        rule_ids = {v.rule_id for v in violations}
        assert "R01" in rule_ids
        assert "R07" in rule_ids
        assert len(violations) >= 2

    def test_all_blocking_rules_fire_together(self) -> None:
        draft = {
            "channel": "whatsapp_after_consent",
            "body": "We guarantee results. URGENT ACT NOW! Competitor is a scam.",
            "body_ar": "نضمن لك يا عم. فرصة محدودة.",
            "body_en": "We guarantee results.",
            "subject_ar": "",
            "subject_en": "",
            "evidence_level": "L0",
            "drafted_by": "",
            "pricing_status": "draft_only",
            "approval_required": False,
            "consent_record_ref": "",
        }
        passed, violations = _run(draft)
        assert not passed
        assert len(violations) >= 5


# ---------------------------------------------------------------------------
# Clean draft passes all checks
# ---------------------------------------------------------------------------

class TestCleanDraftPasses:
    def test_clean_email_draft_passes_all_rules(self) -> None:
        draft = _clean_draft()
        passed, violations = _run(draft)
        block_viols = [v for v in violations if v.severity == "block"]
        assert passed
        assert len(block_viols) == 0

    def test_run_preflight_returns_tuple(self) -> None:
        result = run_preflight(_clean_draft())
        assert isinstance(result, tuple)
        assert len(result) == 2
        passed, violations = result
        assert isinstance(passed, bool)
        assert isinstance(violations, list)


# ---------------------------------------------------------------------------
# TrustViolation structure
# ---------------------------------------------------------------------------

class TestTrustViolationStructure:
    def test_trust_violation_has_rule_id(self) -> None:
        draft = _clean_draft(evidence_level="L0")
        _, violations = _run(draft)
        assert len(violations) > 0
        v = violations[0]
        assert hasattr(v, "rule_id")
        assert isinstance(v.rule_id, str)

    def test_trust_violation_has_severity(self) -> None:
        draft = _clean_draft(evidence_level="L0")
        _, violations = _run(draft)
        v = violations[0]
        assert hasattr(v, "severity")
        assert v.severity in ("block", "warn")

    def test_trust_violation_has_message_ar(self) -> None:
        draft = _clean_draft(evidence_level="L0")
        _, violations = _run(draft)
        v = violations[0]
        assert hasattr(v, "message_ar")
        assert isinstance(v.message_ar, str)

    def test_trust_violation_has_message_en(self) -> None:
        draft = _clean_draft(evidence_level="L0")
        _, violations = _run(draft)
        v = violations[0]
        assert hasattr(v, "message_en")
        assert isinstance(v.message_en, str)

    def test_block_severity_violation_makes_passed_false(self) -> None:
        draft = _clean_draft(body="We guarantee ROI.")
        passed, violations = _run(draft)
        block_viols = [v for v in violations if v.severity == "block"]
        if block_viols:
            assert not passed
