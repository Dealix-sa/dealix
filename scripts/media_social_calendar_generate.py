#!/usr/bin/env python3
"""Generate a 30-day, manual-posting content calendar to config/media_social_calendar.json.

No auto-posting, no platform APIs, no secrets. Output is a plan the founder posts manually.
"""
from __future__ import annotations
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "config" / "media_social_calendar.json"

PILLARS = ["AI trust & safety", "Sector ops insight", "Proof / case method", "Founder POV"]
PLATFORMS = ["LinkedIn", "X", "Instagram", "TikTok", "YouTube Shorts"]
VERTICALS = ["facilities_management", "contracting_project_controls", "real_estate_property_ops",
             "legal_professional_services", "consulting_training_b2b"]


def main() -> int:
    start = dt.date.today()
    days = []
    for i in range(30):
        d = start + dt.timedelta(days=i)
        pillar = PILLARS[i % len(PILLARS)]
        vertical = VERTICALS[i % len(VERTICALS)]
        days.append({
            "date": d.isoformat(),
            "pillar": pillar,
            "platform": PLATFORMS[i % len(PLATFORMS)],
            "vertical": vertical,
            "language": "ar" if i % 2 else "en",
            "draft_hook": f"[{pillar}] Insight for {vertical.replace('_', ' ')} teams (review/edit before posting).",
            "posting": "MANUAL — founder edits and posts personally",
            "auto_post": False,
        })
    payload = {
        "version": "v5",
        "generated": start.isoformat(),
        "pillars": PILLARS,
        "rule": "Manual posting only. No auto-post, no platform API, no secrets, no paid ads.",
        "days": days,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote 30-day manual calendar -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
