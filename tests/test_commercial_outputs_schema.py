"""Every generated draft carries the full required field set."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import commercial_generate_400_drafts as gen  # noqa: E402

REQUIRED_FIELDS = [
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
]


def test_all_required_fields_present():
    drafts = gen.generate(400, "2099-01-02")
    for d in drafts[:50]:
        for f in REQUIRED_FIELDS:
            assert f in d, f"missing field {f}"


def test_scores_in_range():
    drafts = gen.generate(400, "2099-01-02")
    for d in drafts:
        assert 0 <= d["quality_score"] <= 100
        assert 0 <= d["compliance_score"] <= 100
        assert 0 <= d["fit_score"] <= 100
        assert d["risk_level"] in {"low", "medium", "high"}
