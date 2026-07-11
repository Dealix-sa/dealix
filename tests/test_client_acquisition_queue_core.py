"""Tests for the canonical, draft-only client acquisition queue."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dealix.client_acquisition import ClientCard, build_queue, write_queue_bundle


def test_queue_ranks_stronger_warm_signal_first() -> None:
    high = ClientCard(
        company="Warm High Intent Co",
        source="referral",
        signal="requested a scope summary",
        intent_score=95,
        urgency_score=90,
        value_score=80,
        trust_score=90,
        risk_score=10,
    )
    low = ClientCard(
        company="Research Hold Co",
        source="manual_research",
        intent_score=20,
        urgency_score=20,
        value_score=50,
        trust_score=30,
        risk_score=50,
    )

    bundle = build_queue([low, high])

    assert bundle.items[0].client.company == "Warm High Intent Co"
    assert bundle.items[0].status == "needs_founder_review"
    assert bundle.items[-1].status == "research_hold"


def test_every_queue_item_is_approval_gated_and_external_execution_is_disabled() -> None:
    bundle = build_queue([ClientCard(company="Approved Target")])

    assert bundle.mode == "draft-only"
    assert "external_execution_disabled" in bundle.safeguards
    assert all(item.approval_required for item in bundle.items)
    assert all(item.external_action_allowed is False for item in bundle.items)
    assert all("manual" in item.recommended_channel for item in bundle.items)


def test_non_draft_mode_is_rejected() -> None:
    with pytest.raises(ValueError, match="draft-only"):
        build_queue([ClientCard(company="Unsafe Target")], mode="live")


def test_invalid_company_and_scores_are_rejected() -> None:
    with pytest.raises(ValueError, match="company"):
        ClientCard(company="  ")
    with pytest.raises(ValueError, match="between 0 and 100"):
        ClientCard(company="Bad Score", urgency_score=101)
    with pytest.raises(TypeError, match="integer"):
        ClientCard(company="Bad Type", intent_score=True)


def test_written_bundle_contains_no_live_execution_permission(tmp_path: Path) -> None:
    bundle = build_queue(
        [
            ClientCard(
                company="Saudi B2B Co",
                segment="local_b2b",
                likely_pain="فجوة المتابعة",
                offer_fit="Revenue Proof Sprint",
            )
        ]
    )
    output = write_queue_bundle(bundle, tmp_path / "queue.json")
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert payload["mode"] == "draft-only"
    assert payload["items"][0]["external_action_allowed"] is False
    assert payload["items"][0]["approval_required"] is True
    assert "نتيجة مضمونة" not in payload["items"][0]["suggested_copy"]
