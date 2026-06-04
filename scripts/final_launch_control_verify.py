#!/usr/bin/env python3
"""Final Launch Control verifier (V7-aware) — safety + go/no-go gate.

Runs the revenue execution and master command verifiers in-process, confirms
the automation-boundaries and crisis docs are present, and asserts the GO/NO-GO
safety posture. Writes outputs/launch_control/final_launch_control_verification.json.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse

import master_startup_command_verify as mscv
import revenue_execution_verify as rev
from _v7_revenue_common import DOCS, REPO, SAFETY_BANNER, write_json

SAFETY_DOCS = [
    "automation-boundaries-os/01_ALLOWED_AUTOMATIONS.md",
    "automation-boundaries-os/02_FORBIDDEN_AUTOMATIONS.md",
    "automation-boundaries-os/03_HUMAN_APPROVAL_GATES.md",
    "crisis-os/01_KILL_SWITCH_POLICY.md",
]

# These are the GO items the launch is allowed to ship.
GO_ITEMS = [
    "Daily founder command center",
    "400+ review-only drafts",
    "Founder action queue",
    "Manual outreach planning",
    "Diagnostic pack generation",
    "Proposal draft generation",
    "Revenue dashboard",
    "CEO daily brief",
    "Weekly board report",
    "Proof asset preparation",
    "Scale readiness tracking",
]

# These are NO-GO — they must never be implemented.
NO_GO_ITEMS = [
    "automated sending",
    "WhatsApp cold outreach",
    "LinkedIn automation",
    "bulk email",
    "paid ads live launch",
    "fake traction",
    "external sending from Actions",
]


def verify() -> dict:
    rev_result = rev.verify()
    master_result = mscv.verify()
    missing_safety = [d for d in SAFETY_DOCS if not (DOCS / d).exists()]

    checks = {
        "revenue_execution_pass": rev_result["status"] == "PASS",
        "master_command_pass": master_result["status"] == "PASS",
        "safety_docs_present": not missing_safety,
        "no_forbidden_send_patterns": rev_result["checks"]["no_forbidden_send_patterns"],
    }
    ok = all(checks.values())
    result = {
        "system": "final-launch-control",
        "status": "PASS" if ok else "FAIL",
        "checks": checks,
        "missing_safety_docs": missing_safety,
        "go_items": GO_ITEMS,
        "no_go_items": NO_GO_ITEMS,
        "safety": SAFETY_BANNER,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    write_json(
        REPO / "outputs" / "launch_control" / "final_launch_control_verification.json",
        result,
    )
    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[final_launch_control_verify] {result['status']}")
    for key, val in result["checks"].items():
        print(f"  - {key}: {'OK' if val else 'FAIL'}")
    print(f"[final_launch_control_verify] {SAFETY_BANNER}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
