"""Verify the (optional) v2 internal dashboard contract.

This is a soft check: dashboards live offline and are not required for the
public audit to pass. The script PASSES with a notice when the dashboard
directory is absent, and FAILS only if the directory exists but is invalid.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = REPO_ROOT / "internal_dashboard"

REQUIRED_FILES = (
    "README.md",
    "schema.json",
)


def main() -> None:
    print("== Dashboard v2 ==")
    if not DASHBOARD_DIR.exists():
        print(f"NOTICE: internal_dashboard/ not present — skipping (optional).")
        print("PASS: dashboard v2 optional check.")
        return

    failures: list[str] = []
    for name in REQUIRED_FILES:
        path = DASHBOARD_DIR / name
        if not path.exists():
            failures.append(f"Missing: {path.relative_to(REPO_ROOT)}")

    schema = DASHBOARD_DIR / "schema.json"
    if schema.exists():
        try:
            json.loads(schema.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"schema.json invalid JSON: {exc}")

    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print("PASS: dashboard v2 contract met.")


if __name__ == "__main__":
    main()
