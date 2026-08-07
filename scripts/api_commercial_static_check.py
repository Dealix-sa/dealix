#!/usr/bin/env python3
"""
Dealix API Commercial Static Check (no running server).

Statically inspects the api/ tree to assert the commercial-launch surface
introduces NO external-send capability:
  - any NEW commercial endpoint (file/router referencing 'commercial' + draft/outreach)
    must not contain external-send patterns (mail transport, platform posting, bulk send).
  - reports a summary of commercial-tagged endpoints found.

This check is scoped to the commercial-launch surface so it does not regress on
unrelated pre-existing API code. Exit 0 if pass, 1 otherwise.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
API = REPO / "api"
OUT = REPO / "outputs" / "final_launch_control" / "api_commercial_static_check.json"

# External-send patterns that are forbidden in any commercial outreach endpoint.
SEND_PATTERNS = [
    r"\bsmtplib\b",
    r"sendmail",
    r"send_email",
    r"send_message_to",
    r"bulk_send",
    r"outbound_send",
    r"\.send_raw_email\b",
]


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if not API.exists():
        result = {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "api_present": False,
            "pass": True,
            "note": "api/ not present — skipped.",
        }
        OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("[api-static] api/ absent — skipped (PASS)")
        return 0

    commercial_files = []
    violations = []
    for f in API.rglob("*.py"):
        txt = f.read_text(encoding="utf-8", errors="ignore")
        low = txt.lower()
        is_commercial = "commercial" in low and (
            "draft" in low or "outreach" in low or "launch" in low
        )
        if not is_commercial:
            continue
        commercial_files.append(str(f.relative_to(REPO)))
        for pat in SEND_PATTERNS:
            if re.search(pat, low):
                violations.append({"file": str(f.relative_to(REPO)), "pattern": pat})

    passed = len(violations) == 0
    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "api_present": True,
        "commercial_files_scanned": commercial_files,
        "send_pattern_violations": violations,
        "pass": passed,
        "note": "No commercial send endpoints found." if not commercial_files
                else "Commercial files scanned for send patterns.",
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[api-static] {'PASS' if passed else 'FAIL'} — commercial files: {len(commercial_files)}")
    for v in violations:
        print(f"  - violation: {v}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
