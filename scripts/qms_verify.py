#!/usr/bin/env python3
"""Verify the Quality Management System OS (V9). Static, read-only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/qms-os/00_QUALITY_MANAGEMENT_SYSTEM.md",
    "docs/qms-os/01_QUALITY_POLICY.md",
    "docs/qms-os/02_DOCUMENT_CONTROL.md",
    "docs/qms-os/03_DELIVERY_QA.md",
    "docs/qms-os/04_SALES_QA.md",
    "docs/qms-os/05_MESSAGE_QA.md",
    "docs/qms-os/06_SECURITY_QA.md",
    "docs/qms-os/07_CONTINUOUS_IMPROVEMENT.md",
    "docs/qms-os/99_QMS_REPORT.md",
]

REQUIRED_CONFIGS = [
    ("config/qms_checklists.json", ("version", "checklists")),
]

REQUIRED_CHECKLISTS = {"delivery", "sales", "message", "security"}


def _checklist_integrity() -> list[str]:
    path = v9_lib.REPO / "config" / "qms_checklists.json"
    if not path.is_file():
        return ["config/qms_checklists.json missing"]
    data = json.loads(path.read_text(encoding="utf-8"))
    checklists = data.get("checklists", {})
    problems = []
    for name in REQUIRED_CHECKLISTS:
        items = checklists.get(name)
        if not items:
            problems.append(f"missing checklist: {name}")
        elif len(items) < 2:
            problems.append(f"checklist {name} too short")
    return problems


def verify() -> dict:
    report = v9_lib.run_system_check("qms", REQUIRED_FILES, REQUIRED_CONFIGS)
    problems = _checklist_integrity()
    report["checklist_integrity"] = problems
    if problems and report["verdict"] == "PASS":
        report["verdict"] = "FAIL"
        report["summary"]["violations"].append({"path": "config/qms_checklists.json", "violations": problems})
        (v9_lib.OUTPUT_DIR / "qms.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
