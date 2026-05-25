"""Verify Tier-2 (Delivery) factory + QA gate are in place."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FACTORY_DOC = (
    REPO_ROOT / "docs" / "delivery" / "revenue_sprint" / "REVENUE_SPRINT_FACTORY.md"
)
QA_DOC = REPO_ROOT / "docs" / "offers" / "revenue_sprint" / "qa_checklist.md"

FACTORY_REQUIRED_SECTIONS = (
    "## Inputs",
    "## Day-by-day",
    "## QA gate",
    "## Hand-off",
    "## Operating constraints",
)

QA_REQUIRED_SECTIONS = (
    "## Accuracy",
    "## Scope",
    "## Tone",
    "## Safety",
    "## Format",
    "## Sign-off",
)


def _check_doc(path: Path, sections: tuple[str, ...]) -> list[str]:
    if not path.exists():
        return [f"Missing: {path.relative_to(REPO_ROOT)}"]
    body = path.read_text(encoding="utf-8")
    return [f"Section missing in {path.name}: {s}" for s in sections if s not in body]


def main() -> None:
    print("== Tier 2 — Delivery Factory + QA ==")
    failures = _check_doc(FACTORY_DOC, FACTORY_REQUIRED_SECTIONS)
    failures += _check_doc(QA_DOC, QA_REQUIRED_SECTIONS)
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print("PASS: Tier 2 delivery factory + QA verified.")


if __name__ == "__main__":
    main()
