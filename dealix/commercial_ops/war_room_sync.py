"""Sync data/war_room_today.json from Motion A targeting seed."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from typing import Any

from dealix.commercial_ops.paths import AGENCY_TARGETS_CSV, REPO_ROOT, WAR_ROOM_TODAY_JSON


def sync_war_room_today(*, top_n: int = 10) -> dict[str, Any]:
    n = max(1, min(top_n, 30))
    items: list[dict[str, str]] = []
    if AGENCY_TARGETS_CSV.is_file():
        with AGENCY_TARGETS_CSV.open(encoding="utf-8", newline="") as f:
            for i, row in enumerate(csv.DictReader(f)):
                if i >= n:
                    break
                items.append(
                    {
                        "company": (row.get("company") or row.get("name") or "").strip(),
                        "priority": (row.get("priority") or "P1").strip(),
                        "city": (row.get("city") or "").strip(),
                        "status": "pending",
                    }
                )
    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "motion": "A",
        "targets": {"items": items, "count": len(items)},
        "source": str(AGENCY_TARGETS_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
    }
    WAR_ROOM_TODAY_JSON.parent.mkdir(parents=True, exist_ok=True)
    WAR_ROOM_TODAY_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "ok": True,
        "targets": len(items),
        "path": str(WAR_ROOM_TODAY_JSON.relative_to(REPO_ROOT)).replace("\\", "/"),
    }
