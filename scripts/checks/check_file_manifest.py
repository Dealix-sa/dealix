"""
check_file_manifest.py — verify existence of critical files across the repo.

Run from repo root:
    python scripts/checks/check_file_manifest.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

MANIFEST: list[str] = [
    # Constitution
    "docs/00_constitution/NON_NEGOTIABLES.md",
    "docs/00_constitution/DEALIX_CONSTITUTION.md",
    # Success architecture
    "docs/success/DEALIX_SUCCESS_ARCHITECTURE_AR.md",
    # Agent governance
    "docs/agents/AGENT_REGISTRY_AR.md",
    "docs/agents/AGENT_PERMISSION_MATRIX_AR.md",
    "docs/agents/WORKFLOW_FIRST_AGENT_POLICY_AR.md",
    # Execution
    "docs/execution/DEALIX_EXECUTION_CONTRACT_AR.md",
    # Data OS
    "docs/04_data_os/DATA_OS.md",
    "docs/04_data_os/SOURCE_PASSPORT.md",
    "docs/04_data_os/ALLOWED_USE_POLICY.md",
    "docs/04_data_os/PII_CLASSIFICATION.md",
    # Security / Privacy
    "docs/security/PROMPT_INJECTION_DEFENSE_MAX_AR.md",
    "docs/security/UNTRUSTED_INPUT_SANDBOXING_AR.md",
    "docs/privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md",
    "docs/privacy/CLIENT_DATA_HANDLING_AR.md",
    # Delivery
    "docs/delivery/AUTOMATED_DELIVERY_PIPELINE_AR.md",
    "docs/delivery/CLIENT_DELIVERY_ACCEPTANCE_SYSTEM_AR.md",
    "docs/delivery/DELIVERY_SIGN_OFF_TEMPLATE_AR.md",
    # Proposals
    "docs/proposals/MINI_PROPOSAL_FACTORY_AR.md",
    # Outreach
    "docs/outreach/SYSTEM_BASED_OUTREACH_PLAYBOOK_AR.md",
    # Reports — founder
    "reports/founder/DAILY_SUPER_COMMAND.md",
    "reports/founder/DEALIX_EXECUTION_CONTROL_BOARD.md",
    # Reports — delivery
    "reports/delivery/DELIVERY_PIPELINE_STATUS.md",
    "reports/delivery/DELIVERY_BLOCKERS.md",
    "reports/delivery/CLIENT_SIGN_OFF_QUEUE.md",
    "reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md",
    # Reports — scale
    "reports/scale/ULTIMATE_SCALE_SCORECARD.md",
    "reports/scale/WEEKLY_SCALE_REVIEW.md",
    "reports/scale/DELIVERY_CAPACITY_REVIEW.md",
    # Reports — launch
    "reports/launch/LAUNCH_SCORECARD.md",
]


def run_checks() -> int:
    """Run all manifest checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: file manifest")
    print("=" * 60)

    failures = 0
    for rel in MANIFEST:
        path = REPO_ROOT / rel
        if path.exists():
            print(f"  PASS  {rel}")
        else:
            print(f"  FAIL  {rel}  (not found)")
            failures += 1

    total = len(MANIFEST)
    passed = total - failures
    print("-" * 60)
    print(f"Summary: {passed}/{total} passed, {failures} failed")
    return failures


def main() -> None:
    failures = run_checks()
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
