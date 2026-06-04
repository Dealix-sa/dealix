#!/usr/bin/env python3
"""Verify the media/social OS: docs present, config sane, no auto-post, no secrets.

Checks:
- the media-social docs set exists,
- calendar + ad configs declare auto_post/live_launch disabled,
- no obvious publishing-API/secret usage in the media scripts,
- the ads seed declares plan-only with launch no-go conditions.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import ROOT, load_config

REQUIRED_DOCS = [
    "docs/media-social-os/00_MEDIA_SOCIAL_OS.md",
    "docs/media-social-os/03_30_DAY_CONTENT_CALENDAR.md",
    "docs/media-social-os/10_ADS_OS.md",
    "docs/media-social-os/15_ADS_READINESS_GATE.md",
]

SECRET_OR_PUBLISH = [
    r"api_key\s*=\s*['\"][A-Za-z0-9]",
    r"access_token\s*=\s*['\"][A-Za-z0-9]",
    r"tweepy",
    r"linkedin_api",
    r"facebook_business",
    r"InstagramAPI",
    r"\.create_post\(",
    r"\.publish\(",
]


def verify() -> list[str]:
    errors: list[str] = []
    for doc in REQUIRED_DOCS:
        if not (ROOT / doc).exists():
            errors.append(f"missing doc: {doc}")

    cal = load_config("media_social_calendar.json")
    if cal.get("auto_post") is not False:
        errors.append("media_social_calendar.json: auto_post must be false")

    ads = load_config("ad_campaigns_seed.json")
    if ads.get("live_launch_allowed") is not False:
        errors.append("ad_campaigns_seed.json: live_launch_allowed must be false")
    if not ads.get("launch_no_go_conditions"):
        errors.append("ad_campaigns_seed.json: launch_no_go_conditions missing")

    patterns = [re.compile(p, re.IGNORECASE) for p in SECRET_OR_PUBLISH]
    for script in sorted(ROOT.glob("scripts/media_social_*.py")):
        if script.name == "media_social_verify.py":
            continue  # the verifier names these patterns on purpose
        text = script.read_text(encoding="utf-8", errors="ignore")
        for rx in patterns:
            if rx.search(text):
                # Do not echo the matched pattern/text back into the message.
                errors.append(f"{script.name}: matched a forbidden publish/automation pattern")
                break
    return errors


def main() -> int:
    errors = verify()
    if errors:
        print("MEDIA SOCIAL VERIFY: FAIL", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("MEDIA SOCIAL VERIFY: PASS — docs present, auto_post=false, ads plan-only, no secrets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
