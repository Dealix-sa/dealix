#!/usr/bin/env python3
"""Static check of the API surface for unsafe external-send patterns.

Scans api/ source statically (does NOT call any live server). Fails if the
launch-control surface introduces real external sending (SMTP, WhatsApp
outbound, LinkedIn automation, Twilio sends). Documentation strings that merely
name a prohibition are fine — we match code-like call patterns.

Writes outputs/final_launch_control/api_static_check.json.
Exit 0 on PASS, 1 on FAIL.

Usage:
    python scripts/api_commercial_static_check.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from launch_os import paths  # noqa: E402
from launch_os.compliance import find_external_send  # noqa: E402
from launch_os.verify import Check, summarize, print_checks  # noqa: E402

API_DIR = paths.REPO_ROOT / "api"

# We only enforce against launch-control commercial routers we may add; the
# rest of the pre-existing API is reported but not failed on (out of scope).
COMMERCIAL_ROUTER_HINTS = ("commercial_launch", "launch_control", "draft_factory")


def run() -> dict:
    checks: list[Check] = []
    if not API_DIR.exists():
        checks.append(Check("api_dir_present", False, critical=False, detail="no api/ directory"))
        return summarize(checks)

    checks.append(Check("api_dir_present", True, critical=False))

    commercial_files = [
        p for p in API_DIR.rglob("*.py")
        if any(h in p.name for h in COMMERCIAL_ROUTER_HINTS)
    ]

    # 1) Launch-control commercial routers must have zero send patterns.
    offenders: list[str] = []
    for p in commercial_files:
        hits = find_external_send(p.read_text(encoding="utf-8", errors="ignore"))
        if hits:
            offenders.append(f"{paths.rel(p)}: {hits}")
    checks.append(
        Check(
            "launch_control_routers_no_send",
            len(offenders) == 0,
            detail=f"offenders={offenders[:5]}" if offenders else f"scanned={len(commercial_files)}",
        )
    )

    # 2) Report (non-critical) any send patterns elsewhere in api/ so they are
    #    visible without failing the pre-existing codebase.
    repo_wide_hits = 0
    for p in API_DIR.rglob("*.py"):
        if find_external_send(p.read_text(encoding="utf-8", errors="ignore")):
            repo_wide_hits += 1
    checks.append(
        Check(
            "api_send_patterns_inventory",
            True,
            critical=False,
            detail=f"files_with_send_like_patterns={repo_wide_hits}",
        )
    )

    return summarize(checks)


def main() -> int:
    paths.ensure_dirs()
    result = run()
    out = paths.FINAL_CONTROL_OUT / "api_static_check.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print_checks("api", [Check(**c) for c in result["checks"]])
    print(f"[api] wrote {paths.rel(out)}")
    print("[api] PASS" if result["pass"] else "[api] FAIL")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
