"""DOCTRINE GUARD — marketing operating rules reject malformed assets."""

from __future__ import annotations

from dealix.growth_os.content_engine.operating_rules import (
    MARKETING_OPERATING_RULES,
    check_asset,
    enforce_marketing_rules,
)
from dealix.growth_os.operating_rules import enforce_all


def test_nine_rules_published() -> None:
    keys = {r.key for r in MARKETING_OPERATING_RULES}
    expected = {
        "every_campaign_has_offer",
        "every_offer_has_proof",
        "every_content_has_cta",
        "every_cta_maps_to_paid_offer",
        "every_lead_has_owner",
        "every_deal_has_proof_pack",
        "every_revenue_record_verified",
        "no_external_send_without_approval",
        "no_vanity_metric_reporting",
    }
    assert keys == expected


def test_campaign_without_offer_rejected() -> None:
    violations = check_asset("campaign", {"campaign_id": "c1"})
    assert any(v.rule_key == "every_campaign_has_offer" for v in violations)


def test_content_without_cta_rejected() -> None:
    violations = enforce_marketing_rules({"title": "t", "offer_key": "x"})
    assert any(v.rule_key == "every_content_has_cta" for v in violations)


def test_cta_without_offer_rejected() -> None:
    violations = enforce_marketing_rules(
        {"title": "t", "cta_label": "Read more"}
    )
    assert any(v.rule_key == "every_cta_maps_to_paid_offer" for v in violations)


def test_revenue_record_without_verification_rejected() -> None:
    violations = check_asset("revenue", {"record_id": "r1", "amount_usd": 500})
    assert any(v.rule_key == "every_revenue_record_verified" for v in violations)


def test_deal_without_proof_pack_rejected() -> None:
    violations = check_asset("deal", {"deal_id": "d1"})
    assert any(v.rule_key == "every_deal_has_proof_pack" for v in violations)


def test_lead_without_owner_rejected() -> None:
    violations = check_asset("lead", {"lead_id": "l1"})
    assert any(v.rule_key == "every_lead_has_owner" for v in violations)


def test_offer_without_proof_rejected() -> None:
    violations = check_asset("offer", {"offer_key": "x"})
    assert any(v.rule_key == "every_offer_has_proof" for v in violations)


def test_clean_assets_pass() -> None:
    assert check_asset("campaign", {"offer_key": "revenue_hunter"}) == []
    assert (
        enforce_marketing_rules(
            {"title": "t", "cta_label": "Book diagnostic", "offer_key": "x"}
        )
        == []
    )


def test_enforce_all_batches() -> None:
    out = enforce_all(
        {
            "campaign": [{"id": "1"}],  # missing offer
            "deal": [{"deal_id": "2", "proof_pack_id": "pp"}],  # clean
        }
    )
    assert "campaign" in out
    assert "deal" not in out
