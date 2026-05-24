"""Agent registry + draft-first contract tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from dealix.revenue_marketing.agents import (
    MARKETING_AGENTS,
    propose_via_agent,
)
from dealix.revenue_marketing.store import reset_revenue_marketing_store_for_tests

EXPECTED_AGENTS = {
    "market_radar",
    "audience_research",
    "icp_builder",
    "offer_positioning",
    "content_strategist",
    "copywriter",
    "landing_page",
    "campaign_planner",
    "lead_scoring",
    "attribution",
    "conversion_optimizer",
    "case_study",
}


@pytest.fixture(autouse=True)
def _fresh_store(tmp_path: Path):
    reset_revenue_marketing_store_for_tests(path=tmp_path / "rm.json")


def test_all_twelve_agents_registered() -> None:
    assert set(MARKETING_AGENTS.keys()) == EXPECTED_AGENTS
    assert len(MARKETING_AGENTS) == 12


def test_every_agent_propose_returns_draft() -> None:
    for name in MARKETING_AGENTS:
        out = propose_via_agent(name, {"offer_id": "off_1", "audience_id": "aud_1"})
        assert isinstance(out, dict)
        assert out.get("agent") == name
        assert out.get("requires_approval") is True
        assert out.get("external_send_blocked") is True


def test_unknown_agent_raises() -> None:
    with pytest.raises(ValueError, match="agent_not_registered"):
        propose_via_agent("not_real_agent", {})


def test_no_network_io_during_propose(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail if anyone in the agents path calls requests or httpx at runtime."""

    def _boom(*args, **kwargs):
        raise AssertionError("agents must not make network IO")

    import builtins

    real_import = builtins.__import__

    def _import(name, *a, **k):
        # We allow imports — we are not auditing static imports, only runtime
        # behaviour. The monkeypatches below are the actual guard.
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", _import)

    try:
        import httpx  # type: ignore[import-untyped]

        monkeypatch.setattr(httpx, "get", _boom, raising=False)
        monkeypatch.setattr(httpx, "post", _boom, raising=False)
        if hasattr(httpx, "AsyncClient"):
            monkeypatch.setattr(httpx.AsyncClient, "get", _boom, raising=False)
            monkeypatch.setattr(httpx.AsyncClient, "post", _boom, raising=False)
    except Exception:
        pass

    try:
        import requests  # type: ignore[import-untyped]

        monkeypatch.setattr(requests, "get", _boom, raising=False)
        monkeypatch.setattr(requests, "post", _boom, raising=False)
    except Exception:
        pass

    for name in MARKETING_AGENTS:
        propose_via_agent(name, {"offer_id": "off_1"})


def test_lead_scoring_agent_returns_score() -> None:
    out = propose_via_agent(
        "lead_scoring",
        {
            "icp_fit": 1.0,
            "pain": 1.0,
            "ability_to_pay": 1.0,
            "urgency": 1.0,
            "partner_potential": 1.0,
            "trust_fit": 1.0,
        },
    )
    assert out["score"] == pytest.approx(1.0)
