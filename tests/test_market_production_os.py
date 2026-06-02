"""Tests for the Market Production OS governed core.

Covers production targets, the sending ramp, suppression, subject safety, the
draft/batch gates, reply routing, governance integration, and schema/seed-data
validation. These act as doctrine guards for the go-to-market machine.
"""

from __future__ import annotations

from dealix.marketing_factory import market_production_os as mpo

# --- production targets -----------------------------------------------------


def test_daily_draft_mix_sums_to_250() -> None:
    assert mpo.draft_mix_total() == mpo.DRAFTS_PER_DAY == 250
    assert sum(mpo.daily_draft_mix().values()) == 250
    # mutating the returned copy must not change the source of truth
    mix = mpo.daily_draft_mix()
    mix["first_touch"] = 0
    assert mpo.daily_draft_mix()["first_touch"] == 100


# --- sending ramp + health --------------------------------------------------


def test_health_ok_thresholds() -> None:
    assert mpo.health_ok(None) is True
    assert mpo.health_ok({}) is True
    assert mpo.health_ok({"bounce_rate": 0.02, "spam_complaint_rate": 0.001}) is True
    assert mpo.health_ok({"bounce_rate": 0.03}) is False
    assert mpo.health_ok({"spam_complaint_rate": 0.003}) is False
    assert mpo.health_ok({"provider_warning": True}) is False


def test_sending_ramp_cap_progression() -> None:
    assert mpo.sending_ramp_cap(0) == 20
    assert mpo.sending_ramp_cap(1) == 50
    assert mpo.sending_ramp_cap(2) == 100
    assert mpo.sending_ramp_cap(3) == 150
    assert mpo.sending_ramp_cap(4) == 250
    assert mpo.sending_ramp_cap(9) == 250  # steady state
    assert mpo.sending_ramp_cap(-1) == 0


def test_sending_ramp_cap_pauses_on_unhealthy_domain() -> None:
    # 250/day is only reachable at week 4+ AND when health is within thresholds.
    assert mpo.sending_ramp_cap(4, {"bounce_rate": 0.05}) == 0
    assert mpo.sending_ramp_cap(4, {"spam_complaint_rate": 0.01}) == 0
    assert mpo.sending_ramp_cap(4, {"provider_warning": True}) == 0
    assert mpo.sending_ramp_cap(4, {"bounce_rate": 0.0}) == 250


def test_account_week_mapping() -> None:
    assert mpo.account_week({"warmup_stage": "week0"}) == 0
    assert mpo.account_week({"warmup_stage": "steady"}) == 4
    assert mpo.account_week({}) == 0


# --- suppression + subject safety ------------------------------------------


def test_is_suppressed_by_type() -> None:
    suppression = [
        {"value": "x@example.sa", "type": "email", "reason": "unsubscribe"},
        {"value": "blocked.example", "type": "domain", "reason": "do_not_contact"},
        {"value": "Bad Co", "type": "company", "reason": "complaint"},
    ]
    assert mpo.is_suppressed({"email": "x@example.sa"}, suppression) is True
    assert mpo.is_suppressed({"domain": "blocked.example"}, suppression) is True
    assert mpo.is_suppressed({"company": "bad co"}, suppression) is True
    assert mpo.is_suppressed({"email": "ok@example.sa"}, suppression) is False
    assert mpo.is_suppressed({}, suppression) is False


def test_subject_is_misleading() -> None:
    assert mpo.subject_is_misleading("Re: our last call") is True
    assert mpo.subject_is_misleading("FWD: invoice") is True
    assert mpo.subject_is_misleading("رد: اجتماعنا") is True
    assert mpo.subject_is_misleading("") is True
    assert mpo.subject_is_misleading(None) is True
    assert mpo.subject_is_misleading("أين تضيع متابعات حملات عملائكم؟") is False


# --- governance integration -------------------------------------------------


def test_governance_blocks_cold_channel_language() -> None:
    assert mpo.governance_allows("Use cold whatsapp to reach everyone") is False
    assert mpo.governance_allows("نراجع معكم خريطة المتابعة خلال نصف ساعة") is True


# --- draft + batch gates ----------------------------------------------------


def _good_draft() -> dict:
    return {
        "draft_id": "T-1",
        "company": "Sample Co",
        "sector": "marketing_agencies",
        "recipient_role": "Ops Manager",
        "offer": "Revenue Leakage Diagnostic",
        "subject": "How to recover lost follow-ups",
        "body": "We help order your follow-ups. One-click unsubscribe included.",
        "language": "en",
        "evidence_level": "L1",
        "risk_level": "low",
        "compliance_status": "pass",
        "approval_status": "approved",
        "send_status": "not_sent",
        "personalization_level": "P2",
        "unsubscribe_included": True,
    }


def test_draft_quality_gate_allows_good_draft() -> None:
    result = mpo.draft_quality_gate(_good_draft())
    assert result["allowed"] is True, result["reasons"]


def test_draft_quality_gate_blocks_missing_unsubscribe() -> None:
    draft = _good_draft()
    draft["unsubscribe_included"] = False
    result = mpo.draft_quality_gate(draft)
    assert result["allowed"] is False
    assert "unsubscribe_missing" in result["reasons"]


