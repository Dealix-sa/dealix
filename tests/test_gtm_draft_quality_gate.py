"""Contract: the GTM draft quality gate enforces the Market Production OS doctrine.

A clean draft is "approval_required" (ready for a human, never auto-sent); any
doctrine / compliance / deliverability / quality violation blocks it.
"""

from __future__ import annotations

from auto_client_acquisition.gtm_os import (
    OutreachDraft,
    summarize_gate_results,
    validate_outreach_draft,
)


def _valid_draft(**overrides) -> OutreachDraft:
    base = {
        "draft_id": "d_ok",
        "prospect_ref": "acc_001",
        "company_label": "Riyadh marketing agency (mid)",
        "sector": "marketing_agencies",
        "recipient_role": "Marketing Director",
        "recipient_ref": "rcpt_abc",
        "signal_ref": "sig_001",
        "pain_hypothesis": "Inbound leads pile up; follow-up is manual.",
        "personalization_note": "Posted a Sales Ops role last week.",
        "personalization_tier": "P2",
        "offer": "revenue_intelligence_sprint",
        "offer_matched": True,
        "subject": "ترتيب متابعة الـ leads قبل توظيف Sales Ops",
        "body_ar": "لاحظنا إعلان توظيف Sales Ops. نجهّز طبقة متابعة منظمة قبلها.",
        "body_en": "Saw your Sales Ops opening — we set up an ordered follow-up layer first.",
        "cta": "نراجع 10 حسابات في مكالمة 20 دقيقة؟",
        "language": "ar_en",
        "evidence_level": "L2",
        "risk_level": "low",
        "unsubscribe_included": True,
        "sequence_step": "first_touch",
    }
    base.update(overrides)
    return OutreachDraft(**base)


def test_valid_draft_passes_as_approval_required() -> None:
    res = validate_outreach_draft(_valid_draft(), suppression_refs=set())
    assert res.passed is True
    assert res.verdict == "pass"
    assert res.governance_decision == "approval_required"  # never auto-allowed to send
    assert res.issues == []


def test_missing_unsubscribe_blocks() -> None:
    res = validate_outreach_draft(_valid_draft(unsubscribe_included=False))
    assert res.passed is False
    assert "missing_unsubscribe" in res.codes
    assert res.governance_decision == "BLOCK"


def test_missing_evidence_level_blocks() -> None:
    res = validate_outreach_draft(_valid_draft(evidence_level=""))
    assert "missing_evidence_level" in res.codes


def test_personalization_p0_blocks() -> None:
    res = validate_outreach_draft(_valid_draft(personalization_tier="P0"))
    assert "personalization_below_p1" in res.codes


def test_offer_not_matched_blocks() -> None:
    assert "offer_not_matched" in validate_outreach_draft(_valid_draft(offer_matched=False)).codes
    assert "offer_not_matched" in validate_outreach_draft(_valid_draft(offer="not_a_real_offer")).codes


def test_high_risk_blocks() -> None:
    assert "risk_high" in validate_outreach_draft(_valid_draft(risk_level="high")).codes


def test_fake_reply_prefix_blocks() -> None:
    assert "fake_reply_prefix" in validate_outreach_draft(_valid_draft(subject="Re: our chat")).codes
    assert "fake_reply_prefix" in validate_outreach_draft(_valid_draft(subject="رد: بخصوص اجتماعنا")).codes


def test_spammy_subject_blocks() -> None:
    assert "misleading_subject" in validate_outreach_draft(_valid_draft(subject="100% FREE $$$ ACT NOW")).codes


def test_suppression_hit_blocks() -> None:
    res = validate_outreach_draft(_valid_draft(recipient_ref="rcpt_xyz"), suppression_refs={"rcpt_xyz"})
    assert "suppression_hit" in res.codes


def test_cold_whatsapp_body_blocked_by_governance() -> None:
    res = validate_outreach_draft(_valid_draft(body_en="We will use cold whatsapp to blast everyone."))
    assert res.passed is False
    assert any(c.startswith("governance:") for c in res.codes)


def test_guaranteed_claim_blocked_by_governance() -> None:
    res = validate_outreach_draft(_valid_draft(body_en="We guarantee ROI in 30 days."))
    assert res.passed is False
    assert any(c.startswith("governance:") for c in res.codes)


def test_empty_body_blocks() -> None:
    assert "empty_body" in validate_outreach_draft(_valid_draft(body_ar="", body_en="")).codes


def test_send_state_without_approval_blocks() -> None:
    res = validate_outreach_draft(_valid_draft(send_status="sent", approval_status="approval_required"))
    assert "send_without_approval" in res.codes


def test_summarize_counts_pass_and_fail() -> None:
    results = [
        validate_outreach_draft(_valid_draft(draft_id="ok1")),
        validate_outreach_draft(_valid_draft(draft_id="bad1", unsubscribe_included=False)),
        validate_outreach_draft(_valid_draft(draft_id="bad2", personalization_tier="P0")),
    ]
    summary = summarize_gate_results(results)
    assert summary["total"] == 3
    assert summary["passed"] == 1
    assert summary["failed"] == 2
    assert "ok1" in summary["approval_ready_ids"]
    assert summary["top_failure_reasons"]["missing_unsubscribe"] == 1


def test_dict_input_is_validated() -> None:
    res = validate_outreach_draft(_valid_draft().model_dump())
    assert res.passed is True
