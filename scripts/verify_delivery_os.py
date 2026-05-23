#!/usr/bin/env python3
"""verify_delivery_os.py — Delivery OS structural checks per offer."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "docs/delivery/DELIVERY_QUALITY_STANDARD.md",
    # Sprint
    "docs/delivery/revenue_sprint/OFFER.md",
    "docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md",
    "docs/delivery/revenue_sprint/CLIENT_INTAKE.md",
    "docs/delivery/revenue_sprint/REPORT_TEMPLATE.md",
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
    "docs/delivery/revenue_sprint/HANDOFF_TEMPLATE.md",
    "docs/delivery/revenue_sprint/CASE_STUDY_CAPTURE.md",
    # Managed Pilot
    "docs/delivery/managed_pilot/OFFER.md",
    "docs/delivery/managed_pilot/DELIVERY_PLAYBOOK.md",
    # Revenue Desk
    "docs/delivery/revenue_desk/OFFER.md",
    "docs/delivery/revenue_desk/DELIVERY_PLAYBOOK.md",
]

REQUIRED_OFFER_KEYWORDS = ["Price", "Time", "Trust"]
# Each OFFER.md must have at least 2 "## Scope (...)" headings — one for in-scope
# and one for out-of-scope. We don't constrain the parenthesized label so that
# offers can use clarifications like `Scope (per month, in)`.
_SCOPE_HEADING = re.compile(r"^##\s+Scope\s*\(", re.MULTILINE)


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (REPO_ROOT / rel).exists():
            failures.append(f"missing file: {rel}")

    for offer_path in REPO_ROOT.glob("docs/delivery/*/OFFER.md"):
        text = offer_path.read_text(encoding="utf-8")
        rel = offer_path.relative_to(REPO_ROOT)
        for keyword in REQUIRED_OFFER_KEYWORDS:
            if keyword not in text:
                failures.append(f"{rel}: missing '{keyword}' section/heading")
        scope_headings = _SCOPE_HEADING.findall(text)
        if len(scope_headings) < 2:
            failures.append(
                f"{rel}: needs at least 2 '## Scope (...)' sections (in/out); "
                f"found {len(scope_headings)}"
            )

    if failures:
        print("Delivery OS verification FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("Delivery OS verification OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
