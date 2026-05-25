"""Verify that the Dealix Revenue Operations Playbook v1 layer is in place.

This is a structural check: every public doc that the playbook depends on
must exist and contain real content (more than placeholder size).

Run via:
    python scripts/verify_revenue_operations_playbook.py
"""
from pathlib import Path

REQUIRED = [
    "docs/revenue/REVENUE_OPERATIONS_PLAYBOOK.md",
    "docs/strategy/ICP_OPERATING_SYSTEM.md",
    "docs/acquisition/LEAD_SOURCING_SYSTEM.md",
    "docs/acquisition/LEAD_QUALIFICATION_SCORE.md",
    "docs/acquisition/OUTBOUND_CADENCE_SYSTEM.md",
    "docs/delivery/SAMPLE_OPERATIONS_SYSTEM.md",
    "docs/revenue/PROPOSAL_CONVERSION_SYSTEM.md",
    "docs/finance/PAYMENT_PATH_SYSTEM.md",
    "docs/delivery/DELIVERY_KICKOFF_SYSTEM.md",
    "docs/learning/WIN_LOSS_SYSTEM.md",
]


def main() -> int:
    failures = []
    for file in REQUIRED:
        path = Path(file)
        if not path.exists():
            failures.append(f"Missing: {file}")
        elif path.stat().st_size < 150:
            failures.append(f"Too short: {file}")
    if failures:
        print("Revenue operations playbook verification failed:")
        for failure in failures:
            print("-", failure)
        return 1
    print("PASS: revenue operations playbook is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
