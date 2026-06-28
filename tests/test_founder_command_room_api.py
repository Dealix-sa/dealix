"""Tests for the Founder Command Room endpoint (GET /api/v1/founder/command-room).

Mounts the router in isolation (no DB / no full-app lifespan) so the test is
fast and self-contained. Guards the admin-key auth contract and the aggregated
snapshot shape, including that launch readiness reflects the live war-room
summary and the response stays draft-only.
"""
from __future__ import annotations

import os

import pytest

os.environ.setdefault("ADMIN_API_KEYS", "testkey")

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.founder_command_room import router

PATH = "/api/v1/founder/command-room"


@pytest.fixture()
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_requires_admin_key(client: TestClient) -> None:
    assert client.get(PATH).status_code == 401
    assert client.get(PATH, headers={"X-Admin-API-Key": "wrong"}).status_code == 403


def test_snapshot_shape_and_launch_readiness(client: TestClient) -> None:
    r = client.get(PATH, headers={"X-Admin-API-Key": "testkey"})
    assert r.status_code == 200
    j = r.json()

    # Top-level aggregated contract.
    assert {"generated_at", "mode", "launch", "offer_ladder", "summary"} <= set(j)
    assert j["mode"] == "draft_only"

    # Offer ladder = 6 rungs; founder actions = 4 pending items.
    assert len(j["offer_ladder"]) == 6
    assert len(j["launch"]["founder_actions"]) == 4
    assert j["launch"]["article13_target"] == 3

    # Launch readiness reflects the live war-room summary.
    summary = j["summary"]
    assert {"today", "revenue", "queues", "risks", "top_targets"} <= set(summary)
    assert j["launch"]["paid"] == summary["revenue"]["paid"]

    # Doctrine flags surface to the UI and stay enforced.
    assert summary["risks"]["no_live_auto_send"] is True
    assert summary["risks"]["no_cold_whatsapp"] is True
