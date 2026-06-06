#!/usr/bin/env python3
"""Dealix CTA-map verifier (Wave 7).

The private-launch funnel is: Home -> Command Sprint -> Start/Diagnostic.
This checks that the core pages exist and route the visitor toward the
single conversion path (Start or Diagnostic). It does not grade copy;
it grades that the path is wired.

Exit 0 = PASS, 1 = FAIL. Pure stdlib.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing"

# Pages that must exist for the funnel to function.
REQUIRED_PAGES = [
    "index.html",
    "command-sprint.html",
    "start.html",
    "diagnostic.html",
    "pricing.html",
    "security.html",
]

# Pages whose primary job is to push to the conversion path.
MUST_LINK_TO_CONVERSION = [
    "index.html",
    "command-sprint.html",
    "pricing.html",
]

CONVERSION_TARGETS = re.compile(r'href="[^"]*(start\.html|diagnostic\.html|command-sprint\.html)"', re.IGNORECASE)

FAILURES: list[str] = []
WARNINGS: list[str] = []


def check_pages_exist() -> None:
    for name in REQUIRED_PAGES:
        if not (LANDING / name).is_file():
            FAILURES.append(f"missing required page: landing/{name}")


def check_conversion_links() -> None:
    for name in MUST_LINK_TO_CONVERSION:
        path = LANDING / name
        if not path.is_file():
            continue  # already reported by check_pages_exist
        html = path.read_text(encoding="utf-8")
        if not CONVERSION_TARGETS.search(html):
            FAILURES.append(
                f"{name}: no CTA linking to start.html / diagnostic.html / command-sprint.html"
            )


def check_command_sprint_offer() -> None:
    """The Command Sprint page must name the offer, the 7-day window,
    and the five deliverables that define it."""
    page = LANDING / "command-sprint.html"
    if not page.is_file():
        return  # reported elsewhere
    html = page.read_text(encoding="utf-8")
    low = html.lower()
    if "command sprint" not in low:
        FAILURES.append("command-sprint.html: does not name the 'Command Sprint' offer")
    if not (re.search(r"7[\s-]*(day|days|أيام|يوم)", html, re.IGNORECASE)):
        WARNINGS.append("command-sprint.html: 7-day window not clearly stated")
    deliverables = ["revenue map", "proof register", "command brief", "action board", "approval register"]
    missing = [d for d in deliverables if d not in low]
    if missing:
        WARNINGS.append(
            "command-sprint.html: deliverables not all named -> " + ", ".join(missing)
        )


def main() -> int:
    print("== Dealix CTA-map verifier ==")
    check_pages_exist()
    check_conversion_links()
    check_command_sprint_offer()

    for w in WARNINGS:
        print(f"  WARN: {w}")
    for f in FAILURES:
        print(f"  FAIL: {f}")

    if FAILURES:
        print(f"\nRESULT: FAIL ({len(FAILURES)} blocker(s), {len(WARNINGS)} warning(s))")
        return 1
    print(f"\nRESULT: PASS ({len(WARNINGS)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
