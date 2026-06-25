#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "reports" / "commercial" / "sales_agent_company_brain" / "latest.json"
OUT = ROOT / "apps" / "web" / "lib" / "commercial-command-snapshot.ts"

FALLBACK = {
    "mode": "draft_only",
    "owner_review_required": True,
    "targets_loaded": 0,
    "packs_generated": 0,
    "priority_queue": [],
    "packs": [],
}


def load_payload() -> dict:
    if not SOURCE.exists():
        return FALLBACK
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def main() -> int:
    data = load_payload()
    queue = data.get("priority_queue", [])[:12]
    packs = data.get("packs", [])[:12]
    payload = {
        "mode": data.get("mode", "draft_only"),
        "ownerReviewRequired": bool(data.get("owner_review_required", True)),
        "targetsLoaded": int(data.get("targets_loaded", 0)),
        "packsGenerated": int(data.get("packs_generated", 0)),
        "priorityQueue": queue,
        "packs": packs,
        "commands": [
            "python scripts/commercial/run_sales_agent_company_brain_day.py",
            "python scripts/commercial/prepare_review_actions.py",
            "python scripts/saas/run_commercial_launch_day.py",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "export const commercialCommandSnapshot = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + " as const;\n",
        encoding="utf-8",
    )
    print(f"COMMAND_ROOM_SNAPSHOT={OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
