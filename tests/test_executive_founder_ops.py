"""Executive founder ops — agents, GTM, production snapshot."""

from __future__ import annotations

from dealix.commercial_ops.executive_production_snapshot import (
    build_executive_production_snapshot,
)
from dealix.commercial_ops.founder_agent_tasks import seed_today_queue
from dealix.commercial_ops.gtm_proof_loop import build_gtm_proof_loop_snapshot
from dealix.commercial_ops.railway_production import analyze_railway_production


def test_railway_repo_pass() -> None:
    blob = analyze_railway_production(api_base=False)
    assert blob["repo"]["ok"], blob["repo"]["issues"]


def test_agent_queue_seed() -> None:
    payload = seed_today_queue(force=True)
    assert len(payload["tasks"]) >= 3


def test_gtm_proof_snapshot() -> None:
    snap = build_gtm_proof_loop_snapshot()
    assert snap["schema_version"] == "1.0"
    assert "blockers_ar" in snap


def test_executive_snapshot_offline() -> None:
    snap = build_executive_production_snapshot(api_base=False)
    assert snap["verdict"] in ("PASS", "PARTIAL", "WARN", "FAIL")
