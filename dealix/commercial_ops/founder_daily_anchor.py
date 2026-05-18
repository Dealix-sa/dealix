"""Daily anchor — War Room + agent queue + brief index."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from dealix.commercial_ops.founder_agent_tasks import build_queue_status, seed_today_queue
from dealix.commercial_ops.paths import (
    FOUNDER_BRIEFS_DIR,
    FOUNDER_DAILY_ANCHOR_JSON,
    REPO_ROOT,
    WAR_ROOM_TODAY_JSON,
)
from dealix.commercial_ops.war_room_sync import sync_war_room_today


def run_daily_anchor(*, top_n: int = 10, seed_agents: bool = True) -> dict[str, Any]:
    war = sync_war_room_today(top_n=top_n)
    if seed_agents:
        seed_today_queue()
    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
        "generated_at": datetime.now(UTC).isoformat(),
        "verdict": "PASS" if war.get("ok") else "DEGRADED",
        "war_room": war,
        "agent_queue": build_queue_status(),
        "morning_command": "py -3 scripts/run_dealix_unified_founder_day.py",
        "ui_routes": {
            "founder": "/ar/ops/founder",
            "war_room": "/ar/ops/war-room",
            "approvals": "/ar/ops/approvals",
        },
    }
    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    FOUNDER_DAILY_ANCHOR_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _ = WAR_ROOM_TODAY_JSON  # referenced for tooling
    return payload
