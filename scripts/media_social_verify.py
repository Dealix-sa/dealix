#!/usr/bin/env python3
"""Verify the media & social OS: docs, config, calendar, and no auto-post code.

Writes outputs/media_social/final_media_social_verification.json.
Exit 0 on PASS, 1 on FAIL.

Usage:
    python scripts/media_social_verify.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from launch_os import paths  # noqa: E402
from launch_os.compliance import find_external_send  # noqa: E402
from launch_os.media_social import generate_calendar, write_calendar  # noqa: E402
from launch_os.verify import Check, summarize, print_checks  # noqa: E402

DOCS = paths.REPO_ROOT / "docs" / "media-social-os"
# Implementation surface that must contain no auto-post / platform API calls.
# (This verifier is intentionally excluded — it *names* the forbidden terms as
# detection patterns, which would otherwise self-trip.)
CODE_SURFACE = (paths.REPO_ROOT / "launch_os" / "media_social.py",
                paths.REPO_ROOT / "scripts" / "media_social_calendar_generate.py")
AUTO_POST_TERMS = ("auto_post(", "schedule_post(", "publish_to_linkedin(", "post_to_twitter(",
                   "tweepy", "linkedin_api", "graph.facebook")


def run() -> dict:
    checks: list[Check] = []

    # Required docs.
    for name in ("00_MEDIA_SOCIAL_OS.md", "15_ADS_READINESS_GATE.md", "99_MEDIA_SOCIAL_READY_REPORT.md"):
        p = DOCS / name
        checks.append(Check(f"doc_{name}", p.exists(), detail=paths.rel(p)))

    # Config.
    cfg = paths.MEDIA_CALENDAR_CONFIG
    checks.append(Check("calendar_config_present", cfg.exists(), detail=paths.rel(cfg)))
    if cfg.exists():
        data = json.loads(cfg.read_text(encoding="utf-8"))
        checks.append(Check("config_auto_post_disabled", data.get("auto_post_enabled") is False))
        checks.append(Check("config_manual_only", data.get("publish_method") == "manual_only"))

    # Calendar output (generate if missing).
    paths.ensure_dirs()
    cal_path = paths.MEDIA_OUT / "calendar_30_day.json"
    if not cal_path.exists():
        write_calendar(generate_calendar(), paths.MEDIA_OUT)
    checks.append(Check("calendar_output_present", cal_path.exists(), detail=paths.rel(cal_path)))
    if cal_path.exists():
        cal = json.loads(cal_path.read_text(encoding="utf-8"))
        checks.append(Check("calendar_auto_post_disabled", cal.get("auto_post_enabled") is False))
        checks.append(Check("calendar_has_items", len(cal.get("items", [])) >= 30, critical=False))
        all_manual = all(i.get("publish_method") == "manual_only" for i in cal.get("items", []))
        checks.append(Check("calendar_items_manual_only", all_manual))

    # No auto-post / platform API posting code.
    offenders: list[str] = []
    for p in CODE_SURFACE:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if find_external_send(text):
            offenders.append(f"{paths.rel(p)}: external_send")
        for term in AUTO_POST_TERMS:
            if term in text:
                offenders.append(f"{paths.rel(p)}: {term}")
    checks.append(Check("no_auto_post_code", len(offenders) == 0, detail=f"offenders={offenders[:5]}"))

    return summarize(checks)


def main() -> int:
    result = run()
    out = paths.MEDIA_OUT / "final_media_social_verification.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print_checks("media", [Check(**c) for c in result["checks"]])
    print(f"[media] wrote {paths.rel(out)}")
    print("[media] PASS" if result["pass"] else "[media] FAIL")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
