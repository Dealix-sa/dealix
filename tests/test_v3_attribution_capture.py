"""V3 micro-gap: inbound first-touch attribution flows into the governed lead record.

Proves the attribution sanitizer is bounded/allow-listed and that captured UTM data
lands on the persisted FunnelLeadRecord via the orchestrator — without bypassing the
governed autopilot store.
"""

from __future__ import annotations

from pathlib import Path

from dealix.revenue_ops_autopilot.attribution import (
    ALLOWED_ATTRIBUTION_KEYS,
    attribution_summary,
    sanitize_attribution,
)
from dealix.revenue_ops_autopilot.orchestrator import RevenueAutopilotOrchestrator
from dealix.revenue_ops_autopilot.store import AutopilotJSONStore


def test_sanitize_allowlists_and_bounds() -> None:
    raw = {
        "utm_source": "google",
        "utm_medium": "  cpc  ",
        "utm_campaign": "spring",
        "gclid": "abc123",
        "evil_key": "drop-me",  # not allow-listed → dropped
        "utm_term": "x" * 5000,  # over cap → truncated
        "utm_content": None,  # None → dropped
        "referrer": "",  # empty → dropped
    }
    out = sanitize_attribution(raw)
    assert out["utm_source"] == "google"
    assert out["utm_medium"] == "cpc"  # stripped
    assert out["gclid"] == "abc123"
    assert "evil_key" not in out
    assert "utm_content" not in out
    assert "referrer" not in out
    assert len(out["utm_term"]) == 512  # length cap
    assert set(out).issubset(set(ALLOWED_ATTRIBUTION_KEYS))


def test_sanitize_non_dict_returns_empty() -> None:
    assert sanitize_attribution(None) == {}
    assert sanitize_attribution("utm_source=google") == {}
    assert sanitize_attribution(["utm_source"]) == {}


def test_attribution_summary() -> None:
    assert attribution_summary({"utm_source": "google", "utm_medium": "cpc"}) == "google/cpc"
    assert attribution_summary({"utm_campaign": "launch"}) == "launch"
    assert attribution_summary({}) == ""


def test_capture_lead_persists_sanitized_attribution(tmp_path: Path) -> None:
    store = AutopilotJSONStore(path=tmp_path / "store.json")
    orch = RevenueAutopilotOrchestrator(store=store)

    lead = orch.capture_lead(
        {
            "name": "Sara",
            "email": "sara@example.sa",
            "company": "Acme",
            "pain": "need governed AI ops with clear approval boundaries",
            "source": "risk_score_funnel",
            "attribution": {
                "utm_source": "linkedin",
                "utm_medium": "social",
                "utm_campaign": "governed-ai",
                "landing_path": "/ar/dealix-diagnostic",
                "not_allowed": "should-vanish",
            },
        },
    )

    assert lead.attribution["utm_source"] == "linkedin"
    assert lead.attribution["utm_campaign"] == "governed-ai"
    assert lead.attribution["landing_path"] == "/ar/dealix-diagnostic"
    assert "not_allowed" not in lead.attribution

    # Persisted to the governed store and reloadable (no bypass / flat file).
    reloaded = store.get_lead(lead.id)
    assert reloaded is not None
    assert reloaded.attribution == lead.attribution


def test_capture_lead_without_attribution_is_empty(tmp_path: Path) -> None:
    store = AutopilotJSONStore(path=tmp_path / "store.json")
    orch = RevenueAutopilotOrchestrator(store=store)
    lead = orch.capture_lead({"name": "No UTM", "email": "x@example.sa", "pain": "test"})
    assert lead.attribution == {}
