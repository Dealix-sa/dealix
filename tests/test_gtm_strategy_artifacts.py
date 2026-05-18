"""GTM strategy YAML + north-star smoke tests."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

from dealix.commercial_ops.paths import REPO_ROOT

ROOT = REPO_ROOT


def _load(rel: str) -> dict:
    path = ROOT / rel
    assert path.is_file(), rel
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def test_commercial_sku_ladder() -> None:
    rungs = _load("dealix/config/commercial_sku_ladder.yaml").get("rungs") or []
    assert len(rungs) >= 5


def test_icp_hybrid_three() -> None:
    assert len(_load("dealix/config/icp_hybrid_gtm.yaml").get("icps") or []) == 3


def test_90_day_plan() -> None:
    assert _load("data/commercial/90_day_activation_plan.yaml").get("targets_day_90")


def test_founder_agent_tasks_seed() -> None:
    from dealix.commercial_ops.founder_agent_tasks import seed_today_queue, templates_as_packets

    packets = templates_as_packets()
    assert "pm_morning" in packets
    payload = seed_today_queue(force=True)
    assert len(payload.get("tasks") or []) >= 5


def test_north_star_status() -> None:
    path = ROOT / "scripts" / "founder_north_star_status.py"
    spec = importlib.util.spec_from_file_location("founder_north_star_status", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    blob = mod.build_status(api_base=False, skip_live=True)
    assert blob["verdict"] in ("PASS", "WARN", "FAIL")
    assert blob["commercial"].get("agent_queue_pending_p0", 0) >= 0
