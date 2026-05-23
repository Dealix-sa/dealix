"""Verify Stage 0 (Trust) safety scaffolding.

Checks:
- docs/trust/ has all 10 required files.
- docs/trust/APPROVAL_MATRIX.md mentions all four approval levels A0, A1, A2, A3.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_TRUST_FILES = [
    "APPROVAL_MATRIX.md",
    "AUTONOMY_POLICY.md",
    "NO_OVERCLAIM_POLICY.md",
    "SAFE_LANGUAGE_LIBRARY.md",
    "AUDIT_POLICY.md",
    "HUMAN_OVERSIGHT_MODEL.md",
    "INCIDENT_RESPONSE.md",
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "DATA_TRUST_ARCHITECTURE.md",
    "TRUST_COMMAND_CENTER.md",
]

APPROVAL_LEVELS = ["A0", "A1", "A2", "A3"]


def check_trust_files() -> tuple[bool, list[str]]:
    trust_dir = REPO_ROOT / "docs" / "trust"
    missing: list[str] = []
    for name in REQUIRED_TRUST_FILES:
        if not (trust_dir / name).exists():
            missing.append(name)
    return (not missing, missing)


def check_approval_matrix_sections() -> tuple[bool, list[str]]:
    matrix = REPO_ROOT / "docs" / "trust" / "APPROVAL_MATRIX.md"
    if not matrix.exists():
        return False, APPROVAL_LEVELS
    text = matrix.read_text(encoding="utf-8")
    missing = [lvl for lvl in APPROVAL_LEVELS if lvl not in text]
    return (not missing, missing)


def main() -> int:
    failures: list[str] = []

    ok_files, missing_files = check_trust_files()
    if ok_files:
        print(f"PASS docs/trust/ — all {len(REQUIRED_TRUST_FILES)} required files present")
    else:
        print(f"FAIL docs/trust/ — missing: {missing_files}")
        failures.append("trust_files")

    ok_matrix, missing_levels = check_approval_matrix_sections()
    if ok_matrix:
        print("PASS APPROVAL_MATRIX.md — A0/A1/A2/A3 all present")
    else:
        print(f"FAIL APPROVAL_MATRIX.md — missing levels: {missing_levels}")
        failures.append("approval_matrix")

    if failures:
        print(f"\nverify_tier0_safety: FAIL ({len(failures)} checks)")
        return 1
    print("\nverify_tier0_safety: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
