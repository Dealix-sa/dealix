#!/usr/bin/env python3
"""C5 — Aggregate commercial counts to verify the business is actually moving.

Reads CSVs under `$PRIVATE_OPS/{intelligence,outreach,sales,finance}` and
checks that the scale thresholds are met: 100 leads, 25 approved
outreach, 10 sent, 1 proposal, 1 payment-capture row. Skipped under CI.
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

THRESHOLDS = {
    "leads": 100,
    "approved_outreach": 25,
    "sent": 10,
    "proposals": 1,
    "payments": 1,
}


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

    print("# C5 — Business Evidence")

    if os.environ.get("CI") == "true":
        warn("CI mode: skipping business evidence checks")
        ok_status = not FAILURES
        print(f"VERIFY_BUSINESS_EVIDENCE_READY={'true' if ok_status else 'false'}")
        return 0 if ok_status else 1

    private_ops = args.private_ops
    if not private_ops.exists():
        fail(f"private ops dir does not exist: {private_ops}")
        print("VERIFY_BUSINESS_EVIDENCE_READY=false")
        return 1

    leads = _read_csv(private_ops / "intelligence/lead_intelligence_base.csv")
    outreach = _read_csv(private_ops / "outreach/outreach_queue.csv")
    proposals = _read_csv(private_ops / "sales/proposal_queue.csv")
    payments = _read_csv(private_ops / "finance/payment_capture_queue.csv")

    approved = [
        r for r in outreach if (r.get("approval_status") or "").strip().lower() == "approved"
    ]
    sent = [r for r in outreach if (r.get("send_status") or "").strip().lower() == "sent"]

    counts = {
        "leads": len(leads),
        "approved_outreach": len(approved),
        "sent": len(sent),
        "proposals": len(proposals),
        "payments": len(payments),
    }

    for key, threshold in THRESHOLDS.items():
        actual = counts[key]
        if actual >= threshold:
            ok(f"{key} >= {threshold} (actual: {actual})")
        else:
            fail(f"{key} below threshold (have: {actual}, need: {threshold})")

    ok_status = not FAILURES
    print(f"\nCOUNTS={counts}")
    print(f"WARNINGS={len(WARNINGS)} FAILURES={len(FAILURES)}")
    print(f"VERIFY_BUSINESS_EVIDENCE_READY={'true' if ok_status else 'false'}")
    return 0 if ok_status else 1


if __name__ == "__main__":
    raise SystemExit(main())
