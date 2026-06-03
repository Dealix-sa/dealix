"""
check_security_privacy_gates.py — verify security and privacy doc presence.

Run from repo root:
    python scripts/checks/check_security_privacy_gates.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

REQUIRED_FILES: list[tuple[str, str]] = [
    (
        "docs/security/PROMPT_INJECTION_DEFENSE_MAX_AR.md",
        "PROMPT_INJECTION_DEFENSE",
    ),
    (
        "docs/security/UNTRUSTED_INPUT_SANDBOXING_AR.md",
        "UNTRUSTED_INPUT_SANDBOXING",
    ),
    (
        "docs/privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md",
        "DO_NOT_CONTACT_AND_SUPPRESSION_POLICY",
    ),
    (
        "docs/privacy/CLIENT_DATA_HANDLING_AR.md",
        "CLIENT_DATA_HANDLING",
    ),
    (
        "docs/04_data_os/PII_CLASSIFICATION.md",
        "PII_CLASSIFICATION",
    ),
]


def run_checks() -> int:
    """Run all security and privacy gate checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: security and privacy gates")
    print("=" * 60)

    failures = 0
    for rel, label in REQUIRED_FILES:
        path = REPO_ROOT / rel
        if path.exists():
            print(f"  PASS  {label}: file found")
        else:
            print(f"  FAIL  {label}: file not found at {rel}")
            failures += 1

    total = len(REQUIRED_FILES)
    passed = total - failures
    print("-" * 60)
    print(f"Summary: {passed}/{total} passed, {failures} failed")
    return failures


def main() -> None:
    failures = run_checks()
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
