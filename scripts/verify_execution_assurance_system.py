"""Verify the Dealix Execution Assurance System files exist and have content."""

from __future__ import annotations

from pathlib import Path


REQUIRED = [
    "docs/ops/EXECUTION_ASSURANCE_SYSTEM.md",
    "ops_runtime/execution_assurance.py",
    "scripts/generate_execution_assurance_report.py",
    "docs/ops/SYSTEM_CLOSURE_RULES.md",
    "docs/founder/DECISION_RIGHTS.md",
    "docs/strategy/SCENARIO_PLANNING.md",
    "docs/ops/QUALITY_BAR_SYSTEM.md",
    "docs/founder/founder_operating_review.md",
    "dealix_cli/__init__.py",
    "dealix_cli/commands.py",
    "dealix_cli/__main__.py",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    failures: list[str] = []
    for rel in REQUIRED:
        path = repo_root / rel
        if not path.exists():
            failures.append(f"Missing: {rel}")
        elif path.stat().st_size < 150:
            failures.append(f"Too short: {rel}")

    if failures:
        print("Execution assurance system verification failed:")
        for failure in failures:
            print("-", failure)
        return 1

    print("PASS: execution assurance system is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
