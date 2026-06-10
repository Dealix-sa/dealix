#!/usr/bin/env python3
"""Emit a social metrics template (schema only, no real numbers)."""

from __future__ import annotations

import json

TEMPLATE = {
    "_note": "Manual-entry template. No real numbers assumed.",
    "per_platform": {
        p: {"posts": 0, "impressions": 0, "engagements": 0, "profile_visits": 0, "inbound_dms": 0}
        for p in ("linkedin", "x", "instagram", "tiktok_shorts", "youtube_shorts")
    },
    "funnel": {"audit_requests_from_social": 0, "diagnostics_booked_from_social": 0},
}


def main() -> int:
    print(json.dumps(TEMPLATE, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
