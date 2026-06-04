#!/usr/bin/env python3
"""Static checks for the website launch readiness (no build, no network).

Verifies SEO infrastructure exists in apps/web, the site-launch copy deck is
present and bilingual, and no exaggerated/guarantee claims appear in the copy.
Read-only.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps" / "web"
SITE_DOCS = ROOT / "docs" / "site-launch"

BANNED_CLAIMS = [
    "guaranteed roi",
    "guaranteed revenue",
    "double your revenue",
    "ضمان عائد",
    "نضمن لك",
    "أرباح مضمونة",
    "100% guaranteed",
    "risk free",
]

SEO_FILES = [
    WEB / "app" / "sitemap.ts",
    WEB / "app" / "robots.ts",
    WEB / "app" / "layout.tsx",
]

REQUIRED_DOCS = [
    SITE_DOCS / "00_SITE_LAUNCH_OS.md",
    SITE_DOCS / "01_PAGE_MAP.md",
    SITE_DOCS / "02_SEO_CHECKLIST.md",
    SITE_DOCS / "03_COPY_DECK_AR_EN.md",
    SITE_DOCS / "04_MANUAL_QA_CHECKLIST.md",
]


def run() -> list[str]:
    errors: list[str] = []

    for f in SEO_FILES:
        if not f.exists():
            errors.append(f"missing SEO file: {f.relative_to(ROOT)}")

    layout = WEB / "app" / "layout.tsx"
    if layout.exists():
        txt = layout.read_text(encoding="utf-8")
        if "metadata" not in txt.lower():
            errors.append("apps/web/app/layout.tsx has no metadata export")

    for f in REQUIRED_DOCS:
        if not f.exists():
            errors.append(f"missing site-launch doc: {f.relative_to(ROOT)}")

    copy_deck = SITE_DOCS / "03_COPY_DECK_AR_EN.md"
    if copy_deck.exists():
        text = copy_deck.read_text(encoding="utf-8").lower()
        for claim in BANNED_CLAIMS:
            if claim in text:
                errors.append(f"copy deck contains banned claim: '{claim}'")
        # Require meaningful Arabic content (presence of Arabic Unicode block).
        arabic_chars = sum(1 for ch in text if "؀" <= ch <= "ۿ")
        if arabic_chars < 50:
            errors.append("copy deck appears to be missing an Arabic section")

    return errors


def main() -> int:
    errors = run()
    if not errors:
        print(
            "Site launch static check PASS — SEO files present, copy deck bilingual & claim-safe."
        )
        return 0
    print("Site launch static check FAIL:")
    for e in errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
