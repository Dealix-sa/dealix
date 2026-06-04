#!/usr/bin/env python3
"""Emit a manual social-metrics tracking template (no platform reads)."""

from __future__ import annotations

import json

import commercial_launch_lib as lib


def build_template() -> dict:
    cfg = lib.load_config("media_social_calendar.json")
    return {
        "note": "Manual tracking template. No platform API reads or writes.",
        "platforms": cfg["platforms"],
        "metrics": cfg.get("metrics_to_track", []),
        "rows_example": [
            {"date": "YYYY-MM-DD", "platform": "linkedin", "impressions": 0, "engagement_rate": 0.0, "qualified_dms": 0}
        ],
    }


def main(argv: list[str] | None = None) -> int:
    print(json.dumps(build_template(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
