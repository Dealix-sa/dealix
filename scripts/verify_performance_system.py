#!/usr/bin/env python3
"""Verify the Performance Improvement OS.

Checks:
- Required performance docs exist.
- The Observe -> Decide loop is documented.
- The KPI tree mentions every canonical KPI line.
- Experiment backlog uses the canonical schema.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PERF_DOCS = [
    "docs/performance/PERFORMANCE_IMPROVEMENT_OS.md",
    "docs/performance/REVENUE_KPI_TREE.md",
    "docs/performance/CONVERSION_DIAGNOSTICS.md",
    "docs/performance/EXPERIMENT_BACKLOG.md",
    "docs/performance/LEARNING_LOOP.md",
]

REQUIRED_LOOP_STEPS = [
    "Observe",
    "Diagnose",
    "Prioritise",
    "Experiment",
    "Measure",
    "Decide",
]

REQUIRED_KPI_LINES = [
    "Sourced leads",
    "ICP-matched",
    "A-priority accounts",
    "Drafts queued",
    "Approval rate",
    "Reply rate",
    "Payment conversion",
    "Delivery success",
    "Retention",
]

REQUIRED_BACKLOG_FIELDS = [
    "experiment_id",
    "hypothesis",
    "owner",
    "time_box_days",
    "success_metric",
    "kill_criterion",
    "rollback_plan",
]


def check_files(failures: list[str]) -> None:
    for rel in REQUIRED_PERF_DOCS:
        if not (ROOT / rel).exists():
            failures.append(f"missing file: {rel}")


def check_loop(failures: list[str]) -> None:
    p = ROOT / "docs/performance/PERFORMANCE_IMPROVEMENT_OS.md"
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    for step in REQUIRED_LOOP_STEPS:
        if step not in text:
            failures.append(
                f"PERFORMANCE_IMPROVEMENT_OS.md: missing loop step '{step}'"
            )


def check_kpi(failures: list[str]) -> None:
    p = ROOT / "docs/performance/REVENUE_KPI_TREE.md"
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    for kpi in REQUIRED_KPI_LINES:
        if kpi not in text:
            failures.append(
                f"REVENUE_KPI_TREE.md: missing KPI line '{kpi}'"
            )


def check_backlog(failures: list[str]) -> None:
    p = ROOT / "docs/performance/EXPERIMENT_BACKLOG.md"
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    for f in REQUIRED_BACKLOG_FIELDS:
        if f not in text:
            failures.append(f"EXPERIMENT_BACKLOG.md: missing field '{f}'")


def main() -> int:
    failures: list[str] = []
    check_files(failures)
    check_loop(failures)
    check_kpi(failures)
    check_backlog(failures)

    print("=" * 60)
    print("Dealix Performance Improvement System Verifier")
    print("=" * 60)
    if not failures:
        print("[PASS] performance system verified")
        return 0
    print(f"[FAIL] {len(failures)} issue(s):")
    for f in failures:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
