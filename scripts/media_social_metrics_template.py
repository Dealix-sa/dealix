#!/usr/bin/env python3
"""Write a manual-input social metrics template (schema only, no real numbers)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import MEDIA_OUTPUTS, today_str, write_csv, write_json

METRICS = [
    "impressions",
    "reach",
    "engagements",
    "engagement_rate",
    "link_clicks",
    "profile_visits",
    "followers_gained",
    "saves",
    "shares",
    "comments",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Write social metrics template.")
    parser.add_argument("--date", default=today_str())
    args = parser.parse_args()

    out_dir = MEDIA_OUTPUTS / args.date
    out_dir.mkdir(parents=True, exist_ok=True)

    write_json(
        out_dir / "social_metrics_template.json",
        {
            "date": args.date,
            "source": "manual",
            "platforms": ["linkedin", "x", "instagram", "tiktok", "youtube_shorts"],
            "metrics": dict.fromkeys(METRICS),
            "note": "Manual-input only. No platform API; numbers are never assumed.",
        },
    )
    write_csv(
        out_dir / "social_metrics_template.csv",
        ["date", "platform", *METRICS],
        [
            [args.date, p, *["" for _ in METRICS]]
            for p in ["linkedin", "x", "instagram", "tiktok", "youtube_shorts"]
        ],
    )
    print(f"SOCIAL METRICS TEMPLATE: written -> {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
