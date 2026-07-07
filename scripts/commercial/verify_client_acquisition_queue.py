#!/usr/bin/env python3
"""Verify the Dealix client acquisition queue foundation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "reports" / "client_acquisition" / "verify_queue.json"

REQUIRED_FILES = [
    ROOT / "dealix" / "client_acquisition" / "__init__.py",
    ROOT / "dealix" / "client_acquisition" / "models.py",
    ROOT / "dealix" / "client_acquisition" / "queue.py",
    ROOT / "scripts" / "commercial" / "run_client_acquisition_queue.py",
]

REQUIRED_SAFE_WORDS = [
    "founder_review_required",
    "confirmed_payment_before_revenue_status",
    "proof_required_for_claims",
]


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        print("MISSING_FILES=" + ",".join(missing))
        return 1

    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "commercial" / "run_client_acquisition_queue.py"),
        "--output",
        str(OUTPUT),
    ]
    subprocess.run(cmd, check=True, cwd=ROOT)

    payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
    if payload["mode"] != "draft-only":
        print("MODE_FAIL")
        return 1
    if not payload["items"]:
        print("NO_ITEMS")
        return 1
    if not all(item["approval_required"] for item in payload["items"]):
        print("APPROVAL_FAIL")
        return 1
    missing_words = [word for word in REQUIRED_SAFE_WORDS if word not in payload["safeguards"]]
    if missing_words:
        print("SAFEGUARD_FAIL=" + ",".join(missing_words))
        return 1

    print("CLIENT_ACQUISITION_QUEUE_VERDICT=PASS")
    print(f"QUEUE_ITEMS={len(payload['items'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
