"""Contract: the Daily Draft Factory produces >=400 review-only drafts with
immutable safety flags. Nothing is ever marked sendable."""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "scripts"))

import commercial_launch_core as core


def _drafts(target: int = 400):
    cfg = core.load_all_configs()
    return core.generate_drafts(target=target, leads=core.load_seed_leads(),
                                configs=cfg, date_str="2026-01-01")


def test_generates_at_least_400_drafts():
    drafts = _drafts(400)
    assert len(drafts) >= 400


def test_every_draft_is_send_disallowed():
    for d in _drafts(400):
        assert d["send_allowed"] is False
        assert d["external_send_blocked"] is True
        assert d["requires_founder_approval"] is True
        assert d["no_auto_send"] is True


def test_no_forbidden_status_anywhere():
    for d in _drafts(400):
        assert d["status"] in core.ALLOWED_STATUSES
        assert d["status"] not in core.FORBIDDEN_STATUSES


def test_distribution_minimums():
    drafts = _drafts(400)
    by_channel = core._count_by(drafts, "channel")
    # primary distribution minimums (stress drafts add a few extra cold_email)
    assert by_channel.get("cold_email", 0) >= 175
    assert by_channel.get("follow_up", 0) >= 100
    assert by_channel.get("linkedin", 0) >= 75
    assert by_channel.get("website_form", 0) >= 50


def test_all_five_verticals_present():
    drafts = _drafts(400)
    verts = set(core._count_by(drafts, "vertical"))
    expected = {v["id"] for v in core.load_config("verticals")["verticals"]}
    assert expected.issubset(verts)


def test_rejected_drafts_have_reasons():
    drafts = _drafts(400)
    rejected = [d for d in drafts if d["status"].startswith("rejected")]
    assert rejected, "stress set must produce at least one rejected draft"
    for d in rejected:
        assert d["rejection_reason"].strip()


def test_each_draft_has_full_schema():
    drafts = _drafts(120)
    for d in drafts:
        for field in core.DRAFT_FIELDS:
            assert field in d, f"missing field {field}"


def test_generator_is_deterministic():
    cfg = core.load_all_configs()
    a = core.generate_drafts(target=120, leads=core.load_seed_leads(), configs=cfg, date_str="2026-01-01")
    b = core.generate_drafts(target=120, leads=core.load_seed_leads(), configs=cfg, date_str="2026-01-01")
    assert [d["draft_id"] for d in a] == [d["draft_id"] for d in b]
    assert [d["body"] for d in a] == [d["body"] for d in b]
