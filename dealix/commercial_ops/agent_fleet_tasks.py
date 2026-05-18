"""Unified agent fleet tasks — queue YAML + work packets."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.founder_agent_tasks import build_queue_status, seed_today_queue
from dealix.commercial_ops.paths import REPO_ROOT

AGENT_WORK_PACKETS_YAML = REPO_ROOT / "data" / "agent_work_packets" / "daily_packets.yaml"


def _load_packets() -> dict[str, Any]:
    if not AGENT_WORK_PACKETS_YAML.is_file():
        return {"packets": {}}
    try:
        return yaml.safe_load(AGENT_WORK_PACKETS_YAML.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {"packets": {}}


def _load_queue_config() -> dict[str, Any]:
    from dealix.commercial_ops.paths import FOUNDER_AGENT_TASK_QUEUE_YAML

    if not FOUNDER_AGENT_TASK_QUEUE_YAML.is_file():
        return {}
    return yaml.safe_load(FOUNDER_AGENT_TASK_QUEUE_YAML.read_text(encoding="utf-8")) or {}


def load_unified_daily_tasks() -> list[dict[str, Any]]:
    """Merge founder_agent_task_queue daily_templates + daily_packets (P0 first)."""
    cfg = _load_queue_config()
    unified: list[dict[str, Any]] = []
    for tpl in cfg.get("daily_templates") or []:
        unified.append(
            {
                "source": "founder_agent_task_queue",
                "id": tpl.get("id"),
                "agent": tpl.get("agent"),
                "priority": tpl.get("priority", "P2"),
                "title_ar": tpl.get("title_ar"),
                "commands": tpl.get("commands") or [],
                "approval_required": bool(tpl.get("approval_required")),
            }
        )
    packets = _load_packets().get("packets") or {}
    for pid, spec in packets.items():
        if (spec.get("cadence") or "daily") != "daily":
            continue
        unified.append(
            {
                "source": "daily_packets",
                "id": pid,
                "agent": spec.get("agent"),
                "priority": "P1",
                "title_ar": pid,
                "outputs": spec.get("outputs") or [],
                "verify_commands": spec.get("verify_commands") or [],
            }
        )
    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    unified.sort(key=lambda t: order.get(str(t.get("priority")), 9))
    return unified


def build_agent_fleet_today_pack() -> dict[str, Any]:
    queue = seed_today_queue()
    status = build_queue_status()
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "queue_status": status,
        "queue_tasks": queue.get("tasks") or [],
        "unified_templates": load_unified_daily_tasks(),
        "packets_file": str(AGENT_WORK_PACKETS_YAML.relative_to(REPO_ROOT)).replace("\\", "/"),
        "queue_file": str(
            (REPO_ROOT / "data/founder_agent/queue_today.json").relative_to(REPO_ROOT)
        ).replace("\\", "/"),
    }


def check_weekly_decision_yaml() -> dict[str, Any]:
    from dealix.commercial_ops.paths import FOUNDER_WEEKLY_ONE_DECISION_YAML

    if not FOUNDER_WEEKLY_ONE_DECISION_YAML.is_file():
        return {"filled": False, "issues": ["missing founder_weekly_one_decision.yaml"]}
    data = yaml.safe_load(FOUNDER_WEEKLY_ONE_DECISION_YAML.read_text(encoding="utf-8")) or {}
    issues: list[str] = []
    if not (data.get("one_decision_ar") or "").strip():
        issues.append("one_decision_ar empty")
    for field in ("icp_focus_ar", "weakest_soaen_link_ar", "evidence_before_scale_ar"):
        if not (data.get(field) or "").strip():
            issues.append(f"{field} empty")
    return {"filled": len(issues) == 0, "issues": issues, "active_phase": data.get("active_phase")}
