#!/usr/bin/env python3
"""Verify the Demo & Sandbox OS (V9). Static, read-only, artifact-only."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/demo-os/00_DEMO_OS.md",
    "docs/demo-os/01_DEMO_NARRATIVE.md",
    "docs/demo-os/02_VERTICAL_DEMO_SCENARIOS.md",
    "docs/demo-os/03_SAFE_SAMPLE_DATA_POLICY.md",
    "docs/demo-os/04_DEMO_SCRIPT_AR_EN.md",
    "docs/demo-os/05_DEMO_TO_DIAGNOSTIC_CONVERSION.md",
    "docs/demo-os/06_DEMO_QA_CHECKLIST.md",
    "docs/demo-os/99_DEMO_OS_REPORT.md",
    "scripts/demo_pack_generate.py",
    "data/demo_companies.example.jsonl",
]

REQUIRED_CONFIGS = [
    ("config/demo_scenarios.json", ("version", "safety", "scenarios")),
]


def verify() -> dict:
    return v9_lib.run_system_check("demo_os", REQUIRED_FILES, REQUIRED_CONFIGS)


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
