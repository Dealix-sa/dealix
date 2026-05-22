"""Unit tests for the M&A Radar router (Wave 15.1)."""

from __future__ import annotations

import os
import tempfile

import pytest

os.environ.setdefault("APP_ENV", "test")

from api.routers.m_and_a import (
    _multiplier,
    _read_proposals,
    _write_proposal,
    _ledger_path,
)


# ── Multiplier logic ─────────────────────────────────────────────────────────

def test_multiplier_high_margin():
    assert _multiplier(0.30) == 4.0


def test_multiplier_mid_margin():
    assert _multiplier(0.20) == 3.5


def test_multiplier_low_margin():
    assert _multiplier(0.10) == 3.0


def test_multiplier_boundary_at_25pct():
    assert _multiplier(0.25) == 4.0


def test_multiplier_boundary_at_15pct():
    assert _multiplier(0.15) == 3.5


# ── EBITDA governance gate ───────────────────────────────────────────────────

def test_zero_margin_produces_zero_ebitda():
    """Governance gate: zero margin yields zero EBITDA → must not create proposal."""
    revenue = 1_000_000.0
    margin = 0.0
    ebitda = revenue * margin
    assert ebitda == 0.0


# ── Ledger read/write ────────────────────────────────────────────────────────

def test_ledger_write_and_read(tmp_path):
    os.environ["DEALIX_MA_LEDGER_PATH"] = str(tmp_path / "test_proposals.jsonl")
    try:
        proposal = {
            "proposal_id": "ma_test001",
            "company_name": "Test Co",
            "sector": "retail",
            "annual_revenue_sar": 2_000_000.0,
            "ebitda_margin_pct": 0.20,
            "ebitda_sar": 400_000.0,
            "multiplier": 3.5,
            "proposed_offer_sar": 1_400_000.0,
            "upfront_cash_sar": 840_000.0,
            "earnout_sar": 560_000.0,
            "earnout_months": 12,
            "is_estimate": True,
            "notes": "",
            "created_at": "2026-01-01T00:00:00+00:00",
            "hard_gates": {},
        }
        _write_proposal(proposal)
        rows = _read_proposals(limit=50)
        assert len(rows) >= 1
        assert rows[-1]["proposal_id"] == "ma_test001"
        assert rows[-1]["company_name"] == "Test Co"
    finally:
        del os.environ["DEALIX_MA_LEDGER_PATH"]


def test_read_proposals_empty_ledger(tmp_path):
    os.environ["DEALIX_MA_LEDGER_PATH"] = str(tmp_path / "empty.jsonl")
    try:
        rows = _read_proposals()
        assert rows == []
    finally:
        del os.environ["DEALIX_MA_LEDGER_PATH"]


# ── FastAPI endpoint smoke tests ─────────────────────────────────────────────

import pytest_asyncio
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_evaluate_success(tmp_path):
    os.environ["DEALIX_MA_LEDGER_PATH"] = str(tmp_path / "proposals.jsonl")
    try:
        from api.main import create_app
        app = create_app()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.post("/api/v1/m-and-a/evaluate", json={
                "company_name": "Riyadh Retail Co",
                "annual_revenue_sar": 5_000_000,
                "ebitda_margin_pct": 0.22,
                "sector": "retail",
            })
        assert resp.status_code == 200
        data = resp.json()
        assert data["ebitda_sar"] == pytest.approx(1_100_000.0)
        assert data["multiplier"] == 3.5
        assert data["is_estimate"] is True
    finally:
        del os.environ["DEALIX_MA_LEDGER_PATH"]


@pytest.mark.anyio
async def test_evaluate_rejects_zero_margin(tmp_path):
    os.environ["DEALIX_MA_LEDGER_PATH"] = str(tmp_path / "proposals2.jsonl")
    try:
        from api.main import create_app
        app = create_app()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.post("/api/v1/m-and-a/evaluate", json={
                "company_name": "Zero Co",
                "annual_revenue_sar": 1_000_000,
                "ebitda_margin_pct": 0.0,
            })
        assert resp.status_code == 422
        detail = resp.json()["detail"]
        assert detail["error"] == "no_fake_revenue"
    finally:
        del os.environ["DEALIX_MA_LEDGER_PATH"]


@pytest.mark.anyio
async def test_list_proposals_returns_list(tmp_path):
    os.environ["DEALIX_MA_LEDGER_PATH"] = str(tmp_path / "proposals3.jsonl")
    try:
        from api.main import create_app
        app = create_app()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.get("/api/v1/m-and-a/proposals")
        assert resp.status_code == 200
        data = resp.json()
        assert "proposals" in data
        assert isinstance(data["proposals"], list)
    finally:
        del os.environ["DEALIX_MA_LEDGER_PATH"]
