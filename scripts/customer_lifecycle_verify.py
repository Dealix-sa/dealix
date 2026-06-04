#!/usr/bin/env python3
"""Verify the Customer Lifecycle OS (V9). Static, read-only, artifact-only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/customer-lifecycle-os/00_CUSTOMER_LIFECYCLE_OS.md",
    "docs/customer-lifecycle-os/01_FIRST_TOUCH_TO_DIAGNOSTIC.md",
    "docs/customer-lifecycle-os/02_DIAGNOSTIC_TO_PILOT.md",
    "docs/customer-lifecycle-os/03_PILOT_TO_RETAINER.md",
    "docs/customer-lifecycle-os/04_RETAINER_TO_EXPANSION.md",
    "docs/customer-lifecycle-os/05_CUSTOMER_HEALTH_REVIEW.md",
    "docs/customer-lifecycle-os/06_RENEWAL_PLAYBOOK.md",
    "docs/customer-lifecycle-os/07_CHURN_PREVENTION.md",
    "docs/customer-lifecycle-os/08_EXPANSION_PLAYBOOK.md",
    "docs/customer-lifecycle-os/99_CUSTOMER_LIFECYCLE_REPORT.md",
]

REQUIRED_CONFIGS = [
    ("config/customer_lifecycle_stages.json", ("version", "stages")),
]


def _stage_integrity() -> list[str]:
    """Each stage must declare outputs, measure, next_action, and risk_signals."""
    path = v9_lib.REPO / "config" / "customer_lifecycle_stages.json"
    if not path.is_file():
        return ["config/customer_lifecycle_stages.json missing"]
    data = json.loads(path.read_text(encoding="utf-8"))
    problems: list[str] = []
    required = ("id", "outputs", "measure", "next_action", "risk_signals")
    for stage in data.get("stages", []):
        for key in required:
            if not stage.get(key):
                problems.append(f"stage {stage.get('id', '?')} missing {key}")
    return problems


def verify() -> dict:
    report = v9_lib.run_system_check("customer_lifecycle", REQUIRED_FILES, REQUIRED_CONFIGS)
    problems = _stage_integrity()
    report["stage_integrity"] = problems
    if problems and report["verdict"] == "PASS":
        report["verdict"] = "FAIL"
        report["summary"]["violations"].append({"path": "config/customer_lifecycle_stages.json", "violations": problems})
        (v9_lib.OUTPUT_DIR / "customer_lifecycle.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
