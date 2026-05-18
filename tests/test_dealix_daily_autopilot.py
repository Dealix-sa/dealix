"""Tests for the Daily Autopilot orchestrator.

Validates the founder-approved autopilot doctrine:
- Every queued item is action_mode="draft_only" — never auto-send (Article 4)
- The doctrine block hard-asserts no auto-send / publish / charge
- Rung 2-5 pre-staging flags are ALL inert (Commercial Freeze)
- is_estimate=True (Article 8)
- Targeting is skipped without a founder-supplied candidate list (no scraping)
- Composition produces content drafts + a populated approval queue
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from auto_client_acquisition.approval_center import get_default_approval_store
from scripts import dealix_daily_autopilot as ap


@pytest.fixture(autouse=True)
def _clean_store():
    """Each test starts with an empty approval store (process-scoped singleton)."""
    get_default_approval_store().clear()
    yield
    get_default_approval_store().clear()


def _pack():
    return ap.build_autopilot_pack(on_date=date(2026, 5, 18))


def test_pack_has_content_drafts_and_queue() -> None:
    pack = _pack()
    assert len(pack["content_drafts"]) == len(ap.DEFAULT_CONTENT_PLAN)
    assert len(pack["approval_queue"]) == len(pack["content_drafts"])
    assert len(pack["queued_approval_ids"]) == len(pack["content_drafts"])


def test_every_queued_item_is_draft_only() -> None:
    """Article 4 — autopilot queues drafts, never live sends."""
    pack = _pack()
    assert pack["approval_queue"], "expected a non-empty queue"
    for item in pack["approval_queue"]:
        assert item["action_mode"] == "draft_only"
        assert item["status"] == "pending"


def test_doctrine_block_forbids_autonomous_action() -> None:
    d = _pack()["doctrine"]
    assert d["action_mode"] == "draft_only"
    assert d["auto_send"] is False
    assert d["auto_publish"] is False
    assert d["auto_charge"] is False


def test_rung_2_5_flags_all_inert() -> None:
    """Commercial Freeze — every rung 2-5 flag stays False."""
    assert all(v is False for v in ap.RUNG_2_5_FLAGS.values())
    status = ap.rung_2_5_status()
    assert status["all_inert"] is True


def test_pack_marks_estimates() -> None:
    """Article 8 — numeric outputs are estimates."""
    assert _pack()["is_estimate"] is True


def test_content_drafts_require_approval() -> None:
    for draft in _pack()["content_drafts"]:
        assert draft["approval_required"] is True
        assert draft["action_mode"] == "draft_only"


def test_targeting_skipped_without_candidate_list() -> None:
    """Dealix never scrapes — targeting needs a founder-supplied list."""
    targeting = _pack()["targeting"]
    assert targeting["status"] == "skipped"
    assert targeting["top_leads"] == []


def test_render_markdown_has_all_sections() -> None:
    md = ap.render_markdown(_pack())
    for heading in (
        "Today's single action",
        "Approval queue",
        "Content drafts",
        "Lead targeting",
        "Rung 2-5 pre-stage",
    ):
        assert heading in md
    assert "draft_only" in md
    assert "never auto-send" in md


def test_custom_content_plan_is_honored() -> None:
    plan = [
        {"sector": "fintech", "angle": "manual reconciliation", "content_type": "linkedin_post"}
    ]
    pack = ap.build_autopilot_pack(on_date=date(2026, 5, 18), content_plan=plan)
    assert len(pack["content_drafts"]) == 1
    assert pack["content_drafts"][0]["sector"] == "fintech"