def test_draft_quality_gate_blocks_high_risk_and_low_personalization() -> None:
    draft = _good_draft()
    draft["risk_level"] = "high"
    draft["personalization_level"] = "P0"
    result = mpo.draft_quality_gate(draft)
    assert result["allowed"] is False
    assert "risk_high" in result["reasons"]
    assert "personalization_below_P1" in result["reasons"]


def test_draft_quality_gate_blocks_misleading_subject_and_missing_offer() -> None:
    draft = _good_draft()
    draft["subject"] = "Re: our agreement"
    draft["offer"] = ""
    result = mpo.draft_quality_gate(draft)
    assert result["allowed"] is False
    assert "misleading_subject" in result["reasons"]
    assert "offer_missing" in result["reasons"]


def test_draft_quality_gate_blocks_suppressed_recipient() -> None:
    draft = _good_draft()
    draft["company"] = "Bad Co"
    suppression = [{"value": "Bad Co", "type": "company", "reason": "complaint"}]
    result = mpo.draft_quality_gate(draft, suppression)
    assert result["allowed"] is False
    assert "recipient_suppressed" in result["reasons"]


def test_send_gate_requires_approval() -> None:
    draft = _good_draft()
    assert mpo.send_gate(draft)["allowed"] is True
    draft["approval_status"] = "pending"
    blocked = mpo.send_gate(draft)
    assert blocked["allowed"] is False
    assert "not_approved" in blocked["reasons"]


def test_batch_send_allowed_respects_ramp_and_health() -> None:
    account = {"warmup_stage": "week1", "bounce_rate": 0.0, "spam_complaint_rate": 0.0}
    ok_batch = {"status": "approved", "approved_at": "2026-06-02", "batch_size": 40}
    result = mpo.batch_send_allowed(ok_batch, account)
    assert result["allowed"] is True
    assert result["cap"] == 50

    oversize = {"status": "approved", "approved_at": "2026-06-02", "batch_size": 200}
    assert mpo.batch_send_allowed(oversize, account)["allowed"] is False

    unapproved = {"status": "planned", "approved_at": None, "batch_size": 10}
    res = mpo.batch_send_allowed(unapproved, account)
    assert res["allowed"] is False
    assert "batch_not_approved" in res["reasons"]

    sick_account = {"warmup_stage": "week4", "bounce_rate": 0.06}
    assert mpo.batch_send_allowed(ok_batch, sick_account)["allowed"] is False


# --- reply routing ----------------------------------------------------------


def test_reply_next_action_suppresses_opt_out() -> None:
    assert mpo.reply_next_action("unsubscribe") == "suppress"
    assert mpo.reply_next_action("bounce") == "suppress"
    assert mpo.reply_next_action("angry") == "apologize_and_suppress"
    assert mpo.reply_next_action("positive") == "discovery_invite"
    assert mpo.reply_next_action("price_question") == "offer_card"
    assert mpo.reply_next_action("unknown_category") == "founder_review"


# --- schema + data validation ----------------------------------------------


def test_validate_record_catches_problems() -> None:
    schema = {
        "required": ["a"],
        "additionalProperties": False,
        "properties": {
            "a": {"type": "string"},
            "n": {"type": "integer"},
            "e": {"type": "string", "enum": ["x", "y"]},
        },
    }
    assert mpo.validate_record({"a": "ok"}, schema) == []
    assert any("missing required" in e for e in mpo.validate_record({}, schema))
    assert any("wrong type" in e for e in mpo.validate_record({"a": "ok", "n": "no"}, schema))
    assert any("not in enum" in e for e in mpo.validate_record({"a": "ok", "e": "z"}, schema))
    assert any("unexpected field" in e for e in mpo.validate_record({"a": "ok", "z": 1}, schema))


def test_all_schemas_load() -> None:
    for name in mpo.DATASETS:
        schema = mpo.load_schema(name)
        assert schema.get("type") == "object"
        assert "properties" in schema


def test_all_seed_data_validates_against_schemas() -> None:
    results = mpo.validate_all()
    problems = {name: errs for name, errs in results.items() if errs}
    assert problems == {}, problems


def test_seed_drafts_are_doctrine_clean() -> None:
    # Independent of governance: every shipped draft carries unsubscribe, passes
    # compliance, is at least P1 personalized, and has a non-empty offer.
    drafts = mpo.load_dataset("outreach_draft")
    assert drafts, "expected seed drafts"
    for d in drafts:
        assert d["unsubscribe_included"] is True, d["draft_id"]
        assert d["compliance_status"] == "pass", d["draft_id"]
        assert d["personalization_level"] in mpo.SENDABLE_PERSONALIZATION, d["draft_id"]
        assert d["offer"].strip(), d["draft_id"]
        assert not mpo.subject_is_misleading(d["subject"]), d["draft_id"]


def test_summary_is_clean() -> None:
    summary = mpo.summary()
    assert summary["ok"] is True, summary["errors_by_dataset"]
    assert summary["drafts_per_day"] == 250
    assert summary["datasets"]["sector"] == 10
