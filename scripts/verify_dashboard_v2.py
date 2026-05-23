"""Verify the v2 CEO dashboard HTML.

Checks the file exists and contains the expected widget labels:
pipeline, revenue, delivery, learning, trust.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

WIDGETS = ["Pipeline", "Revenue", "Delivery", "Learning", "Trust"]


def main() -> int:
    target = REPO_ROOT / "internal_dashboard" / "ceo_dashboard_v2.html"
    if not target.exists():
        print(f"FAIL {target} missing")
        print("\nverify_dashboard_v2: FAIL (1 check)")
        return 1
    print(f"PASS {target} exists")

    text = target.read_text(encoding="utf-8")
    missing = [w for w in WIDGETS if w not in text]
    if missing:
        print(f"FAIL ceo_dashboard_v2.html missing widgets: {missing}")
        print("\nverify_dashboard_v2: FAIL (1 check)")
        return 1
    print(f"PASS all {len(WIDGETS)} widgets present ({', '.join(WIDGETS)})")

    print("\nverify_dashboard_v2: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
