"""Verify that operating documents meet the Dealix Document Standard.

Every operating document inside the managed folders below must contain
all eight required sections from ``docs/ops/DOCUMENT_STANDARD.md``.

The list of managed folders is intentionally narrow at the start of the
content-verification stage. As legacy documents are migrated onto the
standard, append their folders here so the verifier expands its
coverage. Verifier output is a TODO list for the founder.
"""

from __future__ import annotations

from pathlib import Path
import sys

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Owner",
    "## Review Cadence",
    "## Inputs",
    "## Outputs",
    "## Rules",
    "## Metrics",
    "## Evidence",
]

MANAGED_FOLDERS = [
    "docs/founder",
    "docs/learning",
    "docs/delivery/revenue_sprint",
]

MANAGED_FILES = [
    "DEALIX_OPERATING_DOCTRINE.md",
    "DEALIX_COMPANY_OS_SCORECARD.md",
    "docs/ops/OPERATING_LOOPS.md",
    "docs/ops/DOCUMENT_STANDARD.md",
    "docs/revenue/OFFER_LADDER.md",
    "docs/revenue/PIPELINE_STAGES.md",
    "docs/trust/APPROVAL_MATRIX.md",
    "docs/trust/AUTONOMY_POLICY.md",
]

SKIP_FILES = {"README.md"}

MIN_BYTES = 400


def collect_paths() -> list[Path]:
    paths: list[Path] = []
    for folder in MANAGED_FOLDERS:
        base = Path(folder)
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            if path.name in SKIP_FILES:
                continue
            paths.append(path)
    for managed_file in MANAGED_FILES:
        path = Path(managed_file)
        if path.exists():
            paths.append(path)
    seen: set[Path] = set()
    deduped: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        deduped.append(path)
    return deduped


def main() -> int:
    failures: list[str] = []

    for folder in MANAGED_FOLDERS:
        if not Path(folder).exists():
            failures.append(f"Missing managed folder: {folder}")

    for managed_file in MANAGED_FILES:
        if not Path(managed_file).exists():
            failures.append(f"Missing managed file: {managed_file}")

    for path in collect_paths():
        text = path.read_text(encoding="utf-8", errors="ignore")

        if path.stat().st_size < MIN_BYTES:
            failures.append(f"Too short ({path.stat().st_size} bytes): {path}")
            continue

        missing = [section for section in REQUIRED_SECTIONS if section not in text]
        if missing:
            failures.append(f"{path} missing sections: {', '.join(missing)}")

    if failures:
        print("Document quality failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: all managed documents meet the Dealix document standard.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
