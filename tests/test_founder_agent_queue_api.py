"""Founder agent queue API — isolated router tests."""

from __future__ import annotations

import os

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-queue")

from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from api.routers.founder_agent_queue import router  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app)
H = {"X-Admin-API-Key": "test-admin-queue"}


def test_agent_queue_seed_and_get() -> None:
    r = client.post("/api/v1/founder/agent-queue/seed-today", headers=H)
    assert r.status_code == 200
    body = r.json()
    assert body.get("seeded") is True
    assert (body.get("stats") or {}).get("total", 0) >= 3

    r2 = client.get("/api/v1/founder/agent-queue", headers=H)
    assert r2.status_code == 200
    tasks = r2.json().get("tasks") or []
    assert tasks

    tid = tasks[0]["id"]
    r3 = client.patch(
        f"/api/v1/founder/agent-queue/tasks/{tid}",
        headers=H,
        json={"status": "done"},
    )
    assert r3.status_code == 200
    assert r3.json().get("ok") is True


def test_founder_agent_tasks_unit() -> None:
    from dealix.commercial_ops.founder_agent_tasks import build_queue_status, seed_today_queue

    seed_today_queue(force=True)
    st = build_queue_status()
    assert st.get("stats", {}).get("total", 0) >= 3
