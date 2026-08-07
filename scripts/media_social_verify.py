#!/usr/bin/env python3
"""
Dealix Media/Social Final Verification.

Verifies the media/social OS is planning-only and safe:
  - required docs exist (OS overview, ready report, ads gate)
  - config/media_social_calendar.json exists with auto_post=false
  - 30-day calendar exists (generates it if missing)
  - no auto-post / platform-posting code in scripts/media_social_*.py

Writes outputs/media_social/final_media_social_verification.json.
Exit 0 if pass, 1 otherwise.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "outputs" / "media_social" / "final_media_social_verification.json"

REQUIRED_DOCS = [
    REPO / "docs" / "media-social-os" / "00_MEDIA_SOCIAL_OS.md",
    REPO / "docs" / "media-social-os" / "99_MEDIA_SOCIAL_READY_REPORT.md",
    REPO / "docs" / "media-social-os" / "15_ADS_READINESS_GATE.md",
]
CONFIG = REPO / "config" / "media_social_calendar.json"
CALENDAR = REPO / "outputs" / "media_social" / "calendar_30_day.json"
# Platform auto-posting indicators that must NOT appear in media/social scripts.
AUTO_POST_TERMS = ["auto_post(", "post_to_platform", "publish_to_", "tweepy", "graph_api_post"]


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    docs_ok = {str(p.relative_to(REPO)): p.exists() for p in REQUIRED_DOCS}
    config_ok = CONFIG.exists()
    auto_post_disabled = False
    if config_ok:
        cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
        auto_post_disabled = cfg.get("auto_post") is False

    if not CALENDAR.exists():
        subprocess.run([sys.executable, str(REPO / "scripts" / "media_social_calendar_generate.py")], check=False)
    calendar_ok = CALENDAR.exists()

    # Scan media/social content scripts for auto-post code (exclude this verifier,
    # which legitimately names the patterns it detects).
    code_violations = []
    for f in (REPO / "scripts").glob("media_social_*.py"):
        if f.name == Path(__file__).name:
            continue
        low = f.read_text(encoding="utf-8", errors="ignore").lower()
        for term in AUTO_POST_TERMS:
            if term in low:
                code_violations.append({"file": f.name, "term": term})

    passed = (
        all(docs_ok.values())
        and config_ok
        and auto_post_disabled
        and calendar_ok
        and len(code_violations) == 0
    )
    result = {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "docs": docs_ok,
        "config_present": config_ok,
        "auto_post_disabled": auto_post_disabled,
        "calendar_present": calendar_ok,
        "auto_post_code_violations": code_violations,
        "pass": passed,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[media-social-verify] {'PASS' if passed else 'FAIL'}")
    print(f"  docs_ok={all(docs_ok.values())} config={config_ok} auto_post_disabled={auto_post_disabled} calendar={calendar_ok}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
