#!/usr/bin/env python3
"""Generate the Dealix content calendar from the weekly cadence pattern."""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.growth._common import (  # noqa: E402
    DATA_DIR,
    REPURPOSE_ASSETS,
    assert_single_cta,
    ensure_dirs,
    write_json,
)

_OUT = DATA_DIR / "content_calendar.json"

# Weekday index (Mon=0 .. Sun=6) -> cadence definition.
_PATTERN: dict[int, dict[str, str]] = {
    6: {  # Sunday
        "day_type": "pain",
        "content_type": "pain_post",
        "hook_ar": "أين تتسرب القيمة في عملك هذا الأسبوع؟",
        "cta": "Free Diagnostic",
        "source": "free_tool_signals",
    },
    0: {  # Monday
        "day_type": "framework",
        "content_type": "framework_post",
        "hook_ar": "إطار اليوم: الفرق بين إنجاز المهمة وإثبات القيمة.",
        "cta": "Business OS Score",
        "source": "operating_doctrine",
    },
    1: {  # Tuesday
        "day_type": "build_log",
        "content_type": "build_log_post",
        "hook_ar": "سجل البناء: ماذا شحنّا في نظام التشغيل هذا الأسبوع.",
        "cta": "Command Sprint",
        "source": "product_changelog",
    },
    2: {  # Wednesday
        "day_type": "sector",
        "content_type": "sector_post",
        "hook_ar": "ألم تشغيلي متكرر في هذا القطاع وكيف يُعالَج.",
        "cta": "Free Diagnostic",
        "source": "sector_pages",
    },
    3: {  # Thursday
        "day_type": "cta",
        "content_type": "cta_post",
        "hook_ar": "خطوة واحدة واضحة هذا الأسبوع.",
        "cta": "Command Sprint",
        "source": "offer_ladder",
    },
    4: {  # Friday
        "day_type": "founder_lesson",
        "content_type": "founder_lesson_post",
        "hook_ar": "درس المؤسس: ما تعلّمناه من التشغيل لا من الوعود.",
        "cta": "Business OS Score",
        "source": "founder_notes",
    },
    5: {  # Saturday
        "day_type": "review",
        "content_type": "review_post",
        "hook_ar": "مراجعة الأسبوع: إشارة، قرار، إجراء تالٍ.",
        "cta": "Free Diagnostic",
        "source": "weekly_brief",
    },
}


def _repurpose_for(day_type: str) -> list[str]:
    """Return a deterministic repurpose target list for a day type."""
    # Every source can fan out to the full 12 assets; keep the order stable.
    return list(REPURPOSE_ASSETS)


def build_calendar(start: date, weeks: int) -> list[dict[str, Any]]:
    """Return a calendar of weeks*7 entries starting at the given date."""
    if weeks < 1:
        raise ValueError("weeks must be >= 1")
    entries: list[dict[str, Any]] = []
    total_days = weeks * 7
    for offset in range(total_days):
        current = start + timedelta(days=offset)
        spec = _PATTERN[current.weekday()]
        assert_single_cta(spec["cta"])
        entries.append(
            {
                "date": current.isoformat(),
                "day_type": spec["day_type"],
                "content_type": spec["content_type"],
                "hook_ar": spec["hook_ar"],
                "single_cta": spec["cta"],
                "source": spec["source"],
                "repurpose_targets": _repurpose_for(spec["day_type"]),
            },
        )
    return sorted(entries, key=lambda e: e["date"])


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    """Parse command-line arguments for weeks and start date."""
    parser = argparse.ArgumentParser(description="Generate the content calendar.")
    parser.add_argument("--weeks", type=int, default=5, help="number of weeks (>=1)")
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help="start date YYYY-MM-DD (defaults to upcoming Sunday)",
    )
    return parser.parse_args(argv)


def _default_start(today: date) -> date:
    """Return the upcoming Sunday on or after today."""
    days_ahead = (6 - today.weekday()) % 7
    return today + timedelta(days=days_ahead)


def main(argv: list[str] | None = None) -> int:
    """Write the content calendar and print a summary line."""
    args = _parse_args(argv)
    if args.start:
        start = datetime.strptime(args.start, "%Y-%m-%d").date()
    else:
        start = _default_start(date.today())
    ensure_dirs()
    calendar = build_calendar(start, args.weeks)
    payload = {
        "start": start.isoformat(),
        "weeks": args.weeks,
        "entries": calendar,
    }
    size = write_json(_OUT, payload)
    print(
        f"content_calendar: wrote {len(calendar)} entries "
        f"({args.weeks} weeks from {start.isoformat()}) to {_OUT} ({size} bytes)",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
