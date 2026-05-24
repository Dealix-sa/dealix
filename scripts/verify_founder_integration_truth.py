#!/usr/bin/env python3
"""Report founder integration truth matrix — no secrets, no invented PASS."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TRUTH_YAML = ROOT / "dealix/transformation/founder_integration_truth.yaml"


def main() -> int:
    if not TRUTH_YAML.is_file():
        print(f"MISSING: {TRUTH_YAML}", file=sys.stderr)
        return 1

    data = yaml.safe_load(TRUTH_YAML.read_text(encoding="utf-8")) or {}
    ladder = data.get("ladder") or []
    integrations = data.get("integrations") or []

    red = []
    yellow = []
    green = []

    for section_name, items in (("ladder", ladder), ("integrations", integrations)):
        for item in items:
            status = (item.get("status") or "unknown").lower()
            label = item.get("label_ar") or item.get("id") or "?"
            row = f"{section_name}:{item.get('id', '?')} [{status}] {label}"
            if status == "red":
                red.append(row)
            elif status == "yellow":
                yellow.append(row)
            elif status == "green":
                green.append(row)

    print("FOUNDER_INTEGRATION_TRUTH_REPORT")
    print(f"  green={len(green)} yellow={len(yellow)} red={len(red)}")
    for row in red[:10]:
        print(f"  RED: {row}")
    for row in yellow[:5]:
        print(f"  YELLOW: {row}")

    # Fail only if critical integrations are red without yellow sandbox path
    critical_red = [
        r for r in red if "postgres" in r.lower() or "ops-autopilot" in r.lower()
    ]
    if critical_red:
        print("FOUNDER_INTEGRATION_TRUTH_VERDICT=FAIL")
        return 1

    print("FOUNDER_INTEGRATION_TRUTH_VERDICT=PASS")
    print("  action: update status in founder_integration_truth.yaml after manual verify")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
