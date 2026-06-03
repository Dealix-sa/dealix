"""
check_agent_governance.py — verify agent registry, permission matrix, and activity reports.

Run from repo root:
    python scripts/checks/check_agent_governance.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

REQUIRED_FILES: list[tuple[str, str]] = [
    (
        "docs/agents/AGENT_REGISTRY_AR.md",
        "AGENT_REGISTRY",
    ),
    (
        "docs/agents/AGENT_PERMISSION_MATRIX_AR.md",
        "AGENT_PERMISSION_MATRIX",
    ),
    (
        "docs/agents/WORKFLOW_FIRST_AGENT_POLICY_AR.md",
        "WORKFLOW_FIRST_AGENT_POLICY",
    ),
    (
        "reports/agents/AGENT_DAILY_ACTIVITY_REVIEW.md",
        "AGENT_DAILY_ACTIVITY_REVIEW",
    ),
    (
        "reports/agents/AGENT_PERMISSION_AUDIT.md",
        "AGENT_PERMISSION_AUDIT",
    ),
]

PERMISSION_MATRIX_PATH = REPO_ROOT / "docs/agents/AGENT_PERMISSION_MATRIX_AR.md"
PERMISSION_MATRIX_REQUIRED_SECTIONS = ["Observe", "Advise", "Act"]


def _check_permission_matrix_sections() -> tuple[int, int]:
    """
    Check that AGENT_PERMISSION_MATRIX_AR.md contains Observe/Advise/Act sections.
    Returns (failures, total_checks).
    """
    if not PERMISSION_MATRIX_PATH.exists():
        return 0, 0  # existence already counted above

    content = PERMISSION_MATRIX_PATH.read_text(encoding="utf-8", errors="replace")
    failures = 0
    total = 0
    for section in PERMISSION_MATRIX_REQUIRED_SECTIONS:
        total += 1
        if section.lower() in content.lower():
            print(f"  PASS  AGENT_PERMISSION_MATRIX: section '{section}' found")
        else:
            print(f"  FAIL  AGENT_PERMISSION_MATRIX: section '{section}' not found")
            failures += 1
    return failures, total


def run_checks() -> int:
    """Run all agent governance checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: agent governance")
    print("=" * 60)

    failures = 0
    total = 0

    for rel, label in REQUIRED_FILES:
        path = REPO_ROOT / rel
        total += 1
        if path.exists():
            print(f"  PASS  {label}: file found")
        else:
            print(f"  FAIL  {label}: file not found at {rel}")
            failures += 1

    matrix_failures, matrix_total = _check_permission_matrix_sections()
    failures += matrix_failures
    total += matrix_total

    passed = total - failures
    print("-" * 60)
    print(f"Summary: {passed}/{total} passed, {failures} failed")
    return failures


def main() -> None:
    failures = run_checks()
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
