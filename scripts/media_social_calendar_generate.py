#!/usr/bin/env python3
"""Generate the 30-day media & social calendar (planning only, manual posting).

No platform API, no auto-post. Writes outputs/media_social/calendar_30_day.json.

Usage:
    python scripts/media_social_calendar_generate.py [--days 30]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from launch_os import paths  # noqa: E402
from launch_os.media_social import generate_calendar, write_calendar  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    args = ap.parse_args(argv)

    paths.ensure_dirs()
    cal = generate_calendar(days=args.days)
    out = write_calendar(cal, paths.MEDIA_OUT)
    print(f"[media] generated {cal['days']}-day calendar ({len(cal['items'])} items)")
    print(f"[media] auto_post_enabled={cal['auto_post_enabled']} publish_method={cal['publish_method']}")
    print(f"[media] wrote {paths.rel(out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
