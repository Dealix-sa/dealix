#!/usr/bin/env python3
"""
Static check for the V5 launch site (no build required).

Verifies required App-Router routes exist under apps/web/app and that key
commercial pages contain SAR pricing + a safety note and no ROI-guarantee text.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "web" / "app"

REQUIRED_ROUTES = [
    "", "en", "commercial", "services", "pricing", "trust", "launch", "contact",
    "status", "faq", "privacy", "terms", "case-method", "media", "verticals",
    "verticals/facilities-management", "verticals/contracting-project-controls",
    "verticals/real-estate-property-ops", "verticals/legal-professional-services",
    "verticals/consulting-training-b2b",
]

BANNED = re.compile(r"guaranteed roi|guaranteed revenue|guaranteed results", re.IGNORECASE)


def page_path(route: str) -> Path:
    return APP / (route + "/page.tsx" if route else "page.tsx")


def main() -> int:
    errors: list[str] = []
    if not APP.exists():
        print("apps/web/app not found", file=sys.stderr)
        return 1
    for r in REQUIRED_ROUTES:
        if not page_path(r).exists():
            errors.append(f"missing route: /{r}")
    # commercial/pricing must mention SAR
    for r in ("commercial", "pricing"):
        p = page_path(r)
        if p.exists() and "SAR" not in p.read_text(encoding="utf-8"):
            errors.append(f"/{r} missing SAR pricing")
    # no ROI guarantees anywhere in V5 pages
    for r in REQUIRED_ROUTES:
        p = page_path(r)
        if p.exists() and BANNED.search(p.read_text(encoding="utf-8")):
            errors.append(f"/{r} contains an ROI guarantee")
    ok = not errors
    print(f"Site launch static check: {'PASS' if ok else 'FAIL'} ({len(REQUIRED_ROUTES)} routes)")
    for e in errors[:30]:
        print("  !", e)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
