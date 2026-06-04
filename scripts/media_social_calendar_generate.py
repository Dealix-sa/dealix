#!/usr/bin/env python3
"""Generate a 30-day bilingual social content calendar -> config/media_social_calendar.json.

PLANNING ONLY. No platform APIs, no auto-posting, no secrets. The founder posts
manually. Output is a structured plan the founder reviews and publishes by hand.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import CONFIG_DIR, load_offers, now_iso, write_json

PILLARS = [
    {"id": "education", "name_en": "AI education", "name_ar": "تثقيف عن الذكاء الاصطناعي"},
    {"id": "proof", "name_en": "Proof & before/after", "name_ar": "أدلة وقبل/بعد"},
    {"id": "vertical", "name_en": "Vertical playbooks", "name_ar": "أدلة القطاعات"},
    {"id": "founder", "name_en": "Founder POV", "name_ar": "رأي المؤسس"},
    {"id": "trust", "name_en": "Trust & safety", "name_ar": "الثقة والأمان"},
]

PLATFORMS = ["linkedin", "x", "instagram", "tiktok_shorts", "youtube_shorts"]


def generate(start: date, days: int) -> dict:
    offers = load_offers()
    verticals = offers["verticals"]
    items = []
    for i in range(days):
        d = start + timedelta(days=i)
        pillar = PILLARS[i % len(PILLARS)]
        vertical = verticals[i % len(verticals)]
        platform = PLATFORMS[i % len(PLATFORMS)]
        items.append(
            {
                "date": d.isoformat(),
                "pillar": pillar["id"],
                "platform": platform,
                "vertical": vertical["id"],
                "hook_en": f"{vertical['name']}: one workflow you can make AI-assisted this week",
                "hook_ar": f"{vertical['name_ar']}: سير عمل واحد تقدر تخليه مدعوم بالذكاء الاصطناعي هذا الأسبوع",
                "body_en": (
                    f"A practical {pillar['name_en']} post about {vertical['pain_angles'][0]} — "
                    f"human-in-the-loop, no blind automation."
                ),
                "body_ar": (
                    f"منشور عملي ({pillar['name_ar']}) عن {vertical['pain_angles'][0]} — "
                    f"بوجود الإنسان في الحلقة وبدون أتمتة عمياء."
                ),
                "cta_en": "Comment 'AUDIT' to learn about our AI Workflow Audit.",
                "cta_ar": "اكتب (تدقيق) لمعرفة المزيد عن تدقيق سير العمل بالذكاء الاصطناعي.",
                "status": "planned",
                "auto_post": False,
                "requires_founder_approval": True,
            }
        )
    return {
        "_meta": {
            "title": "Dealix 30-Day Social Content Calendar",
            "generated_at": now_iso(),
            "start": start.isoformat(),
            "days": days,
            "auto_post": False,
            "platform_apis": "none",
            "secrets": "none",
            "note": "Planning only. Founder publishes manually after review.",
        },
        "pillars": PILLARS,
        "platforms": PLATFORMS,
        "calendar": items,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--start", default=date.today().isoformat())
    args = ap.parse_args()
    cal = generate(date.fromisoformat(args.start), args.days)
    out = CONFIG_DIR / "media_social_calendar.json"
    write_json(out, cal)
    print(f"Generated {len(cal['calendar'])}-day calendar -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
