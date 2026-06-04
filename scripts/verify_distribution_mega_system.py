"""Verify the Distribution Mega-System files are present and non-trivial."""

from pathlib import Path

REQUIRED = [
    "docs/distribution/DISTRIBUTION_PORTFOLIO_OS.md",
    "docs/distribution/LEAD_INTELLIGENCE_BASE_OS.md",
    "docs/distribution/SECTOR_EXPANSION_MACHINES.md",
    "docs/distribution/INBOUND_ENGINE_OS.md",
    "docs/distribution/LANDING_PAGE_CONVERSION_SYSTEM.md",
    "docs/distribution/REFERRAL_ENGINE_OS.md",
    "docs/distribution/STRATEGIC_ACCOUNT_PLAYBOOK.md",
    "docs/distribution/CONVERSATION_ROUTING_SYSTEM.md",
    "docs/distribution/NURTURE_MACHINE_OS.md",
    "docs/distribution/PROPOSAL_ACCELERATION_SYSTEM.md",
    "docs/distribution/PAYMENT_CAPTURE_SYSTEM.md",
    "docs/founder/FOUNDER_5_MINUTE_APPROVAL_WORKFLOW.md",
    "scripts/generate_distribution_command_center.py",
    "scripts/run_distribution_daily.py",
]


def main():
    failures = []
    for file in REQUIRED:
        p = Path(file)
        if not p.exists():
            failures.append(f"Missing: {file}")
        elif p.stat().st_size < 50:
            failures.append(f"Too short: {file}")

    if failures:
        print("Distribution mega system verification failed:")
        for failure in failures:
            print("-", failure)
        raise SystemExit(1)

    print("PASS: Distribution Mega-System is ready.")


if __name__ == "__main__":
    main()
