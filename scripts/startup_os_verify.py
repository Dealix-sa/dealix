#!/usr/bin/env python3
"""Startup OS verifier (V7-aware) — checks all OS doc layers are present.

Aggregates the V7 OS layers and confirms each named directory exists and
contains its overview doc. Writes outputs/startup_os/startup_os_verification.json.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse

from _v7_revenue_common import DOCS, REPO, SAFETY_BANNER, write_json

# V7 OS layers (directory -> overview doc) that the startup OS must include.
LAYER_OVERVIEWS = {
    "revenue-execution-os": "00_REVENUE_EXECUTION_OS.md",
    "delivery-conversion-os": "00_DELIVERY_CONVERSION_OS.md",
    "proof-os": "00_PROOF_ASSET_OS.md",
    "market-intelligence-os": "00_MARKET_INTELLIGENCE_OS.md",
    "knowledge-base-os": "00_KNOWLEDGE_BASE_OS.md",
    "operating-memory-os": "00_OPERATING_MEMORY_OS.md",
    "automation-boundaries-os": "00_AUTOMATION_BOUNDARIES_OS.md",
    "scale-readiness-os": "00_SCALE_READINESS_OS.md",
    "crisis-os": "00_CRISIS_OS.md",
    "master-command-center": "00_MASTER_COMMAND_CENTER.md",
}


def verify() -> dict:
    missing: list[str] = []
    present: list[str] = []
    for layer, overview in LAYER_OVERVIEWS.items():
        rel = f"{layer}/{overview}"
        if (DOCS / rel).exists():
            present.append(layer)
        else:
            missing.append(rel)
    ok = not missing
    result = {
        "system": "startup-os",
        "status": "PASS" if ok else "FAIL",
        "layers_present": present,
        "layers_total": len(LAYER_OVERVIEWS),
        "missing_overviews": missing,
        "safety": SAFETY_BANNER,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    write_json(REPO / "outputs" / "startup_os" / "startup_os_verification.json", result)
    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[startup_os_verify] {result['status']} "
          f"({len(result['layers_present'])}/{result['layers_total']} layers)")
    for m in result["missing_overviews"]:
        print(f"    missing: {m}")
    print(f"[startup_os_verify] {SAFETY_BANNER}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
