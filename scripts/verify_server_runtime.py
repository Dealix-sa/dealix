#!/usr/bin/env python3
"""C2 — Verify server workers actually produce current operating reports.

Checks freshness (mtime within 48h, tightened to 24h via env var
`DEALIX_FRESHNESS_HOURS`) of the four operating reports, and scans worker
logs for tracebacks. Skipped under CI.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

FAILURES: list[str] = []
WARNINGS: list[str] = []

REQUIRED_REPORTS = (
    "runtime/sales_cockpit.md",
    "runtime/approval_center.md",
    "runtime/distribution_command_center.md",
    "runtime/strategic_stoplight.md",
)


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL: {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  warn: {msg}")


def freshness_hours() -> float:
    raw = os.environ.get("DEALIX_FRESHNESS_HOURS", "48")
    try:
        return float(raw)
    except ValueError:
        return 48.0


def main() -> int:
    ensure_stdout_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", required=True, type=Path)
    args = parser.parse_args()

    print("# C2 — Server Runtime")

    if os.environ.get("CI") == "true":
        warn("CI mode: skipping server runtime checks")
        ok_status = not FAILURES
        print(f"VERIFY_SERVER_RUNTIME_READY={'true' if ok_status else 'false'}")
        return 0 if ok_status else 1

    private_ops = args.private_ops
    if not private_ops.exists():
        fail(f"private ops dir does not exist: {private_ops}")
        print("VERIFY_SERVER_RUNTIME_READY=false")
        return 1

    limit_seconds = freshness_hours() * 3600
    now = time.time()
    for rel in REQUIRED_REPORTS:
        path = private_ops / rel
        if not path.exists():
            fail(f"missing report: {rel}")
            continue
        age = now - path.stat().st_mtime
        if age <= limit_seconds:
            ok(f"{rel} fresh ({age/3600:.1f}h)")
        else:
            fail(f"{rel} stale ({age/3600:.1f}h > {freshness_hours():.0f}h)")

    logs_dir = private_ops / "logs"
    if logs_dir.is_dir():
        tracebacks = 0
        scanned = 0
        for log_path in logs_dir.glob("*.log"):
            scanned += 1
            try:
                text = log_path.read_text(encoding="utf-8", errors="ignore")
            except OSError as e:
                warn(f"cannot read log {log_path.name}: {e}")
                continue
            if "Traceback" in text:
                tracebacks += 1
                fail(f"traceback in {log_path.name}")
        if tracebacks == 0:
            ok(f"worker logs clean ({scanned} files)")
    else:
        warn(f"no logs directory at {logs_dir}")

    ok_status = not FAILURES
    print(f"\nWARNINGS={len(WARNINGS)} FAILURES={len(FAILURES)}")
    print(f"VERIFY_SERVER_RUNTIME_READY={'true' if ok_status else 'false'}")
    return 0 if ok_status else 1


if __name__ == "__main__":
    raise SystemExit(main())
