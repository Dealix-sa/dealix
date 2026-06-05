#!/usr/bin/env python3
"""Aggregate verifier: startup operating system readiness across V10 layers.

Updated for V10 — runs all V10 OS checks and emits an aggregate verdict plus
JSON. Read/score/report only; never sends anything externally.

Run: python scripts/startup_os_verify.py [--strict]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from v10_common import write_json
from v10_specs import verify_all

LABEL = "STARTUP_OS"
JSON_OUT = "outputs/v10_verification/startup_os_verify.json"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--strict", action="store_true")
    p.parse_args(argv)

    results = verify_all()
    per_os = {}
    all_pass = True
    for key, result, _ in results:
        per_os[key] = result.verdict
        all_pass = all_pass and result.passed

    payload = {
        "name": LABEL,
        "verdict": "PASS" if all_pass else "FAIL",
        "checked_os_count": len(results),
        "per_os": per_os,
        "safety": {
            "no_external_send": True,
            "no_secrets": True,
            "no_scraping": True,
            "no_live_ads": True,
            "founder_approval_required": True,
        },
    }
    write_json(JSON_OUT, payload)

    print(f"=== {LABEL} VERDICT ===")
    print(f"{LABEL}={payload['verdict']}")
    print(f"CHECKED_OS={payload['checked_os_count']}")
    for k, v in per_os.items():
        print(f"  {k}={v}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
