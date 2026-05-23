#!/usr/bin/env python3
"""C4 — Verify no outreach was sent without approval, and suppression honored.

Walks `$PRIVATE_OPS/outreach/outreach_queue.csv` and ensures no row has
`send_status=sent` with `approval_status!=approved`. If
`$PRIVATE_OPS/security/suppression.csv` exists, ensures no sent row
matches a suppressed company. Skipped under CI.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

FAILURES: list[str] = []
WARNINGS: list[str] = []


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL: {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  warn: {msg}")


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    ensure_stdout_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", required=True, type=Path)
    args = parser.parse_args()

    print("# C4 — Trust & Security Runtime")

    if os.environ.get("CI") == "true":
        warn("CI mode: skipping trust runtime checks")
        ok_status = not FAILURES
        print(f"VERIFY_TRUST_SECURITY_RUNTIME_READY={'true' if ok_status else 'false'}")
        return 0 if ok_status else 1

    queue_path = args.private_ops / "outreach/outreach_queue.csv"
    if not queue_path.exists():
        warn(f"no outreach queue yet at {queue_path}")
    else:
        rows = _read_csv(queue_path)
        unauthorized = [
            r
            for r in rows
            if (r.get("send_status") or "").strip().lower() == "sent"
            and (r.get("approval_status") or "").strip().lower() != "approved"
        ]
        if unauthorized:
            for r in unauthorized[:5]:
                fail(f"outreach sent without approval: {r.get('company')}")
            if len(unauthorized) > 5:
                fail(f"...and {len(unauthorized) - 5} more")
        else:
            ok(f"outreach queue clean ({len(rows)} rows)")

    suppression_path = args.private_ops / "security/suppression.csv"
    if suppression_path.exists():
        suppressed = {(r.get("company") or "").strip().lower() for r in _read_csv(suppression_path)}
        queue_rows = _read_csv(queue_path) if queue_path.exists() else []
        violations = [
            r
            for r in queue_rows
            if (r.get("company") or "").strip().lower() in suppressed
            and (r.get("send_status") or "").strip().lower() == "sent"
        ]
        if violations:
            for r in violations[:5]:
                fail(f"suppressed company contacted: {r.get('company')}")
        else:
            ok(f"suppression honored ({len(suppressed)} suppressed companies)")
    else:
        warn(f"no suppression list at {suppression_path}")

    ok_status = not FAILURES
    print(f"\nWARNINGS={len(WARNINGS)} FAILURES={len(FAILURES)}")
    print(f"VERIFY_TRUST_SECURITY_RUNTIME_READY={'true' if ok_status else 'false'}")
    return 0 if ok_status else 1


if __name__ == "__main__":
    raise SystemExit(main())
