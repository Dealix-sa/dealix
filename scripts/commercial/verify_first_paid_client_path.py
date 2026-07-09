#!/usr/bin/env python3
"""Verify the first paid client manual revenue path guardrails."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = ROOT / "reports" / "full_company_os_first_paid_verify"

REQUIRED_PATHS = [
    "dealix/full_company_os/revenue_path.py",
    "scripts/commercial/run_first_paid_client_path.py",
    "data/commercial/examples/first_paid_client_event.example.json",
    "docs/commercial/FIRST_PAID_CLIENT_SPRINT_AR.md",
    "docs/commercial/PAYMENT_EVIDENCE_AND_REVENUE_POLICY.md",
]


def fail(message: str) -> int:
    print(f"FIRST_PAID_CLIENT_PATH_VERIFY=FAIL {message}")
    return 1


def main() -> int:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    if missing:
        return fail("missing=" + ",".join(missing))
    cmd = [
        sys.executable,
        "scripts/commercial/run_first_paid_client_path.py",
        "--output-root",
        str(OUTPUT_ROOT.relative_to(ROOT)),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if proc.returncode != 0:
        print(proc.stdout)
        return fail("runner_failed")
    report = OUTPUT_ROOT / "first_paid_client_path.json"
    if not report.exists():
        print(proc.stdout)
        return fail("missing_report")
    payload = json.loads(report.read_text(encoding="utf-8"))
    status = payload["status"]
    policy = payload["policy"]
    if policy.get("live_charge_enabled") is not False:
        return fail("live_charge_enabled")
    if policy.get("auto_send_enabled") is not False:
        return fail("auto_send_enabled")
    if status.get("can_count_revenue") is True and "payment_received" not in [event["event_type"] for event in payload.get("events", [])]:
        return fail("revenue_counted_without_payment_received")
    if status.get("can_mark_closed_won") is True and "proof_pack_delivered" not in [event["event_type"] for event in payload.get("events", [])]:
        return fail("closed_won_without_proof_pack")
    if any("fake" in warning for warning in status.get("warnings", [])):
        return fail("fake_evidence_warning")
    print("FIRST_PAID_CLIENT_PATH_VERIFY=PASS manual_close_only=true revenue_requires_payment_received=true proof_required=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
