"""30-day media & social calendar generation — planning only, never posts.

Produces a content calendar of *drafts*. There is no platform API, no
auto-post, no scheduling-to-platform. The founder posts manually.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Channels are for *manual* publishing by the founder.
CHANNELS: tuple[str, ...] = ("linkedin", "x", "blog", "newsletter")

PILLARS: tuple[dict[str, str], ...] = (
    {"key": "category", "en": "Category education", "ar": "تثقيف عن الفئة"},
    {"key": "proof", "en": "Proof & case-style insight", "ar": "إثبات ودراسة حالة"},
    {"key": "founder_pov", "en": "Founder point of view", "ar": "رأي المؤسس"},
    {"key": "how_to", "en": "Practical how-to", "ar": "خطوات عملية"},
    {"key": "offer", "en": "Offer & invitation", "ar": "عرض ودعوة"},
)


def generate_calendar(days: int = 30, start: datetime | None = None) -> dict:
    """Build a 30-day calendar of manual-post drafts."""
    start = start or datetime.now(timezone.utc)
    items = []
    for i in range(days):
        day = start + timedelta(days=i)
        pillar = PILLARS[i % len(PILLARS)]
        channel = CHANNELS[i % len(CHANNELS)]
        items.append(
            {
                "day": i + 1,
                "date": day.strftime("%Y-%m-%d"),
                "channel": channel,
                "pillar": pillar["key"],
                "title_en": f"Day {i+1}: {pillar['en']} for Saudi B2B",
                "title_ar": f"اليوم {i+1}: {pillar['ar']} لشركات B2B السعودية",
                "status": "draft",
                # Hard guards mirroring the draft factory:
                "auto_post": False,
                "requires_founder_approval": True,
                "publish_method": "manual_only",
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "days": days,
        "channels": list(CHANNELS),
        "pillars": [p["key"] for p in PILLARS],
        "auto_post_enabled": False,
        "publish_method": "manual_only",
        "items": items,
    }


def write_calendar(calendar: dict, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "calendar_30_day.json"
    path.write_text(json.dumps(calendar, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
