"""The 400+ daily draft factory generates the right volume and shape."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import commercial_launch_lib as lib  # noqa: E402

REQUIRED_FIELDS = {
    "draft_id",
    "batch_id",
    "created_at",
    "company_name",
    "source_lead_id",
    "vertical",
    "country",
    "city",
    "channel",
    "language",
    "buyer_persona",
    "buyer_title",
    "offer_stage",
    "offer_name",
    "pain_angle",
    "trigger_event",
    "subject",
    "body",
    "cta",
    "opt_out",
    "quality_score",
    "compliance_score",
    "fit_score",
    "priority_score",
    "risk_level",
    "research_required",
    "founder_notes",
    "rejection_reason",
    "status",
    "send_allowed",
    "external_send_blocked",
    "requires_founder_approval",
    "no_auto_send",
}


@pytest.fixture(scope="module")
def drafts():
    return lib.generate_drafts(target=400)


def test_generates_at_least_400(drafts):
    assert len(drafts) >= 400


def test_every_draft_has_required_fields(drafts):
    for d in drafts:
        missing = REQUIRED_FIELDS - set(d.keys())
        assert not missing, f"{d['draft_id']} missing {missing}"


def test_channel_distribution_present(drafts):
    channels = {d["channel"] for d in drafts}
    assert {"cold_email", "follow_up", "linkedin", "website_form"}.issubset(channels)


def test_both_languages_present(drafts):
    langs = {d["language"] for d in drafts}
    assert langs == {"ar", "en"}


def test_all_five_verticals_present(drafts):
    verticals = {d["vertical"] for d in drafts}
    assert len(verticals) == 5


def test_scores_in_range(drafts):
    for d in drafts:
        assert 0.0 <= d["quality_score"] <= 1.0
        assert 0.0 <= d["compliance_score"] <= 1.0
        assert 0.0 <= d["fit_score"] <= 1.0
        assert d["priority_score"] >= 0.0
        assert d["risk_level"] in {"low", "medium", "high"}


def test_higher_target_scales(drafts):
    more = lib.generate_drafts(target=600)
    assert len(more) >= 600


def test_deterministic(drafts):
    again = lib.generate_drafts(target=400)
    assert [d["draft_id"] for d in again] == [d["draft_id"] for d in drafts]
    assert [d["priority_score"] for d in again] == [d["priority_score"] for d in drafts]
