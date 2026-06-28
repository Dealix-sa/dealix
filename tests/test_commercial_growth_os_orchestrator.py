"""End-to-end orchestrator behaviour."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.commercial import safety
from app.commercial.orchestrator import run_growth_os, write_reports

DATA = Path(__file__).resolve().parents[1] / "data" / "commercial"


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    yield


def _accounts():
    return json.loads((DATA / "accounts.sample.json").read_text())["accounts"]


def _replies():
    return json.loads((DATA / "replies.sample.json").read_text())["replies"]


def test_orchestrator_runs_full_pipeline():
    result = run_growth_os(_accounts(), _replies())
    assert result.safety_ok is True
    assert result.snapshot is not None
    assert len(result.accounts) == 5
    assert len(result.cards) == 5
    assert len(result.replies) == 6
    assert len(result.booking_options) == 5
    assert len(result.proposals) == 5
    assert len(result.followups) > 0


def test_every_card_has_decision_and_next_action():
    result = run_growth_os(_accounts(), _replies())
    for card in result.cards:
        assert card.owner_decision  # never empty
        assert card.next_action
        assert card.approval_required is True


def test_decision_queue_present():
    result = run_growth_os(_accounts(), _replies())
    assert result.decisions_required >= 1
    assert result.snapshot.next_actions  # operator has a worklist


def test_write_reports(tmp_path):
    result = run_growth_os(_accounts(), _replies())
    paths = write_reports(result, tmp_path)
    assert Path(paths["json"]).exists()
    assert Path(paths["md"]).exists()
    payload = json.loads(Path(paths["json"]).read_text())
    assert payload["safety_ok"] is True
    assert "snapshot" in payload


def test_orchestrator_blocks_when_unsafe(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    result = run_growth_os(_accounts(), _replies())
    assert result.safety_ok is False
    assert result.safety_violations
    assert result.snapshot is None  # no artefacts built in unsafe state
