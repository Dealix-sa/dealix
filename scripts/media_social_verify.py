#!/usr/bin/env python3
"""Verify the media/social calendar is present, 30 days, and strictly manual (no auto-post)."""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAL = ROOT / "config" / "media_social_calendar.json"
ADS = ROOT / "config" / "ad_campaigns_seed.json"


def main() -> int:
    errors: list[str] = []
    if not CAL.exists():
        print("calendar missing — run media_social_calendar_generate.py", file=sys.stderr)
        return 1
    cal = json.loads(CAL.read_text())
    if len(cal.get("days", [])) < 30:
        errors.append("calendar has fewer than 30 days")
    if any(day.get("auto_post") for day in cal.get("days", [])):
        errors.append("auto_post=true found — forbidden")
    if ADS.exists():
        ads = json.loads(ADS.read_text())
        if ads.get("live_launch") is True:
            errors.append("ad_campaigns_seed.live_launch must be false")
    ok = not errors
    print(json.dumps({"ok": ok, "days": len(cal.get("days", [])), "errors": errors}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
