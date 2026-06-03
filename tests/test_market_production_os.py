"""Tests for the Market Production OS layer.

Covers prospect scoring, the quality/compliance gate (composing the
existing governance cores), the 250/day draft factory, the sending ramp,
the approval queue, the reply router, and report rendering.
"""

from __future__ import annotations

from auto_client_acquisition.market_production_os import (
    DAILY_DRAFT_TARGET,
    Prospect,
    allowed_sends_today,
    check_draft,
    classify_and_route,
    classify_reply,
    daily_gtm_report,
    max_sends_for_week,
    produce_drafts,
    rank_for_approval,
    score_prospect,
    summarize_batch,
    weekly_gtm_review,
)
from auto_client_acquisition.market_production_os.schemas import (
    ComplianceStatus,
    PersonalizationLevel,
    ReplyClass,
    SendStatus,
)

_CLEAN_BODY = (
    "مرحبًا، لاحظنا نمطًا في القطاع يتعلق بضعف متابعة العملاء المحتملين. "
    "نقترح تشخيصًا محدود النطاق. هذه فرص مُثبتة بأدلة. "
    "لإيقاف الرسائل ردّ بكلمة إيقاف."
)


# --- prospect scoring -------------------------------------------------------

def test_score_prospect_full_marks_is_100_and_qualified() -> None:
    s = score_prospect(
        sector_fit=1.0,
        likely_lead_flow=1.0,
        decision_maker_clarity=1.0,
        pain_signal=1.0,
        payment_ability=1.0,
        personalization_signal=1.0,
        risk_low=1.0,
    )
    assert s.total == 100
    assert s.qualified is True


def test_score_prospect_zero_is_not_qualified_with_reasons() -> None:
    s = score_prospect(
        sector_fit=0.0,
        likely_lead_flow=0.0,
        decision_maker_clarity=0.0,
        pain_signal=0.0,
        payment_ability=0.0,
        personalization_signal=0.0,
        risk_low=0.0,
    )
    assert s.total == 0
    assert s.qualified is False
    assert "no_personalization_signal" in s.reasons


def test_score_prospect_threshold_boundary() -> None:
    s = score_prospect(
        sector_fit=1.0,
        likely_lead_flow=1.0,
        decision_maker_clarity=1.0,
        pain_signal=0.0,
        payment_ability=0.0,
        personalization_signal=0.5,
        risk_low=0.0,
    )
    assert s.total == 60
    assert s.qualified is True


# --- quality / compliance gate ---------------------------------------------

def test_gate_passes_clean_draft() -> None:
    r = check_draft(
        subject="ملاحظة سريعة حول متابعة العملاء",
        body=_CLEAN_BODY,
        personalization_level=int(PersonalizationLevel.P2),
        evidence_level=2,
        unsubscribe_included=True,
        recipient_email="ops@example.sa",
        lead_source="founder_supplied",
        suppression=[],
    )
    assert r.passed is True
    assert r.governance_decision == "ALLOW_WITH_REVIEW"
    assert r.risk_level == "low"


def test_gate_blocks_cold_whatsapp() -> None:
    r = check_draft(
        subject="hello",
        body="Use cold whatsapp to reach everyone in the list.",
        personalization_level=int(PersonalizationLevel.P2),
        evidence_level=2,
        unsubscribe_included=True,
    )
    assert r.passed is False
    assert r.governance_decision == "BLOCK"


def test_gate_blocks_guaranteed_claim() -> None:
    r = check_draft(
        subject="offer",
        body="We guarantee ROI in 30 days for your company.",
        personalization_level=int(PersonalizationLevel.P2),
        evidence_level=2,
        unsubscribe_included=True,
    )
    assert r.passed is False


def test_gate_blocks_scraping_source() -> None:
    r = check_draft(
        subject="ملاحظة سريعة",
        body=_CLEAN_BODY,
        personalization_level=int(PersonalizationLevel.P2),
        evidence_level=2,
        unsubscribe_included=True,
        lead_source="scraping",
    )
    assert r.passed is False
    assert "blocked_source" in r.reasons


def test_gate_blocks_missing_unsubscribe() -> None:
    r = check_draft(
        subject="ملاحظة سريعة",
        body=_CLEAN_BODY,
        personalization_level=int(PersonalizationLevel.P2),
        evidence_level=2,
        unsubscribe_included=False,
    )
    assert r.passed is False
    assert "missing_unsubscribe" in r.reasons


def test_gate_blocks_personalization_below_p1() -> None:
    r = check_draft(
        subject="ملاحظة سريعة",
        body=_CLEAN_BODY,
        personalization_level=int(PersonalizationLevel.P0),
        evidence_level=2,
        unsubscribe_included=True,
    )
    assert r.passed is False
    assert "personalization_below_p1" in r.reasons


