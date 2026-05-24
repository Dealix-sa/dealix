"""Quality-gate tests — campaign validation + anti-vanity."""

from __future__ import annotations

from dealix.revenue_marketing.quality_gates import (
    enforce_no_vanity,
    validate_campaign,
    validate_content,
)
from dealix.revenue_marketing.schemas import MarketingCampaign


def _campaign(**overrides: str) -> MarketingCampaign:
    base = {
        "id": "camp_1",
        "campaign_name": "Pilot",
        "target_segment": "smb_founders",
        "offer_id": "off_1",
        "channel": "linkedin",
        "message_angle": "money",
        "budget_sar": 1000,
        "success_metric": "qualified_leads",
        "scale_kill_rule": "kill_if_under_5_pct_close_rate",
        "tracking_url_pattern": "?utm_source=dealix",
    }
    base.update(overrides)
    return MarketingCampaign.model_validate(base)


def test_validate_campaign_passes_when_complete() -> None:
    assert validate_campaign(_campaign()) == []


def test_validate_campaign_flags_missing_target_segment() -> None:
    missing = validate_campaign(_campaign(target_segment=""))
    assert "target_segment_missing" in missing


def test_validate_campaign_flags_missing_offer() -> None:
    missing = validate_campaign(_campaign(offer_id=""))
    assert "offer_id_missing" in missing


def test_validate_campaign_flags_missing_success_metric() -> None:
    missing = validate_campaign(_campaign(success_metric=""))
    assert "success_metric_missing" in missing


def test_validate_campaign_flags_missing_scale_kill_rule() -> None:
    missing = validate_campaign(_campaign(scale_kill_rule=""))
    assert "scale_kill_rule_missing" in missing


def test_validate_campaign_flags_multiple_missing() -> None:
    missing = validate_campaign(
        _campaign(
            target_segment="",
            offer_id="",
            success_metric="",
            scale_kill_rule="",
        ),
    )
    for key in (
        "target_segment_missing",
        "offer_id_missing",
        "success_metric_missing",
        "scale_kill_rule_missing",
    ):
        assert key in missing


def test_validate_content_flags_missing_fields() -> None:
    missing = validate_content({"target_segment": "x"})
    assert "pain_missing" in missing
    assert "offer_id_missing" in missing
    assert "cta_missing" in missing


def test_validate_content_passes() -> None:
    payload = {
        "target_segment": "smb_founders",
        "pain": "leaking_revenue",
        "offer_id": "off_1",
        "cta": "Book the audit",
        "success_metric": "qualified_leads",
        "tracking": "utm_required",
    }
    assert validate_content(payload) == []


def test_enforce_no_vanity_blocks_engagement_with_zero_conversion() -> None:
    assert enforce_no_vanity("impressions", 0) is False
    assert enforce_no_vanity("likes", 0) is False
    assert enforce_no_vanity("engagement_rate", 0) is False


def test_enforce_no_vanity_passes_when_downstream_present() -> None:
    assert enforce_no_vanity("impressions", 1) is True
    assert enforce_no_vanity("ctr", 5) is True


def test_enforce_no_vanity_passes_non_engagement_metric() -> None:
    assert enforce_no_vanity("won_deals", 0) is True
    assert enforce_no_vanity("revenue_attributed", 0) is True
