#!/usr/bin/env python3
"""Generate a 30-day media/social content calendar (manual posting only).

Produces outputs/media_social/<date>/content_calendar.json and .md from
config/media_social_calendar.json. Every item is a DRAFT for the founder to
post manually — there is no auto-post, no platform API, no scheduling
automation, and no secrets.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import (
    MEDIA_OUTPUTS,
    load_config,
    today_str,
    write_json,
    write_text,
)


def generate(start: str) -> dict[str, Any]:
    cfg = load_config("media_social_calendar.json")
    pillars = cfg["content_pillars"]
    platforms = cfg["platforms"]
    verticals = cfg["verticals"]
    ctas = cfg["ctas"]
    days = cfg.get("days", 30)

    start_date = date.fromisoformat(start)
    items: list[dict[str, Any]] = []
    for i in range(days):
        d = start_date + timedelta(days=i)
        pillar = pillars[i % len(pillars)]
        platform = platforms[i % len(platforms)]
        vertical = verticals[i % len(verticals)]
        cta = ctas[i % len(ctas)]
        items.append(
            {
                "day": i + 1,
                "date": d.isoformat(),
                "pillar": pillar["id"],
                "platform": platform,
                "vertical": vertical,
                "hook_en": f"How {vertical.replace('_', ' ')} teams in KSA/GCC can use AI with full human approval — Dealix view.",
                "hook_ar": f"كيف يمكن لفرق {vertical.replace('_', ' ')} في السعودية والخليج استخدام الذكاء الاصطناعي مع اعتماد بشري كامل — رؤية ديليكس.",
                "format": "post" if platform in ("linkedin", "x") else "short_video",
                "cta_en": cta["en"],
                "cta_ar": cta["ar"],
                "status": "draft_for_manual_posting",
                "auto_post": False,
            }
        )
    return {"start": start, "days": days, "auto_post": False, "items": items}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the 30-day content calendar.")
    parser.add_argument("--date", default=today_str())
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    calendar = generate(args.date)
    out_dir = Path(args.out) if args.out else MEDIA_OUTPUTS / args.date
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "content_calendar.json", calendar)

    md = [
        f"# 30-Day Content Calendar — start {args.date}",
        "",
        "> Manual posting only. No auto-post, no platform APIs, no secrets.",
        "",
        "| Day | Date | Platform | Pillar | Vertical | Format | CTA (EN) |",
        "|-----|------|----------|--------|----------|--------|----------|",
    ]
    for it in calendar["items"]:
        md.append(
            f"| {it['day']} | {it['date']} | {it['platform']} | {it['pillar']} | "
            f"{it['vertical']} | {it['format']} | {it['cta_en']} |"
        )
    write_text(out_dir / "content_calendar.md", "\n".join(md) + "\n")

    assert calendar["auto_post"] is False
    print(f"MEDIA CALENDAR: generated {calendar['days']} days -> {out_dir} (auto_post=false)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