def test_gate_blocks_suppressed_recipient() -> None:
    r = check_draft(
        subject="ملاحظة سريعة",
        body=_CLEAN_BODY,
        personalization_level=int(PersonalizationLevel.P2),
        evidence_level=2,
        unsubscribe_included=True,
        recipient_email="stop@example.sa",
        suppression=["STOP@example.sa"],
    )
    assert r.passed is False
    assert "suppressed_recipient" in r.reasons


def test_gate_blocks_fake_thread_subject() -> None:
    r = check_draft(
        subject="Re: our previous deal",
        body=_CLEAN_BODY,
        personalization_level=int(PersonalizationLevel.P2),
        evidence_level=2,
        unsubscribe_included=True,
    )
    assert r.passed is False
    assert "fake_thread_prefix" in r.reasons


# --- draft factory ----------------------------------------------------------

def _prospects(n: int = 5) -> list[Prospect]:
    return [
        Prospect(
            prospect_id=f"p{i}",
            company=f"شركة {i}",
            sector="marketing_agencies",
            recipient_role="مدير العمليات",
            source="founder_supplied",
            score=72,
        )
        for i in range(n)
    ]


def test_factory_produces_250_draft_only() -> None:
    drafts = produce_drafts(
        _prospects(), offers=["Free AI Ops Diagnostic", "7-Day Revenue Intelligence Sprint"]
    )
    assert len(drafts) == DAILY_DRAFT_TARGET
    assert all(d.send_status == SendStatus.DRAFT.value for d in drafts)
    assert all(d.unsubscribe_included for d in drafts)
    assert all(d.governance_decision != "PENDING" for d in drafts)


def test_factory_batch_summary_zero_auto_sends() -> None:
    drafts = produce_drafts(_prospects(), offers=["Free AI Ops Diagnostic"])
    summary = summarize_batch(drafts)
    assert summary["auto_sent"] == 0
    assert summary["generated"] == DAILY_DRAFT_TARGET
    assert summary["quality_passed"] == DAILY_DRAFT_TARGET  # default copy is compliant


def test_factory_empty_prospects_returns_empty() -> None:
    assert produce_drafts([], offers=["x"]) == []


# --- approval queue ---------------------------------------------------------

def test_rank_for_approval_returns_eligible_top_n() -> None:
    drafts = produce_drafts(_prospects(), offers=["Free AI Ops Diagnostic"])
    queue = rank_for_approval(drafts, top_n=50)
    assert len(queue) == 50
    assert all(d.compliance_status == ComplianceStatus.PASSED.value for d in queue)


# --- sending ramp -----------------------------------------------------------

def test_ramp_caps_by_week() -> None:
    assert max_sends_for_week(0) == 20
    assert max_sends_for_week(4) == 250
    assert max_sends_for_week(99) == 250


def test_ramp_allows_within_cap_when_all_conditions_met() -> None:
    d = allowed_sends_today(
        week=1,
        approved_count=100,
        has_approval=True,
        domain_health_ok=True,
        suppression_ok=True,
        personalization_ok=True,
    )
    assert d.allowed_sends == 50  # capped to week-1 max
    assert d.blocked is False


def test_ramp_blocks_without_approval() -> None:
    d = allowed_sends_today(
        week=2,
        approved_count=100,
        has_approval=False,
        domain_health_ok=True,
        suppression_ok=True,
        personalization_ok=True,
    )
    assert d.allowed_sends == 0
    assert d.blocked is True
    assert "no_founder_approval" in d.reasons


def test_ramp_blocks_on_bad_domain_health() -> None:
    d = allowed_sends_today(
        week=4,
        approved_count=100,
        has_approval=True,
        domain_health_ok=False,
        suppression_ok=True,
        personalization_ok=True,
    )
    assert d.allowed_sends == 0
    assert "domain_health_not_ok" in d.reasons


# --- reply router -----------------------------------------------------------

def test_reply_unsubscribe_suppresses() -> None:
    assert classify_reply("Please unsubscribe me") == ReplyClass.UNSUBSCRIBE
    routing = classify_and_route("الرجاء إيقاف الرسائل")
    assert routing.suppress is True
    assert routing.next_action == "suppress_immediately"


def test_reply_positive_routes_to_discovery() -> None:
    routing = classify_and_route("أنا مهتم، نقدر نحدد موعد؟")
    assert routing.reply_class == ReplyClass.POSITIVE.value
    assert routing.suppress is False


def test_reply_price_question() -> None:
    assert classify_reply("ما هو السعر؟") == ReplyClass.PRICE_QUESTION


# --- reports ----------------------------------------------------------------

def test_daily_report_marks_invariant_pass() -> None:
    md = daily_gtm_report({"drafts_generated": 250, "auto_sent": 0})
    assert "Daily GTM Report" in md
    assert "PASS" in md
    assert "drafts_generated" in md


def test_weekly_review_renders() -> None:
    md = weekly_gtm_review({"best_sector": "clinics"})
    assert "Weekly GTM Review" in md
    assert "clinics" in md
