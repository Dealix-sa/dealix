"""Contract: GTM records score prospects and route replies per the plan."""

from __future__ import annotations

from auto_client_acquisition.gtm_os import (
    CompanySignal,
    Prospect,
    Reply,
    SuppressionEntry,
    route_reply,
    score_prospect,
)
from auto_client_acquisition.gtm_os.records import SIGNAL_SOURCES


def test_score_prospect_perfect_is_100_tier_a() -> None:
    res = score_prospect(
        sector_fit=1, buying_signal=1, lead_flow_likelihood=1, decision_maker_clarity=1,
        payment_ability=1, personalization_signal=1, risk_low=1,
    )
    assert res["total"] == 100
    assert res["tier"] == "A"


def test_score_prospect_zero_is_0_tier_c() -> None:
    res = score_prospect(
        sector_fit=0, buying_signal=0, lead_flow_likelihood=0, decision_maker_clarity=0,
        payment_ability=0, personalization_signal=0, risk_low=0,
    )
    assert res["total"] == 0
    assert res["tier"] == "C"


def test_score_prospect_breakdown_uses_weights() -> None:
    res = score_prospect(
        sector_fit=1, buying_signal=1, lead_flow_likelihood=0, decision_maker_clarity=0,
        payment_ability=0, personalization_signal=0, risk_low=0,
    )
    # sector_fit(20) + buying_signal(20) = 40 -> tier B threshold is 50, so C
    assert res["total"] == 40
    assert res["breakdown"]["sector_fit"] == 20
    assert res["tier"] == "C"


def test_score_prospect_clamps_out_of_range() -> None:
    res = score_prospect(
        sector_fit=5, buying_signal=-3, lead_flow_likelihood=1, decision_maker_clarity=1,
        payment_ability=1, personalization_signal=1, risk_low=1,
    )
    # sector_fit clamps to 1 (20), buying_signal clamps to 0 (0), rest full = 20+0+15+15+15+10+5
    assert res["total"] == 80
    assert res["tier"] == "A"


def test_route_reply_unsubscribe_and_bounce_and_angry_suppress() -> None:
    for cls in ("unsubscribe", "bounce", "angry"):
        r = route_reply(cls)
        assert r["requires_suppression"] is True


def test_route_reply_positive_routes_to_discovery_no_suppress() -> None:
    r = route_reply("positive")
    assert r["suggested_action"] == "route_to_discovery"
    assert r["requires_suppression"] is False


def test_route_reply_unknown_is_manual_review() -> None:
    assert route_reply("weird_value")["suggested_action"] == "manual_review"


def test_signal_source_never_scraping() -> None:
    assert "scraping" not in SIGNAL_SOURCES
    sig = CompanySignal(signal_id="s1", signal_type="hiring_sales_ops", source="founder_input")
    assert sig.governance_decision == "approval_required"


def test_records_are_pii_free_by_construction() -> None:
    # Models forbid extra fields, so a raw email/phone field cannot be attached.
    p = Prospect(prospect_ref="acc1", decision_maker_role="CMO", website_domain="example.sa")
    assert p.governance_decision == "approval_required"
    s = SuppressionEntry(recipient_ref="rcpt_1", reason="unsubscribe")
    assert s.permanent is True
    rep = Reply(reply_id="r1", classification="positive")
    assert rep.governance_decision == "approval_required"
