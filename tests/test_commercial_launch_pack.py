"""Commercial launch pack — daily-sales-pack, strategy-os, targeting profiles."""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.mark.asyncio
async def test_founder_daily_sales_pack(async_client):
    r = await async_client.get("/api/v1/founder/daily-sales-pack")
    assert r.status_code == 200
    body = r.json()
    assert body.get("schema_version") == 1
    assert "daily_brief" in body
    assert "launch_readiness" in body
    assert body.get("hard_gates", {}).get("no_cold_whatsapp") is True


@pytest.mark.asyncio
async def test_founder_targeting_profiles(async_client):
    r = await async_client.get("/api/v1/founder/targeting-profiles")
    assert r.status_code == 200
    profiles = r.json().get("profiles") or []
    assert len(profiles) >= 3
    assert "discover_body" in profiles[0]


@pytest.mark.asyncio
async def test_strategy_os_rank_use_cases(async_client):
    r = await async_client.post(
        "/api/v1/strategy-os/rank-use-cases",
        json={
            "use_cases": [
                {
                    "name": "lead_intel",
                    "revenue_impact": 0.9,
                    "time_save": 0.7,
                    "data_readiness": 0.6,
                    "ease": 0.8,
                    "low_risk": 0.9,
                },
                {
                    "name": "support_desk",
                    "revenue_impact": 0.5,
                    "time_save": 0.5,
                    "data_readiness": 0.9,
                    "ease": 0.7,
                    "low_risk": 0.95,
                },
            ]
        },
    )
    assert r.status_code == 200
    ranked = r.json().get("ranked") or []
    assert ranked[0]["score"] >= ranked[-1]["score"]


@pytest.mark.asyncio
async def test_leadops_run_includes_outreach_queue_id(async_client):
    r = await async_client.post(
        "/api/v1/leadops/run",
        json={
            "raw_payload": {
                "company": "Test Co",
                "name": "Test",
                "email": "test@example.sa",
                "phone": "+966501234567",
                "sector": "technology",
                "region": "Saudi Arabia",
                "message": "hello",
            },
            "source": "manual",
        },
    )
    assert r.status_code == 200
    body = r.json()
    if body.get("compliance_status") == "allowed":
        assert body.get("outreach_queue_id", "").startswith("leadops_")


def test_commercial_launch_gap_report_builds():
    import importlib.util

    path = Path(__file__).resolve().parents[1] / "scripts" / "commercial_launch_gap_report.py"
    spec = importlib.util.spec_from_file_location("commercial_launch_gap_report", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    report = mod.build_report()
    assert "missing_secrets" in report
    assert report["governance"]["cold_whatsapp_blocked"] is True
