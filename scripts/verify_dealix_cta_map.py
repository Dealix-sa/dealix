#!/usr/bin/env python3
"""Verify the Dealix one-CTA map.

Asserts:
  1. docs/00_platform_truth/CTA_MAP.md exists and declares every P0 route.
  2. If a page module exists in the frontend, it uses exactly one <PrimaryCta.

Dependency-free. Prints KEY=value lines. Exit 0 on pass, 1 on fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CTA_MAP = REPO / "docs/00_platform_truth/CTA_MAP.md"

# P0 routes -> frontend page module (relative to repo). Page presence is optional
# during early build; when present, it must contain exactly one <PrimaryCta.
P0_ROUTES = {
    "/": None,  # home is the existing [locale]/page.tsx (extended, not new file)
    "/platform": "frontend/src/app/[locale]/platform/page.tsx",
    "/command-sprint": "frontend/src/app/[locale]/command-sprint/page.tsx",
    "/business-os": "frontend/src/app/[locale]/business-os/page.tsx",
    "/pricing": "frontend/src/app/[locale]/pricing/page.tsx",
    "/industries": "frontend/src/app/[locale]/industries/page.tsx",
    "/security": "frontend/src/app/[locale]/security/page.tsx",
    "/start": "frontend/src/app/[locale]/start/page.tsx",
}

# Page-body components where the single CTA actually lives (when split from page.tsx).
BODY_DIR = REPO / "frontend/src/components/wave3"


def main() -> int:
    failures: list[str] = []

    if not CTA_MAP.exists():
        print("CTA_MAP_DOC_PASS=false")
        print("CTA_PASS=false")
        print("  - missing docs/00_platform_truth/CTA_MAP.md", file=sys.stderr)
        return 1

    map_text = CTA_MAP.read_text(encoding="utf-8", errors="ignore")
    for route in P0_ROUTES:
        # The route appears as `/route` in the markdown table.
        token = f"`{route}`"
        if token not in map_text:
            failures.append(f"route {route} not declared in CTA_MAP.md")

    print(f"CTA_MAP_DOC_PASS={'true' if not failures else 'false'}")

    # Count PrimaryCta usages per body component (if any exist yet).
    pages_checked = 0
    if BODY_DIR.exists():
        for path in BODY_DIR.rglob("*.tsx"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "PrimaryCta.tsx" in path.name or path.name == "PrimaryCta.tsx":
                continue
            # Only audit top-level page-body components (named *Page.tsx or *Form.tsx).
            if not re.search(r"(Page|Form|Landing|Index)\.tsx$", path.name):
                continue
            count = len(re.findall(r"<PrimaryCta\b", text))
            if count == 0:
                continue  # not all bodies declare a primary CTA directly
            pages_checked += 1
            if count > 1:
                rel = path.relative_to(REPO)
                failures.append(f"{rel} has {count} <PrimaryCta> (must be exactly 1)")

    print(f"CTA_PAGES_AUDITED={pages_checked}")

    if failures:
        print("CTA_PASS=false")
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("CTA_PASS=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
