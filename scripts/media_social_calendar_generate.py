#!/usr/bin/env python3
"""Generate a 30-day bilingual social content CALENDAR as artifacts.

Plan only. Nothing is published to any platform — there is no platform API,
token, or auto-post path here. Output: outputs/commercial_launch/<date>/media_social/
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

import commercial_launch_lib as lib

PLATFORMS = ["linkedin", "x", "instagram", "tiktok", "youtube_shorts"]


def build_calendar(config: dict | None = None) -> list[dict]:
    cfg = config or lib.load_config("media_social_calendar.json")
    pillars = cfg["content_pillars"]
    verticals = cfg["verticals"]
    days = cfg.get("days", 30)
    start = _dt.date.today()
    calendar = []
    for d in range(days):
        pillar = pillars[d % len(pillars)]
        vertical = verticals[d % len(verticals)]
        platform = PLATFORMS[d % len(PLATFORMS)]
        hook_ar = f"كيف يعالج {pillar} ألمًا حقيقيًا في {vertical}؟"
        hook_en = f"How {pillar} fixes a real bottleneck in {vertical}"
        calendar.append(
            {
                "day": d + 1,
                "date": (start + _dt.timedelta(days=d)).isoformat(),
                "platform": platform,
                "pillar": pillar,
                "target_vertical": vertical,
                "hook_ar": hook_ar,
                "hook_en": hook_en,
                "post_ar": f"{hook_ar}\n\nالذكاء الاصطناعي يجهّز ويرتّب، والمؤسس يعتمد. لا أتمتة عمياء.\n\nشارك تحدّيك في التعليقات.",
                "post_en": f"{hook_en}.\n\nAI drafts and ranks; the founder approves. No blind automation.\n\nWhat's your bottleneck? Comment below.",
                "cta": "Book an AI Workflow Audit",
                "asset_idea": f"Before/after diagram for {vertical}",
                "metric_to_track": cfg.get("metrics_to_track", ["engagement_rate"])[d % len(cfg.get("metrics_to_track", ["engagement_rate"]))],
                "auto_publish": False,
            }
        )
    return calendar


def main(argv: list[str] | None = None) -> int:
    cfg = lib.load_config("media_social_calendar.json")
    calendar = build_calendar(cfg)
    out = lib.output_dir() / "media_social"
    out.mkdir(parents=True, exist_ok=True)

    (out / "content_calendar.json").write_text(
        json.dumps({"days": len(calendar), "auto_publish": False, "calendar": calendar}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = ["# 30-Day Content Calendar (Plan Only — No Auto-Publish)", ""]
    for item in calendar:
        lines += [
            f"## Day {item['day']} — {item['date']} — {item['platform']}",
            f"- Pillar: {item['pillar']}",
            f"- Vertical: {item['target_vertical']}",
            f"- Hook (EN): {item['hook_en']}",
            f"- Hook (AR): {item['hook_ar']}",
            f"- CTA: {item['cta']}",
            f"- Asset: {item['asset_idea']}",
            f"- Metric: {item['metric_to_track']}",
            "",
        ]
    (out / "content_calendar.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"✅ Generated {len(calendar)}-day content calendar at {out} (auto_publish=false)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
