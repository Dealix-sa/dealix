#!/usr/bin/env python3
"""C3 — Verify the revenue factory has the right CSVs and minimum schema.

This is a schema-and-presence gate; numeric thresholds for `business
evidence` live in verify_business_evidence.py. Skipped under CI.
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

REQUIRED_CSVS: dict[str, list[str]] = {
    "intelligence/lead_intelligence_base.csv": ["company", "sector", "priority", "source"],
    "outreach/outreach_queue.csv": ["company", "approval_status", "send_status", "message_body"],
    "outreach/conversation_log.csv": ["company", "reply_type", "timestamp"],
    "sales/sample_queue.csv": ["company", "status"],
    "sales/proposal_queue.csv": ["company", "status", "amount"],
    "finance/payment_capture_queue.csv": ["company", "status", "amount"],
}


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL: {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  warn: {msg}")


def check_csv(path: Path, required_cols: list[str]) -> None:
    if not path.exists():
        fail(f"missing CSV: {path.relative_to(path.parents[1])}")
        return
    try:
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            missing = [c for c in required_cols if c not in headers]
            if missing:
                fail(f"{path.name}: missing columns {missing}")
            else:
                ok(f"{path.name}: schema valid")
    except Exception as e:
        fail(f"{path.name}: cannot read ({e})")


def main() -> int:
    ensure_stdout_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", required=True, type=Path)
    args = parser.parse_args()

    print("# C3 — Revenue Runtime")

    if os.environ.get("CI") == "true":
        warn("CI mode: skipping revenue runtime checks")
        ok_status = not FAILURES
        print(f"VERIFY_REVENUE_RUNTIME_READY={'true' if ok_status else 'false'}")
        return 0 if ok_status else 1

    if not args.private_ops.exists():
        fail(f"private ops dir does not exist: {args.private_ops}")
        print("VERIFY_REVENUE_RUNTIME_READY=false")
        return 1

    for rel, cols in REQUIRED_CSVS.items():
        check_csv(args.private_ops / rel, cols)

    ok_status = not FAILURES
    print(f"\nWARNINGS={len(WARNINGS)} FAILURES={len(FAILURES)}")
    print(f"VERIFY_REVENUE_RUNTIME_READY={'true' if ok_status else 'false'}")
    return 0 if ok_status else 1


if __name__ == "__main__":
    raise SystemExit(main())
