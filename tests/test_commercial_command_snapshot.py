"""Command Room snapshot aggregates artefacts and a decision queue."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.commercial import command_snapshot, safety
from app.commercial.orchestrator import run_growth_os

DATA = Path(__file__).resolve().parents[1] / "data" / "commercial"


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    yield


def _run():
    accounts = json.loads((DATA / "accounts.sample.json").read_text())["accounts"]
    replies = json.loads((DATA / "replies.sample.json").read_text())["replies"]
    return run_growth_os(accounts, replies)


def test_snapshot_has_all_sections():
    snap = _run().snapshot
    assert snap.generated_at
    assert snap.summary["accounts"] == 5
    assert snap.cards
    assert snap.decision_queue
    assert snap.next_actions
    assert "safety_posture" in snap.summary


def test_snapshot_flags_missing_source_as_risk():
    snap = _run().snapshot
    assert any(r["risk"] == "missing_source_url" for r in snap.risks)


def test_markdown_renders_safety_posture():
    snap = _run().snapshot
    md = command_snapshot.render_markdown(snap)
    assert "Command Room" in md
    assert "draft_only" in md
    assert "no external message has been sent" in md.lower()


def test_next_actions_capped_at_10():
    snap = _run().snapshot
    assert len(snap.next_actions) <= 10
