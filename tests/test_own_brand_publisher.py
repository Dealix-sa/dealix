"""Tests for the own-brand social publisher.

Covers the doctrine boundary: own-brand channels (Dealix's own LinkedIn /
X accounts) MAY be auto-published to, but only after the safe publishing
gate is clean. Gate-flagged copy is routed to the approval queue and never
published. Prospect / blocked channels are rejected outright. With no API
token configured the publisher degrades to a dry-run and never crashes.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.self_growth_os import social_publisher


@pytest.fixture(autouse=True)
def _isolated_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Point social_post_log at a temp file and clear the API tokens."""
    monkeypatch.setenv(
        "DEALIX_SOCIAL_POST_LOG_PATH", str(tmp_path / "social_post_log.jsonl")
    )
    monkeypatch.delenv("DEALIX_OWN_LINKEDIN_TOKEN", raising=False)
    monkeypatch.delenv("DEALIX_OWN_X_TOKEN", raising=False)


def _clean_slot(channel: str = "linkedin_own") -> dict[str, str]:
    return {
        "slot_date": "2026-05-20",
        "channel": channel,
        "topic_ar": "كيف تبني عمليات إيرادات محوكمة",
        "topic_en": "How to build governed revenue operations",
    }


def _flagged_slot(channel: str = "linkedin_own") -> dict[str, str]:
    return {
        "slot_date": "2026-05-21",
        "channel": channel,
        "topic_ar": "نتائج مضمونة",
        "topic_en": "guaranteed results for every client",
    }


def test_gate_clean_publishes_dry_run_when_no_token() -> None:
    """Clean copy with no API token → dry-run, intent recorded, nothing sent."""
    result = social_publisher.publish_own_brand(_clean_slot("linkedin_own"))
    assert result["outcome"] == "dry_run"
    assert result["published"] is False
    assert result["gate_decision"] == "allowed_draft"
    assert result["reason"] == "api_token_not_configured"
    log = social_publisher.read_log()
    assert log[-1]["outcome"] == "dry_run"


def test_gate_clean_publishes_when_token_present(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Clean copy with a token configured → published."""
    monkeypatch.setenv("DEALIX_OWN_X_TOKEN", "tok-123")
    result = social_publisher.publish_own_brand(_clean_slot("x_own"))
    assert result["outcome"] == "published"
    assert result["published"] is True
    assert result["endpoint"] == "/2/tweets"


def test_gate_flagged_routes_to_approval_not_published() -> None:
    """Flagged copy → routed to the approval queue, never published."""
    store = ApprovalStore()
    result = social_publisher.publish_own_brand(_flagged_slot(), store=store)
    assert result["outcome"] == "routed_to_approval"
    assert result["published"] is False
    assert "guaranteed" in result["forbidden_tokens"]
    pending = store.list_pending()
    assert len(pending) == 1
    assert pending[0].action_type == "draft_linkedin_manual"
    assert pending[0].channel == "linkedin_own"


def test_gate_flagged_with_token_still_not_published(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The gate is never bypassed — a token does not let flagged copy out."""
    monkeypatch.setenv("DEALIX_OWN_LINKEDIN_TOKEN", "tok-abc")
    store = ApprovalStore()
    result = social_publisher.publish_own_brand(_flagged_slot(), store=store)
    assert result["outcome"] == "routed_to_approval"
    assert result["published"] is False
    assert len(store.list_pending()) == 1


@pytest.mark.parametrize(
    "channel", ["whatsapp", "linkedin", "phone", "linkedin_manual_post"]
)
def test_prospect_and_blocked_channels_rejected(channel: str) -> None:
    """Prospect / blocked channels are rejected and never published."""
    store = ApprovalStore()
    slot = _clean_slot(channel)
    result = social_publisher.publish_own_brand(slot, store=store)
    assert result["outcome"] == "rejected_channel"
    assert result["published"] is False
    assert result["reason"] == "channel_not_own_brand"
    assert store.list_pending() == []


def test_own_brand_channels_constant() -> None:
    """The publisher is restricted to Dealix's own accounts only."""
    assert social_publisher.OWN_BRAND_CHANNELS == frozenset(
        {"linkedin_own", "x_own"}
    )


def test_post_to_api_seam_reports_publish() -> None:
    """_post_to_api reports a successful publish for a present token."""
    assert (
        social_publisher._post_to_api(
            "x_own", "/2/tweets", "tok", "hello"
        )
        is True
    )


def test_api_error_degrades_to_dry_run(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An API error degrades to a dry-run rather than crashing."""
    monkeypatch.setenv("DEALIX_OWN_X_TOKEN", "tok-123")

    def _boom(*_a: object, **_k: object) -> bool:
        raise RuntimeError("network down")

    monkeypatch.setattr(social_publisher, "_post_to_api", _boom)
    result = social_publisher.publish_own_brand(_clean_slot("x_own"))
    assert result["outcome"] == "dry_run"
    assert result["published"] is False
    assert result["reason"].startswith("api_error:")


def test_read_log_and_clear() -> None:
    """social_post_log records every attempt and can be cleared."""
    social_publisher.publish_own_brand(_clean_slot("linkedin_own"))
    social_publisher.publish_own_brand(_clean_slot("x_own"))
    assert len(social_publisher.read_log()) == 2
    social_publisher.clear_log_for_test()
    assert social_publisher.read_log() == []
