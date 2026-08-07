from app.commercial.growth_os_v2 import (
    CommercialAccount,
    can_finalize_proposal,
    can_send_email,
    can_send_whatsapp,
    can_write_calendar,
    classify_reply,
    run_growth_os,
    score_account,
    verify_snapshot,
)


def test_commercial_growth_os_generates_connected_company_outputs():
    snapshot = run_growth_os()
    assert snapshot["summary"]["accounts"] == 3
    assert snapshot["summary"]["cards"] == 3
    assert snapshot["summary"]["replies"] == 3
    assert snapshot["summary"]["booking_options"] == 3
    assert snapshot["summary"]["proposal_briefs"] == 3
    assert snapshot["summary"]["followup_tasks"] == 9
    assert snapshot["decision_queue"]
    assert snapshot["next_10_actions"]
    assert verify_snapshot(snapshot) == []


def test_all_live_channels_are_denied_by_default():
    account = CommercialAccount(
        "a",
        "A",
        "clinics",
        "Riyadh",
        source_url="https://example.com",
        public_email="x@example.com",
        whatsapp="+9665",
        whatsapp_opt_in=True,
    )
    action = {"status": "approved", "owner_decision": "send", "text": "normal message"}
    assert can_send_email(action, account, {}).allowed is False
    assert can_send_whatsapp(action, account, {}).allowed is False
    assert can_write_calendar({"owner_decision": "book"}, account, {}).allowed is False
    assert can_finalize_proposal({"final_price_allowed": True}, account, {}).allowed is False


def test_whatsapp_requires_opt_in_even_in_controlled_design(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("WHATSAPP_SEND_ENABLED", "true")
    monkeypatch.setenv("WHATSAPP_ALLOW_LIVE_SEND", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    account = CommercialAccount(
        "a",
        "A",
        "clinics",
        "Riyadh",
        source_url="https://example.com",
        whatsapp="+9665",
        whatsapp_opt_in=False,
    )
    decision = can_send_whatsapp({"status": "approved", "owner_decision": "send"}, account, {})
    assert decision.allowed is False
    assert "no_opt_in" in decision.blocked_by


def test_reply_classifier_understands_sales_partnership_and_objections():
    assert classify_reply({"reply_id": "r", "card_id": "c", "text": "السعر عالي"}).reply_type == "price_objection"
    assert classify_reply({"reply_id": "r", "card_id": "c", "text": "نحتاج شراكة"}).reply_type == "partnership_interest"
    assert classify_reply({"reply_id": "r", "card_id": "c", "text": "إيقاف"}).reply_type == "unsubscribe"


def test_icp_scoring_uses_sector_city_source_contact_and_pain():
    account = CommercialAccount(
        "a",
        "A",
        "clinics",
        "Riyadh",
        source_url="https://example.com",
        public_email="x@example.com",
        pain_hypothesis="follow-up",
    )
    scored = score_account(account)
    assert scored.icp_score >= 70
    assert scored.risk_level == "low"
