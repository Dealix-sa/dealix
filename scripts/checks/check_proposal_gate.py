"""
check_proposal_gate.py — verify proposal queue and factory doc, scan for required fields.

Run from repo root:
    python scripts/checks/check_proposal_gate.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

PROPOSAL_QUEUE_PATH = REPO_ROOT / "reports/proposals/MINI_PROPOSAL_QUEUE.md"
PROPOSAL_FACTORY_PATH = REPO_ROOT / "docs/proposals/MINI_PROPOSAL_FACTORY_AR.md"

# Fields that each proposal entry must contain (at least one from each tuple)
REQUIRED_FIELD_SETS: list[tuple[str, ...]] = [
    ("price", "السعر"),
    ("deliverables",),
    ("required_inputs",),
    ("approval_required",),
]


def _check_proposal_fields(content: str) -> int:
    """Check that a document contains at least one term from each required field set."""
    failures = 0
    for field_set in REQUIRED_FIELD_SETS:
        found = any(f.lower() in content.lower() for f in field_set)
        label = " / ".join(f"'{f}'" for f in field_set)
        if found:
            print(f"  PASS  PROPOSAL_QUEUE: required field {label} present")
        else:
            print(f"  FAIL  PROPOSAL_QUEUE: required field {label} missing")
            failures += 1
    return failures


def run_checks() -> int:
    """Run all proposal gate checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: proposal gate")
    print("=" * 60)

    failures = 0
    total = 0

    # Proposal factory doc
    total += 1
    if PROPOSAL_FACTORY_PATH.exists():
        print(f"  PASS  PROPOSAL_FACTORY: file found")
    else:
        print(
            f"  FAIL  PROPOSAL_FACTORY: file not found at "
            f"{PROPOSAL_FACTORY_PATH.relative_to(REPO_ROOT)}"
        )
        failures += 1

    # Proposal queue
    total += 1
    if not PROPOSAL_QUEUE_PATH.exists():
        print(
            f"  FAIL  PROPOSAL_QUEUE: file not found at "
            f"{PROPOSAL_QUEUE_PATH.relative_to(REPO_ROOT)}"
        )
        failures += 1
    else:
        print(f"  PASS  PROPOSAL_QUEUE: file found")
        content = PROPOSAL_QUEUE_PATH.read_text(encoding="utf-8", errors="replace")
        total += len(REQUIRED_FIELD_SETS)
        failures += _check_proposal_fields(content)

    passed = total - failures
    print("-" * 60)
    print(f"Summary: {passed}/{total} passed, {failures} failed")
    return failures


def main() -> None:
    failures = run_checks()
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
