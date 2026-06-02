"""Tests for the Dealix Market Production OS (stdlib-only; no pydantic needed)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dealix.market_production_os import (
    OFFERS,
    SECTORS,
    check_draft,
    classify,
    email_sha256,
    evaluate_account,
    produce_daily,
    qualify,
    ready_to_send,
    score_prospect,
    store,
)
from dealix.market_production_os.compliance_gate import check_draft as check
from dealix.market_production_os.control_room import assemble_report, produce_and_store
from dealix.market_production_os.draft_factory import DEFAULT_MIX, build_draft
from dealix.market_production_os.personalization import personalization_floor_ok
from dealix.market_production_os.sending_ramp import (
    allowed_sends,
    can_advance_phase,
    filter_suppressed,
    phase_cap,
    plan_batch,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SENDER = {
    "from_name": "Dealix",
    "from_email": "team@go.dealix-mail.sa",
    "physical_address": "Riyadh, KSA",
}


def _clean_prospect(**overrides):
    base = {
        "prospect_id": "pr_t",
        "company": "Test Co (sample)",
        "sector": "marketing_agencies",
        "decision_maker_role": "مدير الوكالة",
        "decision_maker_clear": True,
        "source": "founder_input",
        "pain_hypothesis": "ضياع متابعة الفرص",
        "pain_clear": True,
        "has_expected_leads": True,
        "payment_capacity": "high",
        "personalization_available": True,
        "personalization_level": "P2",
        "personalization_note": "ملاحظة حقيقية عن الشركة",
        "risk_level": "low",
        "status": "qualified",
        "language": "ar",
    }
    base.update(overrides)
    return base


def _clean_draft(**overrides):
    draft = build_draft(
        _clean_prospect(),
        touch_type="first_touch",
        offer="revenue_diagnostic",
        sender_identity=_SENDER,
    )
    draft.update(overrides)
    return draft


# --- catalog + helpers -------------------------------------------------------


def test_catalog_has_seven_offers_with_canonical_prices():
    assert set(OFFERS) == {
        "free_diagnostic",
        "revenue_diagnostic",
        "lead_intelligence_sprint",
        "pilot_conversion_sprint",
        "monthly_revops_starter",
        "monthly_revops_growth",
        "enterprise_revenue_os",
    }
    assert OFFERS["revenue_diagnostic"]["price_sar_min"] == 3500
    assert OFFERS["lead_intelligence_sprint"]["price_sar_min"] == 9500
    assert OFFERS["pilot_conversion_sprint"]["price_sar_min"] == 22000
    assert OFFERS["free_diagnostic"]["price_sar_min"] == 0


def test_email_sha256_is_normalized_and_stable():
    assert email_sha256("A@B.com ") == email_sha256("a@b.com")
    assert len(email_sha256("a@b.com")) == 64


def test_sectors_include_ten_plus_other():
    assert len(SECTORS) == 11
    assert "other" in SECTORS


# --- prospect scoring --------------------------------------------------------


def test_maxed_prospect_scores_100():
    p = _clean_prospect(personalization_level="P4")
    assert score_prospect(p).total == 100


def test_weak_prospect_below_threshold_not_qualified():
    p = _clean_prospect(
        has_expected_leads=False,
        decision_maker_clear=False,
        payment_capacity="unknown",
        personalization_level="P1",
        risk_level="medium",
    )
    assert score_prospect(p).total < 60
    assert qualify(p) is False


def test_do_not_contact_never_qualifies():
    p = _clean_prospect(status="do_not_contact")
    assert qualify(p) is False


# --- personalization floor ---------------------------------------------------


@pytest.mark.parametrize("level,ok", [("P0", False), ("P1", True), ("P2", True), ("P4", True)])
def test_personalization_floor(level, ok):
    assert personalization_floor_ok(level, "first_touch") is ok


def test_warm_context_exempt_from_floor():
    assert personalization_floor_ok("P0", "first_touch", is_warm=True) is True


# --- compliance gate ---------------------------------------------------------


def test_clean_draft_passes_all_gates():
    assert check_draft(_clean_draft()).allowed is True


def test_missing_unsubscribe_fails():
    res = check(_clean_draft(unsubscribe_included=False, unsubscribe_method="none"))
    assert res.allowed is False
    assert "missing_unsubscribe" in res.failures


def test_misleading_subject_prefix_fails():
    res = check(_clean_draft(subject="Re: عرض سريع"))
    assert res.allowed is False
    assert "misleading_subject_prefix" in res.failures


def test_guaranteed_claim_fails():
    assert check(_clean_draft(body="نضمن لك مبيعات خلال أسبوع")).allowed is False
    assert check(_clean_draft(body="We guarantee ROI in 30 days")).allowed is False


def test_forbidden_channel_term_fails():
    assert check(_clean_draft(body="we will use cold whatsapp to reach everyone")).allowed is False


def test_hype_word_fails():
    assert check(_clean_draft(body="this will 10x your revenue")).allowed is False


def test_unknown_offer_fails():
    res = check(_clean_draft(offer="totally_made_up"))
    assert res.allowed is False
    assert any(f.startswith("unknown_offer") for f in res.failures)


def test_incomplete_sender_identity_fails():
    res = check(_clean_draft(sender_identity={"from_name": "Dealix", "from_email": "x@y.sa"}))
    assert res.allowed is False
    assert "incomplete_sender_identity" in res.failures


def test_suppressed_recipient_fails():
    h = email_sha256("optout@example.test")
    res = check(_clean_draft(), suppressed_hashes={h}, recipient_email_sha256=h)
    assert res.allowed is False
    assert "recipient_suppressed" in res.failures


def test_p0_first_touch_blocked_by_personalization_gate():
    res = check(_clean_draft(personalization_level="P0"))
    assert res.allowed is False
    assert any(f.startswith("personalization_below_floor") for f in res.failures)


# --- deliverability ----------------------------------------------------------


def test_seed_accounts_ready_and_not_ready():
    accounts = {a["account_id"]: a for a in store.load("email_accounts")}
    assert ready_to_send(accounts["ea_sample_ready"]) is True
    assert ready_to_send(accounts["ea_sample_notready"]) is False
    assert evaluate_account(accounts["ea_sample_ready"]).health_score == 100


def test_missing_dkim_makes_account_not_ready():
    ready = {a["account_id"]: a for a in store.load("email_accounts")}["ea_sample_ready"]
    broken = dict(ready)
    broken["dkim"] = False
    assert ready_to_send(broken) is False


# --- sending ramp ------------------------------------------------------------


def test_phase_caps():
    assert phase_cap(0) == 20
    assert phase_cap(1) == 50
    assert phase_cap(2) == 150
    assert phase_cap(3) == 250


def test_allowed_sends_respects_phase_and_readiness():
    accounts = {a["account_id"]: a for a in store.load("email_accounts")}
    ready = accounts["ea_sample_ready"]
    assert allowed_sends(0, ready) == 20  # phase0 cap below daily_cap 50
    assert allowed_sends(3, ready) == 50  # phase3 cap 250, but daily_cap 50
    assert allowed_sends(3, accounts["ea_sample_notready"]) == 0


def test_allowed_sends_zero_on_bounce_or_spam_ceiling():
    ready = {a["account_id"]: a for a in store.load("email_accounts")}["ea_sample_ready"]
    assert allowed_sends(1, ready, bounce_rate=0.05) == 0
    assert allowed_sends(1, ready, spam_rate=0.01) == 0


def test_can_advance_phase_blocked_by_ceilings_and_at_max():
    assert can_advance_phase(0) is True
    assert can_advance_phase(3) is False
    assert can_advance_phase(1, bounce_rate=0.04) is False
    assert can_advance_phase(1, spam_rate=0.01) is False


def test_filter_suppressed():
    assert filter_suppressed(["a", "b", "c"], {"b"}) == ["a", "c"]


def test_plan_batch_caps_to_allowed():
    ready = {a["account_id"]: a for a in store.load("email_accounts")}["ea_sample_ready"]
    batch = plan_batch(
        batch_id="b1",
        date="2026-06-02",
        account=ready,
        phase=0,
        draft_ids=[f"d{i}" for i in range(50)],
    )
    assert batch["planned_count"] == 20
    assert len(batch["draft_ids"]) == 20
    assert batch["status"] == "planned"


# --- reply classifier --------------------------------------------------------


@pytest.mark.parametrize(
    "text,expected",
    [
        ("نعم مهتم نبدأ متى", "positive"),
        ("كم السعر؟", "price_question"),
        ("ابعث لي تفاصيل أكثر", "send_more_info"),
        ("غير مهتم لا شكراً", "not_interested"),
        ("الرجاء الإيقاف", "unsubscribe"),
        ("please unsubscribe me", "unsubscribe"),
        ("out of office until next week", "auto_reply"),
        ("mailer-daemon: address not found", "bounce"),
        ("لست المسؤول عن هذا", "wrong_person"),
        ("نتواصل لاحقاً الربع القادم", "interested_but_later"),
    ],
)
def test_classify_taxonomy(text, expected):
    assert classify(text).classification == expected


def test_suppress_flags_on_optout_bounce():
    assert classify("الرجاء الإيقاف").suppress is True
    assert classify("mailer-daemon undeliverable").suppress is True
    assert classify("نعم مهتم").suppress is False


def test_ambiguous_routes_to_founder():
    res = classify("...")
    assert res.requires_founder is True
    assert res.confidence < 0.5


# --- draft factory -----------------------------------------------------------


def test_build_draft_carries_optout_and_sender():
    d = build_draft(_clean_prospect(), sender_identity=_SENDER)
    assert d["unsubscribe_included"] is True
    assert d["unsubscribe_method"] == "reply_keyword"
    assert "إيقاف" in d["body"]
    assert d["sender_identity"]["physical_address"]
    assert not d["subject"].lower().startswith("re:")


def test_produce_daily_hits_target_and_all_pass_gate():
    prospects = [p for p in store.load("prospects") if qualify(p)]
    drafts = produce_daily(prospects, sender_identity=_SENDER, target=250)
    assert len(drafts) == 250
    assert sum(DEFAULT_MIX.values()) == 250
    touches = {d["touch_type"] for d in drafts}
    assert touches == set(DEFAULT_MIX)
    assert all(check_draft(d).allowed for d in drafts)


def test_produce_daily_empty_prospects():
    assert produce_daily([], sender_identity=_SENDER) == []


# --- store -------------------------------------------------------------------


def test_store_env_override_roundtrip(tmp_path, monkeypatch):
    target = tmp_path / "drafts.jsonl"
    monkeypatch.setenv("DEALIX_OUTREACH_DRAFTS_PATH", str(target))
    assert store.read_all("drafts") == []
    store.append("drafts", {"draft_id": "x", "ok": True})
    rows = store.read_all("drafts")
    assert rows == [{"draft_id": "x", "ok": True}]


def test_load_falls_back_to_seed(monkeypatch, tmp_path):
    monkeypatch.setenv("DEALIX_PROSPECTS_PATH", str(tmp_path / "empty.jsonl"))
    assert len(store.load("prospects")) == 12  # from committed seed


# --- schemas -----------------------------------------------------------------


def test_all_schemas_are_valid_json_with_id():
    files = sorted((_REPO_ROOT / "schemas").glob("*.schema.json"))
    assert len(files) == 8
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        assert data["$schema"].startswith("https://json-schema.org/")
        assert data["$id"].startswith("https://dealix.sa/schemas/")
        assert data["type"] == "object"
        assert data["additionalProperties"] is False


def test_prospect_source_enum_excludes_scraping():
    schema = json.loads(
        (_REPO_ROOT / "schemas" / "prospect.schema.json").read_text(encoding="utf-8")
    )
    sources = schema["$defs"]["Source"]["enum"]
    assert "scraping" not in sources
    assert "founder_input" in sources


# --- control room ------------------------------------------------------------


def test_assemble_report_has_footer_and_sections():
    report = assemble_report(as_of="2026-06-02")
    assert "القيمة التقديرية ليست قيمة مُتحقَّقة" in report
    assert "Founder GTM Control Room" in report
    assert "Draft production" in report


def test_produce_and_store_writes_passing_drafts(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_OUTREACH_DRAFTS_PATH", str(tmp_path / "drafts.jsonl"))
    drafts = produce_and_store(target=50)
    assert len(drafts) == 50
    assert all(d["compliance_status"] == "pass" for d in drafts)
