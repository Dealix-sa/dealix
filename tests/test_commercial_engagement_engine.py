"""The living engagement engine: one brain, many channels, all draft."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.commercial import safety
from app.commercial.engagement_engine import run_engagement, write_engagement_report

DATA = Path(__file__).resolve().parents[1] / "data" / "commercial"


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.delenv("COMMERCIAL_LLM_ENABLED", raising=False)
    yield


def _accounts():
    return json.loads((DATA / "accounts.sample.json").read_text())["accounts"]


def _inbound():
    return json.loads((DATA / "inbound_events.sample.json").read_text())["inbound_by_account"]


def test_engagement_runs_and_is_safe():
    res = run_engagement(_accounts(), inbound_by_account=_inbound())
    assert res.safety_ok is True
    assert len(res.accounts) == 5
    assert len(res.conversations) == 5
    assert len(res.action_plan) == 5


def test_every_payload_is_draft_and_not_sendable():
    res = run_engagement(_accounts(), inbound_by_account=_inbound())
    for p in res.payloads:
        assert p["requires_approval"] is True
        assert p["send_status"] in ("draft", "blocked")
        assert p["safety"].get("allowed", False) is False


def test_action_plan_is_prioritised():
    res = run_engagement(_accounts(), inbound_by_account=_inbound())
    priorities = [a["priority"] for a in res.action_plan]
    assert priorities == sorted(priorities)


def test_optout_account_yields_honour_optout():
    res = run_engagement(_accounts(), inbound_by_account=_inbound())
    actions = {a["account_id"]: a["recommended_action"] for a in res.action_plan}
    assert actions.get("acct_005") == "honour_optout"


def test_engagement_blocked_when_unsafe(monkeypatch):
    monkeypatch.setenv("WHATSAPP_ALLOW_LIVE_SEND", "true")
    res = run_engagement(_accounts(), inbound_by_account=_inbound())
    assert res.safety_ok is False
    assert res.safety_violations


def test_write_report(tmp_path):
    res = run_engagement(_accounts(), inbound_by_account=_inbound())
    paths = write_engagement_report(res, tmp_path)
    assert Path(paths["json"]).exists()
    md = Path(paths["md"]).read_text()
    assert "Living Engagement Room" in md
    assert "draft" in md.lower()
