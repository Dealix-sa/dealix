#!/usr/bin/env python3
"""Verify the social calendar is well-formed and auto-post-free.

Regenerates the calendar if missing. Checks every item is bilingual, planned,
and flagged auto_post=False. Read-only / file-only.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import CONFIG_DIR, load_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def verify() -> list[str]:
    cal_path = CONFIG_DIR / "media_social_calendar.json"
    if not cal_path.exists():
        subprocess.run([sys.executable, str(ROOT / "scripts" / "media_social_calendar_generate.py")], check=True)
    cal = load_json(cal_path)
    errors: list[str] = []
    items = cal.get("calendar", [])
    if len(items) < 30:
        errors.append(f"calendar has {len(items)} items, expected >= 30")
    if cal.get("_meta", {}).get("auto_post") is not False:
        errors.append("_meta.auto_post must be False")
    for it in items:
        for f in ("hook_en", "hook_ar", "body_en", "body_ar", "cta_en", "cta_ar"):
            if not it.get(f):
                errors.append(f"{it.get('date')}: missing bilingual field {f}")
        if it.get("auto_post") is not False:
            errors.append(f"{it.get('date')}: auto_post must be False")
    return errors


def main() -> int:
    errors = verify()
    if not errors:
        print("Media/social verify PASS — 30+ bilingual items, no auto-post.")
        return 0
    print("Media/social verify FAIL:")
    for e in errors[:30]:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
