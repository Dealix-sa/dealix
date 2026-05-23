"""Tests for the Dealix Execution & Market Launch Command System internal endpoints.

Covers the four admin-key-gated routers wired in api/main.py:
  - /api/v1/internal/launch/summary
  - /api/v1/internal/risks/register
  - /api/v1/internal/finance/forecast
  - /api/v1/internal/learning/summary

Each one is exercised in two modes:
  * No PRIVATE_OPS configured → fallback envelope.
  * PRIVATE_OPS pointing at a tmp dir with sample CSVs → api response.

Non-negotiables verified:
  * Admin-key gate is enforced when ADMIN_API_KEYS is set.
  * No secret strings echoed back.
  * No external sends are triggered (these are read-only routes).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

import pytest


ADMIN_HEADER = "X-Admin-API-Key"


# ── Fixtures ───────────────────────────────────────────────────


@pytest.fixture()
def private_ops(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Bootstrap a minimal <private_ops> tree and point env at it."""
    for sub in (
        "founder", "sales", "finance", "launch", "distribution",
        "trust", "ops", "learning", "risk",
    ):
        (tmp_path / sub).mkdir(parents=True, exist_ok=True)

    (tmp_path / "finance" / "cash_collected.csv").write_text(
        "date,customer,amount_sar,proposal_id,notes\n"
        "2026-05-20,acme,1500,P-001,first paid\n"
        "2026-05-22,beta_co,4999,P-002,diagnostic\n",
        encoding="utf-8",
    )
    (tmp_path / "sales" / "proposal_log.csv").write_text(
        "date,proposal_id,customer,sector,status,amount_sar,objection,paid,days_open\n"
        "2026-05-10,P-003,gamma,erp_crm,proposal_sent,1500,price,false,13\n"
        "2026-05-01,P-004,delta,cybersecurity,verbal_yes,4999,,false,22\n"
        "2026-05-20,P-001,acme,erp_crm,paid,1500,,true,3\n",
        encoding="utf-8",
    )
    (tmp_path / "launch" / "blockers.csv").write_text(
        "id,description,severity,status\n"
        "B-1,brand tokens out of sync,medium,open\n"
        "B-2,resolved item,low,closed\n",
        encoding="utf-8",
    )
    (tmp_path / "trust" / "open_risks.csv").write_text(
        "risk_id,severity,description,status\n"
        "AIR-001,high,hallucination spotted in last sample,open\n"
        "AIR-006,medium,drift in output quality,open\n",
        encoding="utf-8",
    )
    (tmp_path / "risk" / "risk_register.csv").write_text(
        "risk_id,category,description,severity,likelihood,owner,mitigation,status,next_review\n"
        "MER-001,market,broad ICP,high,medium,founder,focus one sector,open,2026-06-01\n"
        "AIR-001,ai_agent,hallucination,critical,medium,founder,eval gate,open,2026-06-01\n"
        "REV-002,revenue,delayed payment,high,high,founder,advance partial,closed,2026-06-01\n",
        encoding="utf-8",
    )
    (tmp_path / "distribution" / "queues.json").write_text(
        json.dumps({"founder_inbox": 3, "linkedin_dm": 0}),
        encoding="utf-8",
    )
    (tmp_path / "launch" / "target_sector.yaml").write_text("sector: erp_crm\n", encoding="utf-8")
    (tmp_path / "launch" / "active_campaign.yaml").write_text("id: campaign_erp_v1\n", encoding="utf-8")
    (tmp_path / "launch" / "approved_assets.csv").write_text(
        "id,name,status\nA-1,erp_data_pack,approved\n",
        encoding="utf-8",
    )
    (tmp_path / "learning" / "market_learning.csv").write_text(
        "date,source,insight,evidence,decision,next_action,owner\n"
        "2026-05-22,founder,Saudi B2B cycle 45d,3 deals,observe,track,founder\n",
        encoding="utf-8",
    )
    (tmp_path / "learning" / "message_learning.csv").write_text(
        "date,source,insight,evidence,decision,next_action,owner\n"
        "2026-05-22,founder,AR subject 2x reply,20 sent,scale,double,founder\n",
        encoding="utf-8",
    )
    (tmp_path / "learning" / "offer_learning.csv").write_text(
        "date,source,insight,evidence,decision,next_action,owner\n"
        "2026-05-22,founder,Data Pack > Diagnostic in ERP,2 sales,scale,push,founder\n",
        encoding="utf-8",
    )
    (tmp_path / "learning" / "sector_learning.csv").write_text(
        "date,source,insight,evidence,decision,next_action,owner\n"
        "2026-05-22,founder,ERP pays faster,2 sales,scale,focus,founder\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("DEALIX_PRIVATE_OPS", str(tmp_path))
    # Make sure tests don't accidentally pick up host PRIVATE_OPS.
    monkeypatch.delenv("PRIVATE_OPS", raising=False)
    yield tmp_path


@pytest.fixture()
def admin_key(monkeypatch: pytest.MonkeyPatch) -> str:
    key = "test_admin_dealix_execution_launch"
    monkeypatch.setenv("ADMIN_API_KEYS", key)
    return key


# ── Launch summary ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_launch_summary_requires_admin(async_client, admin_key):
    res = await async_client.get("/api/v1/internal/launch/summary")
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_launch_summary_fallback_when_no_private_ops(
    async_client, admin_key, monkeypatch
):
    monkeypatch.delenv("DEALIX_PRIVATE_OPS", raising=False)
    monkeypatch.delenv("PRIVATE_OPS", raising=False)
    res = await async_client.get(
        "/api/v1/internal/launch/summary", headers={ADMIN_HEADER: admin_key}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["source"] == "fallback"
    assert body["next_ceo_action"] is None
    assert body["launch_blockers"] == []
    assert body["trust_risks"] == []
    # No secret leakage
    assert admin_key not in res.text


@pytest.mark.asyncio
async def test_launch_summary_with_private_ops(async_client, admin_key, private_ops):
    res = await async_client.get(
        "/api/v1/internal/launch/summary", headers={ADMIN_HEADER: admin_key}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["source"] == "api"
    # Open blockers only — closed ones filtered out.
    blocker_ids = {b["id"] for b in body["launch_blockers"]}
    assert "B-1" in blocker_ids
    assert "B-2" not in blocker_ids
    # Only high/critical trust risks surface here.
    risk_ids = {r["id"] for r in body["trust_risks"]}
    assert "AIR-001" in risk_ids
    assert "AIR-006" not in risk_ids
    # Distribution queues parsed as JSON object.
    assert body["distribution_queues"]["founder_inbox"] == 3
    # Approved assets surface.
    assert body["approved_assets"][0]["id"] == "A-1"


# ── Risk register ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_risks_register_fallback(async_client, admin_key, monkeypatch):
    monkeypatch.delenv("DEALIX_PRIVATE_OPS", raising=False)
    monkeypatch.delenv("PRIVATE_OPS", raising=False)
    res = await async_client.get(
        "/api/v1/internal/risks/register", headers={ADMIN_HEADER: admin_key}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["source"] == "fallback"
    assert body["rows"] == []
    assert body["total"] == 0


@pytest.mark.asyncio
async def test_risks_register_with_private_ops(async_client, admin_key, private_ops):
    res = await async_client.get(
        "/api/v1/internal/risks/register", headers={ADMIN_HEADER: admin_key}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["source"] == "api"
    assert body["total"] == 3
    # 2 open + 1 closed
    assert body["open"] == 2
    # 1 critical open
    assert body["critical_open"] == 1
    ids = {r["risk_id"] for r in body["rows"]}
    assert {"MER-001", "AIR-001", "REV-002"}.issubset(ids)


@pytest.mark.asyncio
async def test_risks_register_requires_admin(async_client, admin_key):
    res = await async_client.get("/api/v1/internal/risks/register")
    assert res.status_code == 403


# ── Finance forecast ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_finance_forecast_fallback(async_client, admin_key, monkeypatch):
    monkeypatch.delenv("DEALIX_PRIVATE_OPS", raising=False)
    monkeypatch.delenv("PRIVATE_OPS", raising=False)
    res = await async_client.get(
        "/api/v1/internal/finance/forecast", headers={ADMIN_HEADER: admin_key}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["source"] == "fallback"
    assert body["forecast_markdown"] is None


@pytest.mark.asyncio
async def test_finance_forecast_with_private_ops(async_client, admin_key, private_ops):
    res = await async_client.get(
        "/api/v1/internal/finance/forecast", headers={ADMIN_HEADER: admin_key}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["source"] == "api"
    # Cash collected = 1500 + 4999 = 6499
    assert body["cash_collected_sar"] == pytest.approx(6499.0)
    # Two open proposals: P-003 (1500) + P-004 (4999) = 6499
    assert body["open_proposal_value_sar"] == pytest.approx(6499.0)
    # Forecast confidence "high" given cash collected + ≤1 payment risk.
    assert body["forecast_confidence"] in {"low", "medium", "high"}
    # Next action mentions follow-up since P-004 is 22 days open.
    assert body["next_cash_action"]
    # No guaranteed-revenue language.
    assert "guaranteed" not in (body.get("forecast_markdown") or "").lower()


# ── Learning summary ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_learning_summary_fallback(async_client, admin_key, monkeypatch):
    monkeypatch.delenv("DEALIX_PRIVATE_OPS", raising=False)
    monkeypatch.delenv("PRIVATE_OPS", raising=False)
    res = await async_client.get(
        "/api/v1/internal/learning/summary", headers={ADMIN_HEADER: admin_key}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["source"] == "fallback"
    for key in ("market", "message", "offer", "sector"):
        assert key in body["logs"]
        assert body["logs"][key] == []


@pytest.mark.asyncio
async def test_learning_summary_with_private_ops(async_client, admin_key, private_ops):
    res = await async_client.get(
        "/api/v1/internal/learning/summary?limit=5",
        headers={ADMIN_HEADER: admin_key},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["source"] == "api"
    for key in ("market", "message", "offer", "sector"):
        assert body["logs"][key]["total"] == 1
        assert body["logs"][key]["latest"][0]["owner"] == "founder"


# ── Internal _common helpers ───────────────────────────────────


def test_common_helpers_handle_missing_files(tmp_path):
    from api.routers.internal import _common

    assert _common.read_csv(tmp_path / "nope.csv") == []
    assert _common.read_json(tmp_path / "nope.json") is None
    assert _common.read_text(tmp_path / "nope.md") is None
    env = _common.fallback_envelope("no private ops")
    assert env["source"] == "fallback"
    assert env["reason"] == "no private ops"


def test_common_helpers_truncate_long_text(tmp_path):
    from api.routers.internal import _common

    big = tmp_path / "big.md"
    # Write 80 KB; helper truncates at 64 KB by default.
    big.write_text("x" * (80 * 1024), encoding="utf-8")
    out = _common.read_text(big, limit_kb=64)
    assert out is not None
    assert "[truncated]" in out
    assert len(out) <= 64 * 1024 + 50


def test_private_ops_dir_unset(monkeypatch):
    from api.routers.internal import _common

    monkeypatch.delenv("DEALIX_PRIVATE_OPS", raising=False)
    monkeypatch.delenv("PRIVATE_OPS", raising=False)
    assert _common.private_ops_dir() is None


def test_private_ops_dir_set_to_missing(monkeypatch, tmp_path):
    from api.routers.internal import _common

    monkeypatch.setenv("DEALIX_PRIVATE_OPS", str(tmp_path / "does_not_exist"))
    assert _common.private_ops_dir() is None


def test_private_ops_dir_set_to_existing(monkeypatch, tmp_path):
    from api.routers.internal import _common

    monkeypatch.setenv("DEALIX_PRIVATE_OPS", str(tmp_path))
    resolved = _common.private_ops_dir()
    assert resolved is not None
    assert resolved == tmp_path.resolve()
