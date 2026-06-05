#!/usr/bin/env python3
"""Verify the Cost Control & Model Routing OS (V9). Static, read-only.

Also confirms the routing/budget configs contain no API keys or secrets.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/cost-control-os/00_COST_CONTROL_OS.md",
    "docs/cost-control-os/01_MODEL_ROUTING_POLICY.md",
    "docs/cost-control-os/02_TOKEN_BUDGETS.md",
    "docs/cost-control-os/03_TASK_TIERING.md",
    "docs/cost-control-os/04_COST_ALERTS_MANUAL_PROCESS.md",
    "docs/cost-control-os/05_CHEAP_MODEL_FIRST_POLICY.md",
    "docs/cost-control-os/06_EXPENSIVE_MODEL_APPROVAL_RULES.md",
    "docs/cost-control-os/99_COST_CONTROL_REPORT.md",
]

REQUIRED_CONFIGS = [
    ("config/model_routing_policy.json", ("version", "tiers", "rules")),
    ("config/token_budgets.json", ("version", "budgets", "rules")),
]

# Patterns that would indicate a leaked secret/API key in cost configs.
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"api[_-]?key\"?\s*[:=]\s*\"[A-Za-z0-9]{16,}\""),
    re.compile(r"AKIA[0-9A-Z]{16}"),
)


def _scan_secrets() -> list[str]:
    problems: list[str] = []
    for rel, _ in REQUIRED_CONFIGS:
        path = v9_lib.REPO / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                problems.append(f"possible secret in {rel}")
    return problems


def verify() -> dict:
    report = v9_lib.run_system_check("cost_control", REQUIRED_FILES, REQUIRED_CONFIGS)
    secrets = _scan_secrets()
    report["secret_scan"] = secrets
    if secrets and report["verdict"] == "PASS":
        report["verdict"] = "FAIL"
        report["summary"]["violations"].append({"path": "config", "violations": secrets})
        (v9_lib.OUTPUT_DIR / "cost_control.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
